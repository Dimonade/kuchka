"""Every concrete quantity type is a registered kind, and arithmetic stays linear."""

from __future__ import annotations

import pytest

from kuchka import AbsorbedDose
from kuchka import AbsorbedDoseRate
from kuchka import Activity
from kuchka import Angle
from kuchka import AngularDisplacement
from kuchka import ApparentPower
from kuchka import BaudRate
from kuchka import CatalyticActivity
from kuchka import EnergyDensity
from kuchka import EquivalentDose
from kuchka import EquivalentDoseRate
from kuchka import Exposure
from kuchka import ExposureRate
from kuchka import Frequency
from kuchka import Impedance
from kuchka import Impulse
from kuchka import Instant
from kuchka import LogarithmicRatio
from kuchka import MagneticFieldStrength
from kuchka import Magnetization
from kuchka import MolarFlowRate
from kuchka import Momentum
from kuchka import Power
from kuchka import Pressure
from kuchka import Proportion
from kuchka import Reactance
from kuchka import ReactivePower
from kuchka import Resistance
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka import SpecificCharge
from kuchka import SpecificCurrent
from kuchka import SpecificEnergy
from kuchka import SpecificPower
from kuchka import Stress
from kuchka import Temperature
from kuchka import TemperatureDelta
from kuchka import Time
from kuchka import VelocitySquared
from kuchka.dimensions import ANGLE
from kuchka.dimensions import DIMENSIONLESS
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import MAGNETIC_FIELD_STRENGTH
from kuchka.dimensions import MOLAR_FLOW_RATE
from kuchka.dimensions import MOMENTUM
from kuchka.dimensions import POWER
from kuchka.dimensions import PRESSURE
from kuchka.dimensions import RESISTANCE
from kuchka.dimensions import SPECIFIC_CHARGE
from kuchka.dimensions import SPECIFIC_CURRENT
from kuchka.dimensions import SPECIFIC_ENERGY
from kuchka.dimensions import SPECIFIC_POWER
from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.dimensions import TIME
from kuchka.dimensions import Dimension
from kuchka.quantities.base import AffineQuantity
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import ModularQuantity
from kuchka.quantities.base import registry
from tests.support.kinds import QUANTITY_TYPES

SHARED = {
    TIME: (Time, SamplingPeriod, Instant),
    FREQUENCY: (Frequency, SampleRate, BaudRate, Activity),
    TEMPERATURE_DELTA: (TemperatureDelta, Temperature),
    DIMENSIONLESS: (Proportion, LogarithmicRatio),
    PRESSURE: (Pressure, Stress, EnergyDensity),
    POWER: (Power, ApparentPower, ReactivePower),
    MAGNETIC_FIELD_STRENGTH: (MagneticFieldStrength, Magnetization),
    RESISTANCE: (Resistance, Reactance, Impedance),
    ANGLE: (Angle, AngularDisplacement),
    SPECIFIC_ENERGY: (SpecificEnergy, VelocitySquared, AbsorbedDose, EquivalentDose),
    SPECIFIC_CHARGE: (SpecificCharge, Exposure),
    SPECIFIC_POWER: (SpecificPower, AbsorbedDoseRate, EquivalentDoseRate),
    SPECIFIC_CURRENT: (SpecificCurrent, ExposureRate),
    MOMENTUM: (Momentum, Impulse),
    MOLAR_FLOW_RATE: (MolarFlowRate, CatalyticActivity),
}


def test_the_shared_dimensions_are_exactly_the_listed_ones() -> None:
    assert registry._shared_dimensions() == SHARED  # noqa: SLF001


def test_an_unknown_dimension_has_no_kinds() -> None:
    assert registry._kinds_of(Dimension(mass=7)) == ()  # noqa: SLF001


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=lambda kind: kind.__name__)
def test_every_concrete_type_is_a_registered_kind(cls: type) -> None:
    assert registry._is_registered(cls)  # noqa: SLF001


def test_each_shape_has_registered_kinds() -> None:
    kinds = {kind for found in registry._KINDS_BY_DIMENSION.values() for kind in found}  # noqa: SLF001
    for shape in (LinearQuantity, AffineQuantity, ModularQuantity):
        assert any(issubclass(kind, shape) for kind in kinds)
    assert LogarithmicRatio in kinds


def test_a_dimensionless_kind_is_catalogued() -> None:
    assert registry._kinds_of(DIMENSIONLESS) == (Proportion, LogarithmicRatio)  # noqa: SLF001


@pytest.mark.parametrize(
    "kind",
    [Angle, Instant, Temperature, LogarithmicRatio, Proportion],
    ids=lambda k: k.__name__,
)
def test_a_kind_arithmetic_cannot_produce_is_never_principal(kind: type) -> None:
    assert kind not in registry._DIMENSION_REGISTRY.values()  # noqa: SLF001
    assert not any(kind in group for group in registry._CONTESTED.values())  # noqa: SLF001


def test_the_angular_displacement_is_the_principal_kind_of_the_angle_dimension() -> (
    None
):
    assert registry._DIMENSION_REGISTRY[ANGLE] is AngularDisplacement  # noqa: SLF001
    assert Angle not in registry._DIMENSION_REGISTRY.values()  # noqa: SLF001


def test_a_dimension_with_a_kind_of_another_shape_keeps_its_principal() -> None:
    assert registry._DIMENSION_REGISTRY[TIME] is Time  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[TEMPERATURE_DELTA] is TemperatureDelta  # noqa: SLF001
    assert DIMENSIONLESS not in registry._DIMENSION_REGISTRY  # noqa: SLF001


def test_the_principal_kinds_are_linear_kinds_with_extent() -> None:
    for dimension, kind in registry._DIMENSION_REGISTRY.items():  # noqa: SLF001
        assert issubclass(kind, LinearQuantity)
        assert kind.dimension == dimension != DIMENSIONLESS
        assert registry._is_registered(kind)  # noqa: SLF001


def test_the_contested_kinds_are_exactly_the_listed_ones() -> None:
    contested = registry._CONTESTED  # noqa: SLF001
    assert contested == {
        PRESSURE: (Pressure, EnergyDensity),
        SPECIFIC_ENERGY: (SpecificEnergy, VelocitySquared),
        MOMENTUM: (Momentum, Impulse),
    }
    for dimension in contested:
        assert dimension not in registry._DIMENSION_REGISTRY  # noqa: SLF001
