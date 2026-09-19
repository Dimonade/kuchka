# kuchka

A small pile of strongly-typed engineering units for Python.

```python
from kuchka import Volt, Milliampere

voltage = Volt(4.2)
current = Milliampere(150)
power = voltage * current  # -> Power(0.63 W), typed and computed automatically.
```

## Installation

```bash
uv add kuchka
```

or, with pip:

```bash
pip install kuchka
```

That's the only install step needed to use kuchka in application code.
The `Development` section below covers the separate, larger set of tools (ruff, mypy, ty, pytest, hypothesis, ...) needed to work on `kuchka`.

## Stability

`kuchka` is `0.1.0`: pre-1.0, and versioned accordingly.
Breaking changes are expected between `0.1.x` releases while the API settles.
From `0.2.0` onward, `kuchka` follows ordinary semantic versioning:
a minor version bump won't break existing code, and a breaking change always comes with a major version bump.

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

## What's in v0.1.x

**Electrical**

- **Voltage:** `Volt`, `Millivolt`, `Microvolt`, `Kilovolt`
- **Current:** `Ampere`, `Milliampere`, `Microampere`, `Kiloampere`
- **Power:** `Watt`, `Milliwatt`, `Kilowatt`
- **Resistance:** `Ohm`, `Milliohm`, `Kiloohm`, `Megaohm`
- **Conductance:** `Siemens`, `Microsiemens`, `Millisiemens`, `Kilosiemens`
- **Charge:** `Coulomb`, `Millicoulomb`, `Microcoulomb`, `Nanocoulomb`, `Picocoulomb`, `MilliampereSecond`, `MilliampereHour`, `AmpereHour`
- **Energy:** `Joule`, `Millijoule`, `Microjoule`, `Nanojoule`, `Picojoule`, `Kilojoule`, `Megajoule`, `MilliwattHour`, `WattHour`

**Time & Signal**

- **Temperature:** `Celsius`, `Kelvin`
- **Temperature Delta:** `DeltaCelsius`, `DeltaKelvin`
- **Time:** `Second`, `Millisecond`, `Microsecond`, `Minute`, `Hour`
- **Frequency:** `Hertz`, `Kilohertz`, `Megahertz`
- **Sampling Period:** `SecondSamplingPeriod`, `MillisecondSamplingPeriod`, `MicrosecondSamplingPeriod`
- **Sample Rate:** `SamplesPerSecond`, `KilosamplesPerSecond`, `MegasamplesPerSecond`
- **Baud Rate:** `Baud`, `Kilobaud`

**Geometry & Mechanics**

- **Length:** `Nanometer`, `Micrometer`, `Millimeter`, `Centimeter`, `Decimeter`, `Meter`, `Kilometer`, `Inch`
- **Area:** `SquareMillimetre`, `SquareCentimetre`, `SquareMetre`, `SquareKilometre`, `Hectare`, `Acre`, `SquareInch`
- **Volume:** `CubicMillimetre`, `CubicCentimetre`, `CubicMetre`, `Microlitre`, `Millilitre`, `Litre`, `Kilolitre`
- **Velocity:** `MetrePerSecond`
- **Mass:** `Nanogram`, `Microgram`, `Milligram`, `Gram`, `Kilogram`, `Megagram`, `Tonne`

**Chemistry & Light**

- **Amount of Substance:** `Micromole`, `Millimole`, `Mole`
- **Luminous Intensity:** `Candela`

**Dimensionless**

- **Proportion:** `Ratio`, `Percent`

See "What this is not (yet)" below.

## Design choices, and why

- **Exact rational storage, not `float`.**
  Every magnitude is stored as an exact `Fraction`, so `Volt(1) + Millivolt(500) == Volt(1.5)` is true by construction, not by lucky rounding, and `Litre(Fraction(5, 18))` keeps its exact value instead of being rounded at construction.
  `Decimal` is how a value displays -- `repr()`/`__format__` materialize the exact `Fraction` into a `Decimal` only at that point.
