"""Electric field strength constructors: volts per metre, centimetre, and millimetre.

    from kuchka import KilovoltPerMillimetre
    from kuchka import VoltPerMetre

    mains_wire = VoltPerMetre(5)
    breakdown = KilovoltPerMillimetre(3)

`ElectricFieldStrength` is the force on a charge per charge, `Voltage / Length`.
Its canonical unit is the volt per metre (`V/m`).
The kilovolt per millimetre is the unit the dielectric strength of an insulator is
quoted in.

Examples
--------
A 3 kV/mm field across a 2 mm gap is a 6 kV drop:

>>> from kuchka import Millimetre
>>> KilovoltPerMillimetre(3) * Millimetre(2)
6000 V

A force of 12 N on a charge of 4 C is a field of 3 V/m:

>>> from kuchka import Coulomb
>>> from kuchka import Newton
>>> Newton(12) / Coulomb(4)
3 V/m

`ELECTRIC_FIELD_STRENGTH_UNITS` maps symbols such as ``"V/m"`` and ``"kV/mm"`` to their
constructors, for boundary code that reads a unit as a string from outside the
application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ELECTRIC_FIELD_STRENGTH
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import ElectricFieldStrength
from kuchka.quantities import UnitDef
from kuchka.units.electromagnetics.voltage import VOLT
from kuchka.units.length import CENTIMETRE
from kuchka.units.length import MILLIMETRE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

VOLT_PER_METRE = UnitDef(
    "volt_per_metre",
    "V/m",
    1,
    ELECTRIC_FIELD_STRENGTH,
    words=("volts per metre", "volts per meter"),
)
MICROVOLT_PER_METRE = with_prefix(prefixes.MICRO, VOLT_PER_METRE)
MILLIVOLT_PER_METRE = with_prefix(prefixes.MILLI, VOLT_PER_METRE)
KILOVOLT_PER_METRE = with_prefix(prefixes.KILO, VOLT_PER_METRE)
MEGAVOLT_PER_METRE = with_prefix(prefixes.MEGA, VOLT_PER_METRE)
VOLT_PER_CENTIMETRE = UnitDef(
    "volt_per_centimetre",
    "V/cm",
    VOLT.scale / CENTIMETRE.scale,
    ELECTRIC_FIELD_STRENGTH,
    words=("volts per centimetre", "volts per centimeter"),
)
KILOVOLT_PER_CENTIMETRE = with_prefix(prefixes.KILO, VOLT_PER_CENTIMETRE)
VOLT_PER_MILLIMETRE = UnitDef(
    "volt_per_millimetre",
    "V/mm",
    VOLT.scale / MILLIMETRE.scale,
    ELECTRIC_FIELD_STRENGTH,
    words=("volts per millimetre", "volts per millimeter"),
)
KILOVOLT_PER_MILLIMETRE = with_prefix(prefixes.KILO, VOLT_PER_MILLIMETRE)

ElectricFieldStrength._canonical_unit = VOLT_PER_METRE  # noqa: SLF001 -- this module owns ElectricFieldStrength's canonical unit


def VoltPerMetre(value: Numeric) -> ElectricFieldStrength:
    """Construct a ElectricFieldStrength from volts per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in volts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in volts per metre.

    """
    return ElectricFieldStrength(to_exact(value) * VOLT_PER_METRE.scale, VOLT_PER_METRE)


def MicrovoltPerMetre(value: Numeric) -> ElectricFieldStrength:
    """Construct a ElectricFieldStrength from microvolts per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in microvolts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in microvolts per metre.

    """
    return ElectricFieldStrength(
        to_exact(value) * MICROVOLT_PER_METRE.scale, MICROVOLT_PER_METRE
    )


def MillivoltPerMetre(value: Numeric) -> ElectricFieldStrength:
    """Construct a ElectricFieldStrength from millivolts per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in millivolts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in millivolts per metre.

    """
    return ElectricFieldStrength(
        to_exact(value) * MILLIVOLT_PER_METRE.scale, MILLIVOLT_PER_METRE
    )


def KilovoltPerMetre(value: Numeric) -> ElectricFieldStrength:
    """Construct a ElectricFieldStrength from kilovolts per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilovolts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in kilovolts per metre.

    """
    return ElectricFieldStrength(
        to_exact(value) * KILOVOLT_PER_METRE.scale, KILOVOLT_PER_METRE
    )


def MegavoltPerMetre(value: Numeric) -> ElectricFieldStrength:
    """Construct a ElectricFieldStrength from megavolts per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in megavolts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in megavolts per metre.

    """
    return ElectricFieldStrength(
        to_exact(value) * MEGAVOLT_PER_METRE.scale, MEGAVOLT_PER_METRE
    )


def VoltPerCentimetre(value: Numeric) -> ElectricFieldStrength:
    """Construct a ElectricFieldStrength from volts per centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in volts per centimetre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in volts per centimetre.

    """
    return ElectricFieldStrength(
        to_exact(value) * VOLT_PER_CENTIMETRE.scale, VOLT_PER_CENTIMETRE
    )


def KilovoltPerCentimetre(value: Numeric) -> ElectricFieldStrength:
    """Construct a ElectricFieldStrength from kilovolts per centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilovolts per centimetre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in kilovolts per centimetre.

    """
    return ElectricFieldStrength(
        to_exact(value) * KILOVOLT_PER_CENTIMETRE.scale, KILOVOLT_PER_CENTIMETRE
    )


def VoltPerMillimetre(value: Numeric) -> ElectricFieldStrength:
    """Construct a ElectricFieldStrength from volts per millimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in volts per millimetre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in volts per millimetre.

    """
    return ElectricFieldStrength(
        to_exact(value) * VOLT_PER_MILLIMETRE.scale, VOLT_PER_MILLIMETRE
    )


def KilovoltPerMillimetre(value: Numeric) -> ElectricFieldStrength:
    """Construct a ElectricFieldStrength from kilovolts per millimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilovolts per millimetre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in kilovolts per millimetre.

    """
    return ElectricFieldStrength(
        to_exact(value) * KILOVOLT_PER_MILLIMETRE.scale, KILOVOLT_PER_MILLIMETRE
    )


ELECTRIC_FIELD_STRENGTH_UNITS: Mapping[
    str, Callable[[Numeric], ElectricFieldStrength]
] = unit_table(
    "ELECTRIC_FIELD_STRENGTH_UNITS",
    {
        VOLT_PER_METRE: VoltPerMetre,
        MICROVOLT_PER_METRE: MicrovoltPerMetre,
        MILLIVOLT_PER_METRE: MillivoltPerMetre,
        KILOVOLT_PER_METRE: KilovoltPerMetre,
        MEGAVOLT_PER_METRE: MegavoltPerMetre,
        VOLT_PER_CENTIMETRE: VoltPerCentimetre,
        KILOVOLT_PER_CENTIMETRE: KilovoltPerCentimetre,
        VOLT_PER_MILLIMETRE: VoltPerMillimetre,
        KILOVOLT_PER_MILLIMETRE: KilovoltPerMillimetre,
    },
)

__all__ = [
    "ELECTRIC_FIELD_STRENGTH_UNITS",
    "KILOVOLT_PER_CENTIMETRE",
    "KILOVOLT_PER_METRE",
    "KILOVOLT_PER_MILLIMETRE",
    "MEGAVOLT_PER_METRE",
    "MICROVOLT_PER_METRE",
    "MILLIVOLT_PER_METRE",
    "VOLT_PER_CENTIMETRE",
    "VOLT_PER_METRE",
    "VOLT_PER_MILLIMETRE",
    "KilovoltPerCentimetre",
    "KilovoltPerMetre",
    "KilovoltPerMillimetre",
    "MegavoltPerMetre",
    "MicrovoltPerMetre",
    "MillivoltPerMetre",
    "VoltPerCentimetre",
    "VoltPerMetre",
    "VoltPerMillimetre",
]
