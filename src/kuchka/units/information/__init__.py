"""Unit constructors for Data and DataRate: bits, bytes, and their rates.

    from kuchka import Byte, GigabitPerSecond, Mebibyte

    firmware = Mebibyte(64)
    link = GigabitPerSecond(1)
    record = Byte(96)

`DATA_UNITS` and `DATA_RATE_UNITS` each map a symbol to its constructor, for boundary
code that reads a unit as a string from outside the application.
Information is an axis of its own, so a data rate is not interchangeable with a
`Frequency`, a `SampleRate`, or a `BaudRate`.
"""

from __future__ import annotations

from kuchka.units.information import data
from kuchka.units.information import data_rate
from kuchka.units.information.data import *
from kuchka.units.information.data_rate import *

__all__: list[str] = []
__all__ += data.__all__
__all__ += data_rate.__all__
