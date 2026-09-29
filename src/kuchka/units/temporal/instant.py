"""`Instant`'s canonical unit, reached from `Time`.

    from kuchka import Second, Millisecond, Hour

    reading = Second(1_700_000_000).as_instant()
    later = reading + Millisecond(500)   # -> Instant
    checkpoint = Hour(1).as_instant()    # an hour past whatever the caller calls zero

`INSTANT_SECOND` is the affine counterpart of `Time`'s own `SECOND`:
Same scale (1 second per unit), zero offset, so it sits alongside `Time`'s canonical
unit the way `Temperature`'s `KELVIN` sits alongside `TemperatureDelta`'s canonical
unit.
This is the plain, unshifted reference every reading is ultimately expressed against.
`Time.as_instant()` is what turns a `Time` value into the distinct `Instant` type, at
whichever prefix the value already carries.

`INSTANT_UNITS` maps each symbol to a callable that reads a Time value as an Instant,
for boundary code that reads a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.quantities import AffineUnitDef
from kuchka.quantities import Instant
from kuchka.units.temporal.time import TIME_UNITS

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric
    from kuchka.quantities import Time

INSTANT_SECOND = AffineUnitDef("instant_second", "s", Decimal(1), Decimal(0))

Instant._canonical_unit = INSTANT_SECOND  # noqa: SLF001 -- this module owns Instant's canonical unit


def _via_time(constructor: Callable[[Numeric], Time]) -> Callable[[Numeric], Instant]:
    """Wrap a Time constructor so it reads its result as an Instant instead."""

    def read_as_instant(value: Numeric) -> Instant:
        return constructor(value).as_instant()

    return read_as_instant


INSTANT_UNITS: Mapping[str, Callable[[Numeric], Instant]] = MappingProxyType(
    {symbol: _via_time(constructor) for symbol, constructor in TIME_UNITS.items()}
)

__all__ = ["INSTANT_SECOND", "INSTANT_UNITS"]
