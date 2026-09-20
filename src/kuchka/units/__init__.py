"""Engineer-facing unit constructors, one module per physical dimension.

    from kuchka import Volt, Milliampere

    voltage = Volt(4.2)
    current = Milliampere(150)
    power = voltage * current

Each quantity's canonical unit (the one arithmetic results come back in, e.g.
``Voltage * Current`` yields a result expressed in ``Watt``) is assigned onto the
corresponding domain class from ``kuchka.quantities`` at the bottom of the module that
owns that dimension.

Each leaf module owns a hand-written ``__all__`` naming exactly what it defines;
this package aggregates them with a wildcard import and derives its own ``__all__``
from whatever that leaves in scope, so adding a unit to an existing dimension never
requires touching this file.
"""

from __future__ import annotations

from kuchka.units.amount import *
from kuchka.units.angular import *
from kuchka.units.area import *
from kuchka.units.charge import *
from kuchka.units.conductance import *
from kuchka.units.current import *
from kuchka.units.density import *
from kuchka.units.energy import *
from kuchka.units.kinematics import *
from kuchka.units.length import *
from kuchka.units.luminous_intensity import *
from kuchka.units.mass import *
from kuchka.units.power import *
from kuchka.units.proportion import *
from kuchka.units.resistance import *
from kuchka.units.temporal import *
from kuchka.units.thermal import *
from kuchka.units.voltage import *
from kuchka.units.volume import *

__all__: list[str] = sorted(name for name in globals() if not name.startswith("_"))
