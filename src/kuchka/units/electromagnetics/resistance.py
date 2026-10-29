"""Resistance quantities and constructors for practical electrical engineering.

Resistance describes the opposition to electric current.
Its SI unit is the ohm (Ω), defined by 1 Ω = 1 V/A.
Combining resistance with other electrical quantities lets `kuchka` calculate voltage
drops, currents, power dissipation, and RC time constants without manually tracking
units.

The available prefixes span microohms for precision contacts, milliohms for
current shunts and power connections, ohms and kilohms for ordinary circuits,
and megaohms to gigaohms for high-impedance sensors and insulation testing.
Every prefix is an exact decimal multiple of the ohm.

Examples
--------
During a field inspection, a technician measures a 120 mV voltage drop across
a power connector carrying 300 A. The inferred resistance is 0.4 mΩ, and the
connector dissipates 36 W. That much local heating warrants investigation of
the contact, its fasteners, and its condition:

>>> from kuchka import Ampere, Millivolt
>>> from kuchka.units.electromagnetics.resistance import MILLIOHM
>>> connector_current = Ampere(300)
>>> voltage_drop = Millivolt(120)
>>> contact_resistance = voltage_drop / connector_current
>>> contact_resistance.to(MILLIOHM)
0.4 mΩ
>>> voltage_drop * connector_current
36 W

A signal-conditioning circuit uses a 4.7 kΩ resistor and a 100 nF capacitor.
Their product gives the RC time constant used when estimating the filter's
step response:

>>> from kuchka import Kiloohm, Nanofarad
>>> from kuchka.units.time import MICROSECOND
>>> filter_resistance = Kiloohm(4.7)
>>> filter_capacitance = Nanofarad(100)
>>> (filter_resistance * filter_capacitance).to(MICROSECOND)
470 µs

Notes
-----
For a purely resistive path, resistance and conductance are reciprocals:
R = 1/G. The resistance of a passive resistor is non-negative, although
mathematical models may use negative resistance to describe an active circuit's
negative differential resistance over a particular operating region.

This module represents resistance in ohms and decimal multiples. General AC
impedance is a separate quantity, since it may include reactive contributions.
`Resistance.to_impedance()` and `Resistance.to_reactance()` provide the
corresponding quantity-kind conversions without changing the unit definitions.

`RESISTANCE_UNITS` maps symbols such as ``"µΩ"``, ``"mΩ"``, ``"Ω"``,
``"kΩ"``, ``"MΩ"``, and ``"GΩ"`` to their constructors. It is intended for
boundary code that reads units from configuration files, component databases,
instrument reports, or other external sources.

See Also
--------
~kuchka.quantities.Conductance
    Reciprocal conductance quantities.
~kuchka.quantities.Voltage
    Electric potential difference.
~kuchka.quantities.Current
    Electric current.
~kuchka.quantities.Power
    Rate of energy transfer.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import RESISTANCE
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Resistance

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable


OHM_NAME = "ohm"
OHM_SYMBOL = symbols.OMEGA
OHM_ALIASES = ("ohm", "Ohm")
"""Other symbols for the ohm: what a keyboard gives for the omega."""


MICROOHM = prefixed_unit(
    prefixes.MICRO, OHM_NAME, OHM_SYMBOL, RESISTANCE, base_aliases=OHM_ALIASES
)
MILLIOHM = prefixed_unit(
    prefixes.MILLI, OHM_NAME, OHM_SYMBOL, RESISTANCE, base_aliases=OHM_ALIASES
)
OHM = prefixed_unit(
    prefixes.UNIT, OHM_NAME, OHM_SYMBOL, RESISTANCE, base_aliases=OHM_ALIASES
)
KILOOHM = prefixed_unit(
    prefixes.KILO, OHM_NAME, OHM_SYMBOL, RESISTANCE, base_aliases=OHM_ALIASES
)
MEGAOHM = prefixed_unit(
    prefixes.MEGA, OHM_NAME, OHM_SYMBOL, RESISTANCE, base_aliases=OHM_ALIASES
)
GIGAOHM = prefixed_unit(
    prefixes.GIGA, OHM_NAME, OHM_SYMBOL, RESISTANCE, base_aliases=OHM_ALIASES
)


Resistance._canonical_unit = OHM  # noqa: SLF001 -- this module owns Resistance's canonical unit


def Microohm(value: Numeric) -> Resistance:
    """Construct a resistance from microohms.

    Parameters
    ----------
    value : Numeric
        Resistance in µΩ.

    Returns
    -------
    Resistance
        Resistance represented in microohms.

    Examples
    --------
    A high-current connector has a contact resistance of 250 µΩ and carries 200 A.
    Calculate the voltage drop and the power dissipated at that contact:

    >>> from kuchka import Ampere
    >>> contact = Microohm(250)
    >>> contact_current = Ampere(200)
    >>> contact * contact_current
    0.05 V
    >>> contact * contact_current * contact_current
    10 W

    Ten watts concentrated at a small contact can cause significant heating.
    The actual temperature rise depends on the contact's thermal resistance and the
    surrounding assembly.
    
    """
    return Resistance(to_exact(value) * MICROOHM.scale, MICROOHM)


def Milliohm(value: Numeric) -> Resistance:
    """Construct a resistance from milliohms.

    Parameters
    ----------
    value : Numeric
        Resistance in mΩ.

    Returns
    -------
    Resistance
        Resistance represented in milliohms.

    Examples
    --------
    A 5 mΩ current shunt carries 10 A in a motor controller.
    Its voltage drop produces a measurement signal, while the associated power sets a
    thermal design requirement:

    >>> from kuchka import Ampere
    >>> from kuchka.units.electromagnetics.voltage import MILLIVOLT
    >>> shunt = Milliohm(5)
    >>> shunt_current = Ampere(10)
    >>> (shunt * shunt_current).to(MILLIVOLT)
    50 mV
    >>> shunt * shunt_current * shunt_current
    0.5 W
    """
    return Resistance(to_exact(value) * MILLIOHM.scale, MILLIOHM)


def Ohm(value: Numeric) -> Resistance:
    """Construct a resistance from ohms.

    Parameters
    ----------
    value : Numeric
        Resistance in Ω.

    Returns
    -------
    Resistance
        Resistance represented in ohms.

    Examples
    --------
    A 50 Ω RF termination receives a 1 V RMS signal.
    For a purely resistive load, the RMS current and average power are:

    >>> from kuchka import Volt
    >>> from kuchka.units.electromagnetics.current import MILLIAMPERE
    >>> signal_voltage = Volt(1)
    >>> termination = Ohm(50)
    >>> termination_current = signal_voltage / termination
    >>> termination_current.to(MILLIAMPERE)
    20 mA
    >>> signal_voltage * termination_current
    0.02 W

    This is the load's dissipation for the stated RMS voltage, not the instantaneous
    power at an arbitrary point in the signal waveform.

    Notes
    -----
    Negative resistance values can be useful in mathematical circuit models.
    For example, an active circuit can exhibit negative differential resistance over
    part of its operating curve.
    Such a value does not describe an ordinary passive resistor.
    """
    return Resistance(to_exact(value) * OHM.scale, OHM)


def Kiloohm(value: Numeric) -> Resistance:
    """Construct a resistance from kilohms.

    Parameters
    ----------
    value : Numeric
        Resistance in kΩ.

    Returns
    -------
    Resistance
        Resistance represented in kilohms.

    Examples
    --------
    A 4.7 kΩ resistor drives a 100 nF input capacitor on a sensor interface.
    Calculate the time constant that determines the characteristic settling timescale
    of this first-order RC network:

    >>> from kuchka import Nanofarad
    >>> from kuchka.units.time import MICROSECOND
    >>> source_resistance = Kiloohm(4.7)
    >>> input_capacitance = Nanofarad(100)
    >>> (source_resistance * input_capacitance).to(MICROSECOND)
    470 µs

    The time constant is the product RC.
    The actual settling time depends on the response criterion; reaching approximately
    99% of a step response takes about five time constants.
    """
    return Resistance(to_exact(value) * KILOOHM.scale, KILOOHM)


def Megaohm(value: Numeric) -> Resistance:
    """Construct a resistance from megaohms.

    Parameters
    ----------
    value : Numeric
        Resistance in MΩ.

    Returns
    -------
    Resistance
        Resistance represented in megaohms.

    Examples
    --------
    A high-impedance sensor input has a 10 MΩ bias resistance.
    A leakage current of only 100 nA creates a 1 V error across that resistance:

    >>> from kuchka import Microampere
    >>> input_resistance = Megaohm(10)
    >>> leakage_current = Microampere(0.1)
    >>> input_resistance * leakage_current
    1 V

    This is why contamination, PCB surface leakage, and input bias currents can matter
    in electrometers and other high-impedance measurement circuits.
    """
    return Resistance(to_exact(value) * MEGAOHM.scale, MEGAOHM)


def Gigaohm(value: Numeric) -> Resistance:
    """Construct a resistance from gigaohms.

    Parameters
    ----------
    value : Numeric
        Resistance in GΩ.

    Returns
    -------
    Resistance
        Resistance represented in gigaohms.

    Examples
    --------
    An insulation test applies 500 V across a path measuring 1 GΩ.
    Calculate the leakage current and the power dissipated in the insulation:

    >>> from kuchka import Volt
    >>> from kuchka.units.electromagnetics.current import MICROAMPERE
    >>> test_voltage = Volt(500)
    >>> insulation_resistance = Gigaohm(1)
    >>> leakage_current = test_voltage / insulation_resistance
    >>> leakage_current.to(MICROAMPERE)
    0.5 µA
    >>> test_voltage * leakage_current
    0.00025 W

    This illustrates the electrical consequence of a finite insulation resistance.
    Actual insulation testing must also respect the equipment's rated test voltage and
    safety requirements.
    """
    return Resistance(to_exact(value) * GIGAOHM.scale, GIGAOHM)


RESISTANCE_UNITS: UnitTable[Resistance] = unit_table(
    "RESISTANCE_UNITS",
    {
        MICROOHM: Microohm,
        MILLIOHM: Milliohm,
        OHM: Ohm,
        KILOOHM: Kiloohm,
        MEGAOHM: Megaohm,
        GIGAOHM: Gigaohm,
    },
)

__all__ = [
    "GIGAOHM",
    "KILOOHM",
    "MEGAOHM",
    "MICROOHM",
    "MILLIOHM",
    "OHM",
    "RESISTANCE_UNITS",
    "Gigaohm",
    "Kiloohm",
    "Megaohm",
    "Microohm",
    "Milliohm",
    "Ohm",
]
