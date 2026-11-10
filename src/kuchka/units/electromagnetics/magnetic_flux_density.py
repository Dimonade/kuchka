"""Magnetic flux density constructors: the tesla and the gauss, with prefixes.

The tesla (T) is the SI unit of magnetic flux density: 1 T = 1 Wb/m².
The gauss (G, also Gs) is the corresponding CGS unit, defined by 1 G = 10⁻⁴ T.
Both measure magnetic flux density B, not magnetic field strength H, which is measured
in amperes per metre.

The two unit families cover very different scales.
Femtoteslas describe weak biomagnetic signals; nanoteslas are useful in planetary and
geological surveys; microteslas describe Earth's surface field and parts of planetary
magnetospheres.
Gauss is common in astrophysics and magnet specifications, while milliteslas and teslas
are common in engineering and medicine.
Kiloteslas describe exceptionally intense pulsed-field experiments.

Examples
--------
A geomagnetic survey estimates a local field of 0.5 G.
A square loop with 10 cm sides is oriented perpendicular to the field.
Assuming the field is uniform across the loop, the flux through it is:

>>> from kuchka import Gauss, Metre
>>> from kuchka.units.electromagnetics.magnetic_flux import MICROWEBER
>>> terrestrial_field = Gauss(0.5)
>>> loop_side = Metre(0.1)
>>> loop_area = loop_side * loop_side
>>> (terrestrial_field * loop_area).to(MICROWEBER)
0.5 µWb

In 2018, the University of Tokyo reported a pulsed magnetic field of 985 T.
That is 9850 kG.
For a hypothetical 1 mm square loop placed in a uniform region at the peak field, the
corresponding flux would be:

>>> from kuchka import Millimetre, Tesla
>>> from kuchka.units.electromagnetics.magnetic_flux import MILLIWEBER
>>> peak_field = Tesla(985)
>>> peak_field.to(KILOGAUSS)
9850 kG
>>> loop_side = Millimetre(1)
>>> loop_area = loop_side * loop_side
>>> (peak_field * loop_area).to(MILLIWEBER)
0.985 mWb

Notes
-----
The gauss family uses the same prefix range as the existing Tesla family.
The `G` symbol is canonical; `Gs` is an accepted alias.
Prefix aliases follow automatically from the base alias, so `mGs` and `kGs` are
accepted alongside `mG` and `kG`.

Magnetic flux density is a vector quantity.
These scalar constructors represent a magnitude or a selected component.
Subtracting measurements therefore assumes that they refer to the same component and
axis.

Flux through a surface is calculated as B x A only when the field is uniform and
perpendicular to the surface.
For nonuniform fields or arbitrary orientations, magnetic flux requires integration
over the surface.

Magnetar surface fields can reach 10¹⁴-10¹⁵ G, equivalent to 10¹⁰-10¹¹ T.
These are inferred astrophysical field strengths; the `Gauss` and `Tesla` constructors
can represent them without additional unit prefixes.

`MAGNETIC_FLUX_DENSITY_UNITS` maps symbols such as ``"fT"``, ``"nT"``, ``"µT"``,
``"T"``, ``"fG"``, ``"nG"``, ``"µG"``, ``"G"``, ``"Gs"``, ``"mG"``, ``"mGs"``,
``"kG"``, and ``"kGs"`` to their constructors.

References
----------
NIST, Guide to the SI, conversion factors for electricity and magnetism:
https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9

NOAA National Centers for Environmental Information, Geomagnetism FAQs:
https://www.ncei.noaa.gov/products/geomagnetism-frequently-asked-questions

NASA Goddard Space Flight Center, Jupiter Fact Sheet:
https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html

University of Tokyo, 985 T pulsed-field experiment:
https://www.issp.u-tokyo.ac.jp/maincontents/news2_en.html?pid=4437

Rea et al., SGR J1745-2900 near the Galactic Centre:
https://doi.org/10.1088/2041-8205/775/2/l34

NASA Goddard Space Flight Center, magnetar magnetic fields:
https://ntrs.nasa.gov/citations/20030034659

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MAGNETIC_FLUX_DENSITY
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import MagneticFluxDensity

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

TESLA_NAME = "tesla"
TESLA_SYMBOL = "T"

FEMTOTESLA = prefixed_unit(
    prefixes.FEMTO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
PICOTESLA = prefixed_unit(
    prefixes.PICO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
NANOTESLA = prefixed_unit(
    prefixes.NANO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
MICROTESLA = prefixed_unit(
    prefixes.MICRO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
MILLITESLA = prefixed_unit(
    prefixes.MILLI, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
TESLA = prefixed_unit(
    prefixes.UNIT,
    TESLA_NAME,
    TESLA_SYMBOL,
    MAGNETIC_FLUX_DENSITY,
    aliases=(f"Wb/m{symbols.SUPERSCRIPT_TWO}", *powered("Wb/m", 2)),
    words=("weber per square metre", "weber per square meter"),
)
KILOTESLA = prefixed_unit(
    prefixes.KILO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)

GAUSS_NAME = "gauss"
GAUSS_SYMBOL = "G"
GAUSS_BASE_ALIASES = ("Gs",)
GAUSS_BASE_WORDS = ("gausses",)

FEMTOGAUSS = prefixed_unit(
    prefixes.FEMTO,
    GAUSS_NAME,
    GAUSS_SYMBOL,
    MAGNETIC_FLUX_DENSITY,
    coherent_offset=-4,
    base_aliases=GAUSS_BASE_ALIASES,
    base_words=GAUSS_BASE_WORDS,
)
PICOGAUSS = prefixed_unit(
    prefixes.PICO,
    GAUSS_NAME,
    GAUSS_SYMBOL,
    MAGNETIC_FLUX_DENSITY,
    coherent_offset=-4,
    base_aliases=GAUSS_BASE_ALIASES,
    base_words=GAUSS_BASE_WORDS,
)
NANOGAUSS = prefixed_unit(
    prefixes.NANO,
    GAUSS_NAME,
    GAUSS_SYMBOL,
    MAGNETIC_FLUX_DENSITY,
    coherent_offset=-4,
    base_aliases=GAUSS_BASE_ALIASES,
    base_words=GAUSS_BASE_WORDS,
)
MICROGAUSS = prefixed_unit(
    prefixes.MICRO,
    GAUSS_NAME,
    GAUSS_SYMBOL,
    MAGNETIC_FLUX_DENSITY,
    coherent_offset=-4,
    base_aliases=GAUSS_BASE_ALIASES,
    base_words=GAUSS_BASE_WORDS,
)
MILLIGAUSS = prefixed_unit(
    prefixes.MILLI,
    GAUSS_NAME,
    GAUSS_SYMBOL,
    MAGNETIC_FLUX_DENSITY,
    coherent_offset=-4,
    base_aliases=GAUSS_BASE_ALIASES,
    base_words=GAUSS_BASE_WORDS,
)
GAUSS = prefixed_unit(
    prefixes.UNIT,
    GAUSS_NAME,
    GAUSS_SYMBOL,
    MAGNETIC_FLUX_DENSITY,
    coherent_offset=-4,
    base_aliases=GAUSS_BASE_ALIASES,
    base_words=GAUSS_BASE_WORDS,
)
KILOGAUSS = prefixed_unit(
    prefixes.KILO,
    GAUSS_NAME,
    GAUSS_SYMBOL,
    MAGNETIC_FLUX_DENSITY,
    coherent_offset=-4,
    base_aliases=GAUSS_BASE_ALIASES,
    base_words=GAUSS_BASE_WORDS,
)

MagneticFluxDensity._canonical_unit = TESLA  # noqa: SLF001 -- this module owns MagneticFluxDensity's canonical unit


def Femtotesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a magnetic flux density from femtoteslas.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in fT.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in femtoteslas.

    Examples
    --------
    A biomagnetic sensor records 480 fT while its reference channel measures 310 fT of
    common pickup along the same axis.
    Subtracting the reference leaves the corrected signal:

    >>> from kuchka import Femtotesla
    >>> signal = Femtotesla(480)
    >>> reference = Femtotesla(310)
    >>> signal - reference
    170 fT

    """
    return MagneticFluxDensity(to_exact(value) * FEMTOTESLA.scale, FEMTOTESLA)


