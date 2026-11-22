"""`Bounds` holds the range of measurements a field accepts, exactly.

Validation against limits is the other half of a strict boundary: a value that reads as
a voltage can still be a voltage the device must not be given.
The frameworks adapt this class, so its contract is tested here once.
"""

from __future__ import annotations

import dataclasses
from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kuchka import Ampere
from kuchka import BoundsError
from kuchka import Celsius
from kuchka import Decibel
from kuchka import Degree
from kuchka import Fahrenheit
from kuchka import InvalidMeasurementError
from kuchka import Kelvin
from kuchka import Millivolt
from kuchka import ParseError
from kuchka import Percent
from kuchka import Ratio
from kuchka import Volt
from kuchka import Voltage
from kuchka.bounds import Bounds
from kuchka.quantities.base.ordering import _OrderedScalarMixin
from tests.support.kinds import UNIT_TABLES

SUPPLY = Bounds(gt=Volt(0), le=Volt(60))


@pytest.mark.parametrize(
    ("bounds", "value", "within"),
    [
        (Bounds(ge=Volt(1)), Volt(1), True),
        (Bounds(ge=Volt(1)), Volt(0.999), False),
        (Bounds(gt=Volt(1)), Volt(1), False),
        (Bounds(gt=Volt(1)), Volt(1.001), True),
        (Bounds(le=Volt(1)), Volt(1), True),
        (Bounds(le=Volt(1)), Volt(1.001), False),
        (Bounds(lt=Volt(1)), Volt(1), False),
        (Bounds(lt=Volt(1)), Volt(0.999), True),
        (Bounds(ge=Volt(1), le=Volt(1)), Volt(1), True),
        (SUPPLY, Volt(0), False),
        (SUPPLY, Volt(60), True),
        (SUPPLY, Volt(61), False),
        (Bounds(ge=Volt(-5), lt=Volt(5)), Volt(-5), True),
    ],
)
def test_each_kind_of_bound_holds_or_excludes_its_edge(
    bounds: Bounds[Voltage],
    value: Voltage,
    within: bool,  # noqa: FBT001
) -> None:
    assert (value in bounds) is within
    if within:
        assert bounds.check(value) is value
    else:
        with pytest.raises(BoundsError):
            bounds.check(value)


@pytest.mark.parametrize(
    ("value", "message"),
    [
        (Volt(0), "0 V is not above 0 V."),
        (Volt(-1), "-1 V is not above 0 V."),
        (Volt(61), "61 V is above 60 V, the most allowed."),
        (
            Millivolt(Fraction(200_000, 3)),
            "200000/3 mV is above 60 V, the most allowed.",
        ),
    ],
)
def test_the_error_writes_the_value_and_the_bound_exactly(
    value: Voltage, message: str
) -> None:
    with pytest.raises(BoundsError) as raised:
        SUPPLY.check(value)
    assert str(raised.value) == message


def test_a_lower_and_an_upper_bound_say_which_edge_was_missed() -> None:
    with pytest.raises(BoundsError, match="is below 5 V, the least allowed"):
        Bounds(ge=Volt(5)).check(Volt(1))
    with pytest.raises(BoundsError, match="is not below 5 V"):
        Bounds(lt=Volt(5)).check(Volt(5))


def test_a_bound_compares_in_whatever_unit_either_was_written() -> None:
    assert Millivolt(60_000) in SUPPLY
    assert Millivolt(60_001) not in SUPPLY
    assert Ratio(1) in Bounds(ge=Ratio(0), le=Percent(100))
    assert Percent(100.5) not in Bounds(ge=Ratio(0), le=Ratio(1))


def test_a_bound_compares_exactly() -> None:
    third = Volt(1) / 3
    assert third in Bounds(ge=third, le=third)
    assert Volt(0.33333333333333333) not in Bounds(ge=third)
    assert Volt(Fraction(1, 10)) in Bounds(le=Volt(0.1))


def test_the_bounds_of_an_affine_quantity_hold_across_scales() -> None:
    operating = Bounds(ge=Celsius(-40), le=Celsius(85))
    assert Fahrenheit(-40) in operating
    assert Kelvin(358.15) in operating
    assert Celsius(85.01) not in operating
    with pytest.raises(BoundsError, match=r"-40.1 °C is below -40 °C"):
        operating.check(Celsius(-40.1))
    with pytest.raises(BoundsError, match=r"359 K is above 85 °C"):
        operating.check(Kelvin(359))


def test_the_bounds_of_a_level_and_of_a_proportion_hold() -> None:
    assert Decibel(-3) in Bounds(le=Decibel(0))
    assert Decibel(3) not in Bounds(le=Decibel(0))
    duty = Bounds(ge=Ratio(0), le=Ratio(1))
    assert Percent(25) in duty
    assert Ratio(25) not in duty


def test_the_range_is_written_in_words() -> None:
    assert SUPPLY.describe() == "above 0 V and at most 60 V"
    assert Bounds(ge=Ratio(0), lt=Ratio(1)).describe() == "at least 0 and below 1"
    assert Bounds(le=Millivolt(Fraction(1, 3))).describe() == "at most 1/3 mV"


