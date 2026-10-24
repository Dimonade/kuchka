# kuchka

A small pile of strongly-typed physical quantities and engineering units for Python.

`kuchka` turns engineering values into first-class Python types instead of raw numbers.
`Volt(5)` returns a `Voltage`; `Kilogram(1000)` returns a `Mass`; `Mass * Acceleration` returns a `Force` automatically, and that physical meaning travels with the value through the rest of your code.
`mypy`/`ty` can catch a `Current` passed where a `Voltage` is expected before the program ever runs, and runtime checks cover the boundaries static analysis can't see: configuration data, hardware readings, unit conversion, dimensional arithmetic.
Existing projects can adopt this incrementally, by typing the values and interfaces that matter first.

Here's a small example that goes from an electrical measurement straight to a duration, using Ohm's law and a battery's rated charge capacity:

```python
from kuchka import AmpereHour
from kuchka import Ohm
from kuchka import Volt
from kuchka.units import HOUR

supply = Volt(3.7)
load = Ohm(148)
battery = AmpereHour(2)

current = supply / load  # Ohm's law -> Current.
runtime = (battery / current).to(HOUR)  # Charge / Current -> Time.

print(current)
# 0.025 A
print(runtime)
# 80 h
```

The important part is not the arithmetic itself.
Each result is a real `kuchka` quantity, and the relationships between the inputs determine the resulting physical type.
The same dimensional machinery is used whether the calculation is mechanical, electrical, geometric, or signal-related.

## Installation

```bash
uv add kuchka
```

or:

```bash
pip install kuchka
```

Application code should normally import from the top-level `kuchka` package.
The development toolchain described later is separate from the package's runtime dependencies.

## Quick start

The useful part of `kuchka` is not just unit conversion.
Values acquire a physical type, typed quantities can cross application boundaries, and ordinary arithmetic can produce other physical quantities.

### 1. Type the values your application is already using

A unit constructor such as `Volt` creates a `Voltage`; `Milliampere` creates a `Current`.
The unit is part of construction, while the resulting object has the physical quantity type.

```python
from kuchka import Ampere
from kuchka import Milliampere
from kuchka import Millivolt
from kuchka import Volt
from kuchka import Voltage

supply = Volt(5)
load = Milliampere(150)
power = supply * load

print(power)
# 0.75 W


def check_supply(voltage: Voltage) -> bool:
    return voltage >= Volt(3)


check_supply(Volt(5))  # valid.
check_supply(Millivolt(4200))  # valid.
check_supply(Ampere(2))  # static type error (`IncompatibleDimensionError`).
check_supply(4.2)  # static type error (`IncompatibleDimensionError`).
```

The type annotation gives static tools the contract.
The comparison inside the function also exercises `kuchka`'s runtime dimensional checks when the function is called with an incompatible value.
Python function annotations themselves remain ordinary annotations; `kuchka` does not add a runtime annotation enforcement mechanism.

This is the basic idea: application functions can name the physical quantity they expect instead of accepting an unqualified `float`.

### 2. Validate units when data enters from configuration

Configuration formats have to represent units as data.
That does not mean the rest of the application has to become stringly typed.
Resolve the unit once at the boundary, then construct a typed value.

For example:

```toml
# device.toml
led_critical_voltage = { value = "2800", unit = "mV" }
```

The corresponding loader can use `VOLTAGE_UNITS`, which contains only voltage units:

<!-- doc-test: skip reads device.toml from disk -->

```python
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import tomllib

from kuchka import Voltage
from kuchka.units import VOLTAGE_UNITS


@dataclass(frozen=True)
class DeviceConfig:
    led_critical_voltage: Voltage


def parse_voltage(raw: Mapping[str, str]) -> Voltage:
    try:
        constructor = VOLTAGE_UNITS[raw["unit"]]
    except KeyError as exc:
        raise ValueError(f"invalid voltage unit: {raw['unit']!r}") from exc

    return constructor(Decimal(raw["value"]))


with Path("device.toml").open("rb") as file:
    raw = tomllib.load(file)

config = DeviceConfig(led_critical_voltage=parse_voltage(raw["led_critical_voltage"]))
```

This is accepted:

```toml
led_critical_voltage = { value = "2800", unit = "mV" }
```

This is rejected while loading because `mA` is not a member of the voltage unit table:

