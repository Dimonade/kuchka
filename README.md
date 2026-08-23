# kuchka

A small pile of physically-typed engineering units for Python.

_v0.1 covers Voltage, Current, Power, Resistance, and Temperature -- deliberately nothing else yet._

```python
from kuchka import Volt, Milliampere

voltage = Volt(4.2)
current = Milliampere(150)
power = voltage * current          # -> Power(0.63 W), typed and computed automatically
```

## Why

Passing raw floats through an engineering pipeline makes unit mistakes easy to write and hard to catch.
The code stays syntactically valid even when it's semantically wrong.
This library makes the physically-typed version of the code no harder to write than the untyped one, so there's no reason to reach for a naked `float` instead.

```python
def analyse_voltage(voltage: Voltage) -> Report: ...

analyse_voltage(4.2)          # rejected by mypy/ty, and again at runtime
analyse_voltage(Ampere(2))    # rejected by mypy/ty, and again at runtime
analyse_voltage(Volt(4.2))    # the only thing that type-checks
```

## Design choices, and why

- **`Decimal`, not `float`, is the internal representation.**
  SI prefixes are powers of ten, and powers of ten are exact in `Decimal` but usually _not_ exact in binary `float`. `Volt(1) + Millivolt(500) == Volt(1.5)` is true by construction, not by lucky rounding.
- **Unit constructors are plain functions, not classes.**
  `Volt(4.2)` returns a `Voltage` -- there is no `Volt` type to accidentally `isinstance()`-check against.
  This sidesteps the classic subclass/`__new__` gotcha where `isinstance(Volt(5), Volt)` is `False` and surprises people.