def Picotesla(value: Numeric) -> MagneticFluxDensity:
    """Construct magnetic flux density from picoteslas.

    Examples
    --------
    A precision magnetometer measures a 1.8 nT background and a 250 pT local anomaly.
    Combining the readings gives the total field component:

    >>> from kuchka import Nanotesla, Picotesla
    >>> background = Nanotesla(1.8)
    >>> anomaly = Picotesla(250)
    >>> (background + anomaly).to(NANOTESLA)
    2.05 nT

    """
    return MagneticFluxDensity(to_exact(value) * PICOTESLA.scale, PICOTESLA)


def Nanotesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a magnetic flux density from nanoteslas.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in nT.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in nanoteslas.

    Examples
    --------
    A Mars crustal-field model includes a 3000 nT local anomaly.
    Estimate the magnetic flux through a square metre whose normal is aligned with the
    field:

    >>> from kuchka import Metre, Nanotesla
    >>> from kuchka.units.electromagnetics.magnetic_flux import MICROWEBER
    >>> crustal_anomaly = Nanotesla(3000)
    >>> survey_side = Metre(1)
    >>> survey_area = survey_side * survey_side
    >>> (crustal_anomaly * survey_area).to(MICROWEBER)
    3 µWb

    """
    return MagneticFluxDensity(to_exact(value) * NANOTESLA.scale, NANOTESLA)


def Microtesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a magnetic flux density from microteslas.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in µT.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in microteslas.

    Examples
    --------
    Jupiter's equatorial dipole field at the 1 R_J reference radius is about 4.3 G, or
    430 µT.
    Estimate the flux through a 5 cm square loop perpendicular to that field:

    >>> from kuchka import Metre, Microtesla
    >>> from kuchka.units.electromagnetics.magnetic_flux import MICROWEBER
    >>> jovian_field = Microtesla(430)
    >>> loop_side = Metre(0.05)
    >>> loop_area = loop_side * loop_side
    >>> (jovian_field * loop_area).to(MICROWEBER)
    1.075 µWb

    """
    return MagneticFluxDensity(to_exact(value) * MICROTESLA.scale, MICROTESLA)


def Millitesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a magnetic flux density from milliteslas.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in mT.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in milliteslas.

    Examples
    --------
    A 200-turn pickup coil has a 1 cm square area.
    If the field rises from zero to 15 mT in 2 ms, Faraday's law predicts the average
    induced voltage across the winding:

    >>> from kuchka import Metre, Millisecond, Millitesla
    >>> field_change = Millitesla(15)
    >>> loop_side = Metre(0.01)
    >>> loop_area = loop_side * loop_side
    >>> flux_change = field_change * loop_area
    >>> turns = 200
    >>> induced_voltage = turns * flux_change / Millisecond(2)
    >>> induced_voltage
    0.15 V

    """
    return MagneticFluxDensity(to_exact(value) * MILLITESLA.scale, MILLITESLA)


def Tesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a magnetic flux density from teslas.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in T.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in teslas.

    Examples
    --------
    A 3 T MRI field passes through a 10 cm square calibration loop placed perpendicular
    to the field.
    The flux through the loop is:

    >>> from kuchka import Metre, Tesla
    >>> from kuchka.units.electromagnetics.magnetic_flux import MILLIWEBER
    >>> scanner_field = Tesla(3)
    >>> loop_side = Metre(0.1)
    >>> loop_area = loop_side * loop_side
    >>> (scanner_field * loop_area).to(MILLIWEBER)
    30 mWb

    """
    return MagneticFluxDensity(to_exact(value) * TESLA.scale, TESLA)


def Kilotesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a magnetic flux density from kiloteslas.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in kT.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in kiloteslas.

    Notes
    -----
    Kilotesla-scale fields occur in exceptionally intense pulsed-field experiments.
    They are transient experimental conditions, not fields sustained by ordinary
    laboratory magnets.

    Examples
    --------
    The University of Tokyo reported a short pulsed magnetic field of 985 T.
    Consider a 1 mm square loop placed in a region where the peak field is uniform.
    Calculate the flux linked by that loop:

    >>> from kuchka import Kilotesla, Millimetre
    >>> from kuchka.units.electromagnetics.magnetic_flux import MILLIWEBER
    >>> peak_field = Kilotesla(0.985)
    >>> loop_side = Millimetre(1)
    >>> loop_area = loop_side * loop_side
    >>> (peak_field * loop_area).to(MILLIWEBER)
    0.985 mWb

    """
    return MagneticFluxDensity(to_exact(value) * KILOTESLA.scale, KILOTESLA)


def Femtogauss(value: Numeric) -> MagneticFluxDensity:
    """Construct magnetic flux density from femtogauss.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in fG.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in femtogauss.

    Examples
    --------
    A fictional deep-space gradiometer stores readings in femtogauss.
    Its sensor reports 1,050,000 fG and the reference channel reports 250,000 fG.
    Subtracting the reference and expressing the residual in femtoteslas gives:

    >>> from kuchka import Femtogauss
    >>> residual = Femtogauss(1_050_000) - Femtogauss(250_000)
    >>> residual.to(FEMTOTESLA)
    80 fT

    """
    return MagneticFluxDensity(to_exact(value) * FEMTOGAUSS.scale, FEMTOGAUSS)


def Picogauss(value: Numeric) -> MagneticFluxDensity:
    """Construct magnetic flux density from picogauss.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in pG.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in picogauss.

    Examples
    --------
    A molecular-cloud simulation uses a 5 µG background field and resolves a 250,000 pG
    enhancement around a denser clump.
    Combine the two readings:

    >>> from kuchka import Microgauss, Picogauss
    >>> background_field = Microgauss(5)
    >>> local_enhancement = Picogauss(250_000)
    >>> (background_field + local_enhancement).to(MICROGAUSS)
    5.25 µG

    """
    return MagneticFluxDensity(to_exact(value) * PICOGAUSS.scale, PICOGAUSS)


def Nanogauss(value: Numeric) -> MagneticFluxDensity:
    """Construct magnetic flux density from nanogauss.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in nG.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in nanogauss.

    Examples
    --------
    A biomagnetic channel records 8 nG, while the reference channel contains 3 nG of
    common pickup.
    The corrected component is 5 nG, equivalent to 500 fT:

    >>> from kuchka import Nanogauss
    >>> corrected_signal = Nanogauss(8) - Nanogauss(3)
    >>> corrected_signal.to(FEMTOTESLA)
    500 fT

    """
    return MagneticFluxDensity(to_exact(value) * NANOGAUSS.scale, NANOGAUSS)


def Microgauss(value: Numeric) -> MagneticFluxDensity:
    """Construct magnetic flux density from microgauss.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in µG.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in microgauss.

    Examples
    --------
    A Milky Way molecular-cloud model uses a field of 5 µG.
    Estimate the flux through a one-square-kilometre simulation cell perpendicular to
    the field:

    >>> from kuchka import Metre, Microgauss
    >>> from kuchka.units.electromagnetics.magnetic_flux import MILLIWEBER
    >>> cloud_field = Microgauss(5)
    >>> cell_side = Metre(1000)
    >>> cell_area = cell_side * cell_side
    >>> (cloud_field * cell_area).to(MILLIWEBER)
    0.5 mWb

    """
    return MagneticFluxDensity(to_exact(value) * MICROGAUSS.scale, MICROGAUSS)


def Milligauss(value: Numeric) -> MagneticFluxDensity:
    """Construct magnetic flux density from milligauss.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in mG.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in milligauss.

    Examples
    --------
    During a magnetic-shielding test, the field through a 10 cm square, 1000-turn
    pickup coil changes by 6 mG over 10 ms.
    Faraday's law gives the average induced voltage:

    >>> from kuchka import Metre, Milligauss, Millisecond
    >>> from kuchka.units.electromagnetics.voltage import MILLIVOLT
    >>> field_change = Milligauss(6)
    >>> loop_side = Metre(0.1)
    >>> loop_area = loop_side * loop_side
    >>> turns = 1000
    >>> induced_voltage = turns * field_change * loop_area / Millisecond(10)
    >>> induced_voltage.to(MILLIVOLT)
    0.6 mV

    """
    return MagneticFluxDensity(to_exact(value) * MILLIGAUSS.scale, MILLIGAUSS)


def Gauss(value: Numeric) -> MagneticFluxDensity:
    """Construct magnetic flux density from gauss.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in G.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in gauss.

    Examples
    --------
    A refrigerator magnet is approximated as producing 50 G over a 1 cm square probe
    area.
    Assuming the field is uniform and perpendicular to the area, estimate the flux:

    >>> from kuchka import Gauss, Metre
    >>> from kuchka.units.electromagnetics.magnetic_flux import MICROWEBER
    >>> magnet_field = Gauss(50)
    >>> probe_side = Metre(0.01)
    >>> probe_area = probe_side * probe_side
    >>> (magnet_field * probe_area).to(MICROWEBER)
    0.5 µWb

    """
    return MagneticFluxDensity(to_exact(value) * GAUSS.scale, GAUSS)


def Kilogauss(value: Numeric) -> MagneticFluxDensity:
    """Construct magnetic flux density from kilogauss.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in kG.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in kilogauss.

    Examples
    --------
    A neodymium magnet's remanence may be around 13 kG.
    As a simplified flux estimate, suppose that field fills a 1 cm square gap in a
    magnetic fixture.
    The actual gap field depends on the magnet and geometry:

    >>> from kuchka import Kilogauss, Metre
    >>> from kuchka.units.electromagnetics.magnetic_flux import MILLIWEBER
    >>> field = Kilogauss(13)
    >>> gap_side = Metre(0.01)
    >>> gap_area = gap_side * gap_side
    >>> (field * gap_area).to(MILLIWEBER)
    0.13 mWb

    """
    return MagneticFluxDensity(to_exact(value) * KILOGAUSS.scale, KILOGAUSS)


MAGNETIC_FLUX_DENSITY_UNITS: Mapping[str, Callable[[Numeric], MagneticFluxDensity]] = (
    unit_table(
        "MAGNETIC_FLUX_DENSITY_UNITS",
        {
            FEMTOTESLA: Femtotesla,
            PICOTESLA: Picotesla,
            NANOTESLA: Nanotesla,
            MICROTESLA: Microtesla,
            MILLITESLA: Millitesla,
            TESLA: Tesla,
            KILOTESLA: Kilotesla,
            FEMTOGAUSS: Femtogauss,
            PICOGAUSS: Picogauss,
            NANOGAUSS: Nanogauss,
            MICROGAUSS: Microgauss,
            MILLIGAUSS: Milligauss,
            GAUSS: Gauss,
            KILOGAUSS: Kilogauss,
        },
    )
)

__all__ = [
    "FEMTOGAUSS",
    "FEMTOTESLA",
    "GAUSS",
    "KILOGAUSS",
    "KILOTESLA",
    "MAGNETIC_FLUX_DENSITY_UNITS",
    "MICROGAUSS",
    "MICROTESLA",
    "MILLIGAUSS",
    "MILLITESLA",
    "NANOGAUSS",
    "NANOTESLA",
    "PICOGAUSS",
    "PICOTESLA",
    "TESLA",
    "Femtogauss",
    "Femtotesla",
    "Gauss",
    "Kilogauss",
    "Kilotesla",
    "Microgauss",
    "Microtesla",
    "Milligauss",
    "Millitesla",
    "Nanogauss",
    "Nanotesla",
    "Picogauss",
    "Picotesla",
    "Tesla",
]
