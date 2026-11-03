"""Smoke-test Kuchka as an independently installed consumer dependency."""

from importlib.metadata import version
from importlib.util import find_spec
from sys import version_info

# Development tools must not leak into the runtime installation.
if find_spec("mypy") is not None:
    raise RuntimeError("mypy was unexpectedly installed as a runtime dependency")

# This dependency is required by Kuchka on Python versions below 3.12.
if version_info < (3, 12) and find_spec("typing_extensions") is None:
    raise RuntimeError("typing_extensions is missing from the runtime installation")

# Import through the public API.
from kuchka import AmpereHour, Ohm, Volt
from kuchka.units import HOUR

# Exercise a representative engineering calculation.
supply = Volt(3.7)
load = Ohm(148)
battery = AmpereHour(2)

current = supply / load
runtime = (battery / current).to(HOUR)

print(f"Installed Kuchka: {version('kuchka')}")
print(f"Current: {current}")
print(f"Battery runtime: {runtime}")