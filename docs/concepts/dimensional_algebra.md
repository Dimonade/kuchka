# Dimensional algebra and derived quantities

`kuchka` represents physical dimensions as exponent vectors and uses those vectors for runtime arithmetic.

The arithmetic engine is generic.
A product or quotient is reduced to a resulting dimension, and the registry determines whether that dimension has a named engineering quantity.

Examples of registered relationships include:

```text
Voltage * Current   -> Power
Mass * Acceleration -> Force
Force / Area        -> Pressure
Pressure * Volume   -> Energy
Mass / Volume       -> Density
Length * Length     -> Area
Area * Length       -> Volume
1 / Resistance      -> Conductance
1 / Time            -> Frequency
```

## The registry is closed

The set of named dimensions belongs to the library.
Each quantity module registers its type while `kuchka` is imported, and the registry closes when that import finishes, so every arithmetic result is one of the library's own types and the same expression gives the same type in every program.
The registration function is internal (`kuchka.quantities.base.registry._register`), and calling it after the import raises `RuntimeError`.
A dimension has one registered type, the general SI name for it (`Frequency` for T⁻¹), and a second type that shares the dimension, such as `SampleRate`, is reached by constructing it explicitly.

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

`Frequency`, `SampleRate`, and `BaudRate` all have physical dimension T⁻¹, but they are intentionally separate concepts.

```python
from kuchka import Hertz
from kuchka import SamplesPerSecond

Hertz(50) + SamplesPerSecond(50)  # rejected: `IncompatibleDimensionError`.
```

Canonical generic arithmetic produces the canonical type for a dimension.
Domain-specific types remain available by explicit construction, and stay the domain type even through a reciprocal:

```python
from kuchka import Frequency
from kuchka import SampleRate
from kuchka import Second

rate = 1 / Second(2).as_sampling_period()

isinstance(rate, SampleRate)
# True
isinstance(rate, Frequency)
# False
```

`BaudRate` has no automatic reciprocal relationship because baud counts symbols per second, not bits or cycles.
