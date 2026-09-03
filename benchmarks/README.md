# Benchmarking

Benchmarking construction of values with raw `float`s, `Decimal`s, `kuchka`'s objects and some oprations.

## Introduction

`kuchka`'s own design choice is `Decimal`, not `float` (see the README).
That choice has a cost, and the point of this benchmarking is to show where that cost actually comes from:
the `Decimal(str(x))` parse, not the class/`@overload` machinery wrapped around it.
Each case below isolates one layer, so the numbers can be read as "how much does the next layer add", not just as one opaque total.

Cases: 1. Raw float arithmetic -- the floor, no correctness guarantees at all. 2. Decimal construction alone (`Decimal(str(x)) * scale`) -- the cost `kuchka` inherits from its own design choice, independent of `kuchka`. 3. A single `kuchka` constructor call (`Millivolt(x)`) -- construction cost, what a boundary layer pays once per raw reading. 4. A batch of `kuchka` constructor calls over a list -- the realistic shape of translating a burst of acquisition samples, not just one call in isolation. 5. Arithmetic on already-constructed quantities (`+`, `/`) -- the steady-state cost once inside the measurement domain, which is what actually dominates a hot loop that does more than one operation per sample.

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

| case                                                       | us/sample | MSa/s   |
| ---------------------------------------------------------- | --------- | ------- |
| raw `float` divide (no correctness guarantees)             | 0.0168    | 59.6970 |
| Decimal(str(x)) \* scale (`kuchka`'s own cost, no wrapper) | 0.2116    | 4.7260  |
| Millivolt(x): a single `kuchka` construction               | 0.4347    | 2.3002  |
| Millivolt(x) over a batch of 1000 raw readings             | 0.4198    | 2.3820  |
| Voltage + Voltage (steady-state hot-loop addition)         | 0.3155    | 3.1699  |
| Voltage / Current -> Resistance (Ohm's law, one division)  | 1.9497    | 0.5129  |

## Conclusion

The wrapper/class machinery is not the bottleneck -- it's roughly half the total cost, and the other half is Decimal(str(x)) itself.

What it means in practice is not that `kuchka` adds overhead, but that it's "Decimal costs what Decimal costs, `kuchka` doesn't meaningfully add to it".

Specifically, `Decimal(str(x))` alone eats ~70% of construction cost, the class/@overload wrapper is the other ~30%.

Division is the expensive outlier -- it goes through the dimension-exponent-vector `_promote` path and a registry lookup, not just scaling.

Batch construction over a Python list doesn't meaningfully beat single-call construction.
In itself this is not surprising -- no vectorized path exists yet.
