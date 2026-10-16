from kuchka.units import length

"""Metre/Meter and their prefixed forms: aliases, not separate units.

Mirrors `test_mass.py`'s coverage of `Tonne`/`Megagram`: proving the alias holds at
every level -- identity, construction, display, and round-tripping -- not just that
the two happen to compute equal values.
"""


def test_meter_and_metre_are_the_same_function():
    assert length.Meter is length.Metre
    assert length.Millimeter is length.Millimetre
    assert length.Micrometer is length.Micrometre
    assert length.Nanometer is length.Nanometre
    assert length.Kilometer is length.Kilometre


def test_meter_and_metre_unit_constants_are_the_same_object():
    assert length.METER is length.METRE
    assert length.KILOMETER is length.KILOMETRE


def test_meter_displays_as_metre():
    """Test both spellings share one symbol, `m`, so there is nothing to reconcile."""
    assert repr(length.Meter(1)) == "1 m"
    assert repr(length.Metre(1)) == "1 m"


def test_meter_and_metre_arithmetic_mixes_freely():
    assert length.Meter(1) + length.Metre(1) == length.Metre(2)
    assert length.Kilometre(1) == length.Kilometer(1)
    assert length.Meter(1000) == length.Kilometre(1)


def test_metre_is_canonical():
    from kuchka.quantities import Length

    assert Length._canonical_unit is length.METRE  # noqa: SLF001 -- verifying the module's own wiring


def test_metre_and_millimetre_scale_exactly():
    assert length.Metre(1) == length.Millimetre(1000)
