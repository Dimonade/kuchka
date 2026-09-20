"""The generic quantity engine and the named engineering types built on it.

Application code should not need to read this package.

It exists so that ``Voltage``, ``Current``, ``Power``, ``Resistance``,
``TemperatureDelta``, and the rest of the vocabulary do not each have to hand-roll
their own arithmetic, conversion, and comparison logic:
they share one implementation (:class:`LinearQuantity`, in ``base.py``) and differ only
in their :class:`~kuchka.dimensions.Dimension` and, where relevant, their
multiplication and division overloads (``electrical.py``, ``thermal.py``).

Each leaf module owns a hand-written ``__all__`` naming exactly what it defines;
this package aggregates them with a wildcard import and derives its own ``__all__``
from whatever that leaves in scope, so adding a unit to an existing dimension never
requires touching this file.
"""

from __future__ import annotations

from kuchka.quantities.amount import *
from kuchka.quantities.angular import *
from kuchka.quantities.area import *
from kuchka.quantities.base import *
from kuchka.quantities.charge import *
from kuchka.quantities.density import *
from kuchka.quantities.electrical import *
from kuchka.quantities.energy import *
from kuchka.quantities.kinematics import *
from kuchka.quantities.length import *
from kuchka.quantities.luminous_intensity import *
from kuchka.quantities.mass import *
from kuchka.quantities.proportion import *
from kuchka.quantities.temporal import *
from kuchka.quantities.thermal import *
from kuchka.quantities.volume import *

__all__: list[str] = sorted(name for name in globals() if not name.startswith("_"))
