"""Impedance is a distinct quantity type that uses the resistance units.

No unit definitions live here: `kuchka.units.electromagnetics.resistance` owns the ohm
and its multiples, and each entry of `IMPEDANCE_UNITS` reads the corresponding
resistance constructor's result through `Resistance.to_impedance()`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.quantities import Impedance
from kuchka.units.electromagnetics.resistance import OHM
from kuchka.units.electromagnetics.resistance import RESISTANCE_UNITS

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.internal.unit_table import UnitTable
    from kuchka.numeric import Numeric
    from kuchka.quantities import Resistance

Impedance._canonical_unit = OHM  # noqa: SLF001 -- reused from Resistance's own OHM


def _via_resistance(
    constructor: Callable[[Numeric], Resistance],
) -> Callable[[Numeric], Impedance]:
    """Wrap a `Resistance` constructor so it reads its result as a `Impedance`."""

    def read_as_impedance(value: Numeric) -> Impedance:
        return constructor(value).to_impedance()

    return read_as_impedance


IMPEDANCE_UNITS: UnitTable[Impedance] = RESISTANCE_UNITS.map(
    "IMPEDANCE_UNITS", _via_resistance
)

__all__ = ["IMPEDANCE_UNITS"]
