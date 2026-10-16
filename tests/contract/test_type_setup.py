"""Every concrete quantity type, as assembled, is set up completely.

Each has slots and no per-instance dictionary, and a canonical unit of its own, of the
kind its shape displays and the dimension of the type, that stores the magnitude
unscaled.
The cases are the types the library defines, so a type added later is checked without
an edit here.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from tests.support.kinds import QUANTITY_TYPES
from tests.support.kinds import TYPE_IDS
from tests.support.kinds import sample_of


def test_the_concrete_types_are_discovered() -> None:
    assert len(QUANTITY_TYPES) > 25  # noqa: PLR2004 -- a floor, so discovery cannot silently empty
    assert len(QUANTITY_TYPES) < 30  # noqa: PLR2004 -- just so that I remember to bump it.


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_a_type_declares_slots_and_its_instances_have_no_dictionary(cls: type) -> None:
    assert "__slots__" in vars(cls)
    assert cls.__dictoffset__ == 0
    assert not hasattr(sample_of(cls), "__dict__")


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_a_type_binds_a_canonical_unit_that_stores_the_magnitude_unscaled(
    cls: type,
) -> None:
    assert "_canonical_unit" in vars(cls), (
        f"{cls.__name__} has no canonical unit bound by its unit module"
    )
    unit = cls._canonical_unit
    assert isinstance(unit, cls._unit_type)
    if hasattr(unit, "dimension"):
        assert unit.dimension == cls.dimension
    assert unit.scale == Fraction(1)
    assert getattr(unit, "offset", Fraction(0)) == Fraction(0)
    value = cls(Fraction(7, 3), unit)
    assert value.value_in(unit) == Fraction(7, 3)
    assert value.unit is unit
