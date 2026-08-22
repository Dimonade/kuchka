"""Engineer-facing unit constructors.

Every function here does the same thing: take a plain number, multiply it by a fixed
scale factor, and wrap it in the right named type.
Nothing spectacular, but allows the IDE to jump to the definitions easily.

```python
from kuchka import Volt, Milliampere
voltage = Volt(4.2)
current = Milliampere(150)
power = voltage * current
```

Each quantity's canonical unit (the one arithmetic results come back in,
e.g. ``Voltage * Current`` yields a result expressed in ``Watt``) is
assigned onto the corresponding domain class from ``quantities.py`` at the
bottom of the relevant section below.
"""

from __future__ import annotations

from decimal import Decimal

from .dimensions import CURRENT, POWER, RESISTANCE, VOLTAGE
from .numeric import Numeric, to_decimal
from .quantities import Current, Power, Resistance, UnitDef, Voltage

# Voltage

MICROVOLT = UnitDef("microvolt", "\u00b5V", Decimal("0.000001"), VOLTAGE)
MILLIVOLT = UnitDef("millivolt", "mV", Decimal("0.001"), VOLTAGE)
VOLT = UnitDef("volt", "V", Decimal(1), VOLTAGE)
KILOVOLT = UnitDef("kilovolt", "kV", Decimal(1000), VOLTAGE)

Voltage._canonical_unit = VOLT


def Microvolt(value: Numeric) -> Voltage:
    return Voltage(to_decimal(value) * MICROVOLT.scale, MICROVOLT)


def Millivolt(value: Numeric) -> Voltage:
    return Voltage(to_decimal(value) * MILLIVOLT.scale, MILLIVOLT)


def Volt(value: Numeric) -> Voltage:
    return Voltage(to_decimal(value) * VOLT.scale, VOLT)


def Kilovolt(value: Numeric) -> Voltage:
    return Voltage(to_decimal(value) * KILOVOLT.scale, KILOVOLT)


# Current

MICROAMPERE = UnitDef("microampere", "\u00b5A", Decimal("0.000001"), CURRENT)
MILLIAMPERE = UnitDef("milliampere", "mA", Decimal("0.001"), CURRENT)
AMPERE = UnitDef("ampere", "A", Decimal(1), CURRENT)
KILOAMPERE = UnitDef("kiloampere", "kA", Decimal(1000), CURRENT)

Current._canonical_unit = AMPERE


def Microampere(value: Numeric) -> Current:
    return Current(to_decimal(value) * MICROAMPERE.scale, MICROAMPERE)


def Milliampere(value: Numeric) -> Current:
    return Current(to_decimal(value) * MILLIAMPERE.scale, MILLIAMPERE)


def Ampere(value: Numeric) -> Current:
    return Current(to_decimal(value) * AMPERE.scale, AMPERE)


def Kiloampere(value: Numeric) -> Current:
    return Current(to_decimal(value) * KILOAMPERE.scale, KILOAMPERE)


# Resistance

MILLIOHM = UnitDef("milliohm", "m\u03a9", Decimal("0.001"), RESISTANCE)
OHM = UnitDef("ohm", "\u03a9", Decimal(1), RESISTANCE)
KILOOHM = UnitDef("kiloohm", "k\u03a9", Decimal(1000), RESISTANCE)
MEGAOHM = UnitDef("megaohm", "M\u03a9", Decimal(1_000_000), RESISTANCE)

Resistance._canonical_unit = OHM


def Milliohm(value: Numeric) -> Resistance:
    return Resistance(to_decimal(value) * MILLIOHM.scale, MILLIOHM)


def Ohm(value: Numeric) -> Resistance:
    return Resistance(to_decimal(value) * OHM.scale, OHM)


def Kiloohm(value: Numeric) -> Resistance:
    return Resistance(to_decimal(value) * KILOOHM.scale, KILOOHM)


def Megaohm(value: Numeric) -> Resistance:
    return Resistance(to_decimal(value) * MEGAOHM.scale, MEGAOHM)


# Power

MILLIWATT = UnitDef("milliwatt", "mW", Decimal("0.001"), POWER)
WATT = UnitDef("watt", "W", Decimal(1), POWER)
KILOWATT = UnitDef("kilowatt", "kW", Decimal(1000), POWER)

Power._canonical_unit = WATT


def Milliwatt(value: Numeric) -> Power:
    return Power(to_decimal(value) * MILLIWATT.scale, MILLIWATT)


def Watt(value: Numeric) -> Power:
    return Power(to_decimal(value) * WATT.scale, WATT)


def Kilowatt(value: Numeric) -> Power:
    return Power(to_decimal(value) * KILOWATT.scale, KILOWATT)
