"""The kind of a product or quotient: preserved, ruled, or decided by the dimension.

In order: a dimensionless result is a plain `Fraction`; a dimensionless operand keeps
the other operand's kind; an explicit rule names the kind; otherwise the principal
kind of the dimension is the result, and a contested dimension raises
`AmbiguousKindError`.
No shipped dimension is contested, so the contested cases build one from real kinds
that share a dimension: `Frequency` and `SampleRate`.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AmbiguousKindError
from kuchka import Ampere
from kuchka import BaudRate
from kuchka import Charge
from kuchka import Current
from kuchka import Frequency
from kuchka import Length
from kuchka import Metre
from kuchka import MetrePerSecond
from kuchka import MetrePerSecondSquared
from kuchka import Percent
from kuchka import Power
from kuchka import Proportion
from kuchka import Ratio
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka import Second
from kuchka import Time
from kuchka import Velocity
from kuchka import Volt
from kuchka import Voltage
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.quantities.base import registry

SAMPLE_RATE = SampleRate(Fraction(8), SampleRate._canonical_unit)  # noqa: SLF001
SAMPLING_PERIOD = SamplingPeriod(Fraction(1, 8), SamplingPeriod._canonical_unit)  # noqa: SLF001
BAUD_RATE = BaudRate(Fraction(9600), BaudRate._canonical_unit)  # noqa: SLF001


# A dimensionless operand keeps the kind.


@pytest.mark.parametrize(
    ("quantity", "kind"),
    [
        (SAMPLE_RATE, SampleRate),
        (SAMPLING_PERIOD, SamplingPeriod),
        (BAUD_RATE, BaudRate),
        (Volt(3), Voltage),
    ],
    ids=lambda value: (
        type(value).__name__ if not isinstance(value, type) else value.__name__
    ),
)
@pytest.mark.parametrize("scale", [Ratio(2), Percent(50)], ids=["ratio", "percent"])
def test_a_proportion_keeps_the_kind_of_the_other_operand(
    quantity: object, kind: type, scale: Proportion
) -> None:
    for result in (quantity * scale, scale * quantity, quantity / scale):  # type: ignore[operator]
        assert type(result) is kind


def test_a_scaled_role_keeps_its_own_unit_and_value() -> None:
    assert (SAMPLE_RATE * Percent(50)).magnitude == Fraction(4)
    assert str(SAMPLE_RATE * Percent(50)) == "4 Sa/s"
    assert str(BAUD_RATE * Percent(50)) == "4800 Bd"
    assert (SAMPLING_PERIOD / Percent(50)).magnitude == Fraction(1, 4)


def test_a_proportion_does_not_divide_into_a_kind() -> None:
    assert type(Ratio(1) / SAMPLING_PERIOD) is Frequency


# Otherwise the dimension decides.


def test_a_product_of_two_quantities_takes_the_principal_kind() -> None:
    assert type(Volt(5) * Ampere(2)) is Power
    assert type(Second(1) / Second(2)) is Fraction


def test_a_dimensionless_result_is_a_plain_fraction() -> None:
    assert Percent(50) * Percent(50) == Fraction(1, 4)
    assert type(SAMPLE_RATE * Second(2)) is Fraction


def test_the_reciprocal_of_a_role_is_still_its_own_partner() -> None:
    assert type(1 / SAMPLING_PERIOD) is SampleRate
    assert type(1 / Second(2)) is Frequency


# Contested dimensions.


@pytest.fixture
def open_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(registry, "_closed", False)
    for name in (
        "_KINDS_BY_DIMENSION",
        "_DIMENSION_REGISTRY",
        "_CONTESTED",
        "_SPECIALISATIONS",
        "_RULES",
    ):
        monkeypatch.setattr(registry, name, dict(getattr(registry, name)))


@pytest.fixture
def contested_frequency(open_registry: None) -> None:
    del open_registry
    registry._DIMENSION_REGISTRY.pop(FREQUENCY)  # noqa: SLF001
    registry._SPECIALISATIONS.pop(SampleRate)  # noqa: SLF001
    registry._CONTESTED[FREQUENCY] = (Frequency, SampleRate)  # noqa: SLF001


@pytest.mark.usefixtures("contested_frequency")
def test_a_contested_result_without_a_rule_is_ambiguous() -> None:
    with pytest.raises(AmbiguousKindError, match="Frequency, SampleRate") as caught:
        MetrePerSecondSquared(6) / MetrePerSecond(3)
    assert caught.value.candidates == (Frequency, SampleRate)
    assert "construct the one you mean" in str(caught.value)


@pytest.mark.usefixtures("contested_frequency")
def test_a_rule_names_the_kind_of_a_contested_result() -> None:
    registry._rule(Velocity, "/", Length, SampleRate)  # noqa: SLF001
    result = MetrePerSecond(10) / Metre(2)
    assert type(result) is SampleRate
    assert result.magnitude == Fraction(5)


@pytest.mark.usefixtures("contested_frequency")
def test_a_rule_decides_only_its_own_operands() -> None:
    registry._rule(Velocity, "/", Length, SampleRate)  # noqa: SLF001
    with pytest.raises(AmbiguousKindError):
        MetrePerSecondSquared(6) / MetrePerSecond(3)


@pytest.mark.usefixtures("contested_frequency")
def test_a_contested_kind_keeps_its_kind_when_scaled() -> None:
    frequency = Frequency(Fraction(4), Frequency._canonical_unit)  # noqa: SLF001
    assert type(frequency * Ratio(2)) is Frequency
    assert type(SAMPLE_RATE * Ratio(2)) is SampleRate


@pytest.mark.usefixtures("contested_frequency")
def test_the_reciprocal_of_a_contested_kind_is_resolved_by_dimension() -> None:
    assert type(1 / Frequency(Fraction(4), Frequency._canonical_unit)) is Time  # noqa: SLF001


# Declaring a rule.


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
    registry._rule(Voltage, "*", Current, Power)  # noqa: SLF001
    registry._rule(Current, "*", Voltage, Power)  # noqa: SLF001
    assert len(registry._RULES) == 2  # noqa: PLR2004, SLF001


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
    assert type(MetrePerSecond(10) / Metre(2)) is Frequency


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
