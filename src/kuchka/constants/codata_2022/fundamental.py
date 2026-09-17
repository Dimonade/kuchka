"""A small set of physical constants, expressed as ordinary kuchka quantities.

    from kuchka import Hertz
    from kuchka.constants import SPEED_OF_LIGHT

    wifi_wavelength = SPEED_OF_LIGHT / Hertz(2_400_000_000)

Two different kinds of "exact" live in this module, and each constant's docstring says
which one applies:

- SI-defining constants (`SPEED_OF_LIGHT`, `ELEMENTARY_CHARGE`) have been exact by
    definition since the 2019 SI redefinition.
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

from kuchka.units import Coulomb as _Coulomb
from kuchka.units import Kilogram as _Kilogram
from kuchka.units import MetrePerSecond as _MetrePerSecond

if TYPE_CHECKING:
    from kuchka.quantities import Charge
    from kuchka.quantities import Mass
    from kuchka.quantities import Velocity

ALPHA_PARTICLE_MASS: Mass = _Kilogram(_Decimal("6.6446573450e-27"))
"""Alpha particle mass.

Accuracy: Measured.
Value: 6.644 657 3450 e-27 kg.
Uncertainty: 0.000 000 0021 e-27 kg.
Link: https://en.wikipedia.org/wiki/Alpha_particle
"""

ELECTRON_MASS: Mass = _Kilogram(_Decimal("9.1093837139E-31"))
"""The electron rest mass, m_e.

Accuracy: Measured.
Value: 9.109 383 7139 e-31 kg.
Uncertainty: 0.000 000 0028 e-31 kg.
Link: https://en.wikipedia.org/wiki/Electron_mass
"""

ELEMENTARY_CHARGE: Charge = _Coulomb(_Decimal("1.602176634e-19"))
"""The elementary charge, e.

Accuracy: Exact.
Value: 1.602 176 634 e-19 C.
Uncertainty: None.
Link: https://en.wikipedia.org/wiki/Elementary_charge
"""

SPEED_OF_LIGHT_IN_VACUUM: Velocity = _MetrePerSecond(299_792_458)
"""The speed of light in vacuum, c.

Accuracy: Exact.
Value: 299 792 458 m s^-1.
Uncertainty: None.
Link: https://en.wikipedia.org/wiki/Speed_of_light
"""

NEUTRON_MASS: Mass = _Kilogram(_Decimal("1.67492750056E-27"))
"""The neutron rest mass, m_n.

Accuracy: Measured.
Value: 1.674 927 500 56 e-27 kg.
Uncertainty: 0.000 000 000 85 e-27 kg.
Link: https://en.wikipedia.org/wiki/Neutron#Mass
"""

PROTON_MASS: Mass = _Kilogram(_Decimal("1.67262192595E-27"))
"""The proton rest mass, m_p.

Accuracy: Measured.
Value: 1.672 621 925 95 e-27 kg.
Uncertainty: 0.000 000 000 52 e-27 kg.
Link: https://en.wikipedia.org/wiki/Proton
"""


