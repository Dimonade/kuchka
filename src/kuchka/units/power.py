"""Power quantities and constructors across engineering and scientific scales.

`Power` represents the rate at which energy is transferred:

`P = dE / dt`.

Its SI unit is the watt, defined as one joule per second.

The constructors in this module span power scales from picowatts, encountered in
sensitive measurement and optical systems, through ordinary electronic and mechanical
equipment to petawatts used for ultrashort, high-intensity laser pulses.

Power also provides a common language between different physical domains.
Electrical power follows

`P = V I`,

mechanical power follows

`P = F v`,

and rotational mechanical power follows

`P = tau omega`.

The leaf constructors in this module provide the units.
The package-level documentation for the relevant physical domain demonstrates those
relationships.

`Horsepower` and `MetricHorsepower` are explicitly distinguished because "horsepower"
has several historical definitions.
`Horsepower` in this module means the mechanical horsepower of exactly
550 foot-pound-force per second.
`MetricHorsepower` means the continental horsepower of exactly
75 kilogram-force metres per second.

Examples
--------
Power becomes intuitive when it is attached to something actually doing work.

A picowatt is an extremely small amount of power, useful when discussing sensitive
optical and electronic measurements:

>>> detector_signal = Picowatt(10)
>>> detector_signal
10 pW

Nanowatt-scale signals remain small enough that losses and leakage can become
important:

>>> leakage_power = Nanowatt(250)
>>> leakage_power
250 nW

Low-power embedded and sensing electronics commonly live in the microwatt range:

>>> sleep_power = Microwatt(40)
>>> sleep_power
40 µW

At the milliwatt scale, electronic and optical components become easy to describe
directly:

>>> optical_output = Milliwatt(5)
>>> optical_output
5 mW

Ordinary electrical equipment moves naturally into watts and kilowatts.
A 100 W load is consuming energy at a rate of 100 joules every second:

>>> load = Watt(100)
>>> load
100 W

A 2 kW heater transfers energy twenty times faster:

>>> heater = Kilowatt(2)
>>> heater
2 kW

The unit remains the same physical quantity across these scales:

>>> Kilowatt(2) == Watt(2000)
True

Electrical power follows the familiar relationship

`P = V I`.

A 12 V circuit carrying 2 A therefore transfers power at exactly 24 W:

>>> supply_voltage = Volt(12)
>>> supply_current = Ampere(2)
>>> supply_voltage * supply_current
24 W

The same principle works at much larger scales.
A 400 V industrial circuit carrying 250 A carries exactly 100 kW:

>>> Volt(400) * Ampere(250)
100 kW

Mechanical systems commonly reach the kilowatt and megawatt ranges.
A 5 MW machine has the same physical dimension as a 5 W sensor.
Only the scale changes:

>>> industrial_machine = Megawatt(5)
>>> industrial_machine
5 MW

Grid-scale electrical systems are naturally described in gigawatts:

>>> generating_station = Gigawatt(1)
>>> generating_station
1 GW

Terawatt power is already a scale for very large aggregate systems:

>>> large_scale_power = Terawatt(1)
>>> large_scale_power
1 TW

At the extreme scientific end, petawatt lasers produce enormous peak power during
extremely short pulses:

>>> laser_peak_power = Petawatt(5)
>>> laser_peak_power
5 PW

That value does not imply a five-petawatt continuous power source.
Peak power and average power describe different properties of a pulsed system.

Horsepower is a useful historical engineering unit, especially for engines and motors.
One mechanical horsepower is exactly 745.69987158227022 W:

>>> engine_power = Horsepower(1)
>>> engine_power
1 hp

Its value in watts is exact under the definitions used to construct the unit:

>>> engine_power == Watt(745.69987158227022)
True

A 100 hp engine therefore corresponds to exactly 74,569.987158227022 W:

>>> Horsepower(100) == Watt(74569.987158227022)
True

Continental metric horsepower is a different unit:

>>> MetricHorsepower(1)
1 PS

It is exactly 735.49875 W:

>>> MetricHorsepower(1) == Watt(735.49875)
True

The distinction matters when historical or automotive specifications are being
imported.
The two horsepower definitions differ by about 1.4 percent:

>>> Horsepower(1) != MetricHorsepower(1)
True

Power can also be understood through time.
If an ideal 100 W load runs for ten seconds, it transfers exactly 1000 J of energy:

>>> energy = Watt(100) * Second(10)
>>> energy
1000 J

That relationship is the definition of power in another form:

`P = E / t`.

Notes
-----
The watt is the SI coherent unit of power:

`1 W = 1 J / s`.

A watt is therefore a rate, not an amount of energy.
Running a 1 kW load for one hour transfers 1 kWh of energy.
The `Power` quantity itself remains 1 kW throughout the interval.

The same `Power` quantity can arise from different physical relationships.
Electrical power is `V I`; translational mechanical power is `F v`; and rotational
mechanical power is `tau omega`.
The dimensional result is the same even though the contributing quantities belong to
different physical domains.

SI prefixes represent exact powers of ten.
Consequently, conversions such as

>>> Picowatt(1000) == Nanowatt(1)
True

>>> Nanowatt(1000) == Microwatt(1)
True

>>> Microwatt(1000) == Milliwatt(1)
True

>>> Milliwatt(1000) == Watt(1)
True

>>> Watt(1000) == Kilowatt(1)
True

>>> Kilowatt(1000) == Megawatt(1)
True

>>> Megawatt(1000) == Gigawatt(1)
True

>>> Gigawatt(1000) == Terawatt(1)
True

>>> Terawatt(1000) == Petawatt(1)
True

`Horsepower` is the mechanical horsepower defined as 550 foot-pound-force per second.
With the exact international foot and pound definitions and standard gravity, this is
exactly 745.69987158227022 W.

`MetricHorsepower` is exactly 75 kilogram-force metres per second, or 735.49875 W.

Neither horsepower unit is an SI unit.
They are included because they remain common in engineering specifications, especially
for engines and motors.

`POWER_UNITS` maps symbols such as ``"pW"``, ``"nW"``, ``"µW"``, ``"mW"``, ``"W"``,
``"kW"``, ``"MW"``, ``"GW"``, ``"TW"``, ``"PW"``, ``"hp"``, and ``"PS"`` to their
constructors.
This is intended for boundary code that receives units as external data.

See Also
--------
~kuchka.quantities.Energy
    Energy transferred over a time interval.
~kuchka.quantities.Voltage
    Electric potential difference.
~kuchka.quantities.Current
    Electric current.
~kuchka.quantities.Force
    Force producing mechanical power.
~kuchka.quantities.Velocity
    Translational velocity associated with mechanical power.
~kuchka.quantities.Torque
    Rotational moment associated with rotational power.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import POWER
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Power

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

WATT_NAME = "watt"
WATT_SYMBOL = "W"

MICROWATT = prefixed_unit(prefixes.MICRO, WATT_NAME, WATT_SYMBOL, POWER)
MILLIWATT = prefixed_unit(prefixes.MILLI, WATT_NAME, WATT_SYMBOL, POWER)
WATT = prefixed_unit(prefixes.UNIT, WATT_NAME, WATT_SYMBOL, POWER)
KILOWATT = prefixed_unit(prefixes.KILO, WATT_NAME, WATT_SYMBOL, POWER)


Power._canonical_unit = WATT  # noqa: SLF001 -- this module owns Power's canonical unit


def Microwatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in microwatts."""
    return Power(to_exact(value) * MICROWATT.scale, MICROWATT)


def Milliwatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in milliwatts."""
    return Power(to_exact(value) * MILLIWATT.scale, MILLIWATT)


def Watt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in watts."""
    return Power(to_exact(value) * WATT.scale, WATT)


def Kilowatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in kilowatts."""
    return Power(to_exact(value) * KILOWATT.scale, KILOWATT)


POWER_UNITS: Mapping[str, Callable[[Numeric], Power]] = MappingProxyType(
    {
        MICROWATT.symbol: Microwatt,
        MILLIWATT.symbol: Milliwatt,
        WATT.symbol: Watt,
        KILOWATT.symbol: Kilowatt,
    }
)

__all__ = [
    "KILOWATT",
    "MICROWATT",
    "MILLIWATT",
    "POWER_UNITS",
    "WATT",
    "Kilowatt",
    "Microwatt",
    "Milliwatt",
    "Watt",
]
