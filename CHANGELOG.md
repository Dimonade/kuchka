# Changelog

All notable changes to kuchka are documented here.

The format tries to follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
See the `Stability` section in `README.md` for what versioning means before `0.2.0`.

## [0.1.5] - `develop`

### Added

#### New quantity families, units, relationships, and more

- **Electromagnetics:**
  Added magnetic flux and flux density (weber, tesla, and gauss families), capacitance, inductance, resistance-based `Reactance` and `Impedance` roles, magnetic field strength and its `Magnetization` role, permittivity, and permeability.
  Dimensional arithmetic now derives these quantities through relationships such as `Voltage * Time`, `MagneticFlux / Area`, `Charge / Voltage`, `Resistance * Time`, `Current / Length`, and `Permeability * MagneticFieldStrength`.
  Both role families reuse their parent units through explicit conversions and dedicated unit tables.

- **Thermodynamics and mechanics:**
  Added specific energy (including J/kg, Wh/kg, and cal/kg), heating rates in Kelvin, Celsius, and Fahrenheit scales, momentum (SI, CGS, and FPS), impulse (N·s, mN·s, kN·s, dyn·s, and lbf·s), velocity squared, and volumetric and mass flow rates.
  Added `CubicFoot` and `UsGallon` volume units.
  Derived quantities now include `SpecificEnergy` from energy, pressure, density, and acceleration relationships; `HeatingRate` from temperature change and time; `Momentum` from `Mass * Velocity`; `Impulse` from `Force * Time`; `VelocitySquared` from `Velocity * Velocity`; and flow rates from volume, mass, density, area, and velocity.
  `Pressure * VolumetricFlowRate` produces `Power`.

- **Photometry:**
  Added solid angle, luminous flux, illuminance, luminous energy, luminous exposure, luminance, and luminous efficacy, with SI and customary units including steradians, square degrees, lumens, lux, phot, foot-candle, talbot, nit, stilb, foot-lambert, and lumens per watt.

- **Chemistry:**
  Added molar mass, molar concentration (M, mM, µM, nM), molar energy, entities per amount, molality, molar volume, molar flow rate, catalytic activity (katal and enzyme unit), and molar charge, alongside milligram-per-litre and microgram-per-litre density units.
  Dimensional arithmetic derives these from `Mass / Amount`, `Amount / Volume`, `Energy / Amount`, `Amount / Mass`, `Volume / Amount`, `Amount / Time`, and `Charge / Amount`; `MolarConcentration * MolarMass` produces `Density`.
  `CatalyticActivity` is a role of `MolarFlowRate`, with explicit conversion through `to_molar_flow_rate()`.
  Added `AVOGADRO_CONSTANT` and `FARADAY_CONSTANT` to `codata_2022` for entity counts and molar charge calculations.
  Ambiguous bare spellings `Da`, `u`, `ppm`, `IU`, and molal `m` are refused.

- **Molar heat capacity:**
  Added `MolarHeatCapacity` (J/(mol·K), kJ/(mol·K), cal/(mol·K)) and `MolarEntropy`, a closed role of it, the quantities the molar gas constant and the entropy tables of chemistry are measured in.
  `HeatCapacity / AmountOfSubstance` and `MolarEnergy / TemperatureDelta` are a `MolarHeatCapacity`, and the heat `Q = n * C * dT` is an `Energy` however it is grouped.
  `Entropy / AmountOfSubstance` is a `MolarEntropy`, `MolarEntropy * AmountOfSubstance` an `Entropy`, and `Entropy / MolarEntropy` an `AmountOfSubstance`.
  The calorie per mole kelvin is the classical entropy unit of chemistry tables.

- **Entropy:**
  Added `Entropy` and `SpecificEntropy`, closed roles of `HeatCapacity` and `SpecificHeatCapacity`, so that `Entropy * TemperatureDelta` is refused and never silently an `Energy`.
  `HeatCapacity.to_entropy()` and `Entropy.to_heat_capacity()` move between them, and the same pair exists for the specific kinds.
  `Entropy / Mass` is a `SpecificEntropy`, `SpecificEntropy * Mass` an `Entropy`, and `Entropy / SpecificEntropy` a `Mass`.
  Added `cal/K` and `kcal/K` to the heat capacity units, which the entropy units share.

