"""Energy quantities and constructors for common engineering and scientific units.

`Energy` represents a scalar energy quantity.
The module provides SI-prefixed joules for general engineering use, watt-hours for
stored or consumed electrical energy, electronvolts for microscopic physics, the
erg for astrophysical and historical CGS literature, calories for nutrition and
thermochemistry, and TNT equivalent for very large energy releases.

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
* kilowatt-hours describe household, battery, and grid-scale electrical energy;
* kilocalories (food Calories) are conventional in nutrition and exercise;
* electronvolts describe the energy of individual particles and photons;
* ergs remain common in astrophysical literature;
* kilotonnes and megatonnes of TNT describe very large energy releases.

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

Electrical energy is often specified in watt-hours because battery capacities and
energy budgets are naturally discussed on that scale.

A small spacecraft has an 84 kWh battery.
During one phase of a mission, its thermal system consumes 7.25 kWh, communications
consume 1,875 Wh, and the science payload consumes another 2.625 kWh:

>>> battery = KilowattHour(84)
>>> remaining = (
...     battery
...     - KilowattHour(7.25)
...     - WattHour(1875)
...     - KilowattHour(2.625)
... )
>>> remaining
72.25 kWh

The remaining energy is the same quantity regardless of which engineering scale is used
to report it:

>>> remaining.to(MEGAJOULE)
260.1 MJ

For comparison, a 25 kWh storage system holds exactly 90 MJ:

>>> storage = KilowattHour(25)
>>> storage.to(MEGAJOULE)
90 MJ

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

TNT equivalent provides another useful scale for very large energy releases.
A kilotonne of TNT equivalent corresponds to exactly 4.184 TJ:

>>> kilotonne_release = KilotonneOfTNT(1)
>>> kilotonne_release.to(TERAJOULE)
4.184 TJ

At the megatonne scale the same convention reaches petajoules:

>>> megatonne_release = MegatonneOfTNT(1)
>>> megatonne_release.to(PETAJOULE)
4.184 PJ

Notes
-----
The watt-hour is a unit of energy, not power.
For example, ``500 Wh`` denotes an amount of energy that a 500 W source could deliver
over one hour.

One watt-hour is exactly:

``1 Wh = 3600 J``

A kilowatt-hour is therefore exactly:

``1 kWh = 3600000 J = 3.6 MJ``

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

TNT equivalent is a convenient way to describe very large energy releases without
writing unwieldy numbers of joules.

Suppose an impact model starts with 2.4 megatonnes of TNT equivalent.
The model attributes 350 kilotonnes to atmospheric shock and 0.9 megatonnes to ejecta:

>>> total = MegatonneOfTNT(2.4)
>>> atmospheric = KilotonneOfTNT(350)
>>> ejecta = MegatonneOfTNT(0.9)
>>> remainder = total - atmospheric - ejecta
>>> remainder
1.15 MtTNT

The same remaining energy can be reported in SI units without losing the exact
relationship between the two descriptions:

>>> remainder.to(PETAJOULE)
4.8116 PJ

The individual TNT scales are therefore not separate kinds of energy.
They are different engineering vocabularies for the same `Energy` quantity.

`ENERGY_UNITS` maps unit symbols such as ``"J"``, ``"eV"``, ``"Wh"``, ``"kWh"``, and
``"ktTNT"`` to their constructors.
It is intended for boundary code that receives units from configuration files,
protocols, or other external sources.

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
PETAJOULE = prefixed_unit(prefixes.PETA, JOULE_NAME, JOULE_SYMBOL, ENERGY)


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

    Examples
    --------
    An optical calibration pulse is split between two detector stages:

    >>> stage_one = Picojoule(320)
    >>> stage_two = Picojoule(680)
    >>> calibration = stage_one + stage_two
    >>> calibration.to(NANOJOULE)
    1 nJ

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

    Examples
    --------
    A MEMS actuator stores 80 nJ before releasing 35 nJ into a mechanical movement:

    >>> stored = Nanojoule(80)
    >>> released = Nanojoule(35)
    >>> stored - released
    45 nJ

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

    Examples
    --------
    An optical system delivers 65 microjoules to a target, of which 20 microjoules are
    reflected:

    >>> incident = Microjoule(65)
    >>> reflected = Microjoule(20)
    >>> absorbed = incident - reflected
    >>> absorbed.to(MILLIJOULE)
    0.045 mJ

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
    A pulse energy is assembled from a 2 mJ main pulse and a 500 microjoule pre-pulse:

    >>> main_pulse = Millijoule(2)
    >>> pre_pulse = Microjoule(500)
    >>> main_pulse + pre_pulse
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
    A 2 kg test mass moving at 10 m/s carries 100 J of kinetic energy.
    If 36 J is dissipated by friction, 64 J remains:

    >>> kinetic_energy = Joule(100)
    >>> dissipated = Joule(36)
    >>> kinetic_energy - dissipated
    64 J

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
    Raising an 80 kg load by 5 m at standard gravity requires about 3.92266 kJ.
    A further 0.37734 kJ is lost in the lifting mechanism:

    >>> useful_work = Kilojoule(Decimal("3.92266"))
    >>> losses = Kilojoule(Decimal("0.37734"))
    >>> useful_work + losses
    4.3 kJ

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

    Examples
    --------
    A 1,000 kg test vehicle moving at 60 m/s carries 1.8 MJ of kinetic energy.
    After 0.4 MJ is dissipated during braking, 1.4 MJ remains:

    >>> kinetic_energy = Megajoule(Decimal("1.8"))
    >>> dissipated = Megajoule(Decimal("0.4"))
    >>> kinetic_energy - dissipated
    1.4 MJ

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
    A high-power plasma system deposits 2.4 GJ during a test pulse.
    Thermal losses account for 0.35 GJ:

    >>> deposited = Gigajoule(Decimal("2.4"))
    >>> thermal_losses = Gigajoule(Decimal("0.35"))
    >>> deposited - thermal_losses
    2.05 GJ

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
    A 70 MW generator running continuously for four hours produces 280 MWh:

    >>> output = KilowattHour(280_000)
    >>> output.to(TERAJOULE)
    1.008 TJ

    """
    return Energy(to_exact(value) * TERAJOULE.scale, TERAJOULE)


def Petajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in petajoules.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in petajoules.

    Returns
    -------
    Energy
        Energy represented by `value` petajoules.

    Examples
    --------
    A planetary-defense system has a 12.5 PJ energy budget. Three interception
    burns consume 2.8 PJ, 1.75 PJ, and 3.2 PJ respectively:

    >>> budget = Petajoule(12.5)
    >>> remaining = budget - Petajoule(2.8) - Petajoule(1.75) - Petajoule(3.2)
    >>> remaining
    4.75 PJ

    The remaining budget is also exactly 4,750 TJ:

    >>> remaining.to(TERAJOULE)
    4750 TJ

    ---

    A 2 GW power station operating continuously for one week produces
    336 GWh of energy:

    >>> weekly_output = KilowattHour(2_000_000 * 24 * 7)
    >>> weekly_output.to(PETAJOULE)
    1.2096 PJ

    """
    return Energy(to_exact(value) * PETAJOULE.scale, PETAJOULE)


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

    Examples
    --------
    The Zeeman splitting of an electron spin in a 1 T magnetic field is on the order of
    116 microelectronvolts:

    >>> spin_splitting = Microelectronvolt(Decimal("115.77"))
    >>> spin_splitting.to(MILLIELECTRONVOLT)
    0.11577 meV

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

    Examples
    --------
    At room temperature, the thermal energy scale kT is about 25.85 meV:

    >>> thermal_energy = Millielectronvolt(Decimal("25.85"))
    >>> thermal_energy
    25.85 meV

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
    Ground-state hydrogen requires 13.6 eV to ionize.
    The first excited state lies 10.2 eV above the ground state, leaving a 3.4 eV gap
    to ionization:

    >>> ionization = Electronvolt(Decimal("13.6"))
    >>> excitation = Electronvolt(Decimal("10.2"))
    >>> ionization - excitation
    3.4 eV

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
    A diagnostic X-ray photon carries 60 keV.
    If 45 keV is deposited in a detector, the remaining 15 keV escapes:

    >>> photon_energy = Kiloelectronvolt(60)
    >>> deposited = Kiloelectronvolt(45)
    >>> escaped = photon_energy - deposited
    >>> escaped
    15 keV

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
    An electron and a positron annihilating at rest produce two photons of
    approximately 0.511 MeV each:

    >>> photon_one = Megaelectronvolt(Decimal("0.511"))
    >>> photon_two = Megaelectronvolt(Decimal("0.511"))
    >>> photon_one + photon_two
    1.022 MeV

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
    A proton and an antiproton have the same rest energy.
    Their combined rest energy is therefore twice the proton rest energy:

    >>> proton = Gigaelectronvolt(Decimal("0.938272088"))
    >>> antiproton = Gigaelectronvolt(Decimal("0.938272088"))
    >>> proton + antiproton
    1.876544176 GeV

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
    A collider operating with two symmetric 6.8 TeV proton beams has a centre-of-mass
    energy of 13.6 TeV:

    >>> beam = Teraelectronvolt(Decimal("6.8"))
    >>> beam + beam
    13.6 TeV

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
    A PeV-scale cosmic neutrino carries 2 PeV.
    Subtracting a 500 TeV component leaves 1.5 PeV attributed to the remaining part of
    the event:

    >>> event_energy = Petaelectronvolt(2)
    >>> secondary_energy = Teraelectronvolt(500)
    >>> event_energy - secondary_energy
    1.5 PeV

    """
    return Energy(to_exact(value) * PETAELECTRONVOLT.scale, PETAELECTRONVOLT)


