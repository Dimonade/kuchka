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
Energy / Volume     -> EnergyDensity
Mass / Volume       -> Density
Length * Length     -> Area
Area * Length       -> Volume
1 / Resistance      -> Conductance
1 / Time            -> Frequency
```

## Units belong to quantity types

A quantity type displays in the units of its own `*_UNITS` table, and in no unit of another type, even one with the same dimension.
`Frequency`, `BaudRate`, and `SampleRate` share the dimension T⁻¹, and each has its own units: the hertz, the baud, and the sample per second.
`Hertz(1).to(BAUD)` raises `InvalidConversionError`, and `Frequency(Fraction(1), BAUD)` raises `InvalidMeasurementError`, and both name the type the unit belongs to.
A unit can belong to several types: the second is a unit of `Time` and of `SamplingPeriod`.

Moving a value between quantity types is a separate, explicit step, such as `SampleRate.to_frequency()`.

## The registry is closed

The set of named dimensions belongs to the library.
Each quantity module registers its type while `kuchka` is imported, and the registry closes when that import finishes, so every arithmetic result is one of the library's own types and the same expression gives the same type in every program.
The registration function is internal (`kuchka.quantities.base.registry._register`), and calling it after the import raises `RuntimeError`.
A type is a kind of its dimension, whatever its shape (linear, affine, modular, or logarithmic), and several kinds can share one dimension.
Every concrete quantity type is in the catalogue of kinds, which records which kinds exist and never decides what arithmetic returns.

Arithmetic produces linear kinds only, so the rules that choose its result type look only at the linear kinds of a dimension with extent.
The first such kind is the principal one, and a later one states its relation to the kinds already there:

| Relation       | Meaning                                                                            | Example                                    |
| -------------- | ---------------------------------------------------------------------------------- | ------------------------------------------ |
| principal      | the one linear kind arithmetic produces for a dimension with extent                | `Frequency` for T⁻¹                        |
| specialisation | a role of a kind of the same dimension and shape, reached by explicit construction | `SampleRate` and `BaudRate` of `Frequency` |
| contested      | linear kinds on equal footing, so the dimension has no principal                   |                                            |

`Time` and `Instant`, `Angle` and a linear angular quantity, `Proportion` and `LogarithmicRatio` can share a dimension without a relation, because arithmetic never has to choose between them.
A specialisation records meaning and shape: it converts no value and picks no result.
A result whose dimension is contested raises `AmbiguousKindError`, naming the candidates.
`kuchka` does not finish importing while a concrete quantity type is unregistered, and a second linear kind that states no relation is refused.

## The angle axis

`Dimension` counts angle as an axis of its own, so torque is energy per angle and angular velocity is angle per time.
That separates torque from energy and angular velocity from the hertz, which have the same dimension in SI's base-quantity accounting.

`Angle` is a position on a circle: 370 degrees is 10 degrees, so it wraps and takes no part in arithmetic.
`AngularDisplacement` is the angle swept, which does not wrap, and it multiplies and divides: `Torque * AngularDisplacement` is an `Energy`, and `AngularDisplacement / Time` is an `AngularVelocity`.
`Angle.to_angular_displacement()` and `AngularDisplacement.to_angle()` move between them, and `Frequency.to_angular_velocity()` and `AngularVelocity.to_frequency()` between cycles and angle.
`Torque.from_force(force, lever_arm)` builds a torque from a force at a distance, where `Force * Length` is an `Energy`.

Turn is the canonical angle, so the canonical units are the turn, the turn per second, and the joule per turn, and a radian enters as the exact factor `1 / (2 pi)`.
Arithmetic results display in the radian, the radian per second, and the newton-metre.

## Choosing the result type

The type of a product or quotient is decided in this order:

1. A dimensionless result is a plain `Fraction`.
2. A dimensionless operand, a `Proportion`, keeps the kind of the other operand: `SampleRate(...) * Percent(50)` is a `SampleRate`.
3. A rule for the operand kinds names the kind, for a dimension that has several linear kinds: `Pressure` and `EnergyDensity` share M L⁻¹ T⁻², so `Force / Area` is a `Pressure` and `Energy / Volume` an `EnergyDensity`.
4. Otherwise the principal kind of the dimension is the result, and a contested dimension raises `AmbiguousKindError`.

## Converting between types

`.to(unit)` changes the unit a value is shown in and leaves the type alone.
A conversion between types is a named method: `to_x()` on the value, or `from_x()` on the class.
`Millisecond(2).to_sampling_period()`, `SampleRate.to_frequency()`, and `Decibel(30).to_power_ratio()` are in the first form, and `LogarithmicRatio.from_power_ratio(ratio)` is in the second.
A conversion that has a domain raises `InvalidMeasurementError` outside it, and its docstring says so; `from_power_ratio(Ratio(0))` has no logarithm to return.

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

rate = 1 / Second(2).to_sampling_period()

isinstance(rate, SampleRate)
# True
isinstance(rate, Frequency)
# False
```

`BaudRate` has no automatic reciprocal relationship because baud counts symbols per second, not bits or cycles.