```toml
led_critical_voltage = { value = "150", unit = "mA" }
```

The same boundary pattern exists for the other quantity families through their corresponding `*_UNITS` mappings.
`kuchka` therefore allows strings where the data format requires them without making strings the normal application API.

The tables accept the notations that real files use, so these all resolve to the same temperature unit:

```python
from kuchka.units import TEMPERATURE_UNITS

for text in ("°C", "C", "degC", "degrees C", "Degrees Celsius"):
    constructor = TEMPERATURE_UNITS[text]
    constructor(21.5)  # 21.5 °C
```

Symbols such as `mV` are compared exactly, because `mV` and `MV` are different units, and spoken forms such as `degrees celsius` are compared ignoring case.
A spelling that could mean more than one unit in a table, like `deg` for temperature, is refused rather than guessed.
See [Unit spellings](docs/concepts/unit_spellings.md).

When the whole value arrives as one string, `parse` reads the number and the unit together through the table of the type you name:

```python
from fractions import Fraction

from kuchka import Temperature, Volt, Voltage, parse

parse("5 mV", Voltage)  # 5 mV
parse("-40 °C", Temperature)  # -40 °C
parse("0.1 V", Voltage) == Volt(Fraction(1, 10))  # True: the number is read exactly
```

The caller names the type because the same text can mean different quantities: `"5 s"` is a `Time`, an `Instant`, or a `SamplingPeriod`, so there is no untyped `parse`.
Text that is no measurement of that type raises a `ParseError`, and a unit the type does not have raises an `UnknownUnitError`.

### 3. Compose real engineering relationships

The library is useful when a calculation crosses more than one physical domain. For example, an actuator calculation can derive several quantities in sequence:

```text
Voltage * Current -> Power
Mass * Acceleration -> Force
Force / Area -> Pressure
Pressure * Volume -> Energy
Energy / Volume -> EnergyDensity
Torque * AngularDisplacement -> Energy
Torque * AngularVelocity -> Power
AngularDisplacement / Time -> AngularVelocity
Mass / Volume -> Density
Length * Length -> Area
Area * Length -> Volume
```

That means a calculation can move through a chain such as:

```python
from kuchka import Centimetre
from kuchka import Kilogram
from kuchka import MetrePerSecondSquared
from kuchka import SquareCentimetre

mass = Kilogram(1000)
acceleration = MetrePerSecondSquared(0.5)
piston_area = SquareCentimetre(20)
stroke = Centimetre(10)

force = mass * acceleration
pressure = force / piston_area
volume = piston_area * stroke
energy = pressure * volume

print(force)
# 500 N
print(pressure)
# 250000 Pa
print(volume)
# 0.0002 m³
print(energy)
# 50 J
```

No unit strings or manual conversion factors are needed in the calculation.
The operators determine the physical result types.

### 4. Bring raw sensor data into a control path

A hardware driver may naturally return a plain integer or float.
Give that value a physical type at the hardware boundary, then keep the control logic typed:

```python
from kuchka import Ampere
from kuchka import Milliohm
from kuchka import Millivolt

SHUNT_RESISTANCE = Milliohm(100)
OVERCURRENT_LIMIT = Ampere(1.5)


def handle_adc_sample(raw_shunt_voltage_mv: int) -> None:
    shunt_voltage = Millivolt(raw_shunt_voltage_mv)
    current = shunt_voltage / SHUNT_RESISTANCE

    if current >= OVERCURRENT_LIMIT:
        emergency_shutoff()
```

For a raw sample of `187 mV`, the calculation produces `1.87 A`.
The control decision compares a typed `Current` with a typed current limit, so the two values carry explicit engineering meaning instead of relying on unrelated numbers such as `187` and `1.5`.

This is the intended boundary pattern for `kuchka`: attach physical meaning when data enters the application, then let Python typing and dimensional arithmetic carry that meaning through the rest of the code.

## Take a tour

The examples above use linear engineering quantities, but `kuchka` is broader than a unit-conversion helper.
Quantities have different arithmetic shapes, and the shape determines which operations make physical sense.

### Linear quantities

Most engineering quantities are linear: their units differ by a scale factor.
Addition, subtraction, scalar multiplication, and ordering behave like ordinary numbers.

```python
from kuchka import Millivolt
from kuchka import Volt

Volt(1) + Millivolt(200) == Volt(1.2)
# True
```

