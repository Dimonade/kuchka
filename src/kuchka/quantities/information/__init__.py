"""Quantity types for information: Data and DataRate.

    from kuchka import Data, DataRate

Information is an axis of its own, so a data rate is not interchangeable with a
`Frequency`, a `SampleRate`, or a `BaudRate`.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package composes its own ``__all__`` from theirs, and `kuchka.quantities` composes
its own from this one's.
A new leaf module needs three lines here: its module import, its wildcard import, and
its ``__all__ +=``.
"""

from __future__ import annotations

from kuchka.quantities.information import data
from kuchka.quantities.information import data_rate
from kuchka.quantities.information.data import *
from kuchka.quantities.information.data_rate import *

__all__: list[str] = []
__all__ += data.__all__
__all__ += data_rate.__all__
