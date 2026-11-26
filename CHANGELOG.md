# Changelog

All notable changes to kuchka are documented here.

The format tries to follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
See the `Stability` section in `README.md` for what versioning means.

## [develop]

### Added

#### Display

- **`auto_scale()`:**
  `Ampere(0.000045).auto_scale()` returns the same measurement in the unit of its ladder that suits its size, here `45 µA`.
  The value is unchanged, the result has the type of the measurement, and `str()` and `f"{q}"` keep showing the unit the measurement was given.
  A ladder is the run of prefixed units of a quantity, such as the nanoampere to the megaampere; a measurement moves along the ladder of the unit it displays in, and a unit on no ladder keeps its display unit.
  Every quantity whose units come in decimal or binary prefixes has one ladder for each family of prefixed units: `Data` has the bit and the byte in both, and `Energy` has the joule, the electronvolt, the watt-hour, and the tonne of TNT.
  `Temperature` has the kelvin scale only, since the size of a reading in degrees Celsius is no size of the temperature.

- **`Time.clock_parts()`:**
  `Millisecond(5_025_500).clock_parts()` splits a span into whole days, hours, minutes, seconds, and the smaller units, here `(1 h, 23 min, 45 s, 500 ms)`.
  The parts add up to the span exactly, zero parts are left out, every part has the sign of the span, and the femtosecond takes the exact remainder.
  A day is exactly 86 400 s, so the split holds no calendar.

#### Reading text

- **Fractions in `parse`:**
  `parse("1/3 V", Voltage)` reads exactly one third of a volt, which no decimal holds.
  A fraction is two whole numbers around a slash, written without spaces and without an exponent.
- **A proportion without a unit:**
  `parse("0.25", Proportion)` is a ratio of a quarter, the same as `parse("0.25 1", Proportion)`.
  A unit table may name a bare unit, the unit a number with no unit is read in, and `PROPORTION_UNITS` names the ratio; every other quantity still needs its unit, and any other unit after the number of a proportion is an `UnknownUnitError`.

- **`kuchka.wire`:**
  `wire.dump(Volt(1) / 3)` writes a measurement as one string, `"1/3 V"`: the exact magnitude in the unit it displays in, a decimal when it terminates and a fraction when it does not, and the unit's symbol.
  `wire.load(value, Voltage)` reads what a boundary delivers: an instance of the type, text, a `{"value", "unit"}` mapping, or, for a `Proportion`, a number.
  Every refusal is a `ParseError`, which is a `ValueError`, so a validation framework reports it without a wrapper.

- **`kuchka.attrs`:**
  `attrs.field(converter=parse_field(Voltage))` makes a field a `Voltage` whatever arrives: an instance, text, a `{"value", "unit"}` mapping, or for a `Proportion` a number.
  The module imports nothing from `attrs`, and `pyright` types the `__init__` from the converter, so a bare number for a voltage is a static error.
  `mypy` reads only named functions as converters, so it types the attribute and leaves the `__init__` parameter as `Any`.

- **`kuchka.pydantic`:**
  `Annotated[Voltage, Quantity]` makes a Pydantic v2 field a `Voltage` whatever arrives, reading as `wire.load` reads and reporting every refusal as a `ValidationError`.
  `model_dump()` keeps the quantity, `model_dump(mode="json")` writes `"2800 mV"` and reads back exactly, and the JSON Schema is a string that names the quantity.
  It is the `kuchka[pydantic]` extra; `import kuchka` loads no integration library.

- **`kuchka.msgspec`:**
  `kuchka_dec_hook` and `kuchka_enc_hook` let `msgspec` decode and encode a struct field typed `Voltage`: `msgspec.json.decode(b'{"v": "4.2 V"}', type=Payload, dec_hook=kuchka_dec_hook)`.
  A refusal is a `msgspec.ValidationError` with the path of the field, the hooks raise `NotImplementedError` for what is not a quantity so they chain with an application's own, and `kuchka_schema_hook` lets `msgspec.json.schema` describe the quantity types.
  It is the `kuchka[msgspec]` extra.

