# Writing unit documentation

The documentation of a unit module has two jobs: to explain a physical quantity and the units that express it, and to show the public API doing real work.
Every example is a doctest, so it runs, and every example has a scenario, so a reader learns what is being calculated and why.
[Writing documentation](writing_documentation.md) covers docstrings in general, and this page covers the unit modules.

`units/mass.py` is the model for the shape of a module, and the kinds of example below are what fill it.

## A module docstring

A module docstring follows the NumPy style, in this order:

1. **Title.** The first line is `<Quantity> constructors: <what the family spans>.`, which fits the line length. A module without constructors of its own, because its quantity reads another quantity's units, reads `<Quantity> units: <the units it reads>, read as a <quantity>.`
2. **Summary and introduction.** Name the quantity and the constructors the module provides, show one short example with its public imports, and give the canonical unit with its symbol and what it means physically.
3. **Practical scales.** Describe the range the units cover and where each is at home, with examples from different disciplines where the units reach into them: engineering, medicine, physics, chemistry, biology, astronomy, materials, industry. A unit gets the context it has in practice, so a unit used in one field is shown in that field.
4. **Examples.** Module-level examples that show relationships and features, and that complement the constructor docstrings.
5. **Notes.** The physical definition, the equations, the exact conversion factors, the conventions that explain a symbol or a factor, the distinctions from neighbouring quantities, and the `*_UNITS` table with what it is for.
6. **Sources.** Definitions, standards, and publications, with a note where sources disagree.
7. **See Also.** The related quantity types and the neighbouring unit modules, chosen by direct relationship.

A structural rule (how a module is exported, where it lives) belongs to the comment above the place it applies and stays out of the docstring.

## A constructor docstring

