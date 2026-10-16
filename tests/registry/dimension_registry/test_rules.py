"""The rules of registration, applied while the registry is open."""

from __future__ import annotations

import pytest

from kuchka import Frequency
from kuchka.dimensions import FREQUENCY
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import registry

REGISTERED = registry._DIMENSION_REGISTRY  # noqa: SLF001 -- inspected, never modified


class _Rogue(LinearQuantity):
    dimension = FREQUENCY
    __slots__ = ()


@pytest.mark.usefixtures("open_registry")
def test_a_second_type_for_a_registered_dimension_is_refused() -> None:
    with pytest.raises(TypeError, match="already registered"):
        registry._register(FREQUENCY, _Rogue)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_registering_the_same_type_again_is_not_an_error() -> None:
    registry._register(FREQUENCY, Frequency)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_refused_second_type_leaves_the_first_in_place() -> None:
    with pytest.raises(TypeError):
        registry._register(FREQUENCY, _Rogue)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[FREQUENCY] is Frequency  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_an_open_registry_accepts_a_new_dimension() -> None:
    novel = FREQUENCY * FREQUENCY

    class PerSecondSquared(LinearQuantity):
        dimension = novel
        __slots__ = ()

    registry._register(novel, PerSecondSquared)  # noqa: SLF001
    assert registry._DIMENSION_REGISTRY[novel] is PerSecondSquared  # noqa: SLF001
    assert novel not in REGISTERED