- **`kuchka.bounds`:**
  `Bounds(gt=Volt(0), le=Volt(60))` holds the range a field accepts, compared exactly in any unit, and `check` raises `BoundsError`, a `ValueError`, that writes the value and the bound.
  `kuchka.pydantic.Bounds` is the `Annotated` marker beside `Quantity`, and `kuchka.attrs.Bounds` is the `attrs` validator; a `msgspec` struct calls `check` in `__post_init__`.
  A quantity with no ordering, such as an `Angle`, has no bounds, and both checkers report it.

- **`wire.to_dict` and `wire.from_dict`:**
  `wire.to_dict(Volt(1) / 3)` writes `{"value": "1/3", "unit": "V"}`, the exact data of the text form as two fields for a JSON document or a database row, and `wire.from_dict(data, Voltage)` reads it back with the strictness of `parse`.
  `unit="V"` writes the measurement in another unit of its quantity, converted exactly, and `as_float=True` writes a JSON number for a consumer that accepts nothing else, refusing a magnitude a `float` would corrupt.

- **`format_parts`:**
  `Volt(1234.5).format_parts(".2f")` returns `("1234.50", "V")`, the formatted magnitude and the unit symbol apart, for a table, a CSV column, or a protocol that renders them separately.
  It is the one rule behind `format`, `str`, and `repr`, which now join its two parts, so the rounding and the 28-digit default are the same everywhere.

#### Documentation

- **The limits-file example, read four ways:**
  `docs/examples/config_migration` reads one realistic configuration for an LED test fixture with Pydantic, with `attrs`, with `parse`, and through the `*_UNITS` tables that migrate the legacy file it came from, and `demo.py` walks the four rungs and breaks the file on purpose.
  Every rung refuses the same nine mistakes, checks the limits against what the hardware can do with `Bounds`, and a test holds the README excerpts to the modules.
- **Quick start 2 follows the same ladder:**
  the README reads one limits file with Pydantic, `attrs`, `parse`, and the unit tables, and writes it back with `wire`.

#### New units of existing quantities

- **Prefix families without gaps:**
  `Gigavolt` and `Teravolt` between `Megavolt` and `Petavolt`; `Nanocurie`, with `MillicuriePerGram`, `MicrocuriePerGram`, and `NanocuriePerGram` for specific activity; `KilojoulePerSquareMetre`; and `MillicoulombPerSquareCentimetre`, which electric flux density reads too.
  A test requires every family of prefixed units to hold each step of a thousand between its smallest and largest unit.
- **Temperature:**
  `Millikelvin`, `Microkelvin`, `Millicelsius`, and `Microcelsius`, each with a `Delta` form.
  A prefix keeps the zero of the scale, so `Millicelsius(0)` is 273.15 K, and `m°C` is the spelling of the millidegree.

### Fixed

- **`value_in` refuses a unit that is no unit of the quantity:**
  `Millivolt(2800).value_in(AMPERE)` returned `14/5`, a voltage expressed in amperes, and a value that was no unit at all raised an `AttributeError`.
  It now raises `InvalidConversionError`, as `to` always did, in all four shapes, and the two methods share one check.
  The display unit that `repr`, `format`, and `wire` pass is trusted and skips it.

## [0.1.5] - 2026-11-16

### Added

#### New quantities

- **Electromagnetics:**
  `MagneticFlux` and `MagneticFluxDensity` (weber, tesla, and gauss families), `Capacitance`, `Inductance`, `Permittivity`, `Permeability`, and `MagneticFieldStrength`, with `Magnetization` as its role.
  `Reactance` and `Impedance` are roles of `Resistance`.
  `ElectricFieldStrength` (V/m, kV/mm, ...), `CurrentDensity` (A/m², A/mm², mA/cm², ...), `LinearChargeDensity` (C/m, nC/m, ...), `SurfaceChargeDensity` (C/m², µC/cm², mAh/cm², ...), and `VolumeChargeDensity` (C/m³, C/cm³, Ah/L, ...), with `ElectricFluxDensity` as a role of `SurfaceChargeDensity`.
  A polarization density reads as a `SurfaceChargeDensity`.
