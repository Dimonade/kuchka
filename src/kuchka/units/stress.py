"""`Stress`'s units, reached from `Pressure`.

    from kuchka import Gigapascal, Megapascal

    steel_modulus = Gigapascal(200).to_stress()
    yield_strength = Megapascal(250).to_stress()

A stress is measured in pascals the same way a pressure is.
`Pressure`'s own `PASCAL`, `MEGAPASCAL`, `GIGAPASCAL`, and `POUND_PER_SQUARE_INCH`
already say that, so `Stress` reuses every unit of `kuchka.units.pressure` and mints
no lookalike.
`Pressure.to_stress()` is what turns a `Pressure` value into the distinct `Stress`
type, at whichever unit the value already carries.
`Megapascal(250).to_stress()` and `Pascal(250_000_000).to_stress()` are the same
reading.

`STRESS_UNITS` maps each symbol to a callable that reads a `Pressure` value as a
`Stress`, for boundary code that reads a unit as a string from outside the
application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.quantities import Stress
from kuchka.units.pressure import PASCAL
from kuchka.units.pressure import PRESSURE_UNITS

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.internal.unit_table import UnitTable
    from kuchka.numeric import Numeric
    from kuchka.quantities import Pressure

Stress._canonical_unit = PASCAL  # noqa: SLF001 -- reused from Pressure's own PASCAL


def _via_pressure(
    constructor: Callable[[Numeric], Pressure],
) -> Callable[[Numeric], Stress]:
    """Wrap a `Pressure` constructor so it reads its result as a `Stress`."""

    def read_as_stress(value: Numeric) -> Stress:
        return constructor(value).to_stress()

    return read_as_stress


STRESS_UNITS: UnitTable[Stress] = PRESSURE_UNITS.map("STRESS_UNITS", _via_pressure)

__all__ = ["STRESS_UNITS"]
