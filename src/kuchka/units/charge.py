"""Charge unit constructors: Microcoulomb, Millicoulomb, Coulomb.

    from kuchka import Coulomb, Milliampere, Second

    dose = Milliampere(2) * Second(5)  # -> Charge, computed and typed automatically.

`CHARGE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import CHARGE
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import Charge
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

COULOMB = UnitDef("coulomb", "C", Decimal(1), CHARGE)

Charge._canonical_unit = COULOMB  # noqa: SLF001 -- this module owns Charge's canonical unit


def Coulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in coulombs."""
    return Charge(to_decimal(value) * COULOMB.scale, COULOMB)


# BEGIN GENERATED
MICROCOULOMB = UnitDef("microcoulomb", "µC", Decimal(10) ** -6, CHARGE)
MILLICOULOMB = UnitDef("millicoulomb", "mC", Decimal(10) ** -3, CHARGE)


def Microcoulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in microcoulombs."""
    return Charge(to_decimal(value) * MICROCOULOMB.scale, MICROCOULOMB)


def Millicoulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in millicoulombs."""
    return Charge(to_decimal(value) * MILLICOULOMB.scale, MILLICOULOMB)


GENERATED_CHARGE_UNITS: Mapping[str, Callable[[Numeric], Charge]] = MappingProxyType(
    {
        "µC": Microcoulomb,
        "mC": Millicoulomb,
    }
)
# END GENERATED

CHARGE_UNITS: Mapping[str, Callable[[Numeric], Charge]] = MappingProxyType(
    {
        "C": Coulomb,
        **GENERATED_CHARGE_UNITS,
    }
)
