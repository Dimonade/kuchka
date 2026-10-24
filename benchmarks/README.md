# Benchmarking

Benchmarking construction of values with raw `float`s, `Fraction` (kuchka's actual storage type), `Decimal` (kuchka's display materialization), `kuchka`'s own objects, and some operations.

## Introduction

`kuchka`'s own design choice is `Fraction`, not `float` (see the README).
Every magnitude is stored as an exact rational number, and `Decimal` only re-enters the picture where a value is displayed or a logarithm is taken.
The point of this benchmarking is to show where construction cost comes from - the `Fraction` conversion itself, and the class machinery wrapped around it - and to keep that separate from the unrelated cost of materializing a `Decimal` for display.

Cases:

1. Raw float arithmetic -- the floor, no correctness guarantees at all.
2. `Fraction` construction alone (`Fraction(x) * scale`, same `int` input as case 4 so the two isolate the same layer) -- the cost `kuchka` inherits from its own design choice, independent of `kuchka`.
3. `to_decimal` alone (`Decimal(numerator) / Decimal(denominator)`) -- the cost of turning one `Fraction` into a `Decimal`, which never runs during construction or arithmetic.
4. A single `kuchka` constructor call (`Millivolt(x)`) -- construction cost, what a boundary layer pays once per raw reading.
5. A batch of `kuchka` constructor calls over a list -- the realistic shape of translating a burst of acquisition samples, not just one call in isolation.
6. Arithmetic on already-constructed quantities (`+`, `/`) -- the steady-state cost once inside the measurement domain, which is what actually dominates a hot loop that does more than one operation per sample.

## Results

Run it with

```sh
uv run python benchmarks/construction.py
```

```text
environment:
  python:   3.11.16 (CPython)
  platform: Linux-6.18.54-1-lts-x86_64-with-glibc2.44
  machine:  x86_64
  decimal:  decimal
```

| Case                                                              | us/sample |   MSa/s |
| ----------------------------------------------------------------- | --------: | ------: |
| raw float divide (no correctness guarantees)                      |    0.0144 | 69.3443 |
| Fraction(x) \* scale (kuchka's own construction cost, no wrapper) |    1.0951 |  0.9132 |
| to_decimal(Fraction) (a Fraction as a Decimal, not construction)  |    0.2881 |  3.4716 |
| Millivolt(x): a single kuchka construction                        |    2.9392 |  0.3402 |
| Millivolt(x) over a batch of 1000 raw readings                    |    2.9234 |  0.3421 |
| Voltage + Voltage (steady-state hot-loop addition)                |    2.0158 |  0.4961 |
| Voltage / Current -> Resistance (Ohm's law, one division)         |    5.6172 |  0.1780 |

## Conclusion

A single `Millivolt(x)` costs 2.94 us.
The `Fraction` conversion accounts for 1.10 us of that, about 37 %, and the class machinery around it (input validation, unit binding, and the immutable store) for the remaining 1.84 us, about 63 %.
Against a raw float divide, which does no checking at all, a construction costs about 200 times as much.

Construction and arithmetic never touch `Decimal`, since storage and arithmetic stay in `Fraction` end to end.
Turning one `Fraction` into a `Decimal` costs 0.29 us, a tenth of a construction.

Addition of two quantities costs 2.02 us.
Division is the expensive outlier at 5.62 us, 2.8 times an addition: it goes through the dimension-exponent-vector `_promote` path and a registry lookup, not just scaling.

Batch construction over a Python list costs the same per value as a single call (2.92 us against 2.94 us), since no vectorized path exists yet.

On one core that is about 340,000 constructions, 500,000 additions, or 180,000 divisions per second.
That serves configuration, reporting, and control loops at kilohertz rates.
An acquisition path in the MSa/s range keeps raw floats inside it and builds quantities where the values leave it.
