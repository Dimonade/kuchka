"""Unit constructors for activity concentration: becquerels and curies per volume.

    from kuchka import BecquerelPerCubicMetre, PicocuriePerLitre

    radon = PicocuriePerLitre(4)
    air = BecquerelPerCubicMetre(100)

`ActivityConcentration` is the activity in each unit of volume, `Activity / Volume`.
Its canonical unit is the becquerel per cubic metre (`Bq/m³`).
The module provides it with the kilo- and milli- multiples, the becquerel per litre
that water assays use, and the picocurie per litre that radon is quoted in: one
picocurie per litre is exactly 37 Bq/m³.

Examples
--------
A radon level of 4 pCi/L, in the SI unit:

>>> PicocuriePerLitre(4).to(BECQUEREL_PER_CUBIC_METRE)
148 Bq/m³

An activity concentration times a volume is an activity:

>>> from kuchka import CubicMetre
>>> from kuchka.units.radiation.activity import KILOBECQUEREL
>>> (BecquerelPerCubicMetre(150) * CubicMetre(60)).to(KILOBECQUEREL)
9 kBq

`ACTIVITY_CONCENTRATION_UNITS` maps symbols such as ``"Bq/m3"``, ``"Bq/L"``, and
``"pCi/L"`` to their constructors for boundary code that reads unit labels from
external data.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import ACTIVITY_CONCENTRATION
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import ActivityConcentration
from kuchka.quantities import UnitDef
from kuchka.units.geometry.volume import LITRE
from kuchka.units.radiation.activity import BECQUEREL
from kuchka.units.radiation.activity import PICOCURIE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

BECQUEREL_PER_CUBIC_METRE = UnitDef(
    "becquerel_per_cubic_metre",
    "Bq/m³",
    1,
    ACTIVITY_CONCENTRATION,
    aliases=("Bq/m3", "Bq/m^3"),
    words=("becquerels per cubic metre", "becquerels per cubic meter"),
)
KILOBECQUEREL_PER_CUBIC_METRE = UnitDef(
    "kilobecquerel_per_cubic_metre",
    "kBq/m³",
    1000,
    ACTIVITY_CONCENTRATION,
    aliases=("kBq/m3", "kBq/m^3"),
    words=("kilobecquerels per cubic metre", "kilobecquerels per cubic meter"),
)
MILLIBECQUEREL_PER_CUBIC_METRE = UnitDef(
    "millibecquerel_per_cubic_metre",
    "mBq/m³",
    Fraction(1, 1000),
    ACTIVITY_CONCENTRATION,
    aliases=("mBq/m3", "mBq/m^3"),
    words=("millibecquerels per cubic metre", "millibecquerels per cubic meter"),
)
BECQUEREL_PER_LITRE = UnitDef(
    "becquerel_per_litre",
    "Bq/L",
    BECQUEREL.scale / LITRE.scale,
    ACTIVITY_CONCENTRATION,
    aliases=("Bq/l",),
    words=("becquerels per litre", "becquerels per liter"),
)
PICOCURIE_PER_LITRE = UnitDef(
    "picocurie_per_litre",
    "pCi/L",
    PICOCURIE.scale / LITRE.scale,
    ACTIVITY_CONCENTRATION,
    aliases=("pCi/l",),
    words=("picocuries per litre", "picocuries per liter"),
)

ActivityConcentration._canonical_unit = BECQUEREL_PER_CUBIC_METRE  # noqa: SLF001 -- this module owns ActivityConcentration's canonical unit


def BecquerelPerCubicMetre(value: Numeric) -> ActivityConcentration:
    """Construct an ActivityConcentration in becquerels per cubic metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in becquerels per cubic metre.

    Returns
    -------
    ActivityConcentration
        ActivityConcentration represented in becquerels per cubic metre.

    """
    return ActivityConcentration(
        to_exact(value) * BECQUEREL_PER_CUBIC_METRE.scale, BECQUEREL_PER_CUBIC_METRE
    )


def KilobecquerelPerCubicMetre(value: Numeric) -> ActivityConcentration:
    """Construct an ActivityConcentration in kilobecquerels per cubic metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilobecquerels per cubic metre.

    Returns
    -------
    ActivityConcentration
        ActivityConcentration represented in kilobecquerels per cubic metre.

    """
    return ActivityConcentration(
        to_exact(value) * KILOBECQUEREL_PER_CUBIC_METRE.scale,
        KILOBECQUEREL_PER_CUBIC_METRE,
    )


def MillibecquerelPerCubicMetre(value: Numeric) -> ActivityConcentration:
    """Construct an ActivityConcentration in millibecquerels per cubic metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in millibecquerels per cubic metre.

    Returns
    -------
    ActivityConcentration
        ActivityConcentration represented in millibecquerels per cubic metre.

    """
    return ActivityConcentration(
        to_exact(value) * MILLIBECQUEREL_PER_CUBIC_METRE.scale,
        MILLIBECQUEREL_PER_CUBIC_METRE,
    )


def BecquerelPerLitre(value: Numeric) -> ActivityConcentration:
    """Construct an ActivityConcentration from a magnitude in becquerels per litre.

    Parameters
    ----------
    value : Numeric
        Magnitude in becquerels per litre.

    Returns
    -------
    ActivityConcentration
        ActivityConcentration represented in becquerels per litre.

    """
    return ActivityConcentration(
        to_exact(value) * BECQUEREL_PER_LITRE.scale, BECQUEREL_PER_LITRE
    )


def PicocuriePerLitre(value: Numeric) -> ActivityConcentration:
    """Construct an ActivityConcentration from a magnitude in picocuries per litre.

    Parameters
    ----------
    value : Numeric
        Magnitude in picocuries per litre.

    Returns
    -------
    ActivityConcentration
        ActivityConcentration represented in picocuries per litre.

    """
    return ActivityConcentration(
        to_exact(value) * PICOCURIE_PER_LITRE.scale, PICOCURIE_PER_LITRE
    )


ACTIVITY_CONCENTRATION_UNITS: Mapping[
    str, Callable[[Numeric], ActivityConcentration]
] = unit_table(
    "ACTIVITY_CONCENTRATION_UNITS",
    {
        BECQUEREL_PER_CUBIC_METRE: BecquerelPerCubicMetre,
        KILOBECQUEREL_PER_CUBIC_METRE: KilobecquerelPerCubicMetre,
        MILLIBECQUEREL_PER_CUBIC_METRE: MillibecquerelPerCubicMetre,
        BECQUEREL_PER_LITRE: BecquerelPerLitre,
        PICOCURIE_PER_LITRE: PicocuriePerLitre,
    },
)

__all__ = [
    "ACTIVITY_CONCENTRATION_UNITS",
    "BECQUEREL_PER_CUBIC_METRE",
    "BECQUEREL_PER_LITRE",
    "KILOBECQUEREL_PER_CUBIC_METRE",
    "MILLIBECQUEREL_PER_CUBIC_METRE",
    "PICOCURIE_PER_LITRE",
    "BecquerelPerCubicMetre",
    "BecquerelPerLitre",
    "KilobecquerelPerCubicMetre",
    "MillibecquerelPerCubicMetre",
    "PicocuriePerLitre",
]
