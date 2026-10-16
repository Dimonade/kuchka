# Changelog

All notable changes to kuchka are documented here.

The format tries to follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
See the `Stability` section in `README.md` for what versioning means before `0.2.0`.

## [0.1.4] - `develop`

### Added

#### New units added

- Time:
  - `Femtosecond`, `Picosecond`, and `Nanosecond`.
  - `Day`, `Week`, `Fortnight`, and `JulianYear`. All exact scales of a `Second`.
  - `Jiffy`.
- Temperature: `Fahrenheit`, the usual `Fahrenheit(32) == Celsius(0)`, `Fahrenheit(-459.67) == Kelvin(0)`.
- Current: `Picoampere`, `Nanoampere`, and `Megaampere`.
- Resistance: `Microohm` and `Gigaohm`.
- Conductance: `Nanosiemens`.
- Voltage: `Nanovolt`, `Megavolt`, and `Petavolt`.
- Power: `Picowatt`, `Nanowatt`, `Megawatt` to `Petawatt`, `Horsepower`, and `MetricHorsepower`.
- Force: `KilogramForce`, `Meganewton`, `Micronewton`,.
- Acceleration: `Gal`, `Milligal`, and `Microgal`.
- Length: `AstronomicalUnit` and `LightYear`.
- Energy: `Petajoule`, `KilowattHour`, `TonneOfTNT`, `KilotonneOfTNT`, and `MegatonneOfTNT`.
- Velocity: `Knot`.
- Frequency: `Nanohertz`, `Microhertz`, and `Millihertz`.
- Amount: `Femtomole`, `Picomole`, `Nanomole`, and `Kilomole`.
- Baud Rate: `Megabaud` and `Gigabaud`.
- Density: `GramPerLitre`, `GramPerMillilitre`, and `KilogramPerLitre`.

#### Energy density is its own quantity

`EnergyDensity` (`JoulePerCubicMetre`, `KilojoulePerCubicMetre`, `MegajoulePerCubicMetre`, `WattHourPerLitre`) shares its dimension with `Pressure`, and the two are contested.
`Energy / Volume` is an `EnergyDensity` and `Force / Area` a `Pressure`.

#### The angle axis takes part in arithmetic

`AngularDisplacement` is the angle swept, which does not wrap, next to the wrapping `Angle`.
`AngularVelocity` (`RadianPerSecond`, `DegreePerSecond`, `TurnPerSecond`, `RevolutionPerMinute`) and `Torque` (`NewtonMetre`, `PoundForceFoot`, and more) follow from it.
`Torque * AngularDisplacement` is an `Energy`, `AngularDisplacement / Time` is an `AngularVelocity`, and `Hertz(1)` is not an `AngularVelocity`.
`Torque.from_force(force, lever_arm)`, `Frequency.to_angular_velocity()`, `AngularVelocity.to_frequency()`, `Angle.to_angular_displacement()`, and `AngularDisplacement.to_angle()` convert by name.

#### Unit tables accept the notations real files use

`TEMPERATURE_UNITS` takes `C`, `degC`, `degrees C`, and `Degrees Celsius`, and the other tables take `u` for micro and the dalton, `Mohm`, `meter`, `sec`, `kwh`, `yr`, `mm2`, `m^3`, `cc`, and similar.
Symbols stay case-sensitive (`mV` is not `MV`), names and spoken forms ignore case, and a table cannot be built if a spelling could mean two units.
Iterating a table now yields display symbols (`°C`, `ΔK`), and the earlier keys (`C`, `dK`, `t`, `As`) still resolve.
See `docs/concepts/unit_spellings.md`.

#### Quantity kinds are catalogued separately from arithmetic

Every quantity type, of any shape, is registered as a kind of its dimension, and `kuchka` does not import with a type that is missing.
Arithmetic keeps choosing its result from the linear kinds alone: a second linear kind of a dimension states whether it specialises the first or is contested with it.
`SamplingPeriod`, `SampleRate`, and `BaudRate` are specialisations of `Time` and `Frequency`.
A dimension whose linear kinds are on equal footing has no principal kind, and arithmetic that produces it raises the new `AmbiguousKindError`.

#### `is_close` compares with an explicit tolerance

`a.is_close(b, tolerance=...)` on every quantity shape.
The tolerance is a required keyword-only quantity (a `TemperatureDelta` for `Temperature`, a `Time` for `Instant`), and the test is exact and inclusive.
Angles measure the short way round the circle.

#### `LogarithmicRatio`, the first logarithmic quantity

