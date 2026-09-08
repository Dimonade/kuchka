"""Velocity unit constructors: MetrePerSecond.

    from kuchka import MetrePerSecond

    speed = MetrePerSecond(3)

`VELOCITY_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.

NOTE: `KilometrePerHour` is deliberately not implemented here:
its scale relative to metres per second is `1000 / 3600`, which does not terminate in
`Decimal` any more than in binary `float` (the denominator's prime factors are not
only 2 and 5, the same reason `Inch`'s reciprocal sits out some property tests in
`length.py`).
Adding it needs a decision about how much rounding is acceptable, not just a new
`UnitDef`.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import VELOCITY
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import UnitDef
from kuchka.quantities import Velocity

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

METRE_PER_SECOND = UnitDef("metre_per_second", "m/s", Decimal(1), VELOCITY)

METER_PER_SECOND = METRE_PER_SECOND

Velocity._canonical_unit = METRE_PER_SECOND  # noqa: SLF001 -- this module owns Velocity's canonical unit


def MetrePerSecond(value: Numeric) -> Velocity:
    """Construct a Velocity from a magnitude expressed in metres per second."""
    return Velocity(to_decimal(value) * METRE_PER_SECOND.scale, METRE_PER_SECOND)


MeterPerSecond = MetrePerSecond
"""American spelling, aliasing `MetrePerSecond`: the same function object."""

VELOCITY_UNITS: Mapping[str, Callable[[Numeric], Velocity]] = MappingProxyType(
    {
        METRE_PER_SECOND.symbol: MetrePerSecond,
    }
)

__all__ = [
    "METER_PER_SECOND",
    "METRE_PER_SECOND",
    "VELOCITY_UNITS",
    "MeterPerSecond",
    "MetrePerSecond",
]
