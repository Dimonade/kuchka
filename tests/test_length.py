"""Length: arithmetic, exact imperial conversion, and Metre/Meter naming.

NOTE: `Inch`'s scale (`0.0254`) is the one unit definition in this library that isn't a
power of ten.
Its conversions are pinned here to specific, known-exact values: an inch has been
exactly 25.4 mm since 1959, and that's the claim these tests check.

The rest of the module covers ordinary arithmetic on `Length`, and dividing a `Length`
by a `Time`, whose error message names `Velocity` directly.
"""

from decimal import Decimal

import pytest

from kuchka import Centimeter
from kuchka import Decimeter
from kuchka import Inch
from kuchka import InvalidMeasurementError
from kuchka import Kilometer
from kuchka import Kilometre
from kuchka import Length
from kuchka import Meter
from kuchka import Metre
from kuchka import Micrometer
from kuchka import Micrometre
from kuchka import Millimeter
from kuchka import Millimetre
from kuchka import Nanometer
from kuchka import Nanometre
from kuchka import PlannedDimensionError
from kuchka import UnrepresentableDimensionError
from kuchka.units import KILOMETER
from kuchka.units import KILOMETRE
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
        (Centimeter, Meter, Decimal("0.01")),
        (Decimeter, Meter, Decimal("0.1")),
        (Kilometer, Meter, Decimal(1000)),
    ],
    ids=[
        "nanometer",
        "micrometer",
        "millimeter",
        "centimeter",
        "decimeter",
        "kilometer",
    ],
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


def test_length_times_length_is_unrepresentable_not_planned():
    """Test that area is out of scope but planned and gives unrepresentable error."""
    match = "no registered engineering type"
    with pytest.raises(UnrepresentableDimensionError, match=match):
        Meter(5) * Meter(2)


def test_length_times_length_does_not_raise_planned_dimension_error():
    """Area must not be mistaken for a tracked, planned relation."""
    with pytest.raises(UnrepresentableDimensionError) as excinfo:
        Meter(5) * Meter(2)
    assert not isinstance(excinfo.value, PlannedDimensionError)


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
