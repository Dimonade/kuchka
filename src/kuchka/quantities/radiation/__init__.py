"""Quantity types for radioactivity: Activity.

    from kuchka import Activity

`Activity` is a role of `Frequency`: the same dimension, counting decays per second.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package composes its own ``__all__`` from theirs, and `kuchka.quantities` composes
its own from this one's.
A new leaf module needs three lines here: its module import, its wildcard import, and
its ``__all__ +=``.
"""

from __future__ import annotations

from kuchka.quantities.radiation import activity
from kuchka.quantities.radiation.activity import *

__all__: list[str] = []
__all__ += activity.__all__
