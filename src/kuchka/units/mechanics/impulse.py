"""Impulse unit constructors: newton seconds and dyne seconds.

    from kuchka import NewtonSecond, PoundForceSecond

    burn = NewtonSecond(60)
    thruster_log = PoundForceSecond(13.5)

An impulse is measured in newton seconds (1 N·s = 1 kg·m/s) or in dyne seconds
(1 dyn·s = 1 g·cm/s).
The pound-force second is exact, because the pound-force is: one is exactly
4.4482216152605 N·s.

`IMPULSE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import IMPULSE
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Impulse
from kuchka.quantities import UnitDef
from kuchka.units.mechanics.force import POUND_FORCE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_DOT = symbols.MIDDLE_DOT

NEWTON_SECOND = UnitDef(
    "newton_second",
    f"N{_DOT}s",
    Decimal(1),
    IMPULSE,
    aliases=(
        "N*s",
        "N s",
        "N\u22c5s",
        "N.s",
    ),
    words=("newton seconds", "newton-seconds"),
)
MILLINEWTON_SECOND = UnitDef(
    "millinewton_second",
    f"mN{_DOT}s",
    Decimal("0.001"),
    IMPULSE,
    aliases=(
        "mN*s",
        "mN s",
        "mN\u22c5s",
    ),
    words=("millinewton seconds",),
)
KILONEWTON_SECOND = UnitDef(
    "kilonewton_second",
    f"kN{_DOT}s",
    Decimal(1000),
    IMPULSE,
    aliases=(
        "kN*s",
        "kN s",
        "kN\u22c5s",
    ),
    words=("kilonewton seconds",),
)
DYNE_SECOND = UnitDef(
    "dyne_second",
    f"dyn{_DOT}s",
    Decimal("0.00001"),
    IMPULSE,
    aliases=(
        "dyn*s",
        "dyn s",
        "dyn\u22c5s",
    ),
    words=("dyne seconds", "dyne-seconds"),
)
POUND_FORCE_SECOND = UnitDef(
    "pound_force_second",
    f"lbf{_DOT}s",
    POUND_FORCE.scale,
    IMPULSE,
    aliases=(
        "lbf*s",
        "lbf s",
        "lbf\u22c5s",
    ),
    words=("pound-force seconds",),
)

Impulse._canonical_unit = NEWTON_SECOND  # noqa: SLF001 -- this module owns Impulse's canonical unit


def NewtonSecond(value: Numeric) -> Impulse:
    """Construct a Impulse from a magnitude in newton seconds."""
    return Impulse(to_exact(value) * NEWTON_SECOND.scale, NEWTON_SECOND)


def MillinewtonSecond(value: Numeric) -> Impulse:
    """Construct a Impulse from a magnitude in millinewton seconds."""
    return Impulse(to_exact(value) * MILLINEWTON_SECOND.scale, MILLINEWTON_SECOND)


def KilonewtonSecond(value: Numeric) -> Impulse:
    """Construct a Impulse from a magnitude in kilonewton seconds."""
    return Impulse(to_exact(value) * KILONEWTON_SECOND.scale, KILONEWTON_SECOND)


def DyneSecond(value: Numeric) -> Impulse:
    """Construct a Impulse from a magnitude in dyne seconds."""
    return Impulse(to_exact(value) * DYNE_SECOND.scale, DYNE_SECOND)


def PoundForceSecond(value: Numeric) -> Impulse:
    """Construct a Impulse from a magnitude in pound-force seconds."""
    return Impulse(to_exact(value) * POUND_FORCE_SECOND.scale, POUND_FORCE_SECOND)


IMPULSE_UNITS: Mapping[str, Callable[[Numeric], Impulse]] = unit_table(
    "IMPULSE_UNITS",
    {
        NEWTON_SECOND: NewtonSecond,
        MILLINEWTON_SECOND: MillinewtonSecond,
        KILONEWTON_SECOND: KilonewtonSecond,
        DYNE_SECOND: DyneSecond,
        POUND_FORCE_SECOND: PoundForceSecond,
    },
)

__all__ = [
    "DYNE_SECOND",
    "IMPULSE_UNITS",
    "KILONEWTON_SECOND",
    "MILLINEWTON_SECOND",
    "NEWTON_SECOND",
    "POUND_FORCE_SECOND",
    "DyneSecond",
    "KilonewtonSecond",
    "MillinewtonSecond",
    "NewtonSecond",
    "PoundForceSecond",
]
