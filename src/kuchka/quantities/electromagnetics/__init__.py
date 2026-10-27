"""Quantity types for the electrical and magnetic quantities other than current."""

from __future__ import annotations

from kuchka.quantities.electromagnetics import ac_power
from kuchka.quantities.electromagnetics import capacitance
from kuchka.quantities.electromagnetics import charge
from kuchka.quantities.electromagnetics import conductance
from kuchka.quantities.electromagnetics import inductance
from kuchka.quantities.electromagnetics import magnetic_flux
from kuchka.quantities.electromagnetics import magnetic_flux_density
from kuchka.quantities.electromagnetics import permeability
from kuchka.quantities.electromagnetics import permittivity
from kuchka.quantities.electromagnetics import resistance
from kuchka.quantities.electromagnetics import voltage
from kuchka.quantities.electromagnetics.ac_power import *
from kuchka.quantities.electromagnetics.capacitance import *
from kuchka.quantities.electromagnetics.charge import *
from kuchka.quantities.electromagnetics.conductance import *
from kuchka.quantities.electromagnetics.inductance import *
from kuchka.quantities.electromagnetics.magnetic_flux import *
from kuchka.quantities.electromagnetics.magnetic_flux_density import *
from kuchka.quantities.electromagnetics.permeability import *
from kuchka.quantities.electromagnetics.permittivity import *
from kuchka.quantities.electromagnetics.resistance import *
from kuchka.quantities.electromagnetics.voltage import *

__all__: list[str] = []
__all__ += ac_power.__all__
__all__ += capacitance.__all__
__all__ += charge.__all__
__all__ += conductance.__all__
__all__ += inductance.__all__
__all__ += magnetic_flux.__all__
__all__ += magnetic_flux_density.__all__
__all__ += permeability.__all__
__all__ += permittivity.__all__
__all__ += resistance.__all__
__all__ += voltage.__all__
