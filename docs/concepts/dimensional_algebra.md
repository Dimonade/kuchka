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
`Frequency`, `BaudRate`, `SampleRate`, and `Activity` share the dimension T⁻¹, and each has its own units: the hertz, the baud, the sample per second, and the becquerel.
`AbsorbedDose` and `EquivalentDose` share L²T⁻² with `SpecificEnergy`, with the gray and the sievert as their units and the rad and the rem as their older ones.
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

| Relation       | Meaning                                                                            | Example                                                                                        |
| -------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| principal      | the one linear kind arithmetic produces for a dimension with extent                | `Frequency` for T⁻¹                                                                            |
| specialisation | a role of a kind of the same dimension and shape, reached by explicit construction | `SampleRate` and `BaudRate` of `Frequency`, `ApparentPower` of `Power`, `Stress` of `Pressure` |
| contested      | linear kinds on equal footing, so the dimension has no principal                   |                                                                                                |

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

## The solid angle axis

`Dimension` counts solid angle as an axis of its own, so luminous flux is luminous intensity times solid angle and illuminance is flux per area.
That separates the lumen from the candela, which have the same dimension in SI's base-quantity accounting, where the steradian is a square metre per square metre.

The axis is not the square of the angle axis, because a solid angle is not the product of two plane angles: `AngularDisplacement * AngularDisplacement` has no registered type.
It is not reached by cancelling areas either, because `Area / Area` is a `Proportion`.
A `SolidAngle` comes from a constructor, or from `SolidAngle.from_area(area, radius)`, the area an object cuts from a sphere over the radius squared.

The steradian is the canonical solid angle, so a candela steradian is a lumen and a lumen per square metre is a lux, with no factor between them.
Only the square degree and its relatives, which are the angle units squared, carry pi.
`Candela * Steradian` is a `LuminousFlux`, `LuminousFlux / Area` an `Illuminance`, and `LuminousFlux * Time` a `LuminousEnergy`, which `/ Area` turns into a `LuminousExposure`.
`LuminousIntensity / Area` is a `Luminance`, which has no solid angle in it, and `LuminousFlux / Power` is a `LuminousEfficacy`.

## The information axis

`Dimension` counts information as an axis of its own, so data is a dimension and a data rate is data per time.
That keeps `Data` apart from `Proportion`, which is dimensionless, and `DataRate` apart from `Frequency`, `SampleRate`, and `BaudRate`, which share T⁻¹.

`Data` counts bits, and the bit is its canonical unit.
`Data / Time` is a `DataRate`, `DataRate * Time` is `Data`, and the quotient of two `Data` values is a `Proportion`, the way `Current * Time` is a `Charge`:

```python
from kuchka import Gibibyte
from kuchka import Hertz
from kuchka import Kibibyte
from kuchka import Megabit
from kuchka import MegabitPerSecond
from kuchka import Second

Gibibyte(4) / Second(10)  # a DataRate
MegabitPerSecond(100) * Second(10) == Megabit(1000)  # a Data
Gibibyte(4) / MegabitPerSecond(100)  # a Time
Hertz(1000) * Kibibyte(4)  # a DataRate
MegabitPerSecond(100) + Hertz(1)  # rejected: `IncompatibleDimensionError`.
```

The SI prefixes count in thousands and the IEC binary prefixes in powers of 1024, so `Kilobyte(1)` is 1000 bytes, `Kibibyte(1)` is 1024 bytes, and the two never compare equal.
Spellings follow the same split: `kB` and `KiB` resolve, and `KB` is refused.

## Choosing the result type

The type of a product or quotient is decided in this order:

