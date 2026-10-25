"""Unit constructors for charge, voltage, resistance, conductance, and AC power.

    from kuchka import Coulomb, Ohm, Siemens, Volt, VoltAmpere

    stored = Coulomb(0.5)
    supply = Volt(12)
    load = Ohm(47)
    admittance = Siemens(0.02)
    rating = VoltAmpere(1500)

The package holds `Charge`, `Voltage`, `Resistance`, `Conductance`, `ApparentPower`, and
`ReactivePower`.
Each has a table (`VOLTAGE_UNITS`, `RESISTANCE_UNITS`, ...) that maps a symbol to its
constructor, for boundary code that reads a unit as a string from outside the
application.
Electric current is a base quantity and is defined at the top level of `kuchka.units`
beside length and mass.
"""

from __future__ import annotations

from kuchka.units.electromagnetics import ac_power
from kuchka.units.electromagnetics import charge
from kuchka.units.electromagnetics import conductance
from kuchka.units.electromagnetics import resistance
from kuchka.units.electromagnetics import voltage
from kuchka.units.electromagnetics.ac_power import *
from kuchka.units.electromagnetics.charge import *
from kuchka.units.electromagnetics.conductance import *
from kuchka.units.electromagnetics.resistance import *
from kuchka.units.electromagnetics.voltage import *

__all__: list[str] = []
__all__ += ac_power.__all__
__all__ += charge.__all__
__all__ += conductance.__all__
__all__ += resistance.__all__
__all__ += voltage.__all__
