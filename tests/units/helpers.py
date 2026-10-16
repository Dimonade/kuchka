"""Helpers the unit tests share: the published units, and a made-up unit."""

from __future__ import annotations

import kuchka.units as published
from kuchka.dimensions import VOLTAGE
from kuchka.quantities.base import UnitDef
from kuchka.quantities.base.units import _Unit

PUBLISHED = {
    name: getattr(published, name)
    for name in published.__all__
    if isinstance(getattr(published, name), _Unit)
}


PUBLISHED_NAMES = list(PUBLISHED)


def _linear(**changes: object) -> UnitDef:
    fields: dict[str, object] = {
        "name": "volt",
        "symbol": "V",
        "scale": 1,
        "dimension": VOLTAGE,
        "aliases": ("v",),
        "words": ("volts",),
    }
    fields.update(changes)
    return UnitDef(
        str(fields["name"]),
        str(fields["symbol"]),
        fields["scale"],  # type: ignore[arg-type]
        fields["dimension"],  # type: ignore[arg-type]
        aliases=fields["aliases"],  # type: ignore[arg-type]
        words=fields["words"],  # type: ignore[arg-type]
    )
