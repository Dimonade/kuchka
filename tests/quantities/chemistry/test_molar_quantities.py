"""The molar quantities and EntitiesPerAmount: how they combine."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AmountOfSubstance
from kuchka import Density
from kuchka import Energy
from kuchka import EntitiesPerAmount
from kuchka import IncompatibleDimensionError
from kuchka import Mass
from kuchka import MolarConcentration
from kuchka import MolarEnergy
from kuchka import MolarMass
from kuchka import Volume
from kuchka.constants.codata_2022 import AVOGADRO_CONSTANT
from kuchka.units import amount
from kuchka.units import mass
from kuchka.units.chemistry import entities_per_amount as epa
from kuchka.units.chemistry import molar_concentration as conc
from kuchka.units.chemistry import molar_energy
from kuchka.units.chemistry import molar_mass
from kuchka.units.geometry import volume
from kuchka.units.mechanics import density
from kuchka.units.mechanics import energy


def test_a_mass_over_an_amount_is_a_molar_mass() -> None:
    value = mass.Gram(36) / amount.Mole(2)
    assert isinstance(value, MolarMass)
    assert value == molar_mass.GramPerMole(18)


def test_a_mass_over_a_molar_mass_is_an_amount() -> None:
    moles = mass.Gram(90) / molar_mass.GramPerMole(18)
    assert isinstance(moles, AmountOfSubstance)
    assert moles == amount.Mole(5)


def test_a_molar_mass_times_an_amount_is_a_mass() -> None:
    grams = molar_mass.GramPerMole(18) * amount.Mole(5)
    assert isinstance(grams, Mass)
    assert grams == mass.Gram(90)


def test_an_amount_over_a_volume_is_a_molar_concentration() -> None:
    value = amount.Mole(1) / volume.Litre(2)
    assert isinstance(value, MolarConcentration)
    assert value == conc.MolePerLitre(Fraction(1, 2))


def test_a_molar_concentration_times_a_volume_is_an_amount() -> None:
    moles = conc.MolePerLitre(2) * volume.Millilitre(500)
    assert isinstance(moles, AmountOfSubstance)
    assert moles == amount.Mole(1)


def test_an_amount_over_a_molar_concentration_is_a_volume() -> None:
    needed = amount.Mole(1) / conc.MolePerLitre(2)
    assert isinstance(needed, Volume)
    assert needed == volume.Millilitre(500)


def test_a_molar_concentration_times_a_molar_mass_is_a_density() -> None:
    mass_concentration = conc.MolePerLitre(2) * molar_mass.GramPerMole(58.44)
    assert isinstance(mass_concentration, Density)
    assert mass_concentration == density.GramPerLitre(116.88)


def test_a_density_over_a_molar_mass_is_a_molar_concentration() -> None:
    molar = density.GramPerLitre(116.88) / molar_mass.GramPerMole(58.44)
    assert isinstance(molar, MolarConcentration)
    assert molar == conc.MolePerLitre(2)


def test_a_milligram_per_litre_is_a_density() -> None:
    assert isinstance(density.MilligramPerLitre(8), Density)
    assert density.MilligramPerLitre(1000) == density.GramPerLitre(1)
    assert density.MicrogramPerLitre(1000) == density.MilligramPerLitre(1)


def test_a_molar_energy_times_an_amount_is_an_energy() -> None:
    released = molar_energy.KilojoulePerMole(890) * amount.Mole(2)
    assert isinstance(released, Energy)
    assert released == energy.Kilojoule(1780)


def test_an_energy_over_an_amount_is_a_molar_energy() -> None:
    per_mole = energy.Kilojoule(1780) / amount.Mole(2)
    assert isinstance(per_mole, MolarEnergy)
    assert per_mole == molar_energy.KilojoulePerMole(890)


def test_a_kilocalorie_per_mole_is_4_184_kilojoules_per_mole() -> None:
    assert molar_energy.KilocaloriePerMole(1) == molar_energy.KilojoulePerMole(
        Fraction(4184, 1000)
    )


def test_a_reciprocal_amount_times_an_amount_is_a_count() -> None:
    count = AVOGADRO_CONSTANT * amount.Micromole(1)
    assert count == Fraction(602_214_076_000_000_000)
    assert not isinstance(count, EntitiesPerAmount)


def test_one_over_an_amount_is_entities_per_amount() -> None:
    assert isinstance(1 / amount.Mole(4), EntitiesPerAmount)
    assert 1 / amount.Mole(4) == epa.PerMole(Fraction(1, 4))


def test_a_molar_mass_over_the_avogadro_constant_is_the_mass_of_one_entity() -> None:
    one_molecule = molar_mass.GramPerMole(18) / AVOGADRO_CONSTANT
    assert isinstance(one_molecule, Mass)
    assert one_molecule * AVOGADRO_CONSTANT == molar_mass.GramPerMole(18)


def test_a_gram_per_mole_and_a_kilogram_per_kilomole_are_the_same_value() -> None:
    assert molar_mass.GramPerMole(44) == molar_mass.KilogramPerKilomole(44)


def test_a_millimolar_is_a_millimole_per_litre() -> None:
    assert conc.MillimolePerLitre(1) == amount.Millimole(1) / volume.Litre(1)


def test_a_molar_mass_is_not_a_molar_energy() -> None:
    with pytest.raises(IncompatibleDimensionError):
        molar_mass.GramPerMole(1) + molar_energy.JoulePerMole(1)  # type: ignore[operator]


def test_the_molar_symbols_are_known_with_the_prefixes() -> None:
    from kuchka.units import MOLAR_CONCENTRATION_UNITS

    assert MOLAR_CONCENTRATION_UNITS["M"] is conc.MolePerLitre
    assert MOLAR_CONCENTRATION_UNITS["mM"] is conc.MillimolePerLitre
    assert MOLAR_CONCENTRATION_UNITS["uM"] is conc.MicromolePerLitre
    assert MOLAR_CONCENTRATION_UNITS["µM"] is conc.MicromolePerLitre
    assert MOLAR_CONCENTRATION_UNITS["nM"] is conc.NanomolePerLitre
    assert MOLAR_CONCENTRATION_UNITS["millimolar"] is conc.MillimolePerLitre


def test_the_avogadro_constant_is_exact() -> None:
    assert AVOGADRO_CONSTANT.value_in(epa.PER_MOLE) == Fraction(602_214_076, 1) * (
        10**15
    )
    assert isinstance(AVOGADRO_CONSTANT, EntitiesPerAmount)
