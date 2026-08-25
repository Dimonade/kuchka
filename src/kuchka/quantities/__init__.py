"""The generic quantity engine and the named engineering types built on it.

Application code should not need to read this package.
It exists so that ``Voltage``, ``Current``, ``Power``, ``Resistance``, and
``TemperatureDelta`` do not each have to hand-roll their own arithmetic,
conversion, and comparison logic: they share one implementation
(:class:`LinearQuantity`, in ``base.py``) and differ only in their
:class:`~kuchka.dimensions.Dimension` and their multiplication/division
overloads (``electrical.py``, ``thermal.py``).
"""

from __future__ import annotations

from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import UnitDef
from kuchka.quantities.electrical import Current
from kuchka.quantities.electrical import Power
from kuchka.quantities.electrical import Resistance
from kuchka.quantities.electrical import Voltage
from kuchka.quantities.temporal import BaudRate
from kuchka.quantities.temporal import ConvertibleToFrequency
from kuchka.quantities.temporal import Frequency
from kuchka.quantities.temporal import SampleRate
from kuchka.quantities.temporal import SamplingPeriod
from kuchka.quantities.temporal import Time
from kuchka.quantities.thermal import TemperatureDelta

__all__: list[str] = [
    "BaudRate",
    "ConvertibleToFrequency",
    "Current",
    "Frequency",
    "LinearQuantity",
    "Power",
    "Resistance",
    "SampleRate",
    "SamplingPeriod",
    "TemperatureDelta",
    "Time",
    "UnitDef",
    "Voltage",
]
