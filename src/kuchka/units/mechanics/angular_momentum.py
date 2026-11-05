"""Angular momentum unit constructors, such as KilogramSquareMetrePerSecond.

Angular momentum is a moment of inertia times its angular velocity, and a torque applied
for a time changes it by their product.
A kilogram square metre per second is a joule second per radian, so its scale is
`2 pi` joule seconds per turn, with pi held as an exact rational.
The joule second per turn is the canonical unit, because a turn is the canonical angle,
and arithmetic results display in the kilogram square metre per second.

Examples
--------
A 0.04 kg·m² disc spinning at 300 rad/s carries 12 kg·m²/s, and a 2 N·m brake takes it
to rest in six seconds:

>>> from kuchka import KilogramSquareMetre, NewtonMetre, RadianPerSecond
>>> spin = KilogramSquareMetre(0.04) * RadianPerSecond(300)
>>> spin
12 kg·m²/s
>>> spin / NewtonMetre(2)
6 s

`ANGULAR_MOMENTUM_UNITS` maps symbols such as ``"kg·m²/s"`` and ``"N·m·s"`` to their
constructors, for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.MomentOfInertia
    An angular momentum per angular velocity.
~kuchka.quantities.Torque
    The rate of change of angular momentum.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ANGULAR_MOMENTUM
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import AngularMomentum
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_PER_RADIAN = 2 * PI

JOULE_SECOND_PER_TURN = UnitDef(
    "joule_second_per_turn",
    f"J{symbols.MIDDLE_DOT}s/tr",
    1,
    ANGULAR_MOMENTUM,
    aliases=("J*s/tr", "J s/tr"),
    words=("joule second per turn",),
)
KILOGRAM_SQUARE_METRE_PER_SECOND = UnitDef(
    "kilogram_square_metre_per_second",
    f"kg{symbols.MIDDLE_DOT}m{symbols.SUPERSCRIPT_TWO}/s",
    _PER_RADIAN,
    ANGULAR_MOMENTUM,
    aliases=(
        *(f"{base}/s" for base in powered("kg*m", 2)),
        *(f"{base}/s" for base in powered("kg m", 2)),
        "kg*m2/s",
        "kg m2/s",
    ),
    words=("kilogram square metre per second", "kilogram square meter per second"),
)
NEWTON_METRE_SECOND = UnitDef(
    "newton_metre_second",
    f"N{symbols.MIDDLE_DOT}m{symbols.MIDDLE_DOT}s",
    _PER_RADIAN,
    ANGULAR_MOMENTUM,
    aliases=("N*m*s", "N m s", "Nms"),
    words=("newton metre second", "newton meter second"),
)

KILOGRAM_SQUARE_METER_PER_SECOND = KILOGRAM_SQUARE_METRE_PER_SECOND
NEWTON_METER_SECOND = NEWTON_METRE_SECOND

AngularMomentum._canonical_unit = JOULE_SECOND_PER_TURN  # noqa: SLF001 -- this module owns AngularMomentum's canonical unit
AngularMomentum._result_unit = KILOGRAM_SQUARE_METRE_PER_SECOND  # noqa: SLF001 -- and the unit its arithmetic results display in


def JouleSecondPerTurn(value: Numeric) -> AngularMomentum:
    """Construct an angular momentum from joule seconds per turn.

    Parameters
    ----------
    value : Numeric
        Angular momentum in J·s/tr.

    Returns
    -------
    AngularMomentum
        Angular momentum represented in the canonical unit.

    Examples
    --------
    The canonical unit is what `magnitude` reads in:

    >>> JouleSecondPerTurn(3).magnitude
    Fraction(3, 1)

    """
    return AngularMomentum(
        to_exact(value) * JOULE_SECOND_PER_TURN.scale, JOULE_SECOND_PER_TURN
    )


def KilogramSquareMetrePerSecond(value: Numeric) -> AngularMomentum:
    """Construct an angular momentum from kilogram square metres per second.

    Parameters
    ----------
    value : Numeric
        Angular momentum in kg·m²/s.

    Returns
    -------
    AngularMomentum
        Angular momentum represented in kilogram square metres per second.

    Examples
    --------
    Divided by its moment of inertia, an angular momentum is the angular velocity:

    >>> from kuchka import KilogramSquareMetre
    >>> KilogramSquareMetrePerSecond(12) / KilogramSquareMetre(0.04)
    300 rad/s

    """
    return AngularMomentum(
        to_exact(value) * KILOGRAM_SQUARE_METRE_PER_SECOND.scale,
        KILOGRAM_SQUARE_METRE_PER_SECOND,
    )


def NewtonMetreSecond(value: Numeric) -> AngularMomentum:
    """Construct an angular momentum from newton-metre seconds.

    Parameters
    ----------
    value : Numeric
        Angular momentum in N·m·s, the angular impulse of a torque over a time.

    Returns
    -------
    AngularMomentum
        Angular momentum represented in newton-metre seconds.

    Examples
    --------
    A 2 N·m torque applied for 6 s:

    >>> from kuchka import NewtonMetre, Second
    >>> NewtonMetre(2) * Second(6) == NewtonMetreSecond(12)
    True

    """
    return AngularMomentum(
        to_exact(value) * NEWTON_METRE_SECOND.scale, NEWTON_METRE_SECOND
    )


KilogramSquareMeterPerSecond = KilogramSquareMetrePerSecond
NewtonMeterSecond = NewtonMetreSecond


ANGULAR_MOMENTUM_UNITS: Mapping[str, Callable[[Numeric], AngularMomentum]] = unit_table(
    "ANGULAR_MOMENTUM_UNITS",
    {
        JOULE_SECOND_PER_TURN: JouleSecondPerTurn,
        KILOGRAM_SQUARE_METRE_PER_SECOND: KilogramSquareMetrePerSecond,
        NEWTON_METRE_SECOND: NewtonMetreSecond,
    },
)

__all__ = [
    "ANGULAR_MOMENTUM_UNITS",
    "JOULE_SECOND_PER_TURN",
    "KILOGRAM_SQUARE_METER_PER_SECOND",
    "KILOGRAM_SQUARE_METRE_PER_SECOND",
    "NEWTON_METER_SECOND",
    "NEWTON_METRE_SECOND",
    "JouleSecondPerTurn",
    "KilogramSquareMeterPerSecond",
    "KilogramSquareMetrePerSecond",
    "NewtonMeterSecond",
    "NewtonMetreSecond",
]
