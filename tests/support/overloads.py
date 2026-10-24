"""The static overloads of every linear type, read back so a test can check them.

`@overload` declarations are the typing contract of `*` and `/`: the result type a
type checker infers for a pair of operand types.
Reading them at runtime lets a test hold that contract against what the code does.
"""

from __future__ import annotations

import typing
from dataclasses import dataclass

from kuchka import quantities
from tests.support.families import FAMILIES

OPERATIONS = ("__mul__", "__truediv__")
SYMBOL = {"__mul__": "*", "__truediv__": "/"}
NOT_A_QUANTITY_OPERAND = ("Numeric", "object")
WEAK_RESULT = "LinearQuantity | Fraction"
"""The result of the fallback overload, which declares no pair."""
FAMILY_OF = {family.quantity: family for family in FAMILIES}


@dataclass(frozen=True)
class Overload:
    """One declared overload: `left <operation> right` has the type `result`."""

    left: type
    operation: str
    right: type
    result: type | None
    """The result type, or `None` for a plain `Fraction`."""

    @property
    def id(self) -> str:
        """A readable test id, such as `Voltage*Current->Power`."""
        result = "Fraction" if self.result is None else self.result.__name__
        symbol = SYMBOL[self.operation]
        return f"{self.left.__name__}{symbol}{self.right.__name__}->{result}"


def declared_overloads() -> tuple[Overload, ...]:
    """Return every overload of `*` and `/` that names two quantity types."""
    found = []
    for cls in FAMILY_OF:
        for operation in OPERATIONS:
            implementation = vars(cls).get(operation)
            if implementation is None:
                continue
            for overload in typing.get_overloads(implementation):
                other = overload.__annotations__.get("other")
                result = overload.__annotations__.get("return")
                if other in NOT_A_QUANTITY_OPERAND or result == WEAK_RESULT:
                    continue
                right = getattr(quantities, other)
                if result == "Fraction":
                    found.append(Overload(cls, operation, right, None))
                elif result in vars(quantities):
                    found.append(
                        Overload(cls, operation, right, getattr(quantities, result))
                    )
    return tuple(found)


OVERLOADS = declared_overloads()
OVERLOAD_IDS = tuple(overload.id for overload in OVERLOADS)
