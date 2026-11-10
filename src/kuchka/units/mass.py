"""Mass constructors: from picograms to solar masses.

`Mass` represents the amount of matter in an object.
The kilogram is the canonical SI base unit for mass, so every constructor in this
module scales relative to the kilogram, even though the family is named after the gram.

Alongside SI prefixes, the module provides several non-SI units useful in science and
engineering:

* `Dalton` for atoms, molecules, and molecular biology;
* `Grain` for small (and perhaps, obscure) precision masses;
* `Pound` and `Ounce` for imperial engineering and logistics;
* `SolarMass` and `EarthMass` for planetary, stellar, and galactic scales.

`Tonne` is a true alias of `Megagram`.
Both names construct the same quantity and share the same underlying unit definition.

Examples
--------
Mass spans an absurd range of scales without changing what the quantity is.

A human red blood cell has a mass of roughly 27 picograms:

>>> red_blood_cell = Picogram(27)

A fruit fly is about a milligram.
You would need roughly six billion of them to reach the mass of a six-tonne elephant:

>>> fruit_fly = Milligram(1)
>>> elephant = Tonne(6)
>>> elephant_to_fly_equivalent = round((elephant / fruit_fly).magnitude)
>>> elephant_to_fly_equivalent
6000000000

At molecular scales, daltons are much more useful than kilograms.
Water has a molecular mass of about 18 Da, while a hemoglobin molecule is roughly
64.5 kDa:

>>> water = Dalton(18)
>>> hemoglobin = Dalton(64_500)

On the engineering scale, the same arithmetic works without converting everything to
kilograms first:

>>> payload = Kilogram(2) + Gram(350)
>>> payload
2.35 kg

A car is naturally described in tonnes or kilograms:

>>> small_car = Tonne(1)

Now jump to astronomy.
Sagittarius A*, the supermassive black hole at the centre of the Milky Way, has a mass
of about 4.3 million Suns.
Even if a Toyota Yaris is represented by a deliberately round one-tonne mass, replacing
that black hole with cars would require an utterly unreasonable fleet:

>>> yaris = Kilogram(1_000)
>>> sagittarius_a = SolarMass(4_300_000)
>>> yaris_per_sagittarius_a = round((sagittarius_a / yaris).magnitude)
>>> yaris_per_sagittarius_a
8550163000000000000000000000000000

Phew.
That is...
Eighty-five nonillion, five hundred eighteen octillion, eight hundred eighty septillion
Toyota Yaris cars.
I hope I got it right.

The point is not the car model or the precision of the estimate.
The same `Mass` type that handled a picogram-scale cell can represent a microscopic
molecule, a tonne-scale vehicle, or millions of solar masses without changing the
arithmetic model.

Notes
-----
The kilogram is the canonical unit of `Mass`.
This is unusual among SI base quantities because the base unit itself contains a prefix.

`Tonne` is an alias of `Megagram`, not a separate unit definition:

>>> Tonne is Megagram
True

`MASS_UNITS` maps unit symbols such as ``"mg"``, ``"kg"``, ``"Da"``, and
``"lb"`` to their constructors for configuration files and other external
interfaces.

See Also
--------
~kuchka.quantities.Force
    Force combines mass with acceleration.
~kuchka.quantities.Density
    Density expresses mass per unit volume.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import MASS
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
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
    aliases=("t",),
    words=("tonne", "metric ton", "metric tonne"),
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

    Roughly 300 thousand fruit flies weigh about the same as a dog:

    >>> fly = Gram(0.1)
    >>> dog = Kilogram(30)
    >>> swarm = round((dog / fly).magnitude)
    >>> swarm
    300000

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

DALTON = UnitDef(
    "dalton",
    "Da",
    Decimal("1.66053906892e-27"),
    MASS,
    aliases=("u", "amu"),
    words=("atomic mass unit",),
)


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
    It is the CODATA 2022 atomic mass constant, 1.660 539 068 92 e-27 kg.

    Examples
    --------
    A water molecule has a molecular mass of about 18 Da:

    >>> water = Dalton(18)

    A hemoglobin molecule is roughly 64.5 kDa:

    >>> hemoglobin = Dalton(64500)

    """
    return Mass(to_exact(value) * DALTON.scale, DALTON)


