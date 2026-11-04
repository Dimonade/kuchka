"""`Entropy`'s units, reached from `HeatCapacity`.

    from kuchka import JoulePerKelvin

    change = JoulePerKelvin(5).to_entropy()

An entropy is measured in joules per kelvin the same way a heat capacity is.
`HeatCapacity`'s own `JOULE_PER_KELVIN`, `KILOJOULE_PER_KELVIN`, and the calorie units
already say that, so `Entropy` reuses them as its own canonical unit and avoids minting
a lookalike.
`HeatCapacity.to_entropy()` is what turns a value into the distinct `Entropy` type, at
whichever unit the value already carries.

`ENTROPY_UNITS` maps each symbol to a callable that reads a `HeatCapacity` value as an
`Entropy`, for boundary code that reads a unit as a string from outside the
application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.quantities import Entropy
from kuchka.units.thermodynamics.heat_capacity import HEAT_CAPACITY_UNITS
from kuchka.units.thermodynamics.heat_capacity import JOULE_PER_KELVIN

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric
    from kuchka.quantities import HeatCapacity

Entropy._canonical_unit = JOULE_PER_KELVIN  # noqa: SLF001 -- reused from HeatCapacity's own JOULE_PER_KELVIN


def _via_heat_capacity(
    constructor: Callable[[Numeric], HeatCapacity],
) -> Callable[[Numeric], Entropy]:
    """Wrap a `HeatCapacity` constructor so it reads its result as an `Entropy`."""

    def read_as_entropy(value: Numeric) -> Entropy:
        return constructor(value).to_entropy()

    return read_as_entropy


ENTROPY_UNITS: Mapping[str, Callable[[Numeric], Entropy]] = HEAT_CAPACITY_UNITS.map(
    "ENTROPY_UNITS", _via_heat_capacity
)

__all__ = ["ENTROPY_UNITS"]
