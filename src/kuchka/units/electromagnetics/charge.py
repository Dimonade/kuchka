"""Electric charge constructors: coulombs and ampere-hours.

The coulomb (C) is the SI unit of electric charge: 1 C = 1 A·s.
Charge is the time integral of electric current.
For a constant current, Q = It; for a capacitor, Q = CV.
Multiplying charge by voltage gives energy, while dividing charge by current gives the
time required to transfer that charge.

The useful scale depends on the application.
Picocoulombs describe small sensor and detector signals; nanocoulombs and microcoulombs
appear in electrostatic actuators, pulse measurements, and charge-sensitive
electronics.
Millicoulombs and coulombs suit larger current pulses and capacitor banks.
Ampere-seconds express integrated current directly, while milliampere-hours and
ampere-hours are common ways to specify battery capacity.

Examples
--------
A remote environmental sensor draws 18 mA during a 240 ms measurement burst.
It takes one measurement each minute.
Calculate the charge used in one burst and the total charge accumulated over a day,
counting only the measurement bursts and excluding the device's idle consumption:

>>> from kuchka import Milliampere, Millisecond
>>> from kuchka.units.electromagnetics.charge import COULOMB, MILLICOULOMB
>>> burst_current = Milliampere(18)
>>> burst_duration = Millisecond(240)
>>> burst_charge = burst_current * burst_duration
>>> burst_charge.to(MILLICOULOMB)
4.32 mC
>>> (burst_charge * 1440).to(COULOMB)
6.2208 C

Notes
-----
Ampere-hour units express charge, not energy.
Comparing battery capacities in ampere-hours is meaningful when the nominal voltages
are comparable; estimating stored energy also requires voltage information.
Actual battery runtime depends on discharge rate, temperature, cell chemistry, cutoff
voltage, and conversion losses.

For radiographic equipment, the mAs quantity is the product of tube current and
exposure time.
It helps describe the charge transported through the tube, but it is not by itself a
measure of absorbed radiation dose.

`CHARGE_UNITS` maps symbols such as ``"pC"``, ``"nC"``, ``"µC"``, ``"mC"``, ``"C"``,
``"mAs"``, ``"mAh"``, and ``"Ah"`` to their constructors.
It is intended for boundary code that reads a charge unit from configuration files,
instrument reports, battery specifications, and other external sources.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import CHARGE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Charge
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

COULOMB_NAME = "coulomb"
COULOMB_SYMBOL = "C"

PICOCOULOMB = prefixed_unit(prefixes.PICO, COULOMB_NAME, COULOMB_SYMBOL, CHARGE)
NANOCOULOMB = prefixed_unit(prefixes.NANO, COULOMB_NAME, COULOMB_SYMBOL, CHARGE)
MICROCOULOMB = prefixed_unit(prefixes.MICRO, COULOMB_NAME, COULOMB_SYMBOL, CHARGE)
MILLICOULOMB = prefixed_unit(prefixes.MILLI, COULOMB_NAME, COULOMB_SYMBOL, CHARGE)
COULOMB = prefixed_unit(
    prefixes.UNIT,
    COULOMB_NAME,
    COULOMB_SYMBOL,
    CHARGE,
    aliases=("As", "A·s", "A*s"),
    words=("ampere second", "ampere-second"),
)

Charge._canonical_unit = COULOMB  # noqa: SLF001 -- this module owns Charge's canonical unit


def Picocoulomb(value: Numeric) -> Charge:
    """Construct electric charge from picocoulombs.

    Parameters
    ----------
    value : Numeric
        Electric charge in pC.

    Returns
    -------
    Charge
        Charge represented in picocoulombs.

    Examples
    --------
    A charge-sensitive detector transfers 8 pC to a 20 pF input capacitor.
    Calculate the resulting voltage change across the input capacitance:

    >>> from kuchka import Picocoulomb, Picofarad
    >>> detector_charge = Picocoulomb(8)
    >>> input_capacitance = Picofarad(20)
    >>> detector_charge / input_capacitance
    0.4 V

    The calculation uses the magnitude of the charge transfer; signal polarity depends
    on the detector and amplifier configuration.

    """
    return Charge(to_exact(value) * PICOCOULOMB.scale, PICOCOULOMB)


def Nanocoulomb(value: Numeric) -> Charge:
    """Construct electric charge from nanocoulombs.

    Parameters
    ----------
    value : Numeric
        Electric charge in nC.

    Returns
    -------
    Charge
        Charge represented in nanocoulombs.

    Examples
    --------
    An electrostatic actuator transfers 3 nC over a 2 ms pulse.
    Determine the average current during that interval:

    >>> from kuchka import Millisecond, Nanocoulomb
    >>> from kuchka.units import MICROAMPERE
    >>> transferred_charge = Nanocoulomb(3)
    >>> pulse_duration = Millisecond(2)
    >>> (transferred_charge / pulse_duration).to(MICROAMPERE)
    1.5 µA

    """
    return Charge(to_exact(value) * NANOCOULOMB.scale, NANOCOULOMB)


def Microcoulomb(value: Numeric) -> Charge:
    """Construct electric charge from microcoulombs.

    Parameters
    ----------
    value : Numeric
        Electric charge in µC.

    Returns
    -------
    Charge
        Charge represented in microcoulombs.

    Examples
    --------
    A piezoelectric test fixture transfers 18 µC to a 3 µF integration capacitor during
    a mechanical impact.
    Calculate the voltage change:

    >>> from kuchka import Microcoulomb, Microfarad
    >>> transferred_charge = Microcoulomb(18)
    >>> integration_capacitor = Microfarad(3)
    >>> transferred_charge / integration_capacitor
    6 V

    The result assumes that the transferred charge is stored on the stated capacitance;
    the mechanics of a real piezoelectric sensor determine how much charge is produced.

    """
    return Charge(to_exact(value) * MICROCOULOMB.scale, MICROCOULOMB)


def Millicoulomb(value: Numeric) -> Charge:
    """Construct electric charge from millicoulombs.

    Parameters
    ----------
    value : Numeric
        Electric charge in mC.

    Returns
    -------
    Charge
        Charge represented in millicoulombs.

    Examples
    --------
    A pulsed solenoid transfers 20 mC over an 8 ms current pulse.
    Calculate the average current during the pulse:

    >>> from kuchka import Millicoulomb, Millisecond
    >>> transferred_charge = Millicoulomb(20)
    >>> pulse_duration = Millisecond(8)
    >>> transferred_charge / pulse_duration
    2.5 A

    This is the time-averaged current over the pulse interval; a shaped pulse can have
    a different peak current.

    """
    return Charge(to_exact(value) * MILLICOULOMB.scale, MILLICOULOMB)


def Coulomb(value: Numeric) -> Charge:
    """Construct electric charge from coulombs.

    Parameters
    ----------
    value : Numeric
        Electric charge in C.

    Returns
    -------
    Charge
        Charge represented in coulombs.

    Examples
    --------
    A pulse-power test fixture stores 0.2 C on a capacitor charged to 2 kV.
    For a capacitor charged from zero, the stored energy is QV/2:

    >>> from kuchka import Coulomb, Volt
    >>> capacitor_charge = Coulomb(0.2)
    >>> charging_voltage = Volt(2000)
    >>> capacitor_charge * charging_voltage / 2
    200 J

    This describes stored electrical energy, not the energy necessarily delivered to a
    load during a discharge.

    """
    return Charge(to_exact(value) * COULOMB.scale, COULOMB)


# Ampere multiplied by time is charge.


MILLIAMPERE_SECOND = UnitDef("milliampere_second", "mAs", Decimal("0.001"), CHARGE)
MILLIAMPERE_HOUR = UnitDef("milliampere_hour", "mAh", Decimal("3.6"), CHARGE)
AMPERE_HOUR = UnitDef("ampere_hour", "Ah", Decimal(3600), CHARGE)

AmpereSecond = Coulomb
"""An ampere-second is exactly one coulomb."""


def MilliampereSecond(value: Numeric) -> Charge:
    """Construct electric charge from milliampere-seconds.

    Parameters
    ----------
    value : Numeric
        Charge in mAs, the product of current in milliamperes and time in seconds.

    Returns
    -------
    Charge
        Charge represented in milliampere-seconds.

    Examples
    --------
    An X-ray tube operates at 200 mA for an exposure lasting 100 ms.
    Calculate the tube charge, a commonly specified radiographic technique factor:

    >>> from kuchka import Milliampere, Millisecond
    >>> tube_current = Milliampere(200)
    >>> exposure_time = Millisecond(100)
    >>> tube_charge = tube_current * exposure_time
    >>> tube_charge.to(MILLIAMPERE_SECOND)
    20 mAs
    >>> tube_charge.to(COULOMB)
    0.02 C

    The mAs value describes electrical charge through the tube; radiation dose also
    depends on tube voltage, filtration, geometry, and other factors.

    """
    return Charge(to_exact(value) * MILLIAMPERE_SECOND.scale, MILLIAMPERE_SECOND)


def MilliampereHour(value: Numeric) -> Charge:
    """Construct electric charge from milliampere-hours.

    Parameters
    ----------
    value : Numeric
        Battery capacity in mAh.

    Returns
    -------
    Charge
        Charge represented in milliampere-hours.

    Examples
    --------
    A battery rated at 3000 mAh powers a device drawing a steady 150 mA.
    Estimate the operating time from the rated capacity:

    >>> from kuchka import Milliampere, MilliampereHour
    >>> from kuchka.units import HOUR
    >>> battery_capacity = MilliampereHour(3000)
    >>> device_current = Milliampere(150)
    >>> (battery_capacity / device_current).to(HOUR)
    20 h

    This is a capacity-based estimate.
    Real runtime varies with discharge conditions, battery ageing, and the device's
    cutoff voltage.

    """
    return Charge(to_exact(value) * MILLIAMPERE_HOUR.scale, MILLIAMPERE_HOUR)


def AmpereHour(value: Numeric) -> Charge:
    """Construct electric charge from ampere-hours.

    Parameters
    ----------
    value : Numeric
        Battery capacity in Ah.

    Returns
    -------
    Charge
        Charge represented in ampere-hours.

    Examples
    --------
    A field robot uses a 48 V battery rated at 60 Ah.
    Multiplying its nominal voltage by its charge capacity estimates the nominal stored
    energy:

    >>> from kuchka import AmpereHour, Volt
    >>> from kuchka.units import KILOWATT_HOUR
    >>> battery_capacity = AmpereHour(60)
    >>> nominal_voltage = Volt(48)
    >>> (battery_capacity * nominal_voltage).to(KILOWATT_HOUR)
    2.88 kWh

    Actual battery energy depends on voltage throughout the discharge cycle;
    multiplying rated ampere-hours by nominal voltage is an estimate.

    """
    return Charge(to_exact(value) * AMPERE_HOUR.scale, AMPERE_HOUR)


CHARGE_UNITS: Mapping[str, Callable[[Numeric], Charge]] = unit_table(
    "CHARGE_UNITS",
    {
        PICOCOULOMB: Picocoulomb,
        NANOCOULOMB: Nanocoulomb,
        MICROCOULOMB: Microcoulomb,
        MILLICOULOMB: Millicoulomb,
        COULOMB: Coulomb,
        MILLIAMPERE_SECOND: MilliampereSecond,
        MILLIAMPERE_HOUR: MilliampereHour,
        AMPERE_HOUR: AmpereHour,
    },
)

__all__ = [
    "AMPERE_HOUR",
    "CHARGE_UNITS",
    "COULOMB",
    "MICROCOULOMB",
    "MILLIAMPERE_HOUR",
    "MILLIAMPERE_SECOND",
    "MILLICOULOMB",
    "NANOCOULOMB",
    "PICOCOULOMB",
    "AmpereHour",
    "AmpereSecond",
    "Coulomb",
    "Microcoulomb",
    "MilliampereHour",
    "MilliampereSecond",
    "Millicoulomb",
    "Nanocoulomb",
    "Picocoulomb",
]
