"""Fluence constructors: J/m², J/cm², mJ/cm², and kWh/m², from lasers to sunshine.

`Fluence` is the energy delivered to a surface per area, `Energy / Area`, and a radiant
exposure is one too.
Its canonical unit is the joule per square metre (`J/m²`).
The module provides:

* `JoulePerSquareMetre`, `KilojoulePerSquareMetre`, and `MegajoulePerSquareMetre`;
* `JoulePerSquareCentimetre`, `MillijoulePerSquareCentimetre`, and
  `MicrojoulePerSquareCentimetre`;
* `WattHourPerSquareMetre` and `KilowattHourPerSquareMetre`.

A laser pulse that puts 80 mJ on a spot of half a square centimetre delivers a fluence
of 160 mJ/cm²:

>>> from kuchka import Millijoule
>>> from kuchka import SquareCentimetre
>>> from kuchka.units import MILLIJOULE_PER_SQUARE_CENTIMETRE
>>> pulse = Millijoule(80) / SquareCentimetre(0.5)
>>> pulse.to(MILLIJOULE_PER_SQUARE_CENTIMETRE)
160 mJ/cm²

Each unit belongs to the field that counts energy per area:

* microjoules per square centimetre (µJ/cm²) describe weak pulsed beams on sensors and
  detectors;
* millijoules per square centimetre (mJ/cm²) are the doses of ultraviolet disinfection
  and curing, and the pulse fluence of excimer laser surgery;
* joules per square centimetre (J/cm²) are the settings of therapeutic and aesthetic
  lasers, such as hair removal, and the damage thresholds of optical coatings;
* joules and kilojoules per square metre (J/m², kJ/m²) count the erythemal dose of
  sunburn research and the radiant exposure of radiometry;
* watt-hours and kilowatt-hours per square metre (Wh/m², kWh/m²) are the daily and
  annual insolation of solar energy and building physics, and megajoules per square
  metre (MJ/m²) are the same insolation in meteorology and agronomy.

Examples
--------
Ultraviolet disinfection is designed around a dose.
A reactor that must deliver 40 mJ/cm² under a lamp of 0.5 mW/cm² needs 80 s of
exposure, assuming the irradiance stays constant:

>>> from kuchka import MilliwattPerSquareCentimetre
>>> from kuchka import MillijoulePerSquareCentimetre
>>> from kuchka.units import SECOND
>>> dose = MillijoulePerSquareCentimetre(40)
>>> lamp = MilliwattPerSquareCentimetre(0.5)
>>> (dose / lamp).to(SECOND)
80 s

A solar designer counts the sunshine of a day as peak sun hours.
One kW/m² for five hours is 5 kWh/m², which a weather service writes as 18 MJ/m²:

>>> from kuchka import Hour
>>> from kuchka import KilowattPerSquareMetre
>>> from kuchka.units import KILOWATT_HOUR_PER_SQUARE_METRE
>>> from kuchka.units import MEGAJOULE_PER_SQUARE_METRE
>>> day = KilowattPerSquareMetre(1) * Hour(5)
>>> day.to(KILOWATT_HOUR_PER_SQUARE_METRE)
5 kWh/m²
>>> day.to(MEGAJOULE_PER_SQUARE_METRE)
18 MJ/m²

A fluence over an area is an energy.
A diode laser handpiece at 20 J/cm² on a spot of 2 cm² delivers 40 J per pulse,
assuming the fluence is uniform over the spot:

>>> from kuchka.units import JOULE
>>> setting = JoulePerSquareCentimetre(20)
>>> (setting * SquareCentimetre(2)).to(JOULE)
40 J

A weather station that logs 600 Wh/m² for an hour reports a mean irradiance of
600 W/m², a heat flux:

>>> from kuchka import WattHourPerSquareMetre
>>> WattHourPerSquareMetre(600) / Hour(1)
600 W/m²

A fluence shares its dimension with a surface tension, and the move between them is
explicit.
One joule per square metre is one newton per metre:

>>> from kuchka import Metre
>>> JoulePerSquareMetre(3).to_surface_tension() * Metre(2)
6 N

A fluence times a length is refused, because the product has no meaning for an energy
per area:

>>> JoulePerSquareMetre(3) * Metre(2)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...

Notes
-----
One joule per square metre is one newton per metre and one kilogram per second squared:

`1 J/m² = 1 N/m = 1 kg/s²`.

The relations of a fluence are the integral of a flux and the energy over an area:

`H = ∫ E dt` and `H = Q / A`.

With a constant irradiance `E`, the fluence of a duration `t` is `E · t`.

The conversions are exact:

`1 J/cm² = 10 000 J/m²`,

`1 Wh/m² = 3600 J/m²`,

and `1 kWh/m² = 3.6 MJ/m²`.

>>> KilowattHourPerSquareMetre(1) == MegajoulePerSquareMetre(3.6)
True

A radiant exposure, a UV dose, and an insolation are read as a `Fluence`.
A dose that an action spectrum weights, such as the erythemal dose, is a weighted
quantity, and its unit spelling carries the weighting outside the library.

`FLUENCE_UNITS` maps symbols such as ``"J/cm2"``, ``"mJ/cm2"``, and ``"kWh/m2"`` to
their constructors, for boundary code that reads a unit as a string from outside the
application.

References
----------
CIE, International Lighting Vocabulary (ILV), on radiant exposure:
https://cie.co.at/e-ilv

BIPM, The International System of Units (SI Brochure), on the joule:
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.Energy
    Fluence is energy per area.
~kuchka.quantities.HeatFlux
    The irradiance whose time integral is a fluence.
~kuchka.quantities.SurfaceTension
    The principal kind of the same dimension.
~kuchka.units.photometry.luminous_exposure
    The photometric counterpart, lux seconds.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import SURFACE_TENSION
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import Fluence
from kuchka.quantities import UnitDef
from kuchka.units.geometry.area import SQUARE_CENTIMETRE
from kuchka.units.mechanics.energy import JOULE
from kuchka.units.mechanics.energy import KILOWATT_HOUR
from kuchka.units.mechanics.energy import WATT_HOUR

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

JOULE_PER_SQUARE_METRE = UnitDef(
    "joule_per_square_metre",
    "J/m²",
    1,
    SURFACE_TENSION,
    aliases=powered("J/m", 2),
    words=("joules per square metre", "joules per square meter"),
)
KILOJOULE_PER_SQUARE_METRE = with_prefix(prefixes.KILO, JOULE_PER_SQUARE_METRE)
MEGAJOULE_PER_SQUARE_METRE = with_prefix(prefixes.MEGA, JOULE_PER_SQUARE_METRE)
JOULE_PER_SQUARE_CENTIMETRE = UnitDef(
    "joule_per_square_centimetre",
    "J/cm²",
    JOULE.scale / SQUARE_CENTIMETRE.scale,
    SURFACE_TENSION,
    aliases=powered("J/cm", 2),
    words=("joules per square centimetre", "joules per square centimeter"),
)
MILLIJOULE_PER_SQUARE_CENTIMETRE = with_prefix(
    prefixes.MILLI, JOULE_PER_SQUARE_CENTIMETRE
)
MICROJOULE_PER_SQUARE_CENTIMETRE = with_prefix(
    prefixes.MICRO, JOULE_PER_SQUARE_CENTIMETRE
)
WATT_HOUR_PER_SQUARE_METRE = UnitDef(
    "watt_hour_per_square_metre",
    "Wh/m²",
    WATT_HOUR.scale,
    SURFACE_TENSION,
    aliases=powered("Wh/m", 2),
    words=("watt hours per square metre", "watt hours per square meter"),
)
KILOWATT_HOUR_PER_SQUARE_METRE = UnitDef(
    "kilowatt_hour_per_square_metre",
    "kWh/m²",
    KILOWATT_HOUR.scale,
    SURFACE_TENSION,
    aliases=powered("kWh/m", 2),
    words=("kilowatt hours per square metre", "kilowatt hours per square meter"),
)

Fluence._canonical_unit = JOULE_PER_SQUARE_METRE  # noqa: SLF001 -- this module owns Fluence's canonical unit


def JoulePerSquareMetre(value: Numeric) -> Fluence:
    """Construct a Fluence from joules per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in joules per square metre.

    Returns
    -------
    Fluence
        Fluence represented in joules per square metre.

    Notes
    -----
    One joule per square metre is one newton per metre.

    Examples
    --------
    Sunburn research counts ultraviolet exposure in standard erythema doses, and one
    dose is 100 J/m² of erythemally weighted radiation.
    A reading of 250 J/m² is two and a half doses:

    >>> exposure = JoulePerSquareMetre(250)
    >>> exposure
    250 J/m²
    >>> float((exposure / JoulePerSquareMetre(100)).magnitude)
    2.5

    A joule per square metre is the energy that a unit surface takes, so 3 J/m² over
    4 m² is 12 J:

    >>> from kuchka import SquareMetre
    >>> JoulePerSquareMetre(3) * SquareMetre(4)
    12 J

    """
    return Fluence(
        to_exact(value) * JOULE_PER_SQUARE_METRE.scale, JOULE_PER_SQUARE_METRE
    )


def KilojoulePerSquareMetre(value: Numeric) -> Fluence:
    """Construct a Fluence from kilojoules per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilojoules per square metre.

    Returns
    -------
    Fluence
        Fluence represented in kilojoules per square metre.

    Examples
    --------
    Sunburn research reports the erythemal ultraviolet dose of a day in kilojoules per
    square metre, and a summer day at mid latitudes gives a few of them:

    >>> daily_dose = KilojoulePerSquareMetre(5)
    >>> daily_dose
    5 kJ/m²

    In the units of a disinfection reactor, 1 kJ/m² is 100 mJ/cm²:

    >>> from kuchka.units import MILLIJOULE_PER_SQUARE_CENTIMETRE
    >>> KilojoulePerSquareMetre(1).to(MILLIJOULE_PER_SQUARE_CENTIMETRE)
    100 mJ/cm²

    """
    return Fluence(
        to_exact(value) * KILOJOULE_PER_SQUARE_METRE.scale, KILOJOULE_PER_SQUARE_METRE
    )


def MegajoulePerSquareMetre(value: Numeric) -> Fluence:
    """Construct a Fluence from megajoules per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in megajoules per square metre.

    Returns
    -------
    Fluence
        Fluence represented in megajoules per square metre.

    Examples
    --------
    Meteorological stations and agronomic models state the solar radiation of a day in
    megajoules per square metre, and a clear summer day gives about 25 MJ/m²:

    >>> summer_day = MegajoulePerSquareMetre(25)
    >>> summer_day
    25 MJ/m²

    In the units of a solar designer, 18 MJ/m² is exactly 5 kWh/m²:

    >>> from kuchka.units import KILOWATT_HOUR_PER_SQUARE_METRE
    >>> MegajoulePerSquareMetre(18).to(KILOWATT_HOUR_PER_SQUARE_METRE)
    5 kWh/m²

    """
    return Fluence(
        to_exact(value) * MEGAJOULE_PER_SQUARE_METRE.scale, MEGAJOULE_PER_SQUARE_METRE
    )


def JoulePerSquareCentimetre(value: Numeric) -> Fluence:
    """Construct a Fluence from joules per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in joules per square centimetre.

    Returns
    -------
    Fluence
        Fluence represented in joules per square centimetre.

    Notes
    -----
    One joule per square centimetre is exactly 10 000 joules per square metre.

    Examples
    --------
    Diode lasers for hair removal are set to a fluence in the range of 10 to
    40 J/cm²:

    >>> setting = JoulePerSquareCentimetre(20)
    >>> setting
    20 J/cm²

    The same setting in SI units is 200 000 J/m²:

    >>> from kuchka.units import JOULE_PER_SQUARE_METRE
    >>> setting.to(JOULE_PER_SQUARE_METRE)
    200000 J/m²

    """
    return Fluence(
        to_exact(value) * JOULE_PER_SQUARE_CENTIMETRE.scale, JOULE_PER_SQUARE_CENTIMETRE
    )


def MillijoulePerSquareCentimetre(value: Numeric) -> Fluence:
    """Construct a Fluence from millijoules per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in millijoules per square centimetre.

    Returns
    -------
    Fluence
        Fluence represented in millijoules per square centimetre.

    Examples
    --------
    The design dose of an ultraviolet water disinfection reactor is often 40 mJ/cm²:

    >>> design_dose = MillijoulePerSquareCentimetre(40)
    >>> design_dose
    40 mJ/cm²

    A reactor that delivers 25 mJ/cm² each second reaches the design dose in 1.6 s,
    assuming the dose accumulates at a constant rate:

    >>> from kuchka import Second
    >>> from kuchka.units import SECOND
    >>> dose_rate = MillijoulePerSquareCentimetre(25) / Second(1)
    >>> (design_dose / dose_rate).to(SECOND)
    1.6 s

    """
    return Fluence(
        to_exact(value) * MILLIJOULE_PER_SQUARE_CENTIMETRE.scale,
        MILLIJOULE_PER_SQUARE_CENTIMETRE,
    )


def MicrojoulePerSquareCentimetre(value: Numeric) -> Fluence:
    """Construct a Fluence from microjoules per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in microjoules per square centimetre.

    Returns
    -------
    Fluence
        Fluence represented in microjoules per square centimetre.

    Examples
    --------
    A weak pulsed beam that reaches an imaging sensor deposits tens of microjoules per
    square centimetre:

    >>> beam = MicrojoulePerSquareCentimetre(30)
    >>> beam
    30 µJ/cm²

    On a sensor of 2 cm² that is 60 µJ of pulse energy:

    >>> from kuchka import SquareCentimetre
    >>> from kuchka.units import MICROJOULE
    >>> (beam * SquareCentimetre(2)).to(MICROJOULE)
    60 µJ

    """
    return Fluence(
        to_exact(value) * MICROJOULE_PER_SQUARE_CENTIMETRE.scale,
        MICROJOULE_PER_SQUARE_CENTIMETRE,
    )


def WattHourPerSquareMetre(value: Numeric) -> Fluence:
    """Construct a Fluence from watt-hours per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in watt-hours per square metre.

    Returns
    -------
    Fluence
        Fluence represented in watt-hours per square metre.

    Notes
    -----
    One watt-hour per square metre is exactly 3600 joules per square metre.

    Examples
    --------
    Weather stations log the global radiation of each hour in watt-hours per square
    metre, and a bright noon hour gives about 800 Wh/m²:

    >>> noon = WattHourPerSquareMetre(800)
    >>> noon
    800 Wh/m²

    Six such hours collect 4.8 kWh/m²:

    >>> from kuchka.units import KILOWATT_HOUR_PER_SQUARE_METRE
    >>> (noon * 6).to(KILOWATT_HOUR_PER_SQUARE_METRE)
    4.8 kWh/m²

    """
    return Fluence(
        to_exact(value) * WATT_HOUR_PER_SQUARE_METRE.scale, WATT_HOUR_PER_SQUARE_METRE
    )


def KilowattHourPerSquareMetre(value: Numeric) -> Fluence:
    """Construct a Fluence from kilowatt-hours per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilowatt-hours per square metre.

    Returns
    -------
    Fluence
        Fluence represented in kilowatt-hours per square metre.

    Notes
    -----
    One kilowatt-hour per square metre is exactly 3.6 megajoules per square metre.

    Examples
    --------
    Solar designers rate a site by its insolation, and a temperate site collects about
    1100 kWh/m² over a year:

    >>> site = KilowattHourPerSquareMetre(1100)
    >>> site
    1100 kWh/m²

    A 20 m² array that converts 20 percent of that insolation yields 4400 kWh, assuming
    the efficiency is constant over the year:

    >>> from kuchka import Percent
    >>> from kuchka import SquareMetre
    >>> from kuchka.units import KILOWATT_HOUR
    >>> (site * SquareMetre(20) * Percent(20)).to(KILOWATT_HOUR)
    4400 kWh

    """
    return Fluence(
        to_exact(value) * KILOWATT_HOUR_PER_SQUARE_METRE.scale,
        KILOWATT_HOUR_PER_SQUARE_METRE,
    )


FLUENCE_UNITS: Mapping[str, Callable[[Numeric], Fluence]] = unit_table(
    "FLUENCE_UNITS",
    {
        JOULE_PER_SQUARE_METRE: JoulePerSquareMetre,
        KILOJOULE_PER_SQUARE_METRE: KilojoulePerSquareMetre,
        MEGAJOULE_PER_SQUARE_METRE: MegajoulePerSquareMetre,
        JOULE_PER_SQUARE_CENTIMETRE: JoulePerSquareCentimetre,
        MILLIJOULE_PER_SQUARE_CENTIMETRE: MillijoulePerSquareCentimetre,
        MICROJOULE_PER_SQUARE_CENTIMETRE: MicrojoulePerSquareCentimetre,
        WATT_HOUR_PER_SQUARE_METRE: WattHourPerSquareMetre,
        KILOWATT_HOUR_PER_SQUARE_METRE: KilowattHourPerSquareMetre,
    },
)

__all__ = [
    "FLUENCE_UNITS",
    "JOULE_PER_SQUARE_CENTIMETRE",
    "JOULE_PER_SQUARE_METRE",
    "KILOJOULE_PER_SQUARE_METRE",
    "KILOWATT_HOUR_PER_SQUARE_METRE",
    "MEGAJOULE_PER_SQUARE_METRE",
    "MICROJOULE_PER_SQUARE_CENTIMETRE",
    "MILLIJOULE_PER_SQUARE_CENTIMETRE",
    "WATT_HOUR_PER_SQUARE_METRE",
    "JoulePerSquareCentimetre",
    "JoulePerSquareMetre",
    "KilojoulePerSquareMetre",
    "KilowattHourPerSquareMetre",
    "MegajoulePerSquareMetre",
    "MicrojoulePerSquareCentimetre",
    "MillijoulePerSquareCentimetre",
    "WattHourPerSquareMetre",
]
