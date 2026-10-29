"""Quantity types for how heat changes a temperature."""

from __future__ import annotations

from kuchka.quantities.thermodynamics import heating_rate
from kuchka.quantities.thermodynamics.heating_rate import *

__all__: list[str] = []
__all__ += heating_rate.__all__