A constructor has a summary, `Parameters`, `Returns`, `Notes` where a definition needs stating, and `Examples`.
The examples show at least two [kinds](#the-example-kinds), and the first is always a typical measurement.
A unit with a story of its own, such as a non-SI, historical, or domain-specific unit, or the canonical unit of a type, earns three or more.

A prefixed variant of a unit that is documented elsewhere (`Kiloohm`, `Megaohm`, `Microvolt`) gets a typical measurement at its own scale, which is a magnitude someone really reads at that prefix, and one example of another kind.
A [boundary example](#5-boundary-interpretation) is a short second example that fits any unit.

The examples import what a reader needs from the public paths, `kuchka` for types and constructors and `kuchka.units` for unit definitions.
A constructor docstring leaves out the import of its own constructor, and a module docstring states its imports once, in the first example.

<!-- doc-test: skip an illustration of a docstring that does not exist in the library -->

```python
def Shell(value: Numeric) -> Length:
    """Construct a length from a magnitude expressed in shells.

    Parameters
    ----------
    value : Numeric
        Length magnitude in shells.

    Returns
    -------
    Length
        Length represented in shells.

    Examples
    --------
    A krakenperson's cabin window is ten shells across:

    >>> from kuchka.units import CENTIMETRE
    >>> window = Shell(10)
    >>> window.to(CENTIMETRE)
    30 cm

    An eight-shell reef hook hangs below the window, so the drop from the sill is:

    >>> window + Shell(8)
    18 shell
    """
```

## The example kinds

The kinds below are a menu.
Pick the ones that show something about this unit, and a module that mixes kinds teaches more than one that repeats a kind.
The first five describe what a unit is, how it converts, and how it combines and enters the program.
The last three show what `kuchka` guarantees, which is the part a unit-conversion helper lacks.

The snippets run as written with these imports:

```python
from fractions import Fraction

from kuchka import (
    Ampere,
    AmpereHour,
    Celsius,
    Centigray,
    Centimetre,
    Charge,
    Current,
    DeltaCelsius,
    Decibel,
    Degree,
    Gray,
    Katal,
    Kilogram,
    Litre,
    Metre,
    Millivolt,
    Newton,
    RadianPerSecond,
    Temperature,
    Time,
    Torque,
    Volt,
    Voltage,
    parse,
)
from kuchka.units import AMPERE, CENTIGRAY, GRAY, HOUR, VOLTAGE_UNITS
```

### 1. Typical measurement

A realistic magnitude, with a sentence that says what is measured and where the unit is at home.
Every public constructor has one.

```python
# A standard radiotherapy fraction.
fraction = Gray(2)
fraction  # 2 Gy
```

### 2. Scale conversion

A conversion that explains a relationship, a convention, or a change of scale.
Choose a conversion with a reason, such as the centigray that equals the older rad, and use it as one example among several, because a module made of conversions alone teaches little.

```python
# A gray is a hundred centigray, and the centigray equals the older rad.
Gray(2).to(CENTIGRAY)  # 200 cGy
```

### 3. Quantity calculation

The quantity in a calculation that means something: accumulating measurements, combining sources, a duration-dependent quantity, an energy, a momentum, a power, or an estimate from measured values.
The operations are the typed ones, so each result is the type its physics gives it, and a stated assumption goes next to the arithmetic that depends on it.

```python
# A course of 30 fractions, each assumed to deliver the same dose.
fraction = Centigray(200)
course = fraction * 30
course.to(GRAY)  # 60 Gy
```

A calculation can also sit behind a signature, which is how the library is meant to be used.
The annotations tell the reader and the type checker what goes in, and the arithmetic inside is checked as it runs:

```python
def runtime(battery: Charge, current: Current) -> Time:
    return battery / current


runtime(AmpereHour(2), Ampere(0.025)).to(HOUR)  # 80 h
```

The static errors a signature catches, such as passing a bare number, are shown in a block marked for the checker, as in the README.

### 4. Concept bridge

An explicit move between quantities that share a dimension and mean different things.
The example uses the conversion method or the registered operator, and states what the new quantity means.

```python
# A catalyst that converts 3 mol of substrate per second is a molar flow of 3 mol/s.
Katal(3).to_molar_flow_rate()  # 3 mol/s

# The rim of a 20 cm drum turning at 2.5 rad/s moves at 0.5 m/s.
RadianPerSecond(2.5) * Centimetre(20)  # 0.5 m/s

# A force of 10 N at a lever arm of half a metre is a torque.
Torque.from_force(Newton(10), Metre(0.5))  # 5 N·m
```

A refusal that names the bridge is a bridge example too, because it shows where the road is:

```python
Katal(3) / Litre(1)  # rejected: `IncompatibleDimensionError`.
```

The message of this error points to `.to_molar_flow_rate()`.

### 5. Boundary interpretation

How a measurement enters and leaves the library.
`parse` reads a complete measurement written as text, and the `*_UNITS` table reads a unit that arrives apart from its number, such as a CSV column or a `{ value, unit }` pair:

```python
parse("5 mV", Voltage)  # 5 mV
VOLTAGE_UNITS["mV"](5)  # 5 mV
parse("21.5 degrees C", Temperature)  # 21.5 °C
```

An example that shows the spellings a real file uses, the historical symbol, or a symbol whose case carries meaning (`mV` against `MV`) says more than the plain one.

A value leaves as formatted text for people, and as an exact magnitude and a unit symbol for storage:

```python
f"{Kilogram(2.35):.1f}"  # '2.4 kg'

stored = Millivolt(Fraction(7, 3))
stored.value_in(stored.unit), stored.unit.symbol  # (Fraction(7, 3), 'mV')
```

### 6. Refusal

A mistake that the library stops, shown as the error it raises.
A reader learns the contract of a type from what it refuses, and the error carries a message that names the dimensions involved:

```python
Volt(1) + Ampere(1)  # rejected: `IncompatibleDimensionError`.
Volt(1).to(AMPERE)  # rejected: `InvalidConversionError`.
parse("150 mA", Voltage)  # rejected: `UnknownUnitError`.
```

In a docstring, the error is a doctest with the traceback form and an ellipsis for the message, as `parse` shows:

<!-- doc-test: skip an illustration of the doctest form -->

```python
>>> Volt(1) + Ampere(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...
```

### 7. Quantity shape

Quantities differ in the arithmetic that makes sense for them, and a module of a non-linear shape shows its own.
A difference of two temperatures is a temperature difference, an angle has a short way round, and a level adds in decibels:

```python
Celsius(25) - Celsius(20)  # 5 ΔK
Celsius(20) + DeltaCelsius(5)  # 25 °C
Degree(350).difference(Degree(10))  # -20 °
Degree(0.1).is_close(Degree(359.9), tolerance=Degree(0.5))  # True
Decibel(3) + Decibel(3)  # 6 dB
```

### 8. Exactness

Magnitudes are exact, so an example can state an equality that floating-point numbers fail:

```python
0.1 + 0.2 == 0.3  # False
Volt(0.1) + Volt(0.2) == Volt(0.3)  # True
```

An exact relationship in the Notes, such as an inch being 25.4 mm, reads best as the equality that proves it.

## Writing a good example

- **A scenario first.** A sentence says what is measured, where, and why the number is what it is. An example that changes a prefix or a digit and nothing else adds no information, so the second example earns its place by showing something the first did not.
- **Variables that carry meaning.** `fraction = Centigray(200)` followed by `fraction * 30` explains itself, where `Centigray(200) * 30` leaves the reader to work out what is multiplied.
- **Contexts that vary.** The scenarios of one module differ from each other, and from those of its neighbours, and each is a real use of the unit. A field is named when the unit belongs to it.
- **Exact results.** An exact result is written exactly. Floating-point arithmetic and approximate expectations are used where the physics is approximate, with the approximation said aloud.
- **Public API only.** An example uses public imports and the documented methods, and every method it calls exists.

## Checking scientific correctness

- Quantities that share a dimension are told apart in the text, and the reference material or system is named where it matters, for a mass, a dose, or a heat capacity.
- Assumptions such as a constant rate or a uniform dose are stated next to the calculation that needs them.
- A historical unit states its exact conversion factor and where the factor comes from.
- A measured quantity is not confused with one derived from it or with an interpretation of it.
- A relationship that is exact is exact in the code: a `Fraction` or an integer, and an equality in the example when it helps.

## Checklist

- [ ] a module docstring with introduction, practical scales, examples, notes, sources, and see also,
- [ ] two or more kinds of example per constructor, the first a typical measurement,
- [ ] prefixed variants with a real magnitude and one example of another kind,
- [ ] a scenario sentence for each example, and varied contexts,
- [ ] public imports, exact results, and the traceback form for an error,
- [ ] `just test` clean, which runs every example.
