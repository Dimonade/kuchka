"""Permittivity constructors, from picofarads per metre to farads per metre.

Permittivity (ε) describes how a dielectric responds to an electric field.
For a linear, isotropic material, electric displacement and field are related by
D = εE.
Absolute permittivity is measured in farads per metre (F/m).
Relative permittivity (εᵣ) is dimensionless, with ε = εᵣ ε₀.

F/m is also the dimension of capacitance per unit length, but these are distinct
physical quantities.
For example, the capacitance per metre of a coaxial cable depends on both the
dielectric permittivity and the conductor geometry.
This module constructs `Permittivity` only.

Examples
--------
An RF engineer estimates the absolute permittivity of the polyethylene dielectric used
in a coaxial cable.
Using the 2022 CODATA value of vacuum permittivity and a relative permittivity of 2.25
gives about 19.92 pF/m:

>>> from math import log, pi
>>> vacuum = PicofaradPerMetre(8.8541878188)
>>> polyethylene = vacuum * 2.25
>>> f"{polyethylene.to(PICOFARAD_PER_METRE):.2f}"
'19.92 pF/m'

For a coaxial geometry with inner-conductor radius 0.292 mm and shield radius 1.855 mm,
the ideal capacitance per length is C` = 2πε / ln(b/a).
The geometry turns the material permittivity into a different quantity, capacitance per
length:

>>> epsilon_pF_per_m = 8.8541878188 * 2.25
>>> capacitance_pF_per_m = 2 * pi * epsilon_pF_per_m / log(1.855 / 0.292)
>>> round(capacitance_pF_per_m, 1)
67.7

A field-energy estimate uses the same material property.
At an electric-field strength of 1 MV/m, a linear dielectric with this permittivity
stores about 9.96 J/m³ of electric-field energy:

>>> energy_density_J_per_m3 = 0.5 * (8.8541878188e-12 * 2.25) * (1_000_000**2)
>>> round(energy_density_J_per_m3, 2)
9.96

Notes
-----
The vacuum value used above is the 2022 CODATA recommended value,
ε₀ = 8.8541878188(14) x 10⁻¹² F/m.
Material permittivity depends on the dielectric and may vary with frequency,
temperature, and measurement conditions.
The polyethylene value here is the nominal value used in the cited coaxial-cable
example, not a universal value for all polyethylene formulations.

`PERMITTIVITY_UNITS` maps symbols such as ``"pF/m"``, ``"nF/m"``, and ``"F/m"`
to their constructors. It is intended for boundary code that reads a unit
from configuration files, material data, or external instrument reports.

References
----------
NIST, 2022 CODATA value of vacuum electric permittivity:
https://physics.nist.gov/cgi-bin/cuu/Value?ep0

Engineering LibreTexts, coaxial-line equations and the RG-59 example:
https://phys.libretexts.org/Bookshelves/Electricity_and_Magnetism/Electromagnetics_I_%28Ellingson%29/05%3A_Electrostatics/5.24%3A_Capacitance_of_a_Coaxial_Structure

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import PERMITTIVITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Permittivity

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

FARAD_PER_METRE_NAME = "farad_per_metre"
FARAD_PER_METRE_SYMBOL = "F/m"
FARAD_PER_METRE_WORDS = ("farad per metre", "farad per meter")
"""Spoken forms, which prefixed names follow: `picofarad per metre`."""

PICOFARAD_PER_METRE = prefixed_unit(
    prefixes.PICO,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
NANOFARAD_PER_METRE = prefixed_unit(
    prefixes.NANO,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
MICROFARAD_PER_METRE = prefixed_unit(
    prefixes.MICRO,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
MILLIFARAD_PER_METRE = prefixed_unit(
    prefixes.MILLI,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
FARAD_PER_METRE = prefixed_unit(
    prefixes.UNIT,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)

Permittivity._canonical_unit = FARAD_PER_METRE  # noqa: SLF001 -- this module owns Permittivity's canonical unit


def PicofaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from picofarads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in pF/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Examples
    --------
    The 2022 CODATA vacuum permittivity is approximately 8.8542 pF/m:

    >>> vacuum = PicofaradPerMetre(8.8541878188)
    >>> f"{vacuum.to(PICOFARAD_PER_METRE):.4f}"
    '8.8542 pF/m'

    """
    return Permittivity(
        to_exact(value) * PICOFARAD_PER_METRE.scale, PICOFARAD_PER_METRE
    )


def NanofaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from nanofarads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in nF/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Notes
    -----
    Values in nF/m are far above the permittivity of vacuum, so this scale can be
    useful when representing a high-permittivity material or a deliberately effective,
    frequency-dependent dielectric model.

    Examples
    --------
    A model with an absolute permittivity of 1 nF/m corresponds to 1000 pF/m:

    >>> f"{NanofaradPerMetre(1).to(PICOFARAD_PER_METRE):.0f}"
    '1000 pF/m'

    """
    return Permittivity(
        to_exact(value) * NANOFARAD_PER_METRE.scale, NANOFARAD_PER_METRE
    )


def MicrofaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from microfarads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in µF/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Notes
    -----
    This is an extreme scale for ordinary dielectrics.
    It is included for completeness and for models that deliberately use effective
    parameters.

    Examples
    --------
    A fictional starship's electrostatic sail uses an invented field-shaping dielectric
    specified at 0.4 µF/m:

    >>> f"{MicrofaradPerMetre(0.4).to(MICROFARAD_PER_METRE):.1f}"
    '0.4 µF/m'

    """
    return Permittivity(
        to_exact(value) * MICROFARAD_PER_METRE.scale, MICROFARAD_PER_METRE
    )


def MillifaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from millifarads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in mF/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Notes
    -----
    This scale is not representative of ordinary engineering dielectrics.
    A value this large should be understood as an effective model parameter or as part
    of an explicitly fictional setting.

    Examples
    --------
    A fictional containment lattice is specified with an effective permittivity of
    3 mF/m:

    >>> f"{MillifaradPerMetre(3).to(MILLIFARAD_PER_METRE):.0f}"
    '3 mF/m'

    """
    return Permittivity(
        to_exact(value) * MILLIFARAD_PER_METRE.scale, MILLIFARAD_PER_METRE
    )


def FaradPerMetre(value: Numeric) -> Permittivity:
    """Construct permittivity from farads per metre.

    Parameters
    ----------
    value : Numeric
        Absolute permittivity in F/m.

    Returns
    -------
    Permittivity
        The supplied value represented as a permittivity.

    Notes
    -----
    One F/m is roughly 113 billion times the permittivity of vacuum.
    In this scale, a material example should be treated as speculative or fictional,
    not as a known ordinary dielectric.

    Examples
    --------
    A fictional reactor's field-confinement medium is assigned an effective
    permittivity of 0.75 F/m:

    >>> f"{FaradPerMetre(0.75).to(FARAD_PER_METRE):.2f}"
    '0.75 F/m'

    """
    return Permittivity(to_exact(value) * FARAD_PER_METRE.scale, FARAD_PER_METRE)


PERMITTIVITY_UNITS: Mapping[str, Callable[[Numeric], Permittivity]] = unit_table(
    "PERMITTIVITY_UNITS",
    {
        PICOFARAD_PER_METRE: PicofaradPerMetre,
        NANOFARAD_PER_METRE: NanofaradPerMetre,
        MICROFARAD_PER_METRE: MicrofaradPerMetre,
        MILLIFARAD_PER_METRE: MillifaradPerMetre,
        FARAD_PER_METRE: FaradPerMetre,
    },
)

__all__ = [
    "FARAD_PER_METRE",
    "MICROFARAD_PER_METRE",
    "MILLIFARAD_PER_METRE",
    "NANOFARAD_PER_METRE",
    "PERMITTIVITY_UNITS",
    "PICOFARAD_PER_METRE",
    "FaradPerMetre",
    "MicrofaradPerMetre",
    "MillifaradPerMetre",
    "NanofaradPerMetre",
    "PicofaradPerMetre",
]
