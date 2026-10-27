"""Magnetic permeability constructors, from nanohenries per metre to henries per metre.

Magnetic permeability (μ) describes how a medium relates magnetic flux density (B) to
magnetic field strength (H).
For a linear, isotropic medium, B = μH, and absolute permeability is measured in
henries per metre (H/m).
Relative permeability is the dimensionless ratio μᵣ = μ / μ₀.

Permeability has the same dimensions as inductance per unit length, but they are not
the same physical quantity.
For example, the inductance of a sufficiently long solenoid is approximately
L = μN²A / ℓ: the medium's permeability contributes to the result, while turn count,
cross-sectional area, and coil length determine how that property becomes an
inductance.

Examples
--------
A long air-core solenoid has 400 turns, a radius of 8 mm, and a length of 20 cm.
Using the recommended vacuum permeability gives an ideal inductance of about 202 µH.
The long-solenoid approximation neglects end effects and assumes the field is nearly
uniform inside the coil:

>>> from math import pi
>>> vacuum = MicrohenryPerMetre(1.25663706127)
>>> mu0 = float(vacuum.magnitude)
>>> turns = 400
>>> radius_m = 8e-3
>>> length_m = 0.2
>>> inductance_microhenries = mu0 * turns**2 * pi * radius_m**2 / length_m * 1e6
>>> f"{inductance_microhenries:.1f} µH"
'202.1 µH'

A low-field model assigns a ferrite core a relative permeability of 800.
This gives an absolute permeability of about 1.005 mH/m.
The figure is a model parameter, not a universal ferrite constant: permeability depends
on material grade, frequency, temperature, and operating field, and can become
nonlinear near saturation.

>>> relative_permeability = 800
>>> core = MillihenryPerMetre(relative_permeability * 1.25663706127e-3)
>>> f"{core.to(MILLIHENRY_PER_METRE):.3f}"
'1.005 mH/m'

Notes
-----

The 2022 CODATA recommended value of vacuum permeability is
μ₀ = 1.256 637 061 27(20) × 10⁻⁶ H/m.
The older approximation μ₀ ≈ 4π × 10⁻⁷ H/m remains useful for many engineering
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
    Vacuum permeability is approximately 1.256637 µH/m.
    For an ideal linear medium, multiplying this value by a field strength of 800 A/m
    predicts a flux density of about 1.005 mT:

    >>> vacuum = MicrohenryPerMetre(1.25663706127)
    >>> magnetic_field_strength_A_per_m = 800
    >>> flux_density_mT = float(vacuum.magnitude) * magnetic_field_strength_A_per_m * 1e3
    >>> f"{flux_density_mT:.3f} mT"
    '1.005 mT'
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
    An idealized core model uses μᵣ = 800.
    Multiplying that ratio by vacuum permeability gives approximately 1.005 mH/m:

    >>> core = MillihenryPerMetre(800 * 1.25663706127e-3)
    >>> f"{core.to(MILLIHENRY_PER_METRE):.3f}"
    '1.005 mH/m'
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
    In a clearly fictional spacecraft setting, a magnetic-field confinement medium is
    assigned an effective permeability of 0.25 H/m.
    If its response is treated as linear, a field strength of 2 A/m corresponds to a
    flux density of 0.5 T:

    >>> confinement_medium = HenryPerMetre(0.25)
    >>> field_strength_A_per_m = 2
    >>> flux_density_T = float(confinement_medium.magnitude) * field_strength_A_per_m
    >>> f"{flux_density_T:.1f} T"
    '0.5 T'
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