- **Unit constructors are plain functions, not classes.**
  `Volt(4.2)` returns a `Voltage`.
  There's no `Volt` type to accidentally `isinstance()`-check against, and no subclass/`__new__` surprise where `isinstance(Volt(5), Volt)` is `False`.
- **`.to(Unit)` uses Python names, never unit strings.**
  There's no `voltage.to("mV")` anywhere in this library.
- **Boundary code that must resolve a unit from a string has a maintained table to use.**
  `kuchka.units` exports a `*_UNITS` mapping per dimension (`VOLTAGE_UNITS`, `CURRENT_UNITS`, `FREQUENCY_UNITS`, and so on), closed to that dimension's own constructors and immutable.
  This is not a second construction path: `Volt(5)` is still how application code builds a `Voltage`.
  It exists for the one place a unit is expected to arrive as a string -- a config file, a CSV header, a hardware descriptor.
  The intention is so that place doesn't have to hand-roll the same table every other application resolving `kuchka` units already needed.
- **Cross-type arithmetic is rejected statically, not just at runtime.**
  `Volt(5) + Ampere(2)` and `Volt(5) + 4.2` are both mypy errors, not only runtime ones.
  This falls out of typing the base arithmetic methods against `Self` instead of `object`, so every quantity type only ever type-checks arithmetic against its own kind.
  See "Known limitations" for where `ty` doesn't (yet) enforce this the same way.
- **A hand-written overload table.**
  The runtime arithmetic derives any product or quotient from general exponent-vector algebra.
  Type checkers can't infer "Voltage times Current is Power" from that algebra on their own, so each pairing is spelled out as an explicit `@overload`.
- **`Temperature` is a separate, smaller type from everything else.**
  Absolute temperature is affine, not linear:
  `20 degC + 5 degC` isn't meaningful the way `5V + 3V` is.
  It supports `Temperature +/- TemperatureDelta` and `Temperature - Temperature`, but not `Temperature  - Temperature`, and no scalar multiplication at all.
  See the module docstring next to `Temperature` for the full reasoning.
- **Scope gaps are curated, not generic, where the gap has a name.**
  `Resistance * Resistance` raises `UnrepresentableDimensionError`: dimensionally valid, no registered type, and no plan to add one.
  Planned to be implemented dimensions raise a `PlannedDimensionError` instead, a subclass of the same error, because some calculations are planned to be implemented soon.
  The error message is explicitly different, and not leaving the reader to reverse-engineer the physics from an exponent vector.

### Same dimension, different concepts

`Frequency`, `SampleRate`, and `BaudRate` all share the same physical dimension (T^-1), but they are not the same thing, and `kuchka` keeps them as separate types on purpose:

```python
# IncompatibleDimensionError, even though both are dimensionally T^-1.
Hertz(50) + SamplesPerSecond(50)
```

Only one type per dimension is ever the _canonical_ one -- the type generic arithmetic produces automatically.
That's always the plain SI name (`Frequency` for T^-1, `Time` for T^1), never a domain-specific type like `SampleRate` or `BaudRate`.
Those stay reachable only by explicit construction, the same way `Temperature` already works.

Genuine reciprocal pairs convert into each other directly:

```python
rate = 1 / SecondSamplingPeriod(2)  # -> SampleRate, not Frequency.
period = 1 / rate  # -> SamplingPeriod again.
```

`BaudRate` gets no reciprocal at all: baud counts symbols per second, not bits or cycles, so a default equivalence with `Frequency` would be wrong for any encoding other than exactly one bit per symbol.
Silently guessing here is worse than refusing.

For code that wants to accept "a Frequency or a SampleRate, interchangeably", there's a `ConvertibleToFrequency` protocol:

```python
from kuchka import ConvertibleToFrequency, Frequency


def nyquist_ok(signal: ConvertibleToFrequency, sample_rate: Frequency) -> bool:
    return signal.as_frequency() * 2 <= sample_rate
```

