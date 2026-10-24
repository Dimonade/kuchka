"""The error a division by zero raises."""

from __future__ import annotations

import pytest

import kuchka
import kuchka.errors
from kuchka import DivisionByZeroError
from kuchka import MeasurementError
from kuchka.units import voltage


def test_the_error_is_both_a_measurement_error_and_a_zero_division_error() -> None:
    assert issubclass(DivisionByZeroError, MeasurementError)
    assert issubclass(DivisionByZeroError, ZeroDivisionError)


def test_the_error_is_exported_at_the_top_level() -> None:
    assert kuchka.DivisionByZeroError is kuchka.errors.DivisionByZeroError
    assert "DivisionByZeroError" in kuchka.__all__


def test_the_message_quotes_both_operands() -> None:
    with pytest.raises(DivisionByZeroError) as caught:
        voltage.Volt(1) / voltage.Volt(0)
    assert str(caught.value) == "cannot divide 1 V by 0 V: the divisor is zero."


def test_the_operands_are_attributes_of_the_error() -> None:
    with pytest.raises(DivisionByZeroError) as caught:
        voltage.Volt(5) / 0
    assert caught.value.dividend == voltage.Volt(5)
    assert caught.value.divisor == 0


def test_either_base_class_catches_it() -> None:
    with pytest.raises(MeasurementError):
        voltage.Volt(1) / 0
    with pytest.raises(ZeroDivisionError):
        voltage.Volt(1) / 0
