"""Luminous intensity constructors: the candela.

`LuminousIntensity` is the light a source emits in one direction, per unit of solid
angle, weighted by the sensitivity of the eye.
The candela (`cd`) is the SI base unit and the canonical unit, and it is the only unit
of the module:

>>> from kuchka import Candela
>>> lamp = Candela(120)

A candle flame gives about one candela, an indicator LED a few hundredths of one, a
car headlamp thousands, and a lighthouse beam millions.

Examples
--------
A bulb of 1200 lm that radiates equally in every direction, a solid angle of 4 pi
steradians, has an intensity of about 95.5 cd:

>>> import math
>>> from kuchka import Lumen
>>> from kuchka import Steradian
>>> from kuchka.units import CANDELA
>>> bulb = Lumen(1200) / Steradian(4 * math.pi)
>>> f"{bulb.to(CANDELA):.1f}"
'95.5 cd'

A source of 100 cd sends 100 lm into each steradian, and a surface that faces it at
2 m, where each steradian spreads over 4 m², is lit with 25 lx:

>>> from kuchka import SquareMetre
>>> Candela(100) * Steradian(1) / SquareMetre(4)
25 lx

Intensities of sources in the same direction add:

>>> Candela(15) + Candela(45)
60 cd

An intensity and a flux are different quantities, since the flux is spread over a solid
angle, so the two refuse to add:

>>> Candela(1) + Lumen(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...

Notes
-----
The candela is defined by fixing the luminous efficacy of monochromatic radiation of
frequency 540E+12 Hz at exactly 683 lm/W.
It is the base unit that ties the SI to human vision, and the lumen follows from it as
a candela times a steradian.

`LUMINOUS_INTENSITY_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.

References
----------
BIPM, The International System of Units (SI Brochure), on the candela:
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.LuminousFlux
    An intensity times a solid angle is a flux.
~kuchka.quantities.Illuminance
    An intensity times a solid angle over an area is an illuminance.
~kuchka.quantities.SolidAngle
    The angle that a source's light is spread over.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import LUMINOUS_INTENSITY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import LuminousIntensity
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

CANDELA = UnitDef("candela", "cd", Decimal(1), LUMINOUS_INTENSITY)
"""Definition of the candela unit."""

LuminousIntensity._canonical_unit = CANDELA  # noqa: SLF001 -- this module owns LuminousIntensity's canonical unit


def Candela(value: Numeric) -> LuminousIntensity:
    """Construct a luminous intensity from a magnitude in candela.

    Parameters
    ----------
    value : Numeric
        Magnitude expressed in candela.

    Returns
    -------
    LuminousIntensity
        Luminous intensity represented by `value` candela.

    Examples
    --------
    The beam of a desk lamp reads 120 cd on its axis:

    >>> source = Candela(120)
    >>> source
    120 cd

    If that intensity held over a cone of 2 sr, the lamp would send out 240 lm:

    >>> from kuchka import Steradian
    >>> from kuchka.units import LUMEN
    >>> (source * Steradian(2)).to(LUMEN)
    240 lm

    An intensity that arrives as text, as a datasheet writes it, enters through `parse`:

    >>> from kuchka import LuminousIntensity
    >>> from kuchka import parse
    >>> parse("120 cd", LuminousIntensity) == source
    True

    """
    return LuminousIntensity(to_exact(value) * CANDELA.scale, CANDELA)


LUMINOUS_INTENSITY_UNITS: Mapping[str, Callable[[Numeric], LuminousIntensity]] = (
    unit_table(
        "LUMINOUS_INTENSITY_UNITS",
        {
            CANDELA: Candela,
        },
    )
)
"""Mappings from unit symbols to their constructors."""

__all__ = [
    "CANDELA",
    "LUMINOUS_INTENSITY_UNITS",
    "Candela",
]