This includes quantities such as `Voltage`, `Current`, `Length`, `Mass`, `Time`, and many others.

### Affine quantities

Some values represent readings on a scale.

A reading minus a reading gives a linear delta, and adding a delta shifts the reading.
Adding two readings is rejected.

```python
from kuchka import Celsius
from kuchka import DeltaCelsius

Celsius(25) - Celsius(20) == DeltaCelsius(5)
Celsius(20) + DeltaCelsius(5) == Celsius(25)
Celsius(20) + Celsius(5)  # rejected: `MeasurementError`.
5 * Celsius(5)  # rejected: there is no `__mul__` defined (`TypeError`).
```

Temperatures below absolute zero are rejected as invalid measurements:

```python
from kuchka import Celsius
from kuchka import Fahrenheit
from kuchka import Kelvin

Kelvin(-1)  # raises `InvalidMeasurementError`.
Celsius(-274)  # raises `InvalidMeasurementError`.
Fahrenheit(-460)  # raises `InvalidMeasurementError`.
Kelvin(0)  # valid.
```

`Instant` follows the same shape, reached from any `Time` value:

```python
from kuchka import Second, Millisecond

reading = Second(1_700_000_000).to_instant()
reading + Millisecond(500)  # -> Instant, 500 ms later
reading - Second(100).to_instant()  # -> Time(1_699_999_900)
reading + reading  # rejected: `MeasurementError`.
```

`Time.to_instant()` and `Time.to_sampling_period()` work at whatever prefix the `Time` value was already constructed with:

```python
from kuchka import Hour, Minute

Hour(1).to_instant() == Second(3600).to_instant()
Minute(1).to_sampling_period() == Second(60).to_sampling_period()
```

An `Instant` carries no calendar or epoch of its own.
Where its zero point falls is up to whatever the value is being used to represent.

### Modular quantities

Some quantities wrap around after a fixed period.
`Angle` is the current example.

```python
from kuchka import Degree

Degree(350) + Degree(20) == Degree(10)
Degree(300).difference(Degree(350)) == Degree(-50)
Degree(10) < Degree(20)  # rejected: no total order on a circle (`TypeError`).
```

`+` and `-` use ordinary wraparound arithmetic.
`difference()` is the separate shortest-signed-path operation.

### Logarithmic quantities

Ratios that engineers quote on a logarithmic scale are levels.
`LogarithmicRatio` is the current example: a gain, an attenuation, a signal-to-noise ratio.

Multiplying two ratios adds their levels, so stages in series combine by plain addition, exactly:

```python
from kuchka import Decibel

Decibel(20) + Decibel(-3.5) + Decibel(-1.5) == Decibel(15)
Decibel(-0.2) * 30 == Decibel(-6)  # 0.2 dB per metre over 30 metres.
Decibel(20.3).is_close(Decibel(20), tolerance=Decibel(0.5))  # a gain tolerance check.
Decibel(3) * Decibel(3)  # rejected: two levels do not multiply (`TypeError`).
```

Converting to or from the linear ratio a level describes goes through a logarithm, so it comes in two flavours: `10 ** (level / 10)` for power quantities and `10 ** (level / 20)` for field quantities such as voltage.

```python
from kuchka import Decibel, LogarithmicRatio, Ratio

Decibel(30).to_power_ratio() == Ratio(1000)  # whole decades are exact.
Decibel(40).to_field_ratio() == Ratio(100)
LogarithmicRatio.from_power_ratio(Ratio(100)) == Decibel(20)
```

Levels that are not whole decades convert to the precision of the active `decimal` context.

See [Quantity shapes and semantics](docs/concepts/quantity_shapes.md) for the full semantics.

## Why `kuchka`?

A raw `float` does not remember what it means.
Passing floats through an engineering pipeline makes unit mistakes easy to write and hard to catch because the code remains syntactically valid even when it is semantically wrong.

Consider:

```python
voltage_mv = 4200
current_ma = 150
power_w = voltage_mv * current_ma
```

This looks reasonable at first glance, but `4200 mV * 150 mA` is `630 mW`, not `630000 W`.
The mistake is hidden because the units exist only in variable names.

With `kuchka`, physical meaning is part of the value itself:

