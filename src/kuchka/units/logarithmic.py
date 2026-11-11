"""Logarithmic ratio constructors: the decibel and the bel.

`LogarithmicRatio` expresses a ratio of two like quantities on a logarithmic scale:
the gain of an amplifier, the loss of a cable, a signal-to-noise ratio.
The decibel is the canonical unit, and the bel is ten decibels.

Multiplying two ratios adds their levels.
Stages in series therefore combine by plain addition, and every such sum is exact.

Amplifier gains, cable and filter losses, signal-to-noise ratios, and the dynamic range
of converters are quoted in decibels.
The bel, ten decibels, is the larger unit that the decibel is named after.

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

A 16-bit converter tells 2**16 amplitude steps apart, so its dynamic range is the level
of a field ratio of 65 536:

>>> f"{LogarithmicRatio.from_field_ratio(Ratio(2**16)):.1f}"
'96.3 dB'

A level and a linear ratio are different things, so the two refuse to add:

>>> Decibel(3) + Ratio(2)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
TypeError: ...

Notes
-----
A level is the same number for a ratio of power quantities and for a ratio of field
quantities.
`to_power_ratio()` and `to_field_ratio()` pick the flavour at the point of conversion.

Only a positive ratio has a level.
`LogarithmicRatio.from_power_ratio(Ratio(0))` raises `InvalidMeasurementError`.

`LOGARITHMIC_RATIO_UNITS` maps unit symbols (``"dB"``, ``"B"``) to their constructors
for configuration files and other external interfaces.

References
----------
BIPM, The International System of Units (SI Brochure), on the neper, the bel, and
logarithmic quantities:
https://www.bipm.org/en/publications/si-brochure

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
    A microphone preamplifier adds 40 dB of gain:

    >>> preamp_gain = Decibel(40)
    >>> preamp_gain
    40 dB

    A gain and the attenuation that undoes it cancel exactly:

    >>> preamp_gain + Decibel(-40) == Decibel(0)
    True

    A filter is specified by its half-power point, 3 dB down, where it passes about half
    of the power:

    >>> half_power = Decibel(-3).to_power_ratio()
    >>> f"{float(half_power.magnitude):.3f}"
    '0.501'

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
    A power gain of 3 B is a factor of a thousand:

    >>> gain = Bel(3)
    >>> gain
    3 B
    >>> from kuchka import Ratio
    >>> gain.to_power_ratio() == Ratio(1000)
    True

    Two bels are twenty decibels, and a level displays in whichever unit it was last
    asked to be seen in:

    >>> Bel(2) == Decibel(20)
    True
    >>> from kuchka.units import BEL
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
