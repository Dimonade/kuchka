"""Quantity types for force and the work it does.

    from kuchka import Energy, Force, Power, Pressure, Torque

The package holds `Force`, `Torque`, `Pressure`, `Stress`, `Density`, `Energy`, `Power`,
and `EnergyDensity`.
`Energy` and `Power` are defined here, from force and motion, and the thermal and
electrical quantities reuse them.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package composes its own ``__all__`` from theirs, and `kuchka.quantities` composes
its own from this one's.
A new leaf module needs three lines here: its module import, its wildcard import, and
its ``__all__ +=``.
"""

from __future__ import annotations

from kuchka.quantities.mechanics import density
from kuchka.quantities.mechanics import energy
from kuchka.quantities.mechanics import energy_density
from kuchka.quantities.mechanics import force
from kuchka.quantities.mechanics import power
from kuchka.quantities.mechanics import pressure
from kuchka.quantities.mechanics import torque
from kuchka.quantities.mechanics.density import *
from kuchka.quantities.mechanics.energy import *
from kuchka.quantities.mechanics.energy_density import *
from kuchka.quantities.mechanics.force import *
from kuchka.quantities.mechanics.power import *
from kuchka.quantities.mechanics.pressure import *
from kuchka.quantities.mechanics.torque import *

__all__: list[str] = []
__all__ += density.__all__
__all__ += energy.__all__
__all__ += energy_density.__all__
__all__ += force.__all__
__all__ += power.__all__
__all__ += pressure.__all__
__all__ += torque.__all__
