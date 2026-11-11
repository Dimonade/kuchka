"""Moment of inertia constructors: kilogram square metres and their relatives.

A moment of inertia is how a body resists angular acceleration about an axis.
A kilogram square metre is a kilogram square metre per square radian, the way a
newton-metre of torque is a joule per radian, so its scale is `(2 pi) ** 2` kilogram
square metres per square turn, with pi held as an exact rational (see
`kuchka.units.angular`).
The kilogram square metre per square turn is the canonical unit, because a turn is the
canonical angle, and arithmetic results display in the kilogram square metre.
A datasheet value is typed as written, in kg·m², kg·cm², g·cm², lb·ft², or lb·in².

Examples
--------
A motor datasheet gives a rotor inertia of 30 kg·cm², and the drive accelerates it at
400 rad/s²:

>>> from kuchka import RadianPerSecondSquared
>>> rotor = KilogramSquareCentimetre(30)
>>> rotor * RadianPerSecondSquared(400)
1.2 N·m

A solid disc of 2 kg and 0.2 m radius has half the inertia of the same mass at its
rim:

>>> from kuchka import Kilogram
>>> from kuchka import Metre
>>> 0.5 * Kilogram(2) * Metre(0.2) * Metre(0.2)
0.04 kg·m²

`MOMENT_OF_INERTIA_UNITS` maps symbols such as ``"kg·m²"`` and ``"lb·in²"`` to their
constructors, for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.Torque
    A moment of inertia times an angular acceleration.
~kuchka.quantities.AngularMomentum
    A moment of inertia times an angular velocity.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MOMENT_OF_INERTIA
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import MomentOfInertia
from kuchka.quantities import UnitDef
from kuchka.units.length import FOOT
from kuchka.units.length import INCH
from kuchka.units.mass import POUND

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_PER_SQUARE_RADIAN = (2 * PI) ** 2

KILOGRAM_SQUARE_METRE_PER_SQUARE_TURN = UnitDef(
    "kilogram_square_metre_per_square_turn",
    f"kg{symbols.MIDDLE_DOT}m{symbols.SUPERSCRIPT_TWO}/tr{symbols.SUPERSCRIPT_TWO}",
    1,
    MOMENT_OF_INERTIA,
    words=("kilogram square metre per square turn",),
)
KILOGRAM_SQUARE_METRE = UnitDef(
    "kilogram_square_metre",
    f"kg{symbols.MIDDLE_DOT}m{symbols.SUPERSCRIPT_TWO}",
    _PER_SQUARE_RADIAN,
    MOMENT_OF_INERTIA,
    aliases=(*powered("kg*m", 2), *powered("kg m", 2), "kg*m2", "kg m2"),
    words=("kilogram square metre", "kilogram square meter"),
)
KILOGRAM_SQUARE_CENTIMETRE = UnitDef(
    "kilogram_square_centimetre",
    f"kg{symbols.MIDDLE_DOT}cm{symbols.SUPERSCRIPT_TWO}",
    _PER_SQUARE_RADIAN / 10_000,
    MOMENT_OF_INERTIA,
    aliases=(*powered("kg*cm", 2), *powered("kg cm", 2), "kg*cm2", "kg cm2"),
    words=("kilogram square centimetre", "kilogram square centimeter"),
)
GRAM_SQUARE_CENTIMETRE = UnitDef(
    "gram_square_centimetre",
    f"g{symbols.MIDDLE_DOT}cm{symbols.SUPERSCRIPT_TWO}",
    _PER_SQUARE_RADIAN / 10_000_000,
    MOMENT_OF_INERTIA,
    aliases=(*powered("g*cm", 2), *powered("g cm", 2), "g*cm2", "g cm2"),
    words=("gram square centimetre", "gram square centimeter"),
)
POUND_SQUARE_FOOT = UnitDef(
    "pound_square_foot",
    f"lb{symbols.MIDDLE_DOT}ft{symbols.SUPERSCRIPT_TWO}",
    _PER_SQUARE_RADIAN * POUND.scale * FOOT.scale**2,
    MOMENT_OF_INERTIA,
    aliases=(*powered("lb*ft", 2), *powered("lb ft", 2), "lb*ft2", "lb ft2"),
    words=("pound square foot",),
)
POUND_SQUARE_INCH = UnitDef(
    "pound_square_inch",
    f"lb{symbols.MIDDLE_DOT}in{symbols.SUPERSCRIPT_TWO}",
    _PER_SQUARE_RADIAN * POUND.scale * INCH.scale**2,
    MOMENT_OF_INERTIA,
    aliases=(*powered("lb*in", 2), *powered("lb in", 2), "lb*in2", "lb in2"),
    words=("pound square inch",),
)

KILOGRAM_SQUARE_METER_PER_SQUARE_TURN = KILOGRAM_SQUARE_METRE_PER_SQUARE_TURN
KILOGRAM_SQUARE_METER = KILOGRAM_SQUARE_METRE
KILOGRAM_SQUARE_CENTIMETER = KILOGRAM_SQUARE_CENTIMETRE
GRAM_SQUARE_CENTIMETER = GRAM_SQUARE_CENTIMETRE

MomentOfInertia._canonical_unit = KILOGRAM_SQUARE_METRE_PER_SQUARE_TURN  # noqa: SLF001 -- this module owns MomentOfInertia's canonical unit
MomentOfInertia._result_unit = KILOGRAM_SQUARE_METRE  # noqa: SLF001 -- and the unit its arithmetic results display in


def KilogramSquareMetrePerSquareTurn(value: Numeric) -> MomentOfInertia:
    """Construct a moment of inertia from kilogram square metres per square turn.

    Parameters
    ----------
    value : Numeric
        Moment of inertia in kg·m²/tr².

    Returns
    -------
    MomentOfInertia
        Moment of inertia represented in the canonical unit.

    Examples
    --------
    The canonical unit is what `magnitude` reads in:

    >>> KilogramSquareMetrePerSquareTurn(3).magnitude
    Fraction(3, 1)

    """
    return MomentOfInertia(
        to_exact(value) * KILOGRAM_SQUARE_METRE_PER_SQUARE_TURN.scale,
        KILOGRAM_SQUARE_METRE_PER_SQUARE_TURN,
    )


def KilogramSquareMetre(value: Numeric) -> MomentOfInertia:
    """Construct a moment of inertia from kilogram square metres.

    Parameters
    ----------
    value : Numeric
        Moment of inertia in kg·m².

    Returns
    -------
    MomentOfInertia
        Moment of inertia represented in kilogram square metres.

    Examples
    --------
    A flywheel of 0.5 kg·m² spinning at 100 rad/s stores 2.5 kJ:

    >>> from kuchka import RadianPerSecond
    >>> omega = RadianPerSecond(100)
    >>> 0.5 * KilogramSquareMetre(0.5) * omega * omega
    2500 J

    """
    return MomentOfInertia(
        to_exact(value) * KILOGRAM_SQUARE_METRE.scale, KILOGRAM_SQUARE_METRE
    )


def KilogramSquareCentimetre(value: Numeric) -> MomentOfInertia:
    """Construct a moment of inertia from kilogram square centimetres.

    Parameters
    ----------
    value : Numeric
        Moment of inertia in kg·cm², the unit of most servo motor datasheets.

    Returns
    -------
    MomentOfInertia
        Moment of inertia represented in kilogram square centimetres.

    Examples
    --------
    >>> KilogramSquareCentimetre(10_000) == KilogramSquareMetre(1)
    True

    """
    return MomentOfInertia(
        to_exact(value) * KILOGRAM_SQUARE_CENTIMETRE.scale, KILOGRAM_SQUARE_CENTIMETRE
    )


def GramSquareCentimetre(value: Numeric) -> MomentOfInertia:
    """Construct a moment of inertia from gram square centimetres.

    Parameters
    ----------
    value : Numeric
        Moment of inertia in g·cm², the unit of small motors and encoders.

    Returns
    -------
    MomentOfInertia
        Moment of inertia represented in gram square centimetres.

    Examples
    --------
    >>> GramSquareCentimetre(1000) == KilogramSquareCentimetre(1)
    True

    """
    return MomentOfInertia(
        to_exact(value) * GRAM_SQUARE_CENTIMETRE.scale, GRAM_SQUARE_CENTIMETRE
    )


def PoundSquareFoot(value: Numeric) -> MomentOfInertia:
    """Construct a moment of inertia from pound square feet.

    Parameters
    ----------
    value : Numeric
        Moment of inertia in lb·ft².

    Returns
    -------
    MomentOfInertia
        Moment of inertia represented in pound square feet.

    Examples
    --------
    >>> PoundSquareFoot(1) == PoundSquareInch(144)
    True

    """
    return MomentOfInertia(to_exact(value) * POUND_SQUARE_FOOT.scale, POUND_SQUARE_FOOT)


def PoundSquareInch(value: Numeric) -> MomentOfInertia:
    """Construct a moment of inertia from pound square inches.

    Parameters
    ----------
    value : Numeric
        Moment of inertia in lb·in².

    Returns
    -------
    MomentOfInertia
        Moment of inertia represented in pound square inches.

    Examples
    --------
    >>> f"{PoundSquareInch(10).to(KILOGRAM_SQUARE_CENTIMETRE):.3f}"
    '29.264 kg·cm²'

    """
    return MomentOfInertia(to_exact(value) * POUND_SQUARE_INCH.scale, POUND_SQUARE_INCH)


KilogramSquareMeterPerSquareTurn = KilogramSquareMetrePerSquareTurn
KilogramSquareMeter = KilogramSquareMetre
KilogramSquareCentimeter = KilogramSquareCentimetre
GramSquareCentimeter = GramSquareCentimetre


MOMENT_OF_INERTIA_UNITS: Mapping[str, Callable[[Numeric], MomentOfInertia]] = (
    unit_table(
        "MOMENT_OF_INERTIA_UNITS",
        {
            KILOGRAM_SQUARE_METRE_PER_SQUARE_TURN: KilogramSquareMetrePerSquareTurn,
            KILOGRAM_SQUARE_METRE: KilogramSquareMetre,
            KILOGRAM_SQUARE_CENTIMETRE: KilogramSquareCentimetre,
            GRAM_SQUARE_CENTIMETRE: GramSquareCentimetre,
            POUND_SQUARE_FOOT: PoundSquareFoot,
            POUND_SQUARE_INCH: PoundSquareInch,
        },
    )
)

__all__ = [
    "GRAM_SQUARE_CENTIMETER",
    "GRAM_SQUARE_CENTIMETRE",
    "KILOGRAM_SQUARE_CENTIMETER",
    "KILOGRAM_SQUARE_CENTIMETRE",
    "KILOGRAM_SQUARE_METER",
    "KILOGRAM_SQUARE_METER_PER_SQUARE_TURN",
    "KILOGRAM_SQUARE_METRE",
    "KILOGRAM_SQUARE_METRE_PER_SQUARE_TURN",
    "MOMENT_OF_INERTIA_UNITS",
    "POUND_SQUARE_FOOT",
    "POUND_SQUARE_INCH",
    "GramSquareCentimeter",
    "GramSquareCentimetre",
    "KilogramSquareCentimeter",
    "KilogramSquareCentimetre",
    "KilogramSquareMeter",
    "KilogramSquareMeterPerSquareTurn",
    "KilogramSquareMetre",
    "KilogramSquareMetrePerSquareTurn",
    "PoundSquareFoot",
    "PoundSquareInch",
]
