"""Mass quantities and constructors for SI, biological, engineering, and astronomical units.

`Mass` represents the amount of matter in an object.
The kilogram is the canonical SI base unit for mass, so every constructor in this
module scales relative to the kilogram, even though the family is named after the gram.

This makes `Mass` unusual among the SI base quantities:
its canonical unit already contains an SI prefix.
The internal representation still follows the same exact `Decimal` conversion model as
every other quantity in `kuchka`.

Alongside SI prefixes, the module includes several exact non-SI units commonly used in
science and engineering:

* `Dalton` for atoms, proteins, and molecular biology;
* `Grain` for precision mechanical and ballistic measurements;
* `Pound` for imperial engineering and logistics;
* `SolarMass` for stellar and galactic scales.

`Tonne` is a true alias of `Megagram`.
Both names construct the same quantity and share the same underlying unit definition.

Examples
--------
The same physical quantity spans microscopic biology and astronomy.

A human red blood cell has a mass of roughly 27 picograms:

>>> red_blood_cell = Picogram(27)

An average fruit fly weighs about 1 milligram:

>>> fruit_fly = Milligram(1)

A small laboratory mouse weighs about 25 grams:

>>> mouse = Gram(25)

A 2 kg engineering payload can combine kilogram and gram measurements without manual
conversion:

>>> payload = Kilogram(2) + Gram(350)

Shipping and structural engineering naturally use tonnes:

>>> steel_beam = Tonne(2.4)

At astronomical scales, stars are measured in solar masses:

>>> sun = SolarMass(1)
>>> alpha_centauri_a = SolarMass(1.1)

Notes
-----
`MASS_UNITS` maps symbols such as ``"mg"``, ``"kg"``, ``"lb"``, and ``"Da"``
to their constructors for configuration files and other external interfaces.

`Tonne` and `Megagram` are interchangeable names for the same unit.
Both display using the SI symbol ``Mg`` to preserve a single coherent unit
definition.

See Also
--------
~kuchka.quantities.Force
    Force combines mass with acceleration.
~kuchka.quantities.Density
    Density expresses mass per unit volume.

"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import MASS
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Mass
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

GRAM_NAME = "gram"
GRAM_SYMBOL = "g"


PICOGRAM = prefixed_unit(
    prefixes.PICO,
    GRAM_NAME,
    GRAM_SYMBOL,
    MASS,
    coherent_offset=-3,
)
NANOGRAM = prefixed_unit(
    prefixes.NANO,
    GRAM_NAME,
    GRAM_SYMBOL,
    MASS,
    coherent_offset=-3,
)
MICROGRAM = prefixed_unit(
    prefixes.MICRO,
    GRAM_NAME,
    GRAM_SYMBOL,
    MASS,
    coherent_offset=-3,
)
MILLIGRAM = prefixed_unit(
    prefixes.MILLI,
    GRAM_NAME,
    GRAM_SYMBOL,
    MASS,
    coherent_offset=-3,
)
GRAM = prefixed_unit(
    prefixes.UNIT,
    GRAM_NAME,
    GRAM_SYMBOL,
    MASS,
    coherent_offset=-3,
)
KILOGRAM = prefixed_unit(
    prefixes.KILO,
    GRAM_NAME,
    GRAM_SYMBOL,
    MASS,
    coherent_offset=-3,
)
MEGAGRAM = prefixed_unit(
    prefixes.MEGA,
    GRAM_NAME,
    GRAM_SYMBOL,
    MASS,
    coherent_offset=-3,
)

Mass._canonical_unit = KILOGRAM  # noqa: SLF001 -- this module owns Mass's canonical unit


def Picogram(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in picograms.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in picograms.

    Returns
    -------
    Mass
        Mass represented in picograms.

    Examples
    --------
    A human red blood cell has a mass of roughly 27 pg:

    >>> red_blood_cell = Picogram(27)

    """
    return Mass(to_exact(value) * PICOGRAM.scale, PICOGRAM)


