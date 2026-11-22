# kuchka

![PyPI Version](https://img.shields.io/pypi/v/kuchka)
![PyPI License](https://img.shields.io/pypi/l/kuchka)

---

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

## Contents

<!-- BEGIN TOC -->

- [Installation](#installation)
- [Quick start](#quick-start)
  - [1. Put the physical meaning in the signature](#1-put-the-physical-meaning-in-the-signature)
  - [2. Read measurements from text and config](#2-read-measurements-from-text-and-config)
  - [3. Compose real engineering relationships](#3-compose-real-engineering-relationships)
  - [4. Bring raw sensor data into a control path](#4-bring-raw-sensor-data-into-a-control-path)
- [Take a tour](#take-a-tour)
  - [Linear quantities](#linear-quantities)
  - [Affine quantities](#affine-quantities)
  - [Modular quantities](#modular-quantities)
  - [Logarithmic quantities](#logarithmic-quantities)
- [Why `kuchka`?](#why-kuchka)
- [Where `kuchka` fits](#where-kuchka-fits)
- [What's included in 0.1.x](#whats-included-in-01x)
  - [Core](#core)
  - [Chemistry](#chemistry)
  - [Electromagnetics](#electromagnetics)
  - [Geometry](#geometry)
  - [Information](#information)
  - [Kinematics](#kinematics)
  - [Mechanics](#mechanics)
  - [Photometry](#photometry)
  - [Radiation](#radiation)
  - [Temporal](#temporal)
  - [Thermodynamics](#thermodynamics)
  - [Archaic and historical units](#archaic-and-historical-units)
- [A few important distinctions](#a-few-important-distinctions)
  - [Same dimension does not always mean the same concept](#same-dimension-does-not-always-mean-the-same-concept)
  - [Canonical types and domain-specific types](#canonical-types-and-domain-specific-types)
- [Conversions](#conversions)
- [Exact arithmetic](#exact-arithmetic)
  - [Angles and pi](#angles-and-pi)
  - [Comparing with a tolerance](#comparing-with-a-tolerance)
- [Physical constants](#physical-constants)
- [Errors](#errors)
- [Formatting](#formatting)
  - [Readable units](#readable-units)
- [Examples](#examples)
- [Performance](#performance)
- [What this is not yet](#what-this-is-not-yet)
- [Stability](#stability)
  - [Compatibility](#compatibility)
- [Development](#development)
- [Further reading](#further-reading)

<!-- END TOC -->

## Installation

```bash
uv add kuchka
```

or:

```bash
pip install kuchka
```

`kuchka` is pure Python and imports only the standard library at runtime.
On Python 3.11 it also installs `typing_extensions`, the backport that provides `override`; from Python 3.12 it has no dependencies at all.
The development toolchain described later is separate from the package's runtime dependencies.

Application code should normally import from the top-level `kuchka` package.

## Quick start

The useful part of `kuchka` is not just unit conversion.
Values acquire a physical type, typed quantities can cross application boundaries, and ordinary arithmetic can produce other physical quantities.

### 1. Put the physical meaning in the signature

In 1983 an Air Canada Boeing 767 ran out of fuel in flight and glided down to a disused airfield at Gimli, Manitoba (the "Gimli Glider").
The fuel gauges were out of service, so the ground crew worked the load out by hand: the flight needed 22,300 kg, the dipsticks showed 7,682 L in the tanks, and the fuel table gave a density of 1.77.
That number was pounds per litre.
It was used as kilograms per litre, and the tanks received about a quarter of the fuel they needed.

Written with plain numbers, the calculation looks fine and runs without complaint:

```python
def compute_fuel_to_add(required, in_tanks, density):
    return (required - in_tanks * density) / density


print(f"{compute_fuel_to_add(22_300, 7_682, 1.77):.0f}")
# 4917
```

Nothing in `4917` says litres, and nothing in `1.77` says pounds.
With quantities, the unit travels with the number from the moment it is read, and the checks that matter are written once, in the unit that is convenient:

```python
from kuchka import Density
from kuchka import Kilogram
from kuchka import KilogramPerLitre
from kuchka import Litre
from kuchka import Mass
from kuchka import Volume
from kuchka import parse
from kuchka.units import LITRE

JET_FUEL_MIN = KilogramPerLitre(0.775)
JET_FUEL_MAX = KilogramPerLitre(0.840)


def read_fuel_density(text: str) -> Density:
    density = parse(text, Density)
    if not JET_FUEL_MIN <= density <= JET_FUEL_MAX:
        raise ValueError(f"{density} is not the density of jet fuel")
    return density


def compute_fuel_to_add(required: Mass, in_tanks: Volume, density: Density) -> Volume:
    in_tanks_mass = in_tanks * density
    missing = required - in_tanks_mass
    return missing / density


density = read_fuel_density("1.77 lb/L")  # the fuel table, as it is printed.
fuel = compute_fuel_to_add(
    required=Kilogram(22_300),
    in_tanks=Litre(7_682),
    density=density,
)

print(f"{fuel.to(LITRE):.0f}")
# 20094 L
```

The flight plan is in kilograms, the table in pounds and litres, and the dipstick in litres, and nothing in the calculation converts anything: the quantities carry their units and combine exactly.
Every line has a physical type: `Volume * Density` is a `Mass`, a `Mass` over a `Density` is a `Volume`.

`kuchka` cannot know what the table meant: the unit comes from whoever wrote it, and a card that says `1.77 kg/L` is as readable as one that says `1.77 lb/L`.
What changes is where a mistake can hide:

```python
read_fuel_density("1.77")  # rejected: `ParseError`.
read_fuel_density("1.77 kg")  # rejected: `UnknownUnitError`.
read_fuel_density("1.77 kg/L")  # rejected: `ValueError`.
```

A number without a unit cannot enter the program, and the plausibility check is written once, in kilograms per litre, whichever unit the card uses: `1.77 lb/L` and `0.803 kg/L` pass, and `1.77 kg/L` is stopped on the ground.
With plain numbers the same check needs the pounds-to-kilograms factor, which is the conversion the crew got wrong.

The signature is the contract as well, and a bare number has nowhere to go:

<!-- doc-test: skip static type errors, shown for the checker -->

```python
compute_fuel_to_add(
    Kilogram(22_300), Litre(7_682), 1.77
)  # static type error: a bare number is not a Density.
compute_fuel_to_add(
    Kilogram(22_300), Litre(7_682), Kilogram(1.77)
)  # static type error: a Mass is not a Density.
```

The type annotation gives static tools the contract.
The arithmetic inside the function exercises `kuchka`'s runtime dimensional checks when it is called with an incompatible value.
Python function annotations themselves remain ordinary annotations; `kuchka` does not add a runtime annotation enforcement mechanism.

The point is not to replace every unit library.
The point is to make one particular style of engineering code feel natural: ordinary Python functions taking and returning ordinary Python types that happen to carry physical meaning.

### 2. Read measurements from text and config

Configuration files, CSV logs, command lines, and instrument replies write units as text.
That does not mean the rest of the application has to become stringly typed.
`parse` reads the number and the unit together, through the table of units of the type you name, and returns a typed value:

```python
import tomllib
from dataclasses import dataclass

from kuchka import Voltage
from kuchka import parse


@dataclass(frozen=True)
class DeviceConfig:
    led_critical_voltage: Voltage


raw = tomllib.loads('led_critical_voltage = "2800 mV"')
config = DeviceConfig(led_critical_voltage=parse(raw["led_critical_voltage"], Voltage))
```

The unit is closed to the quantity the field expects, so these are rejected while loading:

```python
parse("150 mA", Voltage)  # rejected: `UnknownUnitError`.
parse("five volts", Voltage)  # rejected: `ParseError`.
parse(2.8, Voltage)  # rejected: `TypeError`.
```

`mA` is no unit of `Voltage`, and the last line is what a bare TOML number would be: a binary float with no unit.
Quote the value and keep the unit in the string, and the digits are read exactly:

```python
from fractions import Fraction

from kuchka import Proportion
from kuchka import Temperature
from kuchka import Volt

parse("0.1 V", Voltage) == Volt(Fraction(1, 10))  # True: the number is read exactly
parse("1/3 V", Voltage) == Volt(1) / 3  # True: a fraction holds what no decimal can
parse("-40 °C", Temperature)  # -40 °C
parse("0.25", Proportion)  # 0.25 1: a proportion is a pure number and needs no unit
```

The tables accept the notations that real files use, so these all read as the same temperature:

```python
for text in (
    "21.5 °C",
    "21.5 degC",
    "21.5 degrees C",
    "21.5 Degrees Celsius",
    "21.5 C",
):
    parse(text, Temperature)  # 21.5 °C
```

Symbols such as `mV` are compared exactly, because `mV` and `MV` are different units, and spoken forms such as `degrees celsius` are compared ignoring case.
A spelling that could mean more than one unit in a table, like `deg` for temperature, is refused rather than guessed.
See [Unit spellings](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/unit_spellings.md).

The caller names the type because the same text can mean different quantities: `"5 s"` is a `Time`, an `Instant`, or a `SamplingPeriod`, so there is no untyped `parse`.

When the unit arrives in a field of its own, such as a CSV column or a `{ value, unit }` pair, the `*_UNITS` table of the type resolves the spelling directly: `VOLTAGE_UNITS["mV"]` is the `Millivolt` constructor.

`kuchka.wire` writes a measurement as text and reads what a boundary delivers, so a value crosses a file, a payload, or a database column and comes back exactly:

```python
from kuchka import wire

wire.dump(Volt(1) / 3)  # '1/3 V'
wire.load("1/3 V", Voltage) == Volt(1) / 3  # True
wire.load({"value": "2800", "unit": "mV"}, Voltage)  # 2800 mV
wire.load(2.8, Voltage)  # rejected: `ParseError`.
```

Every refusal is a `ParseError`, which is a `ValueError`, so a validation framework reports it without a wrapper.
An `attrs` class gets the same reading from `kuchka.attrs.parse_field(Voltage)`, the converter of a field, and a Pydantic v2 model from `Annotated[Voltage, kuchka.pydantic.Quantity]`, which also writes and describes the field in JSON (`pip install kuchka[pydantic]`); see [The wire form](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/wire_form.md).

### 3. Compose real engineering relationships

A calculation is most useful when it crosses physical domains and every step keeps its type.
A winch lifts a 250 kg load by 12 m, and the same lift is followed from the weight on the hook to the heat in the motor winding:

<details>
<summary>Imports</summary>

```python
from kuchka import Ampere
from kuchka import Centimetre
from kuchka import JoulePerKelvin
from kuchka import Kilogram
from kuchka import Metre
from kuchka import MetrePerSecond
from kuchka import MetrePerSecondSquared
from kuchka import RadianPerSecond
from kuchka import Torque
from kuchka import Volt
from kuchka.units import PERCENT
from kuchka.units import WATT_HOUR
```

</details>

```python
load = Kilogram(250)
height = Metre(12)
lift_speed = MetrePerSecond(0.5)
gravity = MetrePerSecondSquared(9.80665)

supply = Volt(400)
current = Ampere(6.5)

drum_radius = Centimetre(20)
drum_speed = RadianPerSecond(2.5)  # 0.5 m/s on a 0.2 m drum.
winding_heat_capacity = JoulePerKelvin(900)

# Mechanics: the weight and the work of lifting it.
weight = load * gravity  # Mass * Acceleration -> Force
work = weight * height  # Force * Length -> Energy
lift_time = height / lift_speed  # Length / Velocity -> Time
useful_power = work / lift_time  # Energy / Time -> Power

# Electrics: what the supply delivers for the same lift.
supply_power = supply * current  # Voltage * Current -> Power
supply_energy = supply_power * lift_time  # Power * Time -> Energy
efficiency = useful_power / supply_power  # Power / Power -> Proportion

# Rotation: the same power measured on the drum shaft.
shaft_torque = Torque.from_force(weight, drum_radius)
shaft_power = shaft_torque * drum_speed  # Torque * AngularVelocity -> Power

# Heat: what the winding has to absorb.
losses = supply_energy - work  # Energy - Energy -> Energy
rise = losses / winding_heat_capacity  # Energy / HeatCapacity -> TemperatureDelta

print(weight, work, lift_time)
# 2451.6625 N 29419.95 J 24 s
print(useful_power, supply_power)
# 1225.83125 W 2600 W
print(f"{efficiency.to(PERCENT):.1f}")
# 47.1 %
print(f"{supply_energy.to(WATT_HOUR):.1f}")
# 17.3 Wh
print(shaft_torque, shaft_power == useful_power)
# 490.3325 N·m True
print(f"{rise:.1f}")
# 36.6 ΔK
```

No unit strings and no conversion factors appear in the calculation, and each quantity is the type its physics says it is.
The shaft power computed from a torque and a rate in radians per second is exactly the power computed from a force and a speed, because `kuchka` holds pi as an exact rational.
Mixing up two of these, say energy with power, is rejected as soon as it runs:

```python
supply_energy + supply_power  # rejected: `IncompatibleDimensionError`.
```

The products and quotients the library knows are declared on the quantity types, so editors and type checkers see them, and [Dimensional algebra](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/dimensional_algebra.md) describes how a result gets its type.

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

Powers work too.
A power is the product written out, so each step lands on a registered type, and the result is the quantity the dimension has:

```python
from kuchka import Metre
from kuchka import MetrePerSecond
from kuchka import Second
from kuchka import SquareMetre
from kuchka import VelocitySquared

Metre(3) ** 2 == SquareMetre(9)
# True

isinstance(MetrePerSecond(3) ** 2, VelocitySquared)
# True

Second(2) ** -1
# 0.5 Hz
```

See [dimensional algebra](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/dimensional_algebra.md) for the products and powers the registry knows.

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
from kuchka import Millisecond
from kuchka import Second

reading = Second(1_700_000_000).to_instant()
reading + Millisecond(500)  # -> Instant, 500 ms later
reading - Second(100).to_instant()  # -> Time(1_699_999_900)
reading + reading  # rejected: `MeasurementError`.
```

`Time.to_instant()` and `Time.to_sampling_period()` work at whatever prefix the `Time` value was already constructed with:

```python
from kuchka import Hour
from kuchka import Minute

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
from kuchka import Decibel
from kuchka import LogarithmicRatio
from kuchka import Ratio

Decibel(30).to_power_ratio() == Ratio(1000)  # whole decades are exact.
Decibel(40).to_field_ratio() == Ratio(100)
LogarithmicRatio.from_power_ratio(Ratio(100)) == Decibel(20)
```

Levels that are not whole decades convert to the precision of the active `decimal` context.

See [Quantity shapes and semantics](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/quantity_shapes.md) for the full semantics.

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
from kuchka import Milliampere
from kuchka import Millivolt

voltage = Millivolt(4200)
current = Milliampere(150)
power = voltage * current

power  # 0.63 W
type(power)  # `<class 'kuchka.quantities.mechanics.power.Power'>`
```

A function can require `Voltage`, a configuration loader can construct a `Voltage`, and an engineering formula can produce a `Power`.
The unit does not have to be carried in a variable name, a comment, or an application-specific string convention.

That is the niche `kuchka` is aiming for: a curated set of engineering quantities that behave as ordinary Python types and are checked by ordinary Python type checkers, with runtime validation still available at untyped boundaries.

This is deliberately narrower than a general-purpose unit language.
`kuchka` does not try to accept arbitrary unit expressions, provide a mutable application-wide unit registry, or make every physical quantity array-native.
Those are useful capabilities, but they optimize for a different problem.
See [Comparison with existing tools](https://github.com/Dimonade/kuchka/blob/HEAD/docs/comparison.md) for the trade-offs.

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

The tables below show a number of representative units per package of `kuchka.units`, with `Core` holding its top-level modules.
The complete unit vocabulary is available in the API reference.

### Core

The units of the top-level modules of `kuchka.units`.

| Quantity             | Representative units                                                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Length               | `Picometre` through `Kilometre`, `Inch` and other exact imperial units, `AstronomicalUnit`, `LightYear`, and `Parsec` through `Gigaparsec` |
| Mass                 | `Nanogram` through `Megagram`, `Tonne`, along with `SolarMass` and `EarthMass`                                                             |
| Current              | `Picoampere`, through `Megaampere`                                                                                                         |
| Amount of Substance  | `Femtoomole` through `Kilomole`                                                                                                            |
| Luminous Intensity   | `Candela`                                                                                                                                  |
| Temperature          | `Microkelvin` through `Kelvin`, `Microcelsius` through `Celsius`, `Fahrenheit`, `Rankine`                                                  |
| Temperature Delta    | `DeltaMicrokelvin` through `DeltaKelvin`, `DeltaMicrocelsius` through `DeltaCelsius`, `DeltaFahrenheit`, `DeltaRankine`                    |
| Angle                | `Radian`, `Degree`, `Turn`, `Gradian`, `ArcMinute`, `ArcSecond`                                                                            |
| Angular displacement | `RadianDisplacement`, `DegreeDisplacement`, `TurnDisplacement`, `GradianDisplacement`, `ArcMinuteDisplacement`, `ArcSecondDisplacement`    |
| Solid angle          | `Steradian`, `Millisteradian`, `Microsteradian`, `SquareDegree`, `SquareArcMinute`, `SquareArcSecond`                                      |
| Proportion           | `Ratio`, `Percent`                                                                                                                         |
| LogarithmicRatio     | `Decibel`, `Bel`                                                                                                                           |

### Chemistry

The units of `kuchka.units.chemistry`.

| Quantity            | Representative units                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------- |
| Molar mass          | `KilogramPerMole`, `GramPerMole`, `KilogramPerKilomole`                                                       |
| Molar concentration | `MolePerCubicMetre`, `MolePerLitre`, `MillimolePerLitre`, `MicromolePerLitre`, `NanomolePerLitre`             |
| Molar energy        | `JoulePerMole`, `KilojoulePerMole`, `KilocaloriePerMole`                                                      |
| Entities per amount | `PerMole`                                                                                                     |
| Molality            | `MolePerKilogram`, `MillimolePerKilogram`, `MicromolePerKilogram`                                             |
| Molar volume        | `CubicMetrePerMole`, `LitrePerMole`, `CubicCentimetrePerMole`                                                 |
| Molar flow rate     | `MolePerSecond`, `KilomolePerSecond`, `MillimolePerMinute`, `MolePerMinute`, `MolePerHour`, `KilomolePerHour` |
| Catalytic activity  | `Nanokatal`, `Microkatal`, `Millikatal`, `Katal`, `EnzymeUnit`                                                |
| Molar charge        | `CoulombPerMole`, `KilocoulombPerMole`                                                                        |
| Molar heat cap.     | `JoulePerMoleKelvin`, `KilojoulePerMoleKelvin`, `ThermochemicalCaloriePerMoleKelvin`                          |
| Molar entropy       | `MolarHeatCapacity.to_molar_entropy()`, and `MOLAR_ENTROPY_UNITS`                                             |

### Electromagnetics

The units of `kuchka.units.electromagnetics`.

| Quantity                | Representative units                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------ |
| Voltage                 | `Nanovolt` through `Petavolt`                                                                    |
| Apparent Power          | `MillivoltAmpere` through `GigavoltAmpere`                                                       |
| Reactive Power          | `Millivar` through `Gigavar`                                                                     |
| Resistance              | `Microohm`, through `Gigaohm`                                                                    |
| Conductance             | `Nanosiemens` through `Kilosiemens`                                                              |
| Charge                  | `Picocoulomb` through `Coulomb`, `MilliampereSecond`, `MilliampereHour`, `AmpereHour`            |
| Specific charge         | `CoulombPerKilogram`, `AmpereHourPerKilogram`, `MilliampereHourPerGram`                          |
| Electric field strength | `MicrovoltPerMetre` through `MegavoltPerMetre`, `VoltPerCentimetre`, `KilovoltPerMillimetre`     |
| Current density         | `AmperePerSquareMetre`, `AmperePerSquareMillimetre`, `MilliamperePerSquareCentimetre`            |
| Linear charge density   | `CoulombPerMetre`, `NanocoulombPerMetre`, `PicocoulombPerMetre`                                  |
| Surface charge density  | `CoulombPerSquareMetre`, `MicrocoulombPerSquareCentimetre`, `MilliampereHourPerSquareCentimetre` |
| Volume charge density   | `CoulombPerCubicMetre`, `CoulombPerCubicCentimetre`, `AmpereHourPerLitre`                        |
| Specific current        | `AmperePerKilogram`, `MilliamperePerKilogram`, `MicroamperePerKilogram`                          |
| Magnetic Flux           | `Nanoweber` through `Kiloweber`                                                                  |
| Flux Density            | `Femtotesla` through `Kilotesla`, `Femtogauss` through `Kilogauss`                               |
| Capacitance             | `Femtofarad` through `Kilofarad`                                                                 |
| Inductance              | `Picohenry` through `Kilohenry`                                                                  |
| Reactance               | reached via `Resistance.to_reactance()`                                                          |
| Impedance               | reached via `Resistance.to_impedance()`                                                          |
| Permittivity            | `PicofaradPerMetre` through `FaradPerMetre`                                                      |
| Permeability            | `NanohenryPerMetre` through `HenryPerMetre`                                                      |
| Field Strength          | `MicroamperePerMetre` through `MegaamperePerMetre`                                               |
| Magnetization           | reached via `MagneticFieldStrength.to_magnetization()`                                           |

### Geometry

The units of `kuchka.units.geometry`.

| Quantity | Representative units                                                                                              |
| -------- | ----------------------------------------------------------------------------------------------------------------- |
| Area     | `SquareMillimetre` through `SquareKilometre`, `Hectare`, `Acre`                                                   |
| Volume   | `CubicMillimetre` through `CubicMetre`, `Microlitre`, `Millilitre`, `Litre`, `Kilolitre`, `CubicFoot`, `UsGallon` |

### Information

The units of `kuchka.units.information`.

| Quantity  | Representative units                                                                                  |
| --------- | ----------------------------------------------------------------------------------------------------- |
| Data      | `Bit` and `Byte`, `Kilobyte` through `Petabyte`, `Kibibyte` through `Pebibyte`, and the same for bits |
| Data Rate | `BitPerSecond` and `BytePerSecond`, with the same SI and IEC multiples                                |

### Kinematics

The units of `kuchka.units.kinematics`.

| Quantity                 | Representative units                                                                                       |
| ------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Velocity                 | `MetrePerSecond`, `KilometrePerHour`, `MilePerHour`, `Knot`                                                |
| Acceleration             | `MetrePerSecondSquared`, `Microgal` through `Gal`                                                          |
| Jerk                     | `MetrePerSecondCubed`, `MillimetrePerSecondCubed`                                                          |
| Snap                     | `MetrePerSecondFourthPower`, `MillimetrePerSecondFourthPower`                                              |
| Angular velocity         | `RadianPerSecond`, `DegreePerSecond`, `TurnPerSecond`, `RevolutionPerMinute`                               |
| Angular acceleration     | `RadianPerSecondSquared`, `DegreePerSecondSquared`, `TurnPerSecondSquared`, `RevolutionPerMinutePerSecond` |
| Angular jerk             | `RadianPerSecondCubed`, `DegreePerSecondCubed`, `TurnPerSecondCubed`                                       |
| Angular velocity squared | `RadianSquaredPerSecondSquared`, `TurnSquaredPerSecondSquared`, `DegreeSquaredPerSecondSquared`            |
| Time squared             | `NanosecondSquared` through `SecondSquared`, `MinuteSquared`, `HourSquared`                                |
| Time cubed               | `NanosecondCubed` through `SecondCubed`, `MinuteCubed`, `HourCubed`                                        |
| Time to the fourth power | `NanosecondFourthPower` through `SecondFourthPower`, `MinuteFourthPower`, `HourFourthPower`                |

### Mechanics

The units of `kuchka.units.mechanics`.

| Quantity             | Representative units                                                                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Force                | `Micronewton` through `MegaNewton`, `Dyne`, `PoundForce`, and `KilogramForce`                                                                                 |
| Pressure             | `Pascal`, `Hectopascal`, `Kilopascal`, `Megapascal`, `Gigapascal`, `Bar`, `Millibar`, `Atmosphere`, `PoundPerSquareInch`, `KilopoundPerSquareInch`            |
| Stress               | the units of Pressure, reached with `Pressure.to_stress()`                                                                                                    |
| Energy               | `Picojoule` through `Petajoule`, `Electronvolt` through `Teraelectronvolt`, `MilliwattHour` through `KilowattHour`                                            |
| _energy, continued_  | `Erg`, `Calorie`, `Kilocalorie`, `TonneOfTNT` through `MegatonneOfTNT`                                                                                        |
| Power                | `Picowatt` through `Petawatt`, `Horsepower`, `MetricHorsepower`, `JoulePerMinute`, `JoulePerHour`, `KilojoulePerHour`, `MegajoulePerHour`, `GigajoulePerHour` |
| Torque               | `NewtonMetre`, `MillinewtonMetre`, `KilonewtonMetre`, `PoundForceFoot`, `PoundForceInch`, `JoulePerTurn`                                                      |
| Density              | `KilogramPerCubicMetre`, `GramPerCubicCentimetre`, `KilogramPerLitre`, `GramPerLitre`, `MilligramPerLitre`, `MicrogramPerLitre`                               |
| Energy density       | `JoulePerCubicMetre`, `KilojoulePerCubicMetre`, `MegajoulePerCubicMetre`, `WattHourPerLitre`                                                                  |
| Momentum             | `KilogramMetrePerSecond`, `GramCentimetrePerSecond`, `PoundFootPerSecond`                                                                                     |
| Impulse              | `NewtonSecond`, `MillinewtonSecond`, `KilonewtonSecond`, `DyneSecond`, `PoundForceSecond`                                                                     |
| Angular momentum     | `KilogramSquareMetrePerSecond`, `NewtonMetreSecond`, `JouleSecondPerTurn`                                                                                     |
| Moment of inertia    | `KilogramSquareMetre`, `KilogramSquareCentimetre`, `GramSquareCentimetre`, `PoundSquareFoot`, `PoundSquareInch`                                               |
| First moment of mass | `KilogramMetre`, `GramCentimetre`, `GramMillimetre`, `OunceInch`                                                                                              |
| Velocity squared     | `SquareMetrePerSecondSquared`, `SquareKilometrePerSecondSquared`                                                                                              |
| Specific energy      | `JoulePerKilogram`, `MegajoulePerKilogram`, `WattHourPerKilogram`, `KilowattHourPerKilogram`, `KilocaloriePerKilogram`                                        |
| Specific power       | `WattPerKilogram`, `MilliwattPerKilogram`, `KilowattPerKilogram`, `WattPerGram`, `MilliwattPerGram`                                                           |
| Volumetric flow      | `CubicMetrePerSecond`, `LitrePerSecond`, `LitrePerMinute`, `CubicMetrePerHour`, `MillilitrePerMinute`, `UsGallonPerMinute`, `CubicFootPerMinute`              |
| Mass flow            | `KilogramPerSecond`, `GramPerSecond`, `KilogramPerHour`, `TonnePerHour`, `PoundPerHour`                                                                       |
| Dynamic viscosity    | `PascalSecond`, `MillipascalSecond`, `Poise`, `Centipoise`                                                                                                    |
| Kinematic viscosity  | `SquareMetrePerSecond`, `SquareMillimetrePerSecond`, `Stokes`, `Centistokes`                                                                                  |

### Photometry

The units of `kuchka.units.photometry`.

| Quantity          | Representative units                                                                                       |
| ----------------- | ---------------------------------------------------------------------------------------------------------- |
| Luminous flux     | `Millilumen`, `Lumen`, `Kilolumen`                                                                         |
| Luminous energy   | `LumenSecond`, `LumenHour`                                                                                 |
| Illuminance       | `Millilux`, `Lux`, `Kilolux`, `Phot`, `FootCandle`                                                         |
| Luminous exposure | `LuxSecond`, `LuxHour`, `KiloluxHour`                                                                      |
| Luminance         | `CandelaPerSquareMetre`, `MillicandelaPerSquareMetre`, `KilocandelaPerSquareMetre`, `Stilb`, `FootLambert` |
| Luminous efficacy | `LumenPerWatt`                                                                                             |

### Radiation

The units of `kuchka.units.radiation`.

| Quantity          | Representative units                                                                                        |
| ----------------- | ----------------------------------------------------------------------------------------------------------- |
| Activity          | `Millibecquerel` through `Terabecquerel`, `Curie`, `Millicurie`, `Microcurie`, `Nanocurie`, and `Picocurie` |
| Absorbed dose     | `Nanogray` through `Megagray`, `Rad`, and `Millirad`                                                        |
| Equivalent dose   | `Nanosievert` through `Kilosievert`, `Rem`, and `Millirem`                                                  |
| Exposure          | `Roentgen`, `Milliroentgen`, `Microroentgen`, and `C/kg` through `EXPOSURE_UNITS`                           |
| Abs. dose rate    | `GrayPerSecond`, `GrayPerMinute`, `GrayPerHour` through `NanograyPerHour`, and `RadPerHour`                 |
| Equiv. dose rate  | `SievertPerSecond`, `SievertPerHour` through `NanosievertPerHour`, and `RemPerHour`                         |
| Exposure rate     | `RoentgenPerSecond` through `RoentgenPerHour`, `MilliroentgenPerHour`, `MicroroentgenPerHour`               |
| Activity conc.    | `BecquerelPerCubicMetre`, `BecquerelPerLitre`, `PicocuriePerLitre`, and the kilo- and milli- multiples      |
| Specific activity | `BecquerelPerKilogram`, `BecquerelPerGram`, `PicocuriePerGram` through `CuriePerGram`                       |
| Surface activity  | `BecquerelPerSquareCentimetre`, `DpmPer100SquareCentimetre`, `CuriePerSquareKilometre`                      |

### Temporal

The units of `kuchka.units.temporal`.

| Quantity        | Representative units                                                       |
| --------------- | -------------------------------------------------------------------------- |
| Time            | `Femtosecond` through `Second`, `Minute` through `JulianYear`, and `Jiffy` |
| Instant         | reached via `Time.to_instant()`                                            |
| Frequency       | `Nanohertz` through `Petahertz`                                            |
| Sampling Period | reached via `Time.to_sampling_period()`                                    |
| Sample Rate     | `SamplesPerSecond`, `KilosamplesPerSecond`, `MegasamplesPerSecond`         |
| Baud Rate       | `Baud` through `Gigabaud`                                                  |

### Thermodynamics

The units of `kuchka.units.thermodynamics`.

| Quantity             | Representative units                                                                                             |
| -------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Heating Rate         | `KelvinPerSecond`, `CelsiusPerMinute`, `FahrenheitPerMinute`, and the per-second, per-minute, and per-hour units |
| Heat capacity        | `JoulePerKelvin`, `KilojoulePerKelvin`, `ThermochemicalCaloriePerKelvin`, `KilocaloriePerKelvin`                 |
| Specific heat        | `JoulePerKilogramKelvin`, `KilojoulePerKilogramKelvin`, `ThermochemicalCaloriePerGramKelvin`                     |
| Heat flux            | `WattPerSquareMetre`, `KilowattPerSquareMetre`, `MilliwattPerSquareCentimetre`                                   |
| Thermal conductivity | `WattPerMetreKelvin`, `MilliwattPerMetreKelvin`, `WattPerCentimetreKelvin`                                       |
| Entropy              | `HeatCapacity.to_entropy()`, and `ENTROPY_UNITS` for the same units as text                                      |
| Specific entropy     | `SpecificHeatCapacity.to_specific_entropy()`, and `SPECIFIC_ENTROPY_UNITS`                                       |

Most SI-derived families expose a selected set of SI prefixes appropriate to their engineering use.
The README does not list every prefix individually; the API reference contains the complete constructor and unit vocabulary.

The canonical spelling of SI `metre` is used throughout `kuchka`.
American-English `*meter` names are aliases of the corresponding `*metre`
constructors, not separate unit implementations. The same principle applies
to `Litre`/`Liter` and other spelling aliases.

### Archaic and historical units

Historical, regional, and culturally specific units live apart from the main vocabulary, in `kuchka.units.archaic`.
They are imported explicitly from the module of their tradition and add nothing to the top-level namespace:

```python
from kuchka.units.archaic.russian.length import Arshin
from kuchka.units import CENTIMETRE

print(Arshin(3).to(CENTIMETRE))
# 213.36 cm
```

`parse` reads an archaic unit only when asked, and only from the modules that have been imported:

```python
from kuchka import Length
from kuchka import parse

parse("3 arshin", Length, allow_archaic=True)  # 3 arshin
```

`allow_archaic` takes an `ArchaicPolicy`, `Deny` by default or `Allow`, and `False` and `True` stand for them.
The error for a refused archaic unit says how to read it.

The traditions today are German (the Meilen), Hebrew, Japanese, and Russian.
See the [archaic units README](https://github.com/Dimonade/kuchka/blob/HEAD/src/kuchka/units/archaic/README.md) for what each provides, and [How to extend kuchka](https://github.com/Dimonade/kuchka/blob/HEAD/docs/how-to/README.md) for adding more.

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

An impulse and a momentum are both newton seconds, and still different concepts: a force over a time delivers one, a mass moving at a velocity has the other.
Each product returns its own type, and converting is explicit:

```python
from kuchka import Kilogram
from kuchka import MetrePerSecond
from kuchka import Newton
from kuchka import Second

push = Newton(20) * Second(3)  # an Impulse
cart = Kilogram(12) * MetrePerSecond(5)  # a Momentum

push + cart  # rejected: `IncompatibleDimensionError`.
push.to_momentum() == cart  # True: the push brings the cart from rest to 5 m/s.
```

Likewise a velocity squared and a specific energy share m²/s², and `VelocitySquared.to_specific_energy()` is its half, the kinetic energy per mass.

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
String resolution belongs at boundaries such as configuration and import code, where `parse` and the maintained `*_UNITS` mappings provide the bridge.

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
See [Exactness, angles, and tolerance](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/exactness.md) for why equality stays exact and how each shape measures distance.

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
A test ties every constant, and the `Dalton`, `EarthMass`, and `SolarMass` units, to the NIST listing shipped with the package, so a new adjustment fails a test until the values are updated on purpose.

`kuchka.constants.icrp_103` holds the radiation weighting factors of ICRP Publication 103 as plain proportions, for `EquivalentDose.from_absorbed_dose`.
They are the Commission's recommendations and not measurements, and the Commission has revised them before.

```python
from kuchka import EquivalentDose
from kuchka import Milligray
from kuchka.constants import icrp_103

EquivalentDose.from_absorbed_dose(Milligray(3), icrp_103.ALPHA_PARTICLES)
# EquivalentDose: 60 mSv
```

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

### Readable units

A measurement displays in the unit it was given, and two methods choose one that reads well when you ask for it.
`auto_scale()` returns the same exact value in the prefixed unit that suits its size, and `Time.clock_parts()` splits a duration into days, hours, minutes, and seconds.

```python
from kuchka import Ampere
from kuchka import Millisecond

str(Ampere(0.000045).auto_scale()) == "45 µA"  # True
parts = Millisecond(5_025_500).clock_parts()
" ".join(map(str, parts)) == "1 h 23 min 45 s 500 ms"  # True
```

A quantity without prefixed units, a temperature in degrees Celsius, and an angle keep their unit.
See [Readable units](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/auto_scaling.md) for the ladders, the rule that picks a unit, and the quantities that have none.

## Examples

The repository contains longer, task-oriented examples:

- **[A heated beaker on a stepper-driven lever](https://github.com/Dimonade/kuchka/blob/HEAD/docs/examples/heated_beaker/README.md)** - reads a TOML spec and a CSV run log whose cells mix `V`, `mV`, `°C`, and `°F`, then measures the run with angles that wrap, temperature differences, tolerances, and power into energy.
- **[Migrating a config from unit-suffixed keys to `kuchka`](https://github.com/Dimonade/kuchka/blob/HEAD/docs/examples/config_migration/README.md)** - moves units from names such as `accepted_voltage_min_mv` into TOML strings such as `"-1.000 mV"` and reads them with `parse` into typed dataclasses at the boundary.
- **[Working around an unrepresentable intermediate dimension](https://github.com/Dimonade/kuchka/blob/HEAD/docs/examples/unrepresentable_dimensions/README.md)** - shows how to handle formulas such as `P = V²/R` and parallel resistor networks when an intermediate dimension has no registered type.
- **[Hiroshimas per datacenter](https://github.com/Dimonade/kuchka/blob/HEAD/docs/examples/hiroshimas_per_datacenter/README.md)** - counts the heat of a planned off-grid data center in Hiroshimas, with an efficiency as a `Proportion`, TNT equivalents, terajoules, a fluence over acres, and the Reddit unit of Hiroshimas per Walmart Supercenter built as a reference quantity.

These examples show `kuchka` in application code, with arithmetic serving the larger engineering task.

## Performance

`kuchka` uses exact rational arithmetic (`Fraction`) for correctness.
The intended use is at configuration, application, control, and reporting boundaries, not inside a per-sample hot loop processing live streams at very high rates.

See [`benchmarks`](https://github.com/Dimonade/kuchka/blob/HEAD/benchmarks/README.md) for current measurements.

## What this is not yet

The vocabulary is intentionally curated and will remain finite. Current gaps include:

- There is no NumPy/Pandas integration.
- There is no msgspec integration yet; `kuchka.pydantic` and `kuchka.attrs` serve Pydantic v2 models and `attrs` classes, and `kuchka.wire` is the text form they read and write.

## Stability

`kuchka` follows [semantic versioning](https://semver.org/).
Before `1.0.0`, a breaking change comes with a minor version bump and is listed under `Changed` or `Removed` in the changelog.
A patch release keeps existing code working.

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

`just test` runs the doctests and the test suite, `just check` runs the generated-file checks (the API, the overloads, and the contents above), `ruff`, `mypy --strict`, and `ty`, and `just ct` (or `just covtest`) runs the full testbench with coverage after `check` passes, so a lint or type error fails before the slower run.
`just tox` runs the doctests and the test suite on every supported Python version, plus a `lint` environment with the same checks as `just check`, a `typing-min` environment that checks the library and its consumer-side types on the oldest supported mypy, and a `pyright` environment that checks the same consumer-side types on pyright.

`uv run` resolves the tools from `uv.lock`, while tox installs the newest versions the floors in `pyproject.toml` allow.
`just watch-tools` runs the `lint`, `pyright`, and newest-Python environments that way, as an early warning for a new `ruff`, `mypy`, `ty`, or `pyright`: when it fails and `just check` passes, a tool moved, and the fix is a small change followed by `uv lock --upgrade-package <tool>`.
Run it on a schedule, for example weekly.

`tests/api/test_typing.py` exercises negative typing fixtures under `--strict` on mypy and on pyright, and `tests/contract/test_static_types_agree_with_runtime.py` compares what each checker infers with what the runtime returns.
Ruff is configured with `select = ["ALL"]`; disabled rules in `pyproject.toml` carry inline explanations for why they do not fit the codebase.

## Further reading

The README intentionally gives the usage model before the implementation story.
Deeper design material is kept separately:

- **[Quantity shapes and semantics](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/quantity_shapes.md)** - Linear, Affine, Modular, and Logarithmic quantities, including temperature, angle, and decibel semantics.
- **[Dimensional algebra and derived quantities](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/dimensional_algebra.md)** - exponent-vector arithmetic, registered results, reciprocal relationships, and the boundary between runtime algebra and static overloads.
- **[Where the radian meets a length](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/angle_bridges.md)** - how rotational quantities meet lengths: bridges, the moment of inertia, and the relations that stay named constructors.
- **[Copying, pickling, and persistence](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/persistence.md)** - what `copy` and `pickle` guarantee, why pickle is not a storage format, and how to store a value as exact text and a unit symbol.
- **[The wire form](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/wire_form.md)** - `wire.dump` and `wire.load`: a measurement as one exact string, what a boundary may deliver for a field, and why a bare number is refused.
- **[Unit spellings](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/unit_spellings.md)** - what the `*_UNITS` tables accept, how case and plurals are treated, and why no spelling can mean two units.
- **[Readable units](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/auto_scaling.md)** - `auto_scale()` and its ladders of prefixed units, the rule that picks a unit, the quantities without a ladder, and `Time.clock_parts()`.
- **[Exactness, angles, and tolerance](https://github.com/Dimonade/kuchka/blob/HEAD/docs/concepts/exactness.md)** - `Fraction` storage, decimal materialization, float input normalization, angles and pi, and comparing with a tolerance.
- **[How to extend kuchka](https://github.com/Dimonade/kuchka/blob/HEAD/docs/how-to/README.md)** - adding a unit, a quantity, a dimension, or archaic units, splitting a module, and the tests and documentation each needs, with an imaginary krakenpeople example.
- **[Design proposal](https://github.com/Dimonade/kuchka/blob/HEAD/docs/introduction/design_proposal.md)** - the original pre-implementation design: constructor functions, unit definitions, canonical types, string-resolution boundaries, and the reasons for a curated vocabulary.
- **[Comparison with existing tools](https://github.com/Dimonade/kuchka/blob/HEAD/docs/comparison.md)** - the deliberate trade-offs versus Pint, physipy, impunity, and related libraries.
