"""Unit constructors for information and its rate.

from kuchka import Byte
from kuchka import GigabitPerSecond
from kuchka import Mebibyte

firmware = Mebibyte(64)
link = GigabitPerSecond(1)
record = Byte(96)
"""

from __future__ import annotations

from kuchka.units.information import data
from kuchka.units.information import data_rate
from kuchka.units.information.data import *
from kuchka.units.information.data_rate import *

__all__: list[str] = []
__all__ += data.__all__
__all__ += data_rate.__all__
