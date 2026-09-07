"""The generic quantity engine and the named engineering types built on it.

Application code should not need to read this package.

It exists so that ``Voltage``, ``Current``, ``Power``, ``Resistance``,
``TemperatureDelta``, and the rest of the vocabulary do not each have to hand-roll
their own arithmetic, conversion, and comparison logic:
they share one implementation (:class:`LinearQuantity`, in ``base.py``) and differ only
in their :class:`~kuchka.dimensions.Dimension` and, where relevant, their
multiplication and division overloads (``electrical.py``, ``thermal.py``).
"""

from __future__ import annotations

from kuchka.quantities.amount import AmountOfSubstance
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import UnitDef
from kuchka.quantities.charge import Charge
from kuchka.quantities.electrical import Current
from kuchka.quantities.electrical import Power
from kuchka.quantities.electrical import Resistance
from kuchka.quantities.electrical import Voltage
from kuchka.quantities.energy import Energy
from kuchka.quantities.kinematics import Velocity
from kuchka.quantities.length import Length
from kuchka.quantities.luminous_intensity import LuminousIntensity
from kuchka.quantities.mass import Mass
from kuchka.quantities.proportion import Proportion
from kuchka.quantities.temporal import BaudRate
from kuchka.quantities.temporal import ConvertibleToFrequency
from kuchka.quantities.temporal import Frequency
from kuchka.quantities.temporal import SampleRate
from kuchka.quantities.temporal import SamplingPeriod
from kuchka.quantities.temporal import Time
from kuchka.quantities.thermal import AffineUnitDef
from kuchka.quantities.thermal import Temperature
from kuchka.quantities.thermal import TemperatureDelta


__all__: list[str] = [
    "AffineUnitDef",
    "AmountOfSubstance",
    "BaudRate",
    "Charge",
    "ConvertibleToFrequency",
    "Current",
    "Energy",
    "Frequency",
    "Length",
    "LinearQuantity",
    "LuminousIntensity",
    "Mass",
    "Power",
    "Proportion",
    "Resistance",
    "SampleRate",
    "SamplingPeriod",
    "Temperature",
    "TemperatureDelta",
    "Time",
    "UnitDef",
    "Velocity",
    "Voltage",
]
