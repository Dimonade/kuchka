"""Force quantities and constructors for SI and selected historical units.

`Force` represents mechanical interaction capable of changing the motion of a body.
The newton is the canonical SI unit:

    1 N = 1 kg m / s²

The constructors in this module provide SI prefixes from micronewtons through
meganewtons, together with selected exact non-SI units useful in engineering and
scientific work.

Examples
--------
Newton's second law connects force to mass and acceleration.
Accelerating a 2 kg camera rig at 3 m/s² requires exactly 6 N:

>>> from kuchka import Kilogram
>>> from kuchka import MetrePerSecondSquared
>>> mass = Kilogram(2)
>>> acceleration = MetrePerSecondSquared(3)
>>> force = mass * acceleration
>>> force
6 N

The same relationship works in the other direction.
A 10 N force acting on a 2 kg object produces an acceleration of 5 m/s²:

>>> Newton(10) / Kilogram(2)
5 m/s²

Force also connects pressure and area.
A pressure of 100 kPa acting over 0.01 m² produces 1000 N:

>>> from kuchka import Kilopascal
>>> from kuchka import SquareMetre
>>> pressure = Kilopascal(100)
>>> area = SquareMetre(0.01)
>>> pressure * area
1000 N

The prefixes cover very different physical scales.
A sensitive force sensor may measure forces in micronewtons:

>>> sensor_force = Micronewton(250)

Precision mechanical components commonly involve millinewtons:

>>> preload = Millinewton(750)

Structural loads are naturally expressed in kilonewtons:

>>> crane_load = Kilonewton(125)

Large mechanical systems can reach meganewton forces:

>>> thrust = Meganewton(2)

The CGS dyne is much smaller than the newton:

>>> Dyne(1_000_000) == Newton(10)
True

Pound-force is an exact non-SI unit in this library.
One pound-force is exactly 4.4482216152605 N:

>>> PoundForce(1).to(NEWTON)
4.4482216152605 N

A force can also be integrated over time to produce impulse.
A constant 20 N force acting for 3 seconds produces 60 N s of impulse:

>>> from kuchka import Newton
>>> from kuchka import Second
>>> # impulse = Newton(20) * Second(3)

# NOTE: While the example above should be valid, Impulse is currently not implemented.

Notes
-----
Force is a derived quantity with dimensions of mass times acceleration:

    F = m a

The same force can therefore be expressed through several equivalent physical
relationships:

    F = m a
    F = p A
    F = W / d
    F = Δp / Δt

where `p` denotes pressure, `A` area, `W` work, `d` displacement, and `Δp` momentum
change.

The newton is the coherent SI unit of force.
Its defining relation is exact:

    1 N = 1 kg m / s²

Metric prefixes represent exact powers of ten.

The dyne is the CGS unit of force and is exactly `1e-5 N`.

Pound-force is defined from the international avoirdupois pound and standard
acceleration of gravity.
Its conversion to newtons is therefore exact:

    1 lbf = 4.4482216152605 N

`FORCE_UNITS` maps symbols such as ``"N"``, ``"kN"``, ``"dyn"``, and ``"lbf"`` to their
constructors for configuration files and other external interfaces.

See Also
--------
~kuchka.quantities.Mass
    Mass participating in Newton's second law.
~kuchka.quantities.Acceleration
    Acceleration related to force through Newton's second law.
~kuchka.quantities.Pressure
    Pressure multiplied by area produces force.
~kuchka.quantities.Energy
    Work divided by displacement produces force.
~kuchka.quantities.Impulse
    Force integrated over time.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import FORCE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Force
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


NEWTON_NAME = "newton"
NEWTON_SYMBOL = "N"

MICRONEWTON = prefixed_unit(prefixes.MICRO, NEWTON_NAME, NEWTON_SYMBOL, FORCE)
MILLINEWTON = prefixed_unit(prefixes.MILLI, NEWTON_NAME, NEWTON_SYMBOL, FORCE)
NEWTON = prefixed_unit(prefixes.UNIT, NEWTON_NAME, NEWTON_SYMBOL, FORCE)
KILONEWTON = prefixed_unit(prefixes.KILO, NEWTON_NAME, NEWTON_SYMBOL, FORCE)
MEGANEWTON = prefixed_unit(prefixes.MEGA, NEWTON_NAME, NEWTON_SYMBOL, FORCE)

Force._canonical_unit = NEWTON  # noqa: SLF001 -- this module owns Force's canonical unit


def Micronewton(value: Numeric) -> Force:
    """Construct a force from a magnitude expressed in micronewtons.

    Parameters
    ----------
    value : Numeric
        Force magnitude in micronewtons.

    Returns
    -------
    Force
        Force represented in micronewtons.

    Examples
    --------
    An atomic-force microscope can measure forces on the micronewton scale:

    >>> contact_force = Micronewton(2.5)
    >>> contact_force
    2.5 µN

    """
    return Force(to_exact(value) * MICRONEWTON.scale, MICRONEWTON)


def Millinewton(value: Numeric) -> Force:
    """Construct a force from a magnitude expressed in millinewtons.

    Parameters
    ----------
    value : Numeric
        Force magnitude in millinewtons.

    Returns
    -------
    Force
        Force represented in millinewtons.

    Examples
    --------
    A small mechanical preload can be conveniently expressed in millinewtons:

    >>> preload = Millinewton(750)
    >>> preload
    750 mN

    """
    return Force(to_exact(value) * MILLINEWTON.scale, MILLINEWTON)


def Newton(value: Numeric) -> Force:
    """Construct a force from a magnitude expressed in newtons.

    Parameters
    ----------
    value : Numeric
        Force magnitude in newtons.

    Returns
    -------
    Force
        Force represented in newtons.

    Examples
    --------
    Newton's second law gives the force required to accelerate a 2 kg object at 3 m/s²:

    >>> from kuchka import Kilogram
    >>> from kuchka import MetrePerSecondSquared
    >>> mass = Kilogram(2)
    >>> acceleration = MetrePerSecondSquared(3)
    >>> mass * acceleration
    6 N

    """
    return Force(to_exact(value) * NEWTON.scale, NEWTON)


def Kilonewton(value: Numeric) -> Force:
    """Construct a force from a magnitude expressed in kilonewtons.

    Parameters
    ----------
    value : Numeric
        Force magnitude in kilonewtons.

    Returns
    -------
    Force
        Force represented in kilonewtons.

    Examples
    --------
    Structural loads are commonly specified in kilonewtons:

    >>> crane_load = Kilonewton(125)
    >>> crane_load
    125 kN

    """
    return Force(to_exact(value) * KILONEWTON.scale, KILONEWTON)


def Meganewton(value: Numeric) -> Force:
    """Construct a force from a magnitude expressed in meganewtons.

    Parameters
    ----------
    value : Numeric
        Force magnitude in meganewtons.

    Returns
    -------
    Force
        Force represented in meganewtons.

    Examples
    --------
    Large propulsion and structural loads can reach the meganewton scale:

    >>> thrust = Meganewton(2)
    >>> thrust
    2 MN

    """
    return Force(to_exact(value) * MEGANEWTON.scale, MEGANEWTON)


# Non-SI units.

DYNE = UnitDef("dyne", "dyn", Decimal("0.00001"), FORCE)
"""The CGS unit of force.

