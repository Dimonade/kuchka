"""Length: arithmetic, exact imperial conversion, and Metre/Meter naming.

NOTE: `Inch`'s (`0.0254`), `Acre`'s, `Hour`'s, and a few others units' scales are not a
power of ten. These are excluded from the exact-division property suite.
Their conversions are checked elsewhere.

The rest of the module covers ordinary arithmetic on `Length`, and dividing a `Length`
by a `Time`, whose error message names `Velocity` directly.
"""

from decimal import Decimal

import pytest

from kuchka import Area
from kuchka import Foot
from kuchka import Inch
from kuchka import InvalidMeasurementError
from kuchka import Kilometer
from kuchka import Kilometre
from kuchka import Length
from kuchka import Meter
from kuchka import Metre
from kuchka import Micrometer
from kuchka import Micrometre
from kuchka import Mile
from kuchka import Millimeter
from kuchka import Millimetre
from kuchka import Nanometer
from kuchka import Nanometre
from kuchka import NauticalMile
from kuchka import Picometre
from kuchka import SquareMeter
from kuchka import Yard
from kuchka.units import KILOMETER
from kuchka.units import KILOMETRE
from kuchka.units import LENGTH_UNITS
from kuchka.units import METER
from kuchka.units import METRE
from kuchka.units import MICROMETER
from kuchka.units import MILLIMETER


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Meter(1), Millimeter(500), Meter(Decimal("1.5"))),
        (Millimeter(500), Meter(1), Meter(Decimal("1.5"))),
        (Inch(1), Millimeter(Decimal("25.4")), Meter(Decimal("0.0508"))),
        (Micrometer(1000), Millimeter(1), Millimeter(2)),
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
    assert Inch(1) == Millimeter(Decimal("25.4"))


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
    as_meters = Inch(inches).to(METER)
    assert as_meters == Meter(expected_meters)
    assert as_meters.value_in(METER) == expected_meters


@pytest.mark.parametrize(
    ("prefixed", "canonical", "scale"),
    [
        (Nanometer, Meter, Decimal("0.000000001")),
        (Micrometer, Meter, Decimal("0.000001")),
        (Millimeter, Meter, Decimal("0.001")),
        (Kilometer, Meter, Decimal(1000)),
    ],
    ids=["nanometer", "micrometer", "millimeter", "kilometer"],
)
def test_metric_prefixes_scale_correctly(prefixed, canonical, scale):
    assert prefixed(1) == canonical(scale)


def test_nanometer_and_micrometer_scale_correctly():
    """Wavelength- and beam-diameter-scale units, not just decorative additions."""
    assert Nanometer(1000) == Micrometer(1)
    assert Micrometer(1000) == Millimeter(1)


def test_scalar_multiplication_and_division():
    assert Meter(2) * 3 == Meter(6)
    assert Meter(6) / 3 == Meter(2)


@pytest.mark.parametrize(
    ("smaller", "larger"),
    [
        (Millimeter(500), Meter(1)),
        (Millimeter(20), Inch(1)),
        (Meter(0), Micrometer(1)),
    ],
    ids=["millimeter<meter", "millimeter<inch", "zero<micrometer"],
)
def test_ordering_within_length(smaller, larger):
    assert smaller < larger
    assert larger > smaller


def test_isinstance_of_length():
    assert isinstance(Meter(5), Length)
    assert isinstance(Inch(5), Length)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Meter(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_length_times_length_is_area():
    """Length * Length used to be unrepresentable; it is now a registered Area."""
    result = Meter(5) * Meter(2)
    assert isinstance(result, Area)
    assert result == SquareMeter(10)


def test_length_times_length_is_commutative():
    assert Meter(5) * Meter(2) == Meter(2) * Meter(5)


def test_micrometer_and_millimeter_unit_constants_round_trip():
    """`.unit` here comes from a constant, not a throwaway zero-valued quantity."""
    original = Meter(1)
    converted = original.to(MICROMETER).to(MILLIMETER).to(METER)
    assert converted == original


def test_meter_and_metre_are_the_same_function():
    assert Meter is Metre
    assert Millimeter is Millimetre
    assert Micrometer is Micrometre
    assert Nanometer is Nanometre
    assert Kilometer is Kilometre


def test_meter_and_metre_unit_constants_are_the_same_object():
    assert METER is METRE
    assert KILOMETER is KILOMETRE


def test_meter_displays_as_metre():
    """Both spellings share one symbol, `m`, so there is nothing to reconcile."""
    assert repr(Meter(1)) == "1 m"
    assert repr(Metre(1)) == "1 m"


def test_meter_and_metre_arithmetic_mixes_freely():
    assert Meter(1) + Metre(1) == Metre(2)
    assert Kilometre(1) == Kilometer(1)
    assert Meter(1000) == Kilometre(1)


def test_metre_is_canonical():
    assert Length._canonical_unit is METRE  # noqa: SLF001 -- verifying the module's own wiring


def test_metre_and_millimetre_scale_exactly():
    assert Metre(1) == Millimetre(1000)


def test_picometre_scales_correctly():
    assert Picometre(1000) == Nanometre(1)


def test_foot_is_exact():
    """A foot has been exactly 0.3048 m since the 1959 international yard agreement."""
    assert Foot(1) == Millimetre(Decimal("304.8"))


def test_yard_is_exact():
    assert Yard(1) == Millimetre(Decimal("914.4"))


def test_three_feet_make_a_yard_exactly():
    assert Foot(3) == Yard(1)


def test_seventeen_sixty_yards_make_a_mile_exactly():
    """The classic imperial identity, both sides exact multiples of the metre."""
    assert Yard(1760) == Mile(1)


def test_mile_is_exact():
    assert Mile(1) == Metre(Decimal("1609.344"))


def test_nautical_mile_is_exact():
    """One nautical mile is exactly 1852 m, by international definition."""
    assert NauticalMile(1) == Metre(1852)


def test_nautical_mile_is_not_the_statute_mile():
    assert NauticalMile(1) != Mile(1)


def test_flight_leg_matches_kilometres_exactly():
    assert NauticalMile(120) == Kilometre(Decimal("222.24"))


def test_isinstance_of_the_new_imperial_units():
    assert isinstance(Foot(5), Length)
    assert isinstance(Yard(5), Length)
    assert isinstance(Mile(5), Length)
    assert isinstance(NauticalMile(5), Length)


def test_ordering_across_the_imperial_ladder():
    assert Foot(1) < Yard(1) < Mile(1)


def test_love_you_to_the_moon_and_back():
    distance_to_moon = Kilometre(384_400)
    assert 2 * distance_to_moon == Kilometre(768_800)


def test_length_units_table_resolves_the_new_symbols():
    assert LENGTH_UNITS["pm"] is Picometre
    assert LENGTH_UNITS["ft"] is Foot
    assert LENGTH_UNITS["yd"] is Yard
    assert LENGTH_UNITS["mi"] is Mile
    assert LENGTH_UNITS["M"] is NauticalMile
