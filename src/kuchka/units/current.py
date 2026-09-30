"""Current quantities and constructors across practical electrical scales.

`Current` represents the rate at which electric charge passes a point in a circuit.
Its SI unit is the ampere, the SI base unit of electric current.

The constructors in this module provide convenient entry points from picoamperes
through megaamperes.
This range spans semiconductor leakage and precision instrumentation at the small end,
ordinary electronic and electrical loads through the middle, and high-power
experimental and industrial systems at the large end.

All units in this module are exact decimal multiples of the ampere.
A value such as `Milliampere(250)` therefore represents exactly 0.250 A.

Examples
--------
Precision electronic instrumentation can deal with currents measured in picoamperes.
A 250 pA input current is small enough that it matters directly to high-impedance
measurement circuits:

>>> input_bias = Picoampere(250)
>>> input_bias
250 pA

Larger leakage and sensor currents commonly reach the nanoampere range:

>>> leakage = Nanoampere(10)
>>> leakage
10 nA

The conversion between these small scales is exact:

>>> Picoampere(1000) == Nanoampere(1)
True

Ordinary low-power electronics commonly operates in the microampere range.
A precision amplifier with a 600 µA supply current can be represented directly:

>>> amplifier_supply = Microampere(600)
>>> amplifier_supply
600 µA

Digital and analogue circuitry frequently reaches the milliampere range.
A 26 mA circuit current is still the same physical quantity:

>>> circuit_current = Milliampere(26)
>>> circuit_current
26 mA

One thousand milliamperes make exactly one ampere:

>>> Milliampere(1000) == Ampere(1)
True

Ampere-scale currents are ordinary in electrical equipment.
An 8 A load is small compared with a power distribution system but substantial for
electronics:

>>> load_current = Ampere(8)
>>> load_current
8 A

High-power electrical systems reach kiloamperes.
A 3 kA current is used in high-current measurement and power applications:

>>> high_current = Kiloampere(3)
>>> high_current
3 kA

At the extreme end, fusion plasmas can carry currents measured in megaamperes.
A 15 MA current is still represented by the same `Current` quantity:

>>> plasma_current = Megaampere(15)
>>> plasma_current
15 MA

The complete range remains one dimensional quantity.
Changing the prefix does not change the current itself:

>>> Megaampere(1) == Kiloampere(1000)
True

Notes
-----
The ampere is an SI base unit.
Its current definition fixes the numerical value of the elementary charge, linking the
ampere to the coulomb and second.

Current is related to charge and time by

`I = Q / t`.

It is also related to voltage and resistance by Ohm's law:

`I = V / R`.

Those relationships describe different physical quantities;
this module represents current itself and does not encode voltage, charge, or
resistance inside a `Current`.

Metric prefixes represent exact powers of ten.
Consequently, conversions such as

>>> Microampere(1000) == Milliampere(1)
True

and

>>> Kiloampere(1000) == Megaampere(1)
True

hold exactly.

`CURRENT_UNITS` maps symbols such as ``"pA"``, ``"nA"``, ``"µA"``, ``"mA"``, ``"A"``,
``"kA"``, and ``"MA"`` to their constructors.
This is intended for boundary code that receives units as external data, such as
configuration files.

See Also
--------
~kuchka.quantities.Charge
    Electric charge transported by a current.
~kuchka.quantities.Voltage
    Electric potential difference driving current.
~kuchka.quantities.Resistance
    Opposition to current flow.
~kuchka.quantities.Conductance
    Reciprocal of resistance.
~kuchka.quantities.Power
    Rate of energy transfer.

"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import CURRENT
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Current

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


AMPERE_NAME = "ampere"
AMPERE_SYMBOL = "A"

PICOAMPERE = prefixed_unit(prefixes.PICO, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)
NANOAMPERE = prefixed_unit(prefixes.NANO, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)
MICROAMPERE = prefixed_unit(prefixes.MICRO, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)
MILLIAMPERE = prefixed_unit(prefixes.MILLI, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)
AMPERE = prefixed_unit(prefixes.UNIT, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)
KILOAMPERE = prefixed_unit(prefixes.KILO, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)
MEGAAMPERE = prefixed_unit(prefixes.MEGA, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)

Current._canonical_unit = AMPERE  # noqa: SLF001 -- this module owns Current's canonical unit


def Picoampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in picoamperes.

    Parameters
    ----------
    value : Numeric
        Current magnitude in picoamperes.

    Returns
    -------
    Current
        Current represented in picoamperes.

    Examples
    --------
    Precision semiconductor and instrumentation circuits can have input currents in the
    picoampere range:

    >>> input_bias = Picoampere(250)
    >>> input_bias
    250 pA

    One thousand picoamperes make exactly one nanoampere:

    >>> Picoampere(1000) == Nanoampere(1)
    True

    """
    return Current(to_exact(value) * PICOAMPERE.scale, PICOAMPERE)


def Nanoampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in nanoamperes.

    Parameters
    ----------
    value : Numeric
        Current magnitude in nanoamperes.

    Returns
    -------
    Current
        Current represented in nanoamperes.

    Examples
    --------
    Leakage currents and other very small electronic currents can fall in the
    nanoampere range:

    >>> leakage = Nanoampere(10)
    >>> leakage
    10 nA

    One thousand nanoamperes make exactly one microampere:

    >>> Nanoampere(1000) == Microampere(1)
    True

    """
    return Current(to_exact(value) * NANOAMPERE.scale, NANOAMPERE)


def Microampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in microamperes.

    Parameters
    ----------
    value : Numeric
        Current magnitude in microamperes.

    Returns
    -------
    Current
        Current represented in microamperes.

    Examples
    --------
    Low-power electronic circuits commonly operate at currents of a few hundred
    microamperes:

    >>> amplifier_supply = Microampere(600)
    >>> amplifier_supply
    600 µA

    A thousand microamperes make exactly one milliampere:

    >>> Microampere(1000) == Milliampere(1)
    True

    """
    return Current(to_exact(value) * MICROAMPERE.scale, MICROAMPERE)


def Milliampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in milliamperes.

    Parameters
    ----------
    value : Numeric
        Current magnitude in milliamperes.

    Returns
    -------
    Current
        Current represented in milliamperes.

    Examples
    --------
    Milliampere is a natural scale for many electronic circuits.
    A 26 mA circuit current is represented directly:

    >>> circuit_current = Milliampere(26)
    >>> circuit_current
    26 mA

    One thousand milliamperes make exactly one ampere:

    >>> Milliampere(1000) == Ampere(1)
    True

    """
    return Current(to_exact(value) * MILLIAMPERE.scale, MILLIAMPERE)


def Ampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in amperes.

    Parameters
    ----------
    value : Numeric
        Current magnitude in amperes.

    Returns
    -------
    Current
        Current represented in amperes.

    Examples
    --------
    Ampere is the SI base unit for electric current.
    An 8 A load is a substantial current for electronic equipment:

    >>> load_current = Ampere(8)
    >>> load_current
    8 A

    Current may also be negative when a circuit model uses an explicit reference
    direction:

    >>> reverse_current = Ampere(-2)
    >>> reverse_current
    -2 A

    """
    return Current(to_exact(value) * AMPERE.scale, AMPERE)


def Kiloampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in kiloamperes.

    Parameters
    ----------
    value : Numeric
        Current magnitude in kiloamperes.

    Returns
    -------
    Current
        Current represented in kiloamperes.

    Examples
    --------
    High-current electrical systems and precision current measurements can reach the
    kiloampere range:

    >>> high_current = Kiloampere(3)
    >>> high_current
    3 kA

    One thousand kiloamperes make exactly one megaampere:

    >>> Kiloampere(1000) == Megaampere(1)
    True

    """
    return Current(to_exact(value) * KILOAMPERE.scale, KILOAMPERE)


def Megaampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in megaamperes.

    Parameters
    ----------
    value : Numeric
        Current magnitude in megaamperes.

    Returns
    -------
    Current
        Current represented in megaamperes.

    Examples
    --------
    Fusion plasmas can carry currents on the megaampere scale.
    A 15 MA plasma current is represented directly:

    >>> plasma_current = Megaampere(15)
    >>> plasma_current
    15 MA

    One megaampere is exactly one thousand kiloamperes:

    >>> Megaampere(1) == Kiloampere(1000)
    True

    """
    return Current(to_exact(value) * MEGAAMPERE.scale, MEGAAMPERE)


CURRENT_UNITS: Mapping[str, Callable[[Numeric], Current]] = MappingProxyType(
    {
        PICOAMPERE.symbol: Picoampere,
        NANOAMPERE.symbol: Nanoampere,
        MICROAMPERE.symbol: Microampere,
        MILLIAMPERE.symbol: Milliampere,
        AMPERE.symbol: Ampere,
        KILOAMPERE.symbol: Kiloampere,
        MEGAAMPERE.symbol: Megaampere,
    }
)

__all__ = [
    "AMPERE",
    "CURRENT_UNITS",
    "KILOAMPERE",
    "MEGAAMPERE",
    "MICROAMPERE",
    "MILLIAMPERE",
    "NANOAMPERE",
    "PICOAMPERE",
    "Ampere",
    "Kiloampere",
    "Megaampere",
    "Microampere",
    "Milliampere",
    "Nanoampere",
    "Picoampere",
]
