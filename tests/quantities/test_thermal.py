"""Absolute temperature and TemperatureDelta.

Currently the only affine quantity that is implemented, therefore lives in a dedicated
space.
"""

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import MeasurementError
from kuchka import Temperature
from kuchka import TemperatureDelta
from kuchka.internal import symbols
from kuchka.units import thermal


def test_celsius_to_kelvin_offset_is_exact():
    """Test that 273.15 is exactly representable in Decimal, unlike float.

    The float conversion must be exact.
    """
    assert thermal.Celsius(0).kelvin == Decimal("273.15")
    assert thermal.Celsius(0) == thermal.Kelvin(Decimal("273.15"))


def test_boiling_point_round_trip():
    boiling = thermal.Celsius(100)
    assert boiling.value_in(thermal.KELVIN) == Decimal("373.15")


def test_temperature_minus_temperature_is_a_delta():
    delta = thermal.Celsius(25) - thermal.Celsius(20)
    assert delta == thermal.DeltaCelsius(5)
    assert delta == thermal.DeltaKelvin(5)


def test_temperature_plus_delta_is_a_temperature():
    result = thermal.Celsius(20) + thermal.DeltaCelsius(5)
    assert isinstance(result, Temperature)
    assert result == thermal.Celsius(25)


def test_delta_plus_temperature_also_works_reflected():
    result = thermal.DeltaCelsius(5) + thermal.Celsius(20)
    assert result == thermal.Celsius(25)


def test_adding_two_temperatures_is_rejected_with_a_physical_explanation():
    with pytest.raises(MeasurementError, match="point on a scale"):
        thermal.Celsius(20) + thermal.Celsius(5)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_temperature_cannot_be_scaled_by_a_number():
    with pytest.raises(TypeError):
        thermal.Celsius(20) * 2  # type: ignore[operator]  # ty: ignore[unsupported-operator]

    with pytest.raises(TypeError):
        2 * thermal.Celsius(20)  # type: ignore[operator]  # ty: ignore[unsupported-operator]

    with pytest.raises(TypeError):
        thermal.Kelvin(300) * 2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_temperature_ordering():
    assert thermal.Celsius(0) < thermal.Celsius(100)
    assert thermal.Kelvin(0) < thermal.Celsius(0)  # 0 K is colder than 0 degC


def test_temperature_delta_behaves_like_an_ordinary_linear_quantity():
    assert thermal.DeltaCelsius(5) + thermal.DeltaCelsius(5) == thermal.DeltaCelsius(10)
    assert thermal.DeltaCelsius(5) * 2 == thermal.DeltaCelsius(10)


def test_absolute_zero_round_trips_between_kelvin_and_celsius():
    absolute_zero = thermal.Kelvin(0)
    assert absolute_zero.value_in(thermal.CELSIUS) == Decimal("-273.15")
    assert absolute_zero.to(thermal.CELSIUS) == thermal.Celsius(Decimal("-273.15"))


def test_negative_celsius_is_a_valid_temperature():
    """A value below absolute zero is a modelling error, not a type error."""
    below_zero = thermal.Celsius(-40)
    assert below_zero.kelvin == Decimal("233.15")


def test_temperature_minus_delta_shifts_the_reading_down():
    result = thermal.Celsius(20) - thermal.DeltaCelsius(5)
    assert result == thermal.Celsius(15)


def test_delta_across_prefixes_compares_equal():
    assert thermal.DeltaCelsius(1) == thermal.DeltaKelvin(1)


def test_temperature_equality_across_scales():
    assert thermal.Celsius(0) == thermal.Kelvin(Decimal("273.15"))
    assert thermal.Celsius(100) != thermal.Kelvin(100)


