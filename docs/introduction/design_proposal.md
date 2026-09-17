# Engineering Measurements for Python

## Motivation

Engineering software routinely moves physical measurements through acquisition, processing, analysis, reporting, and persistence.
A value such as `4.2` is not meaningful on its own: it may represent volts, millivolts, amperes, seconds, degrees Celsius, or something else entirely.

Using naked numeric values throughout an engineering pipeline makes unit errors easy to introduce and difficult to detect.
A value can be converted incorrectly, combined with an incompatible quantity, or silently lose its unit while passing through a function that accepts an ordinary `float`.

These failures are particularly dangerous because the resulting program often remains perfectly valid Python.
The mistake is semantic rather than syntactic, and therefore may survive testing until it produces an incorrect engineering result.

The goal of this project is to provide a measurement system for Python in which **physical quantities are first-class values**, while presenting an API that is natural to engineers regardless of their familiarity with Python.

The intended user should not need to understand registries, unit strings, dimensional-analysis internals, decorators, metaclasses, or the representation used internally by the library.
They should be able to work with measurements in terms that correspond directly to the engineering concepts they already use.

A typical engineer-facing interface should therefore look approximately like:

```python
from measurements import Ampere, Milliampere, Volt

voltage = Volt(4.2)
current = Milliampere(150)

power = voltage * current
```

The exact names and resulting types are implementation decisions, but the principle is not:

> The obvious engineering notation should also be the safe notation.

## Design Goals

### 1. Measurements must be distinct from ordinary numerics

A measurement is not merely a `float` with metadata attached to it.

The following should therefore be invalid:

```python
analyse_voltage(4.2)
```

when the function expects a voltage.

Instead:

```python
analyse_voltage(Volt(4.2))
```

should be required.

The system should make it possible to enforce this distinction both statically, through type checking, and dynamically, at runtime boundaries where values enter the system.
A raw numeric value may exist at an external boundary — for example, a sensor API, CSV file, database driver, or network message — but it should be converted into a measurement immediately.
Once inside the measurement domain, naked numeric values should not be permitted to silently propagate.

### 2. Engineering concepts should be represented by named types

The public API should expose meaningful engineering types such as:

```python
Voltage
Current
Resistance
Power
Temperature
Pressure
Length
Time
```

These types describe the physical quantity and not its storage representation.

For example:

```python
def calculate_power(voltage: Voltage, current: Current) -> Power: ...
```

communicates considerably more information than:

```python
def calculate_power(voltage: float, current: float) -> float: ...
```

The type itself becomes part of the engineering documentation.

### 3. Units should be selected through Python names, not strings

The public interface must not require users to provide unit names as strings:

```python
Unit("meter")
Unit("m")
Quantity(5, "meter")
```

This introduces a runtime vocabulary that is invisible to Python's type system, is difficult for IDEs and static analysis to understand, and makes spelling and naming conventions part of the API in an unnecessarily fragile way.

The preferred interface is explicit Python names:

```python
Meter(5)
Millimeter(5)
Kilometer(5)
```

or an equivalent API where the unit is encoded directly in the constructor or type.

The system should favour discoverability through normal Python tooling: completion, documentation, static analysis, and symbol search.
There should be no need for engineers to remember whether a particular string is `"m"`, `"meter"`, `"metre"`, or another accepted spelling.

### 4. Units must be readable without being noisy

The API is intended for engineering code, not for demonstrating unit-system completeness.

The common case should remain compact:

```python
voltage = Volt(4.2)
current = Milliampere(150)
```

The library should avoid conventions that turn otherwise readable engineering code into collections of constants written in unusual capitalization or registry boilerplate.
Names should look like normal Python classes and normal engineering terminology.
The API should also distinguish between physical quantity types and unit construction without requiring the user to understand the distinction.

### 5. Dimensional correctness must be enforced

Operations between incompatible quantities must fail clearly.

For example:

```python
Volt(5) + Ampere(2)
```

must not produce a result.

Likewise, functions accepting a voltage must not silently accept current, power, or an untyped number.

Errors should describe the engineering mistake directly.

For example:

```text
Cannot add Voltage and Current.
Expected two quantities with the same physical dimension.
Received Voltage (V) and Current (A).
```

The exact exception hierarchy is an implementation detail, but failures should be specific, actionable, and understandable to a user who may not know anything about the internals of the measurement system.

