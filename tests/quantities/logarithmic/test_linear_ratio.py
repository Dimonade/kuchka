"""A level converts to and from a linear power or field ratio."""

from __future__ import annotations

from decimal import Decimal
from decimal import localcontext

import pytest

from kuchka import InvalidMeasurementError
from kuchka import LogarithmicRatio
from kuchka import Proportion
from kuchka.units import logarithmic
from kuchka.units import proportion


@pytest.mark.parametrize(
    ("level", "power", "field"),
    [
        (0, Decimal(1), Decimal(1)),
        (10, Decimal(10), None),
        (20, Decimal(100), Decimal(10)),
        (30, Decimal(1000), None),
        (40, Decimal(10_000), Decimal(100)),
        (-10, Decimal("0.1"), None),
        (-20, Decimal("0.01"), Decimal("0.1")),
        (-40, Decimal("0.0001"), Decimal("0.01")),
    ],
)
def test_whole_decades_convert_exactly(level, power, field):
    assert logarithmic.Decibel(level).to_power_ratio() == proportion.Ratio(power)
    if field is not None:
        assert logarithmic.Decibel(level).to_field_ratio() == proportion.Ratio(field)


def test_conversion_result_is_a_proportion_in_the_ratio_unit():
    ratio = logarithmic.Decibel(30).to_power_ratio()
    assert isinstance(ratio, Proportion)
    assert ratio.unit is proportion.RATIO
    assert logarithmic.Decibel(-20).to_field_ratio() == proportion.Percent(10)


def test_three_decibels_is_close_to_a_factor_of_two_but_not_exactly():
    power = logarithmic.Decibel(3).to_power_ratio()
    assert power != proportion.Ratio(2)
    assert float(power.magnitude) == pytest.approx(1.9952623149688795, rel=1e-15)


def test_six_decibels_of_voltage_is_the_same_ratio_as_three_of_power():
    assert (
        logarithmic.Decibel(6).to_field_ratio()
        == logarithmic.Decibel(3).to_power_ratio()
    )


def test_conversion_precision_follows_the_decimal_context():
    with localcontext() as context:
        context.prec = 10
        assert logarithmic.Decibel(3).to_power_ratio() == proportion.Ratio(
            Decimal("1.995262315")
        )


def test_bel_display_unit_does_not_change_the_ratio():
    assert (
        logarithmic.Bel(3).to_power_ratio() == logarithmic.Decibel(30).to_power_ratio()
    )


@pytest.mark.parametrize("level", [10**9, -(10**9)], ids=["overflow", "underflow"])
def test_levels_beyond_the_decimal_range_are_rejected(level):
    with pytest.raises(InvalidMeasurementError, match="outside the range"):
        logarithmic.Decibel(level).to_power_ratio()
    with pytest.raises(InvalidMeasurementError, match="outside the range"):
        logarithmic.Decibel(level).to_field_ratio()


@pytest.mark.parametrize(
    ("ratio", "power_level", "field_level"),
    [
        (proportion.Ratio(1), 0, 0),
        (proportion.Ratio(10), 10, 20),
        (proportion.Ratio(100), 20, 40),
        (proportion.Ratio(1000), 30, 60),
        (proportion.Ratio(Decimal("0.1")), -10, -20),
        (proportion.Percent(1), -20, -40),
        (proportion.Percent(100), 0, 0),
    ],
)
def test_powers_of_ten_convert_to_exact_levels(ratio, power_level, field_level):
    assert LogarithmicRatio.from_power_ratio(ratio) == logarithmic.Decibel(power_level)
    assert LogarithmicRatio.from_field_ratio(ratio) == logarithmic.Decibel(field_level)


def test_from_ratio_returns_a_decibel_display_level():
    level = LogarithmicRatio.from_power_ratio(proportion.Ratio(100))
    assert isinstance(level, LogarithmicRatio)
    assert level.unit is logarithmic.DECIBEL


def test_a_factor_of_two_is_about_three_decibels_of_power_and_six_of_voltage():
    power = LogarithmicRatio.from_power_ratio(proportion.Ratio(2))
    field = LogarithmicRatio.from_field_ratio(proportion.Ratio(2))
    assert float(power.magnitude) == pytest.approx(3.010299956639812, rel=1e-15)
    assert float(field.magnitude) == pytest.approx(6.020599913279624, rel=1e-15)
    assert field == power * 2


@pytest.mark.parametrize(
    "bad", [proportion.Ratio(0), proportion.Ratio(-1), proportion.Percent(-5)]
)
def test_a_non_positive_ratio_has_no_level(bad):
    with pytest.raises(InvalidMeasurementError, match="positive ratio"):
        LogarithmicRatio.from_power_ratio(bad)
    with pytest.raises(InvalidMeasurementError, match="positive ratio"):
        LogarithmicRatio.from_field_ratio(bad)
