"""Not a pytest file directly-- run through mypy and pyright, like `should_fail.py`.

The static contract of the `kuchka.msgspec` hooks: a decoded struct is the struct that
was asked for, the field is the exact quantity type, and the constructor takes the
annotated type, so a string there is reported by both checkers.
"""

import msgspec

from kuchka import Ampere
from kuchka import Current
from kuchka import Volt
from kuchka import Voltage
from kuchka.msgspec import kuchka_dec_hook
from kuchka.msgspec import kuchka_enc_hook


class Payload(msgspec.Struct):
    """A voltage."""

    v: Voltage


# Decoding returns the struct that was asked for.
decoded: Payload = msgspec.json.decode(
    b'{"v": "4.2 V"}', type=Payload, dec_hook=kuchka_dec_hook
)  # OK
encoded: bytes = msgspec.json.encode(decoded, enc_hook=kuchka_enc_hook)  # OK

# The field is the exact type.
v: Voltage = decoded.v  # OK
wrong_field: Current = decoded.v  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# The constructor takes the annotated type.
from_instance = Payload(v=Volt(4.2))  # OK
_string_constructor = Payload(v="4.2 V")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
_wrong_instance = Payload(v=Ampere(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
