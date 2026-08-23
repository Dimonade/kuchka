"""Engineer-facing unit constructors, one module per physical dimension.

```python
from kuchka import Volt, Milliampere

voltage = Volt(4.2)
current = Milliampere(150)
power = voltage * current
```

Each quantity's canonical unit (the one arithmetic results come back in,
e.g. ``Voltage * Current`` yields a result expressed in ``Watt``)
is assigned onto the corresponding domain class from ``kuchka.quantities``
at the bottom of the module that owns that dimension.
"""

from __future__ import annotations

from kuchka.units.current import AMPERE
from kuchka.units.current import Ampere
from kuchka.units.current import KILOAMPERE
from kuchka.units.current import Kiloampere
from kuchka.units.current import MICROAMPERE
from kuchka.units.current import Microampere
from kuchka.units.current import MILLIAMPERE
from kuchka.units.current import Milliampere
from kuchka.units.power import KILOWATT
from kuchka.units.power import Kilowatt
from kuchka.units.power import MILLIWATT
from kuchka.units.power import Milliwatt
from kuchka.units.power import WATT
from kuchka.units.power import Watt
from kuchka.units.resistance import KILOOHM
from kuchka.units.resistance import Kiloohm
from kuchka.units.resistance import MEGAOHM
from kuchka.units.resistance import Megaohm
from kuchka.units.resistance import MILLIOHM
from kuchka.units.resistance import Milliohm
from kuchka.units.resistance import OHM
from kuchka.units.resistance import Ohm
from kuchka.units.voltage import KILOVOLT
from kuchka.units.voltage import Kilovolt
from kuchka.units.voltage import MICROVOLT
from kuchka.units.voltage import Microvolt
from kuchka.units.voltage import MILLIVOLT
from kuchka.units.voltage import Millivolt
from kuchka.units.voltage import VOLT
from kuchka.units.voltage import Volt

__all__: list[str] = [
    "AMPERE",
    "KILOAMPERE",
    "KILOOHM",
    "KILOVOLT",
    "KILOWATT",
    "MEGAOHM",
    "MICROAMPERE",
    "MICROVOLT",
    "MILLIAMPERE",
    "MILLIOHM",
    "MILLIVOLT",
    "MILLIWATT",
    "OHM",
    "VOLT",
    "WATT",
    "Ampere",
    "Kiloampere",
    "Kiloohm",
    "Kilovolt",
    "Kilowatt",
    "Megaohm",
    "Microampere",
    "Microvolt",
    "Milliampere",
    "Milliohm",
    "Millivolt",
    "Milliwatt",
    "Ohm",
    "Volt",
    "Watt",
]