```python
voltage = Millivolt(4200)
current = Milliampere(150)
power = voltage * current

power  # 0.63 W
type(power)  # `<class 'kuchka.quantities.electrical.Power'>`
```

A function can require `Voltage`, a configuration loader can construct a `Voltage`, and an engineering formula can produce a `Power`.
The unit does not have to be carried in a variable name, a comment, or an application-specific string convention.

That is the niche `kuchka` is aiming for: a curated set of engineering quantities that behave as ordinary Python types and are checked by ordinary Python type checkers, with runtime validation still available at untyped boundaries.

This is deliberately narrower than a general-purpose unit language.
`kuchka` does not try to accept arbitrary unit expressions, provide a mutable application-wide unit registry, or make every physical quantity array-native.
Those are useful capabilities, but they optimize for a different problem.
See [Comparison with existing tools](docs/comparison.md) for the trade-offs.

## Where `kuchka` fits

`kuchka` is aimed at engineering application code where the physical vocabulary is known ahead of time and correctness matters more than arbitrary unit flexibility.
Typical examples include device configuration, hardware interfaces, control logic, protocol handling, test infrastructure, and reports.

It is less suited to scientific workloads where quantities are primarily NumPy arrays, units are user-defined or discovered at runtime, or arbitrary compound units need to be parsed.
In those cases, an established general-purpose library may fit the problem better.

The point is not to replace every unit library.
The point is to make one particular style of engineering code feel natural: ordinary Python functions taking and returning ordinary Python types that happen to carry physical meaning.

## What's included in 0.1.x

`kuchka` currently covers a growing vocabulary of engineering and scientific quantities.
Units are represented as typed values, with exact conversions where the unit definition permits them.

The tables below show a number of representative units per field or domain.
The complete unit vocabulary is available in the API reference.

### Electrical

| Quantity             | Representative units                                                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Voltage              | `Nanovolt` though `Petavolt`                                                                                       |
| Current              | `Picoampere`, through `Megaampere`                                                                                 |
| Power                | `Picowatt` through `Petawatt`, `Horsepower` and `MetricHorsepower`                                                 |
| Apparent Power       | `MillivoltAmpere` through `GigavoltAmpere`                                                                         |
| Reactive Power       | `Millivar` through `Gigavar`                                                                                       |
| Resistance           | `Microohm`, through `Gigaohm`                                                                                      |
| Conductance          | `Nanosiemens` through `Kilosiemens`                                                                                |
| Charge               | `Picocoulomb` through `Coulomb`, `MilliampereSecond`, `MilliampereHour`, `AmpereHour`                              |
| Energy               | `Picojoule` through `Petajoule`, `Electronvolt` through `Teraelectronvolt`, `MilliwattHour` through `KilowattHour` |
| _energy, countinued_ | `Erg`, `Calorie`, `Kilocalorie`, `TonneOfTNT` through `MegatonneOfTNT`                                             |

### Time and signals

| Quantity          | Representative units                                                                                  |
| ----------------- | ----------------------------------------------------------------------------------------------------- |
| Time              | `Femtosecond` through `Second`, `Minute` through `JulianYear`, and `Jiffy`                            |
| Instant           | reached via `Time.to_instant()`                                                                       |
| Frequency         | `Nanohertz` through `Petahertz`                                                                       |
| Sampling Period   | reached via `Time.to_sampling_period()`                                                               |
| Sample Rate       | `SamplesPerSecond`, `KilosamplesPerSecond`, `MegasamplesPerSecond`                                    |
| Baud Rate         | `Baud` through `Gigabaud`                                                                             |
| Activity          | `Millibecquerel` through `Terabecquerel`, `Curie`, `Millicurie`, `Microcurie`, and `Picocurie`        |
| Data              | `Bit` and `Byte`, `Kilobyte` through `Petabyte`, `Kibibyte` through `Pebibyte`, and the same for bits |
| Data Rate         | `BitPerSecond` and `BytePerSecond`, with the same SI and IEC multiples                                |
| Temperature       | `Celsius`, `Fahrenheit`, `Kelvin`                                                                     |
| Temperature Delta | `DeltaCelsius`, `DeltaFahrenheit`, `DeltaKelvin`                                                      |

### Geometry and mechanics

