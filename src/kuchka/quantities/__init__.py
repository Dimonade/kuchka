"""The generic quantity engine and the named engineering types built on it.

Application code should not need to read this package.

It exists so that ``Voltage``, ``Current``, ``Power``, ``Resistance``,
``TemperatureDelta``, and the rest of the vocabulary do not each have to hand-roll
their own arithmetic, conversion, and comparison logic:
they share one implementation (:class:`LinearQuantity`, in ``kuchka.quantities.base``)
and differ only in their :class:`~kuchka.dimensions.Dimension` and, where relevant,
their multiplication and division overloads.

The base dimensions and the axes that are not dimensions of their own each have a
module at this level, and `temporal` is one module because its types construct one
another.
Related derived types live in themed packages that mirror those of `kuchka.units`:
`geometry`, `kinematics`, `mechanics`, `electromagnetics`, `information`, and
`radiation`.
A package imports only from the top level and from the packages before it in that
order, at import time; an overload may name any type, because it is read by type
checkers and never run.

Runtime arithmetic (`+`, `-`, `*`, `/`) is fully general and lives on `LinearQuantity`:
it derives any product or quotient from `Dimension` exponent-vector algebra.
Type checkers cannot infer "Voltage times Current is Power" from that algebra, so each
type spells out its relationships as explicit `@overload` declarations, and every
overload list ends with a fallback matching the signature declared on `LinearQuantity`,
which keeps the overrides compatible with the base class under strict checking.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines, and
each package composes its own from its leaves.
This package star-imports every leaf directly, which the type checkers follow, and
composes its own ``__all__`` from the packages'.
A new leaf module needs a wildcard import here and its three lines in its own package,
a new package needs its import and its ``__all__ +=`` here, and a test fails if one is
missing.
"""

from __future__ import annotations

from kuchka.quantities import amount
from kuchka.quantities import angular
from kuchka.quantities import base
from kuchka.quantities import current
from kuchka.quantities import electromagnetics
from kuchka.quantities import geometry
from kuchka.quantities import information
from kuchka.quantities import kinematics
from kuchka.quantities import length
from kuchka.quantities import logarithmic
from kuchka.quantities import luminous_intensity
from kuchka.quantities import mass
from kuchka.quantities import mechanics
from kuchka.quantities import proportion
from kuchka.quantities import radiation
from kuchka.quantities import temporal
from kuchka.quantities import thermal
from kuchka.quantities.amount import *
from kuchka.quantities.angular import *
from kuchka.quantities.base import *
from kuchka.quantities.current import *
from kuchka.quantities.electromagnetics.ac_power import *
from kuchka.quantities.electromagnetics.charge import *
from kuchka.quantities.electromagnetics.conductance import *
from kuchka.quantities.electromagnetics.resistance import *
from kuchka.quantities.electromagnetics.voltage import *
from kuchka.quantities.geometry.area import *
from kuchka.quantities.geometry.volume import *
from kuchka.quantities.information.data import *
from kuchka.quantities.information.data_rate import *
from kuchka.quantities.kinematics.acceleration import *
from kuchka.quantities.kinematics.angular_velocity import *
from kuchka.quantities.kinematics.velocity import *
from kuchka.quantities.length import *
from kuchka.quantities.logarithmic import *
from kuchka.quantities.luminous_intensity import *
from kuchka.quantities.mass import *
from kuchka.quantities.mechanics.density import *
from kuchka.quantities.mechanics.energy import *
from kuchka.quantities.mechanics.energy_density import *
from kuchka.quantities.mechanics.force import *
from kuchka.quantities.mechanics.power import *
from kuchka.quantities.mechanics.pressure import *
from kuchka.quantities.mechanics.torque import *
from kuchka.quantities.proportion import *
from kuchka.quantities.radiation.activity import *
from kuchka.quantities.temporal import *
from kuchka.quantities.thermal import *

__all__: list[str] = []
__all__ += amount.__all__
__all__ += angular.__all__
__all__ += base.__all__
__all__ += current.__all__
__all__ += electromagnetics.__all__
__all__ += geometry.__all__
__all__ += information.__all__
__all__ += kinematics.__all__
__all__ += length.__all__
__all__ += logarithmic.__all__
__all__ += luminous_intensity.__all__
__all__ += mass.__all__
__all__ += mechanics.__all__
__all__ += proportion.__all__
__all__ += radiation.__all__
__all__ += temporal.__all__
__all__ += thermal.__all__
