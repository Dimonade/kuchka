"""Resistance quantities and constructors for practical electrical scales.

`Resistance` represents opposition to electric current.
Its SI unit is the ohm, defined by the relationship

`1 Ω = 1 V / A`.

The constructors in this module provide convenient entry points from SI decimal
prefixes spanning very low-resistance power paths through ordinary electronic
components and into high-resistance leakage and insulation measurements.

All units in this module are exact decimal multiples of the ohm.
A value such as `Kiloohm(4.7)` therefore represents exactly 4.7 kΩ, not a measured or
rounded approximation.

Examples
--------
A very low resistance is characteristic of high-current conductors and measurement
shunts.
A 5 mΩ current-sense resistor is small in resistance but still large enough to produce
a measurable voltage drop:

>>> shunt = Milliohm(5)
>>> shunt
5 mΩ

Precision contacts and interconnects can be measured in microohms:

>>> contact_resistance = Microohm(250)
>>> contact_resistance
250 µΩ

The same resistance can be expressed at any supported scale without changing its
physical meaning:

>>> Microohm(250) == Milliohm(0.25)
True

Ordinary electronic resistors occupy the ohm to kilohm range.
A familiar 4.7 kΩ resistor is represented directly:

>>> bias_resistor = Kiloohm(4.7)
>>> bias_resistor
4.7 kΩ

Larger values are common where a circuit needs to draw very little current.
A 1 MΩ resistor is still exactly the same `Resistance` quantity:

>>> high_value_resistor = Megaohm(1)
>>> high_value_resistor
1 MΩ

The conversion between kilohms and megaohms is exact:

>>> Kiloohm(1000) == Megaohm(1)
True

At the high end, gigaohm resistances are useful for describing very small leakage paths
and high-resistance insulation:

>>> insulation = Gigaohm(1)
>>> insulation
1 GΩ

A resistance quantity also naturally represents zero and negative values
mathematically, although a physical passive resistor normally has a non-negative
resistance:

>>> zero_resistance = Ohm(0)
>>> zero_resistance
0 Ω

Notes
-----
Resistance and conductance are reciprocal quantities:

`R = 1 / G`

for a purely resistive path. Consequently, resistance and conductance use
inverse units:

`1 Ω = 1 S⁻¹`.

This module represents resistance in ohms and its SI decimal prefixes.
It does not represent impedance of a general AC circuit; impedance may contain a
reactive component and is a separate physical quantity.

Metric prefixes represent exact powers of ten.
Consequently, conversions such as

>>> Milliohm(1000) == Ohm(1)
True

and

>>> Megaohm(1) == Ohm(1_000_000)
True

hold exactly.

`RESISTANCE_UNITS` maps symbols such as ``"mΩ"``, ``"Ω"``, ``"kΩ"``, and ``"MΩ"`` to
their constructors.
This is intended for boundary code that receives units as external data, such as
configuration files.

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

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import RESISTANCE
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Resistance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


OHM_NAME = "ohm"
OHM_SYMBOL = symbols.OMEGA


MICROOHM = prefixed_unit(prefixes.MICRO, OHM_NAME, OHM_SYMBOL, RESISTANCE)
MILLIOHM = prefixed_unit(prefixes.MILLI, OHM_NAME, OHM_SYMBOL, RESISTANCE)
OHM = prefixed_unit(prefixes.UNIT, OHM_NAME, OHM_SYMBOL, RESISTANCE)
KILOOHM = prefixed_unit(prefixes.KILO, OHM_NAME, OHM_SYMBOL, RESISTANCE)
MEGAOHM = prefixed_unit(prefixes.MEGA, OHM_NAME, OHM_SYMBOL, RESISTANCE)
GIGAOHM = prefixed_unit(prefixes.GIGA, OHM_NAME, OHM_SYMBOL, RESISTANCE)


Resistance._canonical_unit = OHM  # noqa: SLF001 -- this module owns Resistance's canonical unit


def Microohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in microohms.

    Parameters
    ----------
    value : Numeric
        Resistance magnitude in microohms.

    Returns
    -------
    Resistance
        Resistance represented in microohms.

    Examples
    --------
    Very small resistances occur in current shunts, contacts, and other low-resistance
    conductors:

    >>> contact_resistance = Microohm(250)
    >>> contact_resistance
    250 µΩ

    One thousand microohms make exactly one milliohm:

    >>> Microohm(1000) == Milliohm(1)
    True

    """
    return Resistance(to_exact(value) * MICROOHM.scale, MICROOHM)


def Milliohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in milliohms.

    Parameters
    ----------
    value : Numeric
        Resistance magnitude in milliohms.

    Returns
    -------
    Resistance
        Resistance represented in milliohms.

    Examples
    --------
    A low-value current-sense resistor may have a resistance of only a few milliohms:

    >>> shunt = Milliohm(5)
    >>> shunt
    5 mΩ

    One thousand milliohms make exactly one ohm:

    >>> Milliohm(1000) == Ohm(1)
    True

    """
    return Resistance(to_exact(value) * MILLIOHM.scale, MILLIOHM)


def Ohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in ohms.

    Parameters
    ----------
    value : Numeric
        Resistance magnitude in ohms.

    Returns
    -------
    Resistance
        Resistance represented in ohms.

    Examples
    --------
    A one-ohm resistance is a useful reference point for the complete unit family:

    >>> resistance = Ohm(1)
    >>> resistance
    1 Ω

    Resistance values can also be negative mathematically.
    This is useful for quantities produced by circuit models containing active devices,
    even though an ordinary passive resistor does not have negative resistance:

    >>> model_parameter = Ohm(-2)
    >>> model_parameter
    -2 Ω

    """
    return Resistance(to_exact(value) * OHM.scale, OHM)


def Kiloohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in kilohms.

    Parameters
    ----------
    value : Numeric
        Resistance magnitude in kilohms.

    Returns
    -------
    Resistance
        Resistance represented in kilohms.

    Examples
    --------
    Kilohm values are common in electronic circuits. A 4.7 kΩ resistor is represented
    directly:

    >>> bias_resistor = Kiloohm(4.7)
    >>> bias_resistor
    4.7 kΩ

    One thousand kilohms make exactly one megaohm:

    >>> Kiloohm(1000) == Megaohm(1)
    True

    """
    return Resistance(to_exact(value) * KILOOHM.scale, KILOOHM)


def Megaohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in megaohms.

    Parameters
    ----------
    value : Numeric
        Resistance magnitude in megaohms.

    Returns
    -------
    Resistance
        Resistance represented in megaohms.

    Examples
    --------
    High-value resistors are useful when a circuit must draw very little current from
    its source:

    >>> high_value_resistor = Megaohm(1)
    >>> high_value_resistor
    1 MΩ

    One megaohm is exactly one million ohms:

    >>> Megaohm(1) == Ohm(1_000_000)
    True

    """
    return Resistance(to_exact(value) * MEGAOHM.scale, MEGAOHM)


def Gigaohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in gigaohms.

    Parameters
    ----------
    value : Numeric
        Resistance magnitude in gigaohms.

    Returns
    -------
    Resistance
        Resistance represented in gigaohms.

    Examples
    --------
    Very high resistance is useful when describing insulation and extremely
    small leakage paths:

    >>> insulation = Gigaohm(1)
    >>> insulation
    1 GΩ

    One gigaohm is exactly one thousand megaohms:

    >>> Gigaohm(1) == Megaohm(1000)
    True

    """
    return Resistance(to_exact(value) * GIGAOHM.scale, GIGAOHM)


RESISTANCE_UNITS: Mapping[str, Callable[[Numeric], Resistance]] = MappingProxyType(
    {
        MICROOHM.symbol: Microohm,
        MILLIOHM.symbol: Milliohm,
        OHM.symbol: Ohm,
        KILOOHM.symbol: Kiloohm,
        MEGAOHM.symbol: Megaohm,
        GIGAOHM.symbol: Gigaohm,
    }
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