| Quantity       | Representative units                                                                                                                               |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Length         | `Picometre` through `Kilometre`, `Inch` and other exact imperial units, `AstronomicalUnit` and `LightYear`                                         |
| Area           | `SquareMillimetre` through `SquareKilometre`, `Hectare`, `Acre`                                                                                    |
| Volume         | `CubicMillimetre` through `CubicMetre`, `Microlitre`, `Millilitre`, `Litre`, `Kilolitre`                                                           |
| Velocity       | `MetrePerSecond`, `KilometrePerHour`, `MilePerHour`, `Knot`                                                                                        |
| Acceleration   | `MetrePerSecondSquared`, `Microgal` through `Gal`                                                                                                  |
| Mass           | `Nanogram` through `Megagram`, `Tonne`, along with `SolarMass` and `EarthMass`                                                                     |
| Force          | `Micronewton` through `MegaNewton`, `Dyne`, `PoundForce`, and `KilogramForce`                                                                      |
| Density        | `KilogramPerCubicMetre`, `GramPerCubicCentimetre`, `KilogramPerLitre`                                                                              |
| Pressure       | `Pascal`, `Hectopascal`, `Kilopascal`, `Megapascal`, `Gigapascal`, `Bar`, `Millibar`, `Atmosphere`, `PoundPerSquareInch`, `KilopoundPerSquareInch` |
| Stress         | the units of Pressure, reached with `Pressure.to_stress()`                                                                                         |
| Energy density | `JoulePerCubicMetre`, `KilojoulePerCubicMetre`, `MegajoulePerCubicMetre`, `WattHourPerLitre`                                                       |

### Angle and rotation

| Quantity             | Units                                                                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Angle                | `Radian`, `Degree`, `Turn`, `Gradian`, `ArcMinute`, `ArcSecond`                                                                         |
| Angular displacement | `RadianDisplacement`, `DegreeDisplacement`, `TurnDisplacement`, `GradianDisplacement`, `ArcMinuteDisplacement`, `ArcSecondDisplacement` |
| Angular velocity     | `RadianPerSecond`, `DegreePerSecond`, `TurnPerSecond`, `RevolutionPerMinute`                                                            |
| Torque               | `NewtonMetre`, `MillinewtonMetre`, `KilonewtonMetre`, `PoundForceFoot`, `PoundForceInch`, `JoulePerTurn`                                |

### Chemistry and light

| Quantity            | Units                           |
| ------------------- | ------------------------------- |
| Amount of Substance | `Femtoomole` through `Kilomole` |
| Luminous Intensity  | `Candela`                       |

### Dimensionless quantities

| Quantity         | Units              |
| ---------------- | ------------------ |
| Proportion       | `Ratio`, `Percent` |
| LogarithmicRatio | `Decibel`, `Bel`   |

Most SI-derived families expose a selected set of SI prefixes appropriate to their engineering use.
The README does not list every prefix individually;the API reference contains the complete constructor and unit vocabulary.

The canonical spelling of SI `metre` is used throughout `kuchka`.
American-English `*meter` names are aliases of the corresponding `*metre`
constructors, not separate unit implementations. The same principle applies
to `Litre`/`Liter` and other spelling aliases.

### Archaic and historical units

Historical, regional, and culturally specific units live apart from the main vocabulary, in `kuchka.units.archaic`.
They are imported explicitly from the module of their tradition and add nothing to the top-level namespace:

```python
from kuchka.units.archaic.russian.length import Arshin
from kuchka.units.length import CENTIMETRE

print(Arshin(3).to(CENTIMETRE))
# 213.36 cm
```

`parse` reads an archaic unit only when asked, and only from the modules that have been imported:

```python
from kuchka import Length, parse

parse("3 arshin", Length, allow_archaic=True)  # 3 arshin
```

`allow_archaic` takes an `ArchaicPolicy`, `Deny` by default or `Allow`, and `False` and `True` stand for them.
The error for a refused archaic unit says how to read it.

The traditions today are German (the Meilen), Hebrew, Japanese, and Russian.
See the [archaic units README](src/kuchka/units/archaic/README.md) for what each provides, and [How to extend kuchka](docs/how-to/README.md) for adding more.

## A few important distinctions

### Same dimension does not always mean the same concept

`Frequency`, `SampleRate`, and `BaudRate` all have physical dimension T⁻¹, but they remain separate types because they describe different concepts.