1. A ratio of like quantities is a `Proportion`: the quotient of two quantities of one dimension, and the product or quotient of two proportions.
2. Any other dimensionless result is a plain `Fraction`: `Hertz(2) * Second(3)` counts cycles.
3. A dimensionless operand, a `Proportion`, keeps the kind of the other operand: `SampleRate(...) * Percent(50)` is a `SampleRate`.
4. A rule for the operand kinds names the kind, for a dimension that has several linear kinds: `Pressure` and `EnergyDensity` share M L⁻¹ T⁻², so `Force / Area` is a `Pressure` and `Energy / Volume` an `EnergyDensity`.
   A bridge is a rule whose result differs from the plain product on the angle axis alone, described in [Where the radian meets a length](angle_bridges.md).
5. Otherwise the principal kind of the dimension is the result, and a contested dimension raises `AmbiguousKindError`.

A specialisation is checked before any of those.
It combines with a plain number, with a `Proportion`, with itself in a quotient, and with its reciprocal: `SampleRate` times `SamplingPeriod` is a `Fraction`.
Any other operand is refused, and the error names the conversion that leaves the role:

```python
from kuchka import Baud
from kuchka import Metre
from kuchka import SamplesPerSecond
from kuchka import Second

Baud(9600) * Metre(1)  # rejected: `IncompatibleDimensionError`.
SamplesPerSecond(48_000) * Second(2)  # rejected: `IncompatibleDimensionError`.
SamplesPerSecond(48_000).to_frequency() * Second(2) == 96_000
```

## Powers

A linear quantity raised to an integer power is the product written out, so `side ** 3` is `side * side * side`, and each step is a product the registry gives a type:

```python
from kuchka import Metre
from kuchka import MetrePerSecond
from kuchka import Ratio
from kuchka import Second
from kuchka import SquareMetre

Metre(3) ** 2 == SquareMetre(9)
type(MetrePerSecond(3) ** 2).__name__ == "VelocitySquared"
Second(2) ** -1  # a Frequency of 0.5 Hz
Metre(3) ** 0 == Ratio(1)
```

A negative exponent gives the reciprocal of the positive power, and an exponent is an `int`.
Type checkers see the square and the cube of a type whose power has a type of its own.

## Ratios

A ratio is a `Proportion`, and it displays as the coherent ratio:

```python
from kuchka import Hertz, Percent, Ratio, Second, Volt

gain = Volt(5) / Volt(2)
gain == Ratio(2.5)
Percent(50) * Percent(50) == Ratio(0.25)
Hertz(2) * Second(3) == 6  # Cycles are a plain `Fraction`.
```

A `Proportion` scales a quantity and keeps its type, and over a quantity it is the reciprocal:

```python
from kuchka import Hertz
from kuchka import Percent
from kuchka import Ratio
from kuchka import Second
from kuchka import Volt

Percent(50) * Volt(2) == Volt(1)
Volt(2) / Percent(50) == Volt(4)
Ratio(2) / Second(4) == Hertz(0.5)
```

A `Proportion` compares with a `Proportion`, and a quantity is not built from one.
`.magnitude` is the exact `Fraction` when a plain number is what is wanted:

```python
gain > Ratio(2)
gain > 2  # rejected: `IncompatibleDimensionError`.
Volt(gain)  # rejected: `InvalidMeasurementError`.
Volt(gain.magnitude) == Volt(2.5)
```

## Converting between types

`.to(unit)` changes the unit a value is shown in and leaves the type alone.
A conversion between types is a named method: `to_x()` on the value, or `from_x()` on the class.
`Millisecond(2).to_sampling_period()`, `SampleRate.to_frequency()`, and `Decibel(30).to_power_ratio()` are in the first form, and `LogarithmicRatio.from_power_ratio(ratio)` is in the second.
A conversion that has a domain raises `InvalidMeasurementError` outside it, and its docstring says so; `from_power_ratio(Ratio(0))` has no logarithm to return.

## Type-checker support

The runtime engine can derive arbitrary dimensions, but static type checkers cannot infer a semantic mapping such as `Voltage * Current -> Power` from exponent arithmetic alone.
`kuchka` therefore declares explicit overloads for registered derived quantities, generated from the same registry the runtime uses.

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
