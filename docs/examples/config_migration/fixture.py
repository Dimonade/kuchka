"""What the test fixture's hardware can do.

A limits file may narrow these ranges and never exceed them: the fixture cannot source
more than 100 mA, cannot drive beyond 5 V either way, and its climate chamber runs from
-40 °C to 85 °C.
Asking for more than that is a mistake in the file, so every rung of this example
refuses it.
"""

from __future__ import annotations

from kuchka import Celsius
from kuchka import Milliampere
from kuchka import Volt

MAX_VOLTAGE = Volt(5)
MAX_CURRENT = Milliampere(100)
MIN_TEMPERATURE = Celsius(-40)
MAX_TEMPERATURE = Celsius(85)
