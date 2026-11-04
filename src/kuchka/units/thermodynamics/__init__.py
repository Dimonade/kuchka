"""Unit constructors for how heat changes a temperature.

from kuchka import CelsiusPerMinute, JoulePerKelvin, KilojoulePerKilogramKelvin

ramp = CelsiusPerMinute(5)
kettle = JoulePerKelvin(1200)
water = KilojoulePerKilogramKelvin(4.184)
"""

from __future__ import annotations

from kuchka.units.thermodynamics import entropy
from kuchka.units.thermodynamics import heat_capacity
from kuchka.units.thermodynamics import heating_rate
from kuchka.units.thermodynamics import specific_entropy
from kuchka.units.thermodynamics import specific_heat_capacity
from kuchka.units.thermodynamics.entropy import *
from kuchka.units.thermodynamics.heat_capacity import *
from kuchka.units.thermodynamics.heating_rate import *
from kuchka.units.thermodynamics.specific_entropy import *
from kuchka.units.thermodynamics.specific_heat_capacity import *

__all__: list[str] = []
__all__ += entropy.__all__
__all__ += heat_capacity.__all__
__all__ += heating_rate.__all__
__all__ += specific_entropy.__all__
__all__ += specific_heat_capacity.__all__
