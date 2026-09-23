"""Unit constructors for Frequency: Hertz, Kilohertz, Megahertz.

    from kuchka import Hertz, Kilohertz

    rate = Hertz(500)
    carrier = Kilohertz(915)

`Hertz` is the canonical, SI-coherent unit -- the one arithmetic results (e.g.
`1 / Time`) come back expressed in.

`FREQUENCY_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import FREQUENCY
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.prefixes import GIGA
from kuchka.prefixes import KILO
from kuchka.prefixes import MEGA
from kuchka.prefixes import PETA
from kuchka.prefixes import TERA
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import Frequency

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

HERTZ_NAME = "hertz"
HERTZ_SYMBOL = "Hz"

HERTZ = prefixed_unit(UNIT, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
KILOHERTZ = prefixed_unit(KILO, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
MEGAHERTZ = prefixed_unit(MEGA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
GIGAHERTZ = prefixed_unit(GIGA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
TERAHERTZ = prefixed_unit(TERA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
PETAHERTZ = prefixed_unit(PETA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)


Frequency._canonical_unit = HERTZ  # noqa: SLF001 -- this module owns Frequency's canonical unit


def Hertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in hertz."""
    return Frequency(to_exact(value) * HERTZ.scale, HERTZ)


def Kilohertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in kilohertz."""
    return Frequency(to_exact(value) * KILOHERTZ.scale, KILOHERTZ)


def Megahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in megahertz."""
    return Frequency(to_exact(value) * MEGAHERTZ.scale, MEGAHERTZ)


def Gigahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in gigahertz."""
    return Frequency(to_exact(value) * GIGAHERTZ.scale, GIGAHERTZ)


def Terahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in terahertz."""
    return Frequency(to_exact(value) * TERAHERTZ.scale, TERAHERTZ)


def Petahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in petahertz."""
    return Frequency(to_exact(value) * PETAHERTZ.scale, PETAHERTZ)


FREQUENCY_UNITS: Mapping[str, Callable[[Numeric], Frequency]] = MappingProxyType(
    {
        HERTZ.symbol: Hertz,
        KILOHERTZ.symbol: Kilohertz,
        MEGAHERTZ.symbol: Megahertz,
        GIGAHERTZ.symbol: Gigahertz,
        TERAHERTZ.symbol: Terahertz,
        PETAHERTZ.symbol: Petahertz,
    }
)

__all__ = [
    "FREQUENCY_UNITS",
    "GIGAHERTZ",
    "HERTZ",
    "KILOHERTZ",
    "MEGAHERTZ",
    "PETAHERTZ",
    "TERAHERTZ",
    "Gigahertz",
    "Hertz",
    "Kilohertz",
    "Megahertz",
    "Petahertz",
    "Terahertz",
]
