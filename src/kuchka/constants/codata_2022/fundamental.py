"""A small set of physical constants, expressed as ordinary kuchka quantities.

    from kuchka import Hertz
    from kuchka.constants.codata_2022 import SPEED_OF_LIGHT_IN_VACUUM

    wifi_wavelength = SPEED_OF_LIGHT_IN_VACUUM / Hertz(2_400_000_000)

Two different kinds of "exact" live in this module, and each constant's docstring says
which one applies:

- SI-defining constants (`SPEED_OF_LIGHT_IN_VACUUM`, `ELEMENTARY_CHARGE`) have been
    exact by definition since the 2019 SI redefinition.
    The `Decimal` below is the entire value, not a rounded measurement, and every digit
    shown is significant.
- Measured constants (`ELECTRON_MASS`, `PROTON_MASS`, `NEUTRON_MASS`) are CODATA 2022
    recommended values: the best current measurement, not a mathematical constant.
    The `Decimal` stored here carries exactly as many significant digits as CODATA
    publishes for the central value.
    Adding more digits would not add precision -- it would misrepresent how well the
    quantity is actually known.
    Each docstring quotes CODATA's own parenthetical uncertainty in the last digits
    for that reason, even though the stored magnitude itself only carries the central
    value.

Source: CODATA 2022 recommended values,
https://physics.nist.gov/cuu/Constants/
"""

from __future__ import annotations

from decimal import Decimal as _Decimal
from typing import TYPE_CHECKING
from typing import Final

from kuchka.units import NEWTON_METRE_SECOND as _NEWTON_METRE_SECOND
from kuchka.units import Coulomb as _Coulomb
from kuchka.units import CoulombPerMole as _CoulombPerMole
from kuchka.units import FaradPerMetre as _FaradPerMetre
from kuchka.units import Gigaelectronvolt as _Gigaelectronvolt
from kuchka.units import HenryPerMetre as _HenryPerMetre
from kuchka.units import JoulePerKelvin as _JoulePerKelvin
from kuchka.units import JoulePerMoleKelvin as _JoulePerMoleKelvin
from kuchka.units import JouleSecondPerTurn as _JouleSecondPerTurn
from kuchka.units import Kelvin as _Kelvin
from kuchka.units import Kilogram as _Kilogram
from kuchka.units import Metre as _Metre
from kuchka.units import MetrePerSecond as _MetrePerSecond
from kuchka.units import MetrePerSecondSquared as _MetrePerSecondSquared
from kuchka.units import Ohm as _Ohm
from kuchka.units import PerMole as _PerMole
from kuchka.units import Ratio as _Ratio
from kuchka.units import Second as _Second

if TYPE_CHECKING:
    from kuchka.quantities import Acceleration
    from kuchka.quantities import AngularMomentum
    from kuchka.quantities import Charge
    from kuchka.quantities import Energy
    from kuchka.quantities import EntitiesPerAmount
    from kuchka.quantities import Entropy
    from kuchka.quantities import Impedance
    from kuchka.quantities import Length
    from kuchka.quantities import Mass
    from kuchka.quantities import MolarCharge
    from kuchka.quantities import MolarEntropy
    from kuchka.quantities import Permeability
    from kuchka.quantities import Permittivity
    from kuchka.quantities import Proportion
    from kuchka.quantities import Temperature
    from kuchka.quantities import Time
    from kuchka.quantities import Velocity

ALPHA_PARTICLE_MASS: Final[Mass] = _Kilogram(_Decimal("6.6446573450e-27"))
"""Alpha particle mass.

Accuracy: Measured.
Value: 6.644 657 3450 e-27 kg.
Uncertainty: 0.000 000 0021 e-27 kg.
Link: https://en.wikipedia.org/wiki/Alpha_particle
"""

AVOGADRO_CONSTANT: Final[EntitiesPerAmount] = _PerMole(_Decimal("6.02214076e23"))
"""The Avogadro constant, N_A.

Accuracy: Exact.
Value: 6.022 140 76 e23 mol⁻¹.
Uncertainty: None.
Link: https://en.wikipedia.org/wiki/Avogadro_constant
"""

BOLTZMANN_CONSTANT: Final[Entropy] = _JoulePerKelvin(
    _Decimal("1.380649e-23")
).to_entropy()
"""The Boltzmann constant, k: the entropy per particle linking temperature to energy.

Accuracy: Exact.
Value: 1.380 649 e-23 J K⁻¹.
Uncertainty: None.
Note: it is an `Entropy`, so the thermal energy `k * T` goes through
`BOLTZMANN_CONSTANT.to_heat_capacity() * DeltaKelvin(300)`.
Link: https://en.wikipedia.org/wiki/Boltzmann_constant
"""

ELECTRON_MASS: Final[Mass] = _Kilogram(_Decimal("9.1093837139E-31"))
"""The electron rest mass, m_e.

Accuracy: Measured.
Value: 9.109 383 7139 e-31 kg.
Uncertainty: 0.000 000 0028 e-31 kg.
Link: https://en.wikipedia.org/wiki/Electron_mass
"""

