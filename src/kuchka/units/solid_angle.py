"""Solid angle constructors: the steradian and the square angle units.

`SolidAngle` is the part of space seen from a point, measured as the area it cuts from
a sphere over the square of the sphere's radius.
The steradian (`sr`) is the canonical unit, the solid angle that cuts one square metre
from a sphere of one metre radius, and the module adds the microsteradian and the
millisteradian, and the square degree, square arcminute, and square arcsecond of
astronomy:

>>> from kuchka import SquareDegree
>>> from kuchka import Steradian
>>> detector = Steradian(0.02)
>>> survey = SquareDegree(25)

A lumen is a candela steradian, so no factor and no pi lies between the steradian and
the photometric units.
The square degree, the square arcminute, and the square arcsecond are the angular
units squared, which ties each to the steradian by pi squared: a square degree is
`(pi / 180)²` steradians.
kuchka converts them with pi held as an exact rational to 100 decimal places, the same
pi `Radian` uses.

Sensors and the Sun are small, microsteradians and millisteradians, a telescope field or
a survey covers square degrees, and the whole sky is 4 pi steradians.

Examples
--------
A lamp of 100 cd that sends its light into a cone of 2 sr emits 200 lm in it:

>>> from kuchka import Candela
>>> Candela(100) * Steradian(2)
200 lm

A patch of 1 m² on a sphere of radius 2 m lies at a quarter of a steradian, the area
over the square of the radius:

>>> from kuchka import Metre
>>> from kuchka import SolidAngle
>>> from kuchka import SquareMetre
>>> SolidAngle.from_area(SquareMetre(1), Metre(2))
0.25 sr

The whole sky is 4 pi steradians, about 41 253 square degrees:

>>> import math
>>> from kuchka.units import SQUARE_DEGREE
>>> f"{Steradian(4 * math.pi).to(SQUARE_DEGREE):.0f}"
'41253 °²'

A solid angle is not a plane angle, so the two refuse to add:

>>> from kuchka import Radian
>>> Steradian(1) + Radian(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
TypeError: ...

Notes
-----
`SolidAngle.from_area(area, radius)` gives the solid angle of a patch of a sphere.

`SOLID_ANGLE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.

References
----------
BIPM, The International System of Units (SI Brochure), on the steradian:
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.LuminousIntensity
    An intensity times a solid angle is a flux.
~kuchka.quantities.LuminousFlux
    The light a source emits into a solid angle.
~kuchka.quantities.AngularDisplacement
    The plane angle, measured in radians.

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
        Solid angle magnitude in microsteradians.

    Returns
    -------
    SolidAngle
        Solid angle represented in microsteradians.

    Examples
    --------
    The Sun, seen from the Earth, subtends about 68 µsr:

    >>> sun = Microsteradian(68)
    >>> sun
    68 µsr

    In the square degrees of astronomy, that is about a fifth of one:

    >>> from kuchka.units import SQUARE_DEGREE
    >>> f"{sun.to(SQUARE_DEGREE):.4f}"
    '0.2232 °²'

    """
    return SolidAngle(to_exact(value) * MICROSTERADIAN.scale, MICROSTERADIAN)


def Millisteradian(value: Numeric) -> SolidAngle:
    """Construct a solid angle from a magnitude expressed in millisteradians.

    Parameters
    ----------
    value : Numeric
        Solid angle magnitude in millisteradians.

    Returns
    -------
    SolidAngle
        Solid angle represented in millisteradians.

    Examples
    --------
    A photodiode sees the lamp across a solid angle of 10 msr:

    >>> view = Millisteradian(10)
    >>> view
    10 msr

    A 1 cm² photodiode that sits 10 cm from the lamp subtends that solid angle:

    >>> from kuchka import Centimetre
    >>> from kuchka import SolidAngle
    >>> from kuchka import SquareCentimetre
    >>> diode = SolidAngle.from_area(SquareCentimetre(1), Centimetre(10))
    >>> diode == view
    True

    """
    return SolidAngle(to_exact(value) * MILLISTERADIAN.scale, MILLISTERADIAN)


def Steradian(value: Numeric) -> SolidAngle:
    """Construct a solid angle from a magnitude expressed in steradians.

    Parameters
    ----------
    value : Numeric
        Solid angle magnitude in steradians.

    Returns
    -------
    SolidAngle
        Solid angle represented in steradians.

    Examples
    --------
    A spotlight concentrates its beam into a cone of 0.5 sr:

    >>> beam = Steradian(0.5)
    >>> beam
    0.5 sr

    A square metre of a sphere of radius 2 m lies at one quarter of a steradian:

    >>> from kuchka import Metre
    >>> from kuchka import SolidAngle
    >>> from kuchka import SquareMetre
    >>> SolidAngle.from_area(SquareMetre(1), Metre(2))
    0.25 sr

    Solid angles of the same cone, in different units, add:

    >>> from kuchka import Millisteradian
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
    >>> field
    25 °²

    The same field in the square arcminutes of a detector's pixels:

    >>> from kuchka.units import SQUARE_ARCMINUTE
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
    The Moon's disc, about 31 arcminutes across, covers about 755 arcmin²:

    >>> moon = SquareArcMinute(755)
    >>> moon
    755 arcmin²

    In square degrees, that is about a fifth:

    >>> from kuchka.units import SQUARE_DEGREE
    >>> f"{moon.to(SQUARE_DEGREE):.3f}"
    '0.210 °²'

    The Hubble Ultra Deep Field spans about 11 arcmin², which is 39 600 arcsec²:

    >>> from kuchka.units import SQUARE_ARCSECOND
    >>> SquareArcMinute(11).to(SQUARE_ARCSECOND)
    39600 arcsec²

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
    A telescope camera with pixels of 0.2″ by 0.2″ covers 0.04 arcsec² in each pixel:

    >>> from decimal import Decimal
    >>> pixel = SquareArcSecond(Decimal("0.04"))
    >>> pixel
    0.04 arcsec²

    A detector of 4096 by 4096 such pixels covers about 186 arcmin²:

    >>> from kuchka.units import SQUARE_ARCMINUTE
    >>> f"{(pixel * 4096 * 4096).to(SQUARE_ARCMINUTE):.1f}"
    '186.4 arcmin²'

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
