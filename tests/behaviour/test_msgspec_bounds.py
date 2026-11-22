"""A `msgspec` struct limits a quantity field with `Bounds.check` in `__post_init__`."""

from __future__ import annotations

import pytest

from kuchka import BoundsError
from kuchka import Voltage
from kuchka.bounds import Bounds
from kuchka.units.electromagnetics import voltage
from tests.support.libraries import require_or_skip

require_or_skip("msgspec")

import msgspec

from kuchka.msgspec import kuchka_dec_hook

SUPPLY = Bounds(gt=voltage.Volt(0), le=voltage.Volt(60))


class Payload(msgspec.Struct):
    """A bounded voltage."""

    v: Voltage

    def __post_init__(self) -> None:
        """Check the range once the field is read."""
        SUPPLY.check(self.v)


def test_a_value_within_the_bounds_decodes() -> None:
    payload = msgspec.json.decode(
        b'{"v": "12 V"}', type=Payload, dec_hook=kuchka_dec_hook
    )
    assert payload.v == voltage.Volt(12)


def test_a_value_outside_the_bounds_is_a_validation_error_that_says_why() -> None:
    with pytest.raises(msgspec.ValidationError, match="61 V is above 60 V"):
        msgspec.json.decode(b'{"v": "61 V"}', type=Payload, dec_hook=kuchka_dec_hook)


def test_the_constructor_raises_the_bounds_error_itself() -> None:
    with pytest.raises(BoundsError, match="61 V is above 60 V"):
        Payload(voltage.Volt(61))
