"""Energy quantities and constructors for common engineering and scientific units.

`Energy` represents a scalar energy quantity.
The module provides SI-prefixed joules for general engineering use, watt-hours for
stored or consumed electrical energy, electronvolts for microscopic physics, the erg
for astrophysical and historical CGS literature, and calories for nutrition and
thermochemistry.

Joule is the canonical SI unit used internally by :class:`~kuchka.quantities.Energy`.
Every constructor here accepts a plain numeric magnitude in its named unit and returns
an `Energy` value carrying that unit explicitly.

The different unit families suit very different physical scales:

* pico- and nanojoules occur in optical and electronic measurements;
* micro- and millijoules are common for short pulses and small mechanical events;
* joules describe laboratory and everyday mechanical energy;
* kilojoules and megajoules cover human-scale work, chemistry, and transport;
* gigajoules and terajoules suit industrial and geophysical energy budgets;
* watt-hours describe stored or consumed electrical energy;
* kilocalories (food Calories) are conventional in nutrition and exercise;
* electronvolts describe the energy of individual particles and photons;
* ergs remain common in astrophysical literature.

Examples
--------
Energy values carry their physical unit through arithmetic.
A 2 mJ pulse followed by a 500 uJ pulse adds directly, in millijoules:

>>> pulse_energy = Millijoule(2) + Microjoule(500)
>>> pulse_energy
2.5 mJ

A mechanical example needs no special representation for the physics once the energy
has been calculated.
A 2 kg brick moving at 10 m/s carries 100 J of kinetic energy:

>>> brick_energy = Joule(100)

If 20 J is dissipated by deformation, sound, and air resistance, the remaining
mechanical energy is still an `Energy` value:

>>> impact_energy = brick_energy - Joule(20)
>>> impact_energy
80 J

The kilojoule scale suits human-scale mechanical work.
Raising an 80 kg person by 5 m at standard gravity takes about 3.92266 kJ of
gravitational potential energy:

>>> stair_climb = Kilojoule(Decimal("3.92266"))

Electrical energy is often specified in watt-hours.
A nominal 500 Wh battery from which 125 Wh has been consumed leaves:

>>> battery = WattHour(500)
>>> remaining = battery - WattHour(125)
>>> remaining
375 Wh

For very low-power electronics, milliwatt-hours give a convenient scale.
A sensor budget of 5 mWh per acquisition cycle needs no unit encoded into the variable
name:

>>> acquisition_energy = MilliwattHour(5)

Nutrition commonly expresses food energy in kilocalories, printed as Calories on food
labels.
A 650 kcal meal and 420 kcal of exercise energy are ordinary `Energy` values:

>>> meal = Calorie(650)
>>> exercise = Calorie(420)
>>> remaining_budget = meal - exercise
>>> remaining_budget
230 kcal

The quantity stays the same energy when the unit changes.
650 food Calories equal 2719.6 kJ:

>>> meal = Calorie(650)
>>> equivalent = Kilojoule(Decimal("2719.6"))
>>> meal == equivalent
True

At particle-physics scales, the electronvolt is a more common unit.
The ionization energy of ground-state hydrogen is approximately 13.6 eV:

>>> hydrogen_ionization = Electronvolt(Decimal("13.6"))
>>> hydrogen_ionization
13.6 eV

The same unit family extends through atomic, nuclear, and high-energy physics:

>>> xray_photon = Kiloelectronvolt(60)
>>> alpha_particle = Megaelectronvolt(Decimal("5.5"))
>>> proton_rest_energy = Gigaelectronvolt(Decimal("0.938272088"))

At collider-scale particle energies, teraelectronvolts are the natural unit:

>>> collider_particle = Teraelectronvolt(1)
>>> collider_particle
1 TeV

Astrophysics keeps its own historical energy vocabulary.
A canonical supernova-scale energy of 10**51 erg is representable directly, as the same
`Energy` concept the SI constructors already use:

>>> supernova_energy = Erg(10**51)
>>> supernova_energy == Joule(Decimal("1e44"))
True

Notes
-----
The watt-hour is a unit of energy, not power.
For example, ``500 Wh`` denotes an amount of energy that a 500 W source could deliver
over one hour.

The electronvolt derives from the exact SI value of the elementary charge, so the
conversion

``1 eV = 1.602176634e-19 J``

is exact, and every prefixed electronvolt constructor here (`Microelectronvolt`
through `Petaelectronvolt`) scales that same exact value by a power of ten.

The erg is a CGS unit:

``1 erg = 1e-7 J``.

`Calorie` denotes the nutritional kilocalorie: ``1 Cal = 1 kcal = 4184 J``.
The capitalization distinguishes the food-energy convention from the small calorie
used in historical physical measurements. `Kilocalorie` is the same function object,
for callers who prefer the explicit SI-style name.

`ThermochemicalCalorie` denotes the thermochemical calorie:

``1 cal_th = 4.184 J``.

`ENERGY_UNITS` maps unit symbols such as ``"J"``, ``"eV"``, and ``"Wh"`` to their
constructors. It is intended for boundary code that receives units from configuration
files, protocols, or other external sources.

See Also
--------
~kuchka.quantities.Energy
    Quantity type representing energy.
~kuchka.quantities.Power
    Rate of energy transfer.
~kuchka.quantities.Time
    Time intervals that combine with power to describe energy.

"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import ENERGY
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Energy
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


# Joule and its SI prefixes.

JOULE_NAME = "joule"
JOULE_SYMBOL = "J"

PICOJOULE = prefixed_unit(prefixes.PICO, JOULE_NAME, JOULE_SYMBOL, ENERGY)
NANOJOULE = prefixed_unit(prefixes.NANO, JOULE_NAME, JOULE_SYMBOL, ENERGY)
MICROJOULE = prefixed_unit(prefixes.MICRO, JOULE_NAME, JOULE_SYMBOL, ENERGY)
MILLIJOULE = prefixed_unit(prefixes.MILLI, JOULE_NAME, JOULE_SYMBOL, ENERGY)
JOULE = prefixed_unit(prefixes.UNIT, JOULE_NAME, JOULE_SYMBOL, ENERGY)
KILOJOULE = prefixed_unit(prefixes.KILO, JOULE_NAME, JOULE_SYMBOL, ENERGY)
MEGAJOULE = prefixed_unit(prefixes.MEGA, JOULE_NAME, JOULE_SYMBOL, ENERGY)
GIGAJOULE = prefixed_unit(prefixes.GIGA, JOULE_NAME, JOULE_SYMBOL, ENERGY)
TERAJOULE = prefixed_unit(prefixes.TERA, JOULE_NAME, JOULE_SYMBOL, ENERGY)


Energy._canonical_unit = JOULE  # noqa: SLF001 -- this module owns Energy's canonical unit


def Picojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in picojoules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in picojoules.

    Returns
    -------
    Energy
        Energy represented by `value` picojoules.

    """
    return Energy(to_exact(value) * PICOJOULE.scale, PICOJOULE)


def Nanojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in nanojoules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in nanojoules.

    Returns
    -------
    Energy
        Energy represented by `value` nanojoules.

    """
    return Energy(to_exact(value) * NANOJOULE.scale, NANOJOULE)


def Microjoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in microjoules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in microjoules.

    Returns
    -------
    Energy
        Energy represented by `value` microjoules.

    """
    return Energy(to_exact(value) * MICROJOULE.scale, MICROJOULE)


def Millijoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in millijoules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in millijoules.

    Returns
    -------
    Energy
        Energy represented by `value` millijoules.

    Examples
    --------
    A pulse energy budget adds cleanly across prefixes:

    >>> Millijoule(2) + Microjoule(500)
    2.5 mJ

    """
    return Energy(to_exact(value) * MILLIJOULE.scale, MILLIJOULE)


def Joule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in joules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in joules.

    Returns
    -------
    Energy
        Energy represented by `value` joules.

    Examples
    --------
    A 2 kg brick moving at 10 m/s carries 100 J of kinetic energy:

    >>> Joule(100)
    100 J

    """
    return Energy(to_exact(value) * JOULE.scale, JOULE)


def Kilojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in kilojoules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in kilojoules.

    Returns
    -------
    Energy
        Energy represented by `value` kilojoules.

    Examples
    --------
    Raising an 80 kg person by 5 m at standard gravity takes about 3.92266 kJ:

    >>> Kilojoule(Decimal("3.92266"))
    3.92266 kJ

    """
    return Energy(to_exact(value) * KILOJOULE.scale, KILOJOULE)


def Megajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in megajoules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in megajoules.

    Returns
    -------
    Energy
        Energy represented by `value` megajoules.

    """
    return Energy(to_exact(value) * MEGAJOULE.scale, MEGAJOULE)


def Gigajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in gigajoules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in gigajoules.

    Returns
    -------
    Energy
        Energy represented by `value` gigajoules.

    Examples
    --------
    An industrial energy budget sits comfortably in gigajoules:

    >>> Gigajoule(Decimal("2.4"))
    2.4 GJ

    """
    return Energy(to_exact(value) * GIGAJOULE.scale, GIGAJOULE)


def Terajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in terajoules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in terajoules.

    Returns
    -------
    Energy
        Energy represented by `value` terajoules.

    Examples
    --------
    A large hydroelectric dam's yearly output lands in the terajoule range:

    >>> Terajoule(600)
    600 TJ

    """
    return Energy(to_exact(value) * TERAJOULE.scale, TERAJOULE)


# Electronvolt and its SI prefixes.
#
# The electronvolt is not itself SI-coherent, so `prefixed_unit()` (built for scaling
# a dimension's own coherent unit) does not apply directly; each prefix's scale is
# instead computed explicitly as `prefix.factor * _ELECTRONVOLT_IN_JOULES`, reusing
# the same `Prefix.factor` every other family's prefixes come from.

_ELECTRONVOLT_IN_JOULES = Decimal("1.602176634e-19")
"""Energy equivalent of one electronvolt.

Exact since the 2019 SI redefinition fixed the elementary charge's value.
"""

MICROELECTRONVOLT = UnitDef(
    "microelectronvolt",
    f"{symbols.MICRO}eV",
    prefixes.MICRO.factor * _ELECTRONVOLT_IN_JOULES,
    ENERGY,
)
MILLIELECTRONVOLT = UnitDef(
    "millielectronvolt",
    "meV",
    prefixes.MILLI.factor * _ELECTRONVOLT_IN_JOULES,
    ENERGY,
)
ELECTRONVOLT = UnitDef("electronvolt", "eV", _ELECTRONVOLT_IN_JOULES, ENERGY)
KILOELECTRONVOLT = UnitDef(
    "kiloelectronvolt",
    "keV",
    prefixes.KILO.factor * _ELECTRONVOLT_IN_JOULES,
    ENERGY,
)
MEGAELECTRONVOLT = UnitDef(
    "megaelectronvolt",
    "MeV",
    prefixes.MEGA.factor * _ELECTRONVOLT_IN_JOULES,
    ENERGY,
)
GIGAELECTRONVOLT = UnitDef(
    "gigaelectronvolt",
    "GeV",
    prefixes.GIGA.factor * _ELECTRONVOLT_IN_JOULES,
    ENERGY,
)
TERAELECTRONVOLT = UnitDef(
    "teraelectronvolt",
    "TeV",
    prefixes.TERA.factor * _ELECTRONVOLT_IN_JOULES,
    ENERGY,
)
PETAELECTRONVOLT = UnitDef(
    "petaelectronvolt",
    "PeV",
    prefixes.PETA.factor * _ELECTRONVOLT_IN_JOULES,
    ENERGY,
)


def Microelectronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in microelectronvolts.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in microelectronvolts.

    Returns
    -------
    Energy
        Energy represented by `value` microelectronvolts.

    """
    return Energy(to_exact(value) * MICROELECTRONVOLT.scale, MICROELECTRONVOLT)


def Millielectronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in millielectronvolts.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in millielectronvolts.

    Returns
    -------
    Energy
        Energy represented by `value` millielectronvolts.

    """
    return Energy(to_exact(value) * MILLIELECTRONVOLT.scale, MILLIELECTRONVOLT)


def Electronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in electronvolts.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in electronvolts.

    Returns
    -------
    Energy
        Energy represented by `value` electronvolts.

    Examples
    --------
    The ionization energy of ground-state hydrogen is approximately 13.6 eV:

    >>> Electronvolt(Decimal("13.6"))
    13.6 eV

    """
    return Energy(to_exact(value) * ELECTRONVOLT.scale, ELECTRONVOLT)


def Kiloelectronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in kiloelectronvolts.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in kiloelectronvolts.

    Returns
    -------
    Energy
        Energy represented by `value` kiloelectronvolts.

    Examples
    --------
    A diagnostic X-ray photon sits around 60 keV:

    >>> Kiloelectronvolt(60)
    60 keV

    """
    return Energy(to_exact(value) * KILOELECTRONVOLT.scale, KILOELECTRONVOLT)


def Megaelectronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in megaelectronvolts.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in megaelectronvolts.

    Returns
    -------
    Energy
        Energy represented by `value` megaelectronvolts.

    Examples
    --------
    An alpha particle carries a few megaelectronvolts of kinetic energy:

    >>> Megaelectronvolt(Decimal("5.5"))
    5.5 MeV

    """
    return Energy(to_exact(value) * MEGAELECTRONVOLT.scale, MEGAELECTRONVOLT)


def Gigaelectronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in gigaelectronvolts.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in gigaelectronvolts.

    Returns
    -------
    Energy
        Energy represented by `value` gigaelectronvolts.

    Examples
    --------
    A proton's rest energy is about 0.938272088 GeV:

    >>> Gigaelectronvolt(Decimal("0.938272088"))
    0.938272088 GeV

    """
    return Energy(to_exact(value) * GIGAELECTRONVOLT.scale, GIGAELECTRONVOLT)


def Teraelectronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in teraelectronvolts.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in teraelectronvolts.

    Returns
    -------
    Energy
        Energy represented by `value` teraelectronvolts.

    Examples
    --------
    A collider beam particle reaches teraelectronvolt-scale energy:

    >>> Teraelectronvolt(1)
    1 TeV

    """
    return Energy(to_exact(value) * TERAELECTRONVOLT.scale, TERAELECTRONVOLT)


def Petaelectronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in petaelectronvolts.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in petaelectronvolts.

    Returns
    -------
    Energy
        Energy represented by `value` petaelectronvolts.

    Examples
    --------
    Ultra-high-energy cosmic rays reach petaelectronvolt-scale energies:

    >>> Petaelectronvolt(1)
    1 PeV

    """
    return Energy(to_exact(value) * PETAELECTRONVOLT.scale, PETAELECTRONVOLT)


# Watt times Time.

MILLIWATT_HOUR = UnitDef("milliwatt_hour", "mWh", Decimal("3.6"), ENERGY)
WATT_HOUR = UnitDef("watt_hour", "Wh", Decimal(3600), ENERGY)