- **Heat capacity:**
  Added `HeatCapacity` (J/K, kJ/K) and `SpecificHeatCapacity` (J/(kg·K), kJ/(kg·K), cal/(g·K)), so the heat `Q = m * c * dT` is an `Energy` however it is grouped.
  `Energy / TemperatureDelta` is a `HeatCapacity`, `HeatCapacity / Mass` and `SpecificEnergy / TemperatureDelta` are a `SpecificHeatCapacity`, and `SpecificHeatCapacity * TemperatureDelta` is a `SpecificEnergy` by a rule.
  A degree Celsius in the denominator is a kelvin, so `J/°C` and `J/(kg·°C)` are accepted spellings.
  Entropy and the gas constants are not in this release; they are planned as closed roles of these kinds.
  The `thermodynamics` units package moves up the layering order, because it now builds on the energy units.

- **Length:**
  Added `Parsec`, `Kiloparsec`, `Megaparsec`, and `Gigaparsec`.
  A parsec is exactly 648000/pi astronomical units, so it is held as that quotient with pi to 100 decimal places, within one part in 1E+100 of its defined length, and the multiples of it are exact.
  The spelling `pc` is now a parsec, where it was refused before.

- **Temperature:**
  Added `Rankine` and `DeltaRankine`: a Rankine degree is exactly 5/9 of a kelvin, and 0 °R is absolute zero, so 0 °F is exactly 459.67 °R.
  The spellings `deg`, `degrees`, `degree`, and `Grad` stay ambiguous between the scales and are still refused.

- **Magnetic energy density:**
  `MagneticFluxDensity * MagneticFieldStrength` is now an `EnergyDensity`, in either order, and no longer raises `AmbiguousKindError`.
  It is the product `B·H`, twice the energy stored in a linear medium, and `Magnetization` stays refused in it.

- **Impulse:**
  `Force / Frequency` is now an `Impulse`, the force times a period, and no longer raises `AmbiguousKindError`.
  The roles of `Frequency`, such as `Activity` and `SampleRate`, stay refused in that quotient.

- **Activity densities:**
  Added activity concentration (Bq/m³, Bq/L, pCi/L), specific activity (Bq/kg, pCi/g, Ci/g), and surface activity (Bq/cm², dpm/100 cm², Ci/km²), the readings of radon monitors, soil and food assays, and contamination monitors.
  They are principal kinds of their own dimensions, and rules make `Activity / Volume`, `Activity / Mass`, and `Activity / Area` their quotients and `Activity` their product with the divisor.
  `Frequency / Volume`, `Frequency / Mass`, and `Frequency / Area` are these kinds too.

- **Dose rates:**
  Added absorbed dose rate (Gy/h, rad/h), equivalent dose rate (Sv/h, rem/h), and exposure rate (R/h), the readings of survey meters and dosimeters.
  They are roles of the new principal kinds `SpecificPower` (W/kg) and `SpecificCurrent` (A/kg), and a rate times a `Time` is the matching dose, an `Exposure` for exposure rate.
  `Velocity * Acceleration`, `Power / Mass`, and `SpecificEnergy / Time` are now a `SpecificPower`, and `SpecificPower * Time` is a `SpecificEnergy`.
  A `_rule` may now name a role as an operand or as its result, which is how `Sievert(1) / Hour(2)` is a dose rate while `Sv * kg` stays refused.
  `EquivalentDoseRate.from_absorbed_dose_rate(rate, weighting_factor)` weights a rate as `EquivalentDose.from_absorbed_dose` weights a dose.

- **Radiation:**
  Added absorbed dose (gray, rad), equivalent dose (sievert, rem), and exposure (roentgen), with `SpecificCharge` (C/kg, Ah/kg, mAh/g) as the principal kind behind exposure.
  `AbsorbedDose` and `EquivalentDose` are roles of `SpecificEnergy`, and `Exposure` is a role of `SpecificCharge`, so each takes part in arithmetic only when scaled, divided by itself, or converted first.
  `AbsorbedDose.to_specific_energy()` takes a dose as an energy per mass, and `EquivalentDose` has no way into one: a sievert times a kilogram is refused.
  `EquivalentDose.from_absorbed_dose(dose, weighting_factor)` is the one way from grays to sieverts, and takes a plain `Proportion`.
  `Charge / Mass` now derives `SpecificCharge`, and `SpecificCharge * MagneticFluxDensity` a `Frequency`.
  Added `kuchka.constants.icrp_103`, the radiation weighting factors of ICRP Publication 103 as proportions.
  The `radiation` package moves up the layering order, because it now builds on mechanics and electromagnetics.

