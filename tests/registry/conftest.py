"""Fixtures for tests of the kind registry, which write to it while it is open."""

from __future__ import annotations

import pytest

from kuchka import Frequency
from kuchka import SampleRate
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import Dimension
from kuchka.quantities.base import registry
from tests.support.synthetic import REGISTRY_TABLES


@pytest.fixture
def open_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reopen the registry, with its own copy of every table, for one test."""
    monkeypatch.setattr(registry, "_closed", False)
    for name in REGISTRY_TABLES:
        monkeypatch.setattr(registry, name, dict(getattr(registry, name)))


@pytest.fixture
def novel() -> Dimension:
    """Return a dimension no shipped type has."""
    return Dimension(mass=3, angle=2)


@pytest.fixture
def contested_frequency(open_registry: None) -> None:
    """Make `Frequency` and `SampleRate`, real kinds, contested for one test."""
    del open_registry
    registry._DIMENSION_REGISTRY.pop(FREQUENCY)  # noqa: SLF001
    registry._SPECIALISATIONS.pop(SampleRate)  # noqa: SLF001
    registry._CONTESTED[FREQUENCY] = (Frequency, SampleRate)  # noqa: SLF001