- **Kinematics and rotation:**
  `Jerk` (m/s³, mm/s³), `Snap` (m/s⁴, mm/s⁴), `AngularAcceleration` (rad/s², tr/s², °/s², rpm/s), and `AngularJerk` (rad/s³, tr/s³, °/s³).
  `MomentOfInertia` (kg·m², kg·cm², g·cm², lb·ft², lb·in²), `AngularMomentum` (kg·m²/s, N·m·s), and `FirstMomentOfMass` (kg·m, g·cm, g·mm, oz·in), the unbalance of a rotor.
  `kg·m²` carries the scale `(2 pi) ** 2`, the way `N·m` carries `2 pi`, so a datasheet value is typed as written.
  The powers of a duration and of a rate, so that a product of three factors has one value in every order: `TimeSquared` (s², ms², µs², ns², min², h²), `TimeCubed` and `TimeFourthPower` (the same units), and `AngularVelocitySquared` (rad²/s², tr²/s², °²/s²).
- **Mechanics:**
  `SpecificEnergy` (J/kg, Wh/kg, cal/kg), `Momentum` (SI, CGS, and FPS), `Impulse` (N·s, mN·s, kN·s, dyn·s, lbf·s), `VelocitySquared`, `VolumetricFlowRate`, and `MassFlowRate`.
  `DynamicViscosity` (Pa·s, mPa·s, µPa·s, P, cP) and `KinematicViscosity` (m²/s, mm²/s, cm²/s, µm²/s, St, cSt).
  A thermal diffusivity and a diffusion coefficient read as a `KinematicViscosity`.
  `SurfaceTension` (N/m, mN/m, kN/m, dyn/cm) and its role `Fluence` (J/m², MJ/m², J/cm², mJ/cm², µJ/cm², Wh/m², kWh/m²), the two kinds of one dimension.
  A stiffness, a line load, and an interfacial tension read as a `SurfaceTension`, and a radiant exposure and an insolation as a `Fluence`.
- **Thermodynamics:**
  `HeatingRate` (K/s, °C/s, °F/s), `HeatCapacity` (J/K, kJ/K, cal/K, kcal/K), and `SpecificHeatCapacity` (J/(kg·K), kJ/(kg·K), cal/(g·K)).
  `HeatFlux` (W/m², kW/m², mW/cm², ...) and `ThermalConductivity` (W/(m·K), mW/(m·K), W/(cm·K)).
  An irradiance and a sound intensity read as a `HeatFlux`.
  `Entropy` and `SpecificEntropy` are closed roles of them, so that `Entropy * TemperatureDelta` is refused and never silently an `Energy`.
  `MolarHeatCapacity` (J/(mol·K), kJ/(mol·K), cal/(mol·K)) and its role `MolarEntropy`, the quantities the molar gas constant and the entropy tables of chemistry are measured in.
  A degree Celsius in a denominator is a kelvin, so `J/°C` and `J/(kg·°C)` are accepted spellings.
  The `thermodynamics` units package moves up the layering order, because it builds on the energy units.
- **Chemistry:**
  `MolarMass`, `MolarConcentration` (M, mM, µM, nM), `MolarEnergy`, `EntitiesPerAmount`, `Molality`, `MolarVolume`, `MolarFlowRate`, `CatalyticActivity` (katal and enzyme unit, a role of `MolarFlowRate`), and `MolarCharge`.
  Ambiguous bare spellings `Da`, `u`, `ppm`, `IU`, and molal `m` are refused.
- **Radiation:**
  `AbsorbedDose` (gray, rad), `EquivalentDose` (sievert, rem), and `Exposure` (roentgen), the first two roles of `SpecificEnergy` and the last a role of the new `SpecificCharge` (C/kg, Ah/kg, mAh/g).
  `AbsorbedDoseRate` (Gy/h, rad/h), `EquivalentDoseRate` (Sv/h, rem/h), and `ExposureRate` (R/h), roles of the new `SpecificPower` (W/kg) and `SpecificCurrent` (A/kg).
  `ActivityConcentration` (Bq/m³, Bq/L, pCi/L), `SpecificActivity` (Bq/kg, pCi/g, Ci/g), and `SurfaceActivity` (Bq/cm², dpm/100 cm², Ci/km²), principal kinds of their own dimensions.
  The `radiation` package moves up the layering order, because it builds on mechanics and electromagnetics.
