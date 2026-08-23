"""TemperatureDelta: the difference between two temperatures.

A gap of five degrees can be added, subtracted, and scaled the same way a voltage or a
current can: "the gap doubled" is physically meaningful in a way
"the temperature doubled" is not.

That is what makes a difference in temperature an ordinary
:class:`~kuchka.quantities.base.LinearQuantity`, even though absolute
:class:`~kuchka.temperature.Temperature` is not.

See ``temperature.py`` for the affine, non-linear absolute-temperature type this
complements.
"""

from __future__ import annotations

from typing import ClassVar
from typing import TYPE_CHECKING

from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class TemperatureDelta(LinearQuantity):
    """A difference between two temperatures, e.g. a tolerance band."""

    dimension: ClassVar[Dimension] = TEMPERATURE_DELTA


register(TEMPERATURE_DELTA, TemperatureDelta)