def test_a_check_of_another_quantity_type_is_a_mistake_in_the_program() -> None:
    with pytest.raises(TypeError, match="bounds of Voltage cannot check Current"):
        SUPPLY.check(Ampere(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="cannot check Current"):
        Ampere(1) in SUPPLY  # noqa: B015
    float_value = 5.0
    float_value = 1.5
    with pytest.raises(TypeError, match="cannot check float"):
        float_value in SUPPLY  # noqa: B015


def test_the_error_is_a_value_error_and_a_measurement_error_of_its_own() -> None:
    with pytest.raises(BoundsError) as raised:
        SUPPLY.check(Volt(61))
    assert isinstance(raised.value, ValueError)
    assert isinstance(raised.value, InvalidMeasurementError)
    assert not isinstance(raised.value, ParseError)


@pytest.mark.parametrize(
    ("make", "match"),
    [
        (Bounds, "at least one of"),
        (lambda: Bounds(gt=Volt(1), ge=Volt(1)), "gt and ge are both lower bounds"),
        (lambda: Bounds(lt=Volt(1), le=Volt(1)), "lt and le are both upper bounds"),
        (
            lambda: Bounds(ge=Volt(5), le=Volt(1)),
            "no measurement is at least 5 V and",
        ),
        (
            lambda: Bounds(gt=Volt(5), le=Volt(5)),
            "no measurement is above 5 V and",
        ),
        (
            lambda: Bounds(ge=Volt(5), lt=Volt(5)),
            "no measurement is at least 5 V and b",
        ),
        (lambda: Bounds(gt=Volt(5), lt=Volt(6), ge=None), None),
    ],
)
def test_bounds_that_make_no_range_are_refused_where_they_are_written(
    make: object, match: str | None
) -> None:
    if match is None:
        make()  # type: ignore[operator]
        return
    with pytest.raises(ValueError, match=match):
        make()  # type: ignore[operator]


@pytest.mark.parametrize("bound", [5, "5 V", 5.0, object()])
def test_a_bound_that_is_no_measurement_is_refused(bound: object) -> None:
    with pytest.raises(TypeError, match="not a measurement"):
        Bounds(ge=bound)  # type: ignore[type-var]  # ty: ignore[invalid-argument-type]


def test_bounds_of_different_quantity_types_are_refused() -> None:
    with pytest.raises(TypeError, match="different quantity types"):
        Bounds(ge=Volt(0), le=Ampere(1))  # type: ignore[type-var]  # ty: ignore[invalid-argument-type]


def test_a_quantity_with_no_ordering_has_no_bounds() -> None:
    with pytest.raises(TypeError, match="Angle has no ordering"):
        Bounds(ge=Degree(0))  # type: ignore[type-var]  # ty: ignore[invalid-argument-type]


def test_exactly_the_quantity_types_with_an_ordering_have_bounds() -> None:
    bounded = unordered = 0
    for table in UNIT_TABLES.values():
        sample = next(iter(table.values()))(1)
        if isinstance(sample, _OrderedScalarMixin):
            assert Bounds(ge=sample).check(sample) is sample
            bounded += 1
        else:
            with pytest.raises(TypeError, match="no ordering"):
                Bounds(ge=sample)  # type: ignore[type-var]  # ty: ignore[invalid-argument-type]
            unordered += 1
    assert bounded > unordered > 0


def test_bounds_are_values_that_compare_hash_and_do_not_change() -> None:
    assert Bounds(ge=Ratio(1)) == Bounds(ge=Percent(100))
    assert hash(Bounds(ge=Ratio(1))) == hash(Bounds(ge=Percent(100)))
    assert Bounds(ge=Ratio(1)) != Bounds(gt=Ratio(1))
    assert SUPPLY.quantity is Voltage
    with pytest.raises(dataclasses.FrozenInstanceError):
        SUPPLY.le = Volt(1)  # type: ignore[misc]  # ty: ignore[invalid-assignment]


@given(
    value=st.fractions(min_value=-20, max_value=20, max_denominator=7),
    lower=st.fractions(min_value=-10, max_value=10, max_denominator=7),
    width=st.fractions(min_value=0, max_value=10, max_denominator=7),
    lower_open=st.booleans(),
    upper_open=st.booleans(),
)
def test_containment_agrees_with_the_comparisons_it_names(
    value: Fraction,
    lower: Fraction,
    width: Fraction,
    lower_open: bool,  # noqa: FBT001
    upper_open: bool,  # noqa: FBT001
) -> None:
    upper = lower + width
    if width == 0 and (lower_open or upper_open):
        return
    kwargs = {
        ("gt" if lower_open else "ge"): Volt(lower),
        ("lt" if upper_open else "le"): Volt(upper),
    }
    bounds = Bounds(**kwargs)  # type: ignore[arg-type]
    above = value > lower if lower_open else value >= lower
    below = value < upper if upper_open else value <= upper
    assert (Volt(value) in bounds) is (above and below)
