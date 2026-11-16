"""Absorbed dose rate constructors: grays and rads per second, minute, and hour.

`AbsorbedDoseRate` is the absorbed dose delivered per unit time.
The module provides the gray per second, minute, and hour with the multiples that
instruments and radiotherapy use, and the rad per hour of older survey meters:

>>> from kuchka import GrayPerMinute
>>> from kuchka import MicrograyPerHour
>>> field = MicrograyPerHour(0.09)
>>> beam = GrayPerMinute(2)

The canonical unit is the gray per second (`Gy/s`), exactly one watt per kilogram, and
the results of arithmetic display in the gray per hour.
Natural background sits at nanograys and micrograys per hour, a radiotherapy beam
delivers grays per minute, and an industrial gamma irradiator delivers kilograys
per hour.

Examples
--------
A gamma irradiator sterilises medical devices with a dose of 25 kGy.
At a dose rate of 10 000 Gy/h, the exposure takes two and a half hours:

>>> from kuchka import GrayPerHour
>>> from kuchka import Kilogray
>>> from kuchka.units import HOUR
>>> (Kilogray(25) / GrayPerHour(10_000)).to(HOUR)
2.5 h

Natural external background of 0.09 µGy/h, kept up for a year of 8766 hours, adds up
to under a milligray:

>>> from kuchka import Hour
>>> from kuchka import MicrograyPerHour
>>> from kuchka.units import MILLIGRAY
>>> year = MicrograyPerHour(0.09) * Hour(8766)
>>> f"{year.to(MILLIGRAY):.2f}"
'0.79 mGy'

Rates in different units add, and the sum displays in the gray per hour:

>>> from kuchka import GrayPerMinute
>>> GrayPerHour(1) + GrayPerMinute(1)
61 Gy/h

A rate and a dose are different quantities, so the two refuse to add:

>>> from kuchka import Gray
>>> GrayPerHour(1) + Gray(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...

Notes
-----
`AbsorbedDoseRate` has the dimension of `SpecificPower`, which is energy per mass per
time, and the two are distinct quantities.
`AbsorbedDoseRate.to_specific_power()` and `AbsorbedDoseRate.from_specific_power()`
move between them, and one gray per second is exactly one watt per kilogram.

The rad is exactly one hundredth of a gray, so a rad per hour is exactly 10 mGy/h.

`ABSORBED_DOSE_RATE_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
It accepts symbols such as ``"Gy/s"``, ``"uGy/h"``, and ``"cGy/min"``.

References
----------
NIST, Guide for the Use of the International System of Units, Appendix B.8, factors
for units listed alphabetically:
https://www.nist.gov/node/777676

BIPM, The International System of Units (SI Brochure):
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.AbsorbedDose
    The dose a rate delivers over a time.
~kuchka.quantities.SpecificPower
    The quantity with the same dimension, energy per mass per time.
~kuchka.quantities.EquivalentDoseRate
    The rate of the biologically weighted dose.
~kuchka.quantities.Time
    A dose over a dose rate is the time the dose takes.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_POWER
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import AbsorbedDoseRate
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

GRAY_PER_SECOND = UnitDef(
    "gray_per_second",
    "Gy/s",
    Fraction(1, 1),
    SPECIFIC_POWER,
    words=("grays per second",),
)
MILLIGRAY_PER_SECOND = UnitDef(
    "milligray_per_second",
    "mGy/s",
    Fraction(1, 1000),
    SPECIFIC_POWER,
    words=("milligrays per second",),
)
GRAY_PER_MINUTE = UnitDef(
    "gray_per_minute",
    "Gy/min",
    Fraction(1, 60),
    SPECIFIC_POWER,
    words=("grays per minute",),
)
CENTIGRAY_PER_MINUTE = UnitDef(
    "centigray_per_minute",
    "cGy/min",
    Fraction(1, 6000),
    SPECIFIC_POWER,
    words=("centigrays per minute",),
)
GRAY_PER_HOUR = UnitDef(
    "gray_per_hour",
    "Gy/h",
    Fraction(1, 3600),
    SPECIFIC_POWER,
    aliases=("Gy/hr",),
    words=("grays per hour",),
)
MILLIGRAY_PER_HOUR = UnitDef(
    "milligray_per_hour",
    "mGy/h",
    Fraction(1, 3600000),
    SPECIFIC_POWER,
    aliases=("mGy/hr",),
    words=("milligrays per hour",),
)
MICROGRAY_PER_HOUR = UnitDef(
    "microgray_per_hour",
    "µGy/h",
    Fraction(1, 3600000000),
    SPECIFIC_POWER,
    aliases=("µGy/hr", "uGy/h", "uGy/hr"),
    words=("micrograys per hour",),
)
NANOGRAY_PER_HOUR = UnitDef(
    "nanogray_per_hour",
    "nGy/h",
    Fraction(1, 3600000000000),
    SPECIFIC_POWER,
    aliases=("nGy/hr",),
    words=("nanograys per hour",),
)
RAD_PER_HOUR = UnitDef(
    "rad_per_hour",
    "rad/h",
    Fraction(1, 360000),
    SPECIFIC_POWER,
    aliases=("rad/hr",),
    words=("rads per hour",),
)
MILLIRAD_PER_HOUR = UnitDef(
    "millirad_per_hour",
    "mrad/h",
    Fraction(1, 360000000),
    SPECIFIC_POWER,
    aliases=("mrad/hr",),
    words=("millirads per hour",),
)

AbsorbedDoseRate._canonical_unit = GRAY_PER_SECOND  # noqa: SLF001 -- this module owns AbsorbedDoseRate's canonical unit
AbsorbedDoseRate._result_unit = GRAY_PER_HOUR  # noqa: SLF001 -- and the unit its arithmetic results display in


def GrayPerSecond(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in grays per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in grays per second.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in grays per second.

    Examples
    --------
    Flash radiotherapy delivers its dose at more than 40 Gy/s, thousands of times faster
    than a conventional beam:

    >>> flash = GrayPerSecond(40)
    >>> flash
    40 Gy/s

    The gray per second is the watt per kilogram, so the rate reads as a power per mass
    once the quantity is chosen explicitly:

    >>> flash.to_specific_power()
    40 W/kg

    """
    return AbsorbedDoseRate(to_exact(value) * GRAY_PER_SECOND.scale, GRAY_PER_SECOND)


