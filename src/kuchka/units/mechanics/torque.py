"""Torque unit constructors: NewtonMetre, PoundForceFoot, and their relatives.

    from kuchka import NewtonMetre, PoundForceFoot

    bolt = NewtonMetre(40)
    engine = PoundForceFoot(250)

The joule per turn is the canonical unit, because a turn is the canonical angle.
A newton-metre of torque is a joule per radian, so it is `2 pi` joules per turn,
with pi held as an exact rational (see `kuchka.units.angular`).
The pound-force units are computed from kuchka's own exact `POUND_FORCE`, `FOOT`, and
`INCH` scales, so they cannot drift from them.

These units belong to `Torque` and are refused by `Energy`: a newton-metre of torque
differs from a joule by the angle it turns through.
`Torque.from_force(force, lever_arm)` builds a torque from a force at a distance.

`TORQUE_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import TORQUE
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Torque
from kuchka.quantities import UnitDef
from kuchka.units.kinematics.force import POUND_FORCE
from kuchka.units.length import FOOT
from kuchka.units.length import INCH

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_PER_RADIAN = 2 * PI

JOULE_PER_TURN = UnitDef(
    "joule_per_turn",
    "J/tr",
    1,
    TORQUE,
    aliases=("J/rev",),
    words=("joule per revolution",),
)
NEWTON_METRE = UnitDef(
    "newton_metre",
    f"N{symbols.MIDDLE_DOT}m",
    _PER_RADIAN,
    TORQUE,
    aliases=("Nm", "N m", "N*m"),
    words=("newton metre", "newton meter"),
)
MILLINEWTON_METRE = UnitDef(
    "millinewton_metre",
    f"mN{symbols.MIDDLE_DOT}m",
    _PER_RADIAN / 1000,
    TORQUE,
    aliases=("mNm", "mN m", "mN*m"),
)
KILONEWTON_METRE = UnitDef(
    "kilonewton_metre",
    f"kN{symbols.MIDDLE_DOT}m",
    _PER_RADIAN * 1000,
    TORQUE,
    aliases=("kNm", "kN m", "kN*m"),
)
POUND_FORCE_FOOT = UnitDef(
    "pound_force_foot",
    f"lbf{symbols.MIDDLE_DOT}ft",
    _PER_RADIAN * POUND_FORCE.scale * FOOT.scale,
    TORQUE,
    aliases=("lbf-ft", "lbf ft", "lbf*ft"),
    words=("pound-force foot", "pound-foot"),
)
POUND_FORCE_INCH = UnitDef(
    "pound_force_inch",
    f"lbf{symbols.MIDDLE_DOT}in",
    _PER_RADIAN * POUND_FORCE.scale * INCH.scale,
    TORQUE,
    aliases=("lbf-in", "lbf in", "lbf*in"),
    words=("pound-force inch", "pound-inch"),
)

NEWTON_METER = NEWTON_METRE
MILLINEWTON_METER = MILLINEWTON_METRE
KILONEWTON_METER = KILONEWTON_METRE

Torque._canonical_unit = JOULE_PER_TURN  # noqa: SLF001 -- this module owns Torque's canonical unit
Torque._result_unit = NEWTON_METRE  # noqa: SLF001 -- and the unit its arithmetic results display in


def JoulePerTurn(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in joules per turn."""
    return Torque(to_exact(value) * JOULE_PER_TURN.scale, JOULE_PER_TURN)


def NewtonMetre(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in newton-metres."""
    return Torque(to_exact(value) * NEWTON_METRE.scale, NEWTON_METRE)


def MillinewtonMetre(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in millinewton-metres."""
    return Torque(to_exact(value) * MILLINEWTON_METRE.scale, MILLINEWTON_METRE)


def KilonewtonMetre(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in kilonewton-metres."""
    return Torque(to_exact(value) * KILONEWTON_METRE.scale, KILONEWTON_METRE)


def PoundForceFoot(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in pound-force feet."""
    return Torque(to_exact(value) * POUND_FORCE_FOOT.scale, POUND_FORCE_FOOT)


def PoundForceInch(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in pound-force inches."""
    return Torque(to_exact(value) * POUND_FORCE_INCH.scale, POUND_FORCE_INCH)


NewtonMeter = NewtonMetre
MillinewtonMeter = MillinewtonMetre
KilonewtonMeter = KilonewtonMetre


TORQUE_UNITS: Mapping[str, Callable[[Numeric], Torque]] = unit_table(
    "TORQUE_UNITS",
    {
        JOULE_PER_TURN: JoulePerTurn,
        NEWTON_METRE: NewtonMetre,
        MILLINEWTON_METRE: MillinewtonMetre,
        KILONEWTON_METRE: KilonewtonMetre,
        POUND_FORCE_FOOT: PoundForceFoot,
        POUND_FORCE_INCH: PoundForceInch,
    },
)

__all__ = [
    "JOULE_PER_TURN",
    "KILONEWTON_METER",
    "KILONEWTON_METRE",
    "MILLINEWTON_METER",
    "MILLINEWTON_METRE",
    "NEWTON_METER",
    "NEWTON_METRE",
    "POUND_FORCE_FOOT",
    "POUND_FORCE_INCH",
    "TORQUE_UNITS",
    "JoulePerTurn",
    "KilonewtonMeter",
    "KilonewtonMetre",
    "MillinewtonMeter",
    "MillinewtonMetre",
    "NewtonMeter",
    "NewtonMetre",
    "PoundForceFoot",
    "PoundForceInch",
]
