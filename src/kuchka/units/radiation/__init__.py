"""Unit constructors for radioactive Activity.

    from kuchka import Becquerel, Curie, Megabecquerel

    source = Megabecquerel(3.7)
    calibration = Curie(1)

`ACTIVITY_UNITS` maps a symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
"""

from __future__ import annotations

from kuchka.units.radiation import activity
from kuchka.units.radiation.activity import *

__all__: list[str] = []
__all__ += activity.__all__
