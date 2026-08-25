# kuchka

A small pile of physically-typed engineering units for Python.

```python
from kuchka import Volt, Milliampere

voltage = Volt(4.2)
current = Milliampere(150)
power = voltage * current  # -> Power(0.63 W), typed and computed automatically
```

## Why

A raw `float` doesn't remember what it means.
Passing floats through an engineering pipeline makes unit mistakes easy to write and hard to catch:
the code stays syntactically valid even when it's semantically wrong.

`kuchka` makes the physically-typed version of the code no harder to write than the untyped one.
There's no reason left to reach for a naked `float`.

```python
def analyse_voltage(voltage: Voltage) -> Report: ...


analyse_voltage(4.2)  # rejected by mypy/ty, and again at runtime.
analyse_voltage(Ampere(2))  # rejected by mypy/ty, and again at runtime.
analyse_voltage(Volt(4.2))  # one example of a valid type check.
analyse_voltage(Millivolt(4200))  # another example of a valid type check.
```

## What's in v0.1

| Quantity           | Constructors                                                                     |
| ------------------ | -------------------------------------------------------------------------------- |
| `Voltage`          | `Volt`, `Millivolt`, `Microvolt`, `Kilovolt`                                     |
| `Current`          | `Ampere`, `Milliampere`, `Microampere`, `Kiloampere`                             |
| `Power`            | `Watt`, `Milliwatt`, `Kilowatt`                                                  |
| `Resistance`       | `Ohm`, `Milliohm`, `Kiloohm`, `Megaohm`                                          |
| `Temperature`      | `Celsius`, `Kelvin`                                                              |
| `TemperatureDelta` | `DeltaCelsius`, `DeltaKelvin`                                                    |
| `Time`             | `Second`, `Millisecond`, `Microsecond`                                           |
| `Frequency`        | `Hertz`, `Kilohertz`, `Megahertz`                                                |
| `SamplingPeriod`   | `SecondSamplingPeriod`, `MillisecondSamplingPeriod`, `MicrosecondSamplingPeriod` |
| `SampleRate`       | `SamplesPerSecond`, `KilosamplesPerSecond`, `MegasamplesPerSecond`               |
| `BaudRate`         | `Baud`, `Kilobaud`                                                               |

Deliberately nothing else yet.
See "What this is not (yet)" below.

## Design choices, and why

- **`Decimal`, not `float`.**
  SI prefixes are powers of ten, and those are exact in `Decimal` but usually not in binary `float`.
  `Volt(1) + Millivolt(500) == Volt(1.5)` is true by construction, not by lucky rounding.
- **Unit constructors are plain functions, not classes.**
  `Volt(4.2)` returns a `Voltage`.
  There's no `Volt` type to accidentally `isinstance()`-check against, and no subclass/`__new__` surprise where `isinstance(Volt(5), Volt)` is `False`.
- **`.to(Unit)` uses Python names, never unit strings.**
  There's no `voltage.to("mV")` anywhere in this library.
- **Cross-type arithmetic is rejected statically, not just at runtime.**
  `Volt(5) + Ampere(2)` and `Volt(5) + 4.2` are both mypy errors, not only runtime ones.
  This falls out of typing the base arithmetic methods against `Self` instead of `object`, so every quantity type only ever type-checks arithmetic against its own kind.
  See "Known limitations" for where `ty` doesn't (yet) enforce this the same way.
- **A hand-written overload table, not a generated one -- yet.**
  The runtime arithmetic derives any product or quotient from general exponent-vector algebra.
  Type checkers can't infer "Voltage times Current is Power" from that algebra on their own, so each pairing (six total, for Ohm's law and the power triangle) is spelled out as an explicit `@overload`. Tracked as a decision, not a shortcut -- see "Open questions".
- **`Temperature` is a separate, smaller type from everything else.**
  Absolute temperature is affine, not linear:
  `20 degC + 5 degC` isn't meaningful the way `5V + 3V` is.
  It supports `Temperature +/- TemperatureDelta` and `Temperature - Temperature`, but not `Temperature  - Temperature`, and no scalar multiplication at all.
  See the module docstring next to `Temperature` for the full reasoning.

### Same dimension, different concepts

`Frequency`, `SampleRate`, and `BaudRate` all share the same physical dimension (T^-1), but they are not the same thing, and `kuchka` keeps them as separate types on purpose:

```python
Hertz(50) + SamplesPerSecond(50)  # IncompatibleDimensionError, even though both are dimensionally T^-1
```

