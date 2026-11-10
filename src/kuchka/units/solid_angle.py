"""Solid angle constructors: the steradian and the square angle units.

    from kuchka import Steradian, SquareDegree

    detector = Steradian(0.02)
    survey = SquareDegree(25)

The steradian is the canonical unit: the solid angle that cuts one square metre from a
sphere of one metre radius.
A lumen is a candela steradian, so no factor and no pi lies between the steradian and
the photometric units.

The square degree, the square arcminute, and the square arcsecond are the angular
units squared, which ties each to the steradian by pi squared: a square degree is
`(pi / 180)²` steradians.
kuchka converts them with pi held as an exact rational to 100 decimal places
(`kuchka.internal.constants.PI`), the same pi `Radian` uses.

`SOLID_ANGLE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SOLID_ANGLE
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import SolidAngle
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

STERADIAN_NAME = "steradian"
STERADIAN_SYMBOL = "sr"

MICROSTERADIAN = prefixed_unit(
    prefixes.MICRO, STERADIAN_NAME, STERADIAN_SYMBOL, SOLID_ANGLE
)
MILLISTERADIAN = prefixed_unit(
    prefixes.MILLI, STERADIAN_NAME, STERADIAN_SYMBOL, SOLID_ANGLE
)
STERADIAN = prefixed_unit(prefixes.UNIT, STERADIAN_NAME, STERADIAN_SYMBOL, SOLID_ANGLE)

_SQUARE_DEGREE_SCALE = PI * PI / Fraction(180 * 180)

SQUARE_DEGREE = UnitDef(
    "square_degree",
    f"{symbols.DEGREE}{symbols.SUPERSCRIPT_TWO}",
    _SQUARE_DEGREE_SCALE,
    SOLID_ANGLE,
    aliases=(*powered("deg", 2), f"deg{symbols.SUPERSCRIPT_TWO}"),
    words=("sq deg", "square deg"),
)
SQUARE_ARCMINUTE = UnitDef(
    "square_arcminute",
    f"arcmin{symbols.SUPERSCRIPT_TWO}",
    _SQUARE_DEGREE_SCALE / 3600,
    SOLID_ANGLE,
    aliases=(*powered("arcmin", 2), f"{symbols.PRIME}{symbols.SUPERSCRIPT_TWO}"),
    words=("sq arcmin", "square arc minute"),
)
SQUARE_ARCSECOND = UnitDef(
    "square_arcsecond",
    f"arcsec{symbols.SUPERSCRIPT_TWO}",
    _SQUARE_DEGREE_SCALE / 12_960_000,
    SOLID_ANGLE,
    aliases=(
        *powered("arcsec", 2),
        f"{symbols.DOUBLE_PRIME}{symbols.SUPERSCRIPT_TWO}",
    ),
    words=("sq arcsec", "square arc second"),
)

SolidAngle._canonical_unit = STERADIAN  # noqa: SLF001 -- this module owns SolidAngle's canonical unit


def Microsteradian(value: Numeric) -> SolidAngle:
    """Construct a solid angle from a magnitude expressed in microsteradians.

    Parameters
    ----------
    value : Numeric
        Solid angle magnitude in µsr.

    Returns
    -------
    SolidAngle
        Solid angle represented in microsteradians.

    Examples
    --------
    >>> Microsteradian(500).to(MILLISTERADIAN)
    0.5 msr

    """
    return SolidAngle(to_exact(value) * MICROSTERADIAN.scale, MICROSTERADIAN)


def Millisteradian(value: Numeric) -> SolidAngle:
    """Construct a solid angle from a magnitude expressed in millisteradians.

    Parameters
    ----------
    value : Numeric
        Solid angle magnitude in msr.

    Returns
    -------
    SolidAngle
        Solid angle represented in millisteradians.

    Examples
    --------
    A 1 cm² photodiode 10 cm from a lamp subtends 10 msr:

    >>> from kuchka import Centimetre, SolidAngle, SquareCentimetre
    >>> diode = SolidAngle.from_area(SquareCentimetre(1), Centimetre(10))
    >>> diode == Millisteradian(10)
    True

    """
    return SolidAngle(to_exact(value) * MILLISTERADIAN.scale, MILLISTERADIAN)


def Steradian(value: Numeric) -> SolidAngle:
    """Construct a solid angle from a magnitude expressed in steradians.

    Parameters
    ----------
    value : Numeric
        Solid angle magnitude in sr.

    Returns
    -------
    SolidAngle
        Solid angle represented in steradians.

    Examples
    --------
    A square metre of a sphere of radius 2 m lies at one quarter of a steradian:

    >>> from kuchka import Metre, SolidAngle, SquareMetre
    >>> SolidAngle.from_area(SquareMetre(1), Metre(2))
    0.25 sr
    >>> Steradian(2) + Millisteradian(500)
    2.5 sr

    """
    return SolidAngle(to_exact(value) * STERADIAN.scale, STERADIAN)


def SquareDegree(value: Numeric) -> SolidAngle:
    """Construct a solid angle from a magnitude expressed in square degrees.

    Parameters
    ----------
    value : Numeric
        Solid angle magnitude in square degrees.

    Returns
    -------
    SolidAngle
        Solid angle represented in square degrees.

    Examples
    --------
    A sky survey covers a 5° by 5° field:

    >>> field = SquareDegree(25)
    >>> field.to(SQUARE_ARCMINUTE)
    90000 arcmin²

    """
    return SolidAngle(to_exact(value) * SQUARE_DEGREE.scale, SQUARE_DEGREE)


def SquareArcMinute(value: Numeric) -> SolidAngle:
    """Construct a solid angle from a magnitude expressed in square arcminutes.

    Parameters
    ----------
    value : Numeric
        Solid angle magnitude in square arcminutes.

    Returns
    -------
    SolidAngle
        Solid angle represented in square arcminutes.

    Examples
    --------
    >>> SquareArcMinute(3600).to(SQUARE_DEGREE)
    1 °²

    """
    return SolidAngle(to_exact(value) * SQUARE_ARCMINUTE.scale, SQUARE_ARCMINUTE)


def SquareArcSecond(value: Numeric) -> SolidAngle:
    """Construct a solid angle from a magnitude expressed in square arcseconds.

    Parameters
    ----------
    value : Numeric
        Solid angle magnitude in square arcseconds.

    Returns
    -------
    SolidAngle
        Solid angle represented in square arcseconds.

    Examples
    --------
    >>> SquareArcSecond(3600).to(SQUARE_ARCMINUTE)
    1 arcmin²

    """
    return SolidAngle(to_exact(value) * SQUARE_ARCSECOND.scale, SQUARE_ARCSECOND)


SOLID_ANGLE_UNITS: Mapping[str, Callable[[Numeric], SolidAngle]] = unit_table(
    "SOLID_ANGLE_UNITS",
    {
        MICROSTERADIAN: Microsteradian,
        MILLISTERADIAN: Millisteradian,
        STERADIAN: Steradian,
        SQUARE_DEGREE: SquareDegree,
        SQUARE_ARCMINUTE: SquareArcMinute,
        SQUARE_ARCSECOND: SquareArcSecond,
    },
)

__all__ = [
    "MICROSTERADIAN",
    "MILLISTERADIAN",
    "SOLID_ANGLE_UNITS",
    "SQUARE_ARCMINUTE",
    "SQUARE_ARCSECOND",
    "SQUARE_DEGREE",
    "STERADIAN",
    "Microsteradian",
    "Millisteradian",
    "SquareArcMinute",
    "SquareArcSecond",
    "SquareDegree",
    "Steradian",
]