- **Photometry:**
  `SolidAngle` (steradian, square degree), `LuminousFlux` (lumen), `Illuminance` (lux, phot, foot-candle), `LuminousEnergy` (talbot), `LuminousExposure`, `Luminance` (nit, stilb, foot-lambert), and `LuminousEfficacy` (lm/W).

#### New units of existing quantities

- **Length:**
  `Parsec`, `Kiloparsec`, `Megaparsec`, and `Gigaparsec`.
  A parsec is exactly 648000/pi astronomical units, held as that quotient with pi to 100 decimal places, and the multiples of it are exact.
  The spelling `pc` is a parsec, where it was refused before.
- **Temperature:**
  `Rankine` and `DeltaRankine`: a Rankine degree is exactly 5/9 of a kelvin, and 0 °R is absolute zero, so 0 °F is exactly 459.67 °R.
  The spellings `deg`, `degrees`, `degree`, and `Grad` stay ambiguous between the scales and are refused.
- **Volume and density:**
  `CubicFoot` and `UsGallon`, and milligram-per-litre and microgram-per-litre density units.
- **Power:**
  `JoulePerMinute`, `JoulePerHour`, `KilojoulePerMinute`, `KilojoulePerHour`, `MegajoulePerHour`, and `GigajoulePerHour`, for consumption stated as an energy per minute or hour; each is an exact fraction of a watt.

#### New relationships

The quantities above take part in dimensional arithmetic, and the products and quotients below have a result.

- **Integer powers:**
  A linear quantity takes an integer power: `Metre(3) ** 2` is `SquareMetre(9)`, `Second(2) ** -1` is `Hertz(0.5)`, and `q ** 0` is `Ratio(1)`.
  A power is the product written out, so the rules of each step apply, and type checkers see the square, the cube, and the fourth power where those have a type.
- **Mechanics:**
  `Force / Length` and `Pressure * Length` are a `SurfaceTension`, and `SurfaceTension / Length` the `Pressure` of a curved interface.
  `Energy / Area` and `HeatFlux * Time` are a `Fluence`, `Fluence / Time` is a `HeatFlux`, and `Fluence * Area` an `Energy`.
- **Electromagnetics:**
  `Voltage * Time`, `MagneticFlux / Area`, `Charge / Voltage`, `Resistance * Time`, `Current / Length`, and `Permeability * MagneticFieldStrength` derive the electromagnetic quantities.
  `Voltage / Length`, `Force / Charge`, and `MagneticFluxDensity * Velocity` are an `ElectricFieldStrength`, and `Current / Area` and `VolumeChargeDensity * Velocity` a `CurrentDensity`.
  `Charge / Length`, `Charge / Area`, and `Charge / Volume` are the charge densities, and each steps to the next with a division by a `Length`.
  `Permittivity * ElectricFieldStrength` is an `ElectricFluxDensity`, `ElectricFluxDensity * Area` the `Charge` it encloses, and `ElectricFieldStrength * ElectricFluxDensity` an `EnergyDensity`, the product `E·D`.
  `MagneticFluxDensity * MagneticFieldStrength` is an `EnergyDensity`, the product `B·H`, and `Magnetization` stays refused in it.
  Both role families reuse their parent units through explicit conversions and dedicated unit tables.
- **Kinematics:**
  `Acceleration / Time` and `Velocity / TimeSquared` are a `Jerk`, `Jerk / Time` and `Acceleration / TimeSquared` a `Snap`, and `Time ** 3` and `Time ** 4` have a type.
  `AngularAcceleration / Time` is an `AngularJerk`.
  `Momentum * Time` and `Impulse * Time` are a `FirstMomentOfMass`.
  Each of these raised `UnrepresentableDimensionError` before.
