"""Stress is a distinct quantity type that uses the pressure units.

Pressure and material stress share the pascal (Pa), equivalent to a
newton per square metre, but they do not describe the same thing.
Pressure describes a load distributed over a surface, such as hydraulic fluid;
stress describes internal force per area within a loaded solid.
`kuchka` keeps `Pressure` and `Stress` as distinct quantity types even though their
dimensions and units are the same.

No unit definitions live here.
`kuchka.units.pressure` owns the pascal, its multiples, and pound per square inch.
`Pressure.to_stress()` interprets an existing pressure-valued magnitude as stress while
retaining its unit.
It does not calculate material stress from force and area, or establish that a measured
fluid pressure equals the stress within a component.

Examples
--------
A materials report lists a test coupon's proof strength as 0.22 GPa, while a simple
design estimate puts operating stress at 180 MPa.
Treat both readings as stress before calculating the difference:

>>> from kuchka import Gigapascal, Megapascal
>>> from kuchka.units.pressure import MEGAPASCAL
>>> proof_strength = Gigapascal(0.22).to_stress()
>>> operating_stress = Megapascal(180).to_stress()
>>> (proof_strength - operating_stress).to(MEGAPASCAL)
40 MPa

The 40 MPa is only the arithmetic difference between illustrative values;
a real design check also needs the material condition, relevant load cases, fatigue,
and applicable safety factors.

A results importer can use the unit table when a report's unit symbol arrives as data
instead of being hard-coded in the program:

>>> from kuchka.units.stress import STRESS_UNITS
>>> report_unit = "MPa"
>>> specimen_strength = STRESS_UNITS[report_unit](220)
>>> specimen_strength.to(MEGAPASCAL)
220 MPa

Notes
-----
This module exports `STRESS_UNITS`; it does not duplicate the individual pressure unit
definitions.
Each registry entry wraps the corresponding pressure constructor and calls
`.to_stress()`.
For example, `Megapascal(250).to_stress()` and `Pascal(250_000_000).to_stress()`
represent the same stress magnitude.

`STRESS_UNITS` is intended for boundary code that reads a unit symbol from external
data.
A unit symbol alone does not tell the application whether a measurement represents
pressure or stress; the caller must supply that meaning.

See Also
--------
~kuchka.quantities.Stress
    Quantity type representing material stress.
~kuchka.quantities.Pressure
    Quantity type representing pressure.
~kuchka.units.pressure
    Unit definitions shared by pressure and stress.

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
