"""The generic quantity engine and the named engineering types built on it.

Application code should not need to read this package.

It exists so that ``Voltage``, ``Current``, ``Power``, ``Resistance``,
``TemperatureDelta``, and the rest of the vocabulary do not each have to hand-roll
their own arithmetic, conversion, and comparison logic:
they share one implementation (:class:`LinearQuantity`, in ``base.py``) and differ only
in their :class:`~kuchka.dimensions.Dimension` and, where relevant, their
multiplication and division overloads (``electrical.py``, ``thermal.py``).

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package imports each leaf and composes its own ``__all__`` from theirs, so adding
a unit to an existing dimension never requires touching this file.
A new leaf module needs three lines here (its module import, its wildcard import, and
its ``__all__ +=``), and ``tests/test_public_api_surface.py`` fails if one is missing.
"""

from __future__ import annotations

from kuchka.quantities import ac_power
from kuchka.quantities import activity
from kuchka.quantities import amount
from kuchka.quantities import angular
from kuchka.quantities import area
from kuchka.quantities import base
from kuchka.quantities import charge
from kuchka.quantities import data
from kuchka.quantities import density
from kuchka.quantities import electrical
from kuchka.quantities import energy
from kuchka.quantities import energy_density
from kuchka.quantities import kinematics
from kuchka.quantities import length
from kuchka.quantities import logarithmic
from kuchka.quantities import luminous_intensity
from kuchka.quantities import mass
from kuchka.quantities import pressure
from kuchka.quantities import proportion
from kuchka.quantities import rotational
from kuchka.quantities import temporal
from kuchka.quantities import thermal
from kuchka.quantities import volume
from kuchka.quantities.ac_power import *
from kuchka.quantities.activity import *
from kuchka.quantities.amount import *
from kuchka.quantities.angular import *
from kuchka.quantities.area import *
from kuchka.quantities.base import *
from kuchka.quantities.charge import *
from kuchka.quantities.data import *
from kuchka.quantities.density import *
from kuchka.quantities.electrical import *
from kuchka.quantities.energy import *
from kuchka.quantities.energy_density import *
from kuchka.quantities.kinematics import *
from kuchka.quantities.length import *
from kuchka.quantities.logarithmic import *
from kuchka.quantities.luminous_intensity import *
from kuchka.quantities.mass import *
from kuchka.quantities.pressure import *
from kuchka.quantities.proportion import *
from kuchka.quantities.rotational import *
from kuchka.quantities.temporal import *
from kuchka.quantities.thermal import *
from kuchka.quantities.volume import *

__all__: list[str] = []
__all__ += ac_power.__all__
__all__ += activity.__all__
__all__ += amount.__all__
__all__ += angular.__all__
__all__ += area.__all__
__all__ += base.__all__
__all__ += charge.__all__
__all__ += data.__all__
__all__ += density.__all__
__all__ += electrical.__all__
__all__ += energy.__all__
__all__ += energy_density.__all__
__all__ += kinematics.__all__
__all__ += length.__all__
__all__ += logarithmic.__all__
__all__ += luminous_intensity.__all__
__all__ += mass.__all__
__all__ += pressure.__all__
__all__ += proportion.__all__
__all__ += rotational.__all__
__all__ += temporal.__all__
__all__ += thermal.__all__
__all__ += volume.__all__
