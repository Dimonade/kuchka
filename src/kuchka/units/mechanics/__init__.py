"""Unit constructors for the quantities of force and the work it does.

    from kuchka import Bar, Joule, Newton, NewtonMetre, Watt

    push = Newton(10)
    load = Bar(6)
    twist = NewtonMetre(20)
    work = Joule(500)
    rate_of_work = Watt(750)

The package holds `Force`, `Torque`, `Pressure`, `Stress`, `Density`, `Energy`, `Power`,
and `EnergyDensity`.
Each has a table (`FORCE_UNITS`, `TORQUE_UNITS`, ...) that maps a symbol to its
constructor, for boundary code that reads a unit as a string from outside the
application.
Energy and power are defined here, from force and motion, and the thermal and
electrical quantities reuse them.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package composes its own ``__all__`` from theirs, and `kuchka.units` composes its
own from this one's, so adding a unit to an existing dimension never touches either.
A new leaf module needs three lines here: its module import, its wildcard import, and
its ``__all__ +=``.
"""

from __future__ import annotations

from kuchka.units.mechanics import density
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import energy_density
from kuchka.units.mechanics import force
from kuchka.units.mechanics import power
from kuchka.units.mechanics import pressure
from kuchka.units.mechanics import stress
from kuchka.units.mechanics import torque
from kuchka.units.mechanics.density import *
from kuchka.units.mechanics.energy import *
from kuchka.units.mechanics.energy_density import *
from kuchka.units.mechanics.force import *
from kuchka.units.mechanics.power import *
from kuchka.units.mechanics.pressure import *
from kuchka.units.mechanics.stress import *
from kuchka.units.mechanics.torque import *

__all__: list[str] = []
__all__ += density.__all__
__all__ += energy.__all__
__all__ += energy_density.__all__
__all__ += force.__all__
__all__ += power.__all__
__all__ += pressure.__all__
__all__ += stress.__all__
__all__ += torque.__all__
