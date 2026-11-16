"""Specific entropy units: the specific heat capacity units, read as an entropy.

    from kuchka import JoulePerKilogramKelvin

    steam = JoulePerKilogramKelvin(7000).to_specific_entropy()

A specific entropy is measured in joules per kilogram kelvin the same way a specific
heat capacity is, so `SpecificEntropy` reuses `SpecificHeatCapacity`'s own units as its
canonical unit and avoids minting a lookalike.
`SpecificHeatCapacity.to_specific_entropy()` is what turns a value into the distinct
`SpecificEntropy` type, at whichever unit the value already carries.

`SPECIFIC_ENTROPY_UNITS` maps each symbol to a callable that reads a
`SpecificHeatCapacity` value as a `SpecificEntropy`, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.quantities import SpecificEntropy
from kuchka.units.thermodynamics.specific_heat_capacity import JOULE_PER_KILOGRAM_KELVIN
from kuchka.units.thermodynamics.specific_heat_capacity import (
    SPECIFIC_HEAT_CAPACITY_UNITS,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric
    from kuchka.quantities import SpecificHeatCapacity

SpecificEntropy._canonical_unit = JOULE_PER_KILOGRAM_KELVIN  # noqa: SLF001 -- reused from SpecificHeatCapacity's own unit


def _via_specific_heat_capacity(
    constructor: Callable[[Numeric], SpecificHeatCapacity],
) -> Callable[[Numeric], SpecificEntropy]:
    """Wrap a constructor so it reads its result as a `SpecificEntropy`."""

    def read_as_specific_entropy(value: Numeric) -> SpecificEntropy:
        return constructor(value).to_specific_entropy()

    return read_as_specific_entropy


SPECIFIC_ENTROPY_UNITS: Mapping[str, Callable[[Numeric], SpecificEntropy]] = (
    SPECIFIC_HEAT_CAPACITY_UNITS.map(
        "SPECIFIC_ENTROPY_UNITS", _via_specific_heat_capacity
    )
)

__all__ = ["SPECIFIC_ENTROPY_UNITS"]
