"""Unit constructors for Acceleration.

    from kuchka import MetrePerSecondSquared

    rate_of_change = MetrePerSecondSquared(17.2)

`ACCELERATION_UNITS` maps each symbol to its constructor, for boundary code that reads
a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import ACCELERATION
from kuchka.internal import symbols
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Acceleration
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


METRE_PER_SECOND_SQUARED = UnitDef(
    "metre_per_second_squared",
    f"m/s{symbols.SUPERSCRIPT_TWO}",
    Decimal(1),
    ACCELERATION,
)

METER_PER_SECOND_SQUARED = METRE_PER_SECOND_SQUARED

Acceleration._canonical_unit = METRE_PER_SECOND_SQUARED  # noqa: SLF001 -- this module owns Acceleration's canonical unit


def MetrePerSecondSquared(value: Numeric) -> Acceleration:
    """Construct an Acceleration from a magnitude in metres per second squared."""
    return Acceleration(
        to_exact(value) * METRE_PER_SECOND_SQUARED.scale,
        METRE_PER_SECOND_SQUARED,
    )


MeterPerSecondSquared = MetrePerSecondSquared
"""American spelling, aliasing `MetrePerSecondSquared`: the same function object."""

ACCELERATION_UNITS: Mapping[str, Callable[[Numeric], Acceleration]] = MappingProxyType(
    {
        METRE_PER_SECOND_SQUARED.symbol: MetrePerSecondSquared,
    }
)

__all__ = [
    "ACCELERATION_UNITS",
    "METER_PER_SECOND_SQUARED",
    "METRE_PER_SECOND_SQUARED",
    "MeterPerSecondSquared",
    "MetrePerSecondSquared",
]
