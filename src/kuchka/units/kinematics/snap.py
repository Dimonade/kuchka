"""Snap unit constructors: MetrePerSecondFourthPower and MillimetrePerSecondFourthPower.

`Snap` is the rate at which a jerk changes, also called jounce: the fourth derivative
of a position, which the smoothest motion profiles limit.
The metre per second to the fourth power is the canonical unit.

Examples
--------
A jerk rising by 10 m/s³ in half a second has a snap of 20 m/s⁴:

>>> from kuchka import MetrePerSecondCubed, Second
>>> MetrePerSecondCubed(10) / Second(0.5)
20 m/s⁴

A snap of 20 m/s⁴ acting for half a second adds 10 m/s³ of jerk:

>>> MetrePerSecondFourthPower(20) * Second(0.5)
10 m/s³

A snap of 3 m/s⁴ takes 2 s to build up a jerk of 6 m/s³:

>>> MetrePerSecondCubed(6) / MetrePerSecondFourthPower(3)
2 s

Datasheets of linear stages often give the limit in millimetres:

>>> MillimetrePerSecondFourthPower(5000) == MetrePerSecondFourthPower(5)
True

`SNAP_UNITS` maps symbols such as ``"m/s⁴"`` and ``"mm/s⁴"`` to their constructors,
for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.Jerk
    The jerk a snap changes.
~kuchka.quantities.TimeFourthPower
    A snap times a time to the fourth power is a length.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import SNAP
from kuchka.internal import symbols
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Snap
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_FOUR = symbols.SUPERSCRIPT_FOUR

METRE_PER_SECOND_FOURTH_POWER = UnitDef(
    "metre_per_second_fourth_power",
    f"m/s{_FOUR}",
    Decimal(1),
    SNAP,
    aliases=powered("m/s", 4),
    words=(
        "meter per second to the fourth power",
        "meters per second to the fourth power",
        "metre per second to the fourth power",
        "metres per second to the fourth power",
    ),
)
MILLIMETRE_PER_SECOND_FOURTH_POWER = UnitDef(
    "millimetre_per_second_fourth_power",
    f"mm/s{_FOUR}",
    Decimal("0.001"),
    SNAP,
    aliases=powered("mm/s", 4),
    words=(
        "millimeter per second to the fourth power",
        "millimeters per second to the fourth power",
        "millimetre per second to the fourth power",
        "millimetres per second to the fourth power",
    ),
)

METER_PER_SECOND_FOURTH_POWER = METRE_PER_SECOND_FOURTH_POWER
MILLIMETER_PER_SECOND_FOURTH_POWER = MILLIMETRE_PER_SECOND_FOURTH_POWER

Snap._canonical_unit = METRE_PER_SECOND_FOURTH_POWER  # noqa: SLF001 -- this module owns Snap's canonical unit


def MetrePerSecondFourthPower(value: Numeric) -> Snap:
    """Construct a snap from a magnitude in metres per second to the fourth power.

    Parameters
    ----------
    value : Numeric
        Snap magnitude in metres per second to the fourth power.

    Returns
    -------
    Snap
        Snap represented in metres per second to the fourth power.

    Examples
    --------
    A snap of 4 m/s⁴ adds 8 m/s³ of jerk in two seconds:

    >>> from kuchka import Second
    >>> MetrePerSecondFourthPower(4) * Second(2)
    8 m/s³

    """
    return Snap(
        to_exact(value) * METRE_PER_SECOND_FOURTH_POWER.scale,
        METRE_PER_SECOND_FOURTH_POWER,
    )


MeterPerSecondFourthPower = MetrePerSecondFourthPower
"""American spelling, aliasing `MetrePerSecondFourthPower`: the same function object."""


def MillimetrePerSecondFourthPower(value: Numeric) -> Snap:
    """Construct a snap from a magnitude in millimetres per second to the fourth power.

    Parameters
    ----------
    value : Numeric
        Snap magnitude in millimetres per second to the fourth power.

    Returns
    -------
    Snap
        Snap represented in millimetres per second to the fourth power.

    Examples
    --------
    A millimetre per second to the fourth power is a thousandth of a metre per second
    to the fourth power:

    >>> MillimetrePerSecondFourthPower(1) == MetrePerSecondFourthPower(Decimal("0.001"))
    True

    """
    return Snap(
        to_exact(value) * MILLIMETRE_PER_SECOND_FOURTH_POWER.scale,
        MILLIMETRE_PER_SECOND_FOURTH_POWER,
    )


MillimeterPerSecondFourthPower = MillimetrePerSecondFourthPower
"""American spelling, aliasing `MillimetrePerSecondFourthPower`: the same object."""


SNAP_UNITS: Mapping[str, Callable[[Numeric], Snap]] = unit_table(
    "SNAP_UNITS",
    {
        METRE_PER_SECOND_FOURTH_POWER: MetrePerSecondFourthPower,
        MILLIMETRE_PER_SECOND_FOURTH_POWER: MillimetrePerSecondFourthPower,
    },
)

__all__ = [
    "METER_PER_SECOND_FOURTH_POWER",
    "METRE_PER_SECOND_FOURTH_POWER",
    "MILLIMETER_PER_SECOND_FOURTH_POWER",
    "MILLIMETRE_PER_SECOND_FOURTH_POWER",
    "SNAP_UNITS",
    "MeterPerSecondFourthPower",
    "MetrePerSecondFourthPower",
    "MillimeterPerSecondFourthPower",
    "MillimetrePerSecondFourthPower",
]