@pytest.mark.parametrize(
    ("low", "high"),
    [
        (thermal.Celsius(0), thermal.Celsius(1)),
        (thermal.Kelvin(0), thermal.Kelvin(1)),
        (thermal.Celsius(-273), thermal.Kelvin(1)),
    ],
    ids=["celsius<celsius", "kelvin<kelvin", "near_absolute_zero<kelvin"],
)
def test_temperature_ordering_operators_agree_with_each_other(low, high):
    assert low < high
    assert high > low
    assert low <= high
    assert not (low >= high)


def test_unit_property_reflects_the_display_unit():
    assert thermal.Celsius(20).unit is thermal.CELSIUS
    assert thermal.Kelvin(20).unit is thermal.KELVIN


def test_to_rejects_a_non_temperature_unit():
    with pytest.raises(InvalidConversionError, match="temperature unit"):
        thermal.Celsius(20).to(object())  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_comparison_against_a_non_temperature_raises_incompatible_dimension_error():
    with pytest.raises(IncompatibleDimensionError):
        thermal.Celsius(20) < object()  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        thermal.Celsius(20) <= object()  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        thermal.Celsius(20) > object()  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        thermal.Celsius(20) >= object()  # noqa: B015


def test_equality_against_a_non_temperature_is_false_not_an_error():
    assert (thermal.Celsius(20) == object()) is False


def test_addition_with_an_unsupported_operand_raises_type_error():
    with pytest.raises(TypeError):
        thermal.Celsius(20) + object()  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_subtraction_with_an_unsupported_operand_raises_type_error():
    with pytest.raises(TypeError):
        thermal.Celsius(20) - object()  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_repr_shows_the_display_unit_symbol():
    assert repr(thermal.Celsius(20)) == f"20 {symbols.DEGREE}C"
    assert repr(thermal.Kelvin(20)) == "20 K"


def test_kelvin_below_absolute_zero_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        thermal.Kelvin(-1)


def test_celsius_below_absolute_zero_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        thermal.Celsius(-274)


def test_absolute_zero_itself_is_a_valid_temperature():
    assert thermal.Kelvin(0).kelvin == 0
    assert thermal.Celsius(-273.15).kelvin == 0


def test_subtracting_a_delta_below_absolute_zero_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        thermal.Kelvin(5) - thermal.DeltaKelvin(10)


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
    assert thermal.Fahrenheit(fahrenheit) == thermal.Celsius(celsius)
    assert thermal.Fahrenheit(fahrenheit).value_in(thermal.CELSIUS) == celsius


def test_fahrenheit_absolute_zero_is_exactly_zero_kelvin():
    assert thermal.Fahrenheit(Decimal("-459.67")).kelvin == 0
    assert thermal.Fahrenheit(Decimal("-459.67")) == thermal.Kelvin(0)


def test_fahrenheit_below_absolute_zero_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        thermal.Fahrenheit(-460)


def test_fahrenheit_to_kelvin_keeps_the_exact_fraction():
    assert thermal.Fahrenheit(0).kelvin == Fraction(45967, 180)
    assert thermal.Fahrenheit(100).kelvin == Fraction(45967, 180) + Fraction(500, 9)


def test_fahrenheit_round_trips_through_every_temperature_unit():
    reading = thermal.Fahrenheit(Decimal("72.5"))
    for unit in (thermal.KELVIN, thermal.CELSIUS, thermal.FAHRENHEIT):
        converted = reading.to(unit)
        assert converted == reading
        assert converted.value_in(thermal.FAHRENHEIT) == Decimal("72.5")


def test_value_in_fahrenheit_is_exact_for_celsius_and_kelvin_readings():
    assert thermal.Celsius(100).value_in(thermal.FAHRENHEIT) == Decimal(212)
    assert thermal.Kelvin(0).value_in(thermal.FAHRENHEIT) == Decimal("-459.67")
    assert thermal.Celsius(Decimal(37)).value_in(thermal.FAHRENHEIT) == Decimal("98.6")


