"""Current unit constructors: Microampere, Milliampere, Ampere, Kiloampere.

Each function here does the same thing:
take a plain number, multiply it by a fixed scale factor, and wrap it in
:class:`~kuchka.quantities.Current`.

```python
from kuchka import Ampere, Milliampere

current = Ampere(1) - Milliampere(250)
```
"""

from __future__ import annotations

from decimal import Decimal

from kuchka.dimensions import CURRENT
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import Current
from kuchka.quantities import UnitDef

MICROAMPERE = UnitDef("microampere", "\u00b5A", Decimal("0.000001"), CURRENT)
MILLIAMPERE = UnitDef("milliampere", "mA", Decimal("0.001"), CURRENT)
AMPERE = UnitDef("ampere", "A", Decimal(1), CURRENT)
KILOAMPERE = UnitDef("kiloampere", "kA", Decimal(1000), CURRENT)

Current._canonical_unit = AMPERE  # noqa: SLF001 -- this module owns Current's canonical unit


def Microampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in microamperes."""
    return Current(to_decimal(value) * MICROAMPERE.scale, MICROAMPERE)


def Milliampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in milliamperes."""
    return Current(to_decimal(value) * MILLIAMPERE.scale, MILLIAMPERE)


def Ampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in amperes."""
    return Current(to_decimal(value) * AMPERE.scale, AMPERE)


def Kiloampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in kiloamperes."""
    return Current(to_decimal(value) * KILOAMPERE.scale, KILOAMPERE)
