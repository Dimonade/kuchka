from decimal import Decimal

import pytest
from kuchka import Celsius
from kuchka import DeltaCelsius
from kuchka import DeltaKelvin
from kuchka import Kelvin
from kuchka import MeasurementError
from kuchka import Temperature
from kuchka.temperature import KELVIN


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
    with pytest.raises(MeasurementError, match="not a vector"):
        Celsius(20) + Celsius(5)


def test_temperature_cannot_be_scaled_by_a_number():
    with pytest.raises(TypeError):
        Celsius(20) * 2

    with pytest.raises(TypeError):
        2 * Celsius(20)

    with pytest.raises(TypeError):
        Kelvin(300) * 2


def test_temperature_ordering():
    assert Celsius(0) < Celsius(100)
    assert Kelvin(0) < Celsius(0)  # 0 K is colder than 0 degC


def test_temperature_delta_behaves_like_an_ordinary_linear_quantity():
    assert DeltaCelsius(5) + DeltaCelsius(5) == DeltaCelsius(10)
    assert DeltaCelsius(5) * 2 == DeltaCelsius(10)
