"""Hooks that let `msgspec` read and write quantities.

    import msgspec

    from kuchka import Voltage
    from kuchka.msgspec import kuchka_dec_hook
    from kuchka.msgspec import kuchka_enc_hook


    class Payload(msgspec.Struct):
        v: Voltage


    raw = b'{"v": "4.2 V"}'
    payload = msgspec.json.decode(raw, type=Payload, dec_hook=kuchka_dec_hook)
    msgspec.json.encode(payload, enc_hook=kuchka_enc_hook)

`msgspec` calls a decoding hook for a field whose type it does not know, and an
encoding hook for a value it cannot write; these are those hooks, `kuchka.wire.load` and
`kuchka.wire.dump` for the quantity types.
`kuchka_dec_hook(type, obj)` reads what the payload holds for a field of a quantity
type: text such as `"4.2 V"` or `"1/3 V"`, a mapping of a `"value"` and a `"unit"`, and
for a `Proportion` a number.
`kuchka_enc_hook(obj)` writes a quantity as its text, which the decoding hook reads
back exactly.
Every refusal of the decoding hook is a `ParseError`, a `ValueError`, which `msgspec`
reports as its `ValidationError` with the path of the field.

Both hooks raise `NotImplementedError` for what is not theirs, which is the protocol
`msgspec` defines, so they compose with the hooks of an application:

    def dec_hook(type, obj):
        try:
            return kuchka_dec_hook(type, obj)
        except NotImplementedError:
            return my_dec_hook(type, obj)

`kuchka_schema_hook(type)` describes a quantity type to `msgspec.json.schema`, which
refuses a type it does not know without one: a string whose description names the
quantity, and for a `Proportion` also a number.
`make_dec_hook(allow_archaic=True)` returns a decoding hook that reads archaic units,
as `parse` does with the same argument.

The module imports `msgspec`, an extra of the package (`kuchka[msgspec]`); the quantity
classes carry no `msgspec` code, and `import kuchka` loads none.

Static types
------------
The attribute is the exact quantity type under `mypy` and `pyright`, and
`msgspec.json.decode(..., type=Payload)` is a `Payload`.

Examples
--------
>>> import msgspec
>>> from kuchka import Volt
>>> from kuchka import Voltage
>>> Payload = msgspec.defstruct("Payload", [("v", Voltage)])
>>> payload = msgspec.json.decode(
...     b'{"v": "4.2 V"}', type=Payload, dec_hook=kuchka_dec_hook
... )
>>> payload.v == Volt(4.2)
True
>>> msgspec.json.encode(payload, enc_hook=kuchka_enc_hook)
b'{"v":"4.2 V"}'

A value that is no voltage is a validation error with the path of the field:

>>> try:
...     msgspec.json.decode(b'{"v": 3.3}', type=Payload, dec_hook=kuchka_dec_hook)
... except msgspec.ValidationError as error:
...     print(error)  # doctest: +ELLIPSIS
3.3 has no unit, ... - at `$.v`

"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import TypeGuard

try:
    import msgspec  # noqa: F401 -- the module is for installs with msgspec
except (
    ImportError
) as exc:  # pragma: no cover -- the module is for installs with msgspec
    msg = "kuchka.msgspec needs msgspec: `pip install kuchka[msgspec]`."
    raise ImportError(msg) from exc

from kuchka.internal.reading import ArchaicPolicy
from kuchka.internal.reading import archaic_policy_of
from kuchka.internal.wire_schema import json_schema
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.wire import dump
from kuchka.wire import load

if TYPE_CHECKING:
    from collections.abc import Callable


def _is_quantity_type(target: object) -> TypeGuard[type[_ScalarStorage[Any]]]:
    """Return whether `target` is a quantity type, the only kind these hooks serve."""
    return isinstance(target, type) and issubclass(target, _ScalarStorage)


def make_dec_hook(
    *, allow_archaic: ArchaicPolicy | bool = ArchaicPolicy.Deny
) -> Callable[[type, Any], Any]:
    """Return a decoding hook for `msgspec` that reads archaic units as asked.

    Parameters
    ----------
    allow_archaic : ArchaicPolicy or bool, optional
        Whether the hook reads archaic units, as `parse` does.

    Returns
    -------
    Callable
        A `dec_hook` that reads a quantity type as `kuchka.wire.load` does and raises
        `NotImplementedError` for every other type.

    Raises
    ------
    TypeError
        `allow_archaic` is neither an `ArchaicPolicy` nor a `bool`.

    """
    policy = archaic_policy_of(allow_archaic)

    def dec_hook(target: type, obj: Any) -> Any:  # noqa: ANN401 -- msgspec's hook type
        if not _is_quantity_type(target):
            raise NotImplementedError
        return load(obj, target, allow_archaic=policy)

    return dec_hook


kuchka_dec_hook = make_dec_hook()
"""The `dec_hook` for `msgspec` decoding: it reads the quantity types, and raises
`NotImplementedError` for every other type."""


def kuchka_enc_hook(obj: object) -> Any:  # noqa: ANN401 -- msgspec's hook type
    """Write a quantity as its text, for the `enc_hook` of `msgspec` encoding.

    Parameters
    ----------
    obj : object
        A value `msgspec` cannot write itself.

    Returns
    -------
    str
        `kuchka.wire.dump(obj)` for a quantity.

    Raises
    ------
    NotImplementedError
        `obj` is no quantity, which lets the hooks of an application take it.

    """
    if isinstance(obj, _ScalarStorage):
        return dump(obj)
    raise NotImplementedError


def kuchka_schema_hook(target: type) -> dict[str, Any]:
    """Describe a quantity type for `msgspec.json.schema`.

    Parameters
    ----------
    target : type
        A type `msgspec` does not know.

    Returns
    -------
    dict
        The JSON Schema of the quantity type: a string that names it, and for a
        `Proportion` also a number.

    Raises
    ------
    NotImplementedError
        `target` is no quantity type.

    """
    if not _is_quantity_type(target):
        raise NotImplementedError
    return json_schema(target)


__all__ = ["kuchka_dec_hook", "kuchka_enc_hook", "kuchka_schema_hook", "make_dec_hook"]
