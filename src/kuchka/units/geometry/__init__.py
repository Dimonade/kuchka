"""Unit constructors for the measures built from length alone: Area and Volume.

    from kuchka import SquareMetre, Litre

    floor = SquareMetre(12)
    tank = Litre(250)

`AREA_UNITS` and `VOLUME_UNITS` each map a symbol to its constructor, for boundary code
that reads a unit as a string from outside the application.
Area and volume are the length-derived dimensions that pressure, density, and the other
themed packages build on.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package composes its own ``__all__`` from theirs, and `kuchka.units` composes its
own from this one's, so adding a unit to an existing dimension never touches either.
A new leaf module needs three lines here: its module import, its wildcard import, and
its ``__all__ +=``.
"""

from __future__ import annotations

from kuchka.units.geometry import area
from kuchka.units.geometry import volume
from kuchka.units.geometry.area import *
from kuchka.units.geometry.volume import *

__all__: list[str] = []
__all__ += area.__all__
__all__ += volume.__all__
