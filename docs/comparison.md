# Comparison with existing tools

`kuchka` is not the first Python library for physical quantities.
The established libraries are not simply different implementations of the same idea; most of them optimize for a broader or more dynamic problem than `kuchka` does.

Useful points of comparison include [Pint](https://pint.readthedocs.io/), [Astropy units](https://docs.astropy.org/en/stable/units/), [physipy](https://physipy.readthedocs.io/), [unyt](https://unyt.readthedocs.io/), [forallpeople](https://forallpeople.readthedocs.io/), and [impunity](https://pypi.org/project/impunity/).

## Why the registry keeps appearing

A runtime registry is a sensible abstraction when the unit vocabulary is open and the program needs to discover, define, combine, or parse units dynamically.

Pint uses a `UnitRegistry` to hold unit definitions and relationships.
Its documentation also describes parsing unit expressions and defining custom units.
This is useful when a program cannot assume in advance which units it will encounter.
See [Defining Quantities](https://pint.readthedocs.io/en/latest/user/defining-quantities.html) and the [Pint API](https://pint.readthedocs.io/en/latest/api/base.html).

Astropy has a similar runtime model: a `Quantity` combines a value with a `Unit`, and the same object is designed to work with scalars, sequences, and NumPy arrays.
Astropy also supports unit-aware type annotations such as `Quantity[u.kpc]`.
The distinction is that the unit remains metadata attached to a generic `Quantity`, while `kuchka` makes the engineering quantity itself a nominal Python type.
See [Units and Quantities](https://docs.astropy.org/en/stable/units/) and [Unit-Aware Type Annotations](https://docs.astropy.org/en/latest/units/type_hints.html).

physipy follows the same broad family of design: a `Quantity` carries a physical `Dimension`, and its unit vocabulary is exposed separately.
Its current documentation also emphasizes NumPy, matplotlib, pandas, and scipy integration.
See the [physipy documentation](https://physipy.readthedocs.io/).

unyt is explicitly built around unit-bearing scalar and array objects and provides a unit registry, user-defined units, unit systems, and integration with array-oriented tools.
See the [unyt documentation](https://unyt.readthedocs.io/).

Even impunity, which is much closer to `kuchka` in spirit, takes a different path.
It performs physical-unit checking through annotations and static analysis; its project description says the physical units disappear at runtime after the check and optional rewrite.
That makes it attractive when zero runtime quantity representation is the goal, but it is a different model from persistent typed measurement objects.
See [impunity on PyPI](https://pypi.org/project/impunity/).

The common pattern therefore has a reason behind it.
A generic quantity plus runtime unit metadata is an excellent foundation for an open unit language, dynamic parsing, scientific arrays, and interoperability.

## What `kuchka` changes

`kuchka` starts from a narrower assumption: the engineering vocabulary is curated and known to the application developer.
The physical concept can therefore be represented by an ordinary nominal Python type.

```python
from kuchka import Ampere
from kuchka import Volt
from kuchka import Voltage


def check_supply(voltage: Voltage) -> None: ...


check_supply(Volt(5))
check_supply(Ampere(2))  # static type error
```

`Volt` is an ordinary Python constructor, and the resulting object is a `Voltage`.
There is no application-wide registry involved in constructing the value:

```python
voltage = Volt(5)
assert isinstance(voltage, Voltage)
```

That changes where physical meaning lives.
With a generic unit library, the object is generally interpreted through its runtime unit metadata.
With `kuchka`, the quantity kind is also part of the Python type itself, so an application function can express its contract directly in an ordinary annotation.

The distinction becomes stronger when two concepts have the same physical dimension.
`Frequency`, `SampleRate`, and `BaudRate` all involve inverse time, but `kuchka` can keep them as different nominal types instead of reducing them to one generic dimensional value.
That lets the application say that two values are physically related but semantically distinct.

## Why not make `kuchka` dynamic too?

Because the trade would remove much of the property it is trying to provide.

A fully dynamic unit language needs to answer questions such as:

```text
What does the unit string "mbar" mean?
What does "kg*m/s^2" mean?
Has a plugin defined a new unit?
Can this arbitrary unit expression be converted to that one?
Which equivalency or unit system should apply?
```

A registry is good at answering those questions.

`kuchka` instead asks a different question:

```text
Which engineering concept does this value represent in this application?
```

If the answer is `Voltage`, the application writes `Voltage`.
If the value arrives as configuration data, the boundary may resolve a string through `VOLTAGE_UNITS` and then leave the string world behind.

That closed vocabulary is a constraint, not an omission that the library is secretly trying to remove later.

## The cost of the `kuchka` approach

The same choice that gives `kuchka` nominal quantity types creates real maintenance cost.

A new engineering concept requires a new quantity type, units, arithmetic relationships, static overloads, tests, and documentation.
Generic runtime systems can often accept a new unit or compound expression without adding another nominal application type.

Static arithmetic is also not free.
The runtime can derive dimensions generically, but Python type checkers do not infer an arbitrary mapping such as `Voltage * Current -> Power` from exponent-vector algebra.
`kuchka` therefore declares explicit overloads for registered derived quantities, generated from the same registry the runtime uses.
This keeps common relationships visible to mypy and ty at the cost of a type-level vocabulary that grows with every quantity type.

Array computing is another deliberate boundary.
Astropy, physipy, and unyt are designed to work with array data, and Pint provides NumPy-oriented integration.
`kuchka` is intentionally aimed at scalar engineering values at application and data boundaries, where explicit Python types and static checking are useful.
It is not an array-oriented numerical framework.

## Where the niche is

The intended niche is engineering application code with a known vocabulary and a meaningful need for type-level physical semantics.

That includes code such as:

- configuration loading, where unit-bearing external data becomes a typed value at the boundary;
- device and protocol interfaces, where raw measurements need physical meaning before application logic uses them;
- control logic, where limits and derived values should have explicit physical types;
- test infrastructure and reporting, where measurements move through several stages and should not revert to unexplained numbers;
- ordinary application APIs where `Voltage`, `Current`, `Pressure`, or `SamplingPeriod` are useful function contracts.

It is much less suited to applications whose primary need is arbitrary unit parsing, user-defined units, equivalency systems, or array-native scientific computation.

## So is `kuchka` actually useful?

The defensible claim is narrow:

> `kuchka` is useful when physical quantities should behave like ordinary Python application types, the unit vocabulary can be curated ahead of time, and static type checking is part of the desired safety model.

That is a different optimization target from a general-purpose unit system.
It does not require the established libraries to be wrong, and it does not imply that `kuchka` is a replacement for them.

The open question is whether this narrower mechanism actually changes engineering practice enough to justify its costs.
`kuchka` has no adoption history that can answer that yet.
What it can do is make the mechanism explicit and testable:

```text
General-purpose unit libraries
    value + runtime unit/dimension metadata
    -> optimize for openness, parsing, customisation, arrays, interoperability

kuchka
    value + nominal Python quantity type + curated unit vocabulary
    -> optimize for application-level type checking and engineering semantics
```

The value proposition is therefore not "all other unit libraries chose the wrong design".
It is "there is a useful engineering niche where a smaller, statically visible vocabulary is a better fit than a general-purpose unit language".
