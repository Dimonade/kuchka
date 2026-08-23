"""Power unit constructors: Milliwatt, Watt, Kilowatt.

Each function here does the same thing:
take a plain number, multiply it by a fixed scale factor, and wrap it in
:class:`~kuchka.quantities.Power`.

```python
from kuchka import Watt

power = Watt(5)
```
"""

from __future__ import annotations

from decimal import Decimal

from kuchka.dimensions import POWER
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import Power
from kuchka.quantities import UnitDef

MILLIWATT = UnitDef("milliwatt", "mW", Decimal("0.001"), POWER)
WATT = UnitDef("watt", "W", Decimal(1), POWER)
KILOWATT = UnitDef("kilowatt", "kW", Decimal(1000), POWER)

Power._canonical_unit = WATT  # noqa: SLF001 -- this module owns Power's canonical unit


def Milliwatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in milliwatts."""
    return Power(to_decimal(value) * MILLIWATT.scale, MILLIWATT)


def Watt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in watts."""
    return Power(to_decimal(value) * WATT.scale, WATT)


def Kilowatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in kilowatts."""
    return Power(to_decimal(value) * KILOWATT.scale, KILOWATT)
