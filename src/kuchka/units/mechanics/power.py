"""Power constructors: picowatts to petawatts, horsepower, and joules per hour.

`Power` is the rate at which energy is transferred or converted, `P = dE / dt`.
Its canonical unit is the watt, defined as one joule per second.
Every constructor in this module scales relative to the watt.

The module provides:

* `Picowatt` through `Petawatt`, the SI prefixes of the watt;
* `Horsepower` and `MetricHorsepower`, the engine ratings of two traditions;
* `JoulePerMinute`, `JoulePerHour`, `KilojoulePerMinute`, `KilojoulePerHour`,
  `MegajoulePerHour`, and `GigajoulePerHour`, a power written as the energy spent over
  a minute or an hour.

A voltage and a current make a power with one multiplication:

>>> from kuchka import Ampere
>>> from kuchka import Volt
>>> Volt(12) * Ampere(2)
24 W

The units span an enormous range, and each scale belongs to a field.
Picowatts and nanowatts are the signals of optical detectors and the leakage of
sleeping electronics.
Microwatts and milliwatts describe energy-harvesting sensors, radios, and laser
pointers.
Watts and kilowatts are the household and the vehicle: lamps, kettles, motors, and
charging stations.
Megawatts and gigawatts are wind turbines, locomotives, and power stations.
Terawatts describe the energy system of a planet, and petawatts the peak of the
strongest pulsed lasers and the sunlight that Earth intercepts.
Horsepower rates engines, and the joule-per-hour units serve the fields that log an
energy and state a consumption per hour: sensor logging, exercise physiology, heating,
and gas appliances.

Examples
--------
The same power arises in different physical domains.
A cyclist who overcomes 25 N of drag at 8 m/s and a motor that turns at 100 rad/s
against a torque of 2 N·m both deliver 200 W:

>>> from kuchka import Newton
>>> from kuchka import NewtonMetre
>>> from kuchka import MetrePerSecond
>>> from kuchka import RadianPerSecond
>>> cyclist = Newton(25) * MetrePerSecond(8)
>>> motor = NewtonMetre(2) * RadianPerSecond(100)
>>> cyclist
200 W
>>> cyclist == motor
True

Hydraulics adds a third route.
A pump that pushes 60 L/min against a pressure of 5 bar does work at 500 W:

>>> from kuchka import Bar
>>> from kuchka import LitrePerMinute
>>> from kuchka.units import WATT
>>> (Bar(5) * LitrePerMinute(60)).to(WATT)
500 W

Energy and power convert through time.
A 2 kW heater that runs for three hours transfers 6 kWh, and dividing that energy by
the same three hours returns the power:

>>> from kuchka import Hour
>>> from kuchka.units import KILOWATT
>>> from kuchka.units import KILOWATT_HOUR
>>> heat = (Kilowatt(2) * Hour(3)).to(KILOWATT_HOUR)
>>> heat
6 kWh
>>> (heat / Hour(3)).to(KILOWATT)
2 kW

A log that records an energy and the time it took gives the consumption in joules per
hour directly.
A device that spent 5400 J in 90 minutes consumed 3600 J/h, which is one watt:

>>> from kuchka import Joule
>>> from kuchka import Minute
>>> from kuchka.units import JOULE_PER_HOUR
>>> consumption = (Joule(5400) / Minute(90)).to(JOULE_PER_HOUR)
>>> consumption
3600 J/h
>>> consumption == Watt(1)
True

Peak power and average power describe different properties of a pulsed system.
A laser that fires 30 J pulses of 30 fs reaches 1 PW at the peak, and at ten pulses per
second it averages only 300 W:

>>> from kuchka import Femtosecond
>>> from kuchka import Hertz
>>> from kuchka.units import PETAWATT
>>> pulse = Joule(30)
>>> (pulse / Femtosecond(30)).to(PETAWATT)
1 PW
>>> (pulse * Hertz(10)).to(WATT)
300 W

The two horsepower definitions give different powers, which matters when engine
specifications are imported from different markets:

>>> Horsepower(1) != MetricHorsepower(1)
True

Notes
-----
The watt is the SI coherent unit of power:

`1 W = 1 J / s`.

A watt is a rate of energy transfer.
An amount of energy is measured in joules or watt-hours: running a 1 kW load for one
hour transfers 1 kWh, while the power stays 1 kW throughout the interval.

SI prefixes are exact powers of ten:

>>> Kilowatt(1) == Watt(1000)
True

The joule-per-time units are the watt written as an energy over a time, so their
scales are exact fractions of a watt:

`1 J/min = 1/60 W`,

`1 J/h = 1/3600 W`,

`1 kJ/h = 5/18 W`.

>>> JoulePerHour(3600) == Watt(1)
True

>>> MegajoulePerHour(3.6) == Kilowatt(1)
True

`Horsepower` is the mechanical horsepower of exactly 550 foot-pound-force per second.
With the exact international foot and pound and standard gravity, it is exactly
745.69987158227022 W.
`MetricHorsepower` is the continental horsepower of exactly 75 kilogram-force metres
per second, or 735.49875 W.
Neither is an SI unit, and both remain common in engine and motor specifications.

`POWER_UNITS` maps symbols such as ``"pW"``, ``"mW"``, ``"W"``, ``"kW"``, ``"MW"``,
``"hp"``, ``"PS"``, ``"J/h"``, and ``"MJ/h"`` to their constructors.
This is intended for boundary code that receives units as external data.

References
----------
BIPM, The International System of Units (SI Brochure), on the watt:
https://www.bipm.org/en/publications/si-brochure

NIST, Special Publication 811, Guide for the Use of the International System of Units,
on the two horsepower definitions:
https://www.nist.gov/pml/special-publication-811

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
~kuchka.units.mechanics.energy
    Energy units, including the joule and the kilowatt-hour.

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
    An optical receiver at the sensitivity limit of a fibre link detects a signal of
    about 10 pW, which is -80 dBm:

    >>> signal = Picowatt(10)
    >>> signal
    10 pW

    Collected for 100 s at a constant power, that signal delivers exactly 1 nJ:

    >>> from kuchka import Second
    >>> from kuchka.units import NANOJOULE
    >>> (signal * Second(100)).to(NANOJOULE)
    1 nJ

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
    Some real-time clock chips keep time on a few hundred nanowatts:

    >>> clock = Nanowatt(390)
    >>> clock
    390 nW

    That figure is a 130 nA draw from a 3 V supply:

    >>> from kuchka import Nanoampere
    >>> from kuchka import Volt
    >>> Volt(3) * Nanoampere(130) == clock
    True

    Over a day the clock costs 33.696 mJ of energy:

    >>> from kuchka import Hour
    >>> from kuchka.units import MILLIJOULE
    >>> (clock * Hour(24)).to(MILLIJOULE)
    33.696 mJ

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
    A wireless sensor node asleep between readings can draw a few microwatts, such
    as 2 µA from a 3 V supply:

    >>> sleep_power = Microwatt(6)
    >>> sleep_power
    6 µW

    An indoor photovoltaic cell harvests about 50 µW.
    A reading that costs 0.5 mJ can then be taken every 10 s, assuming the harvest
    arrives at a constant rate:

    >>> from kuchka import Millijoule
    >>> from kuchka.units import SECOND
    >>> (Millijoule(0.5) / Microwatt(50)).to(SECOND)
    10 s

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
    Visible laser pointers of class 3R are limited to 5 mW of output:

    >>> pointer = Milliwatt(5)
    >>> pointer
    5 mW

    Left on for ten minutes, such a pointer emits a total of 3 J of light:

    >>> from kuchka import Minute
    >>> pointer * Minute(10)
    3 J

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
    A household LED lamp draws about 9 W:

    >>> lamp = Watt(9)
    >>> lamp
    9 W

    Equipment that draws 100 W around the clock uses 2.4 kWh in a day:

    >>> from kuchka import Day
    >>> from kuchka.units import KILOWATT_HOUR
    >>> (Watt(100) * Day(1)).to(KILOWATT_HOUR)
    2.4 kWh

    A force at a speed and a torque at an angular velocity are powers too.
    A cyclist who overcomes 25 N of drag at 8 m/s delivers 200 W, and so does a motor
    that turns at 100 rad/s against 2 N·m:

    >>> from kuchka import MetrePerSecond
    >>> from kuchka import Newton
    >>> from kuchka import NewtonMetre
    >>> from kuchka import RadianPerSecond
    >>> Newton(25) * MetrePerSecond(8)
    200 W
    >>> NewtonMetre(2) * RadianPerSecond(100)
    200 W

    A watt is a rate, so adding an amount of energy to it is rejected:

    >>> from kuchka import Joule
    >>> Watt(1) + Joule(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    kuchka.errors.IncompatibleDimensionError: ...

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
    An electric kettle is rated at 2 kW:

    >>> kettle = Kilowatt(2)
    >>> kettle
    2 kW

    Boiling for three minutes uses a tenth of a kilowatt-hour:

    >>> from kuchka import Minute
    >>> from kuchka.units import KILOWATT_HOUR
    >>> (kettle * Minute(3)).to(KILOWATT_HOUR)
    0.1 kWh

    An 11 kW wallbox recharges a 55 kWh battery from empty in five hours, assuming it
    holds full power throughout:

    >>> from kuchka import KilowattHour
    >>> from kuchka.units import HOUR
    >>> (KilowattHour(55) / Kilowatt(11)).to(HOUR)
    5 h

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
    An onshore wind turbine has a rated power of about 3 MW:

    >>> turbine = Megawatt(3)
    >>> turbine
    3 MW

    At a capacity factor of 35 percent it averages 1.05 MW, which is 25 200 kWh over a
    day:

    >>> from kuchka import Day
    >>> from kuchka import Percent
    >>> from kuchka.units import KILOWATT_HOUR
    >>> from kuchka.units import MEGAWATT
    >>> average = turbine * Percent(35)
    >>> average.to(MEGAWATT)
    1.05 MW
    >>> (average * Day(1)).to(KILOWATT_HOUR)
    25200 kWh

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
    A nuclear power unit has an electrical output of about 1 GW:

    >>> reactor = Gigawatt(1)
    >>> reactor
    1 GW

    Running for 24 hours at that output, it generates 86.4 TJ:

    >>> from kuchka import Hour
    >>> from kuchka.units import TERAJOULE
    >>> (reactor * Hour(24)).to(TERAJOULE)
    86.4 TJ

    For households that average 500 W, one such unit supplies two million of them:

    >>> round((reactor / Watt(500)).magnitude)
    2000000

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
    The primary energy supply of the world averages roughly 19 TW:

    >>> world = Terawatt(19)
    >>> world
    19 TW

    Shared over eight billion people, that is an average continuous power of
    2.375 kW per person:

    >>> from kuchka.units import KILOWATT
    >>> (world / 8_000_000_000).to(KILOWATT)
    2.375 kW

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
    Petawatt-class lasers reach their peak power in extremely short pulses:

    >>> peak = Petawatt(1)
    >>> peak
    1 PW

    A pulse of 30 fs at that peak power carries only 30 J of energy:

    >>> from kuchka import Femtosecond
    >>> peak * Femtosecond(30)
    30 J

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
    A truck engine is rated at 300 hp:

    >>> engine = Horsepower(300)
    >>> engine
    300 hp

    The conversion to SI is exact:

    >>> from kuchka.units import KILOWATT
    >>> engine.to(KILOWATT)
    223.709961474681066 kW

    The unit comes from the foot-pound-force, so lifting 550 lbf at one foot per second
    is exactly one horsepower:

    >>> from kuchka import Foot
    >>> from kuchka import PoundForce
    >>> from kuchka import Second
    >>> PoundForce(550) * (Foot(1) / Second(1)) == Horsepower(1)
    True

    A specification sheet written as text reads through `parse`, and the spelling `HP`
    is the same unit:

    >>> from kuchka import Power
    >>> from kuchka import parse
    >>> parse("300 HP", Power)
    300 hp

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
    One metric horsepower is exactly 75 kilogram-force metres per second, equivalent
    to 735.49875 W.

    Examples
    --------
    A European car is listed at 110 PS:

    >>> car = MetricHorsepower(110)
    >>> car
    110 PS

    The same car in kilowatts, exactly:

    >>> from kuchka.units import KILOWATT
    >>> car.to(KILOWATT)
    80.9048625 kW

    The unit is defined by a weight lifted at a speed: 75 kgf at one metre per second
    is exactly one metric horsepower:

    >>> from kuchka import KilogramForce
    >>> from kuchka import MetrePerSecond
    >>> KilogramForce(75) * MetrePerSecond(1) == MetricHorsepower(1)
    True

    French and Italian documents write the same unit as CV, which reads as PS:

    >>> from kuchka import Power
    >>> from kuchka import parse
    >>> parse("110 CV", Power)
    110 PS

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

POWER_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        PICOWATT,
        NANOWATT,
        MICROWATT,
        MILLIWATT,
        WATT,
        KILOWATT,
        MEGAWATT,
        GIGAWATT,
        TERAWATT,
        PETAWATT,
    ),
    (
        JOULE_PER_HOUR,
        KILOJOULE_PER_HOUR,
        MEGAJOULE_PER_HOUR,
        GIGAJOULE_PER_HOUR,
    ),
    (
        JOULE_PER_MINUTE,
        KILOJOULE_PER_MINUTE,
    ),
)
"""The runs of units `auto_scale` moves a power along.

There is one run for each family of prefixed units, smallest first.
"""

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
    "POWER_LADDERS",
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
