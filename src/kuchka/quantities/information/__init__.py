"""Quantity types for information and its rate."""

from __future__ import annotations

from kuchka.quantities.information import data
from kuchka.quantities.information import data_rate
from kuchka.quantities.information.data import *
from kuchka.quantities.information.data_rate import *

__all__: list[str] = []
__all__ += data.__all__
__all__ += data_rate.__all__