- **Mechanics and thermodynamics:**
  `SpecificEnergy` derives from energy, pressure, density, and acceleration relationships, `HeatingRate` from temperature change and time, `Momentum` from `Mass * Velocity`, `Impulse` from `Force * Time`, `VelocitySquared` from `Velocity * Velocity`, and the flow rates from volume, mass, density, area, and velocity.
  `Pressure * VolumetricFlowRate` is a `Power`.
  `Pressure * Time` and `Density * KinematicViscosity` are a `DynamicViscosity`, and `Area / Time`, `Velocity * Length`, and `DynamicViscosity / Density` a `KinematicViscosity`, so the Reynolds number `v * L / nu` is a `Proportion`.
  `DynamicViscosity * Frequency` is a `Stress`, the shear stress of a shear rate `Velocity / Length`, and `Stress / Frequency` and `Stress * Time` the `DynamicViscosity` it measures.
  `Power / Area`, `Pressure * Velocity`, and `EnergyDensity * Velocity` are a `HeatFlux`, and `HeatFlux * Area` is a `Power`.
  `Energy / TemperatureDelta` is a `HeatCapacity`, `HeatCapacity / Mass` and `SpecificEnergy / TemperatureDelta` a `SpecificHeatCapacity`, and the heat `Q = m * c * dT` is an `Energy` however it is grouped.
  `HeatCapacity / AmountOfSubstance` and `MolarEnergy / TemperatureDelta` are a `MolarHeatCapacity`.
  `Entropy / Mass`, `Entropy / AmountOfSubstance`, and the matching products and quotients convert between the entropy roles and their divisors.
  `Force / Frequency` is an `Impulse`, the force times a period; the roles of `Frequency`, such as `Activity` and `SampleRate`, stay refused in it.
- **Chemistry:**
  Derived from `Mass / Amount`, `Amount / Volume`, `Energy / Amount`, `Amount / Mass`, `Volume / Amount`, `Amount / Time`, and `Charge / Amount`; `MolarConcentration * MolarMass` is a `Density`.
- **Radiation:**
  `Velocity * Acceleration`, `Power / Mass`, and `SpecificEnergy / Time` are a `SpecificPower`, and a dose rate times a `Time` is the matching dose.
  `Charge / Mass` is a `SpecificCharge`, and `SpecificCharge * MagneticFluxDensity` a `Frequency`.
  `Activity / Volume`, `Activity / Mass`, and `Activity / Area` are the activity densities, and so are `Frequency / Volume`, `Frequency / Mass`, and `Frequency / Area`.
  A `_rule` may name a role as an operand or as its result, which is how `Sievert(1) / Hour(2)` is a dose rate while `Sv * kg` stays refused.
- **Bridges across the angle axis:**
  [Where the radian meets a length](docs/concepts/angle_bridges.md) describes the model, and [Adding a bridge](docs/how-to/adding_a_bridge.md) how one is declared.
  `AngularVelocity * Length` is a `Velocity`, `AngularAcceleration * Length` an `Acceleration`, `AngularJerk * Length` a `Jerk`, `Torque / Force` the lever arm, and `Torque / Length` the force at it.
  `AngularVelocitySquared * Length` is the centripetal `Acceleration`, a bridge with the factor `(2 pi) ** 2`.
  `AngularDisplacement * Length` is the arc swept, and an arc over its angle the radius.
  A `MomentOfInertia` divides back into its mass, area, radius, and unbalance.
- **Rotational dynamics:**
  `Mass * Area` is a `MomentOfInertia`, and so is a mass at a radius in any order: `m * r * r`, `r * m * r`, and `m * r ** 2`.
  `MomentOfInertia * AngularAcceleration` is a `Torque`, `MomentOfInertia * AngularVelocity` and `Torque * Time` an `AngularMomentum`, and `0.5 * I * omega * omega` an `Energy`.
  `AngularVelocity * Velocity` is the centripetal `Acceleration`, `AngularVelocity * Momentum` the centripetal `Force`, and `FirstMomentOfMass * AngularVelocity` the `Momentum` of an unbalance on its circle, so `GramMillimetre(30) * omega * omega` is the force an unbalance pulls the axis with.
  `AngularVelocity * Frequency` is an `AngularAcceleration`.
- **Named relations:**
  `AngularVelocity.from_tangential(velocity, radius)`, since `Velocity / Length` is a `Frequency`, and `AngularDisplacement.from_arc(arc, radius)`, since `Length / Length` is a ratio.
  `Entropy.from_heat(heat, temperature)` is `dS = Q / T` for an `Energy` and an absolute `Temperature` on any scale, and raises `InvalidMeasurementError` at absolute zero.
  `EquivalentDose.from_absorbed_dose(dose, weighting_factor)` and `EquivalentDoseRate.from_absorbed_dose_rate(rate, weighting_factor)` take a plain `Proportion`, and are the only way from grays to sieverts.
  The `Frequency.to_angular_velocity()` docstring notes that a radian rate such as `v / r` reads two pi times too fast through it.
