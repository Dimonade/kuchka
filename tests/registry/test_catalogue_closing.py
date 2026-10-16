"""The registry closes only when every kind is catalogued."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from kuchka import Angle
from kuchka import Instant
from kuchka import Time
from kuchka.dimensions import ANGLE
from kuchka.dimensions import DIMENSIONLESS
from kuchka.dimensions import FREQUENCY
from kuchka.quantities.base import registry
from tests.support.synthetic import linear_kind
from tests.support.synthetic import modular_kind

if TYPE_CHECKING:
    from collections.abc import Callable


def test_closing_a_second_time_does_nothing() -> None:
    registry._close()  # noqa: SLF001
    assert registry._closed is True  # noqa: SLF001


@pytest.mark.parametrize(
    "make",
    [
        lambda: linear_kind("Unregistered", FREQUENCY),
        lambda: linear_kind("Unregistered", DIMENSIONLESS),
        lambda: modular_kind("Unregistered", ANGLE),
    ],
    ids=["linear", "dimensionless", "modular"],
)
def test_closing_with_an_unregistered_kind_is_refused(
    monkeypatch: pytest.MonkeyPatch, make: Callable[[], type]
) -> None:
    kind = make()
    monkeypatch.setattr(registry, "_closed", False)
    with pytest.raises(TypeError, match="Unregistered"):
        registry._close()  # noqa: SLF001
    assert registry._closed is False  # noqa: SLF001
    del kind


def test_closing_with_every_kind_registered_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(registry, "_closed", False)
    monkeypatch.setattr(registry, "_concrete_kinds", lambda: [Time, Angle, Instant])
    registry._close()  # noqa: SLF001
    assert registry._closed is True  # noqa: SLF001