`BaudRate` deliberately does not satisfy this protocol, since it has no `as_frequency()`.

### Percent and Ratio are the same quantity, not different concepts

`Proportion` is the dimensionless quantity: `Ratio` is its coherent, unscaled unit (a bare fraction), and `Percent` is a hundredth of that.
Unlike `Frequency`/`SampleRate`/`BaudRate`, these are not different concepts sharing a dimension -- `5%` and `0.05` are the same quantity at different scale, the same relationship `Volt`/`Millivolt` has:

```python
Percent(5) == Ratio(Decimal("0.05"))  # True
Percent(5) + Ratio(Decimal("0.05")) == Percent(10)  # True
```

`Proportion` is never registered for `DIMENSIONLESS`, and could not usefully be even if it wanted to: `Ohm(5) / Ohm(2)` already returns a bare `Decimal` for any dimensionless result, before the registry is even consulted, and that does not change.
`Percent`/`Ratio` stay reachable only by explicit construction, the same way `SampleRate`/`BaudRate` do.

What does change: multiplying or dividing any existing quantity by a `Proportion` already produces the correctly-typed result, with no new arithmetic added anywhere.

```python
Volt(5) * Ratio(Decimal("0.1")) == Volt(Decimal("0.5"))  # True, a tolerance band.
```

This falls out of the same general dimension algebra that already derives `Power` from `Voltage * Current`: multiplying by the dimensionless identity leaves the other operand's dimension, and therefore its type, unchanged.

### Area and Volume fall out of Length, and Litre is its own unit family

`Length * Length` produces an `Area`, and `Area * Length` (or `Length * Area`) produces a `Volume`, through the same general dimension algebra as everything else -- no special-cased geometry code was needed:

```python
plot = Meter(5) * Meter(2)  # -> Area, 10 m^2
tank = plot * Meter(3)  # -> Volume, 30 m^3
```

`Litre` is not a prefix of `CubicMetre` the way `Millivolt` is a prefix of `Volt` -- it's a separate, coherent metric volume unit in its own right (one cubic decimetre, exactly), with its own full prefix vocabulary (`Microlitre`, `Millilitre`, `Kilolitre`).
Two of those prefixes land on exactly the same scale as a cubic-metric unit by coincidence, not by design: a millilitre and a cubic centimetre are the same quantity, and a microlitre and a cubic millimetre are too.
They stay as separate `UnitDef`s and not aliases (the way `Tonne` aliases `Megagram`) because they come from different naming traditions that happen to agree numerically, not from one SI unit with two names.

### Resistance and Conductance are reciprocals, the same shape as Time and Frequency

`Conductance` (`Siemens`) is `Resistance`'s reciprocal, registered and typed the same way `Frequency` is `Time`'s:

```python
conductance = 1 / Ohm(5)  # -> Conductance, 0.2 S
resistance = 1 / conductance  # -> Resistance, 5 ohm, round-trips exactly
```

Ohm's law works from either side of that reciprocal, and both forms agree:

```python
Volt(10) / Ohm(5) == Volt(10) * Siemens(Decimal("0.2")) == Ampere(2)
```

## Physical constants

`kuchka.constants` provides a small set of physical constants as ordinary `kuchka` quantities.

```python
from kuchka import Hertz
from kuchka.constants import SPEED_OF_LIGHT

wifi_wavelength = SPEED_OF_LIGHT / Hertz(2_400_000_000)  # -> Length, ~0.1249 m
```

`SPEED_OF_LIGHT` and `ELEMENTARY_CHARGE` are exact by SI definition.
`ELECTRON_MASS`, `PROTON_MASS`, and `NEUTRON_MASS` are CODATA 2022 recommended values, carrying exactly as many significant digits as CODATA publishes for each.
The module docstring states which category each constant belongs to.