- `Decibel` and `Bel` constructors, with `LOGARITHMIC_RATIO_UNITS`.
- `PureLogarithmicQuantity`, the base for a ratio expressed as a logarithm, and `LogarithmicUnitDef`, the unit-definition type for it.
- Levels add, subtract, scale by a plain number, negate, take `abs()`, and compare, all exactly.
- `to_power_ratio()` / `to_field_ratio()` and `from_power_ratio()` / `from_field_ratio()` convert to and from a linear `Proportion`.
  They are evaluated in `Decimal` at the active context precision; whole multiples of 10 dB (power) or 20 dB (field) are exact.

### Changed

#### Conversion functions

Conversions between quantity types are named `to_*` and `from_*`.
`as_instant`, `as_sampling_period`, and `as_frequency` are now `to_instant`, `to_sampling_period`, and `to_frequency`; the old names are removed.

#### Angle arithmetic

Multiplying or dividing an `Angle` by a quantity raises `IncompatibleDimensionError`, with a pointer to `to_angular_displacement()`.
It raised a bare `TypeError`.

### Fixed

#### Every unit of a table is published

`KilowattHour`, `GramPerLitre`, and `GramPerMillilitre` were in their tables but not exported, so `from kuchka import KilowattHour` failed and a value in them could not be pickled.

#### A `Proportion` keeps the kind it scales

`SampleRate * Ratio(2)` and `BaudRate * Percent(50)` returned a `Frequency` in hertz.
A dimensionless operand now keeps the kind of the other operand.

#### A unit belongs to its quantity types

`Hertz(1).to(BAUD)` displayed `1 Bd`, and `Frequency(Fraction(1), BAUD)` was accepted, because a type took any unit of its dimension.
Each quantity type now binds the units of its own table and refuses every other, and the error names the type the unit belongs to.
A unit of `Time` is still a unit of `SamplingPeriod`; `SampleRate` no longer converts to hertz with `.to()`, and `SampleRate.as_frequency()` does.

#### Units keep their identity through copy and pickle

`copy.deepcopy(Volt(5)).unit is VOLT` and the same after a pickle round trip were `False`, because a unit was rebuilt by value on the way back.
Unit definitions are now immutable values with value equality: copying returns the same unit, and pickling stores the name `kuchka.units` publishes it under, so a pickle holds no unit internals.
A unit that `kuchka.units` does not publish cannot be pickled.
Pickle is documented as a way to move values between processes of one version, and storage as an exact magnitude plus a unit symbol; see `docs/concepts/persistence.md`.

#### Quantity class constructors validate their arguments

`Voltage(0.5, AMPERE)` and the other quantity classes used to store whatever they were given.
They now accept only an exact `Fraction` magnitude and a display unit of the right kind and dimension, and raise `InvalidMeasurementError` otherwise.
The unit constructors (`Volt(5)`) are unchanged.

#### A quantity keeps its state

Deleting an attribute, calling `__init__` again, or calling `__setstate__` on a live value raises `AttributeError`.
Restoring from `pickle` or `copy` data runs the same validation as construction.

#### Numeric input has a bounded size

`Decimal("1E+1000000")` was accepted and then took seconds to display.
Input is limited to a `Decimal` exponent of +/-1000, 1000 digits, and 8192 bits for an `int` or each part of a `Fraction`; larger values raise `InvalidMeasurementError`.
The limits live in `kuchka.internal.limits`.

#### Display ignores the active `Decimal` context

`repr()` and `format()` no longer depend on the caller's precision, rounding mode, or traps, and round once, from the exact value.
Ties round away from zero: `f"{Volt(2.665):.2f}"` is `2.67 V` (it was `2.66 V`).

#### `__all__` lists only real exports

`kuchka.units.__all__` and `kuchka.quantities.__all__` no longer include submodule names or `annotations`.
`kuchka/__init__.py` shrinks to 42 lines: the promoted names are generated into `kuchka/_api.py` by `tools/generate_api.py` (`just generate-api`).

#### Division by zero raises `DivisionByZeroError`

`Volt(1) / 0`, `Volt(1) / Volt(0)`, and `1 / Second(0)` raised a bare `ZeroDivisionError` with the message `Fraction(1, 0)`.
They raise `DivisionByZeroError`, a `MeasurementError` that is also a `ZeroDivisionError`, so existing handlers keep working.
A unit definition with a zero or negative scale is rejected when it is created.

#### Angles are exact in turns

`Turn` is the canonical angle unit, and `Degree`, `Gradian`, `ArcMinute`, and `ArcSecond` are exact fractions of it.
`Radian` converts with pi to 100 decimals (it was 15), so every displayed digit of a conversion is correct.
`Radian(math.pi) == Degree(180)` is now `False`; compare with `is_close`.
`Angle.magnitude` is now in turns.

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
Additional units are: `GramPerCubicCentimetre`, `KilogramPerLitre`.

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
