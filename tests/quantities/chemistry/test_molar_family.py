"""Molality, molar volume, molar flow rate, catalytic activity, and molar charge."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import AmountOfSubstance
from kuchka import CatalyticActivity
from kuchka import Charge
from kuchka import IncompatibleDimensionError
from kuchka import InvalidConversionError
from kuchka import MassFlowRate
from kuchka import Molality
from kuchka import MolarCharge
from kuchka import MolarFlowRate
from kuchka import MolarVolume
from kuchka import Volume
from kuchka.constants.codata_2022 import AVOGADRO_CONSTANT
from kuchka.constants.codata_2022 import ELEMENTARY_CHARGE
from kuchka.constants.codata_2022 import FARADAY_CONSTANT
from kuchka.units import amount
from kuchka.units import mass
from kuchka.units.chemistry import catalytic_activity as cat
from kuchka.units.chemistry import molality
from kuchka.units.chemistry import molar_charge
from kuchka.units.chemistry import molar_concentration
from kuchka.units.chemistry import molar_flow_rate as mfr
from kuchka.units.chemistry import molar_mass
from kuchka.units.chemistry import molar_volume
from kuchka.units.electromagnetics import charge
from kuchka.units.geometry import volume
from kuchka.units.mechanics import mass_flow_rate
from kuchka.units.mechanics import volumetric_flow_rate
from kuchka.units.temporal import time


def test_an_amount_over_a_mass_is_a_molality() -> None:
    value = amount.Mole(0.5) / mass.Gram(250)
    assert isinstance(value, Molality)
    assert value == molality.MolePerKilogram(2)


def test_one_over_a_molar_mass_is_a_molality() -> None:
    value = 1 / molar_mass.GramPerMole(18)
    assert isinstance(value, Molality)
    assert value == molality.MolePerKilogram(Fraction(1000, 18))


def test_a_molality_times_a_mass_is_an_amount() -> None:
    moles = molality.MolePerKilogram(2) * mass.Gram(250)
    assert isinstance(moles, AmountOfSubstance)
    assert moles == amount.Mole(0.5)


def test_a_volume_over_an_amount_is_a_molar_volume() -> None:
    value = volume.Litre(45.422) / amount.Mole(2)
    assert isinstance(value, MolarVolume)
    assert value == molar_volume.LitrePerMole(22.711)


def test_one_over_a_molar_concentration_is_a_molar_volume() -> None:
    value = 1 / molar_concentration.MolePerLitre(2)
    assert isinstance(value, MolarVolume)
    assert value == molar_volume.LitrePerMole(Fraction(1, 2))


def test_a_molar_volume_times_an_amount_is_a_volume() -> None:
    filled = molar_volume.LitrePerMole(22.711) * amount.Mole(2)
    assert isinstance(filled, Volume)
    assert filled == volume.Litre(45.422)


def test_a_litre_per_mole_is_a_cubic_decimetre_per_mole() -> None:
    from kuchka.units import MOLAR_VOLUME_UNITS

    assert MOLAR_VOLUME_UNITS["dm3/mol"] is molar_volume.LitrePerMole
    assert molar_volume.CubicCentimetrePerMole(1000) == molar_volume.LitrePerMole(1)


def test_an_amount_over_a_time_is_a_molar_flow_rate() -> None:
    flow = amount.Mole(30) / time.Minute(1)
    assert type(flow) is MolarFlowRate
    assert flow == mfr.MolePerSecond(0.5)


def test_a_molar_flow_rate_times_a_time_is_an_amount() -> None:
    moles = mfr.MolePerSecond(0.5) * time.Minute(1)
    assert isinstance(moles, AmountOfSubstance)
    assert moles == amount.Mole(30)


def test_a_molar_flow_rate_times_a_molar_mass_is_a_mass_flow_rate() -> None:
    flow = mfr.KilomolePerHour(36) * molar_mass.GramPerMole(46.07)
    assert isinstance(flow, MassFlowRate)
    assert flow == mass_flow_rate.KilogramPerSecond(0.4607)


def test_a_mass_flow_rate_over_a_molar_mass_is_a_molar_flow_rate() -> None:
    flow = mass_flow_rate.KilogramPerSecond(1) / molar_mass.GramPerMole(100)
    assert type(flow) is MolarFlowRate
    assert flow == mfr.MolePerSecond(10)


def test_a_molar_concentration_times_a_flow_is_a_molar_flow_rate() -> None:
    flow = molar_concentration.MolePerLitre(2) * volumetric_flow_rate.LitrePerSecond(3)
    assert type(flow) is MolarFlowRate
    assert flow == mfr.MolePerSecond(6)


def test_the_minute_and_hour_forms_carry_their_time() -> None:
    assert mfr.MolePerMinute(60) == mfr.MolePerSecond(1)
    assert mfr.MolePerHour(3600) == mfr.MolePerSecond(1)
    assert mfr.KilomolePerHour(3.6) == mfr.MolePerSecond(1)
    assert mfr.MillimolePerMinute(60_000) == mfr.MolePerSecond(1)


def test_a_katal_is_a_catalytic_activity() -> None:
    assert type(cat.Katal(1)) is CatalyticActivity


def test_a_catalytic_activity_reads_as_a_molar_flow_rate() -> None:
    flow = cat.Microkatal(3).to_molar_flow_rate()
    assert type(flow) is MolarFlowRate
    assert flow == mfr.MolePerSecond(Fraction(3, 1_000_000))


def test_a_catalytic_activity_refuses_a_molar_flow_rate_unit() -> None:
    with pytest.raises(InvalidConversionError, match="MolarFlowRate"):
        cat.Katal(1).to(mfr.MOLE_PER_SECOND)


def test_a_catalytic_activity_times_a_time_names_the_conversion() -> None:
    with pytest.raises(IncompatibleDimensionError, match="to_molar_flow_rate"):
        cat.Microkatal(1) * time.Minute(1)


def test_an_enzyme_unit_is_a_micromole_per_minute() -> None:
    assert cat.EnzymeUnit(60) == cat.Microkatal(1)
    assert cat.EnzymeUnit(1).to_molar_flow_rate() == mfr.MolePerMinute(
        Fraction(1, 1_000_000)
    )


def test_the_enzyme_unit_has_a_symbol_and_the_international_unit_none() -> None:
    from kuchka.units import CATALYTIC_ACTIVITY_UNITS

    assert CATALYTIC_ACTIVITY_UNITS["U"] is cat.EnzymeUnit
    assert CATALYTIC_ACTIVITY_UNITS["ukat"] is cat.Microkatal
    assert CATALYTIC_ACTIVITY_UNITS["nanokatal"] is cat.Nanokatal
    with pytest.raises(KeyError):
        CATALYTIC_ACTIVITY_UNITS["IU"]


def test_a_charge_over_an_amount_is_a_molar_charge() -> None:
    value = charge.Coulomb(96485) / amount.Mole(1)
    assert isinstance(value, MolarCharge)
    assert value == molar_charge.CoulombPerMole(96485)


def test_a_molar_charge_times_an_amount_is_a_charge() -> None:
    passed = molar_charge.KilocoulombPerMole(96.485) * amount.Mole(2)
    assert isinstance(passed, Charge)
    assert passed == charge.Coulomb(192_970)


def test_the_faraday_constant_is_avogadro_times_the_elementary_charge() -> None:
    assert AVOGADRO_CONSTANT * ELEMENTARY_CHARGE == FARADAY_CONSTANT
    assert isinstance(FARADAY_CONSTANT, MolarCharge)


def test_a_charge_over_the_faraday_constant_is_an_amount_of_electrons() -> None:
    electrons = charge.Coulomb(Decimal("192970.6642466200368")) / FARADAY_CONSTANT
    assert electrons == amount.Mole(2)
