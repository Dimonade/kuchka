"""Specific activity constructors: becquerels and curies per mass.

    from kuchka import BecquerelPerKilogram
    from kuchka import PicocuriePerGram

    soil = BecquerelPerKilogram(400)
    sample = PicocuriePerGram(15)

`SpecificActivity` is the activity in each unit of mass, `Activity / Mass`.
Its canonical unit is the becquerel per kilogram (`Bq/kg`).
The module provides it with the kilobecquerel per kilogram, the becquerel per gram,
and the curie per gram from picocuries to curies: one picocurie per gram is exactly
37 Bq/kg.

Examples
--------
A soil sample at 15 pCi/g, in the SI unit:

>>> PicocuriePerGram(15).to(BECQUEREL_PER_KILOGRAM)
555 Bq/kg

An activity over a mass is a specific activity:

>>> from kuchka import Kilogram
>>> from kuchka.units import Becquerel
>>> Becquerel(200) / Kilogram(0.5)
400 Bq/kg

`SPECIFIC_ACTIVITY_UNITS` maps symbols such as ``"Bq/kg"``, ``"Bq/g"``, and
``"pCi/g"`` to their constructors for boundary code that reads unit labels from
external data.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_ACTIVITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import SpecificActivity
from kuchka.quantities import UnitDef
from kuchka.units.mass import GRAM
from kuchka.units.radiation.activity import BECQUEREL
from kuchka.units.radiation.activity import CURIE
from kuchka.units.radiation.activity import PICOCURIE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

BECQUEREL_PER_KILOGRAM = UnitDef(
    "becquerel_per_kilogram",
    "Bq/kg",
    1,
    SPECIFIC_ACTIVITY,
    words=("becquerels per kilogram",),
)
KILOBECQUEREL_PER_KILOGRAM = UnitDef(
    "kilobecquerel_per_kilogram",
    "kBq/kg",
    1000,
    SPECIFIC_ACTIVITY,
    words=("kilobecquerels per kilogram",),
)
BECQUEREL_PER_GRAM = UnitDef(
    "becquerel_per_gram",
    "Bq/g",
    BECQUEREL.scale / GRAM.scale,
    SPECIFIC_ACTIVITY,
    words=("becquerels per gram",),
)
PICOCURIE_PER_GRAM = UnitDef(
    "picocurie_per_gram",
    "pCi/g",
    PICOCURIE.scale / GRAM.scale,
    SPECIFIC_ACTIVITY,
    words=("picocuries per gram",),
)
CURIE_PER_GRAM = UnitDef(
    "curie_per_gram",
    "Ci/g",
    CURIE.scale / GRAM.scale,
    SPECIFIC_ACTIVITY,
    words=("curies per gram",),
)
MILLICURIE_PER_GRAM = with_prefix(prefixes.MILLI, CURIE_PER_GRAM)
MICROCURIE_PER_GRAM = with_prefix(prefixes.MICRO, CURIE_PER_GRAM)
NANOCURIE_PER_GRAM = with_prefix(prefixes.NANO, CURIE_PER_GRAM)

SpecificActivity._canonical_unit = BECQUEREL_PER_KILOGRAM  # noqa: SLF001 -- this module owns SpecificActivity's canonical unit


def BecquerelPerKilogram(value: Numeric) -> SpecificActivity:
    """Construct a SpecificActivity from a magnitude in becquerels per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in becquerels per kilogram.

    Returns
    -------
    SpecificActivity
        SpecificActivity represented in becquerels per kilogram.

    """
    return SpecificActivity(
        to_exact(value) * BECQUEREL_PER_KILOGRAM.scale, BECQUEREL_PER_KILOGRAM
    )


def KilobecquerelPerKilogram(value: Numeric) -> SpecificActivity:
    """Construct a SpecificActivity from a magnitude in kilobecquerels per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilobecquerels per kilogram.

    Returns
    -------
    SpecificActivity
        SpecificActivity represented in kilobecquerels per kilogram.

    """
    return SpecificActivity(
        to_exact(value) * KILOBECQUEREL_PER_KILOGRAM.scale, KILOBECQUEREL_PER_KILOGRAM
    )


def BecquerelPerGram(value: Numeric) -> SpecificActivity:
    """Construct a SpecificActivity from a magnitude in becquerels per gram.

    Parameters
    ----------
    value : Numeric
        Magnitude in becquerels per gram.

    Returns
    -------
    SpecificActivity
        SpecificActivity represented in becquerels per gram.

    """
    return SpecificActivity(
        to_exact(value) * BECQUEREL_PER_GRAM.scale, BECQUEREL_PER_GRAM
    )


def PicocuriePerGram(value: Numeric) -> SpecificActivity:
    """Construct a SpecificActivity from a magnitude in picocuries per gram.

    Parameters
    ----------
    value : Numeric
        Magnitude in picocuries per gram.

    Returns
    -------
    SpecificActivity
        SpecificActivity represented in picocuries per gram.

    """
    return SpecificActivity(
        to_exact(value) * PICOCURIE_PER_GRAM.scale, PICOCURIE_PER_GRAM
    )


def CuriePerGram(value: Numeric) -> SpecificActivity:
    """Construct a SpecificActivity from a magnitude in curies per gram.

    Parameters
    ----------
    value : Numeric
        Magnitude in curies per gram.

    Returns
    -------
    SpecificActivity
        SpecificActivity represented in curies per gram.

    """
    return SpecificActivity(to_exact(value) * CURIE_PER_GRAM.scale, CURIE_PER_GRAM)


def MillicuriePerGram(value: Numeric) -> SpecificActivity:
    """Construct a SpecificActivity from a magnitude in millicuries per gram.

    Parameters
    ----------
    value : Numeric
        Magnitude in millicuries per gram.

    Returns
    -------
    SpecificActivity
        SpecificActivity represented in millicuries per gram.

    Examples
    --------
    The curie began as the activity of a gram of radium-226, and a gram of it is a
    little under a curie, about 989 mCi/g:

    >>> radium_226 = MillicuriePerGram(989)
    >>> radium_226
    989 mCi/g

    Radium therapy was dosed in milligram-hours, because a milligram of radium-226 is
    almost exactly a millicurie.
    A 10 mg radium needle of that specific activity holds, from radium-226 alone:

    >>> from kuchka import Milligram
    >>> from kuchka.units import MILLICURIE
    >>> (radium_226 * Milligram(10)).to(MILLICURIE)
    9.89 mCi

    """
    return SpecificActivity(
        to_exact(value) * MILLICURIE_PER_GRAM.scale, MILLICURIE_PER_GRAM
    )


def MicrocuriePerGram(value: Numeric) -> SpecificActivity:
    """Construct a SpecificActivity from a magnitude in microcuries per gram.

    Parameters
    ----------
    value : Numeric
        Magnitude in microcuries per gram.

    Returns
    -------
    SpecificActivity
        SpecificActivity represented in microcuries per gram.

    Examples
    --------
    Pure uranium-238 has a specific activity of about 12.4 kBq/g, which is 0.336 µCi/g:

    >>> uranium_238 = MicrocuriePerGram(0.336)
    >>> uranium_238.to(BECQUEREL_PER_GRAM)
    12432 Bq/g

    A 100 g piece of purified uranium metal then carries, from uranium-238 alone:

    >>> from kuchka import Gram
    >>> from kuchka.units import MICROCURIE
    >>> (uranium_238 * Gram(100)).to(MICROCURIE)
    33.6 µCi

    """
    return SpecificActivity(
        to_exact(value) * MICROCURIE_PER_GRAM.scale, MICROCURIE_PER_GRAM
    )


def NanocuriePerGram(value: Numeric) -> SpecificActivity:
    """Construct a SpecificActivity from a magnitude in nanocuries per gram.

    Parameters
    ----------
    value : Numeric
        Magnitude in nanocuries per gram.

    Returns
    -------
    SpecificActivity
        SpecificActivity represented in nanocuries per gram.

    Examples
    --------
    Natural potassium carries about 31 Bq of potassium-40 per gram, which is about
    0.84 nCi/g:

    >>> potassium = NanocuriePerGram(0.84)
    >>> potassium.to(BECQUEREL_PER_GRAM)
    31.08 Bq/g

    A reference adult holds about 140 g of potassium, which gives the roughly 4 kBq of
    potassium-40 in the body:

    >>> from kuchka import Gram
    >>> from kuchka.units import KILOBECQUEREL
    >>> f"{(potassium * Gram(140)).to(KILOBECQUEREL):.0f}"
    '4 kBq'

    """
    return SpecificActivity(
        to_exact(value) * NANOCURIE_PER_GRAM.scale, NANOCURIE_PER_GRAM
    )


SPECIFIC_ACTIVITY_UNITS: Mapping[str, Callable[[Numeric], SpecificActivity]] = (
    unit_table(
        "SPECIFIC_ACTIVITY_UNITS",
        {
            BECQUEREL_PER_KILOGRAM: BecquerelPerKilogram,
            KILOBECQUEREL_PER_KILOGRAM: KilobecquerelPerKilogram,
            BECQUEREL_PER_GRAM: BecquerelPerGram,
            NANOCURIE_PER_GRAM: NanocuriePerGram,
            PICOCURIE_PER_GRAM: PicocuriePerGram,
            MICROCURIE_PER_GRAM: MicrocuriePerGram,
            MILLICURIE_PER_GRAM: MillicuriePerGram,
            CURIE_PER_GRAM: CuriePerGram,
        },
    )
)

__all__ = [
    "BECQUEREL_PER_GRAM",
    "BECQUEREL_PER_KILOGRAM",
    "CURIE_PER_GRAM",
    "KILOBECQUEREL_PER_KILOGRAM",
    "MICROCURIE_PER_GRAM",
    "MILLICURIE_PER_GRAM",
    "NANOCURIE_PER_GRAM",
    "PICOCURIE_PER_GRAM",
    "SPECIFIC_ACTIVITY_UNITS",
    "BecquerelPerGram",
    "BecquerelPerKilogram",
    "CuriePerGram",
    "KilobecquerelPerKilogram",
    "MicrocuriePerGram",
    "MillicuriePerGram",
    "NanocuriePerGram",
    "PicocuriePerGram",
]
