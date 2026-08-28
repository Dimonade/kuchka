"""Resistance unit constructors: Milliohm, Ohm, Kiloohm, Megaohm.

Each function here does the same thing: take a plain number, multiply it
by a fixed scale factor, and wrap it in :class:`~kuchka.quantities.Resistance`.

    from kuchka import Ohm

    resistance = Ohm(100)

`RESISTANCE_UNITS` maps each symbol to its constructor, for boundary code that reads
 unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import RESISTANCE
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import Resistance
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

MILLIOHM = UnitDef("milliohm", "m\u03a9", Decimal("0.001"), RESISTANCE)
OHM = UnitDef("ohm", "\u03a9", Decimal(1), RESISTANCE)
KILOOHM = UnitDef("kiloohm", "k\u03a9", Decimal(1000), RESISTANCE)
MEGAOHM = UnitDef("megaohm", "M\u03a9", Decimal(1_000_000), RESISTANCE)

Resistance._canonical_unit = OHM  # noqa: SLF001 -- this module owns Resistance's canonical unit


def Milliohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in milliohms."""
    return Resistance(to_decimal(value) * MILLIOHM.scale, MILLIOHM)


def Ohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in ohms."""
    return Resistance(to_decimal(value) * OHM.scale, OHM)


def Kiloohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in kiloohms."""
    return Resistance(to_decimal(value) * KILOOHM.scale, KILOOHM)


def Megaohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in megaohms."""
    return Resistance(to_decimal(value) * MEGAOHM.scale, MEGAOHM)


RESISTANCE_UNITS: Mapping[str, Callable[[Numeric], Resistance]] = MappingProxyType(
    {
        "mOhm": Milliohm,
        "Ohm": Ohm,
        "kOhm": Kiloohm,
        "MOhm": Megaohm,
    }
)