ELEMENTARY_CHARGE: Final[Charge] = _Coulomb(_Decimal("1.602176634e-19"))
"""The elementary charge, e.

Accuracy: Exact.
Value: 1.602 176 634 e-19 C.
Uncertainty: None.
Link: https://en.wikipedia.org/wiki/Elementary_charge
"""

SPEED_OF_LIGHT_IN_VACUUM: Final[Velocity] = _MetrePerSecond(299_792_458)
"""The speed of light in vacuum, c.

Accuracy: Exact.
Value: 299 792 458 m s⁻¹.
Uncertainty: None.
Link: https://en.wikipedia.org/wiki/Speed_of_light
"""

FARADAY_CONSTANT: Final[MolarCharge] = _CoulombPerMole(_Decimal("96485.3321233100184"))
"""The Faraday constant, F, the charge of one mole of electrons.

Accuracy: Exact.
Value: 96 485.332 123 310 0184 C mol⁻¹.
Uncertainty: None.
Link: https://en.wikipedia.org/wiki/Faraday_constant
"""

MOLAR_GAS_CONSTANT: Final[MolarEntropy] = _JoulePerMoleKelvin(
    _Decimal("8.31446261815324")
).to_molar_entropy()
"""The molar gas constant, R, the Avogadro constant times the Boltzmann constant.

Accuracy: Exact.
Value: 8.314 462 618 153 24 J mol⁻¹ K⁻¹.
Uncertainty: None.
Note: CODATA prints 8.314 462 618... because it shows a prefix of the value.
The product of the two exact defining constants has exactly these 15 digits and no more.
`AVOGADRO_CONSTANT * BOLTZMANN_CONSTANT` is this constant by a rule, with no rounding.
Link: https://en.wikipedia.org/wiki/Gas_constant
"""

NEUTRON_MASS: Final[Mass] = _Kilogram(_Decimal("1.67492750056E-27"))
"""The neutron rest mass, m_n.

Accuracy: Measured.
Value: 1.674 927 500 56 e-27 kg.
Uncertainty: 0.000 000 000 85 e-27 kg.
Link: https://en.wikipedia.org/wiki/Neutron#Mass
"""

PLANCK_ENERGY: Final[Energy] = _Gigaelectronvolt(_Decimal("1.220890e19"))
"""The Planck energy, E_p.

Accuracy: Measured.
Value: 1.220 890 e19 GeV.
Uncertainty: 0.000 014 e19 GeV.
Link: https://en.wikipedia.org/wiki/Planck_units#Planck_energy
"""

PLANCK_MASS_ENERGY_EQUIVALENT_IN_GEV = PLANCK_ENERGY
"""An alias of the official CODATA 2022 to a shorter name."""

PLANCK_LENGTH: Final[Length] = _Metre(_Decimal("1.616255e-35"))
"""The Planck length, l_P: the length scale at which quantum gravity dominates.

Accuracy: Measured.
Value: 1.616 255 e-35 m.
Uncertainty: 0.000 018 e-35 m.
Link: https://en.wikipedia.org/wiki/Planck_units#Planck_length
"""

PLANCK_MASS: Final[Mass] = _Kilogram(_Decimal("2.176434e-8"))
"""The Planck mass, m_P.

Accuracy: Measured.
Value: 2.176 434 e-8 kg.
Uncertainty: 0.000 024 e-8 kg.
Link: https://en.wikipedia.org/wiki/Planck_units
"""

PLANCK_TEMPERATURE: Final[Temperature] = _Kelvin(_Decimal("1.416784e32"))
"""The Planck temperature, T_P.

Accuracy: Measured.
Value: 1.416 784 e32 K.
Uncertainty: 0.000 016 e32 K.
Link: https://en.wikipedia.org/wiki/Planck_units#Planck_temperature
"""

PLANCK_TIME: Final[Time] = _Second(_Decimal("5.391247e-44"))
"""The Planck time, t_P: the time light takes to cross one Planck length in vacuum.

Accuracy: Measured.
Value: 5.391 247 e-44 s.
Uncertainty: 0.000 060 e-44 s.
Link: https://en.wikipedia.org/wiki/Planck_units#Planck_time
"""

PROTON_MASS: Final[Mass] = _Kilogram(_Decimal("1.67262192595E-27"))
"""The proton rest mass, m_p.

Accuracy: Measured.
Value: 1.672 621 925 95 e-27 kg.
Uncertainty: 0.000 000 000 52 e-27 kg.
Link: https://en.wikipedia.org/wiki/Proton
"""

STANDARD_ACCELERATION_OF_GRAVITY: Final[Acceleration] = _MetrePerSecondSquared(
    _Decimal("9.80665")
)
"""The standard acceleration of gravity, g_n.

Accuracy: Exact.
Value: 9.806 65 m s⁻².
Uncertainty: None.
Link: https://en.wikipedia.org/wiki/Gravitational_acceleration
"""

