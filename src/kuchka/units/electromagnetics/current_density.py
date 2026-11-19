"""Current density constructors: amperes per square metre, centimetre, and millimetre.

    from kuchka import AmperePerSquareMillimetre
    from kuchka import MilliamperePerSquareCentimetre

    winding = AmperePerSquareMillimetre(4)
    battery_electrode = MilliamperePerSquareCentimetre(2)

`CurrentDensity` describes electric current distributed over a cross-sectional or
electrode area.
Its canonical, SI-coherent unit is the ampere per square metre (A/m²).

For a uniform current distribution perpendicular to a surface, current density is the
electric current divided by the area:

``J = I/A``

The available units cover several distinct areas of electrical and electrochemical
engineering:

* milliamperes per square metre (mA/m²) describe low current densities in cathodic
    protection, corrosion control, and other large-area systems;
* amperes per square metre (A/m²) are used in electroplating, electrode
    characterization, and industrial electrochemical processes;
* kiloamperes per square metre (kA/m²) describe higher-current electrochemical
    processes, including water electrolysis;
* megaamperes per square metre (MA/m²) describe high current densities in compact
    conductors and power connections;
* amperes per square centimetre (A/cm²) are common in fuel cells, electrolyzers, and
    high-current electrochemical cells;
* milliamperes per square centimetre (mA/cm²) are used in battery electrode
    characterization and laboratory electrochemical measurements;
* microamperes per square centimetre (µA/cm²) are used in corrosion measurements and
    electrochemical characterization of metal surfaces;
* amperes per square millimetre (A/mm²) express the current density of compact
    conductors, motor windings, and electrical interconnects.

Examples
--------
A decorative chromium-plating process operates at a current density of 1200 A/m².
The plated area is 200 cm².
Calculate the total current:

>>> from kuchka import SquareMetre
>>> plating_density = AmperePerSquareMetre(1200)
>>> plated_area = SquareMetre(0.02)
>>> plating_density * plated_area
24 A

A battery electrode is characterized at a current density of 2 mA/cm².
The same current density expressed in amperes per square metre is:

>>> electrode = MilliamperePerSquareCentimetre(2)
>>> electrode.to(AMPERE_PER_SQUARE_METRE)
20 A/m²

An acquisition system exports an electrode measurement as text.
The parser reads the value and its unit together:

>>> from kuchka import parse
>>> parse("2 mA/cm2", CurrentDensity)
2 mA/cm²

Notes
-----
Electric current density, conventionally denoted by J or j, is a vector quantity.
Its direction describes the local direction of charge transport, and its magnitude
describes the current passing through a unit area perpendicular to that direction.

For a uniform current density perpendicular to a cross-section:

``I = J A``

More generally, the current through an oriented surface is obtained from the surface
integral of the current-density vector:

``I = ∫ J · dA``

`CurrentDensity` represents the magnitude of current density.
It does not encode the direction of current flow or its spatial distribution.

The SI unit is the ampere per square metre:

``1 A/m² = 1 A/m²``

The alternative area scales have the following exact relationships:

``1 A/cm² = 10 kA/m²``

``1 mA/cm² = 10 A/m²``

``1 µA/cm² = 10 mA/m²``

``1 A/mm² = 1 MA/m²``

The area used to calculate current density is part of the measurement definition.
For conductors, it is normally the cross-sectional area perpendicular to current flow.
For electrodes, it is often the geometric or projected electrode area.
Porous electrodes and rough surfaces may have a substantially different active surface
area.

Reported electrode current densities should therefore identify the area basis used in
the calculation.
The average current density over a geometric area does not necessarily describe the
local distribution across the electrode.

Current density is useful when comparing conductors and electrical connections, but it
is not by itself a current-carrying capacity rating.
Conductor temperature also depends on material, geometry, length, insulation, cooling,
and the surrounding thermal environment.

In electrochemistry, current density is an important operating parameter because it
relates the electrical current to the electrode area.
It appears in electrode kinetics, electrolysis, electroplating, corrosion measurements,
and battery characterization.

`parse` reads complete measurements such as ``"1200 A/m2"``, ``"3 kA/m2"``,
``"2 mA/cm2"``, and ``"4 µA/cm2"``.
The supplied quantity type determines which unit table is consulted.

`CURRENT_DENSITY_UNITS` maps supported symbols such as ``"A/m2"``, ``"mA/m2"``,
``"kA/m2"``, ``"MA/m2"``, ``"A/cm2"``, ``"mA/cm2"``, ``"uA/cm2"``, and ``"A/mm2"`` to
their constructors.
It is useful for boundary code that receives a numeric magnitude and a separate unit
symbol from an external source.

References
----------
IUPAC, Compendium of Chemical Terminology:
https://goldbook.iupac.org/terms/view/E01928

IUPAC, Average current density:
https://goldbook.iupac.org/terms/view/A00539

US EPA, AP-42, Section 12.20, Electroplating:
https://www.epa.gov/sites/default/files/2020-11/documents/b12s20.pdf

A Comprehensive Survey of Alkaline Electrolyzer Modeling:
https://doi.org/10.3390/en15093452

ISO 22858:2020, Electrochemical Test Method for Atmospheric Corrosion.

See Also
--------
~kuchka.quantities.CurrentDensity
    Quantity type representing electric current density.

~kuchka.quantities.Current
    Electric current passing through a conductor or electrode.

~kuchka.quantities.Area
    Cross-sectional or electrode area used to calculate current density.

~kuchka.units.current
    Constructors for electric current.

~kuchka.units.geometry.area
    Constructors for areas and cross-sectional dimensions.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import CURRENT_DENSITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import CurrentDensity
from kuchka.quantities import UnitDef
from kuchka.units.current import AMPERE
from kuchka.units.geometry.area import SQUARE_CENTIMETRE
from kuchka.units.geometry.area import SQUARE_MILLIMETRE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

AMPERE_PER_SQUARE_METRE = UnitDef(
    "ampere_per_square_metre",
    "A/m²",
    1,
    CURRENT_DENSITY,
    aliases=powered("A/m", 2),
    words=("amperes per square metre", "amperes per square meter"),
)
MILLIAMPERE_PER_SQUARE_METRE = with_prefix(prefixes.MILLI, AMPERE_PER_SQUARE_METRE)
KILOAMPERE_PER_SQUARE_METRE = with_prefix(prefixes.KILO, AMPERE_PER_SQUARE_METRE)
MEGAAMPERE_PER_SQUARE_METRE = with_prefix(prefixes.MEGA, AMPERE_PER_SQUARE_METRE)
AMPERE_PER_SQUARE_CENTIMETRE = UnitDef(
    "ampere_per_square_centimetre",
    "A/cm²",
    AMPERE.scale / SQUARE_CENTIMETRE.scale,
    CURRENT_DENSITY,
    aliases=powered("A/cm", 2),
    words=("amperes per square centimetre", "amperes per square centimeter"),
)
MILLIAMPERE_PER_SQUARE_CENTIMETRE = with_prefix(
    prefixes.MILLI, AMPERE_PER_SQUARE_CENTIMETRE
)
MICROAMPERE_PER_SQUARE_CENTIMETRE = with_prefix(
    prefixes.MICRO, AMPERE_PER_SQUARE_CENTIMETRE
)
AMPERE_PER_SQUARE_MILLIMETRE = UnitDef(
    "ampere_per_square_millimetre",
    "A/mm²",
    AMPERE.scale / SQUARE_MILLIMETRE.scale,
    CURRENT_DENSITY,
    aliases=powered("A/mm", 2),
    words=("amperes per square millimetre", "amperes per square millimeter"),
)

CurrentDensity._canonical_unit = AMPERE_PER_SQUARE_METRE  # noqa: SLF001 -- this module owns CurrentDensity's canonical unit


def AmperePerSquareMetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from a magnitude in amperes per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in A/m².

    Returns
    -------
    CurrentDensity
        Current density represented in amperes per square metre.

    Examples
    --------
    A decorative chromium-plating process operates at a current density of 1200 A/m²:

    >>> plating = AmperePerSquareMetre(1200)
    >>> plating
    1200 A/m²

    Express the operating point in kiloamperes per square metre:

    >>> plating.to(KILOAMPERE_PER_SQUARE_METRE)
    1.2 kA/m²

    """
    return CurrentDensity(
        to_exact(value) * AMPERE_PER_SQUARE_METRE.scale, AMPERE_PER_SQUARE_METRE
    )


def MilliamperePerSquareMetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from a magnitude in milliamperes per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in mA/m².

    Returns
    -------
    CurrentDensity
        Current density represented in milliamperes per square metre.

    Examples
    --------
    An uncoated steel structure immersed in stationary seawater has a
    cathodic-protection design current density of 25 mA/m²:

    >>> protection_density = MilliamperePerSquareMetre(25)
    >>> protection_density
    25 mA/m²

    An inspection record uses the ASCII unit spelling `mA/m2`:

    >>> from kuchka import CurrentDensity
    >>> from kuchka import parse
    >>> parse("25 mA/m2", CurrentDensity) == protection_density
    True

    """
    return CurrentDensity(
        to_exact(value) * MILLIAMPERE_PER_SQUARE_METRE.scale,
        MILLIAMPERE_PER_SQUARE_METRE,
    )


def KiloamperePerSquareMetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from a magnitude in kiloamperes per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kA/m².

    Returns
    -------
    CurrentDensity
        Current density represented in kiloamperes per square metre.

    Examples
    --------
    An alkaline water electrolyzer operates at a current density of 3 kA/m², equivalent
    to 0.3 A/cm²:

    >>> electrolyzer = KiloamperePerSquareMetre(3)
    >>> electrolyzer
    3 kA/m²

    Express the same operating point in amperes per square centimetre:

    >>> electrolyzer.to(AMPERE_PER_SQUARE_CENTIMETRE)
    0.3 A/cm²

    """
    return CurrentDensity(
        to_exact(value) * KILOAMPERE_PER_SQUARE_METRE.scale, KILOAMPERE_PER_SQUARE_METRE
    )


def MegaamperePerSquareMetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from a magnitude in megaamperes per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in MA/m².

    Returns
    -------
    CurrentDensity
        Current density represented in megaamperes per square metre.

    Examples
    --------
    A copper busbar carries an average current density of 1.5 MA/m²:

    >>> busbar_density = MegaamperePerSquareMetre(1.5)
    >>> busbar_density
    1.5 MA/m²

    One megaampere per square metre is exactly one ampere per square millimetre:

    >>> busbar_density.to(AMPERE_PER_SQUARE_MILLIMETRE)
    1.5 A/mm²

    """
    return CurrentDensity(
        to_exact(value) * MEGAAMPERE_PER_SQUARE_METRE.scale, MEGAAMPERE_PER_SQUARE_METRE
    )


def AmperePerSquareCentimetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from a magnitude in amperes per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in A/cm².

    Returns
    -------
    CurrentDensity
        Current density represented in amperes per square centimetre.

    Examples
    --------
    A PEM water electrolyzer operates at a current density of 0.8 A/cm²:

    >>> cell_density = AmperePerSquareCentimetre(0.8)
    >>> cell_density
    0.8 A/cm²

    For an active electrode area of 50 cm², this corresponds to a total cell current of
    40 A:

    >>> from kuchka import SquareCentimetre
    >>> cell_density * SquareCentimetre(50)
    40 A

    """
    return CurrentDensity(
        to_exact(value) * AMPERE_PER_SQUARE_CENTIMETRE.scale,
        AMPERE_PER_SQUARE_CENTIMETRE,
    )


def MilliamperePerSquareCentimetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from a magnitude in milliamperes per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in mA/cm².

    Returns
    -------
    CurrentDensity
        Current density represented in milliamperes per square centimetre.

    Examples
    --------
    A lithium-ion battery electrode is characterized at an areal current density of
    2 mA/cm² during a galvanostatic cycling test:

    >>> electrode_density = MilliamperePerSquareCentimetre(2)
    >>> electrode_density
    2 mA/cm²

    For a geometric electrode area of 80 cm², the corresponding current is:

    >>> from kuchka import SquareCentimetre
    >>> electrode_density * SquareCentimetre(80)
    0.16 A

    """  # noqa: E501 -- long unit name.
    return CurrentDensity(
        to_exact(value) * MILLIAMPERE_PER_SQUARE_CENTIMETRE.scale,
        MILLIAMPERE_PER_SQUARE_CENTIMETRE,
    )


def MicroamperePerSquareCentimetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from a magnitude in microamperes per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in µA/cm².

    Returns
    -------
    CurrentDensity
        Current density represented in microamperes per square centimetre.

    Examples
    --------
    An electrochemical corrosion test reports a corrosion current density of 4.2 µA/cm²
    for a metal specimen:

    >>> corrosion_density = MicroamperePerSquareCentimetre(4.2)
    >>> corrosion_density
    4.2 µA/cm²

    Express the result in milliamperes per square metre:

    >>> corrosion_density.to(MILLIAMPERE_PER_SQUARE_METRE)
    42 mA/m²

    """  # noqa: E501 -- long unit name.
    return CurrentDensity(
        to_exact(value) * MICROAMPERE_PER_SQUARE_CENTIMETRE.scale,
        MICROAMPERE_PER_SQUARE_CENTIMETRE,
    )


