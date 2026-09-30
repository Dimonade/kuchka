"""LogarithmicRatio: decibel and bel levels, exact level arithmetic, ratio conversion.

A level is the logarithm of a ratio, stored as an exact `Fraction`.
Everything that combines, scales, orders, or re-expresses levels is exact.
Only the conversion to or from a linear ratio evaluates a logarithm, and that runs in
`Decimal` at the active context precision.
"""

from __future__ import annotations

import copy
import pickle
from decimal import Decimal
from decimal import localcontext
from fractions import Fraction
from typing import TYPE_CHECKING
from typing import ClassVar

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kuchka import Bel
from kuchka import Decibel
from kuchka import IncompatibleDimensionError
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import LogarithmicRatio
from kuchka import Percent
from kuchka import Proportion
from kuchka import Ratio
from kuchka import Volt
from kuchka.dimensions import DIMENSIONLESS
from kuchka.quantities.base import LogarithmicUnitDef
from kuchka.quantities.base import PureLogarithmicQuantity
from kuchka.units import BEL
from kuchka.units import DECIBEL
from kuchka.units import LOGARITHMIC_RATIO_UNITS
from kuchka.units import PERCENT
from kuchka.units import RATIO
from tests.quantity_families import BINARY_IMPRECISE_TRIPLES

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension

LEVELS = st.decimals(
    allow_nan=False,
    allow_infinity=False,
    min_value=Decimal(-300),
    max_value=Decimal(300),
    places=3,
)
"""Levels from -300 dB to +300 dB in millibel steps: ratios up to 1e30 (power)."""

RELATIVE_TOLERANCE = Fraction(1, 10**24)
"""Slack for comparing two `Decimal`-evaluated ratios, well above 28-digit rounding."""


class _OtherLogarithmicQuantity(PureLogarithmicQuantity):
    """A second concrete level type, for exercising the exact-type guards."""

    dimension: ClassVar[Dimension] = DIMENSIONLESS
    __slots__ = ()


def _relatively_close(a: Fraction, b: Fraction) -> bool:
    return abs(a - b) <= RELATIVE_TOLERANCE * abs(b)


# Construction and units.


def test_decibel_is_canonical_and_stored_exactly():
    assert Decibel(3).magnitude == Fraction(3)
    assert Decibel(0.1).magnitude == Fraction(1, 10)


def test_bel_is_ten_decibels():
    assert Bel(1) == Decibel(10)
    assert Bel(1).magnitude == Fraction(10)
    assert Bel(0.35) == Decibel(3.5)


def test_constructors_return_logarithmic_ratio():
    assert isinstance(Decibel(3), LogarithmicRatio)
    assert isinstance(Bel(3), LogarithmicRatio)
    assert isinstance(Decibel(3), PureLogarithmicQuantity)


def test_dimension_is_dimensionless():
    assert LogarithmicRatio.dimension == DIMENSIONLESS


@pytest.mark.parametrize("constructor", [Decibel, Bel])
@pytest.mark.parametrize(
    "bad",
    [True, "3", None, float("nan"), float("inf"), Decimal("NaN")],
    ids=["bool", "str", "none", "nan", "inf", "decimal-nan"],
)
def test_constructors_reject_non_numeric_input(constructor, bad):
    with pytest.raises(InvalidMeasurementError):
        constructor(bad)


def test_logarithmic_unit_def_is_its_own_type():
    assert isinstance(DECIBEL, LogarithmicUnitDef)
    assert isinstance(BEL, LogarithmicUnitDef)
    assert DECIBEL.scale == Fraction(1)
    assert BEL.scale == Fraction(10)
    assert repr(DECIBEL) == "LogarithmicUnitDef('decibel', 'dB')"


def test_units_table_resolves_every_symbol():
    assert LOGARITHMIC_RATIO_UNITS["dB"](3) == Decibel(3)
    assert LOGARITHMIC_RATIO_UNITS["B"](1) == Bel(1)
    assert set(LOGARITHMIC_RATIO_UNITS) == {"dB", "B"}


# Display and conversion between units.


def test_repr_shows_value_and_display_unit():
    assert repr(Decibel(3)) == "3 dB"
    assert repr(Decibel(-3.5)) == "-3.5 dB"
    assert repr(Bel(2)) == "2 B"


def test_format_spec_applies_to_the_display_value():
    assert f"{Decibel(3.14159):.2f}" == "3.14 dB"
    assert f"{Decibel(3)}" == "3 dB"


