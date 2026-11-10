"""Ties between kuchka's values and the CODATA 2022 dataset they claim to follow.

The dataset is the NIST listing shipped next to the constants,
`src/kuchka/constants/codata_2022/allascii.txt`.
When a new adjustment supersedes it, the listing is replaced and these tests fail on
every value that moved: that is a breaking change, and it is made on purpose.
"""

from __future__ import annotations

import re
from decimal import ROUND_HALF_EVEN
from decimal import Context
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

import kuchka.constants.codata_2022 as codata
from kuchka.units import mass
from kuchka.units.mechanics import angular_momentum

LISTING = Path(codata.__file__).parent / "allascii.txt"

# IAU 2015 Resolution B3, nominal values of the solar and terrestrial mass parameters,
# in m^3 s^-2.
NOMINAL_SOLAR_MASS_PARAMETER = Decimal("1.3271244e20")
NOMINAL_TERRESTRIAL_MASS_PARAMETER = Decimal("3.986004e14")

SEVEN_SIGNIFICANT_DIGITS = Context(prec=7, rounding=ROUND_HALF_EVEN)


def _listing() -> dict[str, tuple[Decimal, bool]]:
    """Read the NIST table: quantity name -> (published value, value is exact)."""
    rows: dict[str, tuple[Decimal, bool]] = {}
    started = False
    for line in LISTING.read_text(encoding="utf-8").splitlines():
        if line.startswith("-----"):
            started = True
            continue
        if not started or not line.strip():
            continue
        name, value, uncertainty, *_ = re.split(r"\s{2,}", line.strip())
        digits = value.replace(" ", "").replace("...", "")
        rows[name] = (Decimal(digits), "(exact)" in uncertainty)
    return rows


ROWS = _listing()


def _published(name: str) -> Decimal:
    return ROWS[name][0]


def test_the_listing_is_the_2022_adjustment() -> None:
    assert "2022 CODATA adjustment" in LISTING.read_text(encoding="utf-8")


def test_the_dalton_is_the_codata_atomic_mass_constant() -> None:
    assert mass.DALTON.scale == Fraction(_published("atomic mass constant"))


def test_the_gravitational_constant_is_the_one_the_planetary_masses_assume() -> None:
    assert _published("Newtonian constant of gravitation") == Decimal("6.67430e-11")


def test_the_solar_mass_is_the_nominal_parameter_over_the_codata_constant() -> None:
    gravitational = _published("Newtonian constant of gravitation")
    derived = SEVEN_SIGNIFICANT_DIGITS.divide(
        NOMINAL_SOLAR_MASS_PARAMETER, gravitational
    )
    assert mass.SOLAR_MASS.scale == Fraction(derived)


def test_the_earth_mass_is_the_nominal_parameter_over_the_codata_constant() -> None:
    gravitational = _published("Newtonian constant of gravitation")
    derived = SEVEN_SIGNIFICANT_DIGITS.divide(
        NOMINAL_TERRESTRIAL_MASS_PARAMETER, gravitational
    )
    assert mass.EARTH_MASS.scale == Fraction(derived)


@pytest.mark.parametrize(
    ("constant", "row"),
    [
        (codata.ALPHA_PARTICLE_MASS, "alpha particle mass"),
        (codata.ELECTRON_MASS, "electron mass"),
        (codata.PROTON_MASS, "proton mass"),
        (codata.NEUTRON_MASS, "neutron mass"),
        (codata.ELEMENTARY_CHARGE, "elementary charge"),
        (codata.SPEED_OF_LIGHT_IN_VACUUM, "speed of light in vacuum"),
        (codata.PLANCK_LENGTH, "Planck length"),
        (codata.PLANCK_MASS, "Planck mass"),
        (codata.PLANCK_TIME, "Planck time"),
        (codata.PLANCK_TEMPERATURE, "Planck temperature"),
        (codata.STANDARD_ACCELERATION_OF_GRAVITY, "standard acceleration of gravity"),
        (codata.ATOMIC_MASS_CONSTANT, "atomic mass constant"),
        (codata.BOHR_RADIUS, "Bohr radius"),
        (
            codata.CHARACTERISTIC_IMPEDANCE_OF_VACUUM,
            "characteristic impedance of vacuum",
        ),
        (codata.FINE_STRUCTURE_CONSTANT, "fine-structure constant"),
        (codata.VACUUM_ELECTRIC_PERMITTIVITY, "vacuum electric permittivity"),
        (codata.VACUUM_MAGNETIC_PERMEABILITY, "vacuum mag. permeability"),
    ],
    ids=lambda p: p if isinstance(p, str) else "",
)
def test_a_constant_carries_the_published_value(constant, row) -> None:
    assert constant.value_in(constant.unit) == Fraction(_published(row))


def test_the_planck_constant_carries_the_published_value() -> None:
    value = codata.PLANCK_CONSTANT.value_in(angular_momentum.JOULE_SECOND_PER_TURN)
    assert value == Fraction(_published("Planck constant"))


def test_the_reduced_planck_constant_is_the_planck_constant_per_radian() -> None:
    published = _published("reduced Planck constant")
    stored = codata.REDUCED_PLANCK_CONSTANT.value_in(
        angular_momentum.NEWTON_METRE_SECOND
    )
    last_digit = Fraction(10) ** published.as_tuple().exponent
    assert abs(stored - Fraction(published)) < last_digit
    assert codata.REDUCED_PLANCK_CONSTANT == codata.PLANCK_CONSTANT


def test_the_atomic_mass_constant_is_the_dalton() -> None:
    assert mass.Dalton(1) == codata.ATOMIC_MASS_CONSTANT
