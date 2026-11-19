"""`Time.clock_parts` with the units written out, one case for each rule."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka.units import temporal


def symbols(parts) -> list[str]:
    """Return the symbols the parts are displayed with."""
    return [part.unit.symbol for part in parts]


def test_a_span_splits_into_hours_minutes_seconds_and_milliseconds() -> None:
    span = temporal.Hour(1) + temporal.Minute(23) + temporal.Millisecond(45_500)
    assert span.clock_parts() == (
        temporal.Hour(1),
        temporal.Minute(23),
        temporal.Second(45),
        temporal.Millisecond(500),
    )


def test_a_picosecond_count_reads_as_seconds_and_what_is_left() -> None:
    assert temporal.Picosecond(10**12).clock_parts() == (temporal.Second(1),)
    assert temporal.Picosecond(10**12 + 1).clock_parts() == (
        temporal.Second(1),
        temporal.Picosecond(1),
    )


@pytest.mark.parametrize(
    ("span", "expected"),
    [
        (temporal.Hour(24), ["d"]),
        (temporal.Hour(25), ["d", "h"]),
        (temporal.Second(86_399), ["h", "min", "s"]),
        (temporal.Week(1), ["d"]),
        (temporal.JulianYear(1), ["d", "h"]),
        (temporal.Minute(90), ["h", "min"]),
        (temporal.Second(3600), ["h"]),
    ],
)
def test_the_split_runs_through_days_with_no_calendar(span, expected) -> None:
    assert symbols(span.clock_parts()) == expected


def test_a_count_of_days_has_no_larger_unit() -> None:
    assert temporal.Week(1).clock_parts() == (temporal.Day(7),)
    assert temporal.Day(400).clock_parts() == (temporal.Day(400),)
    assert temporal.JulianYear(1).clock_parts() == (temporal.Day(365), temporal.Hour(6))


def test_a_span_under_a_second_splits_into_the_smaller_units() -> None:
    parts = (temporal.Millisecond(1) + temporal.Nanosecond(250)).clock_parts()
    assert symbols(parts) == ["ms", "ns"]
    assert parts == (temporal.Millisecond(1), temporal.Nanosecond(250))


def test_a_span_of_one_third_of_a_second_keeps_the_exact_remainder() -> None:
    parts = temporal.Second(Fraction(1, 3)).clock_parts()
    assert symbols(parts) == ["ms", "µs", "ns", "ps", "fs"]
    counts = [part.value_in(part.unit) for part in parts]
    assert counts == [333, 333, 333, 333, Fraction(1000, 3)]
    assert sum(parts, start=temporal.Second(0)) == temporal.Second(Fraction(1, 3))


def test_a_span_below_a_femtosecond_is_a_fraction_of_one() -> None:
    assert temporal.Femtosecond(0.5).clock_parts() == (temporal.Femtosecond(0.5),)


def test_a_negative_span_has_negative_parts() -> None:
    assert temporal.Second(-90).clock_parts() == (
        temporal.Minute(-1),
        temporal.Second(-30),
    )


def test_a_zero_span_is_returned_as_it_is() -> None:
    zero = temporal.Millisecond(0)
    (part,) = zero.clock_parts()
    assert part is zero
    assert part.unit == temporal.MILLISECOND


def test_the_parts_are_displayed_in_their_own_units() -> None:
    parts = temporal.Second(3725.5).clock_parts()
    assert " ".join(map(str, parts)) == "1 h 2 min 5 s 500 ms"
