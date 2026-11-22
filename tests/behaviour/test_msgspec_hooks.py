"""The `msgspec` hooks read and write quantities, and leave everything else alone.

The reading and the writing are `kuchka.wire`, tested once for every input in the tests
of `wire`; this module covers what the hooks add: the `msgspec` protocol, the
validation error with its path, containers and formats, composition with the hooks of
an application, and the schema.
"""

from __future__ import annotations

import subprocess
import sys
from decimal import Decimal
from fractions import Fraction
from typing import Any

import pytest

from kuchka import Current
from kuchka import Length
from kuchka import Proportion
from kuchka import Temperature
from kuchka import Voltage
from kuchka.units import current
from kuchka.units import proportion
from kuchka.units import thermal
from kuchka.units.archaic.russian import length as russian_length
from kuchka.units.electromagnetics import voltage
from tests.support.libraries import require_or_skip

require_or_skip("msgspec")

import msgspec
import msgspec.msgpack

from kuchka.msgspec import kuchka_dec_hook
from kuchka.msgspec import kuchka_enc_hook
from kuchka.msgspec import kuchka_schema_hook
from kuchka.msgspec import make_dec_hook


class Payload(msgspec.Struct):
    """A voltage, and fields of every place a quantity can sit."""

    v: Voltage
    optional: Voltage | None = None
    many: list[Voltage] = msgspec.field(default_factory=list)
    by_name: dict[str, Voltage] = msgspec.field(default_factory=dict)
    duty: Proportion | None = None
    temperature: Temperature | None = None


def _decode(raw: bytes) -> Payload:
    return msgspec.json.decode(raw, type=Payload, dec_hook=kuchka_dec_hook)


@pytest.mark.parametrize(
    "raw",
    [
        b'{"v": "2800 mV"}',
        b'{"v": "2.8 V"}',
        b'{"v": "14/5 V"}',
        b'{"v": {"value": "2800", "unit": "mV"}}',
    ],
)
def test_a_field_is_the_quantity_whatever_the_payload_holds(raw: bytes) -> None:
    payload = _decode(raw)
    assert payload.v == voltage.Volt(Decimal("2.8"))
    assert isinstance(payload.v, Voltage)


def test_a_payload_reads_in_the_unit_that_was_written() -> None:
    assert _decode(b'{"v": "7/3 mV"}').v.unit is voltage.MILLIVOLT


def test_a_proportion_reads_a_json_number_too() -> None:
    assert _decode(b'{"v": "1 V", "duty": 0.25}').duty == proportion.Ratio(
        Fraction(1, 4)
    )
    assert _decode(b'{"v": "1 V", "duty": "25 %"}').duty == proportion.Percent(25)


@pytest.mark.parametrize(
    "raw",
    [
        b'{"v": 3.3}',
        b'{"v": 3}',
        b'{"v": true}',
        b'{"v": null}',
        b'{"v": "3.3"}',
        b'{"v": "five volts"}',
        b'{"v": "150 mA"}',
        b'{"v": {"value": "3"}}',
        b'{"v": "1 V", "duty": "7 V"}',
        b'{"v": "1 V", "temperature": "-300 \\u00b0C"}',
    ],
)
def test_a_value_that_is_no_quantity_is_a_validation_error(raw: bytes) -> None:
    with pytest.raises(msgspec.ValidationError):
        _decode(raw)


def test_the_validation_error_names_the_field_and_says_what_to_write() -> None:
    with pytest.raises(msgspec.ValidationError, match=r"at `\$\.v`") as raised:
        _decode(b'{"v": 3.3}')
    assert 'such as "5 V"' in str(raised.value)
    with pytest.raises(msgspec.ValidationError, match=r"at `\$\.many\[1\]`"):
        _decode(b'{"v": "1 V", "many": ["1 V", 2.5]}')


def test_a_field_works_inside_containers_and_unions() -> None:
    many = b'["3 V", {"value": "2", "unit": "mV"}]'
    payload = _decode(
        b'{"v": "1 V", "optional": "2 V", "many": ' + many + b","
        b' "by_name": {"a": "1/3 V"}, "temperature": "-40 \\u00b0C"}'
    )
    assert payload.optional == voltage.Volt(2)
    assert payload.many == [voltage.Volt(3), voltage.Millivolt(2)]
    assert payload.by_name == {"a": voltage.Volt(1) / 3}
    assert payload.temperature == thermal.Celsius(-40)
    assert _decode(b'{"v": "1 V", "optional": null}').optional is None


def test_encoding_writes_the_text_and_decoding_reads_it_back_exactly() -> None:
    payload = Payload(
        v=voltage.Millivolt(Fraction(7, 3)),
        many=[voltage.Volt(3)],
        duty=proportion.Percent(25),
    )
    raw = msgspec.json.encode(payload, enc_hook=kuchka_enc_hook)
    written = msgspec.json.decode(raw)
    assert written["v"] == "7/3 mV"
    assert written["many"] == ["3 V"]
    assert written["duty"] == "25 %"
    assert _decode(raw) == payload
    assert _decode(raw).v.unit is voltage.MILLIVOLT


