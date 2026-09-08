"""Power unit constructors: Milliwatt, Watt, Kilowatt.

Each function here does the same thing: take a plain number, multiply it
by a fixed scale factor, and wrap it in :class:`~kuchka.quantities.Power`.

    from kuchka import Watt

    power = Watt(5)

`POWER_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import POWER
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.prefixes import KILO
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import Power

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

WATT_NAME = "watt"
WATT_SYMBOL = "W"

MICROWATT = prefixed_unit(MICRO, WATT_NAME, WATT_SYMBOL, POWER)
MILLIWATT = prefixed_unit(MILLI, WATT_NAME, WATT_SYMBOL, POWER)
WATT = prefixed_unit(UNIT, WATT_NAME, WATT_SYMBOL, POWER)
KILOWATT = prefixed_unit(KILO, WATT_NAME, WATT_SYMBOL, POWER)


Power._canonical_unit = WATT  # noqa: SLF001 -- this module owns Power's canonical unit


def Microwatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in microwatts."""
    return Power(to_decimal(value) * MICROWATT.scale, MICROWATT)


def Milliwatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in milliwatts."""
    return Power(to_decimal(value) * MILLIWATT.scale, MILLIWATT)


def Watt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in watts."""
    return Power(to_decimal(value) * WATT.scale, WATT)


def Kilowatt(value: Numeric) -> Power:
    """Construct a Power from a magnitude expressed in kilowatts."""
    return Power(to_decimal(value) * KILOWATT.scale, KILOWATT)


POWER_UNITS: Mapping[str, Callable[[Numeric], Power]] = MappingProxyType(
    {
        MICROWATT.symbol: Microwatt,
        MILLIWATT.symbol: Milliwatt,
        WATT.symbol: Watt,
        KILOWATT.symbol: Kilowatt,
    }
)

__all__ = [
    "KILOWATT",
    "MICROWATT",
    "MILLIWATT",
    "POWER_UNITS",
    "WATT",
    "Kilowatt",
    "Microwatt",
    "Milliwatt",
    "Watt",
]
