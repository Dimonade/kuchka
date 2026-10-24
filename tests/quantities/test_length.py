"""Length: arithmetic, exact imperial conversion, and Metre/Meter naming.

NOTE: `Inch`'s (`0.0254`), `Acre`'s, `Hour`'s, and a few others units' scales are not a
power of ten.
These are excluded from the exact-division property suite.
Their conversions are checked elsewhere.

The rest of the module covers ordinary arithmetic on `Length`, and dividing a `Length`
by a `Time`, whose error message names `Velocity` directly.
"""

from decimal import Decimal

import pytest

from kuchka import InvalidMeasurementError
from kuchka import Length
from kuchka.units import length
from kuchka.units import length as length_units


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (
            length_units.Meter(1),
            length_units.Millimeter(500),
            length_units.Meter(Decimal("1.5")),
        ),
        (
            length_units.Millimeter(500),
            length_units.Meter(1),
            length_units.Meter(Decimal("1.5")),
        ),
        (
            length_units.Inch(1),
            length_units.Millimeter(Decimal("25.4")),
            length_units.Meter(Decimal("0.0508")),
        ),
        (
            length_units.Micrometer(1000),
            length_units.Millimeter(1),
            length_units.Millimeter(2),
        ),
    ],
    ids=[
        "meter+millimeter",
        "millimeter+meter",
        "inch+millimeter",
        "micrometer+millimeter",
    ],
)
def test_addition(a, b, expected):
    assert a + b == expected


def test_inch_converts_to_millimeters_exactly():
    """Test that an inch has been exactly 25.4 mm since 1959, not an approximation."""
    assert length_units.Inch(1) == length_units.Millimeter(Decimal("25.4"))


@pytest.mark.parametrize(
    ("inches", "expected_meters"),
    [
        (1, Decimal("0.0254")),
        (2, Decimal("0.0508")),
        (10, Decimal("0.254")),
        (Decimal("0.5"), Decimal("0.0127")),
        (-1, Decimal("-0.0254")),
    ],
    ids=["1in", "2in", "10in", "half_in", "negative_1in"],
)
def test_inch_round_trips_through_meter_exactly(inches, expected_meters):
    as_meters = length_units.Inch(inches).to(length_units.METER)
    assert as_meters == length_units.Meter(expected_meters)
    assert as_meters.value_in(length_units.METER) == expected_meters


@pytest.mark.parametrize(
    ("prefixed", "canonical", "scale"),
    [
        (length_units.Nanometer, length_units.Meter, Decimal("0.000000001")),
        (length_units.Micrometer, length_units.Meter, Decimal("0.000001")),
        (length_units.Millimeter, length_units.Meter, Decimal("0.001")),
        (length_units.Kilometer, length_units.Meter, Decimal(1000)),
    ],
    ids=["nanometer", "micrometer", "millimeter", "kilometer"],
)
def test_metric_prefixes_scale_correctly(prefixed, canonical, scale):
    assert prefixed(1) == canonical(scale)


def test_nanometer_and_micrometer_scale_correctly():
    """Wavelength- and beam-diameter-scale units, not just decorative additions."""
    assert length_units.Nanometer(1000) == length_units.Micrometer(1)
    assert length_units.Micrometer(1000) == length_units.Millimeter(1)


def test_scalar_multiplication_and_division():
    assert length_units.Meter(2) * 3 == length_units.Meter(6)
    assert length_units.Meter(6) / 3 == length_units.Meter(2)


@pytest.mark.parametrize(
    ("smaller", "larger"),
    [
        (length_units.Millimeter(500), length_units.Meter(1)),
        (length_units.Millimeter(20), length_units.Inch(1)),
        (length_units.Meter(0), length_units.Micrometer(1)),
    ],
    ids=["millimeter<meter", "millimeter<inch", "zero<micrometer"],
)
def test_ordering_within_length(smaller, larger):
    assert smaller < larger
    assert larger > smaller