- **Dimensional model:**
  Added solid angle as an independent dimension axis.
  Photometric arithmetic now distinguishes luminous intensity from luminous flux, derives illuminance and luminance separately, and supports luminous energy, exposure, and efficacy.
  `Area / Area` remains a `Proportion`.
  Added explicit conversions between contested kinds: `Impulse` and `Momentum`, and `VelocitySquared` and `SpecificEnergy`, with the latter conversion accounting for the factor of two in kinetic energy.

#### New constants

- **Boltzmann Constant (k_B) and Molar Gas Constant (R)**
  Added `BOLTZMANN_CONSTANT` (an `Entropy`, 1.380649e-23 J/K, exact) and `MOLAR_GAS_CONSTANT` (a `MolarEntropy`, 8.31446261815324 J/(mol·K), exact) to `codata_2022`.
  CODATA prints the gas constant with a trailing ellipsis because it shows a prefix: the product of the two exact defining constants has exactly those 15 digits, and the library stores all of them.
  `AVOGADRO_CONSTANT * BOLTZMANN_CONSTANT` is `MOLAR_GAS_CONSTANT` by a rule, with no rounding, and the two quotients return the other factor.

### Changed

#### Unit modules live in themed packages

`kuchka.units` keeps the base dimensions and the angle, solid angle, proportion, and logarithmic axes at its top level, and groups the other modules in `geometry`, `kinematics`, `mechanics`, `electromagnetics`, `information`, `photometry`, and `radiation`.
Every constructor and table is still imported from `kuchka` and `kuchka.units`.
A unit module is imported from its package, so `from kuchka.units import voltage` is now `from kuchka.units.electromagnetics import voltage`, and `kuchka.units.kinematics.force` is now `kuchka.units.mechanics.force`.

The quantity types follow the same layout, one module per type in the matching package of `kuchka.quantities`: `kuchka.quantities.electrical.Voltage` is now `kuchka.quantities.electromagnetics.voltage.Voltage`, and `Force`, `Power`, and `Torque` are in `kuchka.quantities.mechanics`.
A quantity now pickles by the name `kuchka.quantities` publishes its class under, so a pickle no longer depends on the module that defines the class and survives such a move.
A pickle made by an earlier version names the old module and does not load when its class moved.

### Deprecated

### Removed

### Fixed

## [0.1.4] - 2026-10-24

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
- Force: `KilogramForce`, `Meganewton`, `Micronewton`.
- Acceleration: `Gal`, `Milligal`, and `Microgal`.
- Length: `AstronomicalUnit` and `LightYear`.
- Energy: `Petajoule`, `KilowattHour`, `TonneOfTNT`, `KilotonneOfTNT`, and `MegatonneOfTNT`.
- Velocity: `Knot`.
- Frequency: `Nanohertz`, `Microhertz`, and `Millihertz`.
- Amount: `Femtomole`, `Picomole`, `Nanomole`, and `Kilomole`.
- Baud Rate: `Megabaud` and `Gigabaud`.
- Density: `GramPerLitre`, `GramPerMillilitre`, and `KilogramPerLitre`.

#### Reading text with `parse`

`parse(text, quantity)` reads a number and a unit from text into the quantity type it is given, through that type's own table of unit spellings: `parse("5 mV", Voltage)`.
The caller names the type, since `"5 s"` can be a `Time`, an `Instant`, or a `SamplingPeriod`.
The number is read exactly, and text that cannot be read raises `ParseError`, or `UnknownUnitError` for a unit the type does not have.

- `allow_archaic` takes an `ArchaicPolicy` (`Deny` by default, or `Allow`), with `False` and `True` as shorthands, and reads the archaic modules the application has imported.
- A text that two different units claim raises `ParseError` and never picks one.
- `extend_units` takes the table of an archaic module, and records it on the type for `parse`.

#### Stress, apparent and reactive power, and activity

Four more kinds share a dimension with an existing one, each as a role of it: `Stress` of `Pressure`, `ApparentPower` and `ReactivePower` of `Power`, and `Activity` of `Frequency`.
A role adds with its own kind, scales by a plain number or a `Proportion`, divides by its own kind into a `Proportion`, and takes the conversion back to its principal kind (`to_pressure()`, `to_power()`, `to_frequency()`) for any other arithmetic.

- Stress: reached with `Pressure.to_stress()`, and reads every unit of `Pressure`.
- Apparent power: `VoltAmpere` and `MillivoltAmpere` through `GigavoltAmpere`; reactive power: `Var` and `Millivar` through `Gigavar`, read as `VAr` and `VAR` too.
- Activity: `Millibecquerel` through `Terabecquerel`, and `Curie` with `Millicurie`, `Microcurie`, and `Picocurie`.
- Pressure: `Gigapascal` and `KilopoundPerSquareInch`.