### 6. Unit conversion must be automatic where it is unambiguous

Equivalent units should interoperate naturally:

```python
Volt(1) + Millivolt(500)
```

should produce a voltage value representing `1.5 V`.

Conversion should not require explicit conversion calls merely because two compatible units use different prefixes.

Explicit conversion should nevertheless be available where the representation is relevant, for example:

```python
voltage.to(Millivolt)
```

or an equivalent typed API.

The normal arithmetic path should be concerned with physical quantities and avoiding forcing users to manually normalise units.

### 7. Derived dimensions must emerge naturally from arithmetic

The system should understand relationships between physical quantities.

For example:

```python
voltage * current
```

produces power.

Likewise:

```python
distance / time
```

produces velocity.

The user should not need to manually specify that the resulting value is a particular unit or register a formula with the system.

Dimensional analysis should be performed by the measurement layer.

The arithmetic engine responsible for this can be substantially more sophisticated than the public API. Its complexity should remain an implementation detail.

### 8. Static typing and runtime validation should complement each other

Python's type system can detect many mistakes before execution, but type annotations alone cannot guarantee runtime safety because data commonly enters Python through dynamically typed interfaces.

The architecture should therefore have two complementary safety mechanisms.

Static typing should provide:

```python
def process(voltage: Voltage) -> Power: ...
```

and allow tools such as mypy or pyright to reject:

```python
process(4.2)
process(Current(...))
```

Runtime validation should protect the boundaries where static typing cannot.

For example:

```text
sensor / file / network / database
                |
                v
        boundary conversion
                |
                v
      strongly typed measurement
                |
                v
        engineering pipeline
```

The intended invariant is:

> Once data crosses into the measurement domain, every physical measurement carries its dimensional type and unit semantics with it.

### 9. Persistence must preserve units

A measurement must not lose its dimensional information merely because it is serialized.

A database row, report dataset, dataframe, exported file, or intermediate representation should not turn:

```python
Volt(4.2)
```

into:

```python
4.2
```

without an explicit decision to discard the unit.

Persistence mechanisms should have well-defined strategies for retaining dimensional information, preferably in a machine-readable form.

The exact storage representation may vary by backend, but loading data back into the application must reconstruct a measurement rather than silently returning a naked numeric value.

### 10. The library should make the safe path the easiest path

The central usability principle is:

> Engineers should not have to think about the measurement system while using it.

An engineer should be able to write:

```python
voltage = Volt(12)
current = Milliampere(250)
power = voltage * current
```

and obtain correct unit-aware behaviour without learning how quantities, registries, prefixes, dimensions, or conversion tables work.

Advanced users should be able to access those facilities when necessary, but the basic interface should not expose them.

Safety should come from the architecture rather than from requiring users to remember a large set of rules.

# Architecture

The implementation should be divided into several layers with deliberately narrow responsibilities.

## Public Domain API

This is the only layer ordinary engineers should need to know.

It exposes named measurement types and convenient unit constructors:

```python
Voltage
Current
Power
Resistance

Volt
Millivolt
Kilovolt

Ampere
Milliampere
Kiloampere
```

and so on.

This layer should contain little or no dimensional-analysis machinery. Its responsibility is to provide a stable, readable, typed interface.

The public API should be intentionally boring.

That is a feature.

## Quantity Core

Underneath the public API is a generic quantity representation.

Conceptually:

```text
Quantity
├── magnitude
└── dimension
    └── unit / scale information
```

It is responsible for:

- arithmetic;
- conversion;
- dimensional compatibility;
- comparison;
- derived dimensions;
- normalization;
- numeric representation.

The public measurement classes should delegate to this machinery instead of reimplementing unit mathematics independently.

## Dimension System

The dimension system defines physical relationships independently of particular units.

For example:

```text
Voltage
    = Mass x Length^2 / (Time^3 x Current)

Power
    = Mass x Length^2 / Time^3

Velocity
    = Length / Time
```

The dimension system should work in terms of canonical dimensional identities.

Units such as `Volt` and `Millivolt` should therefore represent different scales of the same dimension and not separate arbitrary concepts.

## Unit Definitions

Units should be declared internally in a structured, typed form.

A definition should contain enough information to establish:

```text
physical dimension
canonical representation
scale
offset, where applicable
display name
conversion rules
```

but this representation should not be exposed to normal users.