The set grows as concrete needs come up, the same way the unit vocabulary itself does.

## Errors

Every error kuchka raises for a mistake in application code is a `MeasurementError`; catch that to handle the whole family at once.

| Error                           | Raised when                                                                                                                      |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `InvalidMeasurementError`       | a unit constructor got a non-numeric value, a `bool`, or an incompatible measurement                                             |
| `IncompatibleDimensionError`    | an operation was attempted between two incompatible dimensions or types                                                          |
| `InvalidConversionError`        | `.to(...)` was given something that isn't a valid unit for that dimension                                                        |
| `UnrepresentableDimensionError` | arithmetic produced a dimension with no registered engineering type                                                              |
| `PlannedDimensionError`         | same as above, but for a dimension already named and intended for a future release (subclass of `UnrepresentableDimensionError`) |

## Formatting

Every quantity supports Python's format mini-language through `__format__`, applied to the magnitude in its current display unit.

```python
from kuchka import Volt

voltage = Volt(1234.5)

f"{voltage}"  # "1234.5 V"   -- matches repr()
f"{voltage:.2f}"  # "1234.50 V"
f"{voltage:.2e}"  # "1.23e+3 V"
f"{voltage:,.2f}"  # "1,234.50 V"
```

An empty format spec matches `repr()`.
A non-empty spec applies to the magnitude, materialized to `Decimal` for display, and the unit symbol is appended after.

## Examples

- **[Migrating a config from unit-suffixed keys to kuchka](docs/examples/config_migration/README.md)** --
  a worked example: an old `.ini` file where units live in the key name (`accepted_voltage_min_mv`), migrated to a `.toml` file where units are data, parsed through a boundary layer into typed dataclasses.
  Covers closed per-dimension unit resolution, `Decimal`-exact parsing, and three concrete failure modes the boundary layer catches at load time.
- **[Working around an unrepresentable intermediate dimension](docs/examples/unrepresentable_dimensions/README.md)** --
  engineering formulas such as `P = V² / R` and parallel resistor networks, demonstrating the recommended pattern of dropping to `.magnitude` only for a single unrepresentable intermediate value before reconstructing a typed quantity.

## Package layout

_subject to change as the design and architecture bounces around and settles down._

```text
src/kuchka/
    constants.py      physical constants
    dimensions.py     dimensional algebra
    prefixes.py       SI prefixes and `prefixed_unit()`
    numeric.py        numeric coercion: exact `Fraction` at construction, `Decimal` for display
    errors.py         exception hierarchy
    quantities/       quantity types and their arithmetic
                       (`base.py`, electrical, temporal, thermal, geometric,
                       kinematic, charge, energy, mass, amount, luminous,
                       proportion, ...)
    units/            unit constructors, one module per dimension
tests/                test suite
```

Application code should only ever need the top-level `kuchka` package.
Everything under `quantities/`, `units/`, and the internals of `temperature.py` is implementation detail, re-exported for convenience but not meant to be imported piecemeal.

## Development

`uv sync` installs the `dev` dependency group (ruff, mypy, ty, pytest, hypothesis, coverage, and editor tooling) alongside `kuchka` itself.

```bash
uv sync

uv run pytest
uv run mypy --strict src/kuchka
uv run ty check src/kuchka tests
uv run coverage run -m pytest && uv run coverage report
```

Alternatively, one can leverage the `justfile`'s `just ct` or `just covtest` to execute the whole testbench and additional statistics.

`tests/test_typing.py` runs mypy against `tests/typing_fixtures/should_fail.py`, a file that mixes lines that must type-check with lines marked `# type: ignore[...]` that must not.
Under `--strict`, an _unused_ `type: ignore` is itself an error.
A clean run of that test is only possible if mypy's static verdict matches the fixture's claim on every single line -- that's the thing that actually proves the type story works, not just that it looks plausible.

