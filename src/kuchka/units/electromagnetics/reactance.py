"""Reactance is the signed imaginary part of impedance in AC circuit analysis.

Reactance is measured in ohms, but it is not resistance or impedance.
Inductive reactance is positive and increases with frequency.
Capacitive reactance is negative and its magnitude decreases with frequency.
With the convention Z = R + jX, ideal components follow X_L = 2πfL and X_C = -1/(2πfC).

No unit definitions live here: `kuchka.units.electromagnetics.resistance` owns the ohm
and its multiples.
Each entry of `REACTANCE_UNITS` reads the corresponding resistance constructor's result
through `Resistance.to_reactance()`.
That conversion preserves the numerical reading and changes its quantity kind; it does
not calculate reactance from frequency, inductance, or capacitance.

Examples
--------
An engineer checks a 50 Hz series branch containing a 10 mH inductor and a 100 µF
capacitor.
The inductor contributes positive reactance, while the capacitor contributes negative
reactance.
Their sum is still capacitive at 50 Hz:

>>> from math import pi, sqrt
>>> from kuchka.units.electromagnetics.resistance import OHM, Ohm
>>> inductive = Ohm(2 * pi * 50 * 10e-3).to_reactance()
>>> capacitive = Ohm(-1 / (2 * pi * 50 * 100e-6)).to_reactance()
>>> f"{inductive.to(OHM):.3f}"
'3.142 Ω'
>>> f"{capacitive.to(OHM):.3f}"
'-31.831 Ω'
>>> f"{(inductive + capacitive).to(OHM):.2f}"
'-28.69 Ω'
>>> f"{1 / (2 * pi * sqrt(10e-3 * 100e-6)):.1f} Hz"
'159.2 Hz'

The last value is the ideal LC resonant frequency.
At resonance the two ideal reactances cancel; real components also have resistance and
parasitic effects, so a physical circuit will not behave as a perfectly lossless
branch.

An impedance analyser exports the signed reactance component in kilo-ohms.
Boundary code can use the shared unit table to interpret that reading as a `Reactance`
rather than as a `Resistance`:

>>> reading = REACTANCE_UNITS["kΩ"](3.3)
>>> reading.to(OHM)
3300 Ω

A domestic microwave oven uses a magnetron operating at 2.45 GHz.
At this frequency, the ideal capacitive reactance of a 1 pF capacitor is about 65 Ω
in magnitude.
This is an ideal lumped-element estimate, not a model of a specific magnetron or its
internal circuitry; component parasitics and layout become important at microwave
frequencies.

>>> from math import pi
>>> from kuchka import Ohm
>>> frequency_Hz = 2.45e9
>>> capacitance_F = 1e-12
>>> capacitor = Ohm(
...     -1 / (2 * pi * frequency_Hz * capacitance_F)
... ).to_reactance()
>>> f"{capacitor.to(OHM):.1f}"
'-65.0 Ω'

Notes
-----
Some references quote capacitive reactance as a positive magnitude, X_C = 1/(2πfC), and
account for its capacitive nature separately in the complex impedance.
Here the signed quantity follows the convention Z = R + jX, so capacitive reactance is
negative.
Both conventions describe the same physical circuit when applied consistently.

For a derivation of the ideal inductive and capacitive formulas, see OpenStax, *College
Physics 2e*, “Reactance, Inductive and Capacitive”:
https://openstax.org/books/college-physics-2e/pages/23-11-reactance-inductive-and-capacitive

EMF Portal, Microwave oven: operating frequency and magnetron use
https://www.emf-portal.org/en/emf-source/603

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
