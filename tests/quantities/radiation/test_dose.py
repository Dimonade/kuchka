"""Absorbed dose, equivalent dose, and exposure: roles of specific energy and charge.

The generic role behaviour (refusals, scaling) is covered once for every role in
`test_role_kinds`; this module covers what is specific to the doses and their units.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AbsorbedDose
from kuchka import Charge
from kuchka import EquivalentDose
from kuchka import Exposure
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import SpecificCharge
from kuchka import SpecificEnergy
from kuchka import parse
from kuchka.constants import icrp_103
from kuchka.units import angular
from kuchka.units.electromagnetics import charge
from kuchka.units.electromagnetics import specific_charge
from kuchka.units.mass import Kilogram
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import specific_energy
from kuchka.units.proportion import Percent
from kuchka.units.proportion import Ratio
from kuchka.units.radiation import absorbed_dose
from kuchka.units.radiation import equivalent_dose
from kuchka.units.radiation import exposure


def test_a_gray_is_a_joule_per_kilogram() -> None:
    taken = absorbed_dose.Gray(3).to_specific_energy()
    assert isinstance(taken, SpecificEnergy)
    assert taken == specific_energy.JoulePerKilogram(3)


def test_a_specific_energy_is_read_as_a_dose_by_name() -> None:
    dose = AbsorbedDose.from_specific_energy(specific_energy.JoulePerKilogram(3))
    assert dose == absorbed_dose.Gray(3)
    assert type(dose) is AbsorbedDose


def test_a_dose_over_a_mass_gives_the_energy_through_the_specific_energy() -> None:
    absorbed = absorbed_dose.Gray(2).to_specific_energy() * Kilogram(3)
    assert absorbed == energy.Joule(6)


def test_a_dose_is_built_from_a_specific_energy_only() -> None:
    with pytest.raises(IncompatibleDimensionError):
        AbsorbedDose.from_specific_energy(energy.Joule(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_a_rad_is_exactly_a_centigray() -> None:
    assert absorbed_dose.Rad(1) == absorbed_dose.Centigray(1)
    assert absorbed_dose.Rad(100) == absorbed_dose.Gray(1)
    assert absorbed_dose.Millirad(1) == absorbed_dose.Microgray(10)


def test_a_rem_is_exactly_ten_millisieverts() -> None:
    assert equivalent_dose.Rem(1) == equivalent_dose.Millisievert(10)
    assert equivalent_dose.Rem(100) == equivalent_dose.Sievert(1)
    assert equivalent_dose.Millirem(1) == equivalent_dose.Microsievert(10)


def test_a_sievert_has_no_way_into_energy() -> None:
    dose = equivalent_dose.Sievert(2)
    assert not hasattr(dose, "to_specific_energy")
    with pytest.raises(IncompatibleDimensionError, match="no conversion"):
        dose * Kilogram(3)
    with pytest.raises(IncompatibleDimensionError, match="no conversion"):
        Kilogram(3) * dose


def test_the_two_doses_and_a_specific_energy_do_not_mix() -> None:
    gray = absorbed_dose.Gray(1)
    sievert = equivalent_dose.Sievert(1)
    joules = specific_energy.JoulePerKilogram(1)
    for left, right in ((gray, sievert), (gray, joules), (sievert, joules)):
        with pytest.raises(IncompatibleDimensionError):
            left + right  # type: ignore[operator]  # ty: ignore[unsupported-operator]
        with pytest.raises(IncompatibleDimensionError):
            left < right  # type: ignore[operator]  # noqa: B015  # ty: ignore[unsupported-operator]
        with pytest.raises(IncompatibleDimensionError):
            left / right  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_dose_over_a_dose_of_its_own_kind_is_a_proportion() -> None:
    assert equivalent_dose.Sievert(3) / equivalent_dose.Millisievert(1) == Ratio(3000)
    assert absorbed_dose.Gray(1) * Percent(50) == absorbed_dose.Centigray(50)


def test_a_weighted_dose_of_alpha_particles_is_twenty_times_the_dose() -> None:
    weighted = EquivalentDose.from_absorbed_dose(
        absorbed_dose.Milligray(3), icrp_103.ALPHA_PARTICLES
    )
    assert type(weighted) is EquivalentDose
    assert weighted == equivalent_dose.Millisievert(60)


def test_the_weighting_reads_the_unit_of_the_dose_and_the_factor() -> None:
    weighted = EquivalentDose.from_absorbed_dose(absorbed_dose.Rad(5), Percent(200))
    assert weighted == equivalent_dose.Rem(10)


def test_a_mixed_field_is_the_sum_of_its_weighted_doses() -> None:
    field = [
        (absorbed_dose.Milligray(1), icrp_103.PHOTONS),
        (absorbed_dose.Milligray(1), icrp_103.PROTONS),
        (absorbed_dose.Milligray(1), icrp_103.ALPHA_PARTICLES),
    ]
    total = sum(
        (EquivalentDose.from_absorbed_dose(d, w) for d, w in field),
        start=equivalent_dose.Sievert(0),
    )
    assert total == equivalent_dose.Millisievert(23)


def test_a_negative_weighting_factor_is_refused() -> None:
    with pytest.raises(InvalidMeasurementError, match="not negative"):
        EquivalentDose.from_absorbed_dose(absorbed_dose.Gray(1), Ratio(-1))


@pytest.mark.parametrize(
    ("dose", "factor"),
    [
        (equivalent_dose.Sievert(1), Ratio(1)),
        (absorbed_dose.Gray(1), absorbed_dose.Gray(1)),
        (absorbed_dose.Gray(1), 2),
    ],
)
def test_the_weighting_takes_an_absorbed_dose_and_a_proportion_only(
    dose: object, factor: object
) -> None:
    with pytest.raises(IncompatibleDimensionError):
        EquivalentDose.from_absorbed_dose(dose, factor)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_rad_text_is_read_by_the_quantity_it_is_given() -> None:
    assert parse("5 rad", AbsorbedDose) == absorbed_dose.Rad(5)
    assert parse("5 rad", AbsorbedDose) != absorbed_dose.Gray(5)
    assert parse("5 rad", angular.Angle) == angular.Radian(5)  # type: ignore[arg-type]
    assert parse("12 uSv", EquivalentDose) == equivalent_dose.Microsievert(12)


def test_the_sievert_table_has_no_gray_and_the_gray_table_no_sievert() -> None:
    assert "Gy" not in equivalent_dose.EQUIVALENT_DOSE_UNITS
    assert "Sv" not in absorbed_dose.ABSORBED_DOSE_UNITS


def test_a_charge_over_a_mass_is_a_specific_charge() -> None:
    result = charge.Coulomb(6) / Kilogram(2)
    assert type(result) is SpecificCharge
    assert result == specific_charge.CoulombPerKilogram(3)
    assert result * Kilogram(2) == charge.Coulomb(6)


def test_a_battery_capacity_is_the_same_in_ah_per_kg_and_mah_per_g() -> None:
    assert specific_charge.MilliampereHourPerGram(250) == (
        specific_charge.AmpereHourPerKilogram(250)
    )
    assert specific_charge.AmpereHourPerKilogram(
        1
    ) == specific_charge.CoulombPerKilogram(3600)


def test_a_roentgen_is_exactly_258_microcoulombs_per_kilogram() -> None:
    assert exposure.Roentgen(1).to_specific_charge() == (
        specific_charge.MicrocoulombPerKilogram(258)
    )
    assert exposure.Roentgen(1).to(exposure.COULOMB_PER_KILOGRAM).value_in(
        exposure.COULOMB_PER_KILOGRAM
    ) == Fraction(258, 1_000_000)


def test_an_exposure_in_coulombs_per_kilogram_is_read_from_its_table() -> None:
    read = exposure.EXPOSURE_UNITS["C/kg"](1)
    assert type(read) is Exposure
    assert read == Exposure.from_specific_charge(specific_charge.CoulombPerKilogram(1))


def test_the_charge_freed_in_air_goes_through_the_specific_charge() -> None:
    freed = exposure.Milliroentgen(5).to_specific_charge() * Kilogram(2)
    assert type(freed) is Charge
    with pytest.raises(IncompatibleDimensionError, match="to_specific_charge"):
        exposure.Milliroentgen(5) * Kilogram(2)


def test_an_exposure_is_built_from_a_specific_charge_only() -> None:
    with pytest.raises(IncompatibleDimensionError):
        Exposure.from_specific_charge(charge.Coulomb(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
