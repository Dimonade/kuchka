"""Mass unit constructors: Nanogram, Microgram, Milligram, Gram, Kilogram, Megagram.

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

NOTE: `Tonne` is a plain alias for `Megagram`, not a second constructor:
a tonne and a megagram are the same quantity, and the common name (`Tonne`) is more
convenient to reach for than the SI-coherent one (`Megagram`) for most engineering use.
Aliasing keeps that convenience without introducing a second `UnitDef` for the same
scale -- `Tonne is Megagram` holds at the function level, so `Tonne(5)` and
`Megagram(5)` are identical `Mass` instances, including their displayed unit symbol
(`Mg`, not `t`).

`MASS_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import MASS
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.prefixes import KILO
from kuchka.prefixes import MEGA
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import NANO
from kuchka.prefixes import PICO
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import Mass

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

GRAM_NAME = "gram"
GRAM_SYMBOL = "g"


PICOGRAM = prefixed_unit(PICO, GRAM_NAME, GRAM_SYMBOL, MASS, coherent_offset=-3)
NANOGRAM = prefixed_unit(NANO, GRAM_NAME, GRAM_SYMBOL, MASS, coherent_offset=-3)
MICROGRAM = prefixed_unit(MICRO, GRAM_NAME, GRAM_SYMBOL, MASS, coherent_offset=-3)
MILLIGRAM = prefixed_unit(MILLI, GRAM_NAME, GRAM_SYMBOL, MASS, coherent_offset=-3)
GRAM = prefixed_unit(UNIT, GRAM_NAME, GRAM_SYMBOL, MASS, coherent_offset=-3)
KILOGRAM = prefixed_unit(KILO, GRAM_NAME, GRAM_SYMBOL, MASS, coherent_offset=-3)
MEGAGRAM = prefixed_unit(MEGA, GRAM_NAME, GRAM_SYMBOL, MASS, coherent_offset=-3)

Mass._canonical_unit = KILOGRAM  # noqa: SLF001 -- this module owns Mass's canonical unit


def Picogram(value: Numeric) -> Mass:
    """Construct a Mass from a magnitude expressed in picograms."""
    return Mass(to_decimal(value) * PICOGRAM.scale, PICOGRAM)


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


def Megagram(value: Numeric) -> Mass:
    """Construct a Mass from a magnitude expressed in megagrams."""
    return Mass(to_decimal(value) * MEGAGRAM.scale, MEGAGRAM)


Tonne = Megagram
"""A tonne is a megagram.

This name is the same function object as `Megagram`, so the two are interchangeable.
"""


MASS_UNITS: Mapping[str, Callable[[Numeric], Mass]] = MappingProxyType(
    {
        PICOGRAM.symbol: Picogram,
        NANOGRAM.symbol: Nanogram,
        MICROGRAM.symbol: Microgram,
        MILLIGRAM.symbol: Milligram,
        GRAM.symbol: Gram,
        KILOGRAM.symbol: Kilogram,
        MEGAGRAM.symbol: Megagram,
        "t": Tonne,
    }
)

__all__ = [
    "GRAM",
    "KILOGRAM",
    "MASS_UNITS",
    "MEGAGRAM",
    "MICROGRAM",
    "MILLIGRAM",
    "NANOGRAM",
    "PICOGRAM",
    "Gram",
    "Kilogram",
    "Megagram",
    "Microgram",
    "Milligram",
    "Nanogram",
    "Picogram",
    "Tonne",
]
