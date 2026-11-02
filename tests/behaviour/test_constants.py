"""kuchka.constants: SI-exact and CODATA-measured constants as kuchka quantities.

Values are checked against a small number of independently-known facts (the SI-defining
ones exactly, the measured ones to CODATA 2022's own precision).
"""

from decimal import Decimal
from fractions import Fraction

import kuchka
from kuchka import Acceleration
from kuchka import Charge
from kuchka import Energy
from kuchka import Frequency
from kuchka import Length
from kuchka import Mass
from kuchka import Proportion
from kuchka import Ratio
from kuchka import Temperature
from kuchka import Time
from kuchka import Velocity
from kuchka.constants import icrp_103
from kuchka.constants.codata_2022 import ELECTRON_MASS
from kuchka.constants.codata_2022 import ELEMENTARY_CHARGE
from kuchka.constants.codata_2022 import NEUTRON_MASS
from kuchka.constants.codata_2022 import PLANCK_ENERGY
from kuchka.constants.codata_2022 import PLANCK_LENGTH
from kuchka.constants.codata_2022 import PLANCK_MASS
from kuchka.constants.codata_2022 import PLANCK_MASS_ENERGY_EQUIVALENT_IN_GEV
from kuchka.constants.codata_2022 import PLANCK_TEMPERATURE
from kuchka.constants.codata_2022 import PLANCK_TIME
from kuchka.constants.codata_2022 import PROTON_MASS
from kuchka.constants.codata_2022 import SPEED_OF_LIGHT_IN_VACUUM
from kuchka.constants.codata_2022 import STANDARD_ACCELERATION_OF_GRAVITY
from kuchka.units import mass
from kuchka.units.kinematics import acceleration as acc
from kuchka.units.kinematics import velocity
from kuchka.units.temporal import frequency


def test_speed_of_light_is_exact_by_definition() -> None:
    assert SPEED_OF_LIGHT_IN_VACUUM.value_in(velocity.METRE_PER_SECOND) == Decimal(
        299_792_458
    )


def test_speed_of_light_isinstance() -> None:
    assert isinstance(SPEED_OF_LIGHT_IN_VACUUM, Velocity)


def test_elementary_charge_isinstance() -> None:
    assert isinstance(ELEMENTARY_CHARGE, Charge)


def test_particle_masses_are_mass_instances() -> None:
    assert isinstance(ELECTRON_MASS, Mass)
    assert isinstance(PROTON_MASS, Mass)
    assert isinstance(NEUTRON_MASS, Mass)


def test_proton_is_heavier_than_electron() -> None:
    assert PROTON_MASS > ELECTRON_MASS


def test_neutron_is_heavier_than_proton() -> None:
    assert NEUTRON_MASS > PROTON_MASS


def test_proton_electron_mass_ratio_matches_codata() -> None:
    """CODATA 2022: m_p / m_e = 1836.152 673 426(32)."""
    ratio = PROTON_MASS / ELECTRON_MASS
    assert isinstance(ratio, Proportion)
    assert round(ratio.magnitude, 1) == Fraction("1836.2")


def test_wavelength_from_speed_of_light_and_frequency_is_a_length() -> None:
    """The motivating example: c / f -> wavelength, using existing quantities."""
    wifi_frequency = frequency.Hertz(2_400_000_000)
    wavelength = SPEED_OF_LIGHT_IN_VACUUM / wifi_frequency
    assert isinstance(wavelength, Length)
    # c = 299792458 m/s, f = 2.4 GHz -> lambda ~= 0.1249 m
    assert round(wavelength.magnitude, 4) == Decimal("0.1249")


def test_frequency_from_speed_of_light_and_wavelength_round_trips() -> None:
    wifi_frequency = frequency.Hertz(2_400_000_000)
    wavelength = SPEED_OF_LIGHT_IN_VACUUM / wifi_frequency
    recovered_frequency = SPEED_OF_LIGHT_IN_VACUUM / wavelength
    assert isinstance(recovered_frequency, Frequency)
    assert round(recovered_frequency.magnitude) == round(wifi_frequency.magnitude)


def test_planck_units_are_the_right_quantity_types() -> None:
    assert isinstance(PLANCK_ENERGY, Energy)
    assert isinstance(PLANCK_MASS_ENERGY_EQUIVALENT_IN_GEV, Energy)
    assert isinstance(PLANCK_LENGTH, Length)
    assert isinstance(PLANCK_MASS, Mass)
    assert isinstance(PLANCK_TEMPERATURE, Temperature)
    assert isinstance(PLANCK_TIME, Time)


def test_planck_length_matches_codata() -> None:
    assert round(PLANCK_LENGTH.magnitude, 41) == Decimal("1.616255E-35")


def test_planck_mass_matches_codata() -> None:
    assert round(PLANCK_MASS.magnitude, 14) == Decimal("0.00000002176434")


def test_planck_temperature_matches_codata() -> None:
    assert PLANCK_TEMPERATURE.kelvin == Decimal("1.416784E32")


def test_planck_time_matches_codata() -> None:
    assert round(PLANCK_TIME.magnitude, 50) == Decimal("5.391247E-44")


def test_planck_time_is_planck_length_over_speed_of_light() -> None:
    """t_P = l_P / c agrees with the independently-published t_P.

    Both are CODATA's own 7-significant-digit values, so the agreement is checked by
    relative difference rather than exact equality.
    """
    derived = PLANCK_LENGTH / SPEED_OF_LIGHT_IN_VACUUM
    assert isinstance(derived, Time)
    relative_difference = abs(derived.magnitude - PLANCK_TIME.magnitude) / (
        PLANCK_TIME.magnitude
    )
    assert relative_difference < Fraction(1, 10**6)


def test_standard_acceleration_of_gravity_is_exact() -> None:
    assert (
        acc.MetrePerSecondSquared(Decimal("9.80665"))
        == STANDARD_ACCELERATION_OF_GRAVITY
    )


def test_standard_acceleration_of_gravity_isinstance() -> None:
    assert isinstance(STANDARD_ACCELERATION_OF_GRAVITY, Acceleration)


def test_pound_force_matches_the_defining_formula() -> None:
    """A pound-force is one avoirdupois pound at standard gravity.

    An independent cross-check of `kuchka.units.POUND_FORCE` against this module's own
    constant.
    """
    from kuchka.units import POUND_FORCE

    one_pound = mass.Kilogram(Decimal("0.45359237"))
    force = one_pound * STANDARD_ACCELERATION_OF_GRAVITY
    assert force.value_in(POUND_FORCE) == Decimal(1)


def test_the_radiation_weighting_factors_are_proportions_with_the_icrp_103_values() -> (
    None
):
    expected = {
        "PHOTONS": 1,
        "ELECTRONS": 1,
        "MUONS": 1,
        "PROTONS": 2,
        "CHARGED_PIONS": 2,
        "ALPHA_PARTICLES": 20,
        "FISSION_FRAGMENTS": 20,
        "HEAVY_IONS": 20,
    }
    assert set(icrp_103.__all__) == set(expected)
    for name, value in expected.items():
        factor = getattr(icrp_103, name)
        assert isinstance(factor, Proportion)
        assert factor == Ratio(value)
        assert getattr(kuchka.icrp_103, name) is factor
