"""Proportion constructors: the plain ratio and the percent.

`Proportion` is a dimensionless quantity, a fraction of a whole or a ratio of two like
quantities.
`Ratio` is the coherent, unscaled unit: a bare fraction, typically between 0 and 1.
`Percent` is a hundredth of that:

>>> from decimal import Decimal
>>> from kuchka import Percent
>>> from kuchka import Ratio
>>> tolerance = Percent(5)
>>> duty_cycle = Ratio(Decimal("0.8"))

ISO 80000 denotes the coherent unit for a dimensionless quantity as `"1"`, and
`repr()` follows that convention, so `Ratio(Decimal("0.05"))` prints as `0.05 1`.
Efficiencies, tolerances, compositions, and duty cycles are proportions, and each is
quoted either as a fraction or as a percent.

Examples
--------
A motor draws 200 W and delivers 50 W of mechanical power.
The quotient of two like quantities is a proportion, and a percent shows it:

>>> from kuchka import Watt
>>> from kuchka.units import PERCENT
>>> efficiency = Watt(50) / Watt(200)
>>> efficiency
0.25 1
>>> efficiency.to(PERCENT)
25 %

A proportion scales a quantity, and the result keeps the quantity's type.
A person of 80 kg with 15 % body fat carries 12 kg of fat:

>>> from kuchka import Kilogram
>>> Percent(15) * Kilogram(80)
12 kg

Proportions add and subtract exactly, whichever unit each is written in:

>>> Ratio(1) - Percent(20)
0.8 1
>>> Percent(5) + Percent(3)
8 %

A proportion has no dimension, but it is a quantity of its own, so it refuses to add to
a mass:

>>> Ratio(1) + Kilogram(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...

Notes
-----
A percent is exactly one hundredth of a ratio, so
`Percent(5) == Ratio(Decimal("0.05"))`.

`PROPORTION_UNITS` maps the symbols ``"1"`` and ``"%"`` to their constructors, for
boundary code that reads a unit as a string from outside the application.
`parse` reads text such as ``"5 %"`` and ``"0.05 1"``.

References
----------
BIPM, The International System of Units (SI Brochure), on dimensionless quantities and
the percent sign:
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.LogarithmicRatio
    A ratio expressed as a level, in decibels.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import DIMENSIONLESS
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Proportion
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

RATIO = UnitDef("ratio", "1", Decimal(1), DIMENSIONLESS)
PERCENT = UnitDef(
    "percent",
    "%",
    Decimal("0.01"),
    DIMENSIONLESS,
    aliases=("pct",),
    words=("per cent",),
)
Proportion._canonical_unit = RATIO  # noqa: SLF001 -- this module owns Proportion's canonical unit


def Ratio(value: Numeric) -> Proportion:
    """Construct a Proportion from a bare fraction, e.g. 0.05 for five percent.

    Parameters
    ----------
    value : Numeric
        Fraction as a plain number, where 1 is the whole.

    Returns
    -------
    Proportion
        Proportion represented as a bare fraction.

    Examples
    --------
    A component is specified with a tolerance of five percent:

    >>> from decimal import Decimal
    >>> tolerance = Ratio(Decimal("0.05"))
    >>> tolerance
    0.05 1

    The same tolerance in percent:

    >>> from kuchka.units import PERCENT
    >>> tolerance.to(PERCENT)
    5 %

    A duty cycle that arrives as text with the plain unit of the ratio enters through
    `parse`:

    >>> from kuchka import Proportion
    >>> from kuchka import parse
    >>> parse("0.8 1", Proportion) == Ratio(Decimal("0.8"))
    True

    """
    return Proportion(to_exact(value) * RATIO.scale, RATIO)


def Percent(value: Numeric) -> Proportion:
    """Construct a Proportion from a magnitude expressed in percent.

    Parameters
    ----------
    value : Numeric
        Magnitude in percent, where 100 is the whole.

    Returns
    -------
    Proportion
        Proportion represented in percent.

    Examples
    --------
    A resistor is sold with a tolerance of 5 %:

    >>> tolerance = Percent(5)
    >>> tolerance
    5 %

    A rod of 250 mm that may be off by 2 % is off by at most 5 mm:

    >>> from kuchka import Millimetre
    >>> from kuchka.units import MILLIMETRE
    >>> (Millimetre(250) * Percent(2)).to(MILLIMETRE)
    5 mm

    A percent is a hundredth of a ratio exactly:

    >>> from decimal import Decimal
    >>> from kuchka import Ratio
    >>> tolerance == Ratio(Decimal("0.05"))
    True

    """
    return Proportion(to_exact(value) * PERCENT.scale, PERCENT)


PROPORTION_UNITS: Mapping[str, Callable[[Numeric], Proportion]] = unit_table(
    "PROPORTION_UNITS",
    {
        RATIO: Ratio,
        PERCENT: Percent,
    },
)

__all__ = [
    "PERCENT",
    "PROPORTION_UNITS",
    "RATIO",
    "Percent",
    "Ratio",
]
