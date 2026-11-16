"""Every quantity type validates what it is built from.

A magnitude is an exact `Fraction` handed over by a unit constructor, and a display
unit is a unit definition of the type's own kind.
The checks live in the shared base, so each type is tried against the same bad inputs.
What is specific to a shape (absolute zero, an affine unit) is tested with the type.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka import Voltage
from kuchka.units import current
from kuchka.units.electromagnetics import voltage
from tests.support.families import FAMILIES
from tests.support.families import FAMILY_IDS
from tests.support.kinds import QUANTITY_TYPES
from tests.support.kinds import TYPE_IDS
from tests.support.kinds import sample_of

NOT_A_FRACTION = (
    0.5,
    5,
    Decimal("0.5"),
    "5",
    None,
    True,
    [5],
    5j,
    voltage.Volt(5),
)
NOT_A_UNIT = (None, "V", 1, 0.5, object())


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_a_magnitude_that_is_not_a_fraction_is_rejected(cls: type) -> None:
    unit = sample_of(cls).unit
    for bad in NOT_A_FRACTION:
        with pytest.raises(InvalidMeasurementError, match="unit constructors"):
            cls(bad, unit)


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_a_display_unit_that_is_not_a_unit_is_rejected(cls: type) -> None:
    for bad in NOT_A_UNIT:
        with pytest.raises(InvalidMeasurementError, match="display unit"):
            cls(Fraction(1), bad)


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_a_linear_type_accepts_every_unit_of_its_table(family) -> None:
    for unit in family.units.units:
        built = family.quantity(Fraction(7, 3), unit)
        assert built.unit is unit
        assert built.magnitude == Fraction(7, 3)


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_a_linear_type_built_directly_equals_the_unit_constructor(family) -> None:
    built = family.quantity(Fraction(7), family.canonical_unit)
    assert built == family.canonical(7)


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_a_linear_type_rejects_units_that_are_not_its_own_kind(family) -> None:
    foreign = next(
        unit
        for other in FAMILIES
        for unit in other.units.units
        if unit.dimension != family.canonical_unit.dimension
    )
    from kuchka.units import thermal

    with pytest.raises(InvalidMeasurementError, match="display unit"):
        family.quantity(Fraction(1), thermal.KELVIN)
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        family.quantity(Fraction(1), foreign)


def test_the_rejection_names_what_was_given() -> None:
    with pytest.raises(InvalidMeasurementError, match="got float"):
        Voltage(0.5, voltage.VOLT)
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        Voltage(Fraction(1), current.AMPERE)
