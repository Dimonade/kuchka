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

`Tonne` is an alias of `Megagram`: both names are one unit definition.

>>> Tonne is Megagram
True

Since the 2019 revision of the SI, the kilogram is defined by fixing the Planck constant
at exactly 6.62607015E-34 J·s.

`MASS_UNITS` maps unit symbols such as ``"mg"``, ``"kg"``, ``"Da"``, and
``"lb"`` to their constructors for configuration files and other external
interfaces.

References
----------
BIPM, The International System of Units (SI Brochure), on the kilogram and the
dalton:
https://www.bipm.org/en/publications/si-brochure

NIST, Fundamental Physical Constants, for the atomic mass constant:
https://physics.nist.gov/cuu/Constants/

IAU 2015 Resolution B3, nominal solar and planetary values:
https://arxiv.org/abs/1605.09788

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
    >>> red_blood_cell
    27 pg

    A millilitre of blood holds about five billion red cells, and together they weigh
    135 mg:

    >>> from kuchka.units import MILLIGRAM
    >>> (red_blood_cell * 5_000_000_000).to(MILLIGRAM)
    135 mg

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
    >>> airborne_sample
    85 ng

    A filter that weighs 150.000000 mg before sampling and 150.000085 mg after has
    collected that sample, and decimal arithmetic keeps the difference exact:

    >>> from decimal import Decimal
    >>> from kuchka import Milligram
    >>> from kuchka.units import NANOGRAM
    >>> before = Milligram(Decimal("150.000000"))
    >>> after = Milligram(Decimal("150.000085"))
    >>> (after - before).to(NANOGRAM)
    85 ng

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
    >>> b12
    500 µg

    A label that spells the unit with a plain `u` is read the same way:

    >>> from kuchka import Mass
    >>> from kuchka import parse
    >>> parse("500 ug", Mass) == b12
    True

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
    >>> fruit_fly
    1 mg

    Roughly thirty million fruit flies weigh about the same as a 30 kg dog:

    >>> from kuchka import Kilogram
    >>> dog = Kilogram(30)
    >>> swarm = round((dog / fruit_fly).magnitude)
    >>> swarm
    30000000

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
    A level teaspoon of table salt weighs about 6 g:

    >>> salt = Gram(6)
    >>> salt
    6 g

    A gram of water fills a millilitre, so a mass over a volume gives the density of
    water:

    >>> from kuchka import Millilitre
    >>> from kuchka.units import KILOGRAM_PER_CUBIC_METRE
    >>> (Gram(1) / Millilitre(1)).to(KILOGRAM_PER_CUBIC_METRE)
    1000 kg/m³

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

    Notes
    -----
    The kilogram is the SI base unit of mass, defined by fixing the Planck constant at
    exactly 6.62607015E-34 J·s.

    Examples
    --------
    A full bowling ball weighs up to about 7.26 kg:

    >>> bowling_ball = Kilogram(7.26)
    >>> bowling_ball
    7.26 kg

    Its weight on Earth, with the standard acceleration of gravity, is a force of about
    71 N:

    >>> from kuchka import MetrePerSecondSquared
    >>> from kuchka.units import NEWTON
    >>> weight = bowling_ball * MetrePerSecondSquared(9.80665)
    >>> f"{weight.to(NEWTON):.1f}"
    '71.2 N'

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
    >>> concrete_load
    18 Mg

    In kilograms, that load is:

    >>> from kuchka.units import KILOGRAM
    >>> concrete_load.to(KILOGRAM)
    18000 kg

    A `Megagram` is aliased to the omnipresent `Tonne`:

    >>> from kuchka import Tonne
    >>> Megagram(1.3) == Tonne(1.3)
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
    >>> water
    18 Da

    A hemoglobin molecule is roughly 64.5 kDa:

    >>> hemoglobin = Dalton(64_500)
    >>> round((hemoglobin / water).magnitude)
    3583

    Eighteen grams of water hold about Avogadro's number of molecules, the mass over
    the dalton:

    >>> from kuchka import Gram
    >>> f"{float((Gram(18) / water).magnitude):.4e}"
    '6.0221e+23'

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
    >>> bullet
    147 gr

    A 147 grain bullet weighs a little over nine and a half grams:

    >>> from kuchka.units import GRAM
    >>> f"{bullet.to(GRAM):.2f}"
    '9.53 g'

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
    >>> suitcase
    50 lb

    A 25 kg limit is a little more than 50 lb, so the suitcase fits:

    >>> from kuchka import Kilogram
    >>> baggage_limit = Kilogram(25)
    >>> baggage_limit > suitcase
    True

    The conversion factor to the kilogram is exact:

    >>> from kuchka.units import KILOGRAM
    >>> Pound(1).to(KILOGRAM)
    0.45359237 kg

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
    >>> letter
    1 oz
    >>> from kuchka import Pound
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
    >>> sagittarius_a
    4300000 M☉

    A binary system can be represented naturally in the same unit:

    >>> primary = SolarMass(1.4)
    >>> secondary = SolarMass(0.8)
    >>> total = primary + secondary
    >>> total
    2.2 M☉

    In kilograms, one solar mass is:

    >>> from kuchka.units import KILOGRAM
    >>> f"{SolarMass(1).to(KILOGRAM):.6e}"
    '1.988410e+30 kg'

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

    >>> from decimal import Decimal
    >>> super_earth = EarthMass(Decimal("1.6"))
    >>> super_earth
    1.6 M♁

    Jupiter, at roughly 318 Earth masses, is still a fraction of a Sun:

    >>> from kuchka import SolarMass
    >>> jupiter = EarthMass(318)
    >>> f"{jupiter / SolarMass(1):.3e}"
    9.551e-4 1

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
