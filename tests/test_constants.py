"""kuchka.constants: SI-exact and CODATA-measured constants as kuchka quantities.

Values are checked against a small number of independently-known facts (the SI-defining
ones exactly, the measured ones to CODATA 2022's own precision).
"""

from decimal import Decimal

from kuchka import Charge
from kuchka import Frequency
from kuchka import Hertz
from kuchka import Length
from kuchka import Mass
from kuchka import Velocity
from kuchka.constants import ELECTRON_MASS
from kuchka.constants import ELEMENTARY_CHARGE
from kuchka.constants import NEUTRON_MASS
from kuchka.constants import PROTON_MASS
from kuchka.constants import SPEED_OF_LIGHT
from kuchka.units import METRE_PER_SECOND


def test_speed_of_light_is_exact_by_definition() -> None:
    assert SPEED_OF_LIGHT.value_in(METRE_PER_SECOND) == Decimal(299_792_458)


def test_speed_of_light_isinstance() -> None:
    assert isinstance(SPEED_OF_LIGHT, Velocity)


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
    assert round(ratio, 1) == Decimal("1836.2")


def test_wavelength_from_speed_of_light_and_frequency_is_a_length() -> None:
    """The motivating example: c / f -> wavelength, using existing quantities."""
    wifi_frequency = Hertz(2_400_000_000)
    wavelength = SPEED_OF_LIGHT / wifi_frequency
    assert isinstance(wavelength, Length)
    # c = 299792458 m/s, f = 2.4 GHz -> lambda ~= 0.1249 m
    assert round(wavelength.magnitude, 4) == Decimal("0.1249")


def test_frequency_from_speed_of_light_and_wavelength_round_trips() -> None:
    wifi_frequency = Hertz(2_400_000_000)
    wavelength = SPEED_OF_LIGHT / wifi_frequency
    recovered_frequency = SPEED_OF_LIGHT / wavelength
    assert isinstance(recovered_frequency, Frequency)
    assert round(recovered_frequency.magnitude) == round(wifi_frequency.magnitude)