#### Data and data rate

`Data` counts bits and `DataRate` is data per time.
Both have a dimension of their own, the new information axis, so a bit rate is not a `Frequency`, a `SampleRate`, or a `BaudRate`, and `Data / Data` is a `Proportion`.
`Data / Time` is a `DataRate`, `DataRate * Time` is `Data`, and `Data / DataRate` is a `Time`.

- Data: `Bit` and `Byte`, with the SI multiples `Kilobit` to `Petabit` and `Kilobyte` to `Petabyte`, and the IEC binary multiples `Kibibit` to `Pebibit` and `Kibibyte` to `Pebibyte`.
- Data rate: `BitPerSecond` and `BytePerSecond`, with the same multiples (`MegabitPerSecond`, `MebibytePerSecond`, and so on).
- `kB` is 1000 bytes and `KiB` is 1024 bytes, `Mb` is the megabit and `MB` the megabyte, and `KB` and `Kb` are refused.

The IEC binary prefixes `kibi` to `yobi` join the SI ones in `kuchka.internal.prefixes`, and a `Prefix` takes a `base`.

#### Energy density is its own quantity

`EnergyDensity` (`JoulePerCubicMetre`, `KilojoulePerCubicMetre`, `MegajoulePerCubicMetre`, `WattHourPerLitre`) shares its dimension with `Pressure`, and the two are contested.
`Energy / Volume` is an `EnergyDensity` and `Force / Area` a `Pressure`.

#### German degree words

`TEMPERATURE_UNITS` reads `grad C`, `Grad Celsius`, `grad F`, `Grad Fahrenheit`, `grad K`, and `Grad Kelvin`, the spellings of historical German data, in any case.
A bare `Grad` names no scale, as `deg` and `degrees` do not.

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

#### Archaic units

A collection of historic, archaic, traditional, and out of use units, imported explicitly from `kuchka.units.archaic`.
The top-level namespace, `kuchka.units`, and the generated API list none of them, and a quantity type displays in an archaic unit once its module is imported.

- `german`: the principal Meilen, with the regional ones in their own module,
- `hebrew`: Biblical and Talmudic units,
- `japanese`: Shakkanho units of length, area, volume, and mass,
- `russian`: Imperial units of length and area.

Modules register their units through `extend_units`, which adds units to a quantity type beside those `bind_units` bound.
The pages under `docs/how-to` describe adding a unit, a quantity, a dimension, and archaic units, splitting a unit module, and the tests and documentation each needs.

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

#### Typed products and quotients

The static overloads of `*` and `/` declare 33 more pairs the runtime already computed, so a type checker infers the result and not `LinearQuantity | Fraction`:

- Energy and charge: `Charge * Voltage`, `Energy / Charge`, and `Energy / Voltage`.
- Charge flow: `Charge * Frequency`, `Current / Charge`, and `Current / Frequency`.
- Power: `Force * Velocity`, `Power / Force`, `Power / Velocity`, `Energy * Frequency`, `Power / Energy`, and `Power / Frequency`.
- Kinematics: `Frequency * Length`, `Frequency * Velocity`, `Velocity / Length`, `Acceleration / Frequency`, and `Acceleration / Velocity`.
- Rotation: `AngularVelocity / AngularDisplacement`.
- Energy density: `EnergyDensity * Area` and `Force / EnergyDensity`.
- Work: `Force * Length`, `Energy / Force`, and `Energy / Length`.
- Resistance: `Resistance * Conductance`, a plain `Fraction`.

Each pair is declared on both operand types, so the commuted product is typed too.

#### A type-checker policy, and the matrix that holds it

The README states which checkers the types are written for: mypy from 1.11 and at the newest, pyright at the newest, and the library's own source under `ty`.
A contract test asks each installed checker about a representative set of operand pairs and operators and compares the answer with the runtime, and the negative typing fixture is checked on mypy and on pyright.
The tox environments `typing-min` and `pyright` run them, and `just watch-tools` runs the checks on the newest tool versions as an early warning.

### Changed

#### Conversion functions

Conversions between quantity types are named `to_*` and `from_*`.
`as_instant`, `as_sampling_period`, and `as_frequency` are now `to_instant`, `to_sampling_period`, and `to_frequency`; the old names are removed.

#### A ratio is a `Proportion`