# Watt times Time.

MILLIWATT_HOUR = UnitDef("milliwatt_hour", "mWh", Decimal("3.6"), ENERGY)
WATT_HOUR = UnitDef("watt_hour", "Wh", Decimal(3600), ENERGY)
KILOWATT_HOUR = UnitDef("kilowatt_hour", "kWh", Decimal(3600000), ENERGY)


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
    A battery test begins with a 1 kWh charge and records three loads:

    >>> battery = KilowattHour(1)
    >>> remaining = battery - WattHour(420) - WattHour(185) - WattHour(95)
    >>> remaining
    0.3 kWh

    """
    return Energy(to_exact(value) * WATT_HOUR.scale, WATT_HOUR)


def KilowattHour(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in kilowatt-hours.

    Parameters
    ----------
    value : Numeric
        Energy magnitude in kilowatt-hours.

    Returns
    -------
    Energy
        Energy represented in kilowatt-hours.

    Examples
    --------
    A 6.5 kWh energy budget is split between two systems, leaving the remainder
    for the propulsion controller:

    >>> budget = KilowattHour(6.5)
    >>> allocated = KilowattHour(2.75) + KilowattHour(1.25)
    >>> reserve = budget - allocated
    >>> reserve
    2.5 kWh

    """
    return Energy(to_exact(value) * KILOWATT_HOUR.scale, KILOWATT_HOUR)


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


# TNT Equivalent.

TONNE_OF_TNT = UnitDef("tonne_of_tnt", "tTNT", Decimal(4184000000), ENERGY)

KILOTONNE_OF_TNT = UnitDef("kilotonne_of_tnt", "ktTNT", Decimal(4184000000000), ENERGY)

MEGATONNE_OF_TNT = UnitDef(
    "megatonne_of_tnt", "MtTNT", Decimal(4184000000000000), ENERGY
)


