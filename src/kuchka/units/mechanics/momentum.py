"""Momentum unit constructors: kilogram metres per second and its CGS and FPS forms.

    from kuchka import KilogramMetrePerSecond, PoundFootPerSecond

    cart = KilogramMetrePerSecond(6)
    freight = PoundFootPerSecond(1200)

A momentum is a mass times a velocity, so the coherent unit is the kilogram metre
per second.
It equals the newton second of an impulse (1 kg·m/s = 1 N·s), and the CGS unit is the
gram centimetre per second (1 g·cm/s = 1e-5 kg·m/s).

`MOMENTUM_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
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

_DOT = symbols.MIDDLE_DOT

KILOGRAM_METRE_PER_SECOND = UnitDef(
    "kilogram_metre_per_second",
    f"kg{_DOT}m/s",
    Decimal(1),
    MOMENTUM,
    aliases=(
        "kg*m/s",
        "kg m/s",
        "kg\u22c5m/s",
        "kg.m/s",
    ),
    words=("kilogram metres per second", "kilogram meters per second"),
)
GRAM_CENTIMETRE_PER_SECOND = UnitDef(
    "gram_centimetre_per_second",
    f"g{_DOT}cm/s",
    Decimal("0.00001"),
    MOMENTUM,
    aliases=(
        "g*cm/s",
        "g cm/s",
        "g\u22c5cm/s",
        "g.cm/s",
    ),
    words=("gram centimetres per second", "gram centimeters per second"),
)
POUND_FOOT_PER_SECOND = UnitDef(
    "pound_foot_per_second",
    f"lb{_DOT}ft/s",
    Decimal("0.138254954376"),
    MOMENTUM,
    aliases=(
        "lb*ft/s",
        "lb ft/s",
        "lb\u22c5ft/s",
        "lb.ft/s",
    ),
    words=("pound feet per second", "pound-feet per second"),
)

Momentum._canonical_unit = KILOGRAM_METRE_PER_SECOND  # noqa: SLF001 -- this module owns Momentum's canonical unit


def KilogramMetrePerSecond(value: Numeric) -> Momentum:
    """Construct a Momentum from a magnitude in kilogram metres per second."""
    return Momentum(
        to_exact(value) * KILOGRAM_METRE_PER_SECOND.scale, KILOGRAM_METRE_PER_SECOND
    )


def GramCentimetrePerSecond(value: Numeric) -> Momentum:
    """Construct a Momentum from a magnitude in gram centimetres per second."""
    return Momentum(
        to_exact(value) * GRAM_CENTIMETRE_PER_SECOND.scale, GRAM_CENTIMETRE_PER_SECOND
    )


def PoundFootPerSecond(value: Numeric) -> Momentum:
    """Construct a Momentum from a magnitude in pound feet per second."""
    return Momentum(
        to_exact(value) * POUND_FOOT_PER_SECOND.scale, POUND_FOOT_PER_SECOND
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