Only one type per dimension is ever the _canonical_ one -- the type generic arithmetic produces automatically.
That's always the plain SI name (`Frequency` for T^-1, `Time` for T^1), never a domain-specific type like `SampleRate` or `BaudRate`.
Those stay reachable only by explicit construction, the same way `Temperature` already works.

Genuine reciprocal pairs convert into each other directly:

```python
rate = 1 / SecondSamplingPeriod(2)  # -> SampleRate, not Frequency
period = 1 / rate  # -> SamplingPeriod again
```

`BaudRate` gets no reciprocal at all: baud counts symbols per second, not bits or cycles, so a default equivalence with `Frequency` would be wrong for any encoding other than exactly one bit per symbol. Silently guessing here is worse than refusing.

For code that wants to accept "a Frequency or a SampleRate, interchangeably", there's a ConvertibleToFrequency` protocol:

```python
from kuchka import ConvertibleToFrequency, Frequency


def nyquist_ok(signal: ConvertibleToFrequency, sample_rate: Frequency) -> bool:
    return signal.as_frequency() * 2 <= sample_rate
```

`BaudRate` deliberately does not satisfy this protocol, since it has no `as_frequency()`.

## Comparison to existing tools

`kuchka` isn't the first attempt at physical quantities in Python.
A non-exhaustive list of prior art: Pint, astropy.units, physipy, unyt, forallpeople, numericalunits, Unum, `quantities`, `units`, `unitpy`, and impunity.

**The uncomfortable starting point.** Pint has existed since roughly 2012.
Despite that, more than a decade of engineering work across healthcare, finance, and secure embedded devices has produced essentially zero sightings of any of these libraries in ordinary, non-scientific Python code.
What actually gets written instead is `voltage_mv`, `temperature_c`, `time_ms`, or a small home-grown newtype.

That's not because engineers don't know these libraries exist.
None of them seem to have made the safe path more comfortable than the naming-convention path.
That's the problem `kuchka` is trying to solve -- and it's worth being honest that `kuchka` hasn't proven it solves it either.
It has no adoption history of its own to point to.
The claim here is about mechanism, not a guarantee.

**Where the existing libraries put the friction:**

```python
# Pint / physipy: a registry, and a unit looked up on or from it
ureg = pint.UnitRegistry()
voltage = 3 * ureg.volt + 40 * ureg.millivolt

# kuchka: the unit is the constructor
voltage = Volt(3) + Millivolt(40)
```

| Library            | Unit is...                                                | Result type                           |
| ------------------ | --------------------------------------------------------- | ------------------------------------- |
| Pint               | looked up on a registry (`ureg.meter`, `"3 m"`)           | one generic `Quantity` for everything |
| physipy            | looked up in a dict (`units["nm"]`)                       | one generic `Quantity` for everything |
| `units` / `unitpy` | a string (`unit("m")`, `U("km")`)                         | --                                    |
| impunity           | a string in a function annotation, checked at import time | none at runtime -- rewritten away     |
| `kuchka`           | an ordinary Python name (`Meter`)                         | a distinct Python type per quantity   |

Pint is the mature, general-purpose default:
a huge unit vocabulary, NumPy/Pandas integration, unit parsing from strings.
That generality is the whole point of Pint, and `kuchka` isn't trying to replicate it.

impunity is the closest in spirit to `kuchka`'s static-first goal, and worth knowing about specifically for that reason.
It's a genuinely different, and in some ways more efficient, trade-off:
zero runtime cost once the check has run, at the cost of the "unit" being a string inside an annotation rather than an ordinary object you can construct, return, and pass around.

`kuchka`'s bet: `isinstance(Volt(5), Voltage)` should work with no registry, no plugin, and no decorator rewriting your function body.
`mypy`/`ty` should understand the arithmetic because it's ordinary overloads on an ordinary class, not a new annotation vocabulary.
The trade-off: a deliberately small, hand-maintained unit vocabulary, and no array/NumPy support yet.

**The gap this is aimed at.** Not "Python has no unit libraries" -- it obviously does.
The narrower claim: physical quantities should be ordinary, boring Python types that a type checker already understands, without an engineer ever carrying a registry or spelling a unit as a string.
Whether that's _also_ the missing ingredient for adoption, versus adoption needing something else entirely (habit, deadlines, nobody
asking), is genuinely open.
`kuchka` is a bet on the first explanation, not proof of it.

## What this is not (yet)

