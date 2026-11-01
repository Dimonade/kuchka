"""Entities per amount constructors: PerMole.

The number of elementary entities (atoms, molecules, ions) per amount of substance, in
reciprocal moles: `1 mol⁻¹` is the canonical unit.
The Avogadro constant is `6.02214076e23 mol⁻¹`, so a quantity of it times an amount of
substance is a plain count of entities.

`ENTITIES_PER_AMOUNT_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ENTITIES_PER_AMOUNT
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import EntitiesPerAmount
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

PER_MOLE = UnitDef(
    "per_mole",
    f"mol{symbols.SUPERSCRIPT_MINUS_SIGN}{symbols.SUPERSCRIPT_ONE}",
    1,
    ENTITIES_PER_AMOUNT,
    aliases=("1/mol", "/mol", "mol^-1", "mol**-1"),
    words=("per mole", "reciprocal mole"),
)

EntitiesPerAmount._canonical_unit = PER_MOLE  # noqa: SLF001 -- this module owns EntitiesPerAmount's canonical unit


def PerMole(value: Numeric) -> EntitiesPerAmount:
    """Construct a number of entities per amount from a magnitude in reciprocal moles.

    Parameters
    ----------
    value : Numeric
        Number of entities per amount magnitude in mol⁻¹.

    Returns
    -------
    EntitiesPerAmount
        Number of entities per amount represented in reciprocal moles.

    Examples
    --------
    A micromole of any substance holds a millionth of the Avogadro constant, as a count:

    >>> from kuchka import Micromole
    >>> count = PerMole(6.02214076e23) * Micromole(1)
    >>> int(count)
    602214076000000000

    """
    return EntitiesPerAmount(to_exact(value) * PER_MOLE.scale, PER_MOLE)


ENTITIES_PER_AMOUNT_UNITS: Mapping[str, Callable[[Numeric], EntitiesPerAmount]] = (
    unit_table(
        "ENTITIES_PER_AMOUNT_UNITS",
        {
            PER_MOLE: PerMole,
        },
    )
)

__all__ = [
    "ENTITIES_PER_AMOUNT_UNITS",
    "PER_MOLE",
    "PerMole",
]
