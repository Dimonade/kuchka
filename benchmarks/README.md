# Benchmarking

Benchmarking construction of values with raw `float`s, `Decimal`s, `kuchka`'s objects and some oprations.

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