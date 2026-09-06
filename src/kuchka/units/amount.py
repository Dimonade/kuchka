"""AmountOfSubstance unit constructors: Micromole, Millimole, Mole.

Each function here does the same thing: take a plain number, multiply it by a fixed
scale factor, and wrap it in :class:`~kuchka.quantities.AmountOfSubstance`.

    from kuchka import Mole, Millimole

    reagent = Mole(1) + Millimole(250)

`AMOUNT_OF_SUBSTANCE_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import AMOUNT_OF_SUBSTANCE
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import prefixed_unit
from kuchka.prefixes import UNIT
from kuchka.quantities import AmountOfSubstance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

MOLE_NAME = "mole"
MOLE_SYMBOL = "mol"

MICROMOLE = prefixed_unit(MICRO, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)
MILLIMOLE = prefixed_unit(MILLI, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)
MOLE = prefixed_unit(UNIT, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)


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
            MICROMOLE.symbol: Micromole,
            MILLIMOLE.symbol: Millimole,
            MOLE.symbol: Mole,
        }
    )
)
