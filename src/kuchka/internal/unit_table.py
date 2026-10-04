"""The `*_UNITS` tables: unit text from outside the program to a unit constructor.

A table maps what a configuration file or specification calls a unit to the
constructor that builds it, so `VOLTAGE_UNITS["mV"](5)` is `Millivolt(5)`.
What a table accepts is data on the unit definitions it is built from:

- `symbol`, the display notation, and `aliases`, other symbols (`C`, `degC`, `u` for
  the dalton), are compared exactly after `normalize`: case matters, because it carries
  meaning in a symbol (`mV` and `MV` differ).
- `name`, such as `celsius`, and `words`, such as `degrees C`, are compared after
  `fold`, ignoring letter case, and a trailing plural `s` is tolerated, so
  `Degrees C` and `volts` both resolve.

A spelling must resolve to one unit.
Building a table raises `ValueError` if two units claim the same spelling, or if a
word could be read as another unit's plural, so a table that exists has no ambiguity.
A spelling that is not claimed raises `KeyError`, as for any mapping.
Iterating a table yields each unit's display symbol once, in definition order.
"""

from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterator
from collections.abc import Mapping
from typing import TYPE_CHECKING
from typing import Protocol
from typing import TypeVar

from kuchka.internal.spelling import fold
from kuchka.internal.spelling import normalize
from kuchka.internal.typing import override

if TYPE_CHECKING:
    from kuchka.numeric import Numeric

_Q = TypeVar("_Q")
_R = TypeVar("_R")
_PLURAL = "s"


class SpelledUnit(Protocol):
    """What a table needs to know about a unit, its spellings."""

    name: str
    symbol: str
    aliases: tuple[str, ...]
    words: tuple[str, ...]


class UnitTable(Mapping[str, Callable[["Numeric"], _Q]]):
    """A read-only mapping from the text of a unit to its constructor."""

    __slots__ = ("_entries", "_exact", "_label", "_words")

    def __init__(
        self,
        label: str,
        entries: Mapping[SpelledUnit, Callable[[Numeric], _Q]],
    ) -> None:
        """Index `entries`, raising `ValueError` if any spelling is ambiguous."""
        self._label = label
        self._entries = tuple(entries.items())
        self._exact: dict[str, tuple[SpelledUnit, Callable[[Numeric], _Q]]] = {}
        self._words: dict[str, tuple[SpelledUnit, Callable[[Numeric], _Q]]] = {}
        for unit, constructor in self._entries:
            for symbol in (unit.symbol, *unit.aliases):
                self._claim(self._exact, normalize(symbol), unit, constructor)
            for word in (unit.name, *unit.words):
                self._claim(self._words, fold(word), unit, constructor)
        self._check_words_against_symbols()
        self._check_plurals()

    def _claim(
        self,
        index: dict[str, tuple[SpelledUnit, Callable[[Numeric], _Q]]],
        spelling: str,
        unit: SpelledUnit,
        constructor: Callable[[Numeric], _Q],
    ) -> None:
        owner = index.setdefault(spelling, (unit, constructor))[0]
        if owner is not unit:
            msg = (
                f"{self._label}: {spelling!r} is claimed by both "
                f"{owner.name!r} and {unit.name!r}."
            )
            raise ValueError(msg)

    def _check_words_against_symbols(self) -> None:
        """No symbol may read as the case-folded word of a different unit."""
        for spelling, (unit, _) in self._exact.items():
            other = self._words.get(fold(spelling))
            if other is not None and other[0] is not unit:
                msg = (
                    f"{self._label}: the symbol {spelling!r} of {unit.name!r} reads "
                    f"as a word of {other[0].name!r}."
                )
                raise ValueError(msg)

    def _check_plurals(self) -> None:
        """No word may be another unit's word with a plural `s` added."""
        for word, (unit, _) in self._words.items():
            stem = self._words.get(word.removesuffix(_PLURAL))
            if word.endswith(_PLURAL) and stem is not None and stem[0] is not unit:
                msg = (
                    f"{self._label}: {word!r} of {unit.name!r} reads as the plural "
                    f"of {stem[0].name!r}."
                )
                raise ValueError(msg)

    @property
    def units(self) -> tuple[SpelledUnit, ...]:
        """The unit definitions in the table, in definition order."""
        return tuple(unit for unit, _ in self._entries)

    @override
    def __getitem__(self, spelling: object) -> Callable[[Numeric], _Q]:
        """Resolve `spelling` to a constructor, or raise `KeyError`."""
        if isinstance(spelling, str):
            exact = self._exact.get(normalize(spelling))
            if exact is not None:
                return exact[1]
            word = fold(spelling)
            found = self._words.get(word)
            if found is None and word.endswith(_PLURAL):
                found = self._words.get(word.removesuffix(_PLURAL))
            if found is not None:
                return found[1]
        raise KeyError(spelling)

    @override
    def __iter__(self) -> Iterator[str]:
        """Yield the display symbol of each unit, in definition order."""
        return (unit.symbol for unit, _ in self._entries)

    @override
    def __len__(self) -> int:
        """Return the number of units."""
        return len(self._entries)

    def map(
        self,
        label: str,
        transform: Callable[[Callable[[Numeric], _Q]], Callable[[Numeric], _R]],
    ) -> UnitTable[_R]:
        """Return a table of the same units, each constructor passed to `transform`.

        The spellings are those of the original, so a table derived from another
        accepts exactly the same text.
        """
        return UnitTable(
            label,
            {unit: transform(constructor) for unit, constructor in self._entries},
        )

    @override
    def __repr__(self) -> str:
        """Return the label and size."""
        return f"UnitTable({self._label!r}, {len(self)} units)"


def unit_table(
    label: str, entries: Mapping[SpelledUnit, Callable[[Numeric], _Q]]
) -> UnitTable[_Q]:
    """Build the table `label` from unit definitions and their constructors."""
    return UnitTable(label, entries)


__all__ = ["SpelledUnit", "UnitTable", "unit_table"]
