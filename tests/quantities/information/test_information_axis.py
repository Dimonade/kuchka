"""The information axis: why data and data rate have dimensions of their own."""

from __future__ import annotations

from kuchka.dimensions import DATA
from kuchka.dimensions import DATA_RATE
from kuchka.dimensions import DIMENSIONLESS
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.dimensions import Dimension


def test_data_is_not_dimensionless() -> None:
    assert DATA != DIMENSIONLESS
    assert Dimension(information=1) == DATA


def test_a_data_rate_is_data_per_time_and_not_a_frequency() -> None:
    assert DATA_RATE == DATA / TIME
    assert DATA_RATE != FREQUENCY
    assert DATA_RATE * TIME == DATA


def test_the_information_axis_cancels_in_a_quotient_of_data() -> None:
    assert DATA / DATA == DIMENSIONLESS


def test_the_information_axis_shows_as_d() -> None:
    assert repr(DATA) == "D¹"
    assert repr(DATA_RATE) == "T⁻¹ D¹"