- **Conversions:**
  Explicit conversions between contested kinds: `Impulse` and `Momentum`, and `VelocitySquared` and `SpecificEnergy`, the latter accounting for the factor of two in kinetic energy.
  Between a role and its parent: `to_magnetization()`, `to_electric_flux_density()`, `to_entropy()`, `to_specific_energy()`, `to_molar_flow_rate()`, and their inverses.
  An `EquivalentDose` has no way into a `SpecificEnergy`, and a sievert times a kilogram is refused.
- **Dimensional model:**
  Solid angle is an independent dimension axis, so photometric arithmetic distinguishes luminous intensity from luminous flux and derives illuminance and luminance separately.
  `Area / Area` remains a `Proportion`.

#### New constants

- **Boltzmann constant (k_B) and molar gas constant (R):**
  `BOLTZMANN_CONSTANT` (an `Entropy`, 1.380649e-23 J/K, exact) and `MOLAR_GAS_CONSTANT` (a `MolarEntropy`, 8.31446261815324 J/(mol·K), exact) in `codata_2022`.
  CODATA prints the gas constant with a trailing ellipsis because it shows a prefix: the product of the two exact defining constants has exactly those 15 digits, and the library stores all of them.
  `AVOGADRO_CONSTANT * BOLTZMANN_CONSTANT` is `MOLAR_GAS_CONSTANT` by a rule, with no rounding, and the two quotients return the other factor.
- **Avogadro and Faraday constants:**
  `AVOGADRO_CONSTANT` and `FARADAY_CONSTANT` in `codata_2022`, for entity counts and molar charge calculations.
- **Electromagnetic and atomic constants:**
  `PLANCK_CONSTANT` and `REDUCED_PLANCK_CONSTANT` (one `AngularMomentum`, per turn and per radian, so `h / (2 pi)` is exact), `VACUUM_ELECTRIC_PERMITTIVITY`, `VACUUM_MAGNETIC_PERMEABILITY`, `CHARACTERISTIC_IMPEDANCE_OF_VACUUM`, `FINE_STRUCTURE_CONSTANT`, `ATOMIC_MASS_CONSTANT`, and `BOHR_RADIUS`, the constants the electromagnetic and angular-momentum kinds made expressible.
- **Radiation weighting factors:**
  `kuchka.constants.icrp_103` holds the radiation weighting factors of ICRP Publication 103 as proportions.

### Changed

#### Unit modules live in themed packages

`kuchka.units` keeps the base dimensions and the angle, solid angle, proportion, and logarithmic axes at its top level, and groups the other modules in `geometry`, `kinematics`, `mechanics`, `electromagnetics`, `information`, `photometry`, and `radiation`.
Every constructor and table is still imported from `kuchka` and `kuchka.units`.
A unit module is imported from its package, so `from kuchka.units import voltage` is now `from kuchka.units.electromagnetics import voltage`, and `kuchka.units.kinematics.force` is now `kuchka.units.mechanics.force`.

The quantity types follow the same layout, one module per type in the matching package of `kuchka.quantities`: `kuchka.quantities.electrical.Voltage` is now `kuchka.quantities.electromagnetics.voltage.Voltage`, and `Force`, `Power`, and `Torque` are in `kuchka.quantities.mechanics`.
A quantity now pickles by the name `kuchka.quantities` publishes its class under, so a pickle no longer depends on the module that defines the class and survives such a move.
A pickle made by an earlier version names the old module and does not load when its class moved.

#### Astronomical mass units follow CODATA 2022

`SolarMass` is exactly 1.988410e30 kg, where it was 1.988416e30 kg: the IAU 2015 nominal solar mass parameter over the CODATA 2022 gravitational constant, to seven significant digits, the way `EarthMass` was already derived.
The value was 3 ppm higher than that derivation gives.
Tests tie `Dalton`, `EarthMass`, `SolarMass`, and the constants of `codata_2022` to the listing the package ships, so a new CODATA adjustment that moves one of them fails a test until the value is updated on purpose.

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

## [0.1.2] - 2026-09-22

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