```python
from kuchka import Hertz
from kuchka import SamplesPerSecond

Hertz(50) + SamplesPerSecond(50)  # rejected: `IncompatibleDimensionError`.
```

Genuine reciprocal pairs remain reciprocal:

```python
from kuchka import Second

rate = 1 / Second(2).to_sampling_period()  # -> SampleRate
period = 1 / rate  # -> SamplingPeriod
```

For APIs that can accept either a `Frequency` or a `SampleRate`, `ConvertibleToFrequency` provides an explicit common protocol:

```python
from kuchka import ConvertibleToFrequency
from kuchka import Frequency


def nyquist_ok(signal: ConvertibleToFrequency, sample_rate: Frequency) -> bool:
    return signal.to_frequency() * 2 <= sample_rate
```

### Canonical types and domain-specific types

For a physical dimension, one type is canonical: the type produced by generic dimensional arithmetic.
Domain-specific types such as `SampleRate` and `BaudRate` remain available through explicit construction when the distinction matters to the application.

## Conversions

Use a unit definition when a value needs to be displayed or handed to a boundary in another unit:

```python
from kuchka import Volt
from kuchka.units import MILLIVOLT

voltage = Volt(5)

print(voltage.to(MILLIVOLT))
# 5000 mV

print(voltage)
# 5 V
```

There is no `voltage.to("mV")`.
Application code uses Python unit definitions.
String resolution belongs at boundaries such as configuration and import code, where the maintained `*_UNITS` mappings provide the bridge.

A conversion to another physical dimension is rejected:

```python
from kuchka import Volt
from kuchka.units import MILLIAMPERE

Volt(5).to(MILLIAMPERE)  # raises `InvalidConversionError`.
```

## Exact arithmetic

Every magnitude is stored as an exact `Fraction`, not a rounded floating-point approximation.
`Decimal` is materialized when a value needs decimal display.

Compare

```python
battery_a_volts = 0.1
battery_b_volts = 0.2
v_total = battery_a_volts + battery_b_volts

print(v_total)
# 0.30000000000000004, not 0.3.
```

with

```python
from kuchka import Volt

v_total = Volt(0.1) + Volt(0.2)
print(v_total)
# 0.3 V

v_total == Volt(0.3)
# True
```

or

```python
from fractions import Fraction
from kuchka import Litre
from kuchka.units import LITRE

q = Litre(Fraction(5, 18))
q.magnitude
# Fraction(1, 3600)

q.value_in(LITRE)
# Fraction(5, 18)
```

`.magnitude` always reads out in the quantity's canonical unit - `CubicMetre` for `Volume`, here - not the unit it was constructed with.
The construction is still exact: `5/18` litre becomes `5/18 * 1/1000 = 1/3600` cubic metre with no rounding at any step.
`.value_in(unit)` is what recovers the value in a specific unit, litres in this case.

`float` input is parsed through its string representation, so `Volt(4.2)` preserves the digits written by the programmer instead of storing the binary floating-point representation of the float.

### Angles and pi

`Turn` is the canonical angle unit, and `Degree`, `Gradian`, `ArcMinute`, and `ArcSecond` are exact fractions of a turn, so none of them involves pi.
Only `Radian` does: it converts with pi held as an exact rational to 100 decimal places, so every digit a conversion displays is correct.

```python
import math

from kuchka import Degree
from kuchka import Radian

Degree(90) + Degree(45) == Degree(135)  # exact.
Radian(math.pi) == Degree(180)  # False: a float is not exactly pi.
```

### Comparing with a tolerance

`==` asks whether two values are the same number, so a float that carries rounding error is never equal to its ideal value.
`is_close` asks whether two values are near enough, with the tolerance written down as a quantity:

```python
import math

from kuchka import Degree
from kuchka import Millivolt
from kuchka import Radian
from kuchka import Volt

Volt(0.1 + 0.2) == Volt(0.3)  # False
Volt(0.1 + 0.2).is_close(Volt(0.3), tolerance=Millivolt(1))  # True
Radian(math.pi).is_close(Degree(180), tolerance=Radian(1e-12))  # True
```

The tolerance has no default and is a quantity of the right type (a `TemperatureDelta` for a `Temperature`), so a bare number is rejected.
See [Exactness, angles, and tolerance](docs/concepts/exactness.md) for why equality stays exact and how each shape measures distance.

## Physical constants

