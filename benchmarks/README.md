# Benchmarking

Benchmarking construction of values with raw `float`s, `Fraction` (`kuchka`'s actual storage type), `kuchka`'s own objects, and the neighbouring operations: reading text, displaying, and arithmetic.

## Introduction

`kuchka`'s own design choice is `Fraction`, not `float` (see the README).
Every magnitude is stored as an exact rational number, and `Decimal` only re-enters the picture where a value is read from text, displayed, or taken through a logarithm.
The point of this benchmarking is to show where construction cost comes from - the `Fraction` conversion itself, and the class machinery wrapped around it - and what the operations around a construction cost in comparison.

Cases:

1. Raw float arithmetic -- the floor, no correctness guarantees at all.
2. `Fraction` construction alone (`Fraction(x) * scale`, same `int` input as case 3 so the two isolate the same layer) -- the cost `kuchka` inherits from its own design choice, independent of `kuchka`.
3. A single `kuchka` constructor call (`Millivolt(x)`) -- construction cost, what a boundary layer pays once per raw reading.
4. A batch of `kuchka` constructor calls over a list -- the realistic shape of translating a burst of acquisition samples, not just one call in isolation.
5. `parse("2350 mV", Voltage)` -- reading a value from text, as a configuration file or a command line delivers it.
6. `repr` of a quantity -- the cost of displaying a value.
7. Arithmetic on already-constructed quantities that keeps the dimension (`+`, `<`) -- the steady-state cost once inside the measurement domain, which is what dominates a hot loop that does more than one operation per sample.
8. Arithmetic that changes the dimension (`*`, `/`) -- the same, for products and ratios such as Ohm's law.

## Method

Each case runs enough executions to fill at least 0.2 s and is timed 7 times.
The table reports the best repeat, because it is the one least disturbed by the rest of the machine, and `spread` is the median repeat over the best one, minus one.
A spread near zero means the figure reproduces; the script flags any row above 5 %.
Every timing includes the loop of the timer itself, 6.1 ns per iteration here, which is about half of the raw float row.

## Results

Run it with

```sh
uv run python benchmarks/construction.py
```

and with `--profile` to see where the time of one construction goes, per function.

```text
environment:
  python:   3.11.16 (CPython)
  platform: Linux-6.18.62-1-lts-x86_64-with-glibc2.44
  machine:  x86_64
  decimal:  decimal
  kuchka:   /home/dimonade/repositories/kuchka/src/kuchka/__init__.py
  method:   best of 7 repeats, each at least 0.2 s
  loop:     6.1 ns per empty iteration
```

| Case                                                              | us/sample |   MSa/s | spread |
| ----------------------------------------------------------------- | --------: | ------: | -----: |
| raw float divide (no correctness guarantees)                      |    0.0145 | 69.2011 |   2.2% |
| Fraction(x) \* scale (kuchka's own construction cost, no wrapper) |    0.8519 |  1.1738 |   0.3% |
| Millivolt(x): a single kuchka construction                        |    2.8187 |  0.3548 |   0.1% |
| Millivolt(x) over a batch of 1000 raw readings                    |    2.8741 |  0.3479 |   0.1% |
| parse("2350 mV", Voltage): reading a value from text              |    7.9880 |  0.1252 |   0.1% |
| repr(Millivolt): display cost, not construction                   |    3.8490 |  0.2598 |   0.2% |
| Voltage + Voltage (steady-state hot-loop addition)                |    1.9597 |  0.5103 |   0.3% |
| Voltage < Voltage (a threshold check)                             |    0.3396 |  2.9447 |   0.5% |
| Voltage \* Current -> Power (one multiplication)                  |    5.1116 |  0.1956 |   0.3% |
| Voltage / Current -> Resistance (Ohm's law, one division)         |    5.3796 |  0.1859 |   0.8% |

## Conclusion

A single `Millivolt(x)` costs 2.82 us.
The `Fraction` conversion accounts for 0.85 us of that, about 30 %, and the class machinery around it for the remaining 1.97 us, about 70 %.
Against a raw float divide, which does no checking at all, a construction costs nearly 200 times as much.

Batch construction over a Python list costs almost the same per value as a single call (2.87 us against 2.82 us), since no vectorized path exists yet.

Reading a value from text with `parse` costs 7.99 us, about 2.8 times a construction.
Displaying a value costs 3.85 us, about 1.4 times a construction.
Construction and arithmetic never touch `Decimal`, since storage and arithmetic stay in `Fraction` end to end; `parse` and `repr` are where it comes in.

Arithmetic that keeps the dimension is cheap: an addition costs 1.96 us and a comparison 0.34 us, the cheapest `kuchka` operation measured.
Arithmetic that changes the dimension costs more than twice an addition: a multiplication costs 5.11 us and a division 5.38 us, because both go through the dimension-exponent-vector `_promote` path and a registry lookup, not just scaling.

On one core that is about 355,000 constructions, 510,000 additions, 196,000 multiplications, or 186,000 divisions per second, and 2.9 million comparisons.
That serves configuration, reporting, and control loops at kilohertz rates.
An acquisition path in the MSa/s range keeps raw floats inside it and builds quantities where the values leave it.
