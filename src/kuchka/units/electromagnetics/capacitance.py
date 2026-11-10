"""Capacitance constructors: the farad, from femtofarads to kilofarads.

The farad (F) is the SI unit of capacitance: 1 F = 1 C/V.
Capacitance relates the charge stored on a component to the voltage across it, Q = CV.
For a capacitor with constant capacitance, the stored electric-field energy is
E = ½CV², and a changing voltage draws current according to I = C dV/dt.

Capacitance spans a wide range of applications.
Femtofarads describe tiny parasitics in semiconductor circuits; picofarads appear in RF
networks and sensor electrodes; nanofarads and microfarads are common in signal
conditioning and power electronics.
Millifarads and farads are useful for energy storage, while kilofarads can describe
large capacitor banks or explicitly fictional systems.

Examples
--------
An input filter uses a 47 Ω resistor and a 100 nF capacitor.
Its RC time constant sets the characteristic timescale of the filter response:

>>> from kuchka import Nanofarad, Ohm
>>> from kuchka.units import MICROSECOND
>>> filter_resistor = Ohm(47)
>>> bypass_capacitor = Nanofarad(100)
>>> time_constant = filter_resistor * bypass_capacitor
>>> time_constant.to(MICROSECOND)
4.7 µs

A camera flash charges a 1200 µF capacitor to 330 V.
The charge and stored energy determine the electrical energy available for a flash:

>>> from kuchka import Microfarad, Volt
>>> flash_capacitor = Microfarad(1200)
>>> charging_voltage = Volt(330)
>>> stored_charge = flash_capacitor * charging_voltage
>>> stored_charge
0.396 C
>>> stored_energy = stored_charge * charging_voltage / 2
>>> stored_energy
65.34 J

Notes
-----
The energy equation E = ½CV² assumes capacitance remains constant over the voltage
range.
Real capacitors also have voltage ratings, leakage, equivalent series resistance, and
other parasitic effects.
For a capacitor supplying a load, usable energy depends on the permitted voltage range,
and runtime also depends on the load and conversion efficiency.

`CAPACITANCE_UNITS` maps symbols such as ``"fF"``, ``"pF"``, ``"nF"``,
``"µF"``, ``"mF"``, ``"F"``, and ``"kF"`` to their constructors. It is intended
for boundary code that reads measurements from configuration files, component
databases, circuit simulations, or instruments.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import CAPACITANCE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Capacitance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

FARAD_NAME = "farad"
FARAD_SYMBOL = "F"

FEMTOFARAD = prefixed_unit(prefixes.FEMTO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
PICOFARAD = prefixed_unit(prefixes.PICO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
NANOFARAD = prefixed_unit(prefixes.NANO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
MICROFARAD = prefixed_unit(prefixes.MICRO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
MILLIFARAD = prefixed_unit(prefixes.MILLI, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
FARAD = prefixed_unit(prefixes.UNIT, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
KILOFARAD = prefixed_unit(prefixes.KILO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)

Capacitance._canonical_unit = FARAD  # noqa: SLF001 -- this module owns Capacitance's canonical unit


def Femtofarad(value: Numeric) -> Capacitance:
    """Construct a capacitance from femtofarads.

    Parameters
    ----------
    value : Numeric
        Capacitance in fF.

    Returns
    -------
    Capacitance
        Capacitance represented in femtofarads.

    Examples
    --------
    A tiny semiconductor input has 20 fF of capacitance.
    Charging it through a voltage change of 0.8 V requires 16 fC of charge:

    >>> from kuchka import Femtofarad, Volt
    >>> from kuchka.units import PICOCOULOMB
    >>> gate_capacitance = Femtofarad(20)
    >>> logic_high = Volt(0.8)
    >>> gate_charge = gate_capacitance * logic_high
    >>> gate_charge.to(PICOCOULOMB)
    0.016 pC

    """
    return Capacitance(to_exact(value) * FEMTOFARAD.scale, FEMTOFARAD)


def Picofarad(value: Numeric) -> Capacitance:
    """Construct a capacitance from picofarads.

    Parameters
    ----------
    value : Numeric
        Capacitance in pF.

    Returns
    -------
    Capacitance
        Capacitance represented in picofarads.

    Examples
    --------
    A 47 pF capacitive sensor electrode is biased at 3.3 V.
    Its stored charge determines the charge that must move during a full voltage
    transition:

    >>> from kuchka import Picofarad, Volt
    >>> from kuchka.units import PICOCOULOMB
    >>> electrode = Picofarad(47)
    >>> bias_voltage = Volt(3.3)
    >>> electrode_charge = electrode * bias_voltage
    >>> electrode_charge.to(PICOCOULOMB)
    155.1 pC

    """
    return Capacitance(to_exact(value) * PICOFARAD.scale, PICOFARAD)


def Nanofarad(value: Numeric) -> Capacitance:
    """Construct a capacitance from nanofarads.

    Parameters
    ----------
    value : Numeric
        Capacitance in nF.

    Returns
    -------
    Capacitance
        Capacitance represented in nanofarads.

    Examples
    --------
    A 1 nF capacitor sees a voltage ramp of 12 V over 500 ns.
    The resulting capacitive current during the ramp is 24 mA:

    >>> from kuchka import Ampere, Nanofarad, Nanosecond, Volt
    >>> from kuchka.units import MILLIAMPERE
    >>> ramp_capacitor = Nanofarad(1)
    >>> voltage_change = Volt(12)
    >>> ramp_duration = Nanosecond(500)
    >>> ramp_current = ramp_capacitor * voltage_change / ramp_duration
    >>> ramp_current.to(MILLIAMPERE)
    24 mA

    """
    return Capacitance(to_exact(value) * NANOFARAD.scale, NANOFARAD)


def Microfarad(value: Numeric) -> Capacitance:
    """Construct a capacitance from microfarads.

    Parameters
    ----------
    value : Numeric
        Capacitance in µF.

    Returns
    -------
    Capacitance
        Capacitance represented in microfarads.

    Examples
    --------
    A 10 µF capacitor in a piezoelectric actuator driver is charged to 24 V.
    Calculate the charge stored and the energy available for the voltage pulse:

    >>> from kuchka import Microfarad, Volt
    >>> from kuchka.units import MICROCOULOMB
    >>> actuator_capacitor = Microfarad(10)
    >>> driver_voltage = Volt(24)
    >>> actuator_charge = actuator_capacitor * driver_voltage
    >>> actuator_charge.to(MICROCOULOMB)
    240 µC
    >>> pulse_energy = actuator_charge * driver_voltage / 2
    >>> pulse_energy
    0.00288 J

    """
    return Capacitance(to_exact(value) * MICROFARAD.scale, MICROFARAD)


def Millifarad(value: Numeric) -> Capacitance:
    """Construct a capacitance from millifarads.

    Parameters
    ----------
    value : Numeric
        Capacitance in mF.

    Returns
    -------
    Capacitance
        Capacitance represented in millifarads.

    Examples
    --------
    A 1500 mF supercapacitor supplies a small controller while its voltage falls from
    5 V to a 3 V cutoff.
    The energy available over that voltage range is 12 J:

    >>> from kuchka import Millifarad, Volt
    >>> hold_up_capacitor = Millifarad(1500)
    >>> charged_voltage = Volt(5)
    >>> cutoff_voltage = Volt(3)
    >>> charge_at_start = hold_up_capacitor * charged_voltage
    >>> charge_at_cutoff = hold_up_capacitor * cutoff_voltage
    >>> available_energy = (
    ...     charge_at_start * charged_voltage
    ...     - charge_at_cutoff * cutoff_voltage
    ... ) / 2
    >>> available_energy
    12 J

    """
    return Capacitance(to_exact(value) * MILLIFARAD.scale, MILLIFARAD)


def Farad(value: Numeric) -> Capacitance:
    """Construct a capacitance from farads.

    Parameters
    ----------
    value : Numeric
        Capacitance in F.

    Returns
    -------
    Capacitance
        Capacitance represented in farads.

    Examples
    --------
    A 2 F backup capacitor powers a 100 mA load while its voltage drops from 5 V to
    3 V.
    Assuming constant load current, it can sustain the load for 40 seconds:

    >>> from kuchka import Ampere, Farad, Volt
    >>> from kuchka.units import SECOND
    >>> backup_capacitor = Farad(2)
    >>> voltage_drop = Volt(5) - Volt(3)
    >>> available_charge = backup_capacitor * voltage_drop
    >>> load_current = Ampere(0.1)
    >>> hold_up_time = available_charge / load_current
    >>> hold_up_time.to(SECOND)
    40 s

    """
    return Capacitance(to_exact(value) * FARAD.scale, FARAD)


def Kilofarad(value: Numeric) -> Capacitance:
    """Construct a capacitance from kilofarads.

    Parameters
    ----------
    value : Numeric
        Capacitance in kF.

    Returns
    -------
    Capacitance
        Capacitance represented in kilofarads.

    Notes
    -----
    Kilofarad-scale banks can store substantial energy.
    The example below is fictional and describes an emergency buffer aboard a
    spacecraft.

    Examples
    --------
    A spacecraft's emergency buffer is rated at 2 kF and charged to 48 V.
    Using its full stored energy, estimate how long it can support a 20 kW emergency
    winch, ignoring conversion losses and the winch's minimum operating voltage:

    >>> from kuchka import Kilofarad, Volt, Watt
    >>> emergency_buffer = Kilofarad(2)
    >>> charged_voltage = Volt(48)
    >>> stored_charge = emergency_buffer * charged_voltage
    >>> stored_energy = stored_charge * charged_voltage / 2
    >>> winch_power = Watt(20_000)
    >>> stored_energy / winch_power
    115.2 s

    """
    return Capacitance(to_exact(value) * KILOFARAD.scale, KILOFARAD)


CAPACITANCE_UNITS: Mapping[str, Callable[[Numeric], Capacitance]] = unit_table(
    "CAPACITANCE_UNITS",
    {
        FEMTOFARAD: Femtofarad,
        PICOFARAD: Picofarad,
        NANOFARAD: Nanofarad,
        MICROFARAD: Microfarad,
        MILLIFARAD: Millifarad,
        FARAD: Farad,
        KILOFARAD: Kilofarad,
    },
)

__all__ = [
    "CAPACITANCE_UNITS",
    "FARAD",
    "FEMTOFARAD",
    "KILOFARAD",
    "MICROFARAD",
    "MILLIFARAD",
    "NANOFARAD",
    "PICOFARAD",
    "Farad",
    "Femtofarad",
    "Kilofarad",
    "Microfarad",
    "Millifarad",
    "Nanofarad",
    "Picofarad",
]