`kuchka.constants` provides curated sets of `kuchka`-typed physical constants.
The initial implementation of one such set is `kuchka.constants.codata_2022`.

```python
from kuchka import Hertz
import kuchka.constants.codata_2022 as kc

wifi_wavelength = kc.SPEED_OF_LIGHT_IN_VACUUM / Hertz(2_400_000_000)
# Length: about 0.1249 m
```

Some constants are exact by definition; others are CODATA 2022 recommended values.
Each constant documents its own status and published precision.

## Errors

Application-level measurement errors derive from `MeasurementError`:

| Error                           | Raised when                                                                                                     |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `InvalidMeasurementError`       | a constructor receives a non-numeric value, a `bool`, or an invalid measurement such as a temperature below 0 K |
| `IncompatibleDimensionError`    | incompatible quantities or concepts are combined                                                                |
| `InvalidConversionError`        | `.to(...)` receives a unit that is not valid for the quantity                                                   |
| `DivisionByZeroError`           | a measurement is divided by zero, or the reciprocal of zero is taken; also a `ZeroDivisionError`                |
| `UnrepresentableDimensionError` | arithmetic produces a dimension without a registered engineering type                                           |
| `PlannedDimensionError`         | an unregistered dimension already has a named future type                                                       |
| `AmbiguousKindError`            | arithmetic produces a dimension shared by several kinds, none of them principal                                 |
| `ParseError`                    | `parse` receives text that is no measurement of the type, or a unit that two tables claim; also a `ValueError`  |
| `UnknownUnitError`              | `parse` receives a unit that the quantity type does not have                                                    |

Catching `MeasurementError` handles the whole family at once.

## Formatting

Quantities support Python's format mini-language.
The specification is applied to the magnitude materialized in the current display unit, and the unit symbol is appended afterwards.

```python
from kuchka import Volt

voltage = Volt(1234.5)

f"{voltage}"  # "1234.5 V"
f"{voltage:.2f}"  # "1234.50 V"
f"{voltage:.2e}"  # "1.23e+3 V"
f"{voltage:,.2f}"  # "1,234.50 V"
```

The text depends on the value and the specification alone.
The precision, rounding mode, and traps of the active `decimal` context do not affect it.
The magnitude is rounded once, from its exact value, and a tie rounds away from zero: `f"{Volt(2.665):.2f}"` is `"2.67 V"`.
Without a precision, a value that has no finite decimal form shows 28 significant digits, so `repr(Volt(Fraction(1, 3)))` is `"0.3333333333333333333333333333 V"`.

## Examples

The repository contains longer, task-oriented examples:

- **[Migrating a config from unit-suffixed keys to `kuchka`](docs/examples/config_migration/README.md)** - moves units from names such as `accepted_voltage_min_mv` into TOML data and resolves them into typed dataclasses at the boundary.
- **[Working around an unrepresentable intermediate dimension](docs/examples/unrepresentable_dimensions/README.md)** - shows how to handle formulas such as `P = V²/R` and parallel resistor networks when an intermediate dimension has no registered type.

These examples show `kuchka` in application code, with arithmetic serving the larger engineering task.

## Performance

`kuchka` uses exact rational arithmetic (`Fraction`) for correctness.
The intended use is at configuration, application, control, and reporting boundaries, not inside a per-sample hot loop processing live streams at very high rates.

See [`benchmarks`](benchmarks/README.md) for current measurements.

## What this is not yet

The vocabulary is intentionally curated and will remain finite. Current gaps include:

- There is no NumPy/Pandas integration.
- There is no JSON/DB persistence layer.

A future persistence layer may use a representation such as `{"value": 4.2, "unit": "V"}` at the serialization boundary while reconstructing a typed quantity when data enters application code.

Quantities have no exponentiation:
`Second(2) ** 2` raises a `TypeError`.
Multiply the factors instead, since every step lands on a registered type: `v0 * t + a * t * t / 2` is a `Length`.

## Stability

`kuchka` is currently `0.1.x`.
Breaking changes are expected while the API settles.

From `0.2.0` onward, `kuchka` follows ordinary semantic versioning: a minor release will not break existing code, and a breaking change comes with a major version bump.

### Compatibility

`kuchka` supports Python 3.11 and later, and its tests run on every release from 3.11 to 3.15.

The types are written for code that other type checkers read, and what is promised is what is tested:

