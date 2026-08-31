"""Metre/Meter and their prefixed forms: aliases, not separate units.

Mirrors `test_mass.py`'s coverage of `Tonne`/`Megagram`: proving the alias holds at
every level -- identity, construction, display, and round-tripping -- not just that
the two happen to compute equal values.
"""

from kuchka import Kilometer
from kuchka import Kilometre
from kuchka import Meter
from kuchka import Metre
from kuchka import Micrometer
from kuchka import Micrometre
from kuchka import Millimeter
from kuchka import Millimetre
from kuchka import Nanometer
from kuchka import Nanometre
from kuchka.units import KILOMETER
from kuchka.units import KILOMETRE
from kuchka.units import METER
from kuchka.units import METRE


def test_meter_and_metre_are_the_same_function():
    assert Meter is Metre
    assert Millimeter is Millimetre
    assert Micrometer is Micrometre
    assert Nanometer is Nanometre
    assert Kilometer is Kilometre


def test_meter_and_metre_unit_constants_are_the_same_object():
    assert METER is METRE
    assert KILOMETER is KILOMETRE


def test_meter_displays_as_metre():
    """Test both spellings share one symbol, `m`, so there is nothing to reconcile."""
    assert repr(Meter(1)) == "1 m"
    assert repr(Metre(1)) == "1 m"


def test_meter_and_metre_arithmetic_mixes_freely():
    assert Meter(1) + Metre(1) == Metre(2)
    assert Kilometre(1) == Kilometer(1)
    assert Meter(1000) == Kilometre(1)


def test_metre_is_canonical():
    from kuchka.quantities import Length

    assert Length._canonical_unit is METRE  # noqa: SLF001 -- verifying the module's own wiring


def test_metre_and_millimetre_scale_exactly():
    assert Metre(1) == Millimetre(1000)
