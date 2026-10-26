"""Quantity types for the electrical and magnetic quantities other than current."""

from __future__ import annotations

from kuchka.quantities.electromagnetics import ac_power
from kuchka.quantities.electromagnetics import charge
from kuchka.quantities.electromagnetics import conductance
from kuchka.quantities.electromagnetics import resistance
from kuchka.quantities.electromagnetics import voltage
from kuchka.quantities.electromagnetics.ac_power import *
from kuchka.quantities.electromagnetics.charge import *
from kuchka.quantities.electromagnetics.conductance import *
from kuchka.quantities.electromagnetics.resistance import *
from kuchka.quantities.electromagnetics.voltage import *

__all__: list[str] = []
__all__ += ac_power.__all__
__all__ += charge.__all__
__all__ += conductance.__all__
__all__ += resistance.__all__
__all__ += voltage.__all__
