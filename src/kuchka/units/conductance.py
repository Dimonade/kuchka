"""Conductance quantities and constructors for practical electrical scales.

`Conductance` represents the ease with which electric current passes through a
resistive path.
Its SI unit is the siemens, defined as one ampere per volt:

`1 S = 1 A / V = 1 Ω⁻¹`.

For a purely resistive path, conductance is the reciprocal of resistance:

`G = 1 / R`.

The constructors in this module cover conductance from nanosiemens through kilosiemens.
This range spans high-resistance leakage paths and sensor inputs at the small end,
ordinary electronic circuits in the micro- to milli- range, and very low-resistance
power paths at the large end.

Examples
--------
A high-resistance path has correspondingly small conductance.
A 1 MΩ resistor has exactly 1 µS of conductance:

>>> leakage = Microsiemens(1)
>>> leakage
1 µS

A 200 kΩ resistor corresponds to 5 µS:

>>> bias_path = Microsiemens(5)
>>> bias_path
5 µS

Ordinary electronic components readily reach the millisiemens range.
A 200 Ω resistor has exactly 5 mS of conductance:

>>> load = Millisiemens(5)
>>> load
5 mS

The reciprocal relationship can be checked directly:

>>> 1 / Millisiemens(5)
200 Ω

A one-ohm resistive path has one siemens of conductance:

>>> one_ohm_path = Siemens(1)
>>> one_ohm_path
1 S

Very low resistances produce very large conductances.
A 1 mΩ current shunt has exactly 1 kS of conductance:

>>> current_shunt = Kilosiemens(1)
>>> current_shunt
1 kS

The same electrical quantity can be expressed at any supported scale without loss of
exactness:

>>> Nanosiemens(1000) == Microsiemens(1)
True

>>> Microsiemens(1000) == Millisiemens(1)
True

>>> Millisiemens(1000) == Siemens(1)
True

>>> Siemens(1000) == Kilosiemens(1)
True

Conductance also adds naturally for parallel resistive paths.
Two independent paths of 1 kΩ and 500 Ω contribute 1 mS and 2 mS respectively:

>>> path_a = Millisiemens(1)
>>> path_b = Millisiemens(2)
>>> total = path_a + path_b
>>> total
3 mS

Notes
-----
Conductance is a property of a conductive path and has units of siemens (`S`).
It must not be confused with **conductivity**, which is a material property with units
of siemens per metre (`S/m`).
Conductivity instruments may display values such as `µS/cm`, but that is not a
`Conductance` quantity.

For a DC resistive element, conductance is the reciprocal of resistance.
For AC circuits containing reactance, the reciprocal of impedance is **admittance**,
whose real part is conductance.
This module represents the conductance quantity itself, not complex admittance.

All units in this module are exact decimal multiples of the siemens.
Consequently, conversions such as

>>> Microsiemens(1000) == Millisiemens(1)
True

are exact.

`CONDUCTANCE_UNITS` maps symbols such as ``"nS"``, ``"µS"``, ``"mS"``, ``"S"``, and
``"kS"`` to their constructors.
It is intended for boundary code that receives the unit as external data, such as a
configuration file.

See Also
--------
~kuchka.quantities.Resistance
    Reciprocal electrical resistance quantities.
~kuchka.quantities.Current
    Electric current quantities related to voltage and conductance.
~kuchka.quantities.Voltage
    Electric potential difference.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import CONDUCTANCE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Conductance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

SIEMENS_NAME = "siemens"
SIEMENS_SYMBOL = "S"
SIEMENS_WORDS = ("mho",)
"""The older name, which prefixed names follow: `millimho`."""

NANOSIEMENS = prefixed_unit(
    prefixes.NANO, SIEMENS_NAME, SIEMENS_SYMBOL, CONDUCTANCE, base_words=SIEMENS_WORDS
)
MICROSIEMENS = prefixed_unit(
    prefixes.MICRO, SIEMENS_NAME, SIEMENS_SYMBOL, CONDUCTANCE, base_words=SIEMENS_WORDS
)
MILLISIEMENS = prefixed_unit(
    prefixes.MILLI, SIEMENS_NAME, SIEMENS_SYMBOL, CONDUCTANCE, base_words=SIEMENS_WORDS
)
SIEMENS = prefixed_unit(
    prefixes.UNIT, SIEMENS_NAME, SIEMENS_SYMBOL, CONDUCTANCE, base_words=SIEMENS_WORDS
)
KILOSIEMENS = prefixed_unit(
    prefixes.KILO, SIEMENS_NAME, SIEMENS_SYMBOL, CONDUCTANCE, base_words=SIEMENS_WORDS
)


Conductance._canonical_unit = SIEMENS  # noqa: SLF001 -- this module owns Conductance's canonical unit


def Nanosiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in nanosiemens.

    Parameters
    ----------
    value : Numeric
        Conductance magnitude in nanosiemens.

    Returns
    -------
    Conductance
        Conductance represented in nanosiemens.

    Examples
    --------
    A 1 GΩ resistive path has exactly 1 nS of conductance:

    >>> leakage = Nanosiemens(1)
    >>> leakage
    1 nS

    One thousand nanosiemens make exactly one microsiemens:

    >>> Nanosiemens(1000) == Microsiemens(1)
    True

    """
    return Conductance(to_exact(value) * NANOSIEMENS.scale, NANOSIEMENS)


def Microsiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in microsiemens.

    Parameters
    ----------
    value : Numeric
        Conductance magnitude in microsiemens.

    Returns
    -------
    Conductance
        Conductance represented in microsiemens.

    Examples
    --------
    A 1 MΩ resistive path has exactly 1 µS of conductance:

    >>> leakage = Microsiemens(1)
    >>> leakage
    1 µS

    A thousand microsiemens make exactly one millisiemens:

    >>> Microsiemens(1000) == Millisiemens(1)
    True

    """
    return Conductance(to_exact(value) * MICROSIEMENS.scale, MICROSIEMENS)


def Millisiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in millisiemens.

    Parameters
    ----------
    value : Numeric
        Conductance magnitude in millisiemens.

    Returns
    -------
    Conductance
        Conductance represented in millisiemens.

    Examples
    --------
    A 200 Ω resistive path has exactly 5 mS of conductance:

    >>> load = Millisiemens(5)
    >>> load
    5 mS

    A 100 Ω path has exactly 10 mS:

    >>> Millisiemens(10)
    10 mS

    One thousand millisiemens make exactly one siemens:

    >>> Millisiemens(1000) == Siemens(1)
    True

    """
    return Conductance(to_exact(value) * MILLISIEMENS.scale, MILLISIEMENS)


def Siemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in siemens.

    Parameters
    ----------
    value : Numeric
        Conductance magnitude in siemens.

    Returns
    -------
    Conductance
        Conductance represented in siemens.

    Examples
    --------
    A 1 Ω resistive path has exactly 1 S of conductance:

    >>> one_ohm_path = Siemens(1)
    >>> one_ohm_path
    1 S

    A 100 Ω path has one hundredth of a siemens:

    >>> Siemens(0.01) == Millisiemens(10)
    True

    A thousand siemens make exactly one kilosiemens:

    >>> Siemens(1000) == Kilosiemens(1)
    True

    """
    return Conductance(to_exact(value) * SIEMENS.scale, SIEMENS)


def Kilosiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in kilosiemens.

    Parameters
    ----------
    value : Numeric
        Conductance magnitude in kilosiemens.

    Returns
    -------
    Conductance
        Conductance represented in kilosiemens.

    Examples
    --------
    A 1 mΩ resistive path has exactly 1 kS of conductance. This scale is
    relevant to very low-resistance power paths and current shunts:

    >>> current_shunt = Kilosiemens(1)
    >>> current_shunt
    1 kS

    One kilosiemens is exactly one million microsiemens:

    >>> Kilosiemens(1) == Microsiemens(1_000_000_000)
    True

    """
    return Conductance(to_exact(value) * KILOSIEMENS.scale, KILOSIEMENS)


CONDUCTANCE_UNITS: Mapping[str, Callable[[Numeric], Conductance]] = unit_table(
    "CONDUCTANCE_UNITS",
    {
        NANOSIEMENS: Nanosiemens,
        MICROSIEMENS: Microsiemens,
        MILLISIEMENS: Millisiemens,
        SIEMENS: Siemens,
        KILOSIEMENS: Kilosiemens,
    },
)

__all__ = [
    "CONDUCTANCE_UNITS",
    "KILOSIEMENS",
    "MICROSIEMENS",
    "MILLISIEMENS",
    "NANOSIEMENS",
    "SIEMENS",
    "Kilosiemens",
    "Microsiemens",
    "Millisiemens",
    "Nanosiemens",
    "Siemens",
]
