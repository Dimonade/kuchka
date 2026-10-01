"""The class constructor of every quantity type is a validation boundary.

`Voltage`, `Temperature`, `Angle`, ... are exported from the top level for annotations
and `isinstance`, so calling them directly is possible for anyone.
Their constructors accept an exact `Fraction` magnitude in the quantity's canonical
unit plus a display unit of the right kind and dimension, and raise
`InvalidMeasurementError` for anything else.
Plain numbers in a particular unit go through the unit constructors (`Volt`,
`Celsius`, ...), which share this boundary.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

import pytest

from kuchka import Angle
from kuchka import Celsius
from kuchka import Instant
from kuchka import InvalidMeasurementError
from kuchka import LogarithmicRatio
from kuchka import Proportion
from kuchka import Temperature
from kuchka import Volt
from kuchka import Voltage
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.units import AMPERE
from kuchka.units import CELSIUS
from kuchka.units import DECIBEL
from kuchka.units import DEGREE
from kuchka.units import INSTANT_SECOND
from kuchka.units import KELVIN
from kuchka.units import MILLIAMPERE
from kuchka.units import PERCENT
from kuchka.units import RADIAN
from kuchka.units import RATIO
from kuchka.units import VOLT
from tests.quantity_families import ALL_UNITDEF_CASES
from tests.quantity_families import FAMILIES
from tests.quantity_families import FAMILY_IDS
from tests.quantity_families import QuantityFamily

if TYPE_CHECKING:
    from collections.abc import Iterator

    from kuchka.quantities.base import UnitDef

NOT_A_FRACTION = [
    0.5,
    5,
    Decimal("0.5"),
    "5",
    None,
    True,
    [5],
    5j,
    Volt(5),
]
NOT_A_FRACTION_IDS = [
    "float",
    "int",
    "decimal",
    "str",
    "none",
    "bool",
    "list",
    "complex",
    "quantity",
]

NOT_A_UNIT = [None, "V", 1, 0.5, object()]
NOT_A_UNIT_IDS = ["none", "str", "int", "float", "object"]


def _quantity_type(family: QuantityFamily) -> type:
    return type(family.canonical(1))


def _foreign_unit(family: QuantityFamily) -> UnitDef:
    """Return a unit definition of some other dimension than `family`'s."""
    dimension = family.canonical_unit.dimension
    for _, unit in ALL_UNITDEF_CASES:
        if unit.dimension != dimension:
            return unit
    raise AssertionError("no unit of a foreign dimension found")  # pragma: no cover


def _concrete_quantity_types(
    base: type = _ScalarStorage,
) -> Iterator[type]:
    """Yield every quantity type that declares its own dimension."""
    for subclass in base.__subclasses__():
        if "dimension" in vars(subclass):
            yield subclass
        yield from _concrete_quantity_types(subclass)


CONCRETE_TYPES = sorted(_concrete_quantity_types(), key=lambda cls: cls.__name__)


# Linear quantities: every registered family


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_accepts_fraction_and_canonical_unit(family) -> None:
    cls = _quantity_type(family)
    built = cls(Fraction(7, 3), family.canonical_unit)
    assert built.magnitude == Fraction(7, 3)
    assert built.unit is family.canonical_unit


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_class_constructor_and_unit_constructor_build_equal_values(family) -> None:
    cls = _quantity_type(family)
    assert cls(Fraction(7), family.canonical_unit) == family.canonical(7)


@pytest.mark.parametrize(
    ("family", "unit"),
    ALL_UNITDEF_CASES,
    ids=[f"{family.id}-{unit.symbol}" for family, unit in ALL_UNITDEF_CASES],
)
def test_accepts_every_unit_of_its_dimension(family, unit) -> None:
    cls = _quantity_type(family)
    assert cls(Fraction(1), unit).unit is unit


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
@pytest.mark.parametrize("bad", NOT_A_FRACTION, ids=NOT_A_FRACTION_IDS)
def test_rejects_a_magnitude_that_is_not_a_fraction(family, bad) -> None:
    cls = _quantity_type(family)
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        cls(bad, family.canonical_unit)


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
@pytest.mark.parametrize("bad", NOT_A_UNIT, ids=NOT_A_UNIT_IDS)
def test_rejects_a_display_unit_that_is_not_a_unit_definition(family, bad) -> None:
    cls = _quantity_type(family)
    with pytest.raises(InvalidMeasurementError, match="display unit"):
        cls(Fraction(1), bad)


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_rejects_an_affine_unit_for_a_linear_quantity(family) -> None:
    cls = _quantity_type(family)
    with pytest.raises(InvalidMeasurementError, match="display unit"):
        cls(Fraction(1), KELVIN)


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_rejects_a_display_unit_of_another_dimension(family) -> None:
    cls = _quantity_type(family)
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        cls(Fraction(1), _foreign_unit(family))


# Reported reproductions


