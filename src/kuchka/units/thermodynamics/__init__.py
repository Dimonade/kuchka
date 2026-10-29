"""Unit constructors for how heat changes a temperature.

from kuchka import CelsiusPerMinute, KelvinPerSecond

ramp = CelsiusPerMinute(5)
cooling = KelvinPerSecond(-0.2)
"""

from __future__ import annotations

from kuchka.units.thermodynamics import heating_rate
from kuchka.units.thermodynamics.heating_rate import *

__all__: list[str] = []
__all__ += heating_rate.__all__
