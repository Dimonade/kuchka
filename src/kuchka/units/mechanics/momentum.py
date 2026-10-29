"""Momentum quantities and constructors in SI, CGS, and FPS units.

Linear momentum is the product of mass and velocity: p = mv.
Its coherent SI unit is the kilogram metre per second (kg·m/s).
Momentum describes the motion of an object and determines how its velocity responds to
an applied impulse.

Impulse has the same dimension and coherent SI scale: 1 N·s = 1 kg·m/s.
They remain distinct quantity kinds in `kuchka`.
An impulse describes a change in momentum, so crossing between the two requires an
explicit conversion through `Impulse.to_momentum()` or
`Impulse.from_momentum(momentum)`.

The module provides kilogram metres per second, gram centimetres per second, and
pound feet per second.
These units serve different conventions in mechanics, from SI engineering calculations
to CGS laboratory measurements and legacy engineering records.

Examples
--------
An autonomous servicing robot approaches a 40 kg instrument package at 0.75 m/s.
Its momentum is 30 kg·m/s.
A braking actuator then applies a 12 N force opposite to the motion for one second.
Calculate the remaining momentum and velocity along the original direction:

>>> from kuchka import Kilogram, MetrePerSecond, Newton, Second
>>> package_mass = Kilogram(40)
>>> approach_speed = MetrePerSecond(0.75)
>>> initial_momentum = package_mass * approach_speed
>>> initial_momentum
30 kg·m/s
>>> braking_impulse = (Newton(-12) * Second(1)).to_momentum()
>>> remaining_momentum = initial_momentum + braking_impulse
>>> remaining_momentum
18 kg·m/s
>>> remaining_momentum / package_mass
0.45 m/s

The impulse opposes the initial motion, reducing the package's speed while leaving its
direction unchanged.
The example treats the quantities as signed components along one axis.

Notes
-----
Momentum is a vector quantity.
These scalar quantities represent magnitudes or components along a selected axis.
Signs must therefore be consistent when combining momentum with an impulse.

`MOMENTUM_UNITS` maps symbols such as ``"kg·m/s"``, ``"g·cm/s"``, and ``"lb·ft/s"`` to
their constructors.
It is intended for boundary code that reads momentum units from simulation output,
measurement records, or engineering data.

See Also
--------
~kuchka.quantities.Impulse
    Force integrated over time, representing a change in momentum.
~kuchka.quantities.Force
    The rate of change of momentum.
~kuchka.quantities.Velocity
    Displacement per unit time.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import MOMENTUM
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Momentum
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

KILOGRAM_METRE_PER_SECOND = UnitDef(
    "kilogram_metre_per_second",
    f"kg{symbols.MIDDLE_DOT}m/s",
    Decimal(1),
    MOMENTUM,
    aliases=(
        "kg*m/s",
        "kg m/s",
        "kg.m/s",
    ),
    words=("kilogram metres per second", "kilogram meters per second"),
)
GRAM_CENTIMETRE_PER_SECOND = UnitDef(
    "gram_centimetre_per_second",
    f"g{symbols.MIDDLE_DOT}cm/s",
    Decimal("0.00001"),
    MOMENTUM,
    aliases=(
        "g*cm/s",
        "g cm/s",
        "g.cm/s",
    ),
    words=("gram centimetres per second", "gram centimeters per second"),
)
POUND_FOOT_PER_SECOND = UnitDef(
    "pound_foot_per_second",
    f"lb{symbols.MIDDLE_DOT}ft/s",
    Decimal("0.138254954376"),
    MOMENTUM,
    aliases=(
        "lb*ft/s",
        "lb ft/s",
        "lb.ft/s",
    ),
    words=("pound feet per second", "pound-feet per second"),
)

Momentum._canonical_unit = KILOGRAM_METRE_PER_SECOND  # noqa: SLF001 -- this module owns Momentum's canonical unit


def KilogramMetrePerSecond(value: Numeric) -> Momentum:
    """Construct momentum from kilogram metres per second.

    Parameters
    ----------
    value : Numeric
        Momentum in kg·m/s.

    Returns
    -------
    Momentum
        Momentum represented in kilogram metres per second.

    Examples
    --------
    A 2 kg instrument carriage travels along a launch rail.
    Its measured momentum is 16 kg·m/s.
    Infer its speed from its mass and momentum:

    >>> from kuchka import Kilogram, KilogramMetrePerSecond
    >>> carriage_momentum = KilogramMetrePerSecond(16)
    >>> carriage_mass = Kilogram(2)
    >>> carriage_momentum / carriage_mass
    8 m/s

    """
    return Momentum(
        to_exact(value) * KILOGRAM_METRE_PER_SECOND.scale,
        KILOGRAM_METRE_PER_SECOND,
    )


def GramCentimetrePerSecond(value: Numeric) -> Momentum:
    """Construct momentum from gram centimetres per second.

    Parameters
    ----------
    value : Numeric
        Momentum in g·cm/s.

    Returns
    -------
    Momentum
        Momentum represented in gram centimetres per second.

    Examples
    --------
    A 2 g calibration bead has a measured momentum of 60 g·cm/s after a light impact.
    Use its mass to infer the velocity along the impact axis:

    >>> from kuchka import Gram, GramCentimetrePerSecond
    >>> bead_momentum = GramCentimetrePerSecond(60)
    >>> bead_mass = Gram(2)
    >>> bead_momentum / bead_mass
    0.3 m/s

    The CGS unit is convenient for small laboratory measurements, while `kuchka`
    resolves the resulting velocity in its own appropriate unit.

    """
    return Momentum(
        to_exact(value) * GRAM_CENTIMETRE_PER_SECOND.scale,
        GRAM_CENTIMETRE_PER_SECOND,
    )


def PoundFootPerSecond(value: Numeric) -> Momentum:
    """Construct momentum from pound feet per second.

    Parameters
    ----------
    value : Numeric
        Momentum in lb·ft/s.

    Returns
    -------
    Momentum
        Momentum represented in pound feet per second.

    Examples
    --------
    A legacy freight-handling record reports a trolley's momentum as 1200 lb·ft/s.
    If the trolley's measured mass is 100 kg, infer its speed in SI units:

    >>> from kuchka import Kilogram, PoundFootPerSecond
    >>> trolley_momentum = PoundFootPerSecond(1200)
    >>> trolley_mass = Kilogram(100)
    >>> f"{trolley_momentum / trolley_mass:.2f}"
    '1.66 m/s'

    This illustrates how a momentum reading from an FPS-based record can participate in
    calculations with SI mass and velocity quantities.

    """
    return Momentum(
        to_exact(value) * POUND_FOOT_PER_SECOND.scale,
        POUND_FOOT_PER_SECOND,
    )


MOMENTUM_UNITS: Mapping[str, Callable[[Numeric], Momentum]] = unit_table(
    "MOMENTUM_UNITS",
    {
        KILOGRAM_METRE_PER_SECOND: KilogramMetrePerSecond,
        GRAM_CENTIMETRE_PER_SECOND: GramCentimetrePerSecond,
        POUND_FOOT_PER_SECOND: PoundFootPerSecond,
    },
)

__all__ = [
    "GRAM_CENTIMETRE_PER_SECOND",
    "KILOGRAM_METRE_PER_SECOND",
    "MOMENTUM_UNITS",
    "POUND_FOOT_PER_SECOND",
    "GramCentimetrePerSecond",
    "KilogramMetrePerSecond",
    "PoundFootPerSecond",
]
