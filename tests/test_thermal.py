"""Absolute temperature and TemperatureDelta.

Currently the only affine quantity that is implemented, therefore lives in a dedicated
space.
"""

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import Celsius
from kuchka import DeltaCelsius
from kuchka import DeltaFahrenheit
from kuchka import DeltaKelvin
from kuchka import Fahrenheit
from kuchka import IncompatibleDimensionError
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import Kelvin
from kuchka import MeasurementError
from kuchka import Temperature
from kuchka import TemperatureDelta
from kuchka.internal import symbols
from kuchka.units import CELSIUS
from kuchka.units import DELTA_FAHRENHEIT
from kuchka.units import FAHRENHEIT
from kuchka.units import KELVIN
from kuchka.units import TEMPERATURE_DELTA_UNITS
from kuchka.units import TEMPERATURE_UNITS


def test_celsius_to_kelvin_offset_is_exact():
    """Test that 273.15 is exactly representable in Decimal, unlike float.

    The float conversion must be exact.
    """
    assert Celsius(0).kelvin == Decimal("273.15")
    assert Celsius(0) == Kelvin(Decimal("273.15"))


def test_boiling_point_round_trip():
    boiling = Celsius(100)
    assert boiling.value_in(KELVIN) == Decimal("373.15")


def test_temperature_minus_temperature_is_a_delta():
    delta = Celsius(25) - Celsius(20)
    assert delta == DeltaCelsius(5)
    assert delta == DeltaKelvin(5)


def test_temperature_plus_delta_is_a_temperature():
    result = Celsius(20) + DeltaCelsius(5)
    assert isinstance(result, Temperature)
    assert result == Celsius(25)


def test_delta_plus_temperature_also_works_reflected():
    result = DeltaCelsius(5) + Celsius(20)
    assert result == Celsius(25)


def test_adding_two_temperatures_is_rejected_with_a_physical_explanation():
    with pytest.raises(MeasurementError, match="point on a scale"):
        Celsius(20) + Celsius(5)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_temperature_cannot_be_scaled_by_a_number():
    with pytest.raises(TypeError):
        Celsius(20) * 2  # type: ignore[operator]  # ty: ignore[unsupported-operator]

    with pytest.raises(TypeError):
        2 * Celsius(20)  # type: ignore[operator]  # ty: ignore[unsupported-operator]

    with pytest.raises(TypeError):
        Kelvin(300) * 2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_temperature_ordering():
    assert Celsius(0) < Celsius(100)
    assert Kelvin(0) < Celsius(0)  # 0 K is colder than 0 degC


def test_temperature_delta_behaves_like_an_ordinary_linear_quantity():
    assert DeltaCelsius(5) + DeltaCelsius(5) == DeltaCelsius(10)
    assert DeltaCelsius(5) * 2 == DeltaCelsius(10)


def test_absolute_zero_round_trips_between_kelvin_and_celsius():
    absolute_zero = Kelvin(0)
    assert absolute_zero.value_in(CELSIUS) == Decimal("-273.15")
    assert absolute_zero.to(CELSIUS) == Celsius(Decimal("-273.15"))


def test_negative_celsius_is_a_valid_temperature():
    """A value below absolute zero is a modelling error, not a type error."""
    below_zero = Celsius(-40)
    assert below_zero.kelvin == Decimal("233.15")


def test_temperature_minus_delta_shifts_the_reading_down():
    result = Celsius(20) - DeltaCelsius(5)
    assert result == Celsius(15)


def test_delta_across_prefixes_compares_equal():
    assert DeltaCelsius(1) == DeltaKelvin(1)


def test_temperature_equality_across_scales():
    assert Celsius(0) == Kelvin(Decimal("273.15"))
    assert Celsius(100) != Kelvin(100)


@pytest.mark.parametrize(
    ("low", "high"),
    [
        (Celsius(0), Celsius(1)),
        (Kelvin(0), Kelvin(1)),
        (Celsius(-273), Kelvin(1)),
    ],
    ids=["celsius<celsius", "kelvin<kelvin", "near_absolute_zero<kelvin"],
)
def test_temperature_ordering_operators_agree_with_each_other(low, high):
    assert low < high
    assert high > low
    assert low <= high
    assert not (low >= high)


def test_unit_property_reflects_the_display_unit():
    assert Celsius(20).unit is CELSIUS
    assert Kelvin(20).unit is KELVIN


def test_to_rejects_a_non_temperature_unit():
    with pytest.raises(InvalidConversionError, match="temperature unit"):
        Celsius(20).to(object())  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_comparison_against_a_non_temperature_raises_incompatible_dimension_error():
    with pytest.raises(IncompatibleDimensionError):
        Celsius(20) < object()  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        Celsius(20) <= object()  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        Celsius(20) > object()  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        Celsius(20) >= object()  # noqa: B015


def test_equality_against_a_non_temperature_is_false_not_an_error():
    assert (Celsius(20) == object()) is False


def test_addition_with_an_unsupported_operand_raises_type_error():
    with pytest.raises(TypeError):
        Celsius(20) + object()  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_subtraction_with_an_unsupported_operand_raises_type_error():
    with pytest.raises(TypeError):
        Celsius(20) - object()  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_repr_shows_the_display_unit_symbol():
    assert repr(Celsius(20)) == f"20 {symbols.DEGREE}C"
    assert repr(Kelvin(20)) == "20 K"


def test_kelvin_below_absolute_zero_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        Kelvin(-1)


def test_celsius_below_absolute_zero_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        Celsius(-274)