def test_to_changes_only_the_display_unit():
    level = Decibel(35).to(BEL)
    assert level == Decibel(35)
    assert level.unit is BEL
    assert repr(level) == "3.5 B"
    assert level.value_in(DECIBEL) == Fraction(35)
    assert level.value_in(BEL) == Fraction(7, 2)


def test_to_rejects_a_dimensionless_unit_of_another_kind():
    """`PERCENT` and `RATIO` are dimensionless too, but they are not levels."""
    with pytest.raises(InvalidConversionError, match="logarithmic unit"):
        Decibel(3).to(PERCENT)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    with pytest.raises(InvalidConversionError):
        Decibel(3).to(RATIO)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_to_rejects_a_string():
    with pytest.raises(InvalidConversionError):
        Decibel(3).to("dB")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


# Level arithmetic: exact, in the log domain.


def test_cascaded_stages_add_their_levels():
    chain = Decibel(20) + Decibel(-3.5) + Decibel(-1.5)
    assert chain == Decibel(15)


def test_addition_is_exact_where_binary_floats_are_not():
    for a, b, total in BINARY_IMPRECISE_TRIPLES:
        assert Decibel(a) + Decibel(b) == Decibel(total)


def test_subtraction_divides_the_ratios():
    assert Decibel(20) - Decibel(3) == Decibel(17)


def test_units_mix_freely_and_the_left_operand_sets_the_display_unit():
    assert Decibel(10) + Bel(1) == Decibel(20)
    total = Bel(1) + Decibel(10)
    assert total == Bel(2)
    assert total.unit is BEL
    assert (Decibel(20) - Bel(1)).unit is DECIBEL


def test_negation_is_the_reciprocal_ratio():
    assert -Decibel(3) == Decibel(-3)
    assert Decibel(3) + (-Decibel(3)) == Decibel(0)
    assert (-Decibel(3)).unit is DECIBEL


def test_absolute_value_is_the_size_of_a_deviation():
    assert abs(Decibel(-0.4)) == Decibel(0.4)
    assert abs(Decibel(0.4)) == Decibel(0.4)
    measured, expected = Decibel(20.3), Decibel(20)
    assert abs(measured - expected) <= Decibel(0.5)
    assert abs(Decibel(19.4) - expected) > Decibel(0.5)


def test_scaling_by_a_plain_number():
    assert Decibel(-0.2) * 30 == Decibel(-6)
    assert 30 * Decibel(-0.2) == Decibel(-6)
    assert Decibel(-6) / 30 == Decibel(-0.2)
    assert Decibel(3) * Decimal("0.5") == Decibel(1.5)
    assert Decibel(3) * Fraction(1, 3) == Decibel(1)


def test_scaling_keeps_the_display_unit():
    assert (Bel(2) * 3).unit is BEL


def test_level_divided_by_level_is_a_plain_fraction():
    assert Decibel(6) / Decibel(3) == Fraction(2)
    assert Bel(1) / Decibel(5) == Fraction(2)
    assert isinstance(Decibel(6) / Decibel(3), Fraction)


def test_sum_needs_a_level_as_its_start_value():
    assert sum([Decibel(1), Decibel(2)], start=Decibel(0)) == Decibel(3)
    with pytest.raises(InvalidMeasurementError):
        sum([Decibel(1), Decibel(2)])  # type: ignore[list-item]  # ty: ignore[no-matching-overload]


# Rejected operations.


def test_naked_number_addition_and_subtraction_are_rejected():
    with pytest.raises(InvalidMeasurementError, match=r"e\.g\. Decibel\(3\)"):
        Decibel(3) + 3  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        3 + Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(InvalidMeasurementError, match="subtract"):
        Decibel(3) - 3  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_level_times_level_is_a_type_error():
    with pytest.raises(TypeError):
        Decibel(3) * Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_number_divided_by_a_level_is_a_type_error():
    with pytest.raises(TypeError):
        2 / Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_level_is_not_a_linear_quantity_and_does_not_mix_with_one():
    with pytest.raises(TypeError):
        Decibel(3) + Ratio(2)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(TypeError):
        Ratio(2) + Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(TypeError):
        Decibel(3) * Volt(1)


def test_bool_scalar_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="bool"):
        Decibel(3) * True


def test_unsupported_scalar_types_are_type_errors():
    with pytest.raises(TypeError):
        Decibel(3) * "2"  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(TypeError):
        Decibel(3) / "2"  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Decibel(3) / 0
    with pytest.raises(ZeroDivisionError):
        Decibel(3) / Decibel(0)


