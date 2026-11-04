"""A role kind combines with a plain number, a proportion, itself and its reciprocal."""

from __future__ import annotations

import operator
from fractions import Fraction

import pytest

from kuchka import AbsorbedDose
from kuchka import AbsorbedDoseRate
from kuchka import Activity
from kuchka import ApparentPower
from kuchka import BaudRate
from kuchka import CatalyticActivity
from kuchka import Entropy
from kuchka import EquivalentDose
from kuchka import EquivalentDoseRate
from kuchka import Exposure
from kuchka import ExposureRate
from kuchka import Impedance
from kuchka import IncompatibleDimensionError
from kuchka import Magnetization
from kuchka import MolarEntropy
from kuchka import Reactance
from kuchka import ReactivePower
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka import SpecificEntropy
from kuchka import Stress
from kuchka import Time
from kuchka.dimensions import DIMENSIONLESS
from kuchka.quantities.base import registry
from kuchka.units import proportion
from kuchka.units.temporal import baud_rate
from kuchka.units.temporal import sample_rate
from kuchka.units.temporal import time
from tests.support.families import FAMILIES

ROLES = [f for f in FAMILIES if f.quantity in registry._SPECIALISATIONS]  # noqa: SLF001
ROLE_IDS = [f.id for f in ROLES]
OTHERS = [f for f in FAMILIES if f.canonical_unit.dimension != DIMENSIONLESS]
CONVERSION = {
    AbsorbedDose: "to_specific_energy",
    AbsorbedDoseRate: "to_specific_power",
    Activity: "to_frequency",
    ApparentPower: "to_power",
    BaudRate: "no conversion",
    CatalyticActivity: "to_molar_flow_rate",
    Entropy: "to_heat_capacity",
    MolarEntropy: "to_molar_heat_capacity",
    EquivalentDose: "no conversion",
    EquivalentDoseRate: "no conversion",
    Exposure: "to_specific_charge",
    ExposureRate: "to_specific_current",
    SpecificEntropy: "to_specific_heat_capacity",
    Impedance: "to_resistance",
    Magnetization: "to_magnetic_field_strength",
    Reactance: "to_resistance",
    ReactivePower: "to_power",
    SampleRate: "to_frequency",
    SamplingPeriod: "to_time",
    Stress: "to_pressure",
}


def _is_ruled(role: type, other: type) -> bool:
    """Return whether a rule names a product or quotient of the two kinds."""
    return any(
        (left, operation, right) in registry._RULES  # noqa: SLF001
        for operation in ("*", "/")
        for left, right in ((role, other), (other, role))
    )


REFUSED = [
    (role, other)
    for role in ROLES
    for other in OTHERS
    if other.quantity is not role.quantity
    and {role.quantity, other.quantity} != {SampleRate, SamplingPeriod}
    and not _is_ruled(role.quantity, other.quantity)
]


@pytest.mark.parametrize(
    ("role", "other"), REFUSED, ids=[f"{r.id}-{o.id}" for r, o in REFUSED]
)
def test_a_role_is_refused_with_any_other_quantity(role, other) -> None:
    left, right = role.canonical(12), other.canonical(3)
    for combine in (operator.mul, operator.truediv):
        for a, b in ((left, right), (right, left)):
            with pytest.raises(IncompatibleDimensionError, match=r"role|conversion"):
                combine(a, b)


@pytest.mark.parametrize("role", ROLES, ids=ROLE_IDS)
def test_the_refusal_names_the_conversion_out_of_the_role(role) -> None:
    other = next(
        f
        for f in OTHERS
        if f.quantity not in {SampleRate, SamplingPeriod, BaudRate}
        and not _is_ruled(role.quantity, f.quantity)
    )
    with pytest.raises(IncompatibleDimensionError, match=CONVERSION[role.quantity]):
        role.canonical(12) * other.canonical(3)


@pytest.mark.parametrize("role", ROLES, ids=ROLE_IDS)
def test_a_role_scales_by_a_number_and_by_a_proportion(role) -> None:
    value = role.canonical(12)
    assert type(value * 2) is role.quantity
    assert type(value / 2) is role.quantity
    assert value * proportion.Percent(50) == role.canonical(6)
    assert value / proportion.Ratio(2) == role.canonical(6)


def test_a_role_divided_by_itself_is_a_proportion() -> None:
    assert baud_rate.Baud(9600) / baud_rate.Baud(4800) == proportion.Ratio(2)


def test_a_rate_and_its_period_multiply_to_a_count() -> None:
    rate = sample_rate.SamplesPerSecond(500)
    period = time.Millisecond(2).to_sampling_period()
    assert rate * period == Fraction(1)
    assert type(period * rate) is Fraction


def test_a_sampling_period_returns_to_a_time_with_its_unit() -> None:
    period = time.Millisecond(2).to_sampling_period()
    back = period.to_time()
    assert type(back) is Time
    assert back == time.Millisecond(2)
    assert back.to_sampling_period() == period


def test_a_proportion_over_a_role_is_its_reciprocal_role() -> None:
    ratio = proportion.Ratio(2)
    assert type(ratio / sample_rate.SamplesPerSecond(4)) is SamplingPeriod
    assert type(ratio / time.Second(4).to_sampling_period()) is SampleRate


def test_a_proportion_over_a_role_without_a_reciprocal_is_refused() -> None:
    with pytest.raises(IncompatibleDimensionError, match="no reciprocal"):
        proportion.Ratio(2) / baud_rate.Baud(9600)
