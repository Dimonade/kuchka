"""Magnetic flux density constructors, from femtoteslas to kiloteslas.

The tesla (T) is the SI unit of magnetic flux density: 1 T = 1 Wb/m².
Magnetic flux density (B) describes the magnetic flux passing through a unit area
perpendicular to the field.
It is distinct from magnetic field strength (H), which is measured in amperes per
metre, and from magnetic permeability (μ), which describes a material's magnetic
response.

The useful scale depends on the application.
Femtoteslas describe the weak signals detected by magnetoencephalography; nanoteslas
are convenient for geophysical surveys and planetary magnetometers; microteslas
describe Earth's surface field and parts of planetary magnetospheres.
Milliteslas and teslas appear in magnetic separation, laboratory magnets, and medical
imaging.
Kiloteslas describe exceptionally intense pulsed fields.

Examples
--------
A geomagnetic survey uses a 10 cm square loop to estimate the flux through the loop
when its plane is perpendicular to a representative 50 µT field at Earth's surface.
The field varies by location, but this gives a useful scale for the measurement:

>>> from kuchka import Metre, Microtesla
>>> from kuchka.units.electromagnetics.magnetic_flux import MICROWEBER
>>> terrestrial_field = Microtesla(50)
>>> loop_side = Metre(0.1)
>>> loop_area = loop_side * loop_side
>>> terrestrial_flux = terrestrial_field * loop_area
>>> terrestrial_flux.to(MICROWEBER)
0.5 µWb

A planetary scientist encounters a different scale at Jupiter.
Its equatorial dipole field at the 1 R_J reference radius is about 4.3 gauss, or
430 µT.
A 5 cm square reference loop normal to this field would intercept:

>>> jovian_field = Microtesla(430)
>>> reference_side = Metre(0.05)
>>> reference_area = reference_side * reference_side
>>> (jovian_field * reference_area).to(MICROWEBER)
1.075 µWb

Notes
-----
Magnetic flux density is a signed/vector quantity physically, but these scalar
constructors represent its magnitude or a selected component.
Subtraction of readings therefore assumes that they refer to the same component and
axis.

The flux calculation B x A assumes a uniform field over the surface and a surface
normal aligned with the field.
For a nonuniform field or arbitrary orientation, magnetic flux requires integration
over the surface.

`MAGNETIC_FLUX_DENSITY_UNITS` maps symbols such as ``"fT"``, ``"pT"``, ``"nT"``,
``"µT"``, ``"mT"``, ``"T"``, and ``"kT"`` to their constructors.
It is intended for boundary code that reads a measurement unit from instrument reports,
geological surveys, simulation inputs, and configuration files.

References
----------
NOAA National Centers for Environmental Information, Geomagnetism FAQs:
https://www.ncei.noaa.gov/products/geomagnetism-frequently-asked-questions

Langlais et al., A New Model of the Crustal Magnetic Field of Mars Using
MGS and MAVEN, Journal of Geophysical Research: Planets, 2019:
https://doi.org/10.1029/2018JE005854

NASA Goddard Space Flight Center, Jupiter Fact Sheet:
https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html

National Institute of Mental Health, Magnetoencephalography Core Facility:
https://www.nimh.nih.gov/research/research-conducted-at-nimh/research-areas/research-support-services/meg

Institute for Solid State Physics, University of Tokyo, 985 T pulsed-field
experiment:
https://www.issp.u-tokyo.ac.jp/maincontents/news2_en.html?pid=4437

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
    A low-noise magnetometer in a magnetoencephalography setup measures a 42 fT
    component, while a reference channel records 27 fT of environmental pickup along
    the same axis.
    Subtracting the reference leaves the corrected signal component:

    >>> from kuchka import Femtotesla
    >>> measured_signal = Femtotesla(42)
    >>> reference_pickup = Femtotesla(27)
    >>> measured_signal - reference_pickup
    15 fT

    These are illustrative readings at the scale of weak brain-generated magnetic
    signals, not measurements from a particular subject.

    """
    return MagneticFluxDensity(to_exact(value) * FEMTOTESLA.scale, FEMTOTESLA)


def Picotesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a magnetic flux density from picoteslas.

    Parameters
    ----------
    value : Numeric
        Magnetic flux density in pT.

    Returns
    -------
    MagneticFluxDensity
        The supplied value represented in picoteslas.

    Examples
    --------
    A geological gradiometer records a 250 pT difference between its reference and
    nearby sensors.
    Adding the measured difference to a reference reading of 1.10 nT reconstructs the
    nearby reading:

    >>> from kuchka import Nanotesla, Picotesla
    >>> reference_reading = Nanotesla(1.10)
    >>> differential_reading = Picotesla(250)
    >>> nearby_reading = reference_reading + differential_reading
    >>> nearby_reading.to(NANOTESLA)
    1.35 nT

    The readings are illustrative.
    Their purpose is to show how a small magnetic anomaly can be combined with a larger
    background measurement.

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
    Mars has no present global magnetic dynamo, but remanent magnetization of its crust
    produces local magnetic anomalies reaching several thousand nanoteslas.
    Consider a 3000 nT anomaly across a one-square-metre surface normal to the field.
    The magnetic flux through that surface is:

    >>> from kuchka import Metre, Nanotesla
    >>> from kuchka.units.electromagnetics.magnetic_flux import MICROWEBER
    >>> crustal_anomaly = Nanotesla(3000)
    >>> survey_side = Metre(1)
    >>> survey_area = survey_side * survey_side
    >>> crustal_flux = crustal_anomaly * survey_area
    >>> crustal_flux.to(MICROWEBER)
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
    Jupiter's equatorial dipole field is about 4.3 gauss at the 1 R_J reference radius,
    approximately 430 µT.
    For a 5 cm square reference loop oriented perpendicular to this field, calculate
    the magnetic flux:

    >>> from kuchka import Metre, Microtesla
    >>> from kuchka.units.electromagnetics.magnetic_flux import MICROWEBER
    >>> jovian_field = Microtesla(430)
    >>> reference_side = Metre(0.05)
    >>> reference_area = reference_side * reference_side
    >>> (jovian_field * reference_area).to(MICROWEBER)
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
    As a laboratory field rises from zero to 15 mT over 2 ms, the change in magnetic
    flux induces an average voltage across the coil:

    >>> from kuchka import Metre, Millisecond, Millitesla
    >>> field_change = Millitesla(15)
    >>> loop_side = Metre(0.01)
    >>> loop_area = loop_side * loop_side
    >>> flux_change = field_change * loop_area
    >>> induced_voltage = 200 * flux_change / Millisecond(2)
    >>> induced_voltage
    0.15 V

    This uses Faraday's law, with the flux change assumed uniform over the loop and
    the winding turns linked by the same flux.

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
    A 3 T research magnet is used to map the flux through a 10 cm square calibration
    loop placed perpendicular to the magnetic field:

    >>> from kuchka import Metre, Tesla
    >>> from kuchka.units.electromagnetics.magnetic_flux import MILLIWEBER
    >>> research_field = Tesla(3)
    >>> loop_side = Metre(0.1)
    >>> loop_area = loop_side * loop_side
    >>> calibration_flux = research_field * loop_area
    >>> calibration_flux.to(MILLIWEBER)
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
    A 2018 University of Tokyo experiment reported a pulsed magnetic field of 985 T,
    or 0.985 kT.
    If a 1 mm square loop were entirely within a region of that peak field, with its
    plane perpendicular to the field, the corresponding flux would be:

    >>> from kuchka import Kilotesla, Millimetre
    >>> from kuchka.units.electromagnetics.magnetic_flux import MILLIWEBER
    >>> peak_field = Kilotesla(0.985)
    >>> loop_side = Millimetre(1)
    >>> loop_area = loop_side * loop_side
    >>> peak_flux = peak_field * loop_area
    >>> peak_flux.to(MILLIWEBER)
    0.985 mWb

    The small-loop calculation is a uniform-field estimate, not a claim that the
    reported peak field filled a loop of this size.

    """
    return MagneticFluxDensity(to_exact(value) * KILOTESLA.scale, KILOTESLA)


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
        },
    )
)

__all__ = [
    "FEMTOTESLA",
    "KILOTESLA",
    "MAGNETIC_FLUX_DENSITY_UNITS",
    "MICROTESLA",
    "MILLITESLA",
    "NANOTESLA",
    "PICOTESLA",
    "TESLA",
    "Femtotesla",
    "Kilotesla",
    "Microtesla",
    "Millitesla",
    "Nanotesla",
    "Picotesla",
    "Tesla",
]
