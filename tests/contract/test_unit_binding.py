"""A unit belongs to the quantity types that display in it.

Each concrete type binds the units it displays in, from its own `*_UNITS` table, and
both its constructor and `.to()` refuse any other, including a unit of a type with the
same dimension.
The cases are the types and tables the library publishes, so a type added later is
checked without an edit here.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka.internal.unit_table import units_of
from tests.support.kinds import QUANTITY_TYPES
from tests.support.kinds import TYPE_IDS
from tests.support.kinds import UNIT_TABLES
from tests.support.kinds import sample_of


def bound_units(cls: type) -> tuple:
    """Return the units a type binds."""
    return cls._applicable_units


def unit_type(cls: type) -> type:
    """Return the kind of unit a type displays in."""
    return cls._unit_type


TABLE_OF = {
    type(next(iter(table.values()))(1)): table for table in UNIT_TABLES.values()
}
TABLED = sorted(TABLE_OF, key=lambda cls: cls.__name__)
TABLED_IDS = [cls.__name__ for cls in TABLED]
PAIRS = [
    (first, second)
    for first in QUANTITY_TYPES
    for second in QUANTITY_TYPES
    if first is not second and first.dimension == second.dimension
]
PAIR_IDS = [f"{a.__name__}-{b.__name__}" for a, b in PAIRS]


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_a_type_binds_units_of_its_own_kind_and_dimension(cls: type) -> None:
    assert "_applicable_units" in vars(cls), f"{cls.__name__} has no bound units"
    bound = bound_units(cls)
    assert bound
    for unit in bound:
        assert isinstance(unit, unit_type(cls))
        if hasattr(unit, "dimension"):
            assert unit.dimension == cls.dimension
    canonical = getattr(cls, "_canonical_unit", None)
    if canonical is not None:
        assert canonical in bound
    assert sample_of(cls).unit in bound


@pytest.mark.parametrize("cls", TABLED, ids=TABLED_IDS)
def test_the_table_of_a_type_builds_values_in_its_bound_units(cls: type) -> None:
    for constructor in TABLE_OF[cls].values():
        value = constructor(1)
        assert type(value) is cls
        assert value.unit in bound_units(cls)
    if cls.__name__ != "Instant":
        assert set(units_of(TABLE_OF[cls])) == set(bound_units(cls))


@pytest.mark.parametrize(("first", "second"), PAIRS, ids=PAIR_IDS)
def test_a_unit_only_the_other_type_displays_in_is_refused(
    first: type, second: type
) -> None:
    only_second = [
        unit
        for unit in bound_units(second)
        if unit not in bound_units(first) and isinstance(unit, unit_type(first))
    ]
    for unit in only_second:
        with pytest.raises(InvalidMeasurementError, match="is not a unit of"):
            first(Fraction(1), unit)


def test_the_types_sharing_a_dimension_are_found() -> None:
    names = {frozenset((a.__name__, b.__name__)) for a, b in PAIRS}
    assert frozenset(("Frequency", "BaudRate")) in names
    assert frozenset(("Frequency", "SampleRate")) in names
    assert frozenset(("Time", "SamplingPeriod")) in names
    assert frozenset(("Pressure", "EnergyDensity")) in names
