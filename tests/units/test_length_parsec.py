"""The parsec: 648000/pi astronomical units, with pi to 100 decimal places."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from kuchka import Length
from kuchka import parse
from kuchka.internal.constants import PI
from kuchka.units import angular
from kuchka.units import length


def test_a_parsec_is_the_distance_at_which_an_au_subtends_an_arcsecond() -> None:
    au = length.AstronomicalUnit(1)
    arcsecond = angular.ArcSecond(1).value_in(angular.RADIAN)
    assert length.Parsec(1).value_in(length.ASTRONOMICAL_UNIT) * arcsecond == 1
    assert length.Parsec(1) * arcsecond == au


def test_a_parsec_is_648000_over_pi_astronomical_units() -> None:
    assert length.PARSEC.scale == Fraction(648000) * length.ASTRONOMICAL_UNIT.scale / PI


def test_a_parsec_agrees_with_the_iau_value_to_all_the_published_digits() -> None:
    published = Fraction("30856775814913672.789139379577965")
    error = abs(length.Parsec(1).value_in(length.METRE) - published)
    assert error < Fraction(1, 10**12)


def test_a_parsec_is_about_3_26_light_years_and_206265_au() -> None:
    in_light_years = length.Parsec(1).value_in(length.LIGHT_YEAR)
    assert Fraction("3.26156377716743") < in_light_years < Fraction("3.26156377716744")
    in_au = length.Parsec(1).value_in(length.ASTRONOMICAL_UNIT)
    assert Fraction("206264.80624709") < in_au < Fraction("206264.80624710")


def test_the_multiples_of_the_parsec_are_exact() -> None:
    assert length.Kiloparsec(1) == length.Parsec(1000)
    assert length.Megaparsec(1) == length.Parsec(1_000_000)
    assert length.Gigaparsec(1) == length.Megaparsec(1000)
    assert length.Megaparsec(Fraction(1, 3)) * 3 == length.Megaparsec(1)


def test_a_parsec_value_round_trips_through_its_own_unit() -> None:
    reading = length.Parsec(Fraction(22, 7))
    assert reading.value_in(length.PARSEC) == Fraction(22, 7)
    assert type(reading) is Length


def test_the_parsec_texts_are_read_as_lengths() -> None:
    assert parse("1.3 pc", Length) == length.Parsec(Decimal("1.3"))
    assert parse("0.78 Mpc", Length) == length.Megaparsec(Decimal("0.78"))
    assert parse("4 parsec", Length) == length.Parsec(4)
