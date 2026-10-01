# Changelog

All notable changes to kuchka are documented here.

The format tries to follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
See the `Stability` section in `README.md` for what versioning means before `0.2.0`.

## [0.1.4] - `develop`

### Added

#### Temperature gets `Fahrenheit`

`Fahrenheit`, and the usual `Fahrenheit(32) == Celsius(0)`, `Fahrenheit(-459.67) == Kelvin(0)`.

#### Electrical families got more units

- `Current` family gets new units: `Picoampere`, `Nanoampere`, and `Megaampere`.
- `Resistance` family gets new units: `Microohm` and `Gigaohm`.
- `Conductance` family gets a new unit: `Nanosiemens`.
- `Voltage` family gets new units: `Nanovolt`, `Megavolt`, and `Petavolt`.

#### `LogarithmicRatio`, the first logarithmic quantity

- `Decibel` and `Bel` constructors, with `LOGARITHMIC_RATIO_UNITS`.
- `PureLogarithmicQuantity`, the base for a ratio expressed as a logarithm, and `LogarithmicUnitDef`, the unit-definition type for it.
- Levels add, subtract, scale by a plain number, negate, take `abs()`, and compare, all exactly.
- `as_power_ratio()` / `as_field_ratio()` and `from_power_ratio()` / `from_field_ratio()` convert to and from a linear `Proportion`.
  They are evaluated in `Decimal` at the active context precision; whole multiples of 10 dB (power) or 20 dB (field) are exact.

### Fixed

#### Quantity class constructors validate their arguments

