"""Impulse: the newton second and its kin, and its place beside momentum.

The generic contracts run for every unit of the table; this module covers what is
specific to impulse.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from kuchka import AmbiguousKindError
from kuchka import Force
from kuchka import Impulse
from kuchka import InvalidConversionError
from kuchka import Momentum
from kuchka import Time
from kuchka import Velocity
from kuchka import parse
from kuchka.units import mass
from kuchka.units import temporal
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import force
from kuchka.units.mechanics import impulse as imp
from kuchka.units.mechanics import momentum


def test_a_dyne_second_is_exactly_a_gram_centimetre_per_second_of_impulse() -> None:
    assert imp.DyneSecond(100_000) == imp.NewtonSecond(1)
    assert imp.DyneSecond(1).to_momentum() == momentum.GramCentimetrePerSecond(1)


def test_the_prefixed_newton_seconds_are_exact() -> None:
    assert imp.MillinewtonSecond(1000) == imp.NewtonSecond(1)
    assert imp.KilonewtonSecond(1) == imp.NewtonSecond(1000)


def test_a_pound_force_second_is_exactly_the_pound_force_in_newton_seconds() -> None:
    assert imp.PoundForceSecond(1) == imp.NewtonSecond(Decimal("4.4482216152605"))


def test_a_mixed_unit_log_adds_exactly() -> None:
    total = imp.NewtonSecond(10) + imp.PoundForceSecond(2)
    assert total == imp.NewtonSecond(Decimal("18.896443230521"))


def test_a_force_times_a_time_is_an_impulse_in_either_order() -> None:
    burn = force.Newton(20) * temporal.Second(3)
    assert type(burn) is Impulse
    assert burn == imp.NewtonSecond(60)
    assert type(temporal.Second(3) * force.Newton(20)) is Impulse


def test_the_quotients_of_an_impulse() -> None:
    burn = imp.NewtonSecond(60)
    assert type(burn / temporal.Second(3)) is Force
    assert type(burn / force.Newton(20)) is Time
    assert burn / mass.Kilogram(12) == velocity.MetrePerSecond(5)
    assert type(burn / mass.Kilogram(12)) is Velocity


def test_an_impulse_and_a_momentum_convert_explicitly() -> None:
    assert imp.NewtonSecond(6).to_momentum() == momentum.KilogramMetrePerSecond(6)
    assert Impulse.from_momentum(
        momentum.KilogramMetrePerSecond(6)
    ) == imp.NewtonSecond(6)
    assert type(imp.NewtonSecond(6).to_momentum()) is Momentum


def test_an_energy_over_a_velocity_is_ambiguous_between_the_two() -> None:
    with pytest.raises(AmbiguousKindError, match="Momentum, Impulse"):
        energy.Joule(1) / velocity.MetrePerSecond(1)


def test_a_momentum_unit_is_not_an_impulse_unit() -> None:
    with pytest.raises(InvalidConversionError, match="not a unit of Impulse"):
        imp.NewtonSecond(1).to(momentum.KILOGRAM_METRE_PER_SECOND)


def test_text_resolves_through_the_table() -> None:
    assert parse("60 N·s", Impulse) == imp.NewtonSecond(60)
    assert parse("60 N s", Impulse) == imp.NewtonSecond(60)
    assert parse("13.5 lbf s", Impulse) == imp.PoundForceSecond(Decimal("13.5"))