One dyne is exactly `1e-5` newtons.
"""

POUND_FORCE = UnitDef(
    "pound_force",
    "lbf",
    Decimal("4.4482216152605"),
    FORCE,
    words=("pound-force",),
)
"""The pound-force unit.

One pound-force is exactly `4.4482216152605` newtons.
This follows from the international definition of the avoirdupois pound and standard
acceleration of gravity.
"""

KILOGRAM_FORCE = UnitDef(
    "kilogram_force",
    "kgf",
    Decimal("9.80665"),
    FORCE,
    aliases=("kp",),
    words=("kilogram-force", "kilopond"),
)
"""The kilogram-force unit.

One kilogram-force is exactly `9.80665` newtons, based on standard acceleration of
gravity.
"""


def Dyne(value: Numeric) -> Force:
    """Construct a force from a magnitude expressed in dynes.

    Parameters
    ----------
    value : Numeric
        Force magnitude in dynes.

    Returns
    -------
    Force
        Force represented in dynes.

    Examples
    --------
    A million dynes correspond to exactly ten newtons:

    >>> Dyne(1_000_000) == Newton(10)
    True

    """
    return Force(to_exact(value) * DYNE.scale, DYNE)


def PoundForce(value: Numeric) -> Force:
    """Construct a force from a magnitude expressed in pound-force.

    Parameters
    ----------
    value : Numeric
        Force magnitude in pound-force.

    Returns
    -------
    Force
        Force represented in pound-force.

    Examples
    --------
    One pound-force has an exact SI conversion:

    >>> PoundForce(1).to(NEWTON)
    4.4482216152605 N

    """
    return Force(to_exact(value) * POUND_FORCE.scale, POUND_FORCE)


def KilogramForce(value: Numeric) -> Force:
    """Construct a force from a magnitude expressed in kilogram-force.

    Parameters
    ----------
    value : Numeric
        Force magnitude in kilogram-force.

    Returns
    -------
    Force
        Force represented in kilogram-force.

    Examples
    --------
    Standard gravity defines one kilogram-force as exactly 9.80665 N:

    >>> KilogramForce(1).to(NEWTON)
    9.80665 N

    """
    return Force(to_exact(value) * KILOGRAM_FORCE.scale, KILOGRAM_FORCE)


FORCE_UNITS: Mapping[str, Callable[[Numeric], Force]] = unit_table(
    "FORCE_UNITS",
    {
        MICRONEWTON: Micronewton,
        MILLINEWTON: Millinewton,
        NEWTON: Newton,
        KILONEWTON: Kilonewton,
        MEGANEWTON: Meganewton,
        DYNE: Dyne,
        POUND_FORCE: PoundForce,
        KILOGRAM_FORCE: KilogramForce,
    },
)

__all__ = [
    "DYNE",
    "FORCE_UNITS",
    "KILOGRAM_FORCE",
    "KILONEWTON",
    "MEGANEWTON",
    "MICRONEWTON",
    "MILLINEWTON",
    "NEWTON",
    "POUND_FORCE",
    "Dyne",
    "KilogramForce",
    "Kilonewton",
    "Meganewton",
    "Micronewton",
    "Millinewton",
    "Newton",
    "PoundForce",
]