Unit definitions should be data-driven internally so that the implementation does not require hundreds of hand-written arithmetic classes.

## Boundary Layer

Every source of external data should have an explicit conversion boundary.

Examples include:

```text
ADC / sensor
CSV
JSON
database
network protocol
test fixtures
third-party arrays / dataframes
```

A boundary converts raw representations into measurement values.

For example:

```python
voltage = Millivolt(sensor.read_voltage())
```

After this conversion, the remainder of the system operates on `Voltage`, not `float`.

This boundary is where assumptions about external units belong.

It is also where unit metadata must be validated rather than guessed.

## Static Type Layer

The package should provide conventional Python type annotations that work with mainstream tooling.

The preferred user experience is ordinary typing:

```python
def analyse(signal: Voltage) -> Measurement: ...
```

rather than custom decorators, string annotations, or a parallel annotation language.

Where Python's type system cannot represent a dimensional relationship precisely, runtime checks should fill the gap rather than introducing an unfamiliar annotation syntax.

The static typing layer should therefore be treated as an aid to safety and developer tooling, not as the sole mechanism enforcing dimensional correctness.

# Ergonomics Before Safety

The project should explicitly adopt a two-stage design philosophy.

First, establish the API that engineers naturally want to use.
Then establish the mechanisms required to make that API safe.

This matters because an extremely safe API that engineers dislike will simply be bypassed.

The goal is not to force engineers to learn a measurement framework.
The goal is to make the correct representation the natural representation.

The desired experience is closer to:

```python
voltage = Volt(4.2)
current = Milliampere(250)
```

with all unit algebra occurring behind the scenes.

# Safety Invariants

The implementation should ultimately aim to establish the following invariants.

**A physical quantity has a physical type.**
A voltage is not represented merely by a float.

**A physical quantity always has dimensional information.**
A value cannot silently become dimensionless during ordinary application operations.

**Raw numerics may enter only at explicit boundaries.**
Acquisition, deserialization, and other external interfaces must convert them into measurements.

**Incompatible dimensions cannot participate in arithmetic.**
`Voltage + Current` is an error.

**Equivalent units are transparently compatible.**
`Volt(1)` and `Millivolt(1000)` represent compatible quantities.

**Derived quantities retain their dimension.**
`Voltage * Current` produces `Power`, not an untyped numeric result.

**Serialization cannot silently strip units.**
Measurement data written by the system remains identifiable as measurement data when read back.

**The public API does not require knowledge of the implementation.**
An engineer should be able to use the system correctly without understanding registries, conversion tables, dimensional vectors, generic quantity classes, or internal numeric representations.

# Non-Goals

The project is not intended to become a general-purpose symbolic mathematics framework.

- It is not intended to expose every possible unit-system feature directly to ordinary users.
- It is not intended to replace NumPy, Pandas, or other data-processing libraries.
- It is not intended to make Python behave exactly like Rust's type system.

Instead, the goal is to use Python's existing runtime and typing capabilities to approximate the strongest practical engineering guarantees while preserving a conventional Python programming experience.

The project should prefer a small amount of sophisticated machinery behind the scenes over exposing that machinery to every user.

# Guiding Principle

The library should make this:

```python
voltage = Millivolt(sensor.read())
analyse(voltage)
```

the normal path.

It should make this:

```python
analyse(sensor.read())
```

obviously wrong.

And it should make this:

```python
analyse(4.2)
```

difficult to introduce, easy for static analysis to reject, and guaranteed to fail at runtime when it crosses a protected API boundary.

- The engineer should see **Voltage**, not `Quantity[float, Dimension[...]]`.
- The engineer should see **Millivolt**, not `"mV"`.
- The engineer should see **Power**, not the result of a unit algebra expression.

All of the machinery required to make those statements true belongs behind the API.

# Initial Implementation Draft-Proposal-However-you-call-it

The first implementation should deliberately avoid attempting to solve every possible unit-system problem.
The objective of version 0.1 is to establish the API and invariants that the rest of the system can grow around.
The implementation should begin with a relatively small set of SI quantities and common engineering prefixes, then expand only after the core semantics are stable.

## 1. Public Package Structure

A possible package layout is:

```text
measurements/
    __init__.py
    quantities.py
    units.py
    dimensions.py
    errors.py
    conversion.py
    numeric.py
    boundary.py
    serialization.py
    typing.py
```

The public package should re-export the engineer-facing names from `__init__.py` so that normal usage remains simple:

