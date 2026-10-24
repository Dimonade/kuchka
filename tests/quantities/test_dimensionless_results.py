"""Dimensionless results: a ratio of like quantities is a `Proportion`."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Proportion
from kuchka.units import proportion
from kuchka.units.electromagnetics import conductance
from kuchka.units.electromagnetics import resistance
from kuchka.units.electromagnetics import voltage
from kuchka.units.mechanics import energy_density as edens
from kuchka.units.mechanics import pressure
from kuchka.units.temporal import frequency
from kuchka.units.temporal import time
from tests.support.families import FAMILIES
from tests.support.families import FAMILY_IDS


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_the_quotient_of_two_like_quantities_is_a_proportion(family) -> None:
    ratio = family.canonical(12) / family.canonical(3)
    assert type(ratio) is Proportion
    assert ratio == proportion.Ratio(4)


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_no_linear_family_is_built_from_a_proportion(family) -> None:
    with pytest.raises(InvalidMeasurementError):
        family.canonical(proportion.Ratio(2))


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_every_linear_family_is_still_built_from_an_exact_fraction(family) -> None:
    assert family.canonical(Fraction(5, 2)) == family.canonical(2.5)


def test_a_quantity_built_from_a_ratio_of_like_quantities_is_refused() -> None:
    ratio = voltage.Volt(5) / voltage.Volt(2)
    with pytest.raises(InvalidMeasurementError):
        voltage.Volt(ratio)
    assert voltage.Volt(ratio.magnitude) == voltage.Volt(Fraction(5, 2))


def test_the_ratio_of_like_quantities_is_exact() -> None:
    ratio = voltage.Volt(1) / voltage.Volt(3)
    assert ratio.magnitude == Fraction(1, 3)


def test_a_product_of_two_proportions_is_a_proportion() -> None:
    product = proportion.Percent(50) * proportion.Percent(50)
    assert type(product) is Proportion
    assert product == proportion.Ratio(Fraction(1, 4))


def test_a_derived_proportion_displays_as_the_coherent_ratio() -> None:
    assert repr(proportion.Percent(50) * proportion.Percent(50)) == "0.25 1"
    assert repr(voltage.Volt(5) / voltage.Volt(2)) == "2.5 1"


def test_kinds_that_share_a_dimension_divide_to_a_proportion() -> None:
    stress = pressure.Pascal(6)
    density = edens.JoulePerCubicMetre(3)
    assert stress / density == proportion.Ratio(2)
    assert density / stress == proportion.Ratio(Fraction(1, 2))


def test_a_ratio_compares_with_a_proportion_and_not_with_a_plain_number() -> None:
    ratio = voltage.Volt(5) / voltage.Volt(2)
    assert ratio > proportion.Ratio(2)
    with pytest.raises(IncompatibleDimensionError):
        ratio > 2  # noqa: B015, PLR2004 -- the comparison raises


def test_a_dimensionless_result_of_unlike_quantities_is_a_plain_fraction() -> None:
    cycles = frequency.Hertz(2) * time.Second(3)
    assert type(cycles) is Fraction
    assert cycles == Fraction(6)
    assert type(conductance.Siemens(2) * resistance.Ohm(3)) is Fraction
