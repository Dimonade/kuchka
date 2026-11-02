"""Unit constructors for radioactivity and the doses it deposits.

from kuchka import Becquerel, Gray, Roentgen, Sievert

source = Becquerel(3.7e6)
absorbed = Gray(0.002)
reading = Sievert(0.00012)
survey = Roentgen(0.005)
"""

from __future__ import annotations

from kuchka.units.radiation import absorbed_dose
from kuchka.units.radiation import activity
from kuchka.units.radiation import equivalent_dose
from kuchka.units.radiation import exposure
from kuchka.units.radiation.absorbed_dose import *
from kuchka.units.radiation.activity import *
from kuchka.units.radiation.equivalent_dose import *
from kuchka.units.radiation.exposure import *

__all__: list[str] = []
__all__ += absorbed_dose.__all__
__all__ += activity.__all__
__all__ += equivalent_dose.__all__
__all__ += exposure.__all__