```python
from measurements import Volt, Milliampere, Voltage, Current
```

The internal modules should not be part of the expected user interface.

## 2. Separate Quantity Types from Unit Constructors

The first concrete design decision should be:

```python
Voltage  # semantic type
Volt  # constructor / unit-specific representation
Millivolt  # constructor / unit-specific representation
Kilovolt  # constructor / unit-specific representation
```

The same applies to other dimensions:

```python
Current
Ampere
Milliampere

Resistance
Ohm
Kiloohm

Power
Watt
Kilowatt
```

A sensible invariant is:

```python
v1 = Volt(4.2)
v2 = Millivolt(4200)

assert isinstance(v1, Voltage)
assert isinstance(v2, Voltage)
```

The precise implementation may instead make `Volt` a factory function or a lightweight class deriving from a common constructor abstraction.
The important part is that the static and runtime semantic type remains `Voltage`.

This prevents the type system from exploding into unrelated types such as `VoltVoltage`, `MillivoltVoltage`, and `KilovoltVoltage`.

## 3. Immutable Measurements

Measurement instances should be immutable.

For example:

```python
voltage = Volt(5.0)
```

should represent a stable value. Operations should return new measurements rather than modifying existing ones.

This makes measurements safe to share between analysis stages, easier to reason about, and significantly safer when used with caching, concurrency, and persistent data structures.

A frozen dataclass is a reasonable starting implementation mechanism, although the public API should not depend on that implementation detail.

## 4. Canonical Internal Representation

Each quantity should have a canonical internal representation for arithmetic.

For voltage this could simply be volts:

```text
Volt       -> 4.2
Millivolt  -> 0.0042
Kilovolt   -> 4200.0
```

The instance still retains enough information to represent or convert its engineering unit as required by the API.

Canonicalisation should happen automatically at construction and conversion boundaries.

The implementation should avoid repeated conversion between prefixes during arithmetic.

## 5. Strongly Typed Arithmetic

The first implementation should explicitly support:

```python
Voltage + Voltage        -> Voltage
Voltage - Voltage        -> Voltage
Voltage * Current        -> Power
Power / Voltage          -> Current
Voltage / Current        -> Resistance
```

and analogous relationships for the initial quantity set.

Incompatible operations should fail deterministically.

For example:

```python
Volt(5) + Ampere(2)
```

should raise a dedicated dimensional exception.

Multiplication and division should use a central dimension algebra instead of a large collection of hand-written pairwise special cases.

For example, dimensions can be represented internally as exponent maps:

```text
Length      -> {L: 1}
Velocity    -> {L: 1, T: -1}
Power       -> {M: 1, L: 2, T: -3}
```

This gives the implementation a general mechanism for deriving compound dimensions.

Named domain types can then map those dimension signatures to engineering concepts such as `Power` or `Velocity`.

## 6. Explicit Conversion API

Normal arithmetic should convert compatible units automatically.

Explicit conversion should use types and completely avoid strings:

```python
voltage = Volt(4.2)
voltage_in_mv = voltage.to(Millivolt)
```

The conversion target should therefore be a Python symbol that IDEs can discover and type check.

The following should not be part of the normal API:

```python
voltage.to("mV")
voltage.to("millivolt")
```

## 7. Numeric Construction Rules

Construction from numerics should be deliberately strict.

The initial implementation should accept a controlled numeric protocol such as:

```python
int
float
Decimal
Fraction
```

where appropriate.

It should reject arbitrary objects rather than coercing them through `float(...)` automatically.

The constructor should also reject measurement objects of an incompatible dimension instead of attempting to interpret their magnitude.

For example:

```python
Volt(Ampere(5))
```

must fail.

The conversion from a raw number into a physical quantity should always occur through an explicitly named unit constructor:

```python
Volt(5)
Millivolt(5000)
```

The library should not provide a generic ambiguous constructor such as:

```python
Quantity(5)
```

## 8. Type Checking

The project should support ordinary Python static analysis from the beginning.

The initial target should be modern mypy, ty, and/or pyright with strict settings.

Example:

```python
def analyse(voltage: Voltage) -> VoltageReport: ...


analyse(Volt(5))  # valid
analyse(4.2)  # type error
analyse(Ampere(2))  # type error
```

The static layer should not require decorators, stringified units, generated annotations, or a custom syntax.

