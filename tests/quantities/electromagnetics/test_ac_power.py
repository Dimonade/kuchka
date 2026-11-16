"""ApparentPower and ReactivePower: the volt-ampere and the var, roles of Power.

The generic role behaviour (refusals, scaling) is covered once for every role in
`test_role_kinds`; this module covers what is specific to the two AC powers.
"""

from __future__ import annotations

import pytest

from kuchka import ApparentPower
from kuchka import IncompatibleDimensionError
from kuchka import Power
from kuchka import Proportion
from kuchka import ReactivePower
from kuchka.units import proportion
from kuchka.units.electromagnetics import ac_power
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import power
from kuchka.units.temporal import time


def test_the_headroom_of_a_transformer_is_an_apparent_power() -> None:
    headroom = ac_power.KilovoltAmpere(5) - ac_power.VoltAmpere(3200)
    assert isinstance(headroom, ApparentPower)
    assert headroom == ac_power.VoltAmpere(1800)
    assert repr(headroom) == "1.8 kVA"


def test_an_inductive_balance_is_a_negative_reactive_power() -> None:
    balance = ac_power.Kilovar(2) - ac_power.Kilovar(3.5)
    assert isinstance(balance, ReactivePower)
    assert balance == ac_power.Var(-1500)
    assert repr(balance) == "-1.5 kvar"


def test_the_three_powers_do_not_add() -> None:
    with pytest.raises(IncompatibleDimensionError):
        ac_power.VoltAmpere(1) + ac_power.Var(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(IncompatibleDimensionError):
        ac_power.VoltAmpere(1) + power.Watt(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(IncompatibleDimensionError):
        ac_power.Var(1) + power.Watt(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (ac_power.KilovoltAmpere(5), power.Kilowatt(5)),
        (ac_power.Kilovar(2), power.Kilowatt(2)),
    ],
    ids=["apparent", "reactive"],
)
def test_to_power_carries_the_value_over(value, expected) -> None:
    taken = value.to_power()
    assert isinstance(taken, Power)
    assert taken == expected


def test_an_apparent_power_over_a_time_is_not_taken_for_an_energy() -> None:
    supply = ac_power.VoltAmpere(5)
    with pytest.raises(IncompatibleDimensionError, match="to_power"):
        supply * time.Second(2)
    assert supply.to_power() * time.Second(2) == energy.Joule(10)


def test_the_ratio_of_two_apparent_powers_is_a_proportion() -> None:
    load = ac_power.VoltAmpere(3200) / ac_power.KilovoltAmpere(5)
    assert isinstance(load, Proportion)
    assert load == proportion.Ratio(0.64)


def test_a_proportion_of_a_reactive_power_is_a_reactive_power() -> None:
    half = proportion.Percent(50) * ac_power.Kilovar(2)
    assert isinstance(half, ReactivePower)
    assert half == ac_power.Kilovar(1)


def test_the_var_reads_as_it_is_written_on_a_nameplate() -> None:
    table = ac_power.REACTIVE_POWER_UNITS
    assert table["kVAR"](2) == ac_power.Kilovar(2)
    assert table["MVAr"](3) == ac_power.Megavar(3)
    assert table["var"](1) == ac_power.Var(1)