def test_fahrenheit_ordering_across_scales():
    assert thermal.Fahrenheit(31) < thermal.Celsius(0)
    assert thermal.Fahrenheit(33) > thermal.Celsius(0)
    assert thermal.Fahrenheit(-459.67) <= thermal.Kelvin(0)
    assert thermal.Fahrenheit(50) < thermal.Fahrenheit(51)


def test_fahrenheit_minus_fahrenheit_is_a_delta_in_kelvin_magnitude():
    delta = thermal.Fahrenheit(77) - thermal.Fahrenheit(68)
    assert delta == thermal.DeltaFahrenheit(9)
    assert delta == thermal.DeltaCelsius(5)
    assert delta == thermal.DeltaKelvin(5)


def test_fahrenheit_minus_celsius_is_a_delta():
    assert thermal.Fahrenheit(212) - thermal.Celsius(0) == thermal.DeltaCelsius(100)


def test_fahrenheit_plus_and_minus_a_delta_shifts_the_reading_and_keeps_its_unit():
    shifted_up = thermal.Fahrenheit(68) + thermal.DeltaFahrenheit(9)
    shifted_down = thermal.Fahrenheit(68) - thermal.DeltaFahrenheit(9)
    assert shifted_up == thermal.Fahrenheit(77)
    assert shifted_down == thermal.Fahrenheit(59)
    assert shifted_up.unit is thermal.FAHRENHEIT
    assert shifted_down.unit is thermal.FAHRENHEIT


def test_a_celsius_delta_shifts_a_fahrenheit_reading():
    assert thermal.Fahrenheit(32) + thermal.DeltaCelsius(5) == thermal.Fahrenheit(41)


def test_adding_two_fahrenheit_readings_is_rejected():
    with pytest.raises(MeasurementError, match="point on a scale"):
        thermal.Fahrenheit(68) + thermal.Fahrenheit(9)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_fahrenheit_cannot_be_scaled_by_a_number():
    with pytest.raises(TypeError):
        thermal.Fahrenheit(68) * 2  # type: ignore[operator]  # ty: ignore[unsupported-operator]

    with pytest.raises(TypeError):
        2 * thermal.Fahrenheit(68)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_delta_fahrenheit_behaves_like_an_ordinary_linear_quantity():
    assert thermal.DeltaFahrenheit(9) + thermal.DeltaFahrenheit(
        9
    ) == thermal.DeltaFahrenheit(18)
    assert thermal.DeltaFahrenheit(9) * 2 == thermal.DeltaFahrenheit(18)
    assert thermal.DeltaFahrenheit(9) / 3 == thermal.DeltaFahrenheit(3)


def test_delta_fahrenheit_is_five_ninths_of_a_delta_kelvin():
    assert thermal.DeltaFahrenheit(9) == thermal.DeltaKelvin(5)
    assert thermal.DELTA_FAHRENHEIT.scale == Fraction(5, 9)
    assert thermal.DeltaFahrenheit(9).magnitude == Decimal(5)


def test_fahrenheit_unit_property_and_repr():
    assert thermal.Fahrenheit(68).unit is thermal.FAHRENHEIT
    assert repr(thermal.Fahrenheit(68)) == f"68 {symbols.DEGREE}F"
    assert repr(thermal.DeltaFahrenheit(9)) == f"9 {symbols.DELTA}{symbols.DEGREE}F"


def test_fahrenheit_is_registered_in_the_unit_tables():
    assert thermal.TEMPERATURE_UNITS["F"] is thermal.Fahrenheit
    assert thermal.TEMPERATURE_DELTA_UNITS["dF"] is thermal.DeltaFahrenheit


def test_fahrenheit_is_a_temperature():
    assert isinstance(thermal.Fahrenheit(68), Temperature)
    assert isinstance(thermal.DeltaFahrenheit(9), TemperatureDelta)


def test_rankine_is_the_fahrenheit_degree_from_absolute_zero():
    assert thermal.Rankine(0) == thermal.Kelvin(0)
    assert thermal.Rankine(Decimal("459.67")) == thermal.Fahrenheit(0)
    assert thermal.Rankine(Decimal("491.67")) == thermal.Celsius(0)
    assert thermal.Rankine(9).kelvin == thermal.Kelvin(5).kelvin