Where static typing cannot express the dimensional algebra, runtime validation remains authoritative.

## 9. Runtime API Guards

Public application functions should be able to validate their inputs at runtime without requiring application developers to write repetitive `isinstance` checks everywhere.

The simplest first approach is to use normal Python type checks at the boundaries:

```python
if not isinstance(voltage, Voltage):
    raise TypeError(f"expected Voltage, got {type(voltage).__name__}")
```

This can later be centralized into reusable validation helpers.

The important point is that runtime protection should be implemented in terms of actual domain types, not strings or registered names.

## 10. Explicit Errors

Define a small, stable exception hierarchy from the beginning.

For example:

```text
MeasurementError
-> InvalidMeasurementError
-> InvalidUnitError
-> IncompatibleDimensionError
-> InvalidConversionError
-> SerializationError
-> etc...
```

The exact names can evolve, but the distinction between ordinary programming errors and measurement-system errors should be clear.

Error messages should always include the relevant engineering concepts.

For example:

```text
Cannot add Voltage and Current.
Voltage has dimension [M L² T⁻³ I⁻¹].
Current has dimension [I].
```

The human-readable engineering names should be preferred over exposing an internal representation alone.

## 11. Unit Registry Exists Internally, Not Publicly

A registry-like mechanism is still useful internally.

The implementation will need a catalogue that maps unit definitions to their dimensions, scales, offsets, and names.

That does not mean users should ever have to write:

```python
registry = UnitRegistry()
```

The registry should be initialized by the library and used internally by constructors and conversion operations.

This is an important distinction -- a registry can be a good implementation technique while still being a bad public API.

## 12. Prefix Generation

SI prefixes should be generated internally from a compact definition rather than implemented independently for each unit.

The public surface can still expose explicit names:

```python
Millivolt
Microvolt
Kilovolt
Megavolt
```

while internally they are simply scaled versions of the same base unit.

This gives a small amount of declarative implementation machinery without requiring end users to interact with it.

The generation mechanism should produce normal exported Python symbols so that IDE completion works naturally.

## 13. Temperature and Offset Units

Temperature should be considered a special case from the beginning, even if it is not part of the first milestone.

Celsius and Fahrenheit are not merely multiplicative scales of Kelvin; they include offsets.

The conversion model therefore needs to distinguish:

```text
scale-only conversions
scale + offset conversions
```

The implementation should not assume every unit can be represented as:

```text
value * scale
```

Ignoring this early will make the design difficult to extend later.

## 14. Persistence

The initial serialization format should be simple and explicit.

A measurement serialized to JSON-like data might become conceptually:

```json
{
  "value": 4.2,
  "unit": "V"
}
```

The string here is acceptable as a **storage format**, because it is not the application API.
The important requirement is that deserialization reconstructs a typed measurement rather than returning `4.2`.

The serializer should validate the unit identifier against the known internal unit catalogue and fail on unknown or malformed units.

Application code should not generally manipulate these unit strings directly.

## 15. DataFrame / NumPy Integration

NumPy and Pandas support should not be part of the first core milestone.

They introduce significant additional design questions around:

- scalar versus vector quantities;
- dtype propagation;
- ufunc dispatch;
- missing values;
- serialization;
- dataframe columns carrying units;
- performance.

The core API should be designed so these integrations can be added later without changing the underlying measurement semantics.

A likely future model is:

```python
voltage: VoltageArray
```

rather than allowing a normal `ndarray[float]` to masquerade as a voltage array.

## 16. Testing Strategy

The safety properties should be encoded as tests, while documentation may provide reasoning for edge cases and uncertainties.

At minimum, the initial test suite should cover:

```python
Volt(5) + Volt(1) == Volt(6)
Volt(1) + Millivolt(500) == Volt(1.5)

Volt(5) + Ampere(1)  # raises IncompatibleDimensionError

Volt(5) * Ampere(2)  # Power
Volt(5) / Ampere(2)  # Resistance

analyse(Volt(5))  # valid
analyse(5.0)  # runtime failure
analyse(Ampere(2))  # runtime failure
```

The test suite should also include property-based tests for conversion and dimensional arithmetic once the core behaviour stabilizes.

Examples of useful properties include:

```text
convert(convert(x, A), B) == convert(x, B)
convert(convert(x, A), A) == x
x + y == y + x          # where addition is valid
x - x == zero_dimension # where meaningful
```

