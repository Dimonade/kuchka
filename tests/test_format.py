from __future__ import annotations

from kuchka import Celsius
from kuchka import Volt
from kuchka.units import MILLIVOLT


def test_empty_format_spec_matches_repr() -> None:
    assert f"{Volt(4.2)}" == repr(Volt(4.2))
    assert format(Volt(4.2), "") == repr(Volt(4.2))


def test_format_spec_applies_to_the_magnitude_only() -> None:
    assert f"{Volt(4.2):.2f}" == "4.20 V"
    assert f"{Volt(4):.0f}" == "4 V"


def test_format_spec_respects_display_unit() -> None:
    voltage = Volt(1).to(MILLIVOLT)
    assert f"{voltage:.1f}" == "1000.0 mV"


def test_temperature_format_spec() -> None:
    assert f"{Celsius(20.5):.1f}" == "20.5 \u00b0C"


def test_format_spec_of_zero() -> None:
    assert f"{Volt(0):.2f}" == "0.00 V"
