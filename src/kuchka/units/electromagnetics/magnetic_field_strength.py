"""Magnetic field strength constructors: amperes per metre, with prefixes.

Magnetic field strength (H) describes the magnetising field associated with free
currents.
Ampère's law relates its circulation around a closed path to the free current enclosed.
For a long solenoid with N turns, length l, and current I, the field inside is
approximately H = NI/l.

In vacuum, magnetic flux density follows B = μ₀H.
More generally, in SI, B = μ₀(H + M), where M is the material's magnetization.
In a linear, isotropic medium, the relationship can also be written B = μH using the
absolute permeability μ of that medium.

Magnetization has the same dimension and unit as magnetic field strength, but it is a
distinct physical quantity.
In `kuchka`'s quantity-kind model, `Magnetization` is a role of
`MagneticFieldStrength`.
The conversion `MagneticFieldStrength.to_magnetization()` preserves the numerical
reading and changes its quantity kind; it does not calculate a material's magnetization
from its applied field.

Examples
--------
A long air-cored solenoid has 1200 turns over 0.4 m and carries 2.5 A.
Its field strength follows from the ampere-turns per metre.
Vacuum permeability then gives the magnetic flux density inside the winding:

>>> from kuchka import Ampere
>>> from kuchka import Metre
>>> from kuchka import MicrohenryPerMetre
>>> from kuchka.units import MILLITESLA
>>> turns = 1200
>>> solenoid_field = turns * Ampere(2.5) / Metre(0.4)
>>> solenoid_field
7500 A/m
>>> vacuum_permeability = MicrohenryPerMetre(1.25663706127)
>>> (vacuum_permeability * solenoid_field).to(MILLITESLA)
9.424777959525 mT

The geomagnetic field near Earth's surface is roughly 50 µT.
In air, whose permeability is very close to μ₀, this corresponds to a field strength of
about 39.8 A/m:

>>> from kuchka import Microtesla
>>> f"{Microtesla(50) / vacuum_permeability:.1f}"
'39.8 A/m'

Notes
-----
The solenoid relationship assumes a sufficiently long winding and neglects end effects.
Magnetic materials can substantially change the resulting flux density, and
ferromagnetic responses depend on field strength, temperature, and magnetic history.

`MAGNETIC_FIELD_STRENGTH_UNITS` maps symbols such as ``"µA/m"``, ``"mA/m"``, ``"A/m"``,
``"kA/m"``, and ``"MA/m"`` to their constructors.
It is intended for boundary code that reads field strengths from instruments, material
measurements, and electromagnetic simulations.

References
----------
HyperPhysics, Magnetic Field Strength H:
https://www.hyperphysics.phy-astr.gsu.edu/hbase/magnetic/magfield.html

NOAA National Centers for Environmental Information, Geomagnetism FAQs:
https://www.ncei.noaa.gov/products/geomagnetism-frequently-asked-questions

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
    """Construct magnetic field strength from microamperes per metre.

    Parameters
    ----------
    value : Numeric
        Field strength in µA/m.

    Returns
    -------
    MagneticFieldStrength
        Field strength represented in microamperes per metre.

    Examples
    --------
    A weak magnetic-field residual of 0.5 pT is measured in air.
    Dividing its flux density by vacuum permeability gives the corresponding field
    strength:

    >>> from kuchka import MicrohenryPerMetre
    >>> from kuchka import Picotesla
    >>> residual_field = Picotesla(0.5)
    >>> vacuum_permeability = MicrohenryPerMetre(1.25663706127)
    >>> f"{(residual_field / vacuum_permeability).to(MICROAMPERE_PER_METRE):.3f}"
    '0.398 µA/m'

    """
    return MagneticFieldStrength(
        to_exact(value) * MICROAMPERE_PER_METRE.scale, MICROAMPERE_PER_METRE
    )


def MilliamperePerMetre(value: Numeric) -> MagneticFieldStrength:
    """Construct magnetic field strength from milliamperes per metre.

    Parameters
    ----------
    value : Numeric
        Field strength in mA/m.

    Returns
    -------
    MagneticFieldStrength
        Field strength represented in milliamperes per metre.

    Examples
    --------
    A small calibration solenoid has 50 turns over a 10 cm winding length.
    Driving 2 µA through its winding produces a field strength of 1 mA/m under the
    long-solenoid approximation:

    >>> from kuchka import Metre
    >>> from kuchka import Microampere
    >>> turns = 50
    >>> calibration_current = Microampere(2)
    >>> winding_length = Metre(0.1)
    >>> field = turns * calibration_current / winding_length
    >>> field.to(MILLIAMPERE_PER_METRE)
    1 mA/m

    """
    return MagneticFieldStrength(
        to_exact(value) * MILLIAMPERE_PER_METRE.scale, MILLIAMPERE_PER_METRE
    )


def AmperePerMetre(value: Numeric) -> MagneticFieldStrength:
    """Construct magnetic field strength from amperes per metre.

    Parameters
    ----------
    value : Numeric
        Field strength in A/m.

    Returns
    -------
    MagneticFieldStrength
        Field strength represented in amperes per metre.

    Examples
    --------
    A long straight wire carries 1 A.
    At a distance of 5 cm from the wire, Ampère's law gives a field strength of
    approximately 3.18 A/m:

    >>> from math import pi
    >>> from kuchka import Ampere
    >>> from kuchka import Metre
    >>> wire_current = Ampere(1)
    >>> observation_distance = Metre(0.05)
    >>> field = wire_current / (2 * pi * observation_distance)
    >>> f"{field:.2f}"
    '3.18 A/m'

    Notes
    -----
    The expression applies outside a long straight conductor carrying a steady current.
    It calculates H, independently of the permeability of the surrounding material.

    """
    return MagneticFieldStrength(
        to_exact(value) * AMPERE_PER_METRE.scale, AMPERE_PER_METRE
    )


def KiloamperePerMetre(value: Numeric) -> MagneticFieldStrength:
    """Construct magnetic field strength from kiloamperes per metre.

    Parameters
    ----------
    value : Numeric
        Field strength in kA/m.

    Returns
    -------
    MagneticFieldStrength
        Field strength represented in kiloamperes per metre.

    Examples
    --------
    A magnetic separator needs a field strength of 20 kA/m across a 30 cm winding.
    Calculate the required ampere-turn product, then the current needed for a winding
    with 60 turns:

    >>> from kuchka import KiloamperePerMetre
    >>> from kuchka import Metre
    >>> target_field = KiloamperePerMetre(20)
    >>> winding_length = Metre(0.3)
    >>> ampere_turns = target_field * winding_length
    >>> ampere_turns
    6000 A
    >>> ampere_turns / 60
    100 A

    The calculation uses the long-solenoid approximation.
    In a real separator, magnetic-circuit geometry and the material's response also
    determine the field in the working gap.

    """
    return MagneticFieldStrength(
        to_exact(value) * KILOAMPERE_PER_METRE.scale, KILOAMPERE_PER_METRE
    )


def MegaamperePerMetre(value: Numeric) -> MagneticFieldStrength:
    """Construct magnetic field strength from megaamperes per metre.

    Parameters
    ----------
    value : Numeric
        Field strength in MA/m.

    Returns
    -------
    MagneticFieldStrength
        Field strength represented in megaamperes per metre.

    Notes
    -----
    Megaampere-per-metre fields are associated with exceptionally intense pulsed
    systems and high magnetizing fields.
    The example uses a pulsed air-core winding and assumes its field during the pulse
    is approximately that of a long solenoid.

    Examples
    --------
    A pulsed-field coil has 200 turns over a 10 cm winding length and carries a peak
    current of 500 A.
    Calculate its field strength and the corresponding flux density in vacuum:

    >>> from kuchka import Ampere
    >>> from kuchka import Metre
    >>> from kuchka import MicrohenryPerMetre
    >>> from kuchka.units import TESLA
    >>> turns = 200
    >>> pulse_current = Ampere(500)
    >>> winding_length = Metre(0.1)
    >>> pulse_field = turns * pulse_current / winding_length
    >>> pulse_field.to(MEGAAMPERE_PER_METRE)
    1 MA/m
    >>> vacuum_permeability = MicrohenryPerMetre(1.25663706127)
    >>> (vacuum_permeability * pulse_field).to(TESLA)
    1.25663706127 T

    """
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