For unit prefixes, the tests should verify exact expected scale relationships.

## 17. Initial Scope

The first release should intentionally cover a limited engineering vocabulary.

A sensible starting point would be:

```text
Length
Time
Mass
Temperature
Current
Voltage
Resistance
Power
Energy
Frequency
Pressure
Velocity
Acceleration
```

with the most common SI prefixes.

This is enough to exercise:

- base quantities;
- derived quantities;
- multiplicative conversions;
- offset conversions;
- division and multiplication;
- compatibility checking;
- practical engineering usage.

The project should not attempt to implement every obscure unit or imperial variant before the core API is proven.

## 18. Milestones

General collection of steps to serve as an accumulation of building blocks.

### Milestone 1: Core semantics

Implement:

- dimensions;
- canonical units;
- immutable quantities;
- conversion;
- compatible addition/subtraction;
- multiplication/division;
- exception hierarchy;
- named public constructors;
- strict runtime rejection of naked numerics at typed boundaries.

The result should support a small electrical and mechanical subset end-to-end.

### Milestone 2: Static typing

Add and verify:

- mypy/pyright compatibility;
- public type aliases and generic machinery as needed;
- strict package configuration;
- type-checking examples as part of CI.

The static typing should remain conventional Python typing.

### Milestone 3: Persistence

Implement:

- JSON serialization;
- structured export/import;
- explicit unit metadata;
- round-trip tests;
- rejection of unknown units and malformed measurements.

### Milestone 4: Engineering integration

Add:

- NumPy scalar support;
- arrays;
- Pandas integration;
- measurement-aware reporting/export;
- performance benchmarking.

Only at this point should broader integration concerns shape the API.

# Recommended First Technical Direction

A practical first implementation should be deliberately conservative.

The core should use ordinary Python classes and a small internal dimension algebra.
The public API should be expressed entirely in conventional Python types and constructors.

A rough shape might be:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Voltage:
    _volts: float

    def to(self, unit: type[Voltage]) -> Voltage: ...


class Volt(Voltage):
    def __new__(cls, value: float) -> Voltage: ...


class Millivolt(Voltage):
    def __new__(cls, value: float) -> Voltage: ...
```

This code is only illustrative.
A real implementation should avoid duplicating conversion behaviour across every prefixed constructor.

A better internal model is likely:

```text
Voltage
  |
  +-- unit definition
        |
        +-- Volt       scale = 1
        +-- Millivolt  scale = 1e-3
        +-- Kilovolt   scale = 1e3
```

with one quantity implementation handling the actual storage and arithmetic.

For example, conceptually:

```text
Measurement
├── magnitude
├── dimension
└── unit
```

while the public layer provides engineering-specific types around it.

The next implementation decision should be whether arithmetic results remain generic measurements or are promoted to named domain types.
The preferred answer is named domain types whenever the resulting dimension has a registered engineering meaning:

```python
Volt(12) * Ampere(2)  # -> Power
```

rather than exposing:

```python
Quantity(...)
```

to ordinary users.

## Open Technical Questions

The following questions should be resolved during implementation rather than prematurely encoded into the public API:

1. Whether the canonical numeric representation should be `float`, `Decimal`, or a pluggable numeric backend.
2. Whether each named unit constructor is best represented by a small subclass, a factory, or a generated callable while preserving strong annotations.
3. How aggressively derived dimensions should be promoted to named types versus remaining generic quantities.
4. How much type-level dimensional algebra can be represented usefully in mypy/pyright without introducing custom syntax or an overly complex generic API.
5. How array quantities should work without contaminating the scalar API.
6. How persistence should represent units while keeping unit strings strictly confined to serialization boundaries.
7. Whether an existing mature dimensional-analysis engine can be wrapped safely enough to avoid reimplementing difficult conversion mathematics.

These should be answered by small prototypes and tests, not by making the public API depend on an implementation choice too early.

# Final Principle

The project is successful when an engineer can work with measurements naturally and cannot accidentally forget what those measurements mean.

The desired experience is not:

> "Remember to use the unit framework correctly."

It is:

> "This value is a Voltage, so Python and the library take care of the units."

The engineering team should spend its attention on engineering problems, not on unit-registry mechanics.

The complexity required to make that safe belongs in the library itself.

---

This is all a set of guideline principles, some of them might not be implemented in this order, others not at all, and the other others might be implemented in a different way.
