"""Amount Of Substance: a count of elementary entities, expressed in moles."""

from __future__ import annotations

from typing import ClassVar
from typing import TYPE_CHECKING

from kuchka.dimensions import AMOUNT_OF_SUBSTANCE
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class AmountOfSubstance(LinearQuantity):
    """A count of elementary entities, expressed in moles."""

    dimension: ClassVar[Dimension] = AMOUNT_OF_SUBSTANCE


register(AMOUNT_OF_SUBSTANCE, AmountOfSubstance)
