"""Electric field strength constructors: volts per metre, centimetre, and millimetre.

`ElectricFieldStrength` is the force on a charge per unit of charge, which is a voltage
per length, and the volt per metre (`V/m`) is its canonical unit.
The module provides the volt per metre with its micro, milli, kilo, and mega forms, and
the volt and kilovolt per centimetre and per millimetre:

>>> from kuchka import KilovoltPerMillimetre
>>> from kuchka import VoltPerMetre
>>> fair_weather = VoltPerMetre(130)
>>> breakdown = KilovoltPerMillimetre(3)

Radio signals are weighed in microvolts and millivolts per metre, the air near the
ground in volts per metre, power lines in kilovolts per metre, and the strength of an
insulator in kilovolts per millimetre.

Examples
--------
A 3 kV/mm field across a 2 mm gap is a 6 kV drop:

>>> from kuchka import Millimetre
>>> KilovoltPerMillimetre(3) * Millimetre(2)
6000 V

A force of 12 N on a charge of 4 C is a field of 3 V/m, and a field times a charge gives
the force back:

>>> from kuchka import Coulomb
>>> from kuchka import Newton
>>> field = Newton(12) / Coulomb(4)
>>> field
3 V/m
>>> field * Coulomb(4)
12 N

A voltage over a gap is a field strength, and a 230 V supply across a 2 mm gap of
insulation sees:

>>> from kuchka import Volt
>>> from kuchka.units import KILOVOLT_PER_METRE
>>> (Volt(230) / Millimetre(2)).to(KILOVOLT_PER_METRE)
115 kV/m

A field and a voltage are different quantities, so the two refuse to add:

>>> VoltPerMetre(1) + Volt(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...

Notes
-----
The quantity is the magnitude of the field, and the direction is the caller's.

`KilovoltPerMillimetre` and `MegavoltPerMetre` are the same scale, as are
`VoltPerMillimetre` and `KilovoltPerMetre`.
They are separate units because each belongs to its own habit: insulation and gap
design work in volts per millimetre, and field mapping in volts per metre.

The dielectric strength of a material is the largest field strength it withstands
before it breaks down, and is quoted in kilovolts per millimetre.
Dry air at normal pressure breaks down near 3 MV/m, which is 3 kV/mm.

`ELECTRIC_FIELD_STRENGTH_UNITS` maps each symbol to its constructor, for boundary code
that reads a unit as a string from outside the application.
It accepts symbols such as ``"V/m"`` and ``"kV/mm"``.

References
----------
BIPM, The International System of Units (SI Brochure), on derived units:
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.Voltage
    A field strength times a length is a voltage.
~kuchka.quantities.Force
    A field strength times a charge is a force.
~kuchka.quantities.Permittivity
    A permittivity times a field strength is a flux density.
~kuchka.quantities.ElectricFluxDensity
    The flux that a field produces in a medium.

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
    """Construct an ElectricFieldStrength from a magnitude in volts per metre.

    Parameters
    ----------
    value : Numeric
        Field strength magnitude in volts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in volts per metre.

    Examples
    --------
    In fair weather, the electric field of the air at the ground is about 130 V/m:

    >>> fair_weather = VoltPerMetre(130)
    >>> fair_weather
    130 V/m

    Over the height of a person of 1.8 m, that field drops about 230 volts between head
    and feet:

    >>> from kuchka import Metre
    >>> fair_weather * Metre(1.8)
    234 V

    """
    return ElectricFieldStrength(to_exact(value) * VOLT_PER_METRE.scale, VOLT_PER_METRE)


def MicrovoltPerMetre(value: Numeric) -> ElectricFieldStrength:
    """Construct an ElectricFieldStrength from a magnitude in microvolts per metre.

    Parameters
    ----------
    value : Numeric
        Field strength magnitude in microvolts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in microvolts per metre.

    Examples
    --------
    A weak broadcast signal arrives with a field strength of 50 µV/m at an antenna:

    >>> signal = MicrovoltPerMetre(50)
    >>> signal
    50 µV/m

    Receiver specifications quote the same field in millivolts per metre:

    >>> from kuchka.units import MILLIVOLT_PER_METRE
    >>> signal.to(MILLIVOLT_PER_METRE)
    0.05 mV/m

    """
    return ElectricFieldStrength(
        to_exact(value) * MICROVOLT_PER_METRE.scale, MICROVOLT_PER_METRE
    )


def MillivoltPerMetre(value: Numeric) -> ElectricFieldStrength:
    """Construct an ElectricFieldStrength from a magnitude in millivolts per metre.

    Parameters
    ----------
    value : Numeric
        Field strength magnitude in millivolts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in millivolts per metre.

    Examples
    --------
    A medium-wave station draws its coverage contour where the field falls to
    0.5 mV/m:

    >>> contour = MillivoltPerMetre(0.5)
    >>> contour
    0.5 mV/m

    A thousand millivolts per metre are one volt per metre:

    >>> from kuchka import VoltPerMetre
    >>> MillivoltPerMetre(1000) == VoltPerMetre(1)
    True

    """
    return ElectricFieldStrength(
        to_exact(value) * MILLIVOLT_PER_METRE.scale, MILLIVOLT_PER_METRE
    )


def KilovoltPerMetre(value: Numeric) -> ElectricFieldStrength:
    """Construct an ElectricFieldStrength from a magnitude in kilovolts per metre.

    Parameters
    ----------
    value : Numeric
        Field strength magnitude in kilovolts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in kilovolts per metre.

    Examples
    --------
    The international reference level for public exposure to a 50 Hz electric field is
    5 kV/m, about what stands under a high-voltage transmission line:

    >>> level = KilovoltPerMetre(5)
    >>> level
    5 kV/m

    On a particle that carries 2 µC, that field pushes with 10 mN:

    >>> from kuchka import Microcoulomb
    >>> from kuchka.units import MILLINEWTON
    >>> (level * Microcoulomb(2)).to(MILLINEWTON)
    10 mN

    """
    return ElectricFieldStrength(
        to_exact(value) * KILOVOLT_PER_METRE.scale, KILOVOLT_PER_METRE
    )


def MegavoltPerMetre(value: Numeric) -> ElectricFieldStrength:
    """Construct an ElectricFieldStrength from a magnitude in megavolts per metre.

    Parameters
    ----------
    value : Numeric
        Field strength magnitude in megavolts per metre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in megavolts per metre.

    Examples
    --------
    Dry air breaks down in a field of about 3 MV/m:

    >>> breakdown = MegavoltPerMetre(3)
    >>> breakdown
    3 MV/m

    Across a gap of 1 cm, that field is a potential difference of 30 kV, which is why a
    spark jumps about a centimetre at that voltage:

    >>> from kuchka import Centimetre
    >>> from kuchka.units import KILOVOLT
    >>> (breakdown * Centimetre(1)).to(KILOVOLT)
    30 kV

    """
    return ElectricFieldStrength(
        to_exact(value) * MEGAVOLT_PER_METRE.scale, MEGAVOLT_PER_METRE
    )


def VoltPerCentimetre(value: Numeric) -> ElectricFieldStrength:
    """Construct an ElectricFieldStrength from a magnitude in volts per centimetre.

    Parameters
    ----------
    value : Numeric
        Field strength magnitude in volts per centimetre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in volts per centimetre.

    Examples
    --------
    A gel electrophoresis run drives DNA through the gel at about 5 V/cm:

    >>> gel = VoltPerCentimetre(5)
    >>> gel
    5 V/cm

    Over a gel of 15 cm, the power supply sets:

    >>> from kuchka import Centimetre
    >>> gel * Centimetre(15)
    75 V

    """
    return ElectricFieldStrength(
        to_exact(value) * VOLT_PER_CENTIMETRE.scale, VOLT_PER_CENTIMETRE
    )


def KilovoltPerCentimetre(value: Numeric) -> ElectricFieldStrength:
    """Construct an ElectricFieldStrength from a magnitude in kilovolts per centimetre.

    Parameters
    ----------
    value : Numeric
        Field strength magnitude in kilovolts per centimetre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in kilovolts per centimetre.

    Examples
    --------
    Bacterial electroporation uses pulses of about 12.5 kV/cm:

    >>> pulse = KilovoltPerCentimetre(12.5)
    >>> pulse
    12.5 kV/cm

    In a cuvette with a gap of 1 mm, that field takes a charge of 1250 V:

    >>> from kuchka import Millimetre
    >>> pulse * Millimetre(1)
    1250 V

    """
    return ElectricFieldStrength(
        to_exact(value) * KILOVOLT_PER_CENTIMETRE.scale, KILOVOLT_PER_CENTIMETRE
    )


def VoltPerMillimetre(value: Numeric) -> ElectricFieldStrength:
    """Construct an ElectricFieldStrength from a magnitude in volts per millimetre.

    Parameters
    ----------
    value : Numeric
        Field strength magnitude in volts per millimetre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in volts per millimetre.

    Examples
    --------
    A 1.5 V cell across a separator 0.3 mm thick sees a field of 5 V/mm:

    >>> from kuchka import Millimetre
    >>> from kuchka import Volt
    >>> from kuchka.units import VOLT_PER_MILLIMETRE
    >>> (Volt(1.5) / Millimetre(0.3)).to(VOLT_PER_MILLIMETRE)
    5 V/mm

    A volt per millimetre is a kilovolt per metre:

    >>> from kuchka import KilovoltPerMetre
    >>> VoltPerMillimetre(1) == KilovoltPerMetre(1)
    True

    """
    return ElectricFieldStrength(
        to_exact(value) * VOLT_PER_MILLIMETRE.scale, VOLT_PER_MILLIMETRE
    )


def KilovoltPerMillimetre(value: Numeric) -> ElectricFieldStrength:
    """Construct an ElectricFieldStrength from a magnitude in kilovolts per millimetre.

    Parameters
    ----------
    value : Numeric
        Field strength magnitude in kilovolts per millimetre.

    Returns
    -------
    ElectricFieldStrength
        ElectricFieldStrength represented in kilovolts per millimetre.

    Examples
    --------
    The dielectric strength of polyethylene insulation is about 20 kV/mm:

    >>> insulation = KilovoltPerMillimetre(20)
    >>> insulation
    20 kV/mm

    A layer 0.5 mm thick withstands 10 kV:

    >>> from kuchka import Millimetre
    >>> from kuchka.units import KILOVOLT
    >>> (insulation * Millimetre(0.5)).to(KILOVOLT)
    10 kV

    A kilovolt per millimetre is a megavolt per metre:

    >>> from kuchka import MegavoltPerMetre
    >>> KilovoltPerMillimetre(1) == MegavoltPerMetre(1)
    True

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