Ruff runs with `select = ["ALL"]`.
Every disabled rule in `pyproject.toml` carries an inline comment explaining why it doesn't fit this codebase.
This mostly includes dunder-per-dunder docstrings, the deliberately capitalized unit-constructor names, and the exception hierarchy's inline-message style.
Worth reading before adding a new blanket ignore.

## Performance

`kuchka` deliberately uses exact rational arithmetic (`Fraction`) under the hood for correctness.
The design philosophy is to utilize `kuchka` for unit correctness as values come from configuration files, through permutations and checks flow into reports.
Running `kuchka` in a hot loop transforming values in a vector of mega-samples-per-second live is not really the intended use case of it.

For more see [`benchmarks`](benchmarks/README.md).

## Comparison to existing tools

`kuchka` isn't the first attempt at physical quantities in Python.
A non-exhaustive list of prior art: `Pint`, `astropy.units`, `physipy`, `unyt`, `forallpeople`, `numericalunits`, `Unum`, `quantities`, `units`, `unitpy`, and `impunity`.

**The uncomfortable starting point.** Pint has existed since roughly 2012.
Despite that, more than a decade of engineering work across healthcare, finance, and secure embedded devices has produced (for me) essentially zero sightings of any of these libraries in Python code.
What actually gets written instead is `voltage_mv`, `temperature_c`, `time_ms`, or a small home-grown newtype.

I assume that's not because engineers don't know these libraries exist.
None of them seem to have made the safe path more comfortable than the naming-convention path.
That's the problem `kuchka` is trying to solve -- and it's worth being honest that `kuchka` hasn't proven it solves it either.
It has no adoption history of its own to point to.
The claim here is about mechanism, not a guarantee.

**Where the existing libraries put the friction:**

```python
# Pint / physipy: a registry, and a unit looked up on or from it.
ureg = pint.UnitRegistry()
voltage = 3 * ureg.volt + 40 * ureg.millivolt

# kuchka: the unit is the constructor.
voltage = Volt(3) + Millivolt(40)
```

| Library        | Unit is...                                                | Result type                           |
| -------------- | --------------------------------------------------------- | ------------------------------------- |
| Pint           | looked up on a registry (`ureg.meter`, `"3 m"`)           | one generic `Quantity` for everything |
| physipy        | looked up in a dict (`units["nm"]`)                       | one generic `Quantity` for everything |
| units / unitpy | a string (`unit("m")`, `U("km")`)                         | --                                    |
| impunity       | a string in a function annotation, checked at import time | none at runtime -- rewritten away     |
| kuchka         | an ordinary Python name (`Meter`)                         | a distinct Python type per quantity   |

Pint is the mature, general-purpose default: a huge unit vocabulary, NumPy/Pandas integration, unit parsing from strings.
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

- `Length` was added, `Foot`/`Yard`/`Mile` were not.
- No NumPy/Pandas integration.
  `Decimal` doesn't vectorize into `ndarray` cleanly, and per-sample scalar wrapping is the wrong shape for high-rate acquisition.
  Intended pattern for now: buffer raw floats at the acquisition boundary, convert once there is a value worth reasoning about.
- No JSON/DB persistence layer. When it's added:
  - the _storage_ format may use a unit string (`{"value": 4.2, "unit": "V"}`), since that's not the application-facing API.
    Loading it back must reconstruct a typed measurement, never hand back a bare number.
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
  Neither mypy nor ty catch this ahead of time, since the fallback overload on each quantity type has to accept `object` to stay compatible with the base class.
- No special array, NumPy/Pandas support.

## Open questions for the upcoming iterations / next versions

- Whether a point-in-time type (`Instant`, most likely) is ever worth adding, and what its "you can't add two timestamps" rule should look like.
- NumPy/Pandas integration strategy, once vectorized acquisition is actually needed, not just anticipated.
- `dB` family.

## History

The original pre-implementation design proposal lives at [`docs/introduction/design_proposal.md`](docs/introduction/design_proposal.md), kept as a record of the initial thinking.