def test_rankine_below_absolute_zero_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        thermal.Rankine(-1)


def test_a_rankine_difference_is_a_fahrenheit_difference():
    assert thermal.Rankine(530) - thermal.Rankine(521) == thermal.DeltaRankine(9)
    assert thermal.DeltaRankine(9) == thermal.DeltaFahrenheit(9)
    assert thermal.DeltaRankine(9) == thermal.DeltaKelvin(5)
    assert thermal.Rankine(500) + thermal.DeltaFahrenheit(9) == thermal.Rankine(509)


def test_rankine_displays_in_its_own_unit():
    assert repr(thermal.Rankine(491.67)) == "491.67 \u00b0R"
    assert thermal.Celsius(0).to(thermal.RANKINE).unit is thermal.RANKINE


def test_a_prefixed_kelvin_is_exact_in_kelvin():
    assert thermal.Millikelvin(1) == thermal.Kelvin(Decimal("0.001"))
    assert thermal.Microkelvin(1_000_000) == thermal.Kelvin(1)
    assert thermal.Microkelvin(999) < thermal.Millikelvin(1)


def test_a_prefixed_celsius_keeps_the_zero_of_the_celsius_scale():
    assert thermal.Millicelsius(0) == thermal.Kelvin(Decimal("273.15"))
    assert thermal.Microcelsius(0) == thermal.Celsius(0)
    assert thermal.Millicelsius(25_000) == thermal.Celsius(25)
    assert thermal.Microcelsius(25_000_000) == thermal.Celsius(25)


def test_a_reading_converts_exactly_to_a_prefixed_unit_and_back():
    reading = thermal.Celsius(Decimal("36.6"))
    shown = reading.to(thermal.MILLICELSIUS)
    assert shown.value_in(thermal.MILLICELSIUS) == Decimal(36_600)
    assert shown.to(thermal.CELSIUS).value_in(thermal.CELSIUS) == Decimal("36.6")


def test_a_prefixed_reading_shows_its_unit():
    assert repr(thermal.Millicelsius(42_000)) == "42000 m\u00b0C"
    assert repr(thermal.Microkelvin(150)) == f"150 {symbols.MICRO}K"


@pytest.mark.parametrize(
    ("reading", "absolute_zero"),
    [
        (thermal.Millikelvin, 0),
        (thermal.Microkelvin, 0),
        (thermal.Millicelsius, -273_150),
        (thermal.Microcelsius, -273_150_000),
    ],
)
def test_a_prefixed_reading_below_absolute_zero_is_rejected(reading, absolute_zero):
    assert reading(absolute_zero) == thermal.Kelvin(0)
    with pytest.raises(InvalidMeasurementError):
        reading(absolute_zero - 1)


def test_a_prefixed_difference_is_the_same_size_in_kelvin_and_celsius():
    assert thermal.DeltaMillicelsius(5) == thermal.DeltaMillikelvin(5)
    assert thermal.DeltaMicrocelsius(5) == thermal.DeltaMicrokelvin(5)
    assert thermal.DeltaMillikelvin(5) == thermal.DeltaKelvin(Decimal("0.005"))
    assert thermal.DeltaMicrokelvin(1000) == thermal.DeltaMillikelvin(1)


def test_a_prefixed_difference_shifts_a_reading_and_the_reading_keeps_its_unit():
    shifted = thermal.Millikelvin(10) + thermal.DeltaMicrokelvin(500)
    assert shifted == thermal.Millikelvin(Decimal("10.5"))
    assert shifted.unit == thermal.MILLIKELVIN
    assert thermal.Millicelsius(25_000) - thermal.Millicelsius(20_000) == (
        thermal.DeltaMillicelsius(5_000)
    )