def test_float_magnitude_is_rejected() -> None:
    with pytest.raises(InvalidMeasurementError, match="got float"):
        Voltage(0.5, AMPERE)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_float_magnitude_is_rejected_with_a_matching_unit() -> None:
    with pytest.raises(InvalidMeasurementError, match="got float"):
        Voltage(0.5, VOLT)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_display_unit_of_another_dimension_is_rejected() -> None:
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        Voltage(Fraction(1), MILLIAMPERE)


# Affine quantities


@pytest.mark.parametrize("unit", [KELVIN, CELSIUS], ids=["kelvin", "celsius"])
def test_temperature_accepts_fraction_and_affine_unit(unit) -> None:
    built = Temperature(Fraction(300), unit)
    assert built.kelvin == Fraction(300)
    assert built.unit is unit


@pytest.mark.parametrize("bad", NOT_A_FRACTION, ids=NOT_A_FRACTION_IDS)
def test_temperature_rejects_a_non_fraction_magnitude_with_a_library_error(bad) -> None:
    # The absolute-zero comparison must never see a value that is not a `Fraction`:
    # a bare `TypeError` from `<` would escape the library's error hierarchy.
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        Temperature(bad, KELVIN)


@pytest.mark.parametrize("bad", [VOLT, None, "K"], ids=["linear_unit", "none", "str"])
def test_temperature_rejects_a_display_unit_that_is_not_affine(bad) -> None:
    with pytest.raises(InvalidMeasurementError, match="display unit"):
        Temperature(Fraction(300), bad)


def test_temperature_validates_type_before_checking_absolute_zero() -> None:
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        Temperature(-1, KELVIN)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_temperature_below_absolute_zero_is_rejected_by_both_constructors() -> None:
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        Temperature(Fraction(-1), KELVIN)
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        Celsius(-300)


def test_instant_accepts_fraction_and_instant_unit() -> None:
    built = Instant(Fraction(5), INSTANT_SECOND)
    assert built.unit is INSTANT_SECOND
    assert built.value_in(INSTANT_SECOND) == Fraction(5)


@pytest.mark.parametrize("bad", NOT_A_FRACTION, ids=NOT_A_FRACTION_IDS)
def test_instant_rejects_a_non_fraction_magnitude(bad) -> None:
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        Instant(bad, INSTANT_SECOND)


def test_instant_rejects_a_linear_unit() -> None:
    with pytest.raises(InvalidMeasurementError, match="display unit"):
        Instant(Fraction(1), VOLT)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


# Modular quantities


@pytest.mark.parametrize("unit", [RADIAN, DEGREE], ids=["radian", "degree"])
def test_angle_accepts_fraction_and_angular_unit(unit) -> None:
    assert Angle(Fraction(1), unit).unit is unit


@pytest.mark.parametrize("bad", NOT_A_FRACTION, ids=NOT_A_FRACTION_IDS)
def test_angle_rejects_a_non_fraction_magnitude(bad) -> None:
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        Angle(bad, RADIAN)


def test_angle_rejects_a_unit_of_another_dimension() -> None:
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        Angle(Fraction(1), VOLT)


def test_angle_rejects_an_affine_unit() -> None:
    with pytest.raises(InvalidMeasurementError, match="display unit"):
        Angle(Fraction(1), KELVIN)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


# Logarithmic quantities


def test_logarithmic_ratio_accepts_fraction_and_logarithmic_unit() -> None:
    assert LogarithmicRatio(Fraction(3), DECIBEL).unit is DECIBEL


@pytest.mark.parametrize("bad", NOT_A_FRACTION, ids=NOT_A_FRACTION_IDS)
def test_logarithmic_ratio_rejects_a_non_fraction_magnitude(bad) -> None:
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        LogarithmicRatio(bad, DECIBEL)


@pytest.mark.parametrize("bad", [RATIO, VOLT, KELVIN], ids=["ratio", "volt", "kelvin"])
def test_logarithmic_ratio_rejects_a_non_logarithmic_unit(bad) -> None:
    # A linear `RATIO` is a ratio, not a level.
    with pytest.raises(InvalidMeasurementError, match="display unit"):
        LogarithmicRatio(Fraction(1), bad)


# Dimensionless quantities


@pytest.mark.parametrize("unit", [RATIO, PERCENT], ids=["ratio", "percent"])
def test_proportion_accepts_dimensionless_units(unit) -> None:
    assert Proportion(Fraction(1), unit).unit is unit


def test_proportion_rejects_a_dimensional_unit() -> None:
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        Proportion(Fraction(1), VOLT)


# Coverage of the type hierarchy


@pytest.mark.parametrize("cls", CONCRETE_TYPES, ids=lambda cls: cls.__name__)
def test_every_concrete_quantity_type_rejects_a_float_magnitude(cls) -> None:
    """Holds for any type added later, since the types are discovered, not listed."""
    unit = getattr(cls, "_canonical_unit", KELVIN)
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        cls(0.5, unit)


@pytest.mark.parametrize("cls", CONCRETE_TYPES, ids=lambda cls: cls.__name__)
def test_every_concrete_quantity_type_rejects_a_string_as_display_unit(cls) -> None:
    with pytest.raises(InvalidMeasurementError, match="display unit"):
        cls(Fraction(1), "unit")
