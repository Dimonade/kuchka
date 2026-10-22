"""Unit constructors for Activity: the becquerel and the curie.

    from kuchka import Megabecquerel, Millicurie

    source = Megabecquerel(37)
    calibration = Millicurie(1)

`Activity` counts decays per second, and its canonical unit is the becquerel (`Bq`),
one decay per second.
The curie (`Ci`) is the older unit, defined as exactly 37 000 000 000 becquerel, and
it is still what a radon reading or a calibration source is labelled in.
The becquerel runs from the milli- to the tera- multiple, and the curie has the milli-,
micro-, and pico- multiples.

Examples
--------
A 1 mCi calibration source is exactly 37 MBq:

>>> Millicurie(1) == Megabecquerel(37)
True

A radon reading of 4 pCi per litre is 0.148 Bq per litre:

>>> Picocurie(4).to(BECQUEREL)
0.148 Bq

Notes
-----
`Activity` has no hertz.
A decay rate that is read as an ordinary rate goes through `Activity.to_frequency()`.

`ACTIVITY_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import FREQUENCY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import Activity
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

BECQUEREL = UnitDef("becquerel", "Bq", 1, FREQUENCY)
CURIE = UnitDef("curie", "Ci", 37_000_000_000, FREQUENCY)
MILLIBECQUEREL = with_prefix(prefixes.MILLI, BECQUEREL)
KILOBECQUEREL = with_prefix(prefixes.KILO, BECQUEREL)
MEGABECQUEREL = with_prefix(prefixes.MEGA, BECQUEREL)
GIGABECQUEREL = with_prefix(prefixes.GIGA, BECQUEREL)
TERABECQUEREL = with_prefix(prefixes.TERA, BECQUEREL)
MILLICURIE = with_prefix(prefixes.MILLI, CURIE)
MICROCURIE = with_prefix(prefixes.MICRO, CURIE)
PICOCURIE = with_prefix(prefixes.PICO, CURIE)

Activity._canonical_unit = BECQUEREL  # noqa: SLF001 -- this module owns Activity's canonical unit


def Becquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in becquerels.

    Parameters
    ----------
    value : Numeric
        Activity in becquerels.

    Returns
    -------
    Activity
        Activity represented in becquerels.

    Examples
    --------
    >>> Becquerel(1).to(BECQUEREL)
    1 Bq

    """
    return Activity(to_exact(value) * BECQUEREL.scale, BECQUEREL)


def Millibecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in millibecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in millibecquerels.

    Returns
    -------
    Activity
        Activity represented in millibecquerels.

    Examples
    --------
    >>> Millibecquerel(1).to(BECQUEREL)
    0.001 Bq

    """
    return Activity(to_exact(value) * MILLIBECQUEREL.scale, MILLIBECQUEREL)


def Kilobecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in kilobecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in kilobecquerels.

    Returns
    -------
    Activity
        Activity represented in kilobecquerels.

    Examples
    --------
    >>> Kilobecquerel(1).to(BECQUEREL)
    1000 Bq

    """
    return Activity(to_exact(value) * KILOBECQUEREL.scale, KILOBECQUEREL)


def Megabecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in megabecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in megabecquerels.

    Returns
    -------
    Activity
        Activity represented in megabecquerels.

    Examples
    --------
    >>> Megabecquerel(1).to(BECQUEREL)
    1000000 Bq

    """
    return Activity(to_exact(value) * MEGABECQUEREL.scale, MEGABECQUEREL)


def Gigabecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in gigabecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in gigabecquerels.

    Returns
    -------
    Activity
        Activity represented in gigabecquerels.

    Examples
    --------
    >>> Gigabecquerel(1).to(BECQUEREL)
    1000000000 Bq

    """
    return Activity(to_exact(value) * GIGABECQUEREL.scale, GIGABECQUEREL)


def Terabecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in terabecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in terabecquerels.

    Returns
    -------
    Activity
        Activity represented in terabecquerels.

    Examples
    --------
    >>> Terabecquerel(1).to(BECQUEREL)
    1000000000000 Bq

    """
    return Activity(to_exact(value) * TERABECQUEREL.scale, TERABECQUEREL)


def Curie(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in curies.

    Parameters
    ----------
    value : Numeric
        Activity in curies.

    Returns
    -------
    Activity
        Activity represented in curies.

    Examples
    --------
    >>> Curie(1).to(BECQUEREL)
    37000000000 Bq

    """
    return Activity(to_exact(value) * CURIE.scale, CURIE)


def Millicurie(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in millicuries.

    Parameters
    ----------
    value : Numeric
        Activity in millicuries.

    Returns
    -------
    Activity
        Activity represented in millicuries.

    Examples
    --------
    >>> Millicurie(1).to(BECQUEREL)
    37000000 Bq

    """
    return Activity(to_exact(value) * MILLICURIE.scale, MILLICURIE)


def Microcurie(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in microcuries.

    Parameters
    ----------
    value : Numeric
        Activity in microcuries.

    Returns
    -------
    Activity
        Activity represented in microcuries.

    Examples
    --------
    >>> Microcurie(1).to(BECQUEREL)
    37000 Bq

    """
    return Activity(to_exact(value) * MICROCURIE.scale, MICROCURIE)


def Picocurie(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in picocuries.

    Parameters
    ----------
    value : Numeric
        Activity in picocuries.

    Returns
    -------
    Activity
        Activity represented in picocuries.

    Examples
    --------
    >>> Picocurie(1).to(BECQUEREL)
    0.037 Bq

    """
    return Activity(to_exact(value) * PICOCURIE.scale, PICOCURIE)


ACTIVITY_UNITS: Mapping[str, Callable[[Numeric], Activity]] = unit_table(
    "ACTIVITY_UNITS",
    {
        BECQUEREL: Becquerel,
        MILLIBECQUEREL: Millibecquerel,
        KILOBECQUEREL: Kilobecquerel,
        MEGABECQUEREL: Megabecquerel,
        GIGABECQUEREL: Gigabecquerel,
        TERABECQUEREL: Terabecquerel,
        CURIE: Curie,
        MILLICURIE: Millicurie,
        MICROCURIE: Microcurie,
        PICOCURIE: Picocurie,
    },
)

__all__ = [
    "ACTIVITY_UNITS",
    "BECQUEREL",
    "CURIE",
    "GIGABECQUEREL",
    "KILOBECQUEREL",
    "MEGABECQUEREL",
    "MICROCURIE",
    "MILLIBECQUEREL",
    "MILLICURIE",
    "PICOCURIE",
    "TERABECQUEREL",
    "Becquerel",
    "Curie",
    "Gigabecquerel",
    "Kilobecquerel",
    "Megabecquerel",
    "Microcurie",
    "Millibecquerel",
    "Millicurie",
    "Picocurie",
    "Terabecquerel",
]