def test_two_distinct_level_types_do_not_combine():
    other = _OtherLogarithmicQuantity(Fraction(3), DECIBEL)
    for operation in (
        lambda: Decibel(3) + other,  # type: ignore[operator]
        lambda: other + Decibel(3),  # type: ignore[operator]
        lambda: Decibel(3) - other,  # type: ignore[operator]
        lambda: Decibel(3) / other,  # type: ignore[operator]
    ):
        with pytest.raises(IncompatibleDimensionError, match="distinct concepts"):
            operation()


# Equality, hashing, ordering.


def test_equality_compares_the_level_across_units():
    assert Bel(0.3) == Decibel(3)
    assert Decibel(3) != Decibel(3.001)


def test_equal_levels_hash_equally():
    assert hash(Bel(1)) == hash(Decibel(10))
    assert {Bel(1), Decibel(10), Decibel(20)} == {Decibel(10), Decibel(20)}


def test_a_level_never_equals_a_linear_ratio():
    assert Decibel(0) != Ratio(1)
    assert Decibel(3) != Ratio(3)
    plain_number = 3
    assert Decibel(3) != plain_number


def test_ordering_follows_the_level():
    assert Decibel(-3) < Decibel(0) < Decibel(3)
    assert Bel(1) > Decibel(9)
    assert Bel(1) >= Decibel(10)
    assert Decibel(-10) <= Bel(-1)
    assert sorted([Decibel(3), Decibel(-6), Bel(0.5)]) == [
        Decibel(-6),
        Decibel(3),
        Decibel(5),
    ]


def test_comparing_with_a_linear_ratio_is_a_dimension_error():
    with pytest.raises(IncompatibleDimensionError, match="distinct concepts"):
        Decibel(3) < Ratio(2)  # noqa: B015  # type: ignore[operator]


# Copy and pickle.


def test_copy_and_pickle_round_trip_and_keep_the_display_unit():
    original = Bel(2)
    for restored in (
        copy.copy(original),
        copy.deepcopy(original),
        pickle.loads(pickle.dumps(original)),
    ):
        assert restored == original
        assert restored.unit.symbol == "B"


def test_instances_are_immutable():
    level = Decibel(3)
    with pytest.raises(AttributeError, match="immutable"):
        level._magnitude = Fraction(4)  # noqa: SLF001  # type: ignore[misc]


# Conversion to a linear ratio.


@pytest.mark.parametrize(
    ("level", "power", "field"),
    [
        (0, Decimal(1), Decimal(1)),
        (10, Decimal(10), None),
        (20, Decimal(100), Decimal(10)),
        (30, Decimal(1000), None),
        (40, Decimal(10_000), Decimal(100)),
        (-10, Decimal("0.1"), None),
        (-20, Decimal("0.01"), Decimal("0.1")),
        (-40, Decimal("0.0001"), Decimal("0.01")),
    ],
)
def test_whole_decades_convert_exactly(level, power, field):
    assert Decibel(level).as_power_ratio() == Ratio(power)
    if field is not None:
        assert Decibel(level).as_field_ratio() == Ratio(field)


def test_conversion_result_is_a_proportion_in_the_ratio_unit():
    ratio = Decibel(30).as_power_ratio()
    assert isinstance(ratio, Proportion)
    assert ratio.unit is RATIO
    assert Decibel(-20).as_field_ratio() == Percent(10)


def test_three_decibels_is_close_to_a_factor_of_two_but_not_exactly():
    power = Decibel(3).as_power_ratio()
    assert power != Ratio(2)
    assert float(power.magnitude) == pytest.approx(1.9952623149688795, rel=1e-15)


def test_six_decibels_of_voltage_is_the_same_ratio_as_three_of_power():
    assert Decibel(6).as_field_ratio() == Decibel(3).as_power_ratio()


def test_conversion_precision_follows_the_decimal_context():
    with localcontext() as context:
        context.prec = 10
        assert Decibel(3).as_power_ratio() == Ratio(Decimal("1.995262315"))


def test_bel_display_unit_does_not_change_the_ratio():
    assert Bel(3).as_power_ratio() == Decibel(30).as_power_ratio()


@pytest.mark.parametrize("level", [10**9, -(10**9)], ids=["overflow", "underflow"])
def test_levels_beyond_the_decimal_range_are_rejected(level):
    with pytest.raises(InvalidMeasurementError, match="outside the range"):
        Decibel(level).as_power_ratio()
    with pytest.raises(InvalidMeasurementError, match="outside the range"):
        Decibel(level).as_field_ratio()


# Conversion from a linear ratio.


