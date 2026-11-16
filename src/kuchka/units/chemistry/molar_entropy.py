"""Molar entropy units: the molar heat capacity units, read as an entropy.

    from kuchka import JoulePerMoleKelvin

    standard = JoulePerMoleKelvin(188.8).to_molar_entropy()

A molar entropy is measured in joules per mole kelvin the same way a molar heat capacity
is, so `MolarEntropy` reuses `MolarHeatCapacity`'s own units as its canonical unit and
avoids minting a lookalike.
`MolarHeatCapacity.to_molar_entropy()` is what turns a value into the distinct
`MolarEntropy` type, at whichever unit the value already carries.
The calorie per mole kelvin is the classical entropy unit of chemistry tables.

`MOLAR_ENTROPY_UNITS` maps each symbol to a callable that reads a `MolarHeatCapacity`
value as a `MolarEntropy`, for boundary code that reads a unit as a string from outside
the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.quantities import MolarEntropy
from kuchka.units.chemistry.molar_heat_capacity import JOULE_PER_MOLE_KELVIN
from kuchka.units.chemistry.molar_heat_capacity import MOLAR_HEAT_CAPACITY_UNITS

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric
    from kuchka.quantities import MolarHeatCapacity

MolarEntropy._canonical_unit = JOULE_PER_MOLE_KELVIN  # noqa: SLF001 -- reused from MolarHeatCapacity's own unit


def _via_molar_heat_capacity(
    constructor: Callable[[Numeric], MolarHeatCapacity],
) -> Callable[[Numeric], MolarEntropy]:
    """Wrap a constructor so it reads its result as a `MolarEntropy`."""

    def read_as_molar_entropy(value: Numeric) -> MolarEntropy:
        return constructor(value).to_molar_entropy()

    return read_as_molar_entropy


MOLAR_ENTROPY_UNITS: Mapping[str, Callable[[Numeric], MolarEntropy]] = (
    MOLAR_HEAT_CAPACITY_UNITS.map("MOLAR_ENTROPY_UNITS", _via_molar_heat_capacity)
)

__all__ = ["MOLAR_ENTROPY_UNITS"]
