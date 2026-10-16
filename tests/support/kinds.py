"""Every concrete quantity type and published unit, discovered from the library."""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

import kuchka.units as published
from kuchka.internal.unit_table import UnitTable
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.quantities.base.units import _Unit
from kuchka.units import thermal

if TYPE_CHECKING:
    from collections.abc import Iterator


def _concrete(base: type = _ScalarStorage) -> Iterator[type]:
    for subclass in base.__subclasses__():
        if "dimension" in vars(subclass) and subclass.__module__.startswith("kuchka."):
            yield subclass
        yield from _concrete(subclass)


QUANTITY_TYPES: tuple[type, ...] = tuple(
    sorted(_concrete(), key=lambda cls: cls.__name__)
)
"""Every concrete quantity type, whatever its shape, discovered from the hierarchy."""

TYPE_IDS: tuple[str, ...] = tuple(cls.__name__ for cls in QUANTITY_TYPES)

UNIT_TABLES: dict[str, UnitTable] = {
    name: table
    for name in published.__all__
    if isinstance(table := getattr(published, name), UnitTable)
}
"""Every published `*_UNITS` table, whatever the shape of the quantity it builds."""

PUBLISHED_UNITS: dict[str, _Unit] = {
    name: unit
    for name in published.__all__
    if isinstance(unit := getattr(published, name), _Unit)
}
"""Every published unit constant, by its exported name."""


def sample_of(cls: type) -> _ScalarStorage:
    """Build one valid value of a concrete quantity type, in its canonical unit."""
    unit = getattr(cls, "_canonical_unit", thermal.KELVIN)
    return cls(Fraction(5), unit)  # type: ignore[no-any-return]
