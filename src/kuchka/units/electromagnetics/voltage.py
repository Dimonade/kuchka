"""Voltage constructors: the volt, from nanovolts to petavolts.

`Voltage` represents electric potential difference.
The volt is the canonical SI unit, and the constructors in this module provide
convenient entry points from SI decimal prefixes spanning sub-microvolt signals to
extreme high-energy potentials.

All units in this module are exact decimal multiples of the volt.
There are no measurement constants or empirical conversion factors involved:
an input such as `Millivolt(700)` represents exactly 0.700 V.

Voltage may be positive or negative.
The sign represents polarity or direction of the potential difference and is part of
the magnitude stored by the quantity.

Examples
--------
Voltage occurs across an unusually wide range of engineering and physical systems.

A very small biological signal can be only a few microvolts:

>>> eeg_signal = Microvolt(2)
>>> eeg_signal
2 µV

A 700 mV forward drop is representative of a conventional silicon diode:

>>> diode_drop = Millivolt(700)
>>> diode_drop
700 mV

Digital electronics commonly works at a handful of volts:

>>> logic_supply = Volt(5)
>>> logic_supply
5 V

The same quantity naturally describes automotive and industrial supplies:

>>> vehicle_supply = Volt(12)
>>> vehicle_supply
12 V

High-voltage equipment moves into the kilovolt range.
A 15 kV supply is also the nominal voltage used by some AC railway electrification
systems:

>>> railway_supply = Kilovolt(15)
>>> railway_supply
15 kV

Conversion between scales is exact:

>>> Kilovolt(15) == Volt(15_000)
True

Negative voltage is no different from positive voltage as far as dimensional
correctness is concerned.
It simply records the opposite polarity:

>>> reverse_bias = Volt(-5)
>>> reverse_bias
-5 V

Voltage differences can be combined when they describe differences between the same
pair of electrical nodes.
For example, removing a 700 mV drop from a 5 V supply leaves:

>>> available = Volt(5) - Millivolt(700)
>>> available
4.3 V

The constructors also make order-of-magnitude changes explicit.
One thousand microvolts is exactly one millivolt:

>>> Microvolt(1000) == Millivolt(1)
True

Notes
-----
The volt is the SI derived unit of electric potential difference:

`1 V = 1 J / C = 1 W / A`.

Metric prefixes represent exact powers of ten.
Consequently, conversions such as

>>> Millivolt(1000) == Volt(1)
True

and

>>> Megavolt(1) == Volt(1_000_000)
True

hold exactly.

`VOLTAGE_UNITS` maps symbols such as ``"µV"``, ``"mV"``, ``"V"``, and ``"kV"`` to their
constructors.
This is intended for boundary code such as parsed configuration files, where the unit
arrives as data.

See Also
--------
~kuchka.quantities.Current
    Electric current quantities.
~kuchka.quantities.Power
    Rate of energy transfer.
~kuchka.quantities.Resistance
    Electrical resistance quantities.
~kuchka.quantities.Charge
    Electric charge quantities related to current and time.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import VOLTAGE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Voltage

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.quantities import UnitDef

VOLT_NAME = "volt"
VOLT_SYMBOL = "V"

NANOVOLT = prefixed_unit(prefixes.NANO, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)
MICROVOLT = prefixed_unit(prefixes.MICRO, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)
MILLIVOLT = prefixed_unit(prefixes.MILLI, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)
VOLT = prefixed_unit(prefixes.UNIT, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)
KILOVOLT = prefixed_unit(prefixes.KILO, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)
MEGAVOLT = prefixed_unit(prefixes.MEGA, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)
PETAVOLT = prefixed_unit(prefixes.PETA, VOLT_NAME, VOLT_SYMBOL, VOLTAGE)


Voltage._canonical_unit = VOLT  # noqa: SLF001 -- this module owns Voltage's canonical unit


def Nanovolt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in nanovolts.

    Parameters
    ----------
    value : Numeric
        Voltage magnitude in nanovolts.

    Returns
    -------
    Voltage
        Voltage represented in nanovolts.

    Examples
    --------
    Extremely small electrical signals can fall into the nanovolt range.
    Change in nerve cell potential caused by a single acetylcholine receptor channel is
    around 500 nV:

    >>> v_diff = Nanovolt(500)
    >>> v_diff
    500 nV

    The same potential difference expressed in microvolts is exactly equal:

    >>> Nanovolt(500) == Microvolt(0.5)
    True

    """
    return Voltage(to_exact(value) * NANOVOLT.scale, NANOVOLT)


