"""Two small circuit-arithmetic helpers.

`power_dissipation` computes P = V² / R. `Voltage` squared has no registered
kuchka type, so the calculation drops to `.magnitude` for that one step and wraps
the result back up as `Power`.

`parallel` and `series` combine resistors using ordinary typed arithmetic: `1 /
Resistance` is a `Conductance`, so no manual unit handling is needed.
"""

from __future__ import annotations

from kuchka import Ohm
from kuchka import Power
from kuchka import Resistance
from kuchka import Voltage
from kuchka import Watt


def parallel(*resistors: Resistance) -> Resistance:
    """Return the equivalent Resistance of `resistors` combined in parallel.

    Sums each resistor's conductance (`1 / Resistance`) and inverts the total.
    Raises `ZeroDivisionError` if `resistors` is empty or any resistor is 0 ohms.
    """
    if not resistors:
        msg = "parallel() needs at least one resistor"
        raise ZeroDivisionError(msg)
    total_conductance = 1 / resistors[0]
    for resistor in resistors[1:]:
        total_conductance = total_conductance + 1 / resistor
    return 1 / total_conductance


def series(*resistors: Resistance) -> Resistance:
    """Return the equivalent Resistance of `resistors` combined in series."""
    total = Ohm(0)
    for resistor in resistors:
        total = total + resistor
    return total


def power_dissipation(voltage: Voltage, resistance: Resistance) -> Power:
    """Return the power dissipated by `resistance` at `voltage`, via P = V² / R.

    `voltage.magnitude` and `resistance.magnitude` are always expressed in kuchka's
    canonical units (volts, ohms), regardless of the prefix each value was
    constructed with, so no unit alignment is needed before the division.
    """
    watts = voltage.magnitude * voltage.magnitude / resistance.magnitude
    return Watt(watts)