@pytest.mark.parametrize(
    ("ratio", "power_level", "field_level"),
    [
        (Ratio(1), 0, 0),
        (Ratio(10), 10, 20),
        (Ratio(100), 20, 40),
        (Ratio(1000), 30, 60),
        (Ratio(Decimal("0.1")), -10, -20),
        (Percent(1), -20, -40),
        (Percent(100), 0, 0),
    ],
)
def test_powers_of_ten_convert_to_exact_levels(ratio, power_level, field_level):
    assert LogarithmicRatio.from_power_ratio(ratio) == Decibel(power_level)
    assert LogarithmicRatio.from_field_ratio(ratio) == Decibel(field_level)


def test_from_ratio_returns_a_decibel_display_level():
    level = LogarithmicRatio.from_power_ratio(Ratio(100))
    assert isinstance(level, LogarithmicRatio)
    assert level.unit is DECIBEL


def test_a_factor_of_two_is_about_three_decibels_of_power_and_six_of_voltage():
    power = LogarithmicRatio.from_power_ratio(Ratio(2))
    field = LogarithmicRatio.from_field_ratio(Ratio(2))
    assert float(power.magnitude) == pytest.approx(3.010299956639812, rel=1e-15)
    assert float(field.magnitude) == pytest.approx(6.020599913279624, rel=1e-15)
    assert field == power * 2


@pytest.mark.parametrize("bad", [Ratio(0), Ratio(-1), Percent(-5)])
def test_a_non_positive_ratio_has_no_level(bad):
    with pytest.raises(InvalidMeasurementError, match="positive ratio"):
        LogarithmicRatio.from_power_ratio(bad)
    with pytest.raises(InvalidMeasurementError, match="positive ratio"):
        LogarithmicRatio.from_field_ratio(bad)


# Properties over a range of levels.


@given(a=LEVELS, b=LEVELS)
def test_addition_is_commutative(a, b):
    assert Decibel(a) + Decibel(b) == Decibel(b) + Decibel(a)


@given(a=LEVELS, b=LEVELS, c=LEVELS)
def test_addition_is_associative(a, b, c):
    left = (Decibel(a) + Decibel(b)) + Decibel(c)
    right = Decibel(a) + (Decibel(b) + Decibel(c))
    assert left == right


@given(a=LEVELS)
def test_zero_is_the_identity_and_negation_the_inverse(a):
    assert Decibel(a) + Decibel(0) == Decibel(a)
    assert Decibel(a) + (-Decibel(a)) == Decibel(0)
    negated = -Decibel(a)
    assert -negated == Decibel(a)


@given(a=LEVELS, b=LEVELS)
def test_adding_levels_multiplies_the_power_ratios(a, b):
    combined = (Decibel(a) + Decibel(b)).as_power_ratio().magnitude
    product = (
        Decibel(a).as_power_ratio().magnitude * Decibel(b).as_power_ratio().magnitude
    )
    assert _relatively_close(combined, product)


@given(a=LEVELS, b=LEVELS)
def test_subtracting_levels_divides_the_field_ratios(a, b):
    combined = (Decibel(a) - Decibel(b)).as_field_ratio().magnitude
    quotient = (
        Decibel(a).as_field_ratio().magnitude / Decibel(b).as_field_ratio().magnitude
    )
    assert _relatively_close(combined, quotient)


@given(a=LEVELS)
def test_a_level_survives_a_round_trip_through_a_ratio(a):
    level = Decibel(a)
    via_power = LogarithmicRatio.from_power_ratio(level.as_power_ratio())
    via_field = LogarithmicRatio.from_field_ratio(level.as_field_ratio())
    assert abs(via_power.magnitude - level.magnitude) < Fraction(1, 10**20)
    assert abs(via_field.magnitude - level.magnitude) < Fraction(1, 10**20)


@given(a=LEVELS, b=LEVELS)
def test_ordering_of_levels_matches_ordering_of_ratios(a, b):
    if Decibel(a) < Decibel(b):
        assert Decibel(a).as_power_ratio() < Decibel(b).as_power_ratio()
    elif Decibel(a) > Decibel(b):
        assert Decibel(a).as_power_ratio() > Decibel(b).as_power_ratio()
    else:
        assert Decibel(a).as_power_ratio() == Decibel(b).as_power_ratio()


@given(a=LEVELS)
def test_field_ratio_of_a_level_is_the_power_ratio_of_its_half(a):
    assert Decibel(a).as_field_ratio() == (Decibel(a) / 2).as_power_ratio()
