"""`clock_parts` splits a span exactly, largest unit first, and loses nothing.

Each test draws a span of any size and sign, so the laws hold for every one of them,
not just for the explicit cases of the behaviour tests.
"""

from __future__ import annotations

from fractions import Fraction

from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

from kuchka import Second
from kuchka import Time
from kuchka.units import CLOCK_UNITS

SPANS = st.one_of(
    st.fractions(
        min_value=Fraction(-(10**9)),
        max_value=Fraction(10**9),
        max_denominator=10**15,
    ),
    st.integers(min_value=-(10**12), max_value=10**12).map(Fraction),
    st.sampled_from(
        [
            Fraction(0),
            Fraction(1),
            Fraction(60),
            Fraction(3600),
            Fraction(86_400),
            Fraction(1, 1000),
            Fraction(1, 10**15),
            Fraction(1, 10**16),
            Fraction(-1),
        ]
    ),
)
"""Spans in seconds: whole, fractional, at a unit, and below the last unit."""
EVERY_SPAN = settings(max_examples=500, deadline=None)


def span_of(seconds: Fraction) -> Time:
    """Return `seconds` as a time."""
    return Second(seconds)


@EVERY_SPAN
@given(SPANS)
def test_the_parts_add_up_to_the_span_exactly(seconds: Fraction) -> None:
    span = span_of(seconds)
    assert sum(span.clock_parts(), start=Second(0)) == span


@EVERY_SPAN
@given(SPANS)
def test_the_parts_use_the_clock_units_from_the_largest_down(
    seconds: Fraction,
) -> None:
    parts = span_of(seconds).clock_parts()
    scales = [part.unit.scale for part in parts]
    assert scales == sorted(scales, reverse=True)
    assert len(set(scales)) == len(scales)
    assert {part.unit for part in parts} <= set(CLOCK_UNITS)


@EVERY_SPAN
@given(SPANS)
def test_no_part_is_zero_and_each_has_the_sign_of_the_span(seconds: Fraction) -> None:
    span = span_of(seconds)
    parts = span.clock_parts()
    if seconds == 0:
        assert parts == (span,)
        return
    sign = 1 if seconds > 0 else -1
    assert all(part.magnitude * sign > 0 for part in parts)


@EVERY_SPAN
@given(SPANS)
def test_every_part_but_the_last_is_a_whole_count_of_its_unit(
    seconds: Fraction,
) -> None:
    parts = span_of(seconds).clock_parts()
    for part in parts[:-1]:
        assert part.value_in(part.unit).denominator == 1


@EVERY_SPAN
@given(SPANS)
def test_the_first_part_is_in_the_largest_unit_the_span_reaches(
    seconds: Fraction,
) -> None:
    span = span_of(seconds)
    if seconds == 0:
        return
    first = span.clock_parts()[0]
    reached = [unit for unit in CLOCK_UNITS if unit.scale <= abs(seconds)]
    expected = reached[0] if reached else CLOCK_UNITS[-1]
    assert first.unit == expected


@EVERY_SPAN
@given(SPANS)
def test_only_the_smallest_unit_holds_a_fraction(seconds: Fraction) -> None:
    for part in span_of(seconds).clock_parts():
        if part.unit != CLOCK_UNITS[-1]:
            assert part.value_in(part.unit).denominator == 1