ATOMIC_MASS_CONSTANT: Final[Mass] = _Kilogram(_Decimal("1.66053906892e-27"))
"""The atomic mass constant, m_u, one twelfth of the mass of a carbon-12 atom.

The `Dalton` unit has the same value.

Accuracy: Measured.
Value: 1.660 539 068 92 e-27 kg.
Uncertainty: 0.000 000 000 52 e-27 kg.
Link: https://en.wikipedia.org/wiki/Dalton_(unit)
"""

BOHR_RADIUS: Final[Length] = _Metre(_Decimal("5.29177210544e-11"))
"""The Bohr radius, a_0, the most probable distance of the electron in a hydrogen atom.

Accuracy: Measured.
Value: 5.291 772 105 44 e-11 m.
Uncertainty: 0.000 000 000 82 e-11 m.
Link: https://en.wikipedia.org/wiki/Bohr_radius
"""

CHARACTERISTIC_IMPEDANCE_OF_VACUUM: Final[Impedance] = _Ohm(
    _Decimal("376.730313412")
).to_impedance()
"""The characteristic impedance of vacuum, Z_0: the electric over the magnetic field.

Accuracy: Measured.
Value: 376.730 313 412 ohm.
Uncertainty: 0.000 000 059 ohm.
Link: https://en.wikipedia.org/wiki/Impedance_of_free_space
"""

FINE_STRUCTURE_CONSTANT: Final[Proportion] = _Ratio(_Decimal("0.0072973525643"))
"""The fine-structure constant, alpha, the strength of the electromagnetic interaction.

Accuracy: Measured.
Value: 7.297 352 5643 e-3.
Uncertainty: 0.000 000 0011 e-3.
Link: https://en.wikipedia.org/wiki/Fine-structure_constant
"""

PLANCK_CONSTANT: Final[AngularMomentum] = _JouleSecondPerTurn(
    _Decimal("6.62607015e-34")
)
"""The Planck constant, h, the action of one cycle.

It is an `AngularMomentum`, in joule-seconds per turn: the angle is a dimension of its
own, so `REDUCED_PLANCK_CONSTANT` is this same quantity read per radian.

Accuracy: Exact.
Value: 6.626 070 15 e-34 J s.
Uncertainty: None.
Link: https://en.wikipedia.org/wiki/Planck_constant
"""

REDUCED_PLANCK_CONSTANT: Final[AngularMomentum] = PLANCK_CONSTANT.to(
    _NEWTON_METRE_SECOND
)
"""The reduced Planck constant, h-bar, the Planck constant per radian.

It is `PLANCK_CONSTANT` displayed in newton-metre-seconds, so that `h / (2 pi)` holds
with the value of pi the library carries and nothing is rounded to CODATA's digits.

Accuracy: Exact.
Value: 1.054 571 817... e-34 J s.
Uncertainty: None.
Link: https://en.wikipedia.org/wiki/Planck_constant#Reduced_Planck_constant
"""

VACUUM_ELECTRIC_PERMITTIVITY: Final[Permittivity] = _FaradPerMetre(
    _Decimal("8.8541878188e-12")
)
"""The vacuum electric permittivity, epsilon_0.

Accuracy: Measured.
Value: 8.854 187 8188 e-12 F m⁻¹.
Uncertainty: 0.000 000 0014 e-12 F m⁻¹.
Link: https://en.wikipedia.org/wiki/Vacuum_permittivity
"""

VACUUM_MAGNETIC_PERMEABILITY: Final[Permeability] = _HenryPerMetre(
    _Decimal("1.25663706127e-6")
)
"""The vacuum magnetic permeability, mu_0.

Accuracy: Measured.
Value: 1.256 637 061 27 e-6 N A⁻².
Uncertainty: 0.000 000 000 20 e-6 N A⁻².
Link: https://en.wikipedia.org/wiki/Vacuum_permeability
"""

__all__ = [
    "ALPHA_PARTICLE_MASS",
    "ATOMIC_MASS_CONSTANT",
    "AVOGADRO_CONSTANT",
    "BOHR_RADIUS",
    "BOLTZMANN_CONSTANT",
    "CHARACTERISTIC_IMPEDANCE_OF_VACUUM",
    "ELECTRON_MASS",
    "ELEMENTARY_CHARGE",
    "FARADAY_CONSTANT",
    "FINE_STRUCTURE_CONSTANT",
    "MOLAR_GAS_CONSTANT",
    "NEUTRON_MASS",
    "PLANCK_CONSTANT",
    "PLANCK_ENERGY",
    "PLANCK_LENGTH",
    "PLANCK_MASS",
    "PLANCK_MASS_ENERGY_EQUIVALENT_IN_GEV",
    "PLANCK_TEMPERATURE",
    "PLANCK_TIME",
    "PROTON_MASS",
    "REDUCED_PLANCK_CONSTANT",
    "SPEED_OF_LIGHT_IN_VACUUM",
    "STANDARD_ACCELERATION_OF_GRAVITY",
    "VACUUM_ELECTRIC_PERMITTIVITY",
    "VACUUM_MAGNETIC_PERMEABILITY",
]