- **A hand-written overload table, not a generated one -- yet.**
  The runtime arithmetic (the quantity engine and its dimension algebra) is fully general:
  it derives any product/quotient from exponent-vector algebra, and would work for a much larger vocabulary.
  But Python's type checkers can't infer "Voltage times Current is Power" from that general algebra -- they only know because each pairing (Ohm's law and the power triangle, six pairs total) is spelled out as an explicit `@overload`.
  This is intentional and tracked as a decision, not a shortcut:
  the moment this vocabulary grows past hand-maintainable size, these overloads are exactly what a generator would need to emit.
  See "Open questions" below.
- **`Temperature` is a separate, smaller type from everything else.**
  Absolute temperature is affine, not linear -- `20 degC + 5 degC` isn't a meaningful operation the way `5V + 3V` is.
  `Temperature` supports addition/subtraction with a `TemperatureDelta` and subtraction between two `Temperature`s (producing a `TemperatureDelta`), but not addition of two `Temperature`s, and no scalar multiplication at all -- for either Celsius or Kelvin.
  See the module docstring next to `Temperature` for the reasoning and the deliberately-not-taken alternative (a Kelvin-specific ratio-scale type).
- **`.to(Unit)` uses Python names, never unit strings.**
  There is no `voltage.to("mV")` anywhere in this library.
- **Cross-type arithmetic is rejected statically, not just at runtime.**
  `Volt(5) + Ampere(2)` and `Volt(5) + 4.2` are both mypy errors, not only `InvalidMeasurementError`/`IncompatibleDimensionError` at runtime.
  This falls out of typing the base arithmetic methods against `Self` rather than `object`, so each quantity type only ever type-checks arithmetic against its own kind, without needing a per-subclass override.
  See "Known limitations" for where this currently falls short under `ty`.

## Comparison to existing tools

This is not the first attempt at physical quantities in Python.
A non-exhaustive list, roughly by how likely you are to already have one installed:
Pint, astropy.units, physipy, unyt, forallpeople, numericalunits, Unum, `quantities`, `units`, `unitpy`, and impunity.
Anyone proposing another one owes an honest answer to "why not just use Pint", the same way a new `uom`-style crate in Rust would owe an answer to "why not just use `uom`".

**The uncomfortable empirical starting point.**
Pint has existed since roughly 2012.
Despite that, more than a decade of engineering work across healthcare, finance, and secure embedded devices has produced essentially
zero sightings of any of these libraries in ordinary, non-scientific Python code.
What actually gets written instead is `voltage_mv`, `temperature_c`, `time_ms`, or a small home-grown newtype -- not because (probably) engineers do not know these libraries exist, but because (I think) none of the existing ones seem to have made the safe path more comfortable than the naming-convention path.
That is the problem kuchka is trying to solve, and it is worth being honest that kuchka has not proven it solves it either:
it has no adoption history to point to.
The claim here is about mechanism (why the existing shape might explain the non-adoption), not a guarantee that a different shape fixes it.

**Where the existing libraries put the friction.**
Compare constructing the same value two ways:

```python
# Pint / physipy: a registry, and a unit looked up on or from it
ureg = pint.UnitRegistry()
voltage = 3 * ureg.volt + 40 * ureg.millivolt

# kuchka: the unit is the constructor
voltage = Volt(3) + Millivolt(40)
```

Both compute the same answer.
The difference is what stands between the number and the result:

- **Pint** is the mature, general-purpose default:
  a huge unit vocabulary, NumPy/Pandas integration, unit parsing from strings (`ureg.meter`, `"3 m"`), and one generic `Quantity` type used for   everything.
  That generality is the entire point of Pint, and is not something `kuchka` is trying to replicate.
- **physipy** has a similar shape to Pint with a smaller core (`Dimension` and `Quantity`, two classes total), but units are still retrieved   through a dict-like registry (`units["nm"]`), and the result of any operation is still the same generic `Quantity` type regardless of what it physically represents.
- **`units`** and **`unitpy`** construct a unit from a string (`unit("m")`, `U("km")`), which means the unit's spelling is part of the runtime API surface, and a typo in that string is a runtime surprise a type checker cannot see.
- **impunity** is the closest in spirit to kuchka's static-first goal, and worth knowing about specifically for that reason:
  physical units live in string annotations on function signatures (`def speed(distance: "m", time: "s") -> "m/s"`), checked and rewritten at import time via PEP 593, with zero runtime cost once that check has run.
  That is a genuinely different, and in some ways more efficient, trade-off -- the cost is that the "unit" is a string inside an annotation rather than an ordinary Python type you can construct, return, and pass around like any other object.
- **kuchka** makes the unit an ordinary Python name:
  `isinstance(Volt(5), Voltage)` works with no registry, no plugin, and no decorator rewriting your function body.
  `mypy`/`ty` understand the arithmetic because it is expressed as ordinary overloads on an ordinary class, not because they were taught a new annotation vocabulary.
  The trade-off going the other way: a deliberately small, hand-maintained unit vocabulary, and no array/NumPy support at all yet (see "What this is not (yet)").

**The gap this is actually aimed at.**
Not "Python has no unit libraries" -- it very obviously does.
The narrower claim is: physical quantities should be able to be ordinary, boring Python types that a type checker already understands, without an engineer ever having to carry a registry, spell a unit as a string, or learn a new annotation syntax to get there.
Whether that narrower shape is *also* the missing ingredient for adoption, versus adoption requiring something else entirely (habit, deadlines, nobody asking for it), is genuinely an open question -- `kuchka` is a bet on the first explanation, not a proof of it.

## What this is not (yet)

- No Length, Mass, Time, or any other SI base quantity beyond what Voltage/Current/Power/Resistance/Temperature need.
- No NumPy/Pandas integration --
  `Decimal` doesn't vectorize into `ndarray` cleanly, and per-sample scalar wrapping is the wrong shape for high-rate acquisition.
  The intended pattern for now: buffer raw floats at the acquisition boundary, convert once you have a value worth reasoning about, not once per raw sample in a hot loop.
- No JSON/DB persistence layer yet.
  When it's added, the rule is: the _storage_ format may use a unit string (e.g. `{"value": 4.2, "unit": "V"}`), because that's not the application-facing API -- loading it back must reconstruct a typed measurement, never hand back a bare number.
- No autogenerated prefix modules.
  `Microvolt`/`Millivolt`/`Volt`/`Kilovolt` etc. are hand-written per dimension for now -- few enough that this is still less code than a codegen pipeline would be.

## Known limitations

- **`ty` does not yet enforce the `Self`-narrowed arithmetic across sibling quantity types the way `mypy --strict` does.**
  `Volt(5) + Ampere(2)` is a `mypy --strict` error but is currently accepted by `ty`;
  both tools agree on naked-number arithmetic (`Volt(5) + 4.2`) and on the `Temperature` cases.
  This is tracked in the test suite rather than hidden: search for "not (yet) flagged by ty" in the test files for the exact cases and the reasoning.
- **The dimension vocabulary is small on purpose.**
  `Resistance * Resistance` and similar mathematically-valid-but-unregistered products raise `UnrepresentableDimensionError` at runtime rather than returning a typed result.
  mypy/ty do not catch this ahead of time, since the fallback overload on each quantity type has to accept `object` to stay compatible with the base class signature.
- **No array or NumPy/Pandas support**, and no persistence layer -- see "What this is not (yet)" above.

## Package layout

_Subject to change as the library settles down on design._

```text
src/kuchka/
    dimensions.py       exponent-vector dimensional algebra
    numeric.py           strict coercion of int/float/Decimal/Fraction into Decimal
    errors.py             the exception hierarchy
    quantities/
        base.py            the quantity engine (LinearQuantity, UnitDef, the dimension registry)
        electrical.py     Voltage, Current, Power, Resistance and their overload tables
        thermal.py        TemperatureDelta
    units/
        voltage.py, current.py, resistance.py, power.py
                            one module per dimension's prefix constructors
    temperature.py      the affine Temperature type, plus Kelvin/Celsius constructors
```

Application code should only ever need the top-level `kuchka` package -- everything under `quantities/`, `units/`, and the internals of `temperature.py` is implementation detail, re-exported for convenience but not meant to be imported piecemeal.

## Development

### `uv`

TODO: Spell it out.

### `pip`

```bash
pip install -e .
pip install pytest mypy ty coverage

pytest
mypy --strict src/kuchka
ty check src/kuchka tests
coverage run -m pytest && coverage report
```

`tests/test_typing.py` runs mypy against `tests/typing_fixtures/should_fail.py`, a file that mixes lines that must type-check with lines marked `# type: ignore[...]` that must not.
Under `--strict`, an _unused_ `type: ignore` is itself an error, so a clean run of that test is only possible if mypy's static verdict matches what the fixture claims on every line -- it's the thing that actually proves the type story works, not just that it looks plausible.

Ruff is configured with `select = ["ALL"]`.
Every disabled rule in `pyproject.toml` carries an inline comment explaining why it doesn't fit this codebase (mostly: dunder-per-dunder docstrings, the deliberately capitalized unit-constructor names, and the exception hierarchy's inline-message style).

## Open questions for the next version

- Whether/how to autogenerate the overload table once the quantity vocabulary outgrows six hand-written pairs.
- Whether Length/Time/Mass get added as their own quantities or wait for a concrete second use case.
- Whether Kelvin should get a distinct, scalar-multipliable type (see the design note next to `Temperature`).
- Whether Frequency/SampleRate/BaudRate (all T^-1) should be distinct nominal types the way Temperature/TemperatureDelta are, and whether   cross-type comparisons between them should be explicitly permitted.
- NumPy/Pandas integration strategy once vectorized acquisition is actually needed, not just anticipated.