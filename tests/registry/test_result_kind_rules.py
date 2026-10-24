"""Declaring a rule for the operand kinds."""

from __future__ import annotations

import pytest

from kuchka import Charge
from kuchka import Current
from kuchka import Frequency
from kuchka import Length
from kuchka import Power
from kuchka import Proportion
from kuchka import SampleRate
from kuchka import Time
from kuchka import Velocity
from kuchka import Voltage
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.quantities.base import registry
from kuchka.units import length
from kuchka.units import velocity


def test_a_rule_after_the_close_is_refused() -> None:
    with pytest.raises(RuntimeError, match="closed"):
        registry._rule(Voltage, "*", Current, Power)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_product_rule_holds_in_both_operand_orders() -> None:
    registry._rule(Voltage, "*", Current, Power)  # noqa: SLF001
    assert registry._RULES[(Voltage, "*", Current)] is Power  # noqa: SLF001
    assert registry._RULES[(Current, "*", Voltage)] is Power  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_quotient_rule_holds_in_one_order() -> None:
    registry._rule(Power, "/", Voltage, Current)  # noqa: SLF001
    assert (Voltage, "/", Power) not in registry._RULES  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_stating_a_rule_again_is_not_an_error() -> None:
    before = len(registry._RULES)  # noqa: SLF001
    registry._rule(Voltage, "*", Current, Power)  # noqa: SLF001
    registry._rule(Current, "*", Voltage, Power)  # noqa: SLF001
    assert len(registry._RULES) - before == 2  # noqa: PLR2004, SLF001


@pytest.mark.usefixtures("open_registry")
@pytest.mark.parametrize(
    ("left", "operation", "right", "result", "match"),
    [
        (Voltage, "+", Current, Power, "'\\*' or '/'"),
        (Voltage, "*", Proportion, Voltage, "operand of a rule"),
        (Proportion, "*", Voltage, Voltage, "operand of a rule"),
        (Voltage, "*", Current, Time, "cannot be its result"),
        (Voltage, "*", Current, SampleRate, "cannot be its result"),
        (Charge, "/", Current, Frequency, "cannot be its result"),
    ],
    ids=[
        "operation",
        "right-dimensionless",
        "left-dimensionless",
        "dimension",
        "role",
        "result",
    ],
)
def test_a_rule_that_does_not_fit_is_refused(
    left: type, operation: str, right: type, result: type, match: str
) -> None:
    before = dict(registry._RULES)  # noqa: SLF001
    with pytest.raises(TypeError, match=match):
        registry._rule(left, operation, right, result)  # type: ignore[arg-type]  # noqa: SLF001
    assert before == registry._RULES  # noqa: SLF001


@pytest.mark.usefixtures("contested_frequency")
def test_a_rule_contradicting_another_is_refused() -> None:
    registry._rule(Velocity, "/", Length, SampleRate)  # noqa: SLF001
    with pytest.raises(TypeError, match="already SampleRate"):
        registry._rule(Velocity, "/", Length, Frequency)  # noqa: SLF001
    assert registry._RULES[(Velocity, "/", Length)] is SampleRate  # noqa: SLF001


@pytest.mark.usefixtures("contested_frequency")
def test_a_contested_kind_can_be_the_result_of_a_rule() -> None:
    registry._rule(Velocity, "/", Length, Frequency)  # noqa: SLF001
    assert type(velocity.MetrePerSecond(10) / length.Metre(2)) is Frequency


def test_every_shipped_rule_fits_the_dimension_it_produces() -> None:
    for (left, operation, right), result in registry._RULES.items():  # noqa: SLF001
        expected = (
            left.dimension * right.dimension
            if operation == "*"
            else left.dimension / right.dimension
        )
        assert result.dimension == expected
        assert result in registry._arithmetic_roots(expected)  # noqa: SLF001


def test_time_and_frequency_are_unaffected() -> None:
    assert registry._DIMENSION_REGISTRY[TIME] is Time  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[FREQUENCY] is Frequency  # noqa: SLF001