def test_isinstance_of_length():
    assert isinstance(length_units.Meter(5), Length)
    assert isinstance(length_units.Inch(5), Length)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        length_units.Meter(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_micrometer_and_millimeter_unit_constants_round_trip():
    """`.unit` here comes from a constant, not a throwaway zero-valued quantity."""
    original = length_units.Meter(1)
    converted = (
        original.to(length_units.MICROMETER)
        .to(length_units.MILLIMETER)
        .to(length_units.METER)
    )
    assert converted == original


def test_meter_and_metre_are_the_same_function():
    assert length_units.Meter is length_units.Metre
    assert length_units.Millimeter is length_units.Millimetre
    assert length_units.Micrometer is length_units.Micrometre
    assert length_units.Nanometer is length_units.Nanometre
    assert length_units.Kilometer is length_units.Kilometre


def test_meter_and_metre_unit_constants_are_the_same_object():
    assert length_units.METER is length_units.METRE
    assert length_units.KILOMETER is length_units.KILOMETRE


def test_meter_displays_as_metre():
    """Both spellings share one symbol, `m`, so there is nothing to reconcile."""
    assert repr(length_units.Meter(1)) == "1 m"
    assert repr(length_units.Metre(1)) == "1 m"


def test_meter_and_metre_arithmetic_mixes_freely():
    assert length_units.Meter(1) + length_units.Metre(1) == length_units.Metre(2)
    assert length_units.Kilometre(1) == length_units.Kilometer(1)
    assert length_units.Meter(1000) == length_units.Kilometre(1)


def test_metre_is_canonical():
    assert Length._canonical_unit is length_units.METRE  # noqa: SLF001 -- verifying the module's own wiring


def test_metre_and_millimetre_scale_exactly():
    assert length_units.Metre(1) == length_units.Millimetre(1000)


def test_picometre_scales_correctly():
    assert length_units.Picometre(1000) == length_units.Nanometre(1)


def test_foot_is_exact():
    """A foot has been exactly 0.3048 m since the 1959 international yard agreement."""
    assert length_units.Foot(1) == length_units.Millimetre(Decimal("304.8"))


def test_yard_is_exact():
    assert length_units.Yard(1) == length_units.Millimetre(Decimal("914.4"))


def test_three_feet_make_a_yard_exactly():
    assert length_units.Foot(3) == length_units.Yard(1)


def test_seventeen_sixty_yards_make_a_mile_exactly():
    """The classic imperial identity, both sides exact multiples of the metre."""
    assert length_units.Yard(1760) == length_units.Mile(1)


def test_mile_is_exact():
    assert length_units.Mile(1) == length_units.Metre(Decimal("1609.344"))


def test_nautical_mile_is_exact():
    """One nautical mile is exactly 1852 m, by international definition."""
    assert length_units.NauticalMile(1) == length_units.Metre(1852)


def test_nautical_mile_is_not_the_statute_mile():
    assert length_units.NauticalMile(1) != length_units.Mile(1)


def test_flight_leg_matches_kilometres_exactly():
    assert length_units.NauticalMile(120) == length_units.Kilometre(Decimal("222.24"))


def test_isinstance_of_the_new_imperial_units():
    assert isinstance(length_units.Foot(5), Length)
    assert isinstance(length_units.Yard(5), Length)
    assert isinstance(length_units.Mile(5), Length)
    assert isinstance(length_units.NauticalMile(5), Length)


def test_ordering_across_the_imperial_ladder():
    assert length_units.Foot(1) < length_units.Yard(1) < length_units.Mile(1)


def test_love_you_to_the_moon_and_back():
    distance_to_moon = length_units.Kilometre(384_400)
    assert 2 * distance_to_moon == length_units.Kilometre(768_800)


def test_length_units_table_resolves_the_new_symbols():
    assert length_units.LENGTH_UNITS["pm"] is length_units.Picometre
    assert length_units.LENGTH_UNITS["ft"] is length_units.Foot
    assert length_units.LENGTH_UNITS["yd"] is length_units.Yard
    assert length_units.LENGTH_UNITS["mi"] is length_units.Mile
    assert length_units.LENGTH_UNITS["M"] is length_units.NauticalMile


def test_astronomical_unit_converts_exactly_to_metres() -> None:
    assert length.AstronomicalUnit(1) == length.Metre(Decimal(149597870700))
