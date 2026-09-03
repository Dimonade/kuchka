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

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.units import Coulomb
from kuchka.units import Kilogram
from kuchka.units import MetrePerSecond

if TYPE_CHECKING:
    from kuchka.quantities import Charge
    from kuchka.quantities import Mass
    from kuchka.quantities import Velocity

SPEED_OF_LIGHT: Velocity = MetrePerSecond(299_792_458)
"""The speed of light in vacuum, c.

Exact by definition: the metre has been defined in terms of c and the second since 1983.
"""

ELEMENTARY_CHARGE: Charge = Coulomb(Decimal("1.602176634E-19"))
"""The elementary charge, e.

Exact by definition since the 2019 SI redefinition: the coulomb is now defined in terms
of e.
"""

ELECTRON_MASS: Mass = Kilogram(Decimal("9.1093837139E-31"))
"""The electron rest mass, m_e.

CODATA 2022 recommended value: 9.109 383 7139(28) x 10^-31 kg. Measured, not exact.
"""

PROTON_MASS: Mass = Kilogram(Decimal("1.67262192595E-27"))
"""The proton rest mass, m_p.

CODATA 2022 recommended value: 1.672 621 925 95(52) x 10^-27 kg. Measured, not exact.
"""

NEUTRON_MASS: Mass = Kilogram(Decimal("1.67492750056E-27"))
"""The neutron rest mass, m_n.

CODATA 2022 recommended value: 1.674 927 500 56(85) x 10^-27 kg. Measured, not exact.
"""
