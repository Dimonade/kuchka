"""Voltage unit constructors: Microvolt, Millivolt, Volt, Kilovolt.

Each function here does the same thing: take a plain number, multiply it
by a fixed scale factor, and wrap it in :class:`~kuchka.quantities.Voltage`.

    from kuchka import Volt, Millivolt

    voltage = Volt(4.2) + Millivolt(200)
"""

from __future__ import annotations

from decimal import Decimal

from kuchka.dimensions import VOLTAGE
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import UnitDef
from kuchka.quantities import Voltage

MICROVOLT = UnitDef("microvolt", "\u00b5V", Decimal("0.000001"), VOLTAGE)
MILLIVOLT = UnitDef("millivolt", "mV", Decimal("0.001"), VOLTAGE)
VOLT = UnitDef("volt", "V", Decimal(1), VOLTAGE)
KILOVOLT = UnitDef("kilovolt", "kV", Decimal(1000), VOLTAGE)

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
