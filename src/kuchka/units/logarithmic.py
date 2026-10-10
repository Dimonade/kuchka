"""Logarithmic ratio quantities and constructors for the decibel and the bel.

`LogarithmicRatio` expresses a ratio of two like quantities on a logarithmic scale:
the gain of an amplifier, the loss of a cable, a signal-to-noise ratio.
The decibel is the canonical unit, and the bel is ten decibels.

Multiplying two ratios adds their levels.
Stages in series therefore combine by plain addition, and every such sum is exact.

Examples
--------
A receive chain has a 20 dB amplifier, a cable with 3.5 dB of loss, and a filter with
1.5 dB of loss.
The levels add:

>>> amplifier = Decibel(20)
>>> cable = Decibel(-3.5)
>>> filter_loss = Decibel(-1.5)
>>> chain = amplifier + cable + filter_loss
>>> chain
15 dB

Scaling a level by a plain number scales the exponent of the ratio it describes.
A cable that loses 0.2 dB per metre loses 6 dB over 30 metres:

>>> loss_per_metre = Decibel(-0.2)
>>> loss_per_metre * 30
-6 dB

Levels compare by the ratios they describe, which makes a gain tolerance check a
one-liner:

>>> expected = Decibel(20)
>>> measured = Decibel(20.3)
>>> abs(measured - expected) <= Decibel(0.5)
True

A level maps to a linear ratio in two flavours.
Power quantities use ``10 ** (level / 10)`` and field quantities such as voltage use
``10 ** (level / 20)``.
Whole multiples of 10 dB (power) or 20 dB (field) convert exactly:

>>> from kuchka import Ratio
>>> Decibel(30).to_power_ratio() == Ratio(1000)
True
>>> Decibel(40).to_field_ratio() == Ratio(100)
True

Other levels convert to the precision of the active `decimal` context.
The much-quoted "3 dB is a factor of two" is a close approximation:

>>> Decibel(3).to_power_ratio() == Ratio(2)
False
>>> float(Decibel(3).to_power_ratio().magnitude)
1.9952623149688795

The reverse direction is a classmethod on `LogarithmicRatio`:

>>> LogarithmicRatio.from_power_ratio(Ratio(100)) == Decibel(20)
True

Notes
-----
A level is the same number for a ratio of power quantities and for a ratio of field
quantities.
`to_power_ratio()` and `to_field_ratio()` pick the flavour at the point of conversion.

Only a positive ratio has a level.
`LogarithmicRatio.from_power_ratio(Ratio(0))` raises `InvalidMeasurementError`.

`LOGARITHMIC_RATIO_UNITS` maps unit symbols (``"dB"``, ``"B"``) to their constructors
for configuration files and other external interfaces.

See Also
--------
~kuchka.quantities.Proportion
    The linear ratio a level converts to and from.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import LogarithmicRatio
from kuchka.quantities import LogarithmicUnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

DECIBEL = LogarithmicUnitDef("decibel", "dB", 1)
BEL = LogarithmicUnitDef("bel", "B", 10)

LogarithmicRatio._canonical_unit = DECIBEL  # noqa: SLF001 -- this module owns LogarithmicRatio's canonical unit


def Decibel(value: Numeric) -> LogarithmicRatio:
    """Construct a logarithmic ratio from a magnitude expressed in decibels.

    Parameters
    ----------
    value : Numeric
        Level in decibels.

    Returns
    -------
    LogarithmicRatio
        Level represented in decibels.

    Notes
    -----
    A positive level is a gain, a negative level is an attenuation, and zero is a
    ratio of one.

    Examples
    --------
    A microphone preamplifier adding 40 dB of gain:

    >>> preamp_gain = Decibel(40)

    A gain and the attenuation that undoes it cancel exactly:

    >>> preamp_gain + Decibel(-40) == Decibel(0)
    True

    """
    return LogarithmicRatio(to_exact(value) * DECIBEL.scale, DECIBEL)


def Bel(value: Numeric) -> LogarithmicRatio:
    """Construct a logarithmic ratio from a magnitude expressed in bels.

    Parameters
    ----------
    value : Numeric
        Level in bels.

    Returns
    -------
    LogarithmicRatio
        Level represented in bels.

    Notes
    -----
    One bel is exactly ten decibels.

    Examples
    --------
    Two bels are twenty decibels:

    >>> Bel(2) == Decibel(20)
    True

    A level displays in whichever unit it was last asked to be seen in:

    >>> Decibel(35).to(BEL)
    3.5 B

    """
    return LogarithmicRatio(to_exact(value) * BEL.scale, BEL)


LOGARITHMIC_RATIO_UNITS: Mapping[str, Callable[[Numeric], LogarithmicRatio]] = (
    unit_table(
        "LOGARITHMIC_RATIO_UNITS",
        {
            DECIBEL: Decibel,
            BEL: Bel,
        },
    )
)

__all__ = [
    "BEL",
    "DECIBEL",
    "LOGARITHMIC_RATIO_UNITS",
    "Bel",
    "Decibel",
]
