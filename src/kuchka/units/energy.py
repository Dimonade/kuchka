"""Energy quantities and constructors for common engineering and scientific units.

`Energy` represents a scalar energy quantity.
The module provides SI-prefixed joules for general engineering use, watt-hours for
stored or consumed electrical energy, electronvolts for microscopic physics, and the
erg for astrophysical and historical CGS literature.

Joule is the canonical SI unit used internally by :class:`~kuchka.quantities.Energy`.
All constructors accept a plain numeric magnitude in their named unit and return an
`Energy` value carrying that unit explicitly.

The different unit families are useful at very different physical scales:

* pico- and nanojoules occur in optical and electronic measurements;
* micro- and millijoules are common for short pulses and small mechanical events;
* joules describe laboratory and everyday mechanical energy;
* kilojoules and megajoules cover human-scale work, chemistry, and transport;
* gigajoules and terajoules are useful for industrial and geophysical energy budgets;
* watt-hours describe stored or consumed electrical energy;
* kilocalories (food Calories) are conventional in nutrition and exercise;
* electronvolts describe the energy of individual particles and photons;
* ergs remain common in astrophysical literature.

Examples
--------
Energy values retain their physical units while participating in arithmetic.
A 2 mJ pulse followed by a 500 uJ pulse can be added directly:

>>> pulse_energy = Millijoule(2) + Microjoule(500)

The same principle works when the scale changes by several orders of magnitude.
One kilowatt-hour is exactly 3.6 MJ:

>>> battery_charge = KilowattHour(1)
>>> battery_work = Megajoule(3.6)

A mechanical example needs no special representation for the physics once the energy
has been calculated.
A 2 kg brick moving at 10 m/s has 100 J of kinetic energy:

>>> brick_energy = Joule(100)

If 20 J is dissipated by deformation, sound, and air resistance, the remaining
mechanical energy is still an `Energy` value:

>>> impact_energy = brick_energy - Joule(20)

The kilojoule scale is useful for human-scale mechanical work.
Raising an 80 kg person by 5 m requires about 3.92 kJ of gravitational potential
energy:

>>> stair_climb = Kilojoule(3.92266)

Electrical energy is often specified in watt-hours.
A nominal 500 Wh battery from which 125 Wh has been consumed leaves:

>>> battery = WattHour(500)
>>> remaining = battery - WattHour(125)

For very low-power electronics, milliwatt-hours provide a convenient scale.
A sensor budget of 5 mWh per acquisition cycle can be expressed without encoding the
unit into the variable name:

>>> acquisition_energy = MilliwattHour(5)

Nutrition commonly expresses food energy in kilocalories, written as Calories on food
labels.
A 650 kcal meal and 420 kcal of exercise energy can be represented as ordinary `Energy`
values:

>>> meal = Calorie(650)
>>> exercise = Calorie(420)
>>> remaining = meal - exercise

The quantity itself does not become a different kind of energy when the unit changes.
The same 650 food Calories correspond to 2723.6 kJ:

>>> meal = Calorie(650)
>>> equivalent = Kilojoule(2723.6)

At particle-physics scales, the electronvolt is more useful than the joule.
The ionization energy of ground-state hydrogen is approximately 13.6 eV:

>>> hydrogen_ionization = Electronvolt(13.6)

The same unit family naturally extends through atomic, nuclear, and high-energy
physics:

>>> xray_photon = Kiloelectronvolt(60)
>>> alpha_particle = Megaelectronvolt(5.5)
>>> proton_rest_energy = Gigaelectronvolt(0.938272088)

At even larger particle energies, teraelectronvolts are the natural scale:

>>> collider_particle = Teraelectronvolt(1)

Astrophysics has its own historical energy vocabulary.
A canonical supernova-scale energy of 10^51 erg can be represented directly, while the
underlying `Energy` quantity remains the same physical concept used by the SI
constructors:

>>> supernova_energy = Erg(10**51)

Notes
-----
The watt-hour is a unit of energy, not power.
For example, ``500 Wh`` denotes an amount of energy that could be delivered by a 500 W
source for one hour.

The electronvolt is defined from the exact SI value of the elementary charge, so the
conversion

``1 eV = 1.602176634e-19 J``

is exact.

The erg is a CGS unit:

``1 erg = 1e-7 J``.

`Calorie` denotes the nutritional kilocalorie: ``1 Cal = 1 kcal = 4184 J``.
The capitalization distinguishes the food-energy convention from the small calorie used
in historical physical measurements.

`ThermochemicalCalorie` denotes the thermochemical calorie:

``1 cal_th = 4.184 J``.

`ENERGY_UNITS` maps unit symbols such as ``"J"``, ``"eV"``, and ``"Wh"`` to
their constructors. It is intended for boundary code that receives units from
configuration files, protocols, or other external sources.

See Also
--------
~kuchka.quantities.Energy
    Quantity type representing energy.
~kuchka.quantities.Power
    Rate of energy transfer.
~kuchka.quantities.Time
    Time intervals that can be combined with power to describe energy.

"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import ENERGY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Energy
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


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
    """Construct an Energy from a magnitude expressed in picojoules."""
    return Energy(to_exact(value) * PICOJOULE.scale, PICOJOULE)


def Nanojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in nanojoules."""
    return Energy(to_exact(value) * NANOJOULE.scale, NANOJOULE)


def Microjoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in microjoules."""
    return Energy(to_exact(value) * MICROJOULE.scale, MICROJOULE)


def Millijoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in millijoules."""
    return Energy(to_exact(value) * MILLIJOULE.scale, MILLIJOULE)


def Joule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in joules."""
    return Energy(to_exact(value) * JOULE.scale, JOULE)


def Kilojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in kilojoules."""
    return Energy(to_exact(value) * KILOJOULE.scale, KILOJOULE)


def Megajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in megajoules."""
    return Energy(to_exact(value) * MEGAJOULE.scale, MEGAJOULE)


def Gigajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in gigajoules."""
    return Energy(to_exact(value) * GIGAJOULE.scale, GIGAJOULE)


def Terajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in terajoules."""
    return Energy(to_exact(value) * TERAJOULE.scale, TERAJOULE)


# Electronvolt

ELECTRONVOLT = UnitDef("electronvolt", "eV", Decimal("1.602176634e-19"), ENERGY)


def Electronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in electronvolts."""
    return Energy(to_exact(value) * ELECTRONVOLT.scale, ELECTRONVOLT)


# Watt times Time.

MILLIWATT_HOUR = UnitDef("milliwatt_hour", "mWh", Decimal("3.6"), ENERGY)
WATT_HOUR = UnitDef("watt_hour", "Wh", Decimal(3600), ENERGY)


def MilliwattHour(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in milliwatt-hours."""
    return Energy(to_exact(value) * MILLIWATT_HOUR.scale, MILLIWATT_HOUR)


def WattHour(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in watt-hours."""
    return Energy(to_exact(value) * WATT_HOUR.scale, WATT_HOUR)


ENERGY_UNITS: Mapping[str, Callable[[Numeric], Energy]] = MappingProxyType(
    {
        PICOJOULE.symbol: Picojoule,
        NANOJOULE.symbol: Nanojoule,
        MICROJOULE.symbol: Microjoule,
        MILLIJOULE.symbol: Millijoule,
        JOULE.symbol: Joule,
        KILOJOULE.symbol: Kilojoule,
        MEGAJOULE.symbol: Megajoule,
        ELECTRONVOLT.symbol: Electronvolt,
        MILLIWATT_HOUR.symbol: MilliwattHour,
        WATT_HOUR.symbol: WattHour,
    }
)

__all__ = [
    "ELECTRONVOLT",
    "ENERGY_UNITS",
    "GIGAJOULE",
    "JOULE",
    "KILOJOULE",
    "MEGAJOULE",
    "MICROJOULE",
    "MILLIJOULE",
    "MILLIWATT_HOUR",
    "NANOJOULE",
    "PICOJOULE",
    "TERAJOULE",
    "WATT_HOUR",
    "Electronvolt",
    "Gigajoule",
    "Joule",
    "Kilojoule",
    "Megajoule",
    "Microjoule",
    "Millijoule",
    "MilliwattHour",
    "Nanojoule",
    "Picojoule",
    "Terajoule",
    "WattHour",
]
