"""Torque constructors: newton-metres, joules per turn, and pound-force feet.

`Torque` is the turning effect of a force acting at a distance from an axis.
The module provides the newton-metre with its milli and kilo forms, the joule per turn,
and the US customary pound-force foot and pound-force inch:

>>> from kuchka import NewtonMetre
>>> from kuchka import PoundForceFoot
>>> bolt = NewtonMetre(40)
>>> engine = PoundForceFoot(250)

Millinewton-metres suit small motors and servos, newton-metres and pound-force feet
suit fasteners and engines, and kilonewton-metres suit the shafts of ships, turbines,
and heavy machinery.

Examples
--------
An electric motor delivers 250 N·m at 3000 rpm.
Torque times angular velocity is the mechanical power:

>>> from kuchka import RevolutionPerMinute
>>> from kuchka.units import KILOWATT
>>> power = NewtonMetre(250) * RevolutionPerMinute(3000)
>>> f"{power.to(KILOWATT):.2f}"
'78.54 kW'

A 200 N push at the end of a 25 cm spanner gives a torque, and a torque divided by the
force that produces it gives the lever arm back:

>>> from kuchka import Centimetre
>>> from kuchka import Newton
>>> from kuchka import Torque
>>> turning = Torque.from_force(Newton(200), Centimetre(25))
>>> turning
50 N·m
>>> turning / Newton(200)
0.25 m

A constant torque of 10 N·m turning a shaft through one full turn does work of
10 N·m times 2π radians:

>>> from kuchka import TurnDisplacement
>>> from kuchka.units import JOULE
>>> f"{(NewtonMetre(10) * TurnDisplacement(1)).to(JOULE):.2f}"
'62.83 J'

A torque and an energy differ by the angle, so a torque never converts to joules:

>>> NewtonMetre(10).to(JOULE)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.InvalidConversionError: ...

Notes
-----
The joule per turn is the canonical unit, because a turn is the canonical angle.
A newton-metre is a joule per radian, so it is `2 pi` joules per turn, with pi held as
an exact rational.
`Energy` refuses these units: a newton-metre of torque differs from a joule by the angle
it turns through, and multiplying a torque by an `AngularDisplacement` gives the energy.

The pound-force units come from the exact pound-force, foot, and inch, so they are exact
too, and a pound-force foot is twelve pound-force inches.
`NewtonMeter`, `MillinewtonMeter`, and `KilonewtonMeter` are the American spellings of
the same constructors.

`TORQUE_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
It accepts the plain spellings `Nm`, `N m`, and `lbf-ft`.

References
----------
NIST, Guide for the Use of the International System of Units, Appendix B.8, factors
for units listed alphabetically:
https://www.nist.gov/node/777676

BIPM, The International System of Units (SI Brochure):
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.Force
    A force at a lever arm makes a torque (`Torque.from_force`).
~kuchka.quantities.Power
    Torque times angular velocity.
~kuchka.quantities.AngularDisplacement
    Torque times an angular displacement is energy.
~kuchka.quantities.Energy
    The quantity whose units differ from torque's by the angle.
~kuchka.quantities.MomentOfInertia
    Moment of inertia times angular acceleration is a torque.

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
from kuchka.units.length import FOOT
from kuchka.units.length import INCH
from kuchka.units.mechanics.force import POUND_FORCE

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
    """Construct a Torque from a magnitude expressed in joules per turn.

    Parameters
    ----------
    value : Numeric
        Torque magnitude in joules per turn.

    Returns
    -------
    Torque
        Torque represented in joules per turn.

    Examples
    --------
    A hand crank takes 15 J of work for each turn, and the same crank in newton-metres:

    >>> crank = JoulePerTurn(15)
    >>> crank
    15 J/tr
    >>> from kuchka.units import NEWTON_METRE
    >>> f"{crank.to(NEWTON_METRE):.2f}"
    '2.39 N·m'

    Six joules per turn over three turns is 18 J, with no factor of π in the way:

    >>> from kuchka import TurnDisplacement
    >>> JoulePerTurn(6) * TurnDisplacement(3)
    18 J

    """
    return Torque(to_exact(value) * JOULE_PER_TURN.scale, JOULE_PER_TURN)


def NewtonMetre(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in newton-metres.

    Parameters
    ----------
    value : Numeric
        Torque magnitude in newton-metres.

    Returns
    -------
    Torque
        Torque represented in newton-metres.

    Examples
    --------
    A torque wrench is set to 110 N·m for a car's wheel nuts:

    >>> setting = NewtonMetre(110)
    >>> setting
    110 N·m

    On a handle half a metre long, that torque is a pull of 220 N:

    >>> from kuchka import Metre
    >>> setting / Metre(0.5)
    220 N

    The torque arrives as text in whatever spelling a datasheet uses, and the American
    spelling of the constructor is the same function:

    >>> from kuchka import Torque
    >>> from kuchka import parse
    >>> parse("110 Nm", Torque) == setting
    True
    >>> from kuchka import NewtonMeter
    >>> NewtonMeter is NewtonMetre
    True

    """
    return Torque(to_exact(value) * NEWTON_METRE.scale, NEWTON_METRE)


