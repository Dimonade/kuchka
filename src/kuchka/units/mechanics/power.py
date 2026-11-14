"""Power constructors: the watt, from picowatts to petawatts, and horsepower.

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

The energy-per-time units `J/min`, `J/h`, `kJ/min`, `kJ/h`, `MJ/h`, and `GJ/h` write a
power as the energy spent over a minute or an hour.
They serve the fields that measure energy in joules and state a consumption or a
rating per hour, such as sensor logging, exercise physiology, heating, and gas
appliances.

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

>>> from kuchka.units import Volt
>>> from kuchka.units import Ampere
>>> supply_voltage = Volt(12)
>>> supply_current = Ampere(2)
>>> supply_voltage * supply_current
24 W

The same principle works at much larger scales.
A 400 V industrial circuit carrying 250 A carries exactly 100 kW:

>>> Volt(400) * Ampere(250)
100000 W

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

>>> engine_power.to(WATT) == Watt(Decimal("745.69987158227022"))
True

A 100 hp engine therefore corresponds to exactly 74,569.987158227022 W:

>>> Horsepower(100).to(WATT) == Watt(Decimal("74569.987158227022"))
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

A log that records an energy and the time it took gives the consumption in joules per
hour directly.
A device that spent 5400 J in 90 minutes consumed 3600 J/h, which is one watt:

>>> from kuchka import Joule
>>> from kuchka import Minute
>>> consumption = (Joule(5400) / Minute(90)).to(JOULE_PER_HOUR)
>>> consumption
3600 J/h
>>> consumption == Watt(1)
True

Power can also be understood through time.
If an ideal 100 W load runs for ten seconds, it transfers exactly 1000 J of energy:

>>> from kuchka import Second
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

The energy-per-time units are the watt written as an energy over a time, so their
scales are exact:

`1 J/min = 1/60 W`,

`1 J/h = 1/3600 W`,

and `1 kJ/h = 5/18 W`.

>>> JoulePerHour(3600) == Watt(1)
True

>>> MegajoulePerHour(3.6) == Kilowatt(1)
True

Neither horsepower unit is an SI unit.
They are included because they remain common in engineering specifications, especially
for engines and motors.

`POWER_UNITS` maps symbols such as ``"pW"``, ``"nW"``, ``"µW"``, ``"mW"``, ``"W"``,
``"kW"``, ``"MW"``, ``"GW"``, ``"TW"``, ``"PW"``, ``"hp"``, ``"PS"``, ``"J/min"``,
``"J/h"``, ``"kJ/min"``, ``"kJ/h"``, ``"MJ/h"``, and ``"GJ/h"`` to their constructors.
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

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import POWER
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Power
from kuchka.quantities import UnitDef
from kuchka.units.mechanics.energy import GIGAJOULE
from kuchka.units.mechanics.energy import JOULE
from kuchka.units.mechanics.energy import KILOJOULE
from kuchka.units.mechanics.energy import MEGAJOULE
from kuchka.units.temporal.time import HOUR
from kuchka.units.temporal.time import MINUTE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

WATT_NAME = "watt"
WATT_SYMBOL = "W"

PICOWATT = prefixed_unit(prefixes.PICO, WATT_NAME, WATT_SYMBOL, POWER)
NANOWATT = prefixed_unit(prefixes.NANO, WATT_NAME, WATT_SYMBOL, POWER)
MICROWATT = prefixed_unit(prefixes.MICRO, WATT_NAME, WATT_SYMBOL, POWER)
MILLIWATT = prefixed_unit(prefixes.MILLI, WATT_NAME, WATT_SYMBOL, POWER)
WATT = prefixed_unit(prefixes.UNIT, WATT_NAME, WATT_SYMBOL, POWER)
KILOWATT = prefixed_unit(prefixes.KILO, WATT_NAME, WATT_SYMBOL, POWER)
MEGAWATT = prefixed_unit(prefixes.MEGA, WATT_NAME, WATT_SYMBOL, POWER)
GIGAWATT = prefixed_unit(prefixes.GIGA, WATT_NAME, WATT_SYMBOL, POWER)
TERAWATT = prefixed_unit(prefixes.TERA, WATT_NAME, WATT_SYMBOL, POWER)
PETAWATT = prefixed_unit(prefixes.PETA, WATT_NAME, WATT_SYMBOL, POWER)


Power._canonical_unit = WATT  # noqa: SLF001 -- this module owns Power's canonical unit


def Picowatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in picowatts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in picowatts.

    Returns
    -------
    Power
        Power represented in picowatts.

    Examples
    --------
    Very small optical and electronic signals can be measured in picowatts:

    >>> signal = Picowatt(10)
    >>> signal
    10 pW

    """
    return Power(to_exact(value) * PICOWATT.scale, PICOWATT)


def Nanowatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in nanowatts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in nanowatts.

    Returns
    -------
    Power
        Power represented in nanowatts.

    Examples
    --------
    A 250 nW signal represents a very small rate of energy transfer:

    >>> signal = Nanowatt(250)
    >>> signal
    250 nW

    """
    return Power(to_exact(value) * NANOWATT.scale, NANOWATT)


def Microwatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in microwatts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in microwatts.

    Returns
    -------
    Power
        Power represented in microwatts.

    Examples
    --------
    A low-power sensor or embedded circuit can operate at only a few tens of
    microwatts:

    >>> sleep_power = Microwatt(40)
    >>> sleep_power
    40 µW

    """
    return Power(to_exact(value) * MICROWATT.scale, MICROWATT)


def Milliwatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in milliwatts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in milliwatts.

    Returns
    -------
    Power
        Power represented in milliwatts.

    Examples
    --------
    Small electronic and optical components commonly use milliwatts as a natural power
    scale:

    >>> optical_output = Milliwatt(5)
    >>> optical_output
    5 mW

    """
    return Power(to_exact(value) * MILLIWATT.scale, MILLIWATT)


def Watt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in watts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in watts.

    Returns
    -------
    Power
        Power represented in watts.

    Examples
    --------
    One watt is one joule transferred every second:

    >>> power = Watt(1)
    >>> power
    1 W

    A 100 W load transfers energy at one hundred joules per second:

    >>> load = Watt(100)
    >>> load
    100 W

    """
    return Power(to_exact(value) * WATT.scale, WATT)


def Kilowatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in kilowatts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in kilowatts.

    Returns
    -------
    Power
        Power represented in kilowatts.

    Examples
    --------
    A 2 kW heater is a familiar household-scale power load:

    >>> heater = Kilowatt(2)
    >>> heater
    2 kW

    """
    return Power(to_exact(value) * KILOWATT.scale, KILOWATT)


def Megawatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in megawatts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in megawatts.

    Returns
    -------
    Power
        Power represented in megawatts.

    Examples
    --------
    Large industrial machines and electrical generators reach the megawatt scale:

    >>> machine = Megawatt(5)
    >>> machine
    5 MW

    """
    return Power(to_exact(value) * MEGAWATT.scale, MEGAWATT)


def Gigawatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in gigawatts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in gigawatts.

    Returns
    -------
    Power
        Power represented in gigawatts.

    Examples
    --------
    Gigawatts are a natural scale for large generating stations and power systems:

    >>> generating_station = Gigawatt(1)
    >>> generating_station
    1 GW

    """
    return Power(to_exact(value) * GIGAWATT.scale, GIGAWATT)


def Terawatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in terawatts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in terawatts.

    Returns
    -------
    Power
        Power represented in terawatts.

    Examples
    --------
    Terawatts describe power on a scale far beyond an individual machine:

    >>> large_scale_power = Terawatt(1)
    >>> large_scale_power
    1 TW

    """
    return Power(to_exact(value) * TERAWATT.scale, TERAWATT)


def Petawatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in petawatts.

    Parameters
    ----------
    value : Numeric
        Power magnitude in petawatts.

    Returns
    -------
    Power
        Power represented in petawatts.

    Examples
    --------
    Petawatt peak powers occur in ultrashort laser systems:

    >>> laser_peak_power = Petawatt(5)
    >>> laser_peak_power
    5 PW

    """
    return Power(to_exact(value) * PETAWATT.scale, PETAWATT)


# Horses.

HORSEPOWER = UnitDef(
    "horsepower",
    "hp",
    Decimal("745.69987158227022"),
    POWER,
    aliases=("HP",),
    words=("mechanical horsepower", "imperial horsepower"),
)

METRIC_HORSEPOWER = UnitDef(
    "metric_horsepower",
    "PS",
    Decimal("735.49875"),
    POWER,
    aliases=("CV", "cv"),
    words=("pferdestarke", "cheval vapeur"),
)


def Horsepower(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in mechanical horsepower.

    Parameters
    ----------
    value : Numeric
        Power magnitude in mechanical horsepower.

    Returns
    -------
    Power
        Power represented in mechanical horsepower.

    Notes
    -----
    One mechanical horsepower is exactly 550 foot-pound-force per second, equivalent
    to 745.69987158227022 W.

    Examples
    --------
    A nominal 100 hp engine is represented directly:

    >>> engine = Horsepower(100)
    >>> engine
    100 hp

    """
    return Power(to_exact(value) * HORSEPOWER.scale, HORSEPOWER)


