"""Impedance units: the resistance units, read as an impedance.

No unit definitions live here: `kuchka.units.electromagnetics.resistance` owns the
ohm and its multiples. Each entry in `IMPEDANCE_UNITS` reads the corresponding
resistance constructor's result through `Resistance.to_impedance()`. That changes
the quantity's semantic role; it does not calculate an AC impedance from a circuit
model.

Examples
--------
For a 75-ohm purely resistive load on a 50-ohm transmission line, the voltage-wave
reflection coefficient is (Z_load - Z_line) / (Z_load + Z_line). Its magnitude is
20%, so 4% of the incident power is reflected, assuming a lossless line and a purely
resistive load:

>>> from kuchka import Ohm
>>> line = Ohm(50).to_impedance()
>>> load = Ohm(75).to_impedance()
>>> line_ohms = line.magnitude
>>> load_ohms = load.magnitude
>>> reflection = (load_ohms - line_ohms) / (load_ohms + line_ohms)
>>> float(reflection)
0.2
>>> float(reflection**2)
0.04

`IMPEDANCE_UNITS` is useful when a configuration or instrument report supplies the
unit symbol separately from the numeric value. It accepts the same symbols as
`RESISTANCE_UNITS`, while returning an `Impedance` rather than a `Resistance`.

Notes
-----
Impedance and resistance share the ohm, but they are not interchangeable concepts.
The example above is deliberately restricted to a purely resistive load. General AC
impedance can depend on frequency and include reactance; these scalar constructors
do not derive that complex impedance from resistance, inductance, and capacitance.

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
    """Wrap a `Resistance` constructor so it reads its result as an `Impedance`."""

    def read_as_impedance(value: Numeric) -> Impedance:
        return constructor(value).to_impedance()

    return read_as_impedance


IMPEDANCE_UNITS: UnitTable[Impedance] = RESISTANCE_UNITS.map(
    "IMPEDANCE_UNITS", _via_resistance
)

__all__ = ["IMPEDANCE_UNITS"]
