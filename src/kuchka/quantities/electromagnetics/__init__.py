"""Quantity types for charge, voltage, resistance, conductance, and AC power.

    from kuchka import Charge, Conductance, Resistance, Voltage

The package holds `Charge`, `Voltage`, `Resistance`, `Conductance`, `ApparentPower`, and
`ReactivePower`.
Electric current is a base quantity and is defined at the top level of
`kuchka.quantities`, beside length and mass.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package composes its own ``__all__`` from theirs, and `kuchka.quantities` composes
its own from this one's.
A new leaf module needs three lines here: its module import, its wildcard import, and
its ``__all__ +=``.
"""

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
