"""Unit constructors for radioactivity and the doses it deposits.

from kuchka import Becquerel, Gray, Roentgen, Sievert

source = Becquerel(3.7e6)
absorbed = Gray(0.002)
reading = Sievert(0.00012)
survey = Roentgen(0.005)
"""

from __future__ import annotations

from kuchka.units.radiation import absorbed_dose
from kuchka.units.radiation import absorbed_dose_rate
from kuchka.units.radiation import activity
from kuchka.units.radiation import activity_concentration
from kuchka.units.radiation import equivalent_dose
from kuchka.units.radiation import equivalent_dose_rate
from kuchka.units.radiation import exposure
from kuchka.units.radiation import exposure_rate
from kuchka.units.radiation import specific_activity
from kuchka.units.radiation import surface_activity
from kuchka.units.radiation.absorbed_dose import *
from kuchka.units.radiation.absorbed_dose_rate import *
from kuchka.units.radiation.activity import *
from kuchka.units.radiation.activity_concentration import *
from kuchka.units.radiation.equivalent_dose import *
from kuchka.units.radiation.equivalent_dose_rate import *
from kuchka.units.radiation.exposure import *
from kuchka.units.radiation.exposure_rate import *
from kuchka.units.radiation.specific_activity import *
from kuchka.units.radiation.surface_activity import *

__all__: list[str] = []
__all__ += absorbed_dose.__all__
__all__ += absorbed_dose_rate.__all__
__all__ += activity.__all__
__all__ += activity_concentration.__all__
__all__ += specific_activity.__all__
__all__ += surface_activity.__all__
__all__ += equivalent_dose.__all__
__all__ += equivalent_dose_rate.__all__
__all__ += exposure.__all__
__all__ += exposure_rate.__all__