- No Length or Mass.
- No NumPy/Pandas integration.
  `Decimal` doesn't vectorize into `ndarray` cleanly, and per-sample scalar wrapping is the wrong shape for high-rate acquisition.
  Intended pattern for now: buffer raw floats at the acquisition boundary, convert once you have a value worth reasoning about.
- No JSON/DB persistence layer. When it's added:
  the _storage_ format may use a unit string (`{"value": 4.2, "unit": "V"}`), since that's not the application-facing API.
  Loading it back must reconstruct a typed measurement, never hand back a bare number.
- No autogenerated prefix modules.
  `Microvolt`/`Millivolt`/`Volt`/etc. are hand-written per dimension for now -- still less code than a codegen pipeline would be, at this size.
- No point-in-time type.
  `Time` is a span (a duration, a timeout, a sample period), not a timestamp.
  A timestamp would need the same affine treatment `Temperature` gets, and isn't modelled yet.

## Known limitations

- **`ty` doesn't yet enforce `Self`-narrowed arithmetic across sibling quantity types the way `mypy --strict` does.**
  `Volt(5) + Ampere(2)` is a `mypy --strict` error but is currently accepted by `ty`.
  Both tools agree on naked-number arithmetic (`Volt(5) + 4.2`) and on the `Temperature` cases.
  Search the test suite for "not (yet) flagged by ty" for the exact cases.
- **The dimension vocabulary is small on purpose.**
  `Resistance * Resistance` and similar mathematically-valid-but-unregistered products raise `UnrepresentableDimensionError` at runtime rather than returning a typed result.
  Neither mypy nor ty catch this ahead of time, since the fallback overload on each quantity type has to accept `object` to stay  compatible with the base class.
- No array, NumPy/Pandas, or persistence support -- see above.

## Examples

- **[Migrating a config from unit-suffixed keys to kuchka](docs/examples/config_migration/README.md)** --
  a worked example: an old `.ini` file where units live in the key name (`accepted_voltage_min_mv`), migrated to a `.toml` file where units are data, parsed through a boundary layer into typed dataclasses.
  Covers closed per-dimension unit resolution, `Decimal`-exact parsing, and three concrete failure modes the boundary layer catches at load time.

## Package layout

_subject to change as the design and architecture bounces around and settles down._

```text
src/kuchka/
    dimensions.py        exponent-vector dimensional algebra
    numeric.py            strict coercion of int/float/Decimal/Fraction into Decimal
    errors.py              the exception hierarchy
    temperature.py       the affine Temperature type, plus Kelvin/Celsius constructors
    quantities/
        base.py             the quantity engine: LinearQuantity, UnitDef, the dimension registry
        electrical.py      Voltage, Current, Power, Resistance and their overload tables
        temporal.py        Time, Frequency, SamplingPeriod, SampleRate, BaudRate
        thermal.py         TemperatureDelta
    units/
        voltage.py, current.py, resistance.py, power.py, temporal.py
                             one module per dimension's prefix constructors
```

Application code should only ever need the top-level `kuchka` package.
Everything under `quantities/`, `units/`, and the internals of `temperature.py` is implementation detail, re-exported for convenience but not meant to be imported piecemeal.

## Development

```bash
pip install -e .
pip install pytest mypy ty coverage

pytest
mypy --strict src/kuchka
ty check src/kuchka tests
coverage run -m pytest && coverage report
```

`tests/test_typing.py` runs mypy against `tests/typing_fixtures/should_fail.py`, a file that mixes lines that must type-check with lines marked `# type: ignore[...]` that must not.
Under `--strict`, an _unused_ `type: ignore` is itself an error.
A clean run of that test is only possible if mypy's static verdict matches the fixture's claim on every single line -- that's the thing that actually proves the type story works, not just that it looks plausible.

Ruff runs with `select = ["ALL"]`.
Every disabled rule in `pyproject.toml` carries an inline comment explaining why it doesn't fit this codebase (mostly: dunder-per-dunder docstrings, the deliberately capitalized unit-constructor names, and the exception hierarchy's inline-message
style).
Worth reading before adding a new blanket ignore.

## Open questions for the next version

- Whether/how to autogenerate the overload table once the quantity vocabulary outgrows hand-maintainable size.
- Whether Length and Mass get added as their own quantities, or wait for a concrete second use case.
- Whether Kelvin should get a distinct, scalar-multipliable type (see the design note next to `Temperature`).
- Whether a point-in-time type (`Instant`, most likely) is ever worth adding, and what its "you can't add two timestamps" rule should look like.
- NumPy/Pandas integration strategy, once vectorized acquisition is actually needed, not just anticipated.
