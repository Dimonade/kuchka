"""Conductance unit constructors: Microsiemens, Millisiemens, Siemens, Kilosiemens.

    from kuchka import Siemens, Millisiemens

    leakage = Microsiemens(2)
    sensor_reading = Millisiemens(5) + Microsiemens(200)

`Microsiemens` and `Millisiemens` are the two that actually show up most often in the
wild -- conductivity meters (water, soil) report in `\u00b5S/cm`, and general
electronics leakage/output-admittance figures land in the micro-to-milli range.

`Kilosiemens` is included for symmetry with `Resistance`'s own prefix span (a
`Kiloohm`-scale resistor has a `Millisiemens`-scale conductance, and a
`Milliohm`-scale one -- a busbar, a battery's internal resistance -- has a
`Kilosiemens`-scale conductance), even though it is rarer in practice than the small
end of the range.

`CONDUCTANCE_UNITS` maps each symbol to its constructor, for boundary code that reads
a unit as a string from outside the application.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import CONDUCTANCE
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.prefixes import KILO
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import Conductance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

SIEMENS_NAME = "siemens"
SIEMENS_SYMBOL = "S"

MICROSIEMENS = prefixed_unit(MICRO, SIEMENS_NAME, SIEMENS_SYMBOL, CONDUCTANCE)
MILLISIEMENS = prefixed_unit(MILLI, SIEMENS_NAME, SIEMENS_SYMBOL, CONDUCTANCE)
SIEMENS = prefixed_unit(UNIT, SIEMENS_NAME, SIEMENS_SYMBOL, CONDUCTANCE)
KILOSIEMENS = prefixed_unit(KILO, SIEMENS_NAME, SIEMENS_SYMBOL, CONDUCTANCE)


Conductance._canonical_unit = SIEMENS  # noqa: SLF001 -- this module owns Conductance's canonical unit


def Microsiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in microsiemens."""
    return Conductance(to_exact(value) * MICROSIEMENS.scale, MICROSIEMENS)


def Millisiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in millisiemens."""
    return Conductance(to_exact(value) * MILLISIEMENS.scale, MILLISIEMENS)


def Siemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in siemens."""
    return Conductance(to_exact(value) * SIEMENS.scale, SIEMENS)


def Kilosiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in kilosiemens."""
    return Conductance(to_exact(value) * KILOSIEMENS.scale, KILOSIEMENS)


CONDUCTANCE_UNITS: Mapping[str, Callable[[Numeric], Conductance]] = MappingProxyType(
    {
        MICROSIEMENS.symbol: Microsiemens,
        MILLISIEMENS.symbol: Millisiemens,
        SIEMENS.symbol: Siemens,
        KILOSIEMENS.symbol: Kilosiemens,
    }
)

__all__ = [
    "CONDUCTANCE_UNITS",
    "KILOSIEMENS",
    "MICROSIEMENS",
    "MILLISIEMENS",
    "SIEMENS",
    "Kilosiemens",
    "Microsiemens",
    "Millisiemens",
    "Siemens",
]