def Nanogram(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in nanograms.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in nanograms.

    Returns
    -------
    Mass
        Mass represented in nanograms.

    Examples
    --------
    Environmental laboratories often measure airborne particles in nanograms:

    >>> airborne_sample = Nanogram(85)

    """
    return Mass(to_exact(value) * NANOGRAM.scale, NANOGRAM)


def Microgram(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in micrograms.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in micrograms.

    Returns
    -------
    Mass
        Mass represented in micrograms.

    Examples
    --------
    Vitamin B12 supplements are commonly measured in hundreds of micrograms:

    >>> b12 = Microgram(500)

    """
    return Mass(to_exact(value) * MICROGRAM.scale, MICROGRAM)


def Milligram(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in milligrams.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in milligrams.

    Returns
    -------
    Mass
        Mass represented in milligrams.

    Examples
    --------
    An average fruit fly weighs about one milligram:

    >>> fruit_fly = Milligram(1)

    Roughly 120 thousand fruit flies weigh about the same as a small dog:

    >>> swarm = Milligram(60000)
    >>> dog = Kilogram(30)
    >>> flies_dog_equivalent = swarm / dog
    >>> flies_dog_equivalent
    120_000

    """
    return Mass(to_exact(value) * MILLIGRAM.scale, MILLIGRAM)


def Gram(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in grams.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in grams.

    Returns
    -------
    Mass
        Mass represented in grams.

    Examples
    --------
    A laboratory balance commonly measures samples on the gram scale:

    >>> mineral_sample = Gram(42)

    """
    return Mass(to_exact(value) * GRAM.scale, GRAM)


def Kilogram(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in kilograms.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in kilograms.

    Returns
    -------
    Mass
        Mass represented in kilograms.

    Examples
    --------
    A full bowling ball weighs up to about 7.26 kg:

    >>> bowling_ball = Kilogram(7.26)

    """
    return Mass(to_exact(value) * KILOGRAM.scale, KILOGRAM)


def Megagram(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in megagrams.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in megagrams.

    Returns
    -------
    Mass
        Mass represented in megagrams.

    Examples
    --------
    A loaded concrete mixer can easily carry several megagrams of material:

    >>> concrete_load = Megagram(18)

    A `Megagram` is aliased to the omnipresent `Tonne`:
    >>> car_megagram = Megagram(1.3)
    >>> car_tonne = Tonne(1.3)
    >>> car_tonne == car_megagram
    True

    """
    return Mass(to_exact(value) * MEGAGRAM.scale, MEGAGRAM)


Tonne = Megagram
"""A tonne is a megagram.

`Tonne` is the everyday engineering name for the SI unit `Megagram`.
The two constructors are the same function object.

Examples
--------
A steel shipping container with cargo may weigh 24 tonnes.
The equivalent SI name produces the same value:

>>> container = Tonne(24)
>>> container_si = Megagram(24)
>>> container == container_si
True
"""


# Non-SI units.

DALTON = UnitDef("dalton", "Da", Decimal("1.66053906892e-27"), MASS)


def Dalton(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in daltons.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in daltons.

    Returns
    -------
    Mass
        Mass represented in daltons.

    Notes
    -----
    The dalton is widely used for atoms, proteins, and molecular biology.

    Examples
    --------
    A water molecule has a molecular mass of about 18 Da:

    >>> water = Dalton(18)

    A hemoglobin molecule is roughly 64.5 kDa:

    >>> hemoglobin = Dalton(64500)

    """
    return Mass(to_exact(value) * DALTON.scale, DALTON)


GRAIN = UnitDef("grain", "gr", Milligram(64.79891).to(KILOGRAM), MASS)

def Grain(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in grains.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in grains.

    Returns
    -------
    Mass
        Mass represented in grains.

    Notes
    -----
    One grain is exactly 64.79891 milligrams.

    Examples
    --------
    Bullet masses are traditionally specified in grains:

    >>> bullet = Grain(147)
    """
    return Mass(to_exact(value) * GRAIN.scale, GRAIN)

POUND = UnitDef("pound", "lb", 0.45359237, MASS)

def Pound(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in pounds.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in pounds.

    Returns
    -------
    Mass
        Mass represented in pounds.

    Notes
    -----
    One international avoirdupois pound is exactly 0.45359237 kilograms.

    Examples
    --------
    Airline baggage limits are often expressed in pounds:

    >>> suitcase = Pound(50)
    >>> baggage_limit = Kilogram(25)
    >>> should_fit = baggage_limit > suitcase
    >>> should_fit
    True
    """
    return Mass(to_exact(value) * POUND.scale, POUND)


MASS_UNITS: Mapping[str, Callable[[Numeric], Mass]] = MappingProxyType(
    {
        PICOGRAM.symbol: Picogram,
        NANOGRAM.symbol: Nanogram,
        MICROGRAM.symbol: Microgram,
        MILLIGRAM.symbol: Milligram,
        GRAM.symbol: Gram,
        KILOGRAM.symbol: Kilogram,
        MEGAGRAM.symbol: Megagram,
        "t": Tonne,
    }
)

__all__ = [
    "GRAM",
    "KILOGRAM",
    "MASS_UNITS",
    "MEGAGRAM",
    "MICROGRAM",
    "MILLIGRAM",
    "NANOGRAM",
    "PICOGRAM",
    "Gram",
    "Kilogram",
    "Megagram",
    "Microgram",
    "Milligram",
    "Nanogram",
    "Picogram",
    "Tonne",
]
