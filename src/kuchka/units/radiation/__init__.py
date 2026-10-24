"""Unit constructors for radioactive activity.

    from kuchka import Becquerel, Curie, Megabecquerel

    source = Megabecquerel(3.7)
    calibration = Curie(1)

`ACTIVITY_UNITS` maps a symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package composes its own ``__all__`` from theirs, and `kuchka.units` composes its
own from this one's, so adding a unit to an existing dimension never touches either.
A new leaf module needs three lines here: its module import, its wildcard import, and
its ``__all__ +=``.
"""

from __future__ import annotations

from kuchka.units.radiation import activity
from kuchka.units.radiation.activity import *

__all__: list[str] = []
__all__ += activity.__all__
