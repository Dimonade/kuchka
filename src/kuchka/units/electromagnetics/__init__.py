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
from kuchka.units.electromagnetics import capacitance
from kuchka.units.electromagnetics import charge
from kuchka.units.electromagnetics import conductance
from kuchka.units.electromagnetics import impedance
from kuchka.units.electromagnetics import inductance
from kuchka.units.electromagnetics import linear_charge_density
from kuchka.units.electromagnetics import magnetic_field_strength
from kuchka.units.electromagnetics import magnetic_flux
from kuchka.units.electromagnetics import magnetic_flux_density
from kuchka.units.electromagnetics import magnetization
from kuchka.units.electromagnetics import permeability
from kuchka.units.electromagnetics import permittivity
from kuchka.units.electromagnetics import reactance
from kuchka.units.electromagnetics import resistance
from kuchka.units.electromagnetics import specific_charge
from kuchka.units.electromagnetics import specific_current
from kuchka.units.electromagnetics import surface_charge_density
from kuchka.units.electromagnetics import voltage
from kuchka.units.electromagnetics import volume_charge_density
from kuchka.units.electromagnetics.ac_power import *
from kuchka.units.electromagnetics.capacitance import *
from kuchka.units.electromagnetics.charge import *
from kuchka.units.electromagnetics.conductance import *
from kuchka.units.electromagnetics.impedance import *
from kuchka.units.electromagnetics.inductance import *
from kuchka.units.electromagnetics.linear_charge_density import *
from kuchka.units.electromagnetics.magnetic_field_strength import *
from kuchka.units.electromagnetics.magnetic_flux import *
from kuchka.units.electromagnetics.magnetic_flux_density import *
from kuchka.units.electromagnetics.magnetization import *
from kuchka.units.electromagnetics.permeability import *
from kuchka.units.electromagnetics.permittivity import *
from kuchka.units.electromagnetics.reactance import *
from kuchka.units.electromagnetics.resistance import *
from kuchka.units.electromagnetics.specific_charge import *
from kuchka.units.electromagnetics.specific_current import *
from kuchka.units.electromagnetics.surface_charge_density import *
from kuchka.units.electromagnetics.voltage import *
from kuchka.units.electromagnetics.volume_charge_density import *

__all__: list[str] = []
__all__ += ac_power.__all__
__all__ += capacitance.__all__
__all__ += charge.__all__
__all__ += conductance.__all__
__all__ += impedance.__all__
__all__ += inductance.__all__
__all__ += linear_charge_density.__all__
__all__ += magnetic_field_strength.__all__
__all__ += magnetic_flux.__all__
__all__ += magnetic_flux_density.__all__
__all__ += magnetization.__all__
__all__ += permeability.__all__
__all__ += permittivity.__all__
__all__ += reactance.__all__
__all__ += resistance.__all__
__all__ += specific_charge.__all__
__all__ += specific_current.__all__
__all__ += surface_charge_density.__all__
__all__ += voltage.__all__
__all__ += volume_charge_density.__all__
