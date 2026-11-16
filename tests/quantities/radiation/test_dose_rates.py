"""Dose rates and exposure rate: roles of specific power and specific current.

The generic role behaviour (refusals, scaling) is covered once for every role in
`test_role_kinds`; this module covers the rules that let a rate and a time make a dose,
and the units of the instruments.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AbsorbedDose
from kuchka import AbsorbedDoseRate
from kuchka import Ampere
from kuchka import Coulomb
from kuchka import EquivalentDose
from kuchka import EquivalentDoseRate
from kuchka import Exposure
from kuchka import ExposureRate
from kuchka import Hour
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Joule
from kuchka import Kilogram
from kuchka import Minute
from kuchka import Power
from kuchka import SpecificCharge
from kuchka import SpecificCurrent
from kuchka import SpecificEnergy
from kuchka import SpecificPower
from kuchka import Time
from kuchka import Watt
from kuchka import parse
from kuchka.constants import icrp_103
from kuchka.units.electromagnetics import specific_charge
from kuchka.units.electromagnetics import specific_current
from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import specific_energy
from kuchka.units.mechanics import specific_power
from kuchka.units.proportion import Ratio
from kuchka.units.radiation import absorbed_dose
from kuchka.units.radiation import absorbed_dose_rate as adr
from kuchka.units.radiation import equivalent_dose
from kuchka.units.radiation import equivalent_dose_rate as edr
from kuchka.units.radiation import exposure
from kuchka.units.radiation import exposure_rate as er


def test_a_dose_rate_times_a_time_is_a_dose_in_either_order() -> None:
    shift = edr.MicrosievertPerHour(0.12) * Hour(8)
    assert type(shift) is EquivalentDose
    assert shift == equivalent_dose.Microsievert(Fraction(96, 100))
    assert Hour(8) * edr.MicrosievertPerHour(0.12) == shift
    assert type(adr.GrayPerMinute(2) * Minute(3)) is AbsorbedDose
    assert adr.GrayPerMinute(2) * Minute(3) == absorbed_dose.Gray(6)


def test_a_dose_over_a_time_is_a_dose_rate() -> None:
    rate = equivalent_dose.Millisievert(3) / Hour(2)
    assert type(rate) is EquivalentDoseRate
    assert rate == edr.MillisievertPerHour(Fraction(3, 2))
    assert type(absorbed_dose.Gray(1) / Minute(1)) is AbsorbedDoseRate
    assert absorbed_dose.Gray(1) / Minute(1) == adr.GrayPerMinute(1)


def test_a_dose_over_a_dose_rate_is_a_time() -> None:
    elapsed = equivalent_dose.Millisievert(1) / edr.MicrosievertPerHour(50)
    assert type(elapsed) is Time
    assert elapsed == Hour(20)


def test_a_dose_rate_displays_in_the_unit_per_hour() -> None:
    assert repr(equivalent_dose.Sievert(1) / Hour(2)) == "0.5 Sv/h"
    assert repr(absorbed_dose.Gray(10) / Hour(5)) == "2 Gy/h"
    assert repr(exposure.Roentgen(1) / Hour(4)) == "0.25 R/h"


def test_the_per_time_units_are_exact() -> None:
    assert adr.GrayPerHour(3600) == adr.GrayPerSecond(1)
    assert adr.CentigrayPerMinute(60) == adr.GrayPerSecond(Fraction(1, 100) * 60 / 60)
    assert adr.RadPerHour(1) == adr.CentigrayPerMinute(Fraction(1, 60))
    assert edr.RemPerHour(1) == edr.MillisievertPerHour(10)
    assert edr.MicrosievertPerHour(1000) == edr.MillisievertPerHour(1)
    assert er.MilliroentgenPerHour(1000) == er.RoentgenPerHour(1)


def test_a_dose_rate_has_no_way_into_a_mass_product_except_through_specific_power() -> (
    None
):
    rate = adr.GrayPerSecond(2)
    with pytest.raises(IncompatibleDimensionError, match="to_specific_power"):
        rate * Kilogram(3)
    absorbed = rate.to_specific_power() * Kilogram(3)
    assert type(absorbed) is Power
    assert absorbed == Watt(6)


def test_an_equivalent_dose_rate_has_no_way_into_power() -> None:
    reading = edr.SievertPerSecond(2)
    assert not hasattr(reading, "to_specific_power")
    with pytest.raises(IncompatibleDimensionError, match="no conversion"):
        reading * Kilogram(3)


def test_a_specific_power_is_read_as_a_dose_rate_by_name() -> None:
    rate = AbsorbedDoseRate.from_specific_power(specific_power.WattPerKilogram(3))
    assert type(rate) is AbsorbedDoseRate
    assert rate == adr.GrayPerSecond(3)
    with pytest.raises(IncompatibleDimensionError):
        AbsorbedDoseRate.from_specific_power(Watt(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_doses_and_their_rates_do_not_mix() -> None:
    gray_rate, sievert_rate = adr.GrayPerHour(1), edr.SievertPerHour(1)
    with pytest.raises(IncompatibleDimensionError):
        gray_rate + sievert_rate  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(IncompatibleDimensionError):
        equivalent_dose.Sievert(1) / gray_rate
    with pytest.raises(IncompatibleDimensionError):
        absorbed_dose.Gray(1) / sievert_rate
    with pytest.raises(IncompatibleDimensionError):
        exposure.Roentgen(1) / gray_rate
    with pytest.raises(IncompatibleDimensionError):
        sievert_rate * absorbed_dose.Gray(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_dose_rate_over_a_dose_rate_is_a_proportion() -> None:
    assert edr.MillisievertPerHour(3) / edr.MicrosievertPerHour(1) == Ratio(3000)


def test_a_weighted_dose_rate_of_alpha_particles_is_twenty_times_the_rate() -> None:
    weighted = EquivalentDoseRate.from_absorbed_dose_rate(
        adr.MilligrayPerHour(3), icrp_103.ALPHA_PARTICLES
    )
    assert type(weighted) is EquivalentDoseRate
    assert weighted == edr.MillisievertPerHour(60)


def test_the_weighting_of_a_rate_agrees_with_the_weighting_of_its_dose() -> None:
    rate = adr.MicrograyPerHour(5)
    by_rate = EquivalentDoseRate.from_absorbed_dose_rate(rate, icrp_103.PROTONS)
    by_dose = EquivalentDose.from_absorbed_dose(rate * Hour(2), icrp_103.PROTONS)
    assert by_rate * Hour(2) == by_dose


def test_a_negative_or_mistyped_weighting_of_a_rate_is_refused() -> None:
    with pytest.raises(InvalidMeasurementError, match="not negative"):
        EquivalentDoseRate.from_absorbed_dose_rate(adr.GrayPerHour(1), Ratio(-1))
    with pytest.raises(IncompatibleDimensionError):
        EquivalentDoseRate.from_absorbed_dose_rate(edr.SievertPerHour(1), Ratio(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_an_exposure_rate_times_a_time_is_an_exposure() -> None:
    visit = er.MilliroentgenPerHour(2.5) * Minute(120)
    assert type(visit) is Exposure
    assert visit == exposure.Milliroentgen(5)
    assert type(exposure.Roentgen(1) / Hour(1)) is ExposureRate
    assert exposure.Milliroentgen(5) / Hour(2) == er.MilliroentgenPerHour(2.5)


def test_a_roentgen_per_hour_is_exact_in_amperes_per_kilogram() -> None:
    assert er.RoentgenPerSecond(1).to_specific_current() == (
        specific_current.AmperePerKilogram(Fraction(258, 1_000_000))
    )
    assert er.RoentgenPerHour(3600) == er.RoentgenPerSecond(1)


def test_an_exposure_rate_in_amperes_per_kilogram_is_read_from_its_table() -> None:
    read = er.EXPOSURE_RATE_UNITS["A/kg"](1)
    assert type(read) is ExposureRate
    assert read == ExposureRate.from_specific_current(
        specific_current.AmperePerKilogram(1)
    )
    with pytest.raises(IncompatibleDimensionError):
        ExposureRate.from_specific_current(Ampere(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_an_exposure_rate_goes_through_the_specific_current() -> None:
    with pytest.raises(IncompatibleDimensionError, match="to_specific_current"):
        er.MilliroentgenPerHour(1) * Kilogram(2)
    current = er.RoentgenPerSecond(1).to_specific_current() * Kilogram(2)
    assert current == Ampere(Fraction(516, 1_000_000))


def test_a_power_over_a_mass_is_a_specific_power() -> None:
    result = Watt(6) / Kilogram(2)
    assert type(result) is SpecificPower
    assert result == specific_power.WattPerKilogram(3)
    assert result * Kilogram(2) == Watt(6)


def test_a_specific_power_and_a_time_make_a_specific_energy() -> None:
    gained = specific_power.WattPerKilogram(2) * Hour(1)
    assert type(gained) is SpecificEnergy
    assert gained == specific_energy.JoulePerKilogram(7200)
    rate = specific_energy.JoulePerKilogram(7200) / Hour(1)
    assert type(rate) is SpecificPower
    assert rate == specific_power.WattPerKilogram(2)
    assert Joule(7200) / Kilogram(1) / Hour(1) == rate


def test_a_velocity_times_an_acceleration_is_a_specific_power() -> None:
    moving = velocity.MetrePerSecond(4) * acceleration.MetrePerSecondSquared(3)
    assert type(moving) is SpecificPower
    assert moving == specific_power.WattPerKilogram(12)


def test_a_current_over_a_mass_is_a_specific_current() -> None:
    result = Ampere(6) / Kilogram(2)
    assert type(result) is SpecificCurrent
    assert result == specific_current.AmperePerKilogram(3)
    assert result * Kilogram(2) == Ampere(6)


def test_a_specific_charge_over_a_time_is_a_specific_current() -> None:
    rate = specific_charge.CoulombPerKilogram(6) / Hour(1)
    assert type(rate) is SpecificCurrent
    assert type(rate * Hour(1)) is SpecificCharge
    assert rate * Hour(1) == specific_charge.CoulombPerKilogram(6)
    assert Coulomb(6) / Kilogram(1) == specific_charge.CoulombPerKilogram(6)


def test_a_milliwatt_per_gram_is_a_watt_per_kilogram() -> None:
    assert specific_power.MilliwattPerGram(2) == specific_power.WattPerKilogram(2)
    assert specific_power.KilowattPerKilogram(1) == specific_power.WattPerGram(1)


def test_the_rate_texts_are_read_by_the_quantity_they_are_given() -> None:
    assert parse("0.12 uSv/h", EquivalentDoseRate) == edr.MicrosievertPerHour(0.12)
    assert parse("0.12 \u00b5Sv/hr", EquivalentDoseRate) == edr.MicrosievertPerHour(
        0.12
    )
    assert parse("90 nGy/h", AbsorbedDoseRate) == adr.NanograyPerHour(90)
    assert parse("2.5 mR/h", ExposureRate) == er.MilliroentgenPerHour(2.5)
    assert parse("2 W/kg", SpecificPower) == specific_power.WattPerKilogram(2)