- `Voltage`, `Temperature`, `Angle`, `LogarithmicRatio`, and every other quantity class are exported for annotations and `isinstance`, but their own constructors used to store whatever they were given.
- `Voltage(0.5, AMPERE)` kept a raw `float` and a unit of the wrong dimension, which defeated the exact-`Fraction` guarantee and failed later, far from the cause, with an unrelated `AttributeError`.
- The class constructors now accept only an exact `Fraction` magnitude (in the quantity's canonical unit) and a display unit of the right kind and dimension, and raise `InvalidMeasurementError` otherwise.

*NOTE:* This changes nothing for code that builds values through the unit constructors (`Volt(5)`, `Celsius(20)`, ...), which is the supported way to do it.

#### A quantity keeps the state it was built with

A quantity's magnitude and display unit are written once, when it is built or restored, and cannot change afterwards.
Deleting an attribute, calling `__init__` again, and calling `__setstate__` on a live value all raise `AttributeError`, the same as assigning an attribute does.

Restoring a value from `pickle` or `copy` data now runs the same validation as construction.
A forged or corrupt payload (a `float` magnitude, a unit of another dimension, a `Temperature` below absolute zero, a state that is not a `(magnitude, display unit)` pair) raises `InvalidMeasurementError` on load instead of producing a value construction would have refused.

## [0.1.3] - 2026-09-29

### Added

#### `Mass` family gets new units

`Dalton`, `Grain`, `Pound`, `Ounce`, `SolarMass`, and `EarthMass`.

#### `Length` family gets new units

- `Picometre`.
- Imperial: `Foot`, `Yard`, `Mile`, `NauticalMile`.

#### `Energy` family gets new units

- `Joule` units expanded.
- `Electronvolt` family added.
- `Erg` unit added.
- Nutritional units - `Calorie`, `Kilocalorie`, and `ThermochemicalCalorie`.

#### `Frequency` family gets new units

`Gigahertz`, `Terahertz`, and `Petahertz`.

#### Dimensions get unicode superscripts

Instead of `T^a L^b M ^c ...` it uses now proper signed superscripts, like: `T⁻¹⁷ M⁻⁴²⁰ I¹⁰²⁴ Θ⁻⁵¹² J⁻⁹⁰⁰⁰ ∠¹⁹⁹¹`.

### Changed

#### `SamplingPeriod` and `Instant` are reached from `Time`, not their own constructors

```python
from kuchka import Second, Millisecond, Hour

period = Millisecond(2).as_sampling_period()
rate = 1 / period  # -> SampleRate(500)

reading = Second(1_700_000_000).as_instant()
later = reading + Millisecond(500)  # -> Instant
checkpoint = Hour(1).as_instant()  # an hour past whatever the caller calls zero
```

`SamplingPeriod` and `Instant` are measured in the same seconds `Time` already is.
There is no separate "sampling-period-second" or "instant-second" out in the world, so there is no separate constructor for one either.
Every `Time` constructor (`Second`, `Millisecond`, `Microsecond`, `Minute`, `Hour`) reaches both types this way, at whatever prefix it was already built with.

### Removed

#### `SamplingPeriod`s unique synthetic units

`SecondSamplingPeriod`, `MillisecondSamplingPeriod`, `MicrosecondSamplingPeriod`, `SecondInstant`, and the `SAMPLING_PERIOD_MICROSECOND` / `SAMPLING_PERIOD_MILLISECOND` / `SAMPLING_PERIOD_SECOND` `UnitDef` constants.
`SAMPLING_PERIOD_UNITS` and `INSTANT_UNITS` stay, now built directly from `TIME_UNITS`.

### Fixed

#### `typing_extensions` import missing

Was missed because `typing_extensions` is a transient dependency of `mypy` which was used in dev-dependencies.
Fixed with import guard in `kuchka.internal.typing` for all affected Python versions.

## [0.1.2] - 2026.09.22

### Added

#### `Pressure` family

`Pascal` is the canonical unit.
Additional units are: `Atmosphere`, `Bar`, `Hectopascal`, `Kilopascal`, `Megapascal`, `Millibar`, and `PoundPerSquareInch`.

#### `Density` family

`KilogramPerCubicMetre` is the canonical unit.
Additional units are: `GramPerCubicCentimetre`, `KilogramPerCubicLitre`.

#### Expanded kinematics

Overall, the new additions to the kinematics module allow to express Newton's Second Law as it is taught in school: `F = ma`.

##### `Velocity` gets new units

`KilometrePerHour`, `KilometerPerHour`, and `MilePerHour`.

##### `Acceleration` family

`MetrePerSecondSquared` and `MeterPerSecondSquared`, where the first unit is the canonical, and the second is an alias.

##### `Force` family

`Newton` is the canonical unit.
Additional multiples are defined as `Millinewton` and `Kilonewton`.

Non-SI units: `Dyne` and `PoundForce`.

#### `Temperature` below 0 degrees Kelvin raises `InvalidMeasurementError`

Except of specific domains, temperature below 0 degrees Kelvin does not make much sense.
Once such domain will be required, it could be added through a distinct quantity.

#### `Angle` family

`Radian` is the canonical unit, matching the SI-coherent unit for plane angle.

`kuchka.units.angular` defines its own fixed, deterministic, 15-significant-digit rational representation of pi (`_PI`, matching the precision commonly cited by NASA/JPL) and uses it to define `Degree`, `Turn`, `Gradian`, `ArcMinute`, and `ArcSecond`'s scales relative to `Radian`.

#### `ModularQuantity`

An algebraic base for quantities that wrap around after a fixed period, such as a position on a circle.

`+`/`-` are ordinary wraparound group arithmetic (`[0, period)`); `difference()` is the separate shortest-signed-path method (`(-period/2, +period/2]`) for heading-error/control-loop-style use.
Deliberately has no total order (`__lt__` and friends are not implemented at all -- there is no universal "greater than" for a cyclic reading).

#### `AffineQuantity` is a generic base

`AffineQuantity` is taken out of `Temperature` to be able to support additional affine quantities like a future `Instant`.

#### `Conductance` family

`Siemens`, `Microsiemens`, `Millisiemens`, `Kilosiemens`, registered as `Resistance`'s reciprocal.
`1 / Resistance -> Conductance`, `1 / Conductance -> Resistance`, and Ohm's law in conductance form (`Voltage * Conductance -> Current`, `Current / Voltage -> Conductance`, `Current / Conductance -> Voltage`).

#### `Area` and `Volume` families

- `SquareMillimetre`/`SquareCentimetre`/`SquareMetre`/`SquareKilometre`, plus `Hectare`, `Acre`, and `SquareInch`.
  `Length * Length -> Area` and `Area / Length -> Length`.
- `CubicMillimetre`/`CubicCentimetre`/`CubicMetre`, plus `Litre` and its own `Microlitre`/`Millilitre`/`Kilolitre` prefixes.
  `Area * Length -> Volume`, `Length * Area -> Volume`, and both inverses (`Volume / Length -> Area`, `Volume / Area -> Length`).

#### New Temporals

- `Minute` and `Hour` for `Time`.

#### New `Charge` units

- `MilliampereSecond`, `MilliampereHour`, and `AmpereHour`.

#### New `Energy` units

- `WattHour` and `MilliwattHour`.

## [0.1.1] - 2026-09-09

### Added

#### `Prefix` constructor for internal unit creation.

Internally used registry that allows reusing the same names, magnitudes, symbols and names across all units.
Serves to avoid manual rolling, reduce typos, reduce visually hard to verify magnitude strings.
Migrate most (aspiring to all) units to the registry.
Some compound units (m/s, kS/s, etc.) require additional review with regard to this change.

### Fixed

#### `Kelvin`, `Celsius`, `TemperatureDelta`, `KELVIN`, `CELSIUS` split and exposed

These objects were clumped together in `quantities/thermal.py`.
Now they are split correctly and exposed as first class API.

#### Coherent `__init__` and `__all__` definitions

Properly exposed API of all units, quantities, utility methods and definitions.

## [0.1.0] - initial release

Base version.
