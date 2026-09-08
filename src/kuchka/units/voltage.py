"""Voltage unit constructors: Microvolt, Millivolt, Volt, Kilovolt.

Each function here does the same thing: take a plain number, multiply it
by a fixed scale factor, and wrap it in :class:`~kuchka.quantities.Voltage`.

    from kuchka import Volt, Millivolt

    voltage = Volt(4.2) + Millivolt(200)

`VOLTAGE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application, e.g. a config file field written as
``{"value": "5", "unit": "mV"}``:

    from kuchka.units import VOLTAGE_UNITS

    magnitude, symbol = "5", "mV"
    voltage = VOLTAGE_UNITS[symbol](magnitude)
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import VOLTAGE
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.prefixes import KILO
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import Voltage

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

VOLT_NAME = "volt"
VOLT_SYMBOL = "V"

MICROVOLT = prefixed_unit(MICRO, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)
MILLIVOLT = prefixed_unit(MILLI, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)
VOLT = prefixed_unit(UNIT, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)
KILOVOLT = prefixed_unit(KILO, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)


Voltage._canonical_unit = VOLT  # noqa: SLF001 -- this module owns Voltage's canonical unit


def Microvolt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in microvolts."""
    return Voltage(to_decimal(value) * MICROVOLT.scale, MICROVOLT)


def Millivolt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in millivolts."""
    return Voltage(to_decimal(value) * MILLIVOLT.scale, MILLIVOLT)


def Volt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in volts."""
    return Voltage(to_decimal(value) * VOLT.scale, VOLT)


def Kilovolt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in kilovolts."""
    return Voltage(to_decimal(value) * KILOVOLT.scale, KILOVOLT)


VOLTAGE_UNITS: Mapping[str, Callable[[Numeric], Voltage]] = MappingProxyType(
    {
        MICROVOLT.symbol: Microvolt,
        MILLIVOLT.symbol: Millivolt,
        VOLT.symbol: Volt,
        KILOVOLT.symbol: Kilovolt,
    }
)

__all__ = [
    "KILOVOLT",
    "MICROVOLT",
    "MILLIVOLT",
    "VOLT",
    "VOLTAGE_UNITS",
    "Kilovolt",
    "Microvolt",
    "Millivolt",
    "Volt",
]
