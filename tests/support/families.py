"""The linear quantity families and their units, discovered from the published tables.

A family is a linear quantity type together with its `*_UNITS` table, so a property
written once runs against every linear type and every unit the library publishes.
Nothing here is listed by hand: a type or a unit added to the library joins the
families, and so joins every contract test, without an edit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import kuchka.units as published
from kuchka.internal.unit_table import UnitTable
from kuchka.quantities import LinearQuantity

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.numeric import Numeric
    from kuchka.quantities.base import UnitDef


@dataclass(frozen=True)
class Family:
    """One linear quantity type with the units its table publishes."""

    id: str
    quantity: type[LinearQuantity]
    units: UnitTable

    @property
    def definitions(self) -> dict[str, UnitDef]:
        """The unit definitions of the table, by display symbol."""
        return {unit.symbol: unit for unit in self.units.units}

    @property
    def canonical_unit(self) -> UnitDef:
        """The unit the magnitude of this type is stored in."""
        return self.quantity._canonical_unit  # noqa: SLF001 -- the type's own unit

    @property
    def canonical(self) -> Callable[[Numeric], LinearQuantity]:
        """The constructor of the canonical unit."""
        return self.units[self.canonical_unit.symbol]


@dataclass(frozen=True)
class UnitCase:
    """One unit of one family: its symbol, its constructor, and its definition."""

    family: Family
    symbol: str
    constructor: Callable[[Numeric], LinearQuantity]
    unit: UnitDef

    @property
    def id(self) -> str:
        """A readable test id, such as `length-km`."""
        return f"{self.family.id}-{self.symbol}"


def _published_tables() -> dict[str, UnitTable]:
    return {
        name: table
        for name in published.__all__
        if isinstance(table := getattr(published, name), UnitTable)
    }


def _discover() -> tuple[Family, ...]:
    families = []
    for name, table in _published_tables().items():
        quantity = type(next(iter(table.values()))(1))
        if issubclass(quantity, LinearQuantity):
            identifier = name.removesuffix("_UNITS").lower()
            families.append(Family(identifier, quantity, table))
    return tuple(sorted(families, key=lambda family: family.id))


FAMILIES: tuple[Family, ...] = _discover()
FAMILY_IDS: tuple[str, ...] = tuple(family.id for family in FAMILIES)

UNIT_CASES: tuple[UnitCase, ...] = tuple(
    UnitCase(family, symbol, constructor, family.definitions[symbol])
    for family in FAMILIES
    for symbol, constructor in family.units.items()
)
UNIT_CASE_IDS: tuple[str, ...] = tuple(case.id for case in UNIT_CASES)