def test_absolute_zero_itself_is_a_valid_temperature():
    assert Kelvin(0).kelvin == 0
    assert Celsius(-273.15).kelvin == 0


def test_subtracting_a_delta_below_absolute_zero_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        Kelvin(5) - DeltaKelvin(10)


@pytest.mark.parametrize(
    ("fahrenheit", "celsius"),
    [
        (32, 0),
        (212, 100),
        (-40, -40),
        (68, 20),
        (Decimal("98.6"), 37),
        (-459.67, Decimal("-273.15")),
    ],
    ids=["freezing", "boiling", "crossover", "room", "body", "absolute_zero"],
)
def test_fahrenheit_reference_points_equal_their_celsius_counterparts(
    fahrenheit, celsius
):
    assert Fahrenheit(fahrenheit) == Celsius(celsius)
    assert Fahrenheit(fahrenheit).value_in(CELSIUS) == celsius


def test_fahrenheit_absolute_zero_is_exactly_zero_kelvin():
    assert Fahrenheit(Decimal("-459.67")).kelvin == 0
    assert Fahrenheit(Decimal("-459.67")) == Kelvin(0)


def test_fahrenheit_below_absolute_zero_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        Fahrenheit(-460)


def test_fahrenheit_to_kelvin_keeps_the_exact_fraction():
    assert Fahrenheit(0).kelvin == Fraction(45967, 180)
    assert Fahrenheit(100).kelvin == Fraction(45967, 180) + Fraction(500, 9)


def test_fahrenheit_round_trips_through_every_temperature_unit():
    reading = Fahrenheit(Decimal("72.5"))
    for unit in (KELVIN, CELSIUS, FAHRENHEIT):
        converted = reading.to(unit)
        assert converted == reading
        assert converted.value_in(FAHRENHEIT) == Decimal("72.5")


def test_value_in_fahrenheit_is_exact_for_celsius_and_kelvin_readings():
    assert Celsius(100).value_in(FAHRENHEIT) == Decimal(212)
    assert Kelvin(0).value_in(FAHRENHEIT) == Decimal("-459.67")
    assert Celsius(Decimal(37)).value_in(FAHRENHEIT) == Decimal("98.6")


def test_fahrenheit_ordering_across_scales():
    assert Fahrenheit(31) < Celsius(0)
    assert Fahrenheit(33) > Celsius(0)
    assert Fahrenheit(-459.67) <= Kelvin(0)
    assert Fahrenheit(50) < Fahrenheit(51)


def test_fahrenheit_minus_fahrenheit_is_a_delta_in_kelvin_magnitude():
    delta = Fahrenheit(77) - Fahrenheit(68)
    assert delta == DeltaFahrenheit(9)
    assert delta == DeltaCelsius(5)
    assert delta == DeltaKelvin(5)


def test_fahrenheit_minus_celsius_is_a_delta():
    assert Fahrenheit(212) - Celsius(0) == DeltaCelsius(100)


def test_fahrenheit_plus_and_minus_a_delta_shifts_the_reading_and_keeps_its_unit():
    shifted_up = Fahrenheit(68) + DeltaFahrenheit(9)
    shifted_down = Fahrenheit(68) - DeltaFahrenheit(9)
    assert shifted_up == Fahrenheit(77)
    assert shifted_down == Fahrenheit(59)
    assert shifted_up.unit is FAHRENHEIT
    assert shifted_down.unit is FAHRENHEIT


def test_a_celsius_delta_shifts_a_fahrenheit_reading():
    assert Fahrenheit(32) + DeltaCelsius(5) == Fahrenheit(41)


def test_adding_two_fahrenheit_readings_is_rejected():
    with pytest.raises(MeasurementError, match="point on a scale"):
        Fahrenheit(68) + Fahrenheit(9)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_fahrenheit_cannot_be_scaled_by_a_number():
    with pytest.raises(TypeError):
        Fahrenheit(68) * 2  # type: ignore[operator]  # ty: ignore[unsupported-operator]

    with pytest.raises(TypeError):
        2 * Fahrenheit(68)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_delta_fahrenheit_behaves_like_an_ordinary_linear_quantity():
    assert DeltaFahrenheit(9) + DeltaFahrenheit(9) == DeltaFahrenheit(18)
    assert DeltaFahrenheit(9) * 2 == DeltaFahrenheit(18)
    assert DeltaFahrenheit(9) / 3 == DeltaFahrenheit(3)


def test_delta_fahrenheit_is_five_ninths_of_a_delta_kelvin():
    assert DeltaFahrenheit(9) == DeltaKelvin(5)
    assert DELTA_FAHRENHEIT.scale == Fraction(5, 9)
    assert DeltaFahrenheit(9).magnitude == Decimal(5)


def test_fahrenheit_unit_property_and_repr():
    assert Fahrenheit(68).unit is FAHRENHEIT
    assert repr(Fahrenheit(68)) == f"68 {symbols.DEGREE}F"
    assert repr(DeltaFahrenheit(9)) == f"9 {symbols.DELTA}{symbols.DEGREE}F"


def test_fahrenheit_is_registered_in_the_unit_tables():
    assert TEMPERATURE_UNITS["F"] is Fahrenheit
    assert TEMPERATURE_DELTA_UNITS["dF"] is DeltaFahrenheit


def test_fahrenheit_is_a_temperature():
    assert isinstance(Fahrenheit(68), Temperature)
    assert isinstance(DeltaFahrenheit(9), TemperatureDelta)