def TonneOfTNT(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in tonnes of TNT equivalent.

    Parameters
    ----------
    value : Numeric
        Energy magnitude in tonnes of TNT equivalent.

    Returns
    -------
    Energy
        Energy represented in tonnes of TNT equivalent.

    Examples
    --------
    A modeled release contains a 1,200 tonne TNT-equivalent component followed by
    a smaller 800 tonne component:

    >>> first_stage = TonneOfTNT(1200)
    >>> second_stage = TonneOfTNT(800)
    >>> total = first_stage + second_stage
    >>> total
    2000 tTNT

    """
    return Energy(to_exact(value) * TONNE_OF_TNT.scale, TONNE_OF_TNT)


def KilotonneOfTNT(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in kilotonnes of TNT equivalent.

    Parameters
    ----------
    value : Numeric
        Energy magnitude in kilotonnes of TNT equivalent.

    Returns
    -------
    Energy
        Energy represented in kilotonnes of TNT equivalent.

    Examples
    --------
    An impact model assigns 350 kilotonnes of TNT equivalent to atmospheric effects.
    Expressing the same energy on the megatonne scale gives:

    >>> atmospheric = KilotonneOfTNT(350)
    >>> atmospheric.to(MEGATONNE_OF_TNT)
    0.35 MtTNT

    """
    return Energy(to_exact(value) * KILOTONNE_OF_TNT.scale, KILOTONNE_OF_TNT)


def MegatonneOfTNT(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in megatonnes of TNT equivalent.

    Parameters
    ----------
    value : Numeric
        Energy magnitude in megatonnes of TNT equivalent.

    Returns
    -------
    Energy
        Energy represented in megatonnes of TNT equivalent.

    Examples
    --------
    An impact model begins with 2.4 megatonnes of TNT equivalent and subtracts a
    350 kilotonne atmospheric component:

    >>> total = MegatonneOfTNT(2.4)
    >>> atmospheric = KilotonneOfTNT(350)
    >>> remaining = total - atmospheric
    >>> remaining
    2.05 MtTNT

    """
    return Energy(to_exact(value) * MEGATONNE_OF_TNT.scale, MEGATONNE_OF_TNT)


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
        PETAJOULE.symbol: Petajoule,
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
        KILOWATT_HOUR.symbol: KilowattHour,
        ERG.symbol: Erg,
        THERMOCHEMICAL_CALORIE.symbol: ThermochemicalCalorie,
        KILOCALORIE.symbol: Kilocalorie,
        TONNE_OF_TNT.symbol: TonneOfTNT,
        KILOTONNE_OF_TNT.symbol: KilotonneOfTNT,
        MEGATONNE_OF_TNT.symbol: MegatonneOfTNT,
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
    "KILOTONNE_OF_TNT",
    "MEGAELECTRONVOLT",
    "MEGAJOULE",
    "MEGATONNE_OF_TNT",
    "MICROELECTRONVOLT",
    "MICROJOULE",
    "MILLIELECTRONVOLT",
    "MILLIJOULE",
    "MILLIWATT_HOUR",
    "NANOJOULE",
    "PETAELECTRONVOLT",
    "PETAJOULE",
    "PICOJOULE",
    "TERAELECTRONVOLT",
    "TERAJOULE",
    "THERMOCHEMICAL_CALORIE",
    "TONNE_OF_TNT",
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
    "KilotonneOfTNT",
    "Megaelectronvolt",
    "Megajoule",
    "MegatonneOfTNT",
    "Microelectronvolt",
    "Microjoule",
    "Millielectronvolt",
    "Millijoule",
    "MilliwattHour",
    "Nanojoule",
    "Petaelectronvolt",
    "Petajoule",
    "Picojoule",
    "Teraelectronvolt",
    "Terajoule",
    "ThermochemicalCalorie",
    "TonneOfTNT",
    "WattHour",
]
