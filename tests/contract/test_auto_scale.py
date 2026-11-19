"""`auto_scale` keeps the value, stays on the ladder, and picks the unit by size.

Each test draws a measurement in a unit of a ladder of a type that has ladders, so one
test covers every laddered type, and a ladder bound later is covered without an edit.
The explicit examples, with their units written out, are in the behaviour tests.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from hypothesis import assume
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

from kuchka import InvalidMeasurementError
from tests.support.kinds import QUANTITY_TYPES

LADDERED = [cls for cls in QUANTITY_TYPES if vars(cls).get("_ladders")]
LADDERED_IDS = [cls.__name__ for cls in LADDERED]
OFF_LADDER = [
    (cls, unit)
    for cls in QUANTITY_TYPES
    if cls._scales_by_size
    for unit in sorted(
        cls._applicable_units - set(cls._ladder_of), key=lambda unit: unit.name
    )
    if vars(cls).get("_ladders")
]
OFF_LADDER_IDS = [f"{cls.__name__}-{unit.name}" for cls, unit in OFF_LADDER]
EVERY_MEASUREMENT = settings(max_examples=300, deadline=None)

SIZES = st.one_of(
    st.fractions(
        min_value=Fraction(-(10**16)), max_value=Fraction(10**16), max_denominator=10**9
    ),
    st.sampled_from(
        [
            Fraction(0),
            Fraction(1),
            Fraction(-1),
            Fraction(999, 1000),
            Fraction(1000),
            Fraction(999_999, 1000),
        ]
    ),
)
"""How many of a unit a measurement is: at, just under, and across the steps."""


@st.composite
def measurements(draw: st.DrawFn) -> tuple[type, object, Fraction]:
    """Draw a type with ladders, a unit on one of them, and a count of that unit."""
    cls = draw(st.sampled_from(LADDERED))
    unit = draw(st.sampled_from([unit for unit in cls._ladder_of]))  # noqa: C416
    return cls, unit, draw(SIZES)


def build(cls: type, unit: object, size: Fraction):
    """Return `size` of `unit` as a `cls`, or skip a size the type cannot hold."""
    try:
        return cls(size * unit.scale + getattr(unit, "offset", 0), unit)
    except InvalidMeasurementError:
        assume(False)
        raise


@EVERY_MEASUREMENT
@given(measurements())
def test_the_scaled_measurement_is_the_same_value_of_the_same_type(drawn) -> None:
    cls, unit, size = drawn
    measurement = build(cls, unit, size)
    scaled = measurement.auto_scale()
    assert type(scaled) is cls
    assert scaled == measurement
    assert hash(scaled) == hash(measurement)


@EVERY_MEASUREMENT
@given(measurements())
def test_the_scaled_measurement_stays_on_the_ladder_of_its_unit(drawn) -> None:
    cls, unit, size = drawn
    scaled = build(cls, unit, size).auto_scale()
    assert scaled.unit in cls._ladder_of[unit]


@EVERY_MEASUREMENT
@given(measurements())
def test_scaling_twice_changes_nothing_more(drawn) -> None:
    cls, unit, size = drawn
    scaled = build(cls, unit, size).auto_scale()
    assert scaled.auto_scale() is scaled


@EVERY_MEASUREMENT
@given(measurements())
def test_the_measurement_is_returned_itself_when_its_unit_is_already_chosen(
    drawn,
) -> None:
    cls, unit, size = drawn
    measurement = build(cls, unit, size)
    scaled = measurement.auto_scale()
    assert (scaled is measurement) == (scaled.unit == measurement.unit)


@EVERY_MEASUREMENT
@given(measurements())
def test_zero_keeps_the_unit_it_has(drawn) -> None:
    cls, unit, _ = drawn
    zero = build(cls, unit, Fraction(0))
    assert zero.auto_scale() is zero


@EVERY_MEASUREMENT
@given(measurements())
def test_the_unit_is_the_largest_one_that_the_size_reaches(drawn) -> None:
    cls, unit, size = drawn
    assume(size != 0)
    scaled = build(cls, unit, size).auto_scale()
    ladder = cls._ladder_of[unit]
    shown = abs(scaled.value_in(scaled.unit))
    position = ladder.index(scaled.unit)
    if position > 0:
        assert shown >= 1
    if position + 1 < len(ladder):
        assert shown < ladder[position + 1].scale / scaled.unit.scale


@EVERY_MEASUREMENT
@given(measurements())
def test_the_sign_does_not_pick_the_unit(drawn) -> None:
    cls, unit, size = drawn
    assume(size != 0)
    plain = build(cls, unit, abs(size))
    try:
        negated = build(cls, unit, -abs(size))
    except InvalidMeasurementError:
        return
    assert negated.auto_scale().unit == plain.auto_scale().unit


@pytest.mark.parametrize(("cls", "unit"), OFF_LADDER, ids=OFF_LADDER_IDS)
def test_a_unit_on_no_ladder_keeps_its_measurement(cls: type, unit: object) -> None:
    for size in (Fraction(1, 2000), Fraction(1), Fraction(3000), Fraction(10**12)):
        try:
            measurement = build(cls, unit, size)
        except InvalidMeasurementError:
            continue
        assert measurement.auto_scale() is measurement


@pytest.mark.parametrize("cls", LADDERED, ids=LADDERED_IDS)
def test_every_unit_of_a_ladder_is_reached_by_some_size(cls: type) -> None:
    for ladder in cls._ladders:
        reached = set()
        for unit in ladder:
            for size in (Fraction(1), Fraction(5)):
                scaled = build(cls, ladder[0], size * unit.scale / ladder[0].scale)
                reached.add(scaled.auto_scale().unit)
        assert reached == set(ladder)