def MillinewtonMetre(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in millinewton-metres.

    Parameters
    ----------
    value : Numeric
        Torque magnitude in millinewton-metres.

    Returns
    -------
    Torque
        Torque represented in millinewton-metres.

    Examples
    --------
    A small geared motor in a camera gimbal is specified at 40 mN·m continuous:

    >>> motor = MillinewtonMetre(40)
    >>> motor
    40 mN·m

    At 6000 rpm, its mechanical output is about 25 W:

    >>> from kuchka import RevolutionPerMinute
    >>> from kuchka.units import WATT
    >>> f"{(motor * RevolutionPerMinute(6000)).to(WATT):.1f}"
    '25.1 W'

    """
    return Torque(to_exact(value) * MILLINEWTON_METRE.scale, MILLINEWTON_METRE)


def KilonewtonMetre(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in kilonewton-metres.

    Parameters
    ----------
    value : Numeric
        Torque magnitude in kilonewton-metres.

    Returns
    -------
    Torque
        Torque represented in kilonewton-metres.

    Examples
    --------
    A slow-speed marine diesel of 10 MW running at 100 rpm turns its shaft with a
    torque of nearly a meganewton-metre, found by dividing power by angular velocity:

    >>> from kuchka import Megawatt
    >>> from kuchka import RevolutionPerMinute
    >>> from kuchka.units import KILONEWTON_METRE
    >>> shaft = Megawatt(10) / RevolutionPerMinute(100)
    >>> f"{shaft.to(KILONEWTON_METRE):.0f}"
    '955 kN·m'

    Read the other way, a shaft that carries 955 kN·m at 100 rpm transmits 10 MW:

    >>> from kuchka.units import MEGAWATT
    >>> load = KilonewtonMetre(955)
    >>> f"{(load * RevolutionPerMinute(100)).to(MEGAWATT):.2f}"
    '10.00 MW'

    """
    return Torque(to_exact(value) * KILONEWTON_METRE.scale, KILONEWTON_METRE)


def PoundForceFoot(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in pound-force feet.

    Parameters
    ----------
    value : Numeric
        Torque magnitude in pound-force feet.

    Returns
    -------
    Torque
        Torque represented in pound-force feet.

    Examples
    --------
    A V8 engine is rated at 250 lbf·ft:

    >>> engine = PoundForceFoot(250)
    >>> engine
    250 lbf·ft

    In SI units, that is a little under 340 N·m:

    >>> from kuchka.units import NEWTON_METRE
    >>> f"{engine.to(NEWTON_METRE):.1f}"
    '339.0 N·m'

    At 5252 rpm, a torque in lbf·ft equals the power in horsepower, which is where the
    torque and power curves of an engine in these units cross:

    >>> from kuchka import RevolutionPerMinute
    >>> from kuchka.units import HORSEPOWER
    >>> f"{(engine * RevolutionPerMinute(5252)).to(HORSEPOWER):.1f}"
    '250.0 hp'

    """
    return Torque(to_exact(value) * POUND_FORCE_FOOT.scale, POUND_FORCE_FOOT)


def PoundForceInch(value: Numeric) -> Torque:
    """Construct a Torque from a magnitude expressed in pound-force inches.

    Parameters
    ----------
    value : Numeric
        Torque magnitude in pound-force inches.

    Returns
    -------
    Torque
        Torque represented in pound-force inches.

    Examples
    --------
    The cover bolts of a small gearbox are tightened to 100 lbf·in:

    >>> bolt = PoundForceInch(100)
    >>> from kuchka.units import NEWTON_METRE
    >>> f"{bolt.to(NEWTON_METRE):.2f}"
    '11.30 N·m'

    A pound-force foot is twelve pound-force inches:

    >>> from kuchka import PoundForceFoot
    >>> PoundForceFoot(1) == PoundForceInch(12)
    True

    """
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