| Checker | Checked against                                                                              |
| ------- | -------------------------------------------------------------------------------------------- |
| mypy    | the oldest supported release, 1.11, and the newest                                           |
| pyright | the newest release                                                                           |
| ty      | the library's own source only: `ty` is `0.0.x`, so its results on user code are not promised |

On every change, mypy and pyright are each asked about a representative set of operand pairs and every operator, and must agree with the runtime: it infers the type the runtime returns, and it refuses what the runtime refuses, such as a quantity of another dimension, a plain number, or a comparison across types.
A fixture of lines that must be accepted and lines that must be rejected is held to the same rule.
The library's own source passes `mypy --strict` from 1.11 on.
Earlier mypy releases, back to 1.5, gave the same answers on consumer code when they were tried, but they are not tested on every change, and they cannot check the library's own source.

Raising the oldest supported checker is recorded in the changelog.

## Development

`uv sync` installs the `dev` dependency group (`ruff`, `mypy`, `ty`, `pytest`, `hypothesis`, `coverage`, and editor tooling) alongside `kuchka` itself.

```bash
uv sync

uv run pytest --doctest-modules src/kuchka
uv run pytest
uv run mypy --strict src/kuchka
uv run ty check src/kuchka tests
uv run coverage run -m pytest && uv run coverage report
```

`just test` runs the doctests and the test suite, `just check` runs the generated-API check, `ruff`, `mypy --strict`, and `ty`, and `just ct` (or `just covtest`) runs the full testbench with coverage after `check` passes, so a lint or type error fails before the slower run.
`just tox` runs the doctests and the test suite on every supported Python version, plus a `lint` environment with the same checks as `just check`, a `typing-min` environment that checks the library and its consumer-side types on the oldest supported mypy, and a `pyright` environment that checks the same consumer-side types on pyright.

`uv run` resolves the tools from `uv.lock`, while tox installs the newest versions the floors in `pyproject.toml` allow.
`just watch-tools` runs the `lint`, `pyright`, and newest-Python environments that way, as an early warning for a new `ruff`, `mypy`, `ty`, or `pyright`: when it fails and `just check` passes, a tool moved, and the fix is a small change followed by `uv lock --upgrade-package <tool>`.
Run it on a schedule, for example weekly.

`tests/api/test_typing.py` exercises negative typing fixtures under `--strict` on mypy and on pyright, and `tests/contract/test_static_types_agree_with_runtime.py` compares what each checker infers with what the runtime returns.
Ruff is configured with `select = ["ALL"]`; disabled rules in `pyproject.toml` carry inline explanations for why they do not fit the codebase.

## Further reading

The README intentionally gives the usage model before the implementation story.
Deeper design material is kept separately:

- **[Quantity shapes and semantics](docs/concepts/quantity_shapes.md)** - Linear, Affine, Modular, and Logarithmic quantities, including temperature, angle, and decibel semantics.
- **[Dimensional algebra and derived quantities](docs/concepts/dimensional_algebra.md)** - exponent-vector arithmetic, registered results, reciprocal relationships, and the boundary between runtime algebra and static overloads.
- **[Copying, pickling, and persistence](docs/concepts/persistence.md)** - what `copy` and `pickle` guarantee, why pickle is not a storage format, and how to store a value as exact text and a unit symbol.
- **[Unit spellings](docs/concepts/unit_spellings.md)** - what the `*_UNITS` tables accept, how case and plurals are treated, and why no spelling can mean two units.
- **[Exactness, angles, and tolerance](docs/concepts/exactness.md)** - `Fraction` storage, decimal materialization, float input normalization, angles and pi, and comparing with a tolerance.
- **[How to extend kuchka](docs/how-to/README.md)** - adding a unit, a quantity, a dimension, or archaic units, splitting a module, and the tests and documentation each needs, with an imaginary krakenpeople example.
- **[Design choices](docs/design_choices.md)** - constructor functions, unit definitions, canonical types, string-resolution boundaries, and the reasons for a curated vocabulary.
- **[Comparison with existing tools](docs/comparison.md)** - the deliberate trade-offs versus Pint, physipy, impunity, and related libraries.

The original pre-implementation design proposal lives at [`docs/introduction/design_proposal.md`](docs/introduction/design_proposal.md). It is retained as historical design material.