def test_other_formats_carry_the_same_text() -> None:
    payload = Payload(v=voltage.Millivolt(Fraction(7, 3)))
    packed = msgspec.msgpack.encode(payload, enc_hook=kuchka_enc_hook)
    restored = msgspec.msgpack.decode(packed, type=Payload, dec_hook=kuchka_dec_hook)
    assert restored == payload
    builtins = msgspec.to_builtins(payload, enc_hook=kuchka_enc_hook)
    assert builtins["v"] == "7/3 mV"
    converted = msgspec.convert(builtins, type=Payload, dec_hook=kuchka_dec_hook)
    assert converted == payload


def test_a_quantity_is_decoded_at_the_top_level_too() -> None:
    value = msgspec.json.decode(b'"7/3 mV"', type=Voltage, dec_hook=kuchka_dec_hook)
    assert value == voltage.Millivolt(Fraction(7, 3))


def test_the_hooks_leave_what_is_not_a_quantity_to_the_next_hook() -> None:
    with pytest.raises(NotImplementedError):
        kuchka_dec_hook(complex, "1+2j")
    with pytest.raises(NotImplementedError):
        kuchka_dec_hook(int, 5)
    with pytest.raises(NotImplementedError):
        kuchka_enc_hook(1 + 2j)
    with pytest.raises(NotImplementedError):
        kuchka_enc_hook(voltage.Volt)
    with pytest.raises(NotImplementedError):
        kuchka_schema_hook(complex)


def test_the_hooks_compose_with_the_hooks_of_an_application() -> None:
    class Mixed(msgspec.Struct):
        c: complex
        v: Voltage

    def dec_hook(target: type, obj: Any) -> Any:  # noqa: ANN401
        try:
            return kuchka_dec_hook(target, obj)
        except NotImplementedError:
            if target is complex:
                return complex(obj)
            raise

    def enc_hook(obj: object) -> Any:  # noqa: ANN401
        try:
            return kuchka_enc_hook(obj)
        except NotImplementedError:
            if isinstance(obj, complex):
                return str(obj)
            raise

    raw = b'{"c": "1+2j", "v": "1 V"}'
    value = msgspec.json.decode(raw, type=Mixed, dec_hook=dec_hook)
    assert value == Mixed(1 + 2j, voltage.Volt(1))
    assert msgspec.json.encode(value, enc_hook=enc_hook) == b'{"c":"(1+2j)","v":"1 V"}'


def test_an_archaic_unit_is_read_where_the_hook_allows_it() -> None:
    class Plot(msgspec.Struct):
        side: Length

    raw = b'{"side": "3 arshin"}'
    with pytest.raises(msgspec.ValidationError, match="archaic"):
        msgspec.json.decode(raw, type=Plot, dec_hook=kuchka_dec_hook)
    hook = make_dec_hook(allow_archaic=True)
    assert msgspec.json.decode(
        raw, type=Plot, dec_hook=hook
    ).side == russian_length.Arshin(3)


def test_a_policy_that_is_no_policy_fails_when_the_hook_is_made() -> None:
    with pytest.raises(TypeError, match="ArchaicPolicy"):
        make_dec_hook(allow_archaic="yes")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_msgspec_cannot_make_a_schema_without_the_hook_and_can_with_it() -> None:
    with pytest.raises(TypeError, match="schema_hook"):
        msgspec.json.schema(Payload)
    schema = msgspec.json.schema(Payload, schema_hook=kuchka_schema_hook)
    properties = schema["$defs"]["Payload"]["properties"]
    assert properties["v"]["type"] == "string"
    assert "Voltage" in properties["v"]["description"]
    assert properties["v"]["examples"] == ["5 V"]
    assert properties["many"]["items"]["type"] == "string"
    assert {"type": "string"} in properties["duty"]["anyOf"][0]["anyOf"]


@pytest.mark.parametrize("value", [3.3, Decimal("3.3"), 3])
def test_the_hook_refuses_a_number_for_a_quantity_that_needs_a_unit(
    value: object,
) -> None:
    with pytest.raises(ValueError, match="has no unit"):
        kuchka_dec_hook(Voltage, value)
    assert kuchka_dec_hook(Proportion, value) == proportion.Ratio(Decimal(str(value)))


def test_an_instance_the_hook_is_given_passes_through() -> None:
    value = current.Ampere(1)
    assert kuchka_dec_hook(Current, value) is value


def test_importing_kuchka_loads_no_integration_library() -> None:
    program = (
        "import sys\n"
        "import kuchka\n"
        "print([n for n in ('msgspec', 'pydantic', 'attrs') if n in sys.modules])\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", program], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "[]"


def test_a_missing_msgspec_says_how_to_install_it() -> None:
    program = "import sys\nsys.modules['msgspec'] = None\nimport kuchka.msgspec\n"
    result = subprocess.run(
        [sys.executable, "-c", program], capture_output=True, text=True, check=False
    )
    assert result.returncode != 0
    assert "kuchka[msgspec]" in result.stderr
