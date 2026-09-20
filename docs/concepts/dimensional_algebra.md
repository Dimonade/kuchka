# Dimensional algebra and derived quantities

`kuchka` represents physical dimensions as exponent vectors and uses those vectors for runtime arithmetic.

The arithmetic engine is generic.
A product or quotient is reduced to a resulting dimension, and the registry determines whether that dimension has a named engineering quantity.

Examples of registered relationships include:

```text
Voltage * Current              -> Power
Mass * Acceleration            -> Force
Force / Area                   -> Pressure
Pressure * Volume              -> Energy
Mass / Volume                 -> Density
Length * Length                -> Area
Area * Length                 -> Volume
Resistance^-1                 -> Conductance
Time^-1                        -> Frequency
SamplingPeriod^-1              -> SampleRate
```

## Type-checker support

The runtime engine can derive arbitrary dimensions, but static type checkers cannot infer a semantic mapping such as `Voltage * Current -> Power` from exponent arithmetic alone.
`kuchka` therefore maintains explicit overloads for registered derived quantities.

This keeps arithmetic visible to mypy and ty while retaining a general runtime model.

## Unrepresentable dimensions

A mathematically valid dimension does not automatically become a public quantity type.
`Resistance * Resistance`, for example, raises `UnrepresentableDimensionError` because the resulting dimension has no registered engineering type.

If a dimension is deliberately planned for a future release, the more specific `PlannedDimensionError` names that scope gap.

See the repository example [Working around an unrepresentable intermediate dimension](../examples/unrepresentable_dimensions/README.md) for an application-level pattern using `.magnitude` only at the unrepresentable intermediate step.

## Same physical dimension, different concepts

`Frequency`, `SampleRate`, and `BaudRate` all have physical dimension T^-1, but they are intentionally separate concepts.

```python
Hertz(50) + SamplesPerSecond(50)
# rejected
```

Canonical generic arithmetic produces the canonical type for a dimension.
Domain-specific types remain available by explicit construction.

Genuine reciprocal pairs retain reciprocal behavior:

```python
rate = 1 / SecondSamplingPeriod(2)  # SampleRate
period = 1 / rate                    # SamplingPeriod
```

`BaudRate` has no automatic reciprocal relationship because baud counts symbols per second as symbols per second, not cycles or bits.