def AmperePerSquareMillimetre(value: Numeric) -> CurrentDensity:
    """Construct a CurrentDensity from a magnitude in amperes per square millimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in A/mm².

    Returns
    -------
    CurrentDensity
        Current density represented in amperes per square millimetre.

    Examples
    --------
    A copper winding conductor in a compact electric motor is evaluated at a current
    density of 4 A/mm²:

    >>> winding = AmperePerSquareMillimetre(4)
    >>> winding
    4 A/mm²

    A conductor with a cross-sectional area of 2.5 mm² carries a current of 10 A at
    this current density:

    >>> from kuchka import SquareMillimetre
    >>> winding * SquareMillimetre(2.5)
    10 A

    """
    return CurrentDensity(
        to_exact(value) * AMPERE_PER_SQUARE_MILLIMETRE.scale,
        AMPERE_PER_SQUARE_MILLIMETRE,
    )


CURRENT_DENSITY_UNITS: Mapping[str, Callable[[Numeric], CurrentDensity]] = unit_table(
    "CURRENT_DENSITY_UNITS",
    {
        AMPERE_PER_SQUARE_METRE: AmperePerSquareMetre,
        MILLIAMPERE_PER_SQUARE_METRE: MilliamperePerSquareMetre,
        KILOAMPERE_PER_SQUARE_METRE: KiloamperePerSquareMetre,
        MEGAAMPERE_PER_SQUARE_METRE: MegaamperePerSquareMetre,
        AMPERE_PER_SQUARE_CENTIMETRE: AmperePerSquareCentimetre,
        MILLIAMPERE_PER_SQUARE_CENTIMETRE: MilliamperePerSquareCentimetre,
        MICROAMPERE_PER_SQUARE_CENTIMETRE: MicroamperePerSquareCentimetre,
        AMPERE_PER_SQUARE_MILLIMETRE: AmperePerSquareMillimetre,
    },
)

CURRENT_DENSITY_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        MILLIAMPERE_PER_SQUARE_METRE,
        AMPERE_PER_SQUARE_METRE,
        KILOAMPERE_PER_SQUARE_METRE,
        MEGAAMPERE_PER_SQUARE_METRE,
    ),
    (
        MICROAMPERE_PER_SQUARE_CENTIMETRE,
        MILLIAMPERE_PER_SQUARE_CENTIMETRE,
        AMPERE_PER_SQUARE_CENTIMETRE,
    ),
)
"""The runs of units `auto_scale` moves a current density along.

There is one run for each family of prefixed units, smallest first.
"""

__all__ = [
    "AMPERE_PER_SQUARE_CENTIMETRE",
    "AMPERE_PER_SQUARE_METRE",
    "AMPERE_PER_SQUARE_MILLIMETRE",
    "CURRENT_DENSITY_LADDERS",
    "CURRENT_DENSITY_UNITS",
    "KILOAMPERE_PER_SQUARE_METRE",
    "MEGAAMPERE_PER_SQUARE_METRE",
    "MICROAMPERE_PER_SQUARE_CENTIMETRE",
    "MILLIAMPERE_PER_SQUARE_CENTIMETRE",
    "MILLIAMPERE_PER_SQUARE_METRE",
    "AmperePerSquareCentimetre",
    "AmperePerSquareMetre",
    "AmperePerSquareMillimetre",
    "KiloamperePerSquareMetre",
    "MegaamperePerSquareMetre",
    "MicroamperePerSquareCentimetre",
    "MilliamperePerSquareCentimetre",
    "MilliamperePerSquareMetre",
]
