"""Mass unit constructors: Nanogram, Microgram, Milligram, Gram, Kilogram.

Each function here does the same thing: take a plain number, multiply it by a fixed
scale factor, and wrap it in :class:`~kuchka.quantities.Mass`.

    from kuchka import Kilogram, Milligram

    payload = Kilogram(2) + Milligram(500)

Kilogram, not Gram, is the canonical unit here (`scale = Decimal(1)`):
the kilogram is the SI base unit for mass, so every other constructor in this module
scales relative to it, the same way every other family's constructors scale relative
to their own SI base or coherent unit.

This makes Mass the one family whose canonical unit already carries an SI prefix in its
own name.

`MASS_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import MASS
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import Mass
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

NANOGRAM = UnitDef("nanogram", "ng", Decimal("0.000000000001"), MASS)
MICROGRAM = UnitDef("microgram", "\u00b5g", Decimal("0.000000001"), MASS)
MILLIGRAM = UnitDef("milligram", "mg", Decimal("0.000001"), MASS)
GRAM = UnitDef("gram", "g", Decimal("0.001"), MASS)
KILOGRAM = UnitDef("kilogram", "kg", Decimal(1), MASS)

Mass._canonical_unit = KILOGRAM  # noqa: SLF001 -- this module owns Mass's canonical unit


def Nanogram(value: Numeric) -> Mass:
    """Construct a Mass from a magnitude expressed in nanograms."""
    return Mass(to_decimal(value) * NANOGRAM.scale, NANOGRAM)


def Microgram(value: Numeric) -> Mass:
    """Construct a Mass from a magnitude expressed in micrograms."""
    return Mass(to_decimal(value) * MICROGRAM.scale, MICROGRAM)


def Milligram(value: Numeric) -> Mass:
    """Construct a Mass from a magnitude expressed in milligrams."""
    return Mass(to_decimal(value) * MILLIGRAM.scale, MILLIGRAM)


def Gram(value: Numeric) -> Mass:
    """Construct a Mass from a magnitude expressed in grams."""
    return Mass(to_decimal(value) * GRAM.scale, GRAM)


def Kilogram(value: Numeric) -> Mass:
    """Construct a Mass from a magnitude expressed in kilograms."""
    return Mass(to_decimal(value) * KILOGRAM.scale, KILOGRAM)


MASS_UNITS: Mapping[str, Callable[[Numeric], Mass]] = MappingProxyType(
    {
        "ng": Nanogram,
        "ug": Microgram,
        "mg": Milligram,
        "g": Gram,
        "kg": Kilogram,
    }
)
