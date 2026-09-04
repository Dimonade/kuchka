"""AmountOfSubstance unit constructors: Micromole, Millimole, Mole.

Each function here does the same thing: take a plain number, multiply it by a fixed
scale factor, and wrap it in :class:`~kuchka.quantities.AmountOfSubstance`.

    from kuchka import Mole, Millimole

    reagent = Mole(1) + Millimole(250)

`AMOUNT_OF_SUBSTANCE_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import AMOUNT_OF_SUBSTANCE
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import AmountOfSubstance
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

MICROMOLE = UnitDef("micromole", "\u00b5mol", Decimal("0.000001"), AMOUNT_OF_SUBSTANCE)
MILLIMOLE = UnitDef("millimole", "mmol", Decimal("0.001"), AMOUNT_OF_SUBSTANCE)
MOLE = UnitDef("mole", "mol", Decimal(1), AMOUNT_OF_SUBSTANCE)

AmountOfSubstance._canonical_unit = MOLE  # noqa: SLF001 -- this module owns AmountOfSubstance's canonical unit


def Micromole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in micromoles."""
    return AmountOfSubstance(to_decimal(value) * MICROMOLE.scale, MICROMOLE)


def Millimole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in millimoles."""
    return AmountOfSubstance(to_decimal(value) * MILLIMOLE.scale, MILLIMOLE)


def Mole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in moles."""
    return AmountOfSubstance(to_decimal(value) * MOLE.scale, MOLE)


AMOUNT_OF_SUBSTANCE_UNITS: Mapping[str, Callable[[Numeric], AmountOfSubstance]] = (
    MappingProxyType(
        {
            "umol": Micromole,
            "mmol": Millimole,
            "mol": Mole,
        }
    )
)
