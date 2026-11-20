"""The third-party libraries that the integrations are tested against.

An integration imports nothing from the library it serves, and its tests do, so a
test environment without the library skips them, and an environment that promises the
library fails them: a tox environment names its libraries in `KUCHKA_LIBRARIES`.
"""

from __future__ import annotations

import importlib.util
import os

import pytest


def available(library: str) -> bool:
    """Return whether `library` can be imported here."""
    return importlib.util.find_spec(library) is not None


def required(library: str) -> bool:
    """Return whether this environment promises `library`, so a miss is a failure."""
    return library in os.environ.get("KUCHKA_LIBRARIES", "").split(",")


def require_or_skip(library: str) -> None:
    """Skip the test for a missing `library`, or fail it where one was promised."""
    if available(library):
        return
    if required(library):
        pytest.fail(f"{library} is promised by this environment and is not installed")
    pytest.skip(f"{library} is not installed")