def MilligrayPerSecond(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in milligrays per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in milligrays per second.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in milligrays per second.

    Examples
    --------
    A cell irradiator is set to 30 mGy/s:

    >>> irradiator = MilligrayPerSecond(30)
    >>> irradiator
    30 mGy/s

    A radiobiologist plans in grays per minute, and the same setting is 1.8 Gy/min:

    >>> from kuchka.units import GRAY_PER_MINUTE
    >>> irradiator.to(GRAY_PER_MINUTE)
    1.8 Gy/min

    """
    return AbsorbedDoseRate(
        to_exact(value) * MILLIGRAY_PER_SECOND.scale, MILLIGRAY_PER_SECOND
    )


def GrayPerMinute(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in grays per minute.

    Parameters
    ----------
    value : Numeric
        Magnitude in grays per minute.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in grays per minute.

    Examples
    --------
    A linear accelerator delivers 4 Gy/min at the reference depth:

    >>> beam = GrayPerMinute(4)
    >>> beam
    4 Gy/min

    A fraction of 2 Gy takes half a minute of beam, as the dose over the rate:

    >>> from kuchka import Gray
    >>> from kuchka.units import SECOND
    >>> (Gray(2) / beam).to(SECOND)
    30 s

    """
    return AbsorbedDoseRate(to_exact(value) * GRAY_PER_MINUTE.scale, GRAY_PER_MINUTE)


def CentigrayPerMinute(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in centigrays per minute.

    Parameters
    ----------
    value : Numeric
        Magnitude in centigrays per minute.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in centigrays per minute.

    Examples
    --------
    A cobalt-60 teletherapy unit is specified at about 100 cGy/min at its calibration
    point:

    >>> source = CentigrayPerMinute(100)
    >>> source
    100 cGy/min

    Treatment plans in centigray need 2 minutes of beam for 200 cGy:

    >>> from kuchka import Minute
    >>> from kuchka.units import CENTIGRAY
    >>> (source * Minute(2)).to(CENTIGRAY)
    200 cGy

    """
    return AbsorbedDoseRate(
        to_exact(value) * CENTIGRAY_PER_MINUTE.scale, CENTIGRAY_PER_MINUTE
    )


def GrayPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in grays per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in grays per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in grays per hour.

    Examples
    --------
    The dose rate inside a gamma irradiator is 10 000 Gy/h:

    >>> chamber = GrayPerHour(10_000)
    >>> chamber
    10000 Gy/h

    A product that must receive 25 kGy stays inside for two and a half hours:

    >>> from kuchka import Kilogray
    >>> from kuchka.units import HOUR
    >>> (Kilogray(25) / chamber).to(HOUR)
    2.5 h

    """
    return AbsorbedDoseRate(to_exact(value) * GRAY_PER_HOUR.scale, GRAY_PER_HOUR)


def MilligrayPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in milligrays per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in milligrays per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in milligrays per hour.

    Examples
    --------
    A survey meter beside the shielding of an irradiator reads 0.4 mGy/h:

    >>> reading = MilligrayPerHour(0.4)
    >>> reading
    0.4 mGy/h

    An operator who stands there for a four-hour shift receives:

    >>> from kuchka import Hour
    >>> from kuchka.units import MILLIGRAY
    >>> (reading * Hour(4)).to(MILLIGRAY)
    1.6 mGy

    """
    return AbsorbedDoseRate(
        to_exact(value) * MILLIGRAY_PER_HOUR.scale, MILLIGRAY_PER_HOUR
    )


def MicrograyPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in micrograys per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in micrograys per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in micrograys per hour.

    Examples
    --------
    The external natural background in many places is about 0.09 µGy/h:

    >>> background = MicrograyPerHour(0.09)
    >>> background
    0.09 µGy/h

    Over a year of 8766 hours, that is under one milligray:

    >>> from kuchka import Hour
    >>> from kuchka.units import MILLIGRAY
    >>> f"{(background * Hour(8766)).to(MILLIGRAY):.2f}"
    '0.79 mGy'

    """
    return AbsorbedDoseRate(
        to_exact(value) * MICROGRAY_PER_HOUR.scale, MICROGRAY_PER_HOUR
    )


def NanograyPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in nanograys per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in nanograys per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in nanograys per hour.

    Examples
    --------
    A gamma monitoring station reports an environmental dose rate of 90 nGy/h, which a
    public display shows in micrograys per hour:

    >>> station = NanograyPerHour(90)
    >>> from kuchka.units import MICROGRAY_PER_HOUR
    >>> station.to(MICROGRAY_PER_HOUR)
    0.09 µGy/h

    The reading arrives from an instrument as text:

    >>> from kuchka import AbsorbedDoseRate
    >>> from kuchka import parse
    >>> parse("90 nGy/h", AbsorbedDoseRate) == station
    True

    """
    return AbsorbedDoseRate(
        to_exact(value) * NANOGRAY_PER_HOUR.scale, NANOGRAY_PER_HOUR
    )


def RadPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in rads per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in rads per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in rads per hour.

    Examples
    --------
    A survey meter calibrated before the SI reads 5 rad/h:

    >>> legacy = RadPerHour(5)
    >>> legacy
    5 rad/h

    A rad is exactly a hundredth of a gray, so 100 rad/h is exactly 1 Gy/h:

    >>> from kuchka import GrayPerHour
    >>> RadPerHour(100) == GrayPerHour(1)
    True

    """
    return AbsorbedDoseRate(to_exact(value) * RAD_PER_HOUR.scale, RAD_PER_HOUR)


def MilliradPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in millirads per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in millirads per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in millirads per hour.

    Examples
    --------
    Natural background was often quoted as about 0.01 mrad/h:

    >>> background = MilliradPerHour(0.01)
    >>> background
    0.01 mrad/h

    In today's units, that is 0.1 µGy/h:

    >>> from kuchka.units import MICROGRAY_PER_HOUR
    >>> background.to(MICROGRAY_PER_HOUR)
    0.1 µGy/h

    """
    return AbsorbedDoseRate(
        to_exact(value) * MILLIRAD_PER_HOUR.scale, MILLIRAD_PER_HOUR
    )


ABSORBED_DOSE_RATE_UNITS: Mapping[str, Callable[[Numeric], AbsorbedDoseRate]] = (
    unit_table(
        "ABSORBED_DOSE_RATE_UNITS",
        {
            GRAY_PER_SECOND: GrayPerSecond,
            MILLIGRAY_PER_SECOND: MilligrayPerSecond,
            GRAY_PER_MINUTE: GrayPerMinute,
            CENTIGRAY_PER_MINUTE: CentigrayPerMinute,
            GRAY_PER_HOUR: GrayPerHour,
            MILLIGRAY_PER_HOUR: MilligrayPerHour,
            MICROGRAY_PER_HOUR: MicrograyPerHour,
            NANOGRAY_PER_HOUR: NanograyPerHour,
            RAD_PER_HOUR: RadPerHour,
            MILLIRAD_PER_HOUR: MilliradPerHour,
        },
    )
)

__all__ = [
    "ABSORBED_DOSE_RATE_UNITS",
    "CENTIGRAY_PER_MINUTE",
    "GRAY_PER_HOUR",
    "GRAY_PER_MINUTE",
    "GRAY_PER_SECOND",
    "MICROGRAY_PER_HOUR",
    "MILLIGRAY_PER_HOUR",
    "MILLIGRAY_PER_SECOND",
    "MILLIRAD_PER_HOUR",
    "NANOGRAY_PER_HOUR",
    "RAD_PER_HOUR",
    "CentigrayPerMinute",
    "GrayPerHour",
    "GrayPerMinute",
    "GrayPerSecond",
    "MicrograyPerHour",
    "MilligrayPerHour",
    "MilligrayPerSecond",
    "MilliradPerHour",
    "NanograyPerHour",
    "RadPerHour",
]