def MetricHorsepower(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in metric horsepower.

    Parameters
    ----------
    value : Numeric
        Power magnitude in metric horsepower.

    Returns
    -------
    Power
        Power represented in metric horsepower.

    Notes
    -----
    One metric horsepower is exactly 735.49875 W.

    Examples
    --------
    Automotive specifications in continental Europe may use metric horsepower:

    >>> engine = MetricHorsepower(100)
    >>> engine
    100 PS

    """
    return Power(
        to_exact(value) * METRIC_HORSEPOWER.scale,
        METRIC_HORSEPOWER,
    )


# Energy per time.

JOULE_PER_MINUTE = UnitDef(
    "joule_per_minute",
    "J/min",
    JOULE.scale / MINUTE.scale,
    POWER,
    words=("joule per minute", "joules per minute"),
)
JOULE_PER_HOUR = UnitDef(
    "joule_per_hour",
    "J/h",
    JOULE.scale / HOUR.scale,
    POWER,
    aliases=("J/hr",),
    words=("joule per hour", "joules per hour"),
)
KILOJOULE_PER_MINUTE = UnitDef(
    "kilojoule_per_minute",
    "kJ/min",
    KILOJOULE.scale / MINUTE.scale,
    POWER,
    words=("kilojoule per minute", "kilojoules per minute"),
)
KILOJOULE_PER_HOUR = UnitDef(
    "kilojoule_per_hour",
    "kJ/h",
    KILOJOULE.scale / HOUR.scale,
    POWER,
    aliases=("kJ/hr",),
    words=("kilojoule per hour", "kilojoules per hour"),
)
MEGAJOULE_PER_HOUR = UnitDef(
    "megajoule_per_hour",
    "MJ/h",
    MEGAJOULE.scale / HOUR.scale,
    POWER,
    aliases=("MJ/hr",),
    words=("megajoule per hour", "megajoules per hour"),
)
GIGAJOULE_PER_HOUR = UnitDef(
    "gigajoule_per_hour",
    "GJ/h",
    GIGAJOULE.scale / HOUR.scale,
    POWER,
    aliases=("GJ/hr",),
    words=("gigajoule per hour", "gigajoules per hour"),
)


def JoulePerMinute(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in joules per minute.

    Parameters
    ----------
    value : Numeric
        Power magnitude in J/min.

    Returns
    -------
    Power
        Power represented in joules per minute.

    Notes
    -----
    One joule per minute is exactly 1/60 W.

    Examples
    --------
    A small calorimeter heater that delivers 600 J every minute runs at 10 W:

    >>> heater = JoulePerMinute(600)
    >>> heater
    600 J/min
    >>> from kuchka.units import WATT
    >>> heater.to(WATT)
    10 W

    Over a 15 minute run the same heater transfers exactly 9 kJ of energy:

    >>> from kuchka import Minute
    >>> from kuchka.units import KILOJOULE
    >>> (heater * Minute(15)).to(KILOJOULE)
    9 kJ

    """
    return Power(to_exact(value) * JOULE_PER_MINUTE.scale, JOULE_PER_MINUTE)


def JoulePerHour(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in joules per hour.

    Parameters
    ----------
    value : Numeric
        Power magnitude in J/h.

    Returns
    -------
    Power
        Power represented in joules per hour.

    Notes
    -----
    One joule per hour is exactly 1/3600 W.

    Examples
    --------
    A battery-powered weather station that spends 1800 J every hour averages half a
    watt:

    >>> station = JoulePerHour(1800)
    >>> station
    1800 J/h
    >>> from kuchka.units import MILLIWATT
    >>> station.to(MILLIWATT)
    500 mW

    A consumption computed from a measured energy and the time it took needs no extra
    conversion step.
    A sensor node that used 7200 J over two hours consumed 3600 J/h:

    >>> from kuchka import Hour
    >>> from kuchka import Joule
    >>> from kuchka.units import JOULE_PER_HOUR
    >>> (Joule(7200) / Hour(2)).to(JOULE_PER_HOUR)
    3600 J/h

    """
    return Power(to_exact(value) * JOULE_PER_HOUR.scale, JOULE_PER_HOUR)


def KilojoulePerMinute(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in kilojoules per minute.

    Parameters
    ----------
    value : Numeric
        Power magnitude in kJ/min.

    Returns
    -------
    Power
        Power represented in kilojoules per minute.

    Notes
    -----
    One kilojoule per minute is exactly 50/3 W.

    Examples
    --------
    Exercise physiology often states a metabolic rate as the energy spent per minute.
    A runner who spends about 36 kJ every minute works at 600 W:

    >>> runner = KilojoulePerMinute(36)
    >>> runner
    36 kJ/min
    >>> from kuchka.units import WATT
    >>> runner.to(WATT)
    600 W

    Holding that pace for a 30 minute run costs 1080 kJ in total, assuming the rate
    stays constant:

    >>> from kuchka import Minute
    >>> from kuchka.units import KILOJOULE
    >>> (runner * Minute(30)).to(KILOJOULE)
    1080 kJ

    """
    return Power(to_exact(value) * KILOJOULE_PER_MINUTE.scale, KILOJOULE_PER_MINUTE)


def KilojoulePerHour(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in kilojoules per hour.

    Parameters
    ----------
    value : Numeric
        Power magnitude in kJ/h.

    Returns
    -------
    Power
        Power represented in kilojoules per hour.

    Notes
    -----
    One kilojoule per hour is exactly 5/18 W.

    Examples
    --------
    Heat loads in refrigeration and air conditioning are commonly listed in kilojoules
    per hour.
    A server rack that dissipates 36 000 kJ/h puts 10 kW into the room:

    >>> rack = KilojoulePerHour(36_000)
    >>> rack
    36000 kJ/h
    >>> from kuchka.units import KILOWATT
    >>> rack.to(KILOWATT)
    10 kW

    The conversion is exact, so 3600 kJ/h is precisely one kilowatt:

    >>> from kuchka import Kilowatt
    >>> KilojoulePerHour(3600) == Kilowatt(1)
    True

    """
    return Power(to_exact(value) * KILOJOULE_PER_HOUR.scale, KILOJOULE_PER_HOUR)


def MegajoulePerHour(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in megajoules per hour.

    Parameters
    ----------
    value : Numeric
        Power magnitude in MJ/h.

    Returns
    -------
    Power
        Power represented in megajoules per hour.

    Notes
    -----
    One megajoule per hour is exactly 2500/9 W, or 277.777... W.

    Examples
    --------
    The input rating of a gas burner is quoted in megajoules per hour in some markets.
    A hob burner rated at 10.8 MJ/h draws 3 kW of fuel energy:

    >>> burner = MegajoulePerHour(10.8)
    >>> burner
    10.8 MJ/h
    >>> from kuchka.units import KILOWATT
    >>> burner.to(KILOWATT)
    3 kW

    Run for two hours at that rating, the burner consumes exactly 21.6 MJ of gas
    energy:

    >>> from kuchka import Hour
    >>> from kuchka.units import MEGAJOULE
    >>> (burner * Hour(2)).to(MEGAJOULE)
    21.6 MJ

    """
    return Power(to_exact(value) * MEGAJOULE_PER_HOUR.scale, MEGAJOULE_PER_HOUR)


def GigajoulePerHour(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in gigajoules per hour.

    Parameters
    ----------
    value : Numeric
        Power magnitude in GJ/h.

    Returns
    -------
    Power
        Power represented in gigajoules per hour.

    Notes
    -----
    One gigajoule per hour is exactly 2500/9 kW, or 277.777... kW.

    Examples
    --------
    A district heating substation that hands over 18 GJ of heat every hour transfers
    5 MW:

    >>> substation = GigajoulePerHour(18)
    >>> substation
    18 GJ/h
    >>> from kuchka.units import MEGAWATT
    >>> substation.to(MEGAWATT)
    5 MW

    Heat meters of large plants report gigajoules per hour, and the conversion is
    exact.
    A plant at 36 GJ/h is precisely a 10 MW source:

    >>> from kuchka import Megawatt
    >>> GigajoulePerHour(36) == Megawatt(10)
    True

    """
    return Power(to_exact(value) * GIGAJOULE_PER_HOUR.scale, GIGAJOULE_PER_HOUR)


POWER_UNITS: Mapping[str, Callable[[Numeric], Power]] = unit_table(
    "POWER_UNITS",
    {
        PICOWATT: Picowatt,
        NANOWATT: Nanowatt,
        MICROWATT: Microwatt,
        MILLIWATT: Milliwatt,
        WATT: Watt,
        KILOWATT: Kilowatt,
        MEGAWATT: Megawatt,
        GIGAWATT: Gigawatt,
        TERAWATT: Terawatt,
        PETAWATT: Petawatt,
        HORSEPOWER: Horsepower,
        METRIC_HORSEPOWER: MetricHorsepower,
        JOULE_PER_MINUTE: JoulePerMinute,
        JOULE_PER_HOUR: JoulePerHour,
        KILOJOULE_PER_MINUTE: KilojoulePerMinute,
        KILOJOULE_PER_HOUR: KilojoulePerHour,
        MEGAJOULE_PER_HOUR: MegajoulePerHour,
        GIGAJOULE_PER_HOUR: GigajoulePerHour,
    },
)

__all__ = [
    "GIGAJOULE_PER_HOUR",
    "GIGAWATT",
    "HORSEPOWER",
    "JOULE_PER_HOUR",
    "JOULE_PER_MINUTE",
    "KILOJOULE_PER_HOUR",
    "KILOJOULE_PER_MINUTE",
    "KILOWATT",
    "MEGAJOULE_PER_HOUR",
    "MEGAWATT",
    "METRIC_HORSEPOWER",
    "MICROWATT",
    "MILLIWATT",
    "NANOWATT",
    "PETAWATT",
    "PICOWATT",
    "POWER_UNITS",
    "TERAWATT",
    "WATT",
    "GigajoulePerHour",
    "Gigawatt",
    "Horsepower",
    "JoulePerHour",
    "JoulePerMinute",
    "KilojoulePerHour",
    "KilojoulePerMinute",
    "Kilowatt",
    "MegajoulePerHour",
    "Megawatt",
    "MetricHorsepower",
    "Microwatt",
    "Milliwatt",
    "Nanowatt",
    "Petawatt",
    "Picowatt",
    "Terawatt",
    "Watt",
]
