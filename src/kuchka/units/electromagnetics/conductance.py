"""Conductance constructors: the siemens, from nanosiemens to kilosiemens.

    from kuchka import Kilosiemens
    from kuchka import Microsiemens
    from kuchka import Millisiemens
    from kuchka import Siemens

    sensor_input = Microsiemens(0.4)
    bias_path = Millisiemens(5)
    current_shunt = Kilosiemens(1)

`Conductance` describes the ability of an electrical path to carry current for a given
potential difference.
Its SI unit is the siemens (S), defined as one ampere per volt, or the reciprocal of
one ohm:

``1 S = 1 A/V = 1 Ω⁻¹``

For a linear, purely resistive element, conductance is the reciprocal of resistance:

``G = 1/R``

The available units cover electrical paths from very high resistance to extremely low
resistance:

* nanosiemens (nS) describe leakage paths, insulation resistance, and high-impedance
    measurement inputs, typically associated with gigaohm resistance;
* microsiemens (µS) are useful for sensor inputs, bias networks, and high-resistance
    circuit paths in the megaohm range;
* millisiemens (mS) cover ordinary electronic components, resistive loads, and circuit
    branches in the kiloohm range;
* siemens (S) describe lower-resistance circuit paths and components, including
    resistors around one ohm;
* kilosiemens (kS) describe milliohm-scale paths, including current shunts, busbars,
    and low-resistance power connections.

Examples
--------
Conductances of parallel resistive paths add because each branch experiences the same
potential difference while their currents combine.

A circuit has two parallel branches, each with a resistance of 1 kΩ.
Each branch contributes 1 mS of conductance:

>>> branch_a = Millisiemens(1)
>>> branch_b = Millisiemens(1)
>>> equivalent = branch_a + branch_b
>>> equivalent
2 mS

The equivalent resistance of the parallel network is the reciprocal of its combined
conductance:

>>> 1 / equivalent
500 Ω

Older circuit diagrams and component references sometimes express conductance using the
historical name mho.
The parser recognizes this spelling and its prefixed forms:

>>> from kuchka import Conductance
>>> from kuchka import parse
>>> parse("5 millimho", Conductance)
5 mS

Notes
-----
Conductance, denoted by G, is the reciprocal of electrical resistance.
For a linear resistive element, Ohm's law gives:

``G = I/V = 1/R``

where I is the current through the element and V is the potential difference across it.

The siemens is the SI derived unit of conductance:

``1 S = 1 A/V = 1 Ω⁻¹``

In a parallel network, conductances add directly:

``G_total = G₁ + G₂ + ... + Gₙ``

This follows because parallel branches share a common potential difference and their
individual currents add.

Conductance is a property of an electrical path or component.
It must not be confused with electrical conductivity, denoted by σ, which is a material
property and has units of siemens per metre (S/m).

For a uniform, isotropic conductor of length l and cross-sectional area A, conductance
relates to material conductivity through:

``G = σ A/l``

Thus, conductance depends on both the material and the geometry of the conducting path,
whereas conductivity describes the material itself.

For AC circuits, the reciprocal of complex impedance is admittance:

``Y = 1/Z = G + jB``

where G is conductance and B is susceptance.
Conductance is the real part of admittance; this module represents the conductance
quantity, not complex admittance.

The older name for the siemens is the mho, derived from the reverse spelling of ohm.
`SIEMENS_WORDS` registers ``"mho"`` as an alternative unit name, and the prefixed unit
definitions provide corresponding forms such as ``"millimho"``.

All supported units are exact decimal multiples of the siemens.
Conversions between nanosiemens, microsiemens, millisiemens, siemens, and kilosiemens
therefore preserve exactness.

`parse` reads complete measurements such as ``"1 nS"``, ``"0.4 µS"``, ``"5 mS"``, and
``"1 millimho"``.

`CONDUCTANCE_UNITS` maps symbols such as ``"nS"``, ``"µS"``, ``"mS"``, ``"S"``, and
``"kS"`` to their constructors.
It is intended for boundary code that receives a numeric magnitude and a separate unit
symbol from an external source.

The siemens was adopted as the SI unit of electrical conductance by the 14th CGPM in
1971.

BIPM, The International System of Units (SI), 9th edition:
https://www.bipm.org/en/si-brochure-9

IUPAC, Compendium of Chemical Terminology:
https://goldbook.iupac.org/terms/view/E01925
https://goldbook.iupac.org/terms/view/C01245

See Also
--------
~kuchka.quantities.Conductance
    Quantity type representing electrical conductance.

~kuchka.quantities.Resistance
    Electrical resistance, which is reciprocal to conductance.

~kuchka.quantities.Current
    Electric current through a conducting path.

~kuchka.quantities.Voltage
    Potential difference across a conducting path.

"""  # noqa: RUF002 -- using "sigma" symbol.

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

    from kuchka.quantities import UnitDef
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
        Conductance magnitude in nS.

    Returns
    -------
    Conductance
        Conductance represented in nanosiemens.

    Examples
    --------
    A high-resistance insulation path has a resistance of 1 GΩ, corresponding to a
    conductance of 1 nS:

    >>> leakage = Nanosiemens(1)
    >>> leakage
    1 nS

    The reciprocal of the conductance gives the resistance of the path:

    >>> from kuchka import Ohm
    >>> 1 / leakage == Ohm(1_000_000_000)
    True

    """
    return Conductance(to_exact(value) * NANOSIEMENS.scale, NANOSIEMENS)


def Microsiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in microsiemens.

    Parameters
    ----------
    value : Numeric
        Conductance magnitude in µS.

    Returns
    -------
    Conductance
        Conductance represented in microsiemens.

    Examples
    --------
    A sensor-conditioning input has a resistance of 2.5 MΩ.
    Its corresponding conductance is 0.4 µS:

    >>> from kuchka import Megaohm
    >>> resistance = Megaohm(2.5)
    >>> input_conductance = (1 / resistance).to(MICROSIEMENS)
    >>> input_conductance
    0.4 µS

    An acquisition system stores the measurement as text.
    Read the complete measurement:

    >>> from kuchka import Conductance
    >>> from kuchka import parse
    >>> parse("0.4 µS", Conductance) == input_conductance
    True

    """
    return Conductance(to_exact(value) * MICROSIEMENS.scale, MICROSIEMENS)


def Millisiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in millisiemens.

    Parameters
    ----------
    value : Numeric
        Conductance magnitude in mS.

    Returns
    -------
    Conductance
        Conductance represented in millisiemens.

    Examples
    --------
    A 200 Ω resistive bias path has a conductance of exactly 5 mS:

    >>> bias_path = Millisiemens(5)
    >>> bias_path
    5 mS

    An electronic load contains two parallel resistive paths:
    one of 1 kΩ and another of 500 Ω.
    Their conductances are 1 mS and 2 mS respectively:

    >>> branch_a = Millisiemens(1)
    >>> branch_b = Millisiemens(2)
    >>> branch_a + branch_b
    3 mS

    """
    return Conductance(to_exact(value) * MILLISIEMENS.scale, MILLISIEMENS)


def Siemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in siemens.

    Parameters
    ----------
    value : Numeric
        Conductance magnitude in S.

    Returns
    -------
    Conductance
        Conductance represented in siemens.

    Examples
    --------
    A one-ohm resistive path has a conductance of exactly one siemens:

    >>> one_ohm_path = Siemens(1)
    >>> one_ohm_path
    1 S

    Older electrical literature uses the name mho for the same unit:

    >>> from kuchka import Conductance
    >>> from kuchka import parse
    >>> parse("1 mho", Conductance) == one_ohm_path
    True

    """
    return Conductance(to_exact(value) * SIEMENS.scale, SIEMENS)


def Kilosiemens(value: Numeric) -> Conductance:
    """Construct a Conductance from a magnitude expressed in kilosiemens.

    Parameters
    ----------
    value : Numeric
        Conductance magnitude in kS.

    Returns
    -------
    Conductance
        Conductance represented in kilosiemens.

    Examples
    --------
    A current shunt with a resistance of 1 mΩ has a conductance of exactly 1 kS:

    >>> current_shunt = Kilosiemens(1)
    >>> current_shunt
    1 kS

    The reciprocal gives the shunt's resistance:

    >>> from kuchka import Ohm
    >>> 1 / current_shunt == Ohm(0.001)
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

CONDUCTANCE_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        NANOSIEMENS,
        MICROSIEMENS,
        MILLISIEMENS,
        SIEMENS,
        KILOSIEMENS,
    ),
)
"""The units `auto_scale` moves a conductance along, smallest first."""

__all__ = [
    "CONDUCTANCE_LADDERS",
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
