"""Quantity types for radioactivity: Activity.

    from kuchka import Activity

`Activity` is a role of `Frequency`: the same dimension, counting decays per second.
"""

from __future__ import annotations

from kuchka.quantities.radiation import activity
from kuchka.quantities.radiation.activity import *

__all__: list[str] = []
__all__ += activity.__all__