GRAIN = UnitDef("grain", "gr", Decimal("0.00006479891"), MASS)


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


POUND = UnitDef("pound", "lb", Decimal("0.45359237"), MASS, aliases=("lbs",))


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


OUNCE = UnitDef("ounce", "oz", Decimal("0.028349523125"), MASS)


def Ounce(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in ounces.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in ounces.

    Returns
    -------
    Mass
        Mass represented in ounces.

    Notes
    -----
    One ounce is exactly 1/16 pound, i.e. exactly 0.028349523125 kilograms.

    Examples
    --------
    A first-class letter sits within the one-ounce postage limit:

    >>> letter = Ounce(1)
    >>> letter <= Pound(1)
    True

    Sixteen ounces make a pound exactly:

    >>> Ounce(16) == Pound(1)
    True

    """
    return Mass(to_exact(value) * OUNCE.scale, OUNCE)


SOLAR_MASS = UnitDef(
    "solar_mass",
    f"M{symbols.SUN}",
    Decimal("1.988410e30"),
    MASS,
    aliases=("Msun", "M_sun"),
    words=("solar masses",),
)


def SolarMass(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in solar masses.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in solar masses.

    Returns
    -------
    Mass
        Mass represented in solar masses.

    Notes
    -----
    The IAU 2015 nominal solar mass parameter over the CODATA 2022 gravitational
    constant, rounded to seven significant digits: 1.988410e30 kg.

    Examples
    --------
    The Milky Way's central black hole has a mass of about 4.3 million Suns:

    >>> sagittarius_a = SolarMass(4_300_000)

    A binary system can be represented naturally in the same unit:

    >>> primary = SolarMass(1.4)
    >>> secondary = SolarMass(0.8)
    >>> total = primary + secondary
    >>> total
    2.2 M☉

    """
    return Mass(to_exact(value) * SOLAR_MASS.scale, SOLAR_MASS)


EARTH_MASS = UnitDef(
    "earth_mass",
    f"M{symbols.EARTH}",
    Decimal("5.972168e24"),
    MASS,
    aliases=("Mearth", "M_earth"),
    words=("earth masses",),
)


def EarthMass(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in Earth masses.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in Earth masses.

    Returns
    -------
    Mass
        Mass represented in Earth masses.

    Notes
    -----
    The IAU 2015 nominal terrestrial mass parameter over the CODATA 2022 gravitational
    constant, rounded to seven significant digits: 5.972168e24 kg.

    Examples
    --------
    Exoplanet masses are conventionally reported in Earth masses:

    >>> super_earth = EarthMass(Decimal("1.6"))

    Jupiter, at roughly 318 Earth masses, is still a fraction of a Sun:

    >>> jupiter = EarthMass(318)
    >>> jupiter <= SolarMass(1)
    True

    """
    return Mass(to_exact(value) * EARTH_MASS.scale, EARTH_MASS)


MASS_UNITS: Mapping[str, Callable[[Numeric], Mass]] = unit_table(
    "MASS_UNITS",
    {
        PICOGRAM: Picogram,
        NANOGRAM: Nanogram,
        MICROGRAM: Microgram,
        MILLIGRAM: Milligram,
        GRAM: Gram,
        KILOGRAM: Kilogram,
        MEGAGRAM: Megagram,
        DALTON: Dalton,
        GRAIN: Grain,
        POUND: Pound,
        OUNCE: Ounce,
        SOLAR_MASS: SolarMass,
        EARTH_MASS: EarthMass,
    },
)

__all__ = [
    "DALTON",
    "EARTH_MASS",
    "GRAIN",
    "GRAM",
    "KILOGRAM",
    "MASS_UNITS",
    "MEGAGRAM",
    "MICROGRAM",
    "MILLIGRAM",
    "NANOGRAM",
    "OUNCE",
    "PICOGRAM",
    "POUND",
    "SOLAR_MASS",
    "Dalton",
    "EarthMass",
    "Grain",
    "Gram",
    "Kilogram",
    "Megagram",
    "Microgram",
    "Milligram",
    "Nanogram",
    "Ounce",
    "Picogram",
    "Pound",
    "SolarMass",
    "Tonne",
]
