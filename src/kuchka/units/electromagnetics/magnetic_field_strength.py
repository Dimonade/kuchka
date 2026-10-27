"""Magnetic field strength constructors, from microamperes to megaamperes per metre.

Magnetic field strength (H) is the magnetising field: the part of a magnetic field that
is set by free currents, through Ampère's law.
In a long solenoid of N turns and length l carrying a current I, it is H = NI / l.
In a linear medium of permeability μ, magnetic flux density follows as B = μH.
More generally B = μ0(H + M), where the magnetization M is the material's own response.

Magnetization has the same dimension and the same ampere per metre, but it is a distinct
quantity: `MagneticFieldStrength.to_magnetization()` reads a field strength as a
`Magnetization`, and `kuchka.units.electromagnetics.magnetization` has its table.

Examples
--------
A long air-cored solenoid has 1200 turns over 0.4 m and carries 2.5 A.
Its field strength follows from the ampere-turns per metre, and vacuum permeability
turns that into the flux density inside:

>>> from kuchka import Ampere, Metre, MicrohenryPerMetre
>>> from kuchka.units.electromagnetics.magnetic_flux_density import MILLITESLA
>>> turns = 1200
>>> solenoid_field = turns * Ampere(2.5) / Metre(0.4)
>>> solenoid_field
7500 A/m
>>> vacuum_permeability = MicrohenryPerMetre(1.25663706127)
>>> f"{(vacuum_permeability * solenoid_field).to(MILLITESLA):.3f}"
'9.425 mT'

The geomagnetic field near the surface is about 50 µT.
Dividing a flux density by the permeability of free space gives the field strength:

>>> from kuchka import Microtesla
>>> f"{Microtesla(50) / vacuum_permeability:.1f}"
'39.8 A/m'

Notes
-----
`MAGNETIC_FIELD_STRENGTH_UNITS` maps symbols such as ``"µA/m"``, ``"mA/m"``,
``"A/m"``, ``"kA/m"``, and ``"MA/m"`` to their constructors.
It is intended for boundary code that reads field strengths from instrument or
simulation output.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MAGNETIC_FIELD_STRENGTH
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import MagneticFieldStrength

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable

AMPERE_PER_METRE_NAME = "ampere_per_metre"
AMPERE_PER_METRE_SYMBOL = "A/m"
AMPERE_PER_METRE_WORDS = ("ampere per metre", "ampere per meter")
"""Spoken forms, which prefixed names follow: `milliampere per metre`."""

MICROAMPERE_PER_METRE = prefixed_unit(
    prefixes.MICRO,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIC_FIELD_STRENGTH,
    base_words=AMPERE_PER_METRE_WORDS,
)
MILLIAMPERE_PER_METRE = prefixed_unit(
    prefixes.MILLI,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIC_FIELD_STRENGTH,
    base_words=AMPERE_PER_METRE_WORDS,
)
AMPERE_PER_METRE = prefixed_unit(
    prefixes.UNIT,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIC_FIELD_STRENGTH,
    base_words=AMPERE_PER_METRE_WORDS,
)
KILOAMPERE_PER_METRE = prefixed_unit(
    prefixes.KILO,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIC_FIELD_STRENGTH,
    base_words=AMPERE_PER_METRE_WORDS,
)
MEGAAMPERE_PER_METRE = prefixed_unit(
    prefixes.MEGA,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIC_FIELD_STRENGTH,
    base_words=AMPERE_PER_METRE_WORDS,
)

MagneticFieldStrength._canonical_unit = AMPERE_PER_METRE  # noqa: SLF001 -- this module owns MagneticFieldStrength's canonical unit


def MicroamperePerMetre(value: Numeric) -> MagneticFieldStrength:
    """Construct a field strength from a magnitude in microamperes per metre."""
    return MagneticFieldStrength(
        to_exact(value) * MICROAMPERE_PER_METRE.scale, MICROAMPERE_PER_METRE
    )


def MilliamperePerMetre(value: Numeric) -> MagneticFieldStrength:
    """Construct a field strength from a magnitude in milliamperes per metre."""
    return MagneticFieldStrength(
        to_exact(value) * MILLIAMPERE_PER_METRE.scale, MILLIAMPERE_PER_METRE
    )


def AmperePerMetre(value: Numeric) -> MagneticFieldStrength:
    """Construct a field strength from a magnitude in amperes per metre."""
    return MagneticFieldStrength(
        to_exact(value) * AMPERE_PER_METRE.scale, AMPERE_PER_METRE
    )


def KiloamperePerMetre(value: Numeric) -> MagneticFieldStrength:
    """Construct a field strength from a magnitude in kiloamperes per metre."""
    return MagneticFieldStrength(
        to_exact(value) * KILOAMPERE_PER_METRE.scale, KILOAMPERE_PER_METRE
    )


def MegaamperePerMetre(value: Numeric) -> MagneticFieldStrength:
    """Construct a field strength from a magnitude in megaamperes per metre."""
    return MagneticFieldStrength(
        to_exact(value) * MEGAAMPERE_PER_METRE.scale, MEGAAMPERE_PER_METRE
    )


MAGNETIC_FIELD_STRENGTH_UNITS: UnitTable[MagneticFieldStrength] = unit_table(
    "MAGNETIC_FIELD_STRENGTH_UNITS",
    {
        MICROAMPERE_PER_METRE: MicroamperePerMetre,
        MILLIAMPERE_PER_METRE: MilliamperePerMetre,
        AMPERE_PER_METRE: AmperePerMetre,
        KILOAMPERE_PER_METRE: KiloamperePerMetre,
        MEGAAMPERE_PER_METRE: MegaamperePerMetre,
    },
)

__all__ = [
    "AMPERE_PER_METRE",
    "KILOAMPERE_PER_METRE",
    "MAGNETIC_FIELD_STRENGTH_UNITS",
    "MEGAAMPERE_PER_METRE",
    "MICROAMPERE_PER_METRE",
    "MILLIAMPERE_PER_METRE",
    "AmperePerMetre",
    "KiloamperePerMetre",
    "MegaamperePerMetre",
    "MicroamperePerMetre",
    "MilliamperePerMetre",
]