`Volt(5) / Volt(2)` returned a bare `Fraction`, which is indistinguishable from a plain number, so `Volt(Volt(5) / Volt(2))` was accepted as `2.5 V`.
The quotient of two quantities of one dimension is now a `Proportion`, and so is the product or quotient of two proportions and the quotient of two levels: `Percent(50) * Percent(50)` is `0.25 1`, and `Decibel(6) / Decibel(3)` is `2 1`.
A `Proportion` compares with a `Proportion` and is not a valid argument to a quantity constructor, so `Volt(5) / Volt(2) > 2` raises and `Volt(Volt(5) / Volt(2))` raises.
`.magnitude` returns the exact `Fraction`, so `round(Mass / Mass)` is now `round((Mass / Mass).magnitude)`.
The overloads declare the result on every linear type, and on `Pressure` and `EnergyDensity` against each other.
Dimensionless results of unlike quantities, such as `Hertz(2) * Second(3)`, remain plain `Fraction` values.

#### Role kinds refuse arithmetic by dimension

`BaudRate(9600) * Metre(1)` was a `Velocity`, because `BaudRate` shares the dimension T⁻¹ with `Frequency`.
`SampleRate`, `SamplingPeriod`, and `BaudRate` now combine only with a plain number, a `Proportion`, themselves in a quotient, and, for the reciprocal pair, each other.
Every other product or quotient raises `IncompatibleDimensionError`, and the error names the conversion that leaves the role: `SampleRate.to_frequency()`, or the new `SamplingPeriod.to_time()`.
`BaudRate` has no such conversion, and the error says so.

#### A hint where a torque and an energy meet

Adding, subtracting, or comparing an `Energy` and a `Torque` raises `IncompatibleDimensionError` with a pointer to `AngularDisplacement` and `Torque.from_force`.

#### A `Proportion` scales a quantity, and the overloads say so

`Percent(50) * Volt(2)` is `Volt(1)`, and `Volt(2) / Percent(50)` is `Volt(4)`.
The overloads declare it on every linear type, in both orders, and declare `Ratio(2) / Second(4)` as a `Frequency` and the other reciprocals, so mypy and ty infer the type and not `LinearQuantity | Fraction`.
A `Proportion` over a role kind is now the reciprocal role, as a plain number is: `Ratio(2) / SampleRate(4)` is a `SamplingPeriod`.
It returned a plain `Time`, and `Ratio(2) / BaudRate(9600)` returned a `Time` too, where `2 / BaudRate(9600)` raised.
A role with no reciprocal kind now raises `IncompatibleDimensionError` for a `Proportion` as well.

#### `sum()` names its start

`sum([Volt(1), Volt(2)])` raised because `sum()` starts from the plain number `0`.
The error now says what `sum()` needs: `sum(values, start=Volt(0))`, with the zero of the type that was added to.

#### A quantity has no truth value

`bool(Volt(0))` was `True`, so `if not voltage:` was always false, and a rule of zero being false has no single meaning across shapes: `Celsius(0)` is not `Kelvin(0)`, `Degree(360)` is `Degree(0)`, and `Decibel(0)` is a ratio of one.
`bool()` of any quantity now raises `TypeError`, with a pointer to `is None` and to an equality with zero.

#### Static types refuse what the runtime refuses

A parameter typed `object` let `Degree(30) * Volt(1)` and `Celsius(20) * Volt(1)` type-check, as an `Angle` and a `Voltage`, and let any quantity be compared with any other and with a plain number.
Comparisons now take their own type, the reflected operators take a plain number, and a linear quantity multiplies and divides by a linear quantity or a plain number, so mypy and ty refuse each of those.
A test reveals a representative set of operand pairs and operators with mypy, and checks every one against the runtime.

#### Angle arithmetic

Multiplying or dividing an `Angle` by a quantity raises `IncompatibleDimensionError`, with a pointer to `to_angular_displacement()`.
It raised a bare `TypeError`.

### Fixed

#### Every unit of a table is published

`KilowattHour`, `GramPerLitre`, and `GramPerMillilitre` were in their tables but not exported, so `from kuchka import KilowattHour` failed and a value in them could not be pickled.

#### A `Proportion` keeps the kind it scales

`SampleRate * Ratio(2)` and `BaudRate * Percent(50)` returned a `Frequency` in hertz.
A dimensionless operand now keeps the kind of the other operand.

#### `to_sampling_period()` keeps the display unit

`Millisecond(2).to_sampling_period()` displayed `0.002 s`, and so did `SAMPLING_PERIOD_UNITS["ms"](2)`.
Both now display `2 ms`.

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
