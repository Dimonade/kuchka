"""Unit constructors for BaudRate: a symbol rate, e.g. a UART's configured baud rate.

    from kuchka import Baud

    uart_rate = Baud(9600)

`BaudRate` is dimensionally identical to `Frequency` but is not interchangeable with it
or with `SampleRate`.

`BAUD_RATE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import FREQUENCY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import BaudRate
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

BAUD = UnitDef("baud", "Bd", Decimal(1), FREQUENCY)
KILOBAUD = UnitDef("kilobaud", "kBd", Decimal(1000), FREQUENCY)

BaudRate._canonical_unit = BAUD  # noqa: SLF001 -- this module owns BaudRate's canonical unit


def Baud(value: Numeric) -> BaudRate:
    """Construct a BaudRate from a magnitude expressed in baud."""
    return BaudRate(to_exact(value) * BAUD.scale, BAUD)


def Kilobaud(value: Numeric) -> BaudRate:
    """Construct a BaudRate from a magnitude expressed in kilobaud."""
    return BaudRate(to_exact(value) * KILOBAUD.scale, KILOBAUD)


BAUD_RATE_UNITS: Mapping[str, Callable[[Numeric], BaudRate]] = unit_table(
    "BAUD_RATE_UNITS",
    {
        BAUD: Baud,
        KILOBAUD: Kilobaud,
    },
)

__all__ = [
    "BAUD",
    "BAUD_RATE_UNITS",
    "KILOBAUD",
    "Baud",
    "Kilobaud",
]
