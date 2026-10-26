"""Unit constructors for the electrical quantities other than current.

from kuchka import Coulomb, Ohm, Siemens, Volt, VoltAmpere

stored = Coulomb(0.5)
supply = Volt(12)
load = Ohm(47)
admittance = Siemens(0.02)
rating = VoltAmpere(1500)
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
