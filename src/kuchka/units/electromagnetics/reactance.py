"""Reactance is a distinct quantity type that uses the resistance units.

No unit definitions live here: `kuchka.units.electromagnetics.resistance` owns the ohm
and its multiples, and each entry of `REACTANCE_UNITS` reads the corresponding
resistance constructor's result through `Resistance.to_reactance()`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.quantities import Reactance
from kuchka.units.electromagnetics.resistance import OHM
from kuchka.units.electromagnetics.resistance import RESISTANCE_UNITS

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.internal.unit_table import UnitTable
    from kuchka.numeric import Numeric
    from kuchka.quantities import Resistance

Reactance._canonical_unit = OHM  # noqa: SLF001 -- reused from Resistance's own OHM


def _via_resistance(
    constructor: Callable[[Numeric], Resistance],
) -> Callable[[Numeric], Reactance]:
    """Wrap a `Resistance` constructor so it reads its result as a `Reactance`."""

    def read_as_reactance(value: Numeric) -> Reactance:
        return constructor(value).to_reactance()

    return read_as_reactance


REACTANCE_UNITS: UnitTable[Reactance] = RESISTANCE_UNITS.map(
    "REACTANCE_UNITS", _via_resistance
)

__all__ = ["REACTANCE_UNITS"]