def Microvolt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in microvolts.

    Parameters
    ----------
    value : Numeric
        Voltage magnitude in microvolts.

    Returns
    -------
    Voltage
        Voltage represented in microvolts.

    Examples
    --------
    Biological electrical signals are commonly measured on the microvolt scale.
    An EEG signal of 2 µV can be represented directly:

    >>> eeg_signal = Microvolt(2)
    >>> eeg_signal
    2 µV

    A thousand microvolts make exactly one millivolt:

    >>> Microvolt(1000) == Millivolt(1)
    True

    """
    return Voltage(to_exact(value) * MICROVOLT.scale, MICROVOLT)


def Millivolt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in millivolts.

    Parameters
    ----------
    value : Numeric
        Voltage magnitude in millivolts.

    Returns
    -------
    Voltage
        Voltage represented in millivolts.

    Examples
    --------
    A conventional silicon diode may have a forward voltage of roughly 700 mV:

    >>> diode_drop = Millivolt(700)
    >>> diode_drop
    700 mV

    A K-type thermocouple can produce only a few millivolts under ordinary temperature
    differences:

    >>> thermocouple_signal = Millivolt(2)
    >>> thermocouple_signal
    2 mV

    The scale conversion is exact:

    >>> Millivolt(1000) == Volt(1)
    True

    """
    return Voltage(to_exact(value) * MILLIVOLT.scale, MILLIVOLT)


def Volt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in volts.

    Parameters
    ----------
    value : Numeric
        Voltage magnitude in volts.

    Returns
    -------
    Voltage
        Voltage represented in volts.

    Examples
    --------
    Five volts remains one of the most recognizable supply levels in electronics:

    >>> logic_supply = Volt(5)
    >>> logic_supply
    5 V

    Battery-powered systems commonly use much smaller nominal voltages.
    A single alkaline cell is approximately 1.5 V:

    >>> battery_cell = Volt(1.5)
    >>> battery_cell
    1.5 V

    Voltage may be negative when the potential difference has the opposite polarity:

    >>> reverse_bias = Volt(-5)
    >>> reverse_bias
    -5 V

    """
    return Voltage(to_exact(value) * VOLT.scale, VOLT)


def Kilovolt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in kilovolts.

    Parameters
    ----------
    value : Numeric
        Voltage magnitude in kilovolts.

    Returns
    -------
    Voltage
        Voltage represented in kilovolts.

    Examples
    --------
    High-voltage railway electrification commonly reaches the kilovolt range.
    A 15 kV supply is a useful example:

    >>> railway_supply = Kilovolt(15)
    >>> railway_supply
    15 kV

    Air breakdown requires roughly 3 kV per millimetre under ordinary atmospheric
    conditions, making kilovolts relevant even to a tiny gap:

    >>> arc_voltage = Kilovolt(3)
    >>> arc_voltage
    3 kV

    One kilovolt is exactly one thousand volts:

    >>> Kilovolt(1) == Volt(1000)
    True

    """
    return Voltage(to_exact(value) * KILOVOLT.scale, KILOVOLT)


def Megavolt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in megavolts.

    Parameters
    ----------
    value : Numeric
        Voltage magnitude in megavolts.

    Returns
    -------
    Voltage
        Voltage represented in megavolts.

    Examples
    --------
    Particle-physics and electron-optics equipment can operate at megavolt-scale
    accelerating potentials:

    >>> accelerating_voltage = Megavolt(3)
    >>> accelerating_voltage
    3 MV

    The conversion to volts is exact:

    >>> Megavolt(1) == Volt(1_000_000)
    True

    """
    return Voltage(to_exact(value) * MEGAVOLT.scale, MEGAVOLT)


def Petavolt(value: Numeric) -> Voltage:
    """Construct a Voltage from a magnitude expressed in petavolts.

    Parameters
    ----------
    value : Numeric
        Voltage magnitude in petavolts.

    Returns
    -------
    Voltage
        Voltage represented in petavolts.

    Examples
    --------
    Petavolt represents a physical scale far beyond ordinary engineering.
    It is the scale of voltage encountered around a particular energetic highly
    magnetised rotating neutron star:

    >>> extreme_potential = Petavolt(7)
    >>> extreme_potential
    7 PV

    """
    return Voltage(to_exact(value) * PETAVOLT.scale, PETAVOLT)


VOLTAGE_UNITS: Mapping[str, Callable[[Numeric], Voltage]] = unit_table(
    "VOLTAGE_UNITS",
    {
        NANOVOLT: Nanovolt,
        MICROVOLT: Microvolt,
        MILLIVOLT: Millivolt,
        VOLT: Volt,
        KILOVOLT: Kilovolt,
        MEGAVOLT: Megavolt,
        PETAVOLT: Petavolt,
    },
)

VOLTAGE_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        NANOVOLT,
        MICROVOLT,
        MILLIVOLT,
        VOLT,
        KILOVOLT,
        MEGAVOLT,
        PETAVOLT,
    ),
)
"""The units `auto_scale` moves a voltage along, smallest first."""

__all__ = [
    "KILOVOLT",
    "MEGAVOLT",
    "MICROVOLT",
    "MILLIVOLT",
    "NANOVOLT",
    "PETAVOLT",
    "VOLT",
    "VOLTAGE_LADDERS",
    "VOLTAGE_UNITS",
    "Kilovolt",
    "Megavolt",
    "Microvolt",
    "Millivolt",
    "Nanovolt",
    "Petavolt",
    "Volt",
]
