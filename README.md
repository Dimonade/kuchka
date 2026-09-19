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

That covers everything needed to use `kuchka` in application code.
The [Development](#development) section below covers the separate toolchain (ruff, mypy, ty, pytest, hypothesis, ...) needed to work on `kuchka` itself.

## Stability

`kuchka` is currently `0.1.x`.
Breaking changes are expected between releases while the API settles.
From `0.2.0` onward, `kuchka` follows ordinary semantic versioning: a minor release won't break existing code, and a breaking change always comes with a major version bump.

## Why

A raw `float` doesn't remember what it means.
Passing floats through an engineering pipeline makes unit mistakes easy to write and hard to catch, because the code stays syntactically valid even when it is semantically wrong.

`kuchka` makes the strongly-typed version of the code as easy to write as the untyped one.

```python
def analyse_voltage(voltage: Voltage) -> Report: ...


analyse_voltage(4.2)  # rejected by mypy/ty, and again at runtime
analyse_voltage(Ampere(2))  # rejected by mypy/ty, and again at runtime
analyse_voltage(Volt(4.2))  # valid
analyse_voltage(Millivolt(4200))  # also valid, same Voltage
```

## Different shapes of quantity

Every quantity in `kuchka` picks one of the available arithmetic shapes.
The shape a quantity picks decides which operators it supports and what they do.
The quantity itself is an ordinary Python type either way.

**Linear:** units differ by a pure scale factor.
Addition, subtraction, scalar multiplication, and full ordering all work the way they do on ordinary numbers.
Most of the vocabulary is linear: `Voltage`, `Current`, `Length`, `Mass`, `Time`, and so on.

```python
Volt(1) + Millivolt(200) == Volt(1.2)  # True
```

**Affine:** units differ by a scale _and_ an offset, so a reading is a point on a scale, not a vector.
Two readings subtract to a linear delta; a reading plus a delta gives another reading.
Adding two readings together is rejected, since there's no physical meaning to it.
`Temperature` is the current example.
Any future point-in-time quantity (a `Timestamp`, or `Instant`, say) would be another.

```python
Celsius(25) - Celsius(20) == DeltaCelsius(5)  # a delta
Celsius(20) + DeltaCelsius(5) == Celsius(25)  # a shifted reading
Celsius(20) + Celsius(5)  # raises: not a meaningful reading
```

**Modular:** a quantity wraps around after a fixed period, so it's a position on a circle rather than a point on a line.
Addition and subtraction wrap into `[0, period)`.
There is no total order, since "greater than" depends on a direction-of-travel convention the library doesn't pick for you.
`Angle` is the current example.

```python
Degree(350) + Degree(20) == Degree(10)  # wraps around
Degree(300).difference(Degree(350)) == Degree(-50)  # shortest signed path
Degree(10) < Degree(20)  # raises: no total order
```

More shapes can be added later without touching the ones that already exist, and a new quantity within an existing shape is typically a short, self-contained module.

## What's in v0.1.x

**Electrical**

- **Voltage:** `Volt`, `Millivolt`, `Microvolt`, `Kilovolt`
- **Current:** `Ampere`, `Milliampere`, `Microampere`, `Kiloampere`
- **Power:** `Watt`, `Milliwatt`, `Kilowatt`
- **Resistance:** `Ohm`, `Milliohm`, `Kiloohm`, `Megaohm`
- **Conductance:** `Siemens`, `Microsiemens`, `Millisiemens`, `Kilosiemens`
- **Charge:** `Coulomb`, `Millicoulomb`, `Microcoulomb`, `Nanocoulomb`, `Picocoulomb`, `MilliampereSecond`, `MilliampereHour`, `AmpereHour`
- **Energy:** `Joule`, `Millijoule`, `Microjoule`, `Nanojoule`, `Picojoule`, `Kilojoule`, `Megajoule`, `MilliwattHour`, `WattHour`

**Time and Signal**

- **Temperature:** `Celsius`, `Kelvin`
- **Temperature Delta:** `DeltaCelsius`, `DeltaKelvin`
- **Time:** `Second`, `Millisecond`, `Microsecond`, `Minute`, `Hour`
- **Frequency:** `Hertz`, `Kilohertz`, `Megahertz`
- **Sampling Period:** `SecondSamplingPeriod`, `MillisecondSamplingPeriod`, `MicrosecondSamplingPeriod`
- **Sample Rate:** `SamplesPerSecond`, `KilosamplesPerSecond`, `MegasamplesPerSecond`
- **Baud Rate:** `Baud`, `Kilobaud`

**Geometry and Mechanics**

- **Length:** `Nanometer`, `Micrometer`, `Millimeter`, `Centimeter`, `Decimeter`, `Meter`, `Kilometer`, `Inch`
- **Area:** `SquareMillimetre`, `SquareCentimetre`, `SquareMetre`, `SquareKilometre`, `Hectare`, `Acre`, `SquareInch`
- **Volume:** `CubicMillimetre`, `CubicCentimetre`, `CubicMetre`, `Microlitre`, `Millilitre`, `Litre`, `Kilolitre`
- **Velocity:** `MetrePerSecond`
- **Mass:** `Nanogram`, `Microgram`, `Milligram`, `Gram`, `Kilogram`, `Megagram`, `Tonne`

**Angle**

- **Angle:** `Radian`, `Degree`, `Turn`, `Gradian`, `ArcMinute`, `ArcSecond`

**Chemistry and Light**

- **Amount of Substance:** `Micromole`, `Millimole`, `Mole`
- **Luminous Intensity:** `Candela`

**Dimensionless**

- **Proportion:** `Ratio`, `Percent`

_NOTE: The *canonical* spelling of the unit of length is `*metre`. `kuchka` aliases all `*meter` with `*metre`, so they are essentially the same objects._

See [What this is not (yet)](#what-this-is-not-yet) below for the gaps.

## Design choices, and why

- **Exact rational storage, not `float`.**
  Every magnitude is stored as an exact `Fraction`, not a rounded approximation.
  `Ampere(1) + Milliampere(500) == Ampere(1.5)` is true by construction.
  A value like `Litre(Fraction(5, 18))` keeps its exact value all the way through storage and arithmetic.
  `Decimal` is a _display_ format, not the storage type.
  _See [Exact by construction](#exact-by-construction-and-its-limits) below._
- **Unit constructors are plain functions, not classes.**
  `Volt(4.2)` returns a `Voltage`.
  There's no `Volt` type to accidentally `isinstance()`-check against.
- **`.to(UNIT)` uses Python names, never unit strings.**
  There's no `voltage.to("mV")` anywhere in this library.
  Instead, to visually convert one unit to another a strong type is used:

  ```python
  from kuchka import Volt
  from kuchka.units import MILLIVOLT

  voltage = Volt(5)
  voltage.to(MILLIVOLT)

  >>> 5000 mV
  ```

  This does not destroy or alter the canonical storage:

  ```python
  voltage

  >>> 5 V
  ```

  It is not possible to convert to a unit from a different quantity:

  ```python
  from kuchka.units import MILLIAMPERE

  voltage.to(MILLIAMPERE)

  >>> <traceback>
  kuchka.errors.InvalidConversionError:
    cannot convert volt (V) to milliampere (mA):
    incompatible dimensions - [T^-3 L^2 M I^-1] and [I].
  ```

- **Boundary code that must resolve a unit from a string has a maintained table to use.**
  `kuchka.units` exports a `*_UNITS` mapping per dimension (`VOLTAGE_UNITS`, `CURRENT_UNITS`, `ANGLE_UNITS`, and so on), closed to that dimension's own constructors.
  This exists for the one place a unit is expected to arrive as a string - a config file, a CSV header, a hardware descriptor - so that boundary code doesn't have to hand-roll the same table every application resolving `kuchka` units already needs.
- **Cross-type arithmetic is rejected statically, not just at runtime.**
  `Volt(5) + Ampere(2)` and `Volt(5) + 4.2` are both mypy errors, not only runtime ones.
  This falls out of typing the base arithmetic methods against `Self` instead of `object`, so every quantity type only type-checks arithmetic against its own kind.
  _See [Known limitations](#known-limitations) for where `ty` doesn't (yet) enforce this the same way._
- **A hand-written overload table for derived quantities.**
  The runtime arithmetic derives any product or quotient from general exponent-vector algebra.
  Type checkers can't infer "Voltage times Current is Power" from that algebra alone, so each pairing is spelled out as an explicit `@overload`.
- **Scope gaps are curated, not generic, where the gap has a name.**
  `Resistance * Resistance` raises `UnrepresentableDimensionError`: dimensionally valid, no registered type, no plan to add one.
  A dimension planned for a future release raises `PlannedDimensionError` instead, a subclass of the same error, naming what it will become rather than leaving the reader to reverse-engineer the physics from an exponent vector.

### Same dimension, different concepts

`Frequency`, `SampleRate`, and `BaudRate` all share the same physical dimension (T^-1), and `kuchka` keeps them as separate types on purpose:

```python
Hertz(50) + SamplesPerSecond(50)  # IncompatibleDimensionError, despite both being T^-1
```

Only one type per dimension is ever _canonical_ - the type generic arithmetic produces automatically.
That's always the plain SI name (`Frequency` for T^-1, `Time` for T^1), never a domain-specific type like `SampleRate` or `BaudRate`.
Those stay reachable only by explicit construction, the same way `Temperature` does.

Genuine reciprocal pairs still convert into each other directly:

```python
rate = 1 / SecondSamplingPeriod(2)  # -> SampleRate, not Frequency
period = 1 / rate  # -> SamplingPeriod again
```

`BaudRate` gets no reciprocal at all - baud counts symbols per second, not bits or cycles, so a default equivalence with `Frequency` would only be correct for exactly one bit per symbol.
Code that wants to accept "a `Frequency` or a `SampleRate`, interchangeably" can use the `ConvertibleToFrequency` protocol instead of picking one:

```python
from kuchka import ConvertibleToFrequency, Frequency


def nyquist_ok(signal: ConvertibleToFrequency, sample_rate: Frequency) -> bool:
    return signal.as_frequency() * 2 <= sample_rate
```

### A few relationships worth knowing

- **Area and Volume fall out of Length automatically.**
  `Length * Length` gives an `Area`; `Area * Length` gives a `Volume` - plain exponent algebra, no special-cased geometry code.
  `Litre` is its own family, not an alias for `CubicMetre`'s prefixes: a millilitre and a cubic centimetre are the same physical quantity, kept as separate `UnitDef`s because they come from different naming traditions that happen to agree numerically.

  ```python
  plot = Meter(5) * Meter(2)  # -> Area, 10 m^2
  tank = plot * Meter(3)  # -> Volume, 30 m^3
  ```

- **Resistance and Conductance are reciprocals**, the same shape `Time`/`Frequency` already have.

  ```python
  conductance = 1 / Ohm(5)  # -> Conductance, 0.2 S
  Volt(10) / Ohm(5) == Volt(10) * conductance  # both give Ampere(2)
  ```

- **Percent and Ratio are the same quantity at a different scale**, the same relationship `Volt`/`Millivolt` have.

  ```python
  Percent(5) == Ratio(Decimal("0.05"))  # True
  Volt(5) * Ratio(Decimal("0.1")) == Volt(0.5)  # multiplying by a Proportion just scales
  ```

## Exact by construction, and its limitations

Every magnitude in `kuchka` is stored as a `Fraction`.
`int` and `Decimal` both convert to `Fraction` with no rounding.
A `float` is parsed through its string form first, so `Volt(4.2)` keeps the digits typed rather than `4.2`'s binary floating-point value.
`Decimal` only re-enters the picture as a display format: `repr()` and `__format__` materialize the exact `Fraction` into a `Decimal` on request, rounding only if the value doesn't terminate in base ten.

```python
q = Litre(Fraction(5, 18))
q.magnitude  # Fraction(5, 18), exact forever
repr(q)  # "0.2777777777777777777777777778 L", a display rounding at read time
```

This runs into a real wall with π.
A `Turn` is `2π` radians, and no `Fraction` equals π - it is irrational, not just inconveniently long.
Rather than fake exactness or reject radians outright, `kuchka` defines its own fixed rational stand-in for π (fifteen significant digits, the precision commonly cited by NASA/JPL) and uses it only to define `Degree`, `Turn`, `Gradian`, `ArcMinute`, and `ArcSecond`'s scales relative to `Radian`.
`Radian` itself is an ordinary constructor - a sensor reading of `Radian(1.5707963)` is stored exactly, with no lossy step anywhere:

```python
Radian(1.5707963)  # stored exactly, same as any other quantity
```

`kuchka`'s own constant cancels out of every comparison that stays within the non-`Radian` angle units, so `Degree`, `Turn`, `Gradian`, `ArcMinute`, and `ArcSecond` agree with each other exactly regardless of which finite π was chosen.
It only becomes externally visible once a `Radian` value meets the rest of the family:

```python
from kuchka.units.angular import _PI
import math

Radian(_PI) == Degree(180)  # True: built from kuchka's own constant
Radian(math.pi) == Degree(180)  # True: but coincidentally, due to truncation
```

If we inspect the `cpython`'s [`mathmodule`](https://github.com/python/cpython/blob/main/Modules/mathmodule.c#L190C1-L190C68):

`static const double pi = 3.141592653589793238462643383279502884197;`

That last line is intentional, not a bug - `math.pi` and `kuchka`'s `_PI` are simply different values.

## Physical constants

`kuchka.constants` aims to provide to users different sets of `kuchka`-typed constants.

Currently, the only module that is quite sparsely implemented, is the CODATA 2022 module.
The reasoning is that different modules define different (and updated) constants and values, and there is no single, unified source of truth that answers all needs.
Some constants databases may relate to geology, others to physics, or chemistry, or specific engineering domains.
`kuchka` allows importing the constants and avoid reconstructing them manually.

```python
from kuchka import Hertz
import kuchka.constants.codata_2022 as kc

wifi_wavelength = kc.SPEED_OF_LIGHT_IN_VACUUM / Hertz(
    2_400_000_000
)  # -> Length, ~0.1249 m
```

`SPEED_OF_LIGHT_IN_VACUUM` and `ELEMENTARY_CHARGE` are exact by SI definition.
`ELECTRON_MASS`, `PROTON_MASS`, and `NEUTRON_MASS` are CODATA 2022 recommended values, carrying exactly as many significant digits as CODATA publishes for each - each constant's own docstring states which category it belongs to.

## Errors

Every error `kuchka` raises for a mistake in application code is a `MeasurementError`; catch that to handle the whole family at once.

| Error                           | Raised when                                                                                                                      |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `InvalidMeasurementError`       | a unit constructor got a non-numeric value, a `bool`, or an incompatible measurement                                             |
| `IncompatibleDimensionError`    | an operation was attempted between two incompatible dimensions or types                                                          |
| `InvalidConversionError`        | `.to(...)` was given something that isn't a valid unit for that dimension                                                        |
| `UnrepresentableDimensionError` | arithmetic produced a dimension with no registered engineering type                                                              |
| `PlannedDimensionError`         | same as above, but for a dimension already named and intended for a future release (subclass of `UnrepresentableDimensionError`) |

## Formatting

Every quantity supports Python's format mini-language through `__format__`, applied to the magnitude materialized in its current display unit.

```python
from kuchka import Volt

voltage = Volt(1234.5)

f"{voltage}"  # "1234.5 V", matches repr()
f"{voltage:.2f}"  # "1234.50 V"
f"{voltage:.2e}"  # "1.23e+3 V"
f"{voltage:,.2f}"  # "1,234.50 V"
```

An empty format spec matches `repr()`.
A non-empty spec applies to the materialized `Decimal`, and the unit symbol is appended after.

## Examples

- **[Migrating a config from unit-suffixed keys to `kuchka`](docs/examples/config_migration/README.md)** -
  an old `.ini` file where units live in the key name (`accepted_voltage_min_mv`), migrated to a `.toml` file where units are data, parsed through a boundary layer into typed dataclasses.
  Covers closed per-dimension unit resolution and three concrete failure modes the boundary layer catches at load time.
- **[Working around an unrepresentable intermediate dimension](docs/examples/unrepresentable_dimensions/README.md)** -
  engineering formulas such as `P = V²/R` and parallel resistor networks, demonstrating the pattern of dropping to `.magnitude` only for a single unrepresentable intermediate value before reconstructing a typed quantity.

## Package layout

_subject to change as the design settles._

```text
src/kuchka/
    dimensions.py     dimensional algebra
    prefixes.py       SI prefixes and `prefixed_unit()`
    numeric.py        numeric coercion: exact Fraction at construction, Decimal for display
    errors.py         exception hierarchy
    constants/        physical constants databases
    quantities/       quantity types and their arithmetic
                       base/  the generic engine: storage, ordering, and the three shapes
                       electrical, thermal, angular, geometric, kinematic,
                       charge, energy, mass, amount, luminous, proportion, ...
    units/            unit constructors, one module per dimension
tests/                test suite
```

Application code should only ever need the top-level `kuchka` package.
Everything under `quantities/` and `units/` is implementation detail, re-exported for convenience but not meant to be imported piecemeal.
Otherwise, `constants/` provides specific utility objects that the user can also construct manually if they choose so.

## Development

`uv sync` installs the `dev` dependency group (`ruff`, `mypy`, `ty`, `pytest`, `hypothesis`, `coverage`, and editor tooling) alongside `kuchka` itself.

```bash
uv sync

uv run pytest
uv run mypy --strict src/kuchka
uv run ty check src/kuchka tests
uv run coverage run -m pytest && uv run coverage report
```

`just ct` (or `just covtest`) runs the full testbench with coverage; `just check` runs `mypy --strict` and `ty` alone, and gates `covtest` so a type error fails fast before the slower coverage run starts.

`tests/test_typing.py` runs mypy against `tests/typing_fixtures/should_fail.py`, a file that mixes lines that must type-check with lines marked `# type: ignore[...]` that must not.
Under `--strict`, an unused `type: ignore` is itself an error, which is what actually proves the static typing story works rather than just looking plausible.

Ruff runs with `select = ["ALL"]`.
Every disabled rule in `pyproject.toml` carries an inline comment explaining why it doesn't fit this codebase - please read before adding a new blanket ignore.

## Performance

`kuchka` uses exact rational arithmetic (`Fraction`) under the hood for correctness.
The design intent is for `kuchka` to sit at configuration and reporting boundaries, converting values once as they enter or leave a pipeline, not to run inside a per-sample hot loop processing a live stream of mega-samples-per-second.

See [`benchmarks`](benchmarks/README.md) for numbers.

## Comparison to existing tools

`kuchka` isn't the first attempt at physical quantities in Python.
Prior art includes `Pint`, `astropy.units`, `physipy`, `unyt`, `forallpeople`, `numericalunits`, `Unum`, `quantities`, `units`, `unitpy`, and `impunity`.

**The starting observation.** Pint has existed since roughly 2012, yet more than a decade of engineering work across healthcare, finance, and secure embedded devices has produced close to zero real sightings of any of these libraries in production code.
What gets written instead is `voltage_mv`, `temperature_c`, `time_ms`, or a small home-grown newtype.
`kuchka` is a bet that the missing ingredient is mechanism, not awareness - a bet with no adoption history yet to back it up.

**Where the existing libraries put the friction:**

```python
# Pint / physipy: a registry, and a unit looked up on it.
ureg = pint.UnitRegistry()
voltage = 3 * ureg.volt + 40 * ureg.millivolt

# kuchka: the unit is the constructor.
voltage = Volt(3) + Millivolt(40)
```

| Library        | Unit is...                                                | Result type                           |
| -------------- | --------------------------------------------------------- | ------------------------------------- |
| Pint           | looked up on a registry (`ureg.meter`, `"3 m"`)           | one generic `Quantity` for everything |
| physipy        | looked up in a dict (`units["nm"]`)                       | one generic `Quantity` for everything |
| units / unitpy | a string (`unit("m")`, `U("km")`)                         | -                                     |
| impunity       | a string in a function annotation, checked at import time | none at runtime - rewritten away      |
| kuchka         | an ordinary Python name (`Meter`)                         | a distinct Python type per quantity   |

Pint is the mature, general-purpose default: a large unit vocabulary, NumPy/Pandas integration, unit parsing from strings.
`kuchka` isn't trying to replicate that.
impunity is the closest in spirit to `kuchka`'s static-first goal: zero runtime cost once the check has run, at the cost of the "unit" being a string inside an annotation rather than an object that can be constructed, returned, and passed around.

`kuchka`'s bet: `isinstance(Volt(5), Voltage)` should work with no registry, no plugin, and no decorator rewriting a function body.
mypy/ty should understand the arithmetic because it's ordinary overloads on an ordinary class.
The trade-off is a deliberately small, hand-maintained unit vocabulary and no array/NumPy support yet.

## What this is not (yet)

- `Length` has metric prefixes and `Inch`; `Foot`/`Yard`/`Mile` aren't implemented yet.
- No NumPy/Pandas integration.
  `Fraction` doesn't vectorize into `ndarray` cleanly, and per-sample scalar wrapping is the wrong shape for high-rate acquisition.
  The intended pattern for now is buffering raw floats at the acquisition boundary and converting once there's a value worth reasoning about.
- No JSON/DB persistence layer.
  When it's added, the storage format may use a unit string (`{"value": 4.2, "unit": "V"}`), since that's a serialization concern rather than part of the application-facing API - loading it back must reconstruct a typed measurement, never hand back a bare number.
- No point-in-time type.
  `Time` is a span (a duration, a timeout, a sample period), not a timestamp.
  A timestamp would need the same affine treatment `Temperature` gets.

## Known limitations

- **`ty` doesn't yet enforce `Self`-narrowed arithmetic across sibling quantity types the way `mypy --strict` does.**
  `Volt(5) + Ampere(2)` is a `mypy --strict` error but is currently accepted by `ty`.
  Both tools agree on naked-number arithmetic (`Volt(5) + 4.2`) and on the `Temperature` cases.
- **The dimension vocabulary is small on purpose.**
  `Resistance * Resistance` and similar mathematically-valid-but-unregistered products raise `UnrepresentableDimensionError` at runtime rather than returning a typed result, since the fallback overload on each quantity type has to accept `object` to stay compatible with the base class.
- **kuchka's angular units are exact relative to a fixed internal constant, not to the true value of π.**
  See [Exact by construction](#exact-by-construction-and-its-limits) above.
- No special array, NumPy/Pandas support.

Open design questions and planned work are tracked on the [issue tracker](https://codeberg.org/dimonade/kuchka/issues), not in this file.

## History

The original pre-implementation design proposal lives at [`docs/introduction/design_proposal.md`](docs/introduction/design_proposal.md), kept as a record of the initial thinking.
