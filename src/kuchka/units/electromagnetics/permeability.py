"""Permeability constructors: henries per metre, from nano to unit.

Magnetic permeability (μ) describes how a medium relates magnetic flux density (B) to
magnetic field strength (H).
For a linear, isotropic medium, B = μH, and absolute permeability is measured in
henries per metre (H/m).
Relative permeability is the dimensionless ratio μᵣ = μ / μ₀.

Permeability has the same dimensions as inductance per unit length, but they are not
the same physical quantity.
For example, the inductance of a sufficiently long solenoid is approximately
L = μN²A / l: the medium's permeability contributes to the result, while turn count,
cross-sectional area, and coil length determine how that property becomes an
inductance.

Examples
--------
A search-coil probe has 100 turns and a square sensing area 20 mm on each side.
The magnetic field rises from zero to a field strength of 800 A/m over 2 ms.
Using vacuum permeability, estimate the induced voltage.
Assume the field is uniform and perpendicular to the coil.

>>> from kuchka import AmperePerMetre, Metre, MicrohenryPerMetre, Millisecond
>>> vacuum = MicrohenryPerMetre(1.25663706127)
>>> field_strength = AmperePerMetre(800)
>>> flux_density = vacuum * field_strength
>>> sensor_side = Metre(0.02)
>>> sensor_area = sensor_side * sensor_side
>>> flux_change = flux_density * sensor_area
>>> turns = 100
>>> rise_time = Millisecond(2)
>>> induced_voltage = turns * flux_change / rise_time
>>> f"{flux_density:.6f}"
'0.001005 T'
>>> f"{induced_voltage:.5f}"
'0.02011 V'

Notes
-----
The 2022 CODATA recommended value of vacuum permeability is
μ₀ = 1.256 637 061 27(20) x 10⁻⁶ H/m.
The older approximation μ₀ ≈ 4π x 10⁻⁷ H/m remains useful for many engineering
calculations, but it is no longer an exact consequence of the SI definition.

Material permeability is often quoted as a relative value μᵣ, rather than as an
absolute value in H/m.
Convert it to absolute permeability with μ = μᵣμ₀ before constructing a quantity with
these units.
This relationship assumes the stated relative permeability is appropriate for the
material's frequency, temperature, and magnetic-field operating point.

`PERMEABILITY_UNITS` maps symbols such as ``"nH/m"``, ``"µH/m"``, ``"mH/m"``, and
``"H/m"`` to constructors.
It is intended for boundary code that reads measurements or material parameters from
configuration files, simulation inputs, and instrument data.

References
----------
OpenStax, *College Physics 2e*, inductance of a solenoid:
https://openstax.org/books/college-physics-2e/pages/23-9-inductance

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import PERMEABILITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Permeability

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

HENRY_PER_METRE_NAME = "henry_per_metre"
HENRY_PER_METRE_SYMBOL = "H/m"
HENRY_PER_METRE_WORDS = ("henry per metre", "henry per meter")
"""Spoken forms, which prefixed names follow: `nanohenry per metre`."""

NANOHENRY_PER_METRE = prefixed_unit(
    prefixes.NANO,
    HENRY_PER_METRE_NAME,
    HENRY_PER_METRE_SYMBOL,
    PERMEABILITY,
    base_words=HENRY_PER_METRE_WORDS,
)
MICROHENRY_PER_METRE = prefixed_unit(
    prefixes.MICRO,
    HENRY_PER_METRE_NAME,
    HENRY_PER_METRE_SYMBOL,
    PERMEABILITY,
    base_words=HENRY_PER_METRE_WORDS,
)
MILLIHENRY_PER_METRE = prefixed_unit(
    prefixes.MILLI,
    HENRY_PER_METRE_NAME,
    HENRY_PER_METRE_SYMBOL,
    PERMEABILITY,
    base_words=HENRY_PER_METRE_WORDS,
)
HENRY_PER_METRE = prefixed_unit(
    prefixes.UNIT,
    HENRY_PER_METRE_NAME,
    HENRY_PER_METRE_SYMBOL,
    PERMEABILITY,
    base_words=HENRY_PER_METRE_WORDS,
)

Permeability._canonical_unit = HENRY_PER_METRE  # noqa: SLF001 -- this module owns Permeability's canonical unit


def NanohenryPerMetre(value: Numeric) -> Permeability:
    """Construct magnetic permeability from nanohenries per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permeability in nH/m.

    Returns
    -------
    Permeability
        The supplied value represented as a magnetic permeability.

    Examples
    --------
    Expressing vacuum permeability in nH/m is convenient for some electromagnetic
    simulation inputs.
    With the 2022 CODATA value, it is about 1256.637 nH/m:

    >>> vacuum = NanohenryPerMetre(1256.63706127)
    >>> f"{vacuum.to(NANOHENRY_PER_METRE):.3f}"
    '1256.637 nH/m'

    A 100-turn air-core winding is 5 cm long and has an effective square cross-section
    2 mm on each side.
    The long-solenoid approximation gives its inductance from the vacuum permeability
    and the winding geometry:

    >>> from kuchka import Metre
    >>> from kuchka.units.electromagnetics.inductance import MICROHENRY
    >>> vacuum = NanohenryPerMetre(1256.63706127)
    >>> cross_section_side = Metre(0.002)
    >>> winding_length = Metre(0.05)
    >>> geometry_factor = cross_section_side * cross_section_side / winding_length
    >>> winding = vacuum * geometry_factor * 100**2
    >>> f"{winding.to(MICROHENRY):.2f}"
    '1.01 µH'

    """
    return Permeability(
        to_exact(value) * NANOHENRY_PER_METRE.scale, NANOHENRY_PER_METRE
    )


def MicrohenryPerMetre(value: Numeric) -> Permeability:
    """Construct magnetic permeability from microhenries per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permeability in µH/m.

    Returns
    -------
    Permeability
        The supplied value represented as a magnetic permeability.

    Examples
    --------
    A material sample produces a flux density of 2 mT under a magnetic field strength
    of 1600 A/m.
    If the response is linear at the measurement point, the ratio of the two readings
    gives its absolute permeability:

    >>> from kuchka import AmperePerMetre, Millitesla
    >>> measured_flux_density = Millitesla(2)
    >>> field_strength = AmperePerMetre(1600)
    >>> measured_permeability = measured_flux_density / field_strength
    >>> f"{measured_permeability.to(MICROHENRY_PER_METRE):.2f}"
    '1.25 µH/m'

    """
    return Permeability(
        to_exact(value) * MICROHENRY_PER_METRE.scale, MICROHENRY_PER_METRE
    )


def MillihenryPerMetre(value: Numeric) -> Permeability:
    """Construct magnetic permeability from millihenries per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permeability in mH/m.

    Returns
    -------
    Permeability
        The supplied value represented as a magnetic permeability.

    Notes
    -----
    A relative permeability near 800 is a plausible illustrative low-field value for a
    high-permeability core, but it is not a universal property of ferrites.
    Real cores must be characterised at the relevant frequency, temperature, and field
    strength.

    Examples
    --------
    A closed ferrite core has a measured absolute permeability of 1.005 mH/m.
    An 80-turn winding has a square cross-section 1 cm on each side and a magnetic path
    length of 10 cm.
    Neglecting the effects of an air gap, leakage flux, and core nonlinearity, estimate
    the winding inductance:

    >>> from kuchka import Metre
    >>> from kuchka.units.electromagnetics.inductance import MILLIHENRY
    >>> core = MillihenryPerMetre(1.005)
    >>> core_side = Metre(0.01)
    >>> magnetic_path = Metre(0.1)
    >>> geometry_factor = core_side * core_side / magnetic_path
    >>> winding = core * geometry_factor * 80**2
    >>> f"{winding.to(MILLIHENRY):.2f}"
    '6.43 mH'

    """
    return Permeability(
        to_exact(value) * MILLIHENRY_PER_METRE.scale, MILLIHENRY_PER_METRE
    )


def HenryPerMetre(value: Numeric) -> Permeability:
    """Construct magnetic permeability from henries per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permeability in H/m.

    Returns
    -------
    Permeability
        The supplied value represented as a magnetic permeability.

    Notes
    -----
    Values around 1 H/m are enormous compared with ordinary magnetic materials.
    Use values of this scale only when supported by a specific model or when an
    example is explicitly fictional.

    Examples
    --------
    In a fictional spacecraft, a field-confinement medium has an effective permeability
    of 0.25 H/m.
    A field strength of 2 A/m produces a flux density of 0.5 T.
    Estimate the magnetic flux through a circular aperture of radius 2 m, assuming the
    field is uniform and perpendicular to the aperture:

    >>> from math import pi
    >>> from kuchka import AmperePerMetre, Metre
    >>> confinement_medium = HenryPerMetre(0.25)
    >>> field_strength = AmperePerMetre(2)
    >>> flux_density = confinement_medium * field_strength
    >>> aperture_radius = Metre(2)
    >>> aperture_area = pi * aperture_radius * aperture_radius
    >>> magnetic_flux = flux_density * aperture_area
    >>> f"{magnetic_flux:.2f}"
    '6.28 Wb'

    """
    return Permeability(to_exact(value) * HENRY_PER_METRE.scale, HENRY_PER_METRE)


PERMEABILITY_UNITS: Mapping[str, Callable[[Numeric], Permeability]] = unit_table(
    "PERMEABILITY_UNITS",
    {
        NANOHENRY_PER_METRE: NanohenryPerMetre,
        MICROHENRY_PER_METRE: MicrohenryPerMetre,
        MILLIHENRY_PER_METRE: MillihenryPerMetre,
        HENRY_PER_METRE: HenryPerMetre,
    },
)

__all__ = [
    "HENRY_PER_METRE",
    "MICROHENRY_PER_METRE",
    "MILLIHENRY_PER_METRE",
    "NANOHENRY_PER_METRE",
    "PERMEABILITY_UNITS",
    "HenryPerMetre",
    "MicrohenryPerMetre",
    "MillihenryPerMetre",
    "NanohenryPerMetre",
]
