"""Length: arithmetic, exact imperial conversion, and the planned-dimension error.

`Length` has no coupled quantities, so this module is mostly about proving three things:
ordinary arithmetic works the way every other `LinearQuantity` does, `Inch` converts to
and from the metric prefixes exactly rather than approximately, and dividing a `Length`
by a `Time` fails with a message that names `Velocity`, not just a generic
scope-boundary message.
"""

from decimal import Decimal

import pytest
from kuchka import Inch
from kuchka import InvalidMeasurementError
from kuchka import Kilometer
from kuchka import Length
from kuchka import Meter
from kuchka import Micrometer
from kuchka import Millimeter
from kuchka import Nanometer
from kuchka import PlannedDimensionError
from kuchka import Second
from kuchka import UnrepresentableDimensionError


def test_addition_across_prefixes_is_exact():
    total = Meter(1) + Millimeter(500)
    assert total == Meter(Decimal("1.5"))
    assert total == Millimeter(1500)


def test_inch_converts_to_millimeters_exactly():
    """An inch has been exactly 25.4 mm since 1959, not an approximation."""
    assert Inch(1) == Millimeter(Decimal("25.4"))


def test_inch_round_trips_through_meter():
    assert Meter(Decimal("0.0254")) == Inch(1)
    assert Inch(2).to(Meter(0).unit).value_in(Meter(0).unit) == Decimal("0.0508")


def test_nanometer_and_micrometer_scale_correctly():
    """Wavelength- and beam-diameter-scale units, not just decorative additions."""
    assert Nanometer(1000) == Micrometer(1)
    assert Micrometer(1000) == Millimeter(1)


def test_kilometer_scales_correctly():
    assert Kilometer(1) == Meter(1000)


def test_scalar_multiplication_and_division():
    assert Meter(2) * 3 == Meter(6)
    assert Meter(6) / 3 == Meter(2)


def test_ordering_within_length():
    assert Millimeter(500) < Meter(1)
    assert Inch(1) > Millimeter(20)


def test_isinstance_of_length():
    assert isinstance(Meter(5), Length)
    assert isinstance(Inch(5), Length)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Meter(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_length_divided_by_time_names_velocity_as_planned():
    """Length / Time is a real planned relation, not an accidental scope gap."""
    with pytest.raises(PlannedDimensionError, match="Velocity"):
        # Statically valid: falls through to the fallback `object` overload
        # (LinearQuantity | Decimal), so no ignore is needed -- the error
        # only shows up once `_promote` runs at call time.
        Meter(10) / Second(2)


def test_planned_dimension_error_is_also_unrepresentable():
    """A caller that only knows about the general error still catches this one."""
    with pytest.raises(UnrepresentableDimensionError):
        Meter(10) / Second(2)


def test_length_times_length_is_unrepresentable_not_planned():
    """Area is out of scope entirely: the generic message, not the named one."""
    match = "no registered engineering type"
    with pytest.raises(UnrepresentableDimensionError, match=match):
        Meter(5) * Meter(2)


def test_length_times_length_does_not_raise_planned_dimension_error():
    """Area must not be mistaken for a tracked, planned relation."""
    with pytest.raises(UnrepresentableDimensionError) as excinfo:
        Meter(5) * Meter(2)
    assert not isinstance(excinfo.value, PlannedDimensionError)
