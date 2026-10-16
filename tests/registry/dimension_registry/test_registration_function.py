"""The registration function is internal."""

from __future__ import annotations

import pytest

import kuchka
from kuchka import quantities
from kuchka.quantities.base import registry


def test_the_function_is_not_exported_from_the_base_package() -> None:
    assert not hasattr(quantities.base, "register")


@pytest.mark.parametrize(
    "package", [kuchka, quantities, quantities.base, registry], ids=lambda p: p.__name__
)
def test_no_public_list_names_the_registration_function(package: object) -> None:
    exported = package.__all__  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]
    assert not any("register" in name for name in exported)


def test_the_registry_module_exports_nothing() -> None:
    assert registry.__all__ == []


def test_the_registration_function_is_private_by_name() -> None:
    assert hasattr(registry, "_register")
    assert not hasattr(registry, "register")
