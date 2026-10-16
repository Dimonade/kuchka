"""The registry closes when the package has been imported."""

from __future__ import annotations

import pytest

from kuchka import Frequency
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import registry
from kuchka.units import time

REGISTERED = registry._DIMENSION_REGISTRY  # noqa: SLF001 -- inspected, never modified


class _Rogue(LinearQuantity):
    dimension = FREQUENCY
    __slots__ = ()


def test_the_registry_is_closed_once_the_package_has_imported() -> None:
    assert registry._closed is True  # noqa: SLF001


def test_a_registration_after_the_close_is_refused() -> None:
    with pytest.raises(RuntimeError, match="registry is closed"):
        registry._register(TIME, time.Second.__class__)  # type: ignore[arg-type]  # noqa: SLF001  # ty: ignore[invalid-argument-type]


def test_a_new_type_cannot_claim_a_dimension_after_the_close() -> None:
    class Newcomer(LinearQuantity):
        dimension = FREQUENCY
        __slots__ = ()

    with pytest.raises(RuntimeError, match="Newcomer"):
        registry._register(FREQUENCY, Newcomer)  # noqa: SLF001


def test_even_re_registering_the_same_type_is_refused_after_the_close() -> None:
    with pytest.raises(RuntimeError, match="registry is closed"):
        registry._register(FREQUENCY, Frequency)  # noqa: SLF001


def test_a_refused_registration_leaves_the_registry_unchanged() -> None:
    before = dict(REGISTERED)
    with pytest.raises(RuntimeError):
        registry._register(FREQUENCY, _Rogue)  # noqa: SLF001
    assert before == REGISTERED


def test_closing_is_one_way() -> None:
    registry._close()  # noqa: SLF001
    assert registry._closed is True  # noqa: SLF001