def MilliwattHour(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in milliwatt-hours.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in milliwatt-hours.

    Returns
    -------
    Energy
        Energy represented by `value` milliwatt-hours.

    Examples
    --------
    A sensor's per-cycle energy budget fits a few milliwatt-hours:

    >>> MilliwattHour(5)
    5 mWh

    """
    return Energy(to_exact(value) * MILLIWATT_HOUR.scale, MILLIWATT_HOUR)


def WattHour(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in watt-hours.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in watt-hours.

    Returns
    -------
    Energy
        Energy represented by `value` watt-hours.

    Examples
    --------
    A 500 Wh battery from which 125 Wh has been drawn leaves:

    >>> WattHour(500) - WattHour(125)
    375 Wh

    """
    return Energy(to_exact(value) * WATT_HOUR.scale, WATT_HOUR)


# Erg: the CGS unit of energy.

ERG = UnitDef("erg", "erg", Decimal("1E-7"), ENERGY)
"""The CGS unit of energy: exactly 1e-7 joules, by definition of the CGS system."""


def Erg(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in ergs.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in ergs.

    Returns
    -------
    Energy
        Energy represented by `value` ergs.

    Examples
    --------
    A canonical supernova releases on the order of 10**51 erg, exactly 1e44 J:

    >>> Erg(10**51) == Joule(Decimal("1e44"))
    True

    See Also
    --------
    Joule : The SI unit an erg relates to by an exact factor of 1e-7.

    """
    return Energy(to_exact(value) * ERG.scale, ERG)


# Calories: nutritional and thermochemical.

THERMOCHEMICAL_CALORIE = UnitDef(
    "thermochemical_calorie",
    f"cal{symbols.SUBSCRIPT_T}{symbols.SUBSCRIPT_H}",
    Decimal("4.184"),
    ENERGY,
)
KILOCALORIE = UnitDef("kilocalorie", "kcal", Decimal(4184), ENERGY)


def Calorie(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in food Calories.

    A food Calorie (capital C) is a kilocalorie: 1 Cal = 1 kcal = 4184 J exactly.

    Parameters
    ----------
    value : Numeric
        Energy magnitude in Calories (kilocalories).

    Returns
    -------
    Energy
        Energy represented by `value` Calories.

    Examples
    --------
    A food label listing 650 Calories corresponds to 650 kcal:

    >>> breakfast = Calorie(650)
    >>> breakfast
    650 kcal

    The same quantity compares directly with an SI energy value:

    >>> breakfast == Kilojoule(Decimal("2719.6"))
    True

    See Also
    --------
    Kilocalorie : The same constructor, under its explicit SI-style name.
    ThermochemicalCalorie : The unrelated, smaller thermochemical calorie.

    """
    return Energy(to_exact(value) * KILOCALORIE.scale, KILOCALORIE)


Kilocalorie = Calorie
"""A kilocalorie is a food Calorie: the same function object as `Calorie`.

Examples
--------
>>> Kilocalorie(650) == Calorie(650)
True
"""


def ThermochemicalCalorie(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in thermochemical calories.

    One thermochemical calorie is exactly 4.184 J -- a thousandth the size of the
    food Calorie `Calorie` and `Kilocalorie` construct.

    Parameters
    ----------
    value : Numeric
        Energy magnitude in thermochemical calories.

    Returns
    -------
    Energy
        Energy represented by `value` thermochemical calories.

    Examples
    --------
    A laboratory energy quantity reported in the historical thermochemical
    convention:

    >>> laboratory_energy = ThermochemicalCalorie(100)
    >>> laboratory_energy
    100 calₜₕ
    >>> laboratory_energy == Joule(Decimal("418.4"))
    True

    """
    return Energy(
        to_exact(value) * THERMOCHEMICAL_CALORIE.scale, THERMOCHEMICAL_CALORIE
    )


ENERGY_UNITS: Mapping[str, Callable[[Numeric], Energy]] = MappingProxyType(
    {
        PICOJOULE.symbol: Picojoule,
        NANOJOULE.symbol: Nanojoule,
        MICROJOULE.symbol: Microjoule,
        MILLIJOULE.symbol: Millijoule,
        JOULE.symbol: Joule,
        KILOJOULE.symbol: Kilojoule,
        MEGAJOULE.symbol: Megajoule,
        GIGAJOULE.symbol: Gigajoule,
        TERAJOULE.symbol: Terajoule,
        MICROELECTRONVOLT.symbol: Microelectronvolt,
        MILLIELECTRONVOLT.symbol: Millielectronvolt,
        ELECTRONVOLT.symbol: Electronvolt,
        KILOELECTRONVOLT.symbol: Kiloelectronvolt,
        MEGAELECTRONVOLT.symbol: Megaelectronvolt,
        GIGAELECTRONVOLT.symbol: Gigaelectronvolt,
        TERAELECTRONVOLT.symbol: Teraelectronvolt,
        PETAELECTRONVOLT.symbol: Petaelectronvolt,
        MILLIWATT_HOUR.symbol: MilliwattHour,
        WATT_HOUR.symbol: WattHour,
        ERG.symbol: Erg,
        THERMOCHEMICAL_CALORIE.symbol: ThermochemicalCalorie,
        KILOCALORIE.symbol: Kilocalorie,
    }
)
"""Mapping from unit symbol to constructor, for boundary code parsing string units."""

__all__ = [
    "ELECTRONVOLT",
    "ENERGY_UNITS",
    "ERG",
    "GIGAELECTRONVOLT",
    "GIGAJOULE",
    "JOULE",
    "KILOCALORIE",
    "KILOELECTRONVOLT",
    "KILOJOULE",
    "MEGAELECTRONVOLT",
    "MEGAJOULE",
    "MICROELECTRONVOLT",
    "MICROJOULE",
    "MILLIELECTRONVOLT",
    "MILLIJOULE",
    "MILLIWATT_HOUR",
    "NANOJOULE",
    "PETAELECTRONVOLT",
    "PICOJOULE",
    "TERAELECTRONVOLT",
    "TERAJOULE",
    "THERMOCHEMICAL_CALORIE",
    "WATT_HOUR",
    "Calorie",
    "Electronvolt",
    "Erg",
    "Gigaelectronvolt",
    "Gigajoule",
    "Joule",
    "Kilocalorie",
    "Kiloelectronvolt",
    "Kilojoule",
    "Megaelectronvolt",
    "Megajoule",
    "Microelectronvolt",
    "Microjoule",
    "Millielectronvolt",
    "Millijoule",
    "MilliwattHour",
    "Nanojoule",
    "Petaelectronvolt",
    "Picojoule",
    "Teraelectronvolt",
    "Terajoule",
    "ThermochemicalCalorie",
    "WattHour",
]
