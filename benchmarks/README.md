# Benchmarking

Benchmarking construction of values with raw `float`s, `Fraction` (kuchka's actual storage type), `Decimal` (kuchka's display materialization), `kuchka`'s own objects, and some operations.

## Introduction

`kuchka`'s own design choice is `Fraction`, not `float` (see the README).
Every magnitude is stored as an exact rational number, and `Decimal` only re-enters the picture at display time, via `to_decimal()` inside `__repr__`/`__format__`.
The point of this benchmarking is to show where construction cost actually comes from - the `Fraction` conversion itself, not the class/`@overload` machinery wrapped around it - and to keep that separate from the unrelated cost of materializing a `Decimal` for display.

Cases:

1. Raw float arithmetic -- the floor, no correctness guarantees at all.
2. `Fraction` construction alone (`Fraction(x) * scale`, same `int` input as case 4 so the two isolate the same layer) -- the cost `kuchka` inherits from its own design choice, independent of `kuchka`.
3. `to_decimal` alone (`Decimal(numerator) / Decimal(denominator)`) -- the cost of materializing a value for display, which never runs during construction or arithmetic.
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
  platform: Linux-6.18.47-1-lts-x86_64-with-glibc2.44
  machine:  x86_64
  decimal:  decimal
```

| Case                                                                | us/sample |   MSa/s |
| ------------------------------------------------------------------- | --------: | ------: |
| raw float divide (no correctness guarantees)                        |    0.0162 | 61.5659 |
| Fraction(x) \* scale (kuchka's own construction cost, no wrapper)   |    0.9183 |  1.0890 |
| to_decimal(Fraction) (kuchka's display/repr cost, not construction) |    0.2385 |  4.1922 |
| Millivolt(x): a single kuchka construction                          |    1.4966 |  0.6682 |
| Millivolt(x) over a batch of 1000 raw readings                      |    1.4777 |  0.6767 |
| Voltage + Voltage (steady-state hot-loop addition)                  |    0.9918 |  1.0082 |
| Voltage / Current -> Resistance (Ohm's law, one division)           |    2.7661 |  0.3615 |

## Conclusion

The wrapper/class machinery is not the bottleneck: `Fraction` construction is roughly half the cost of a single `Millivolt(x)` call, and the class/`@overload` wrapper accounts for the other half.

Materializing a `Decimal` for display is cheap and, importantly, only happens on `repr()`/`__format__` -- construction and arithmetic never touch `Decimal` at all, since storage and arithmetic stay in `Fraction` end to end.

Division is the expensive outlier -- it goes through the dimension-exponent-vector `_promote` path and a registry lookup, not just scaling.

Batch construction over a Python list doesn't meaningfully beat single-call construction. In itself this is not surprising -- no vectorized path exists yet.
