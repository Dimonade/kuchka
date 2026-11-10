# Adding archaic units

`kuchka.units.archaic` holds historical, regional, and culturally specific units.
A program imports them explicitly (`from kuchka.units.archaic.russian.length import Arshin`), and they reach no top-level namespace and no generated API.
A quantity type displays in an archaic unit once the module that defines it is imported.

## Layout

One package per tradition and one module per quantity:

```text
kuchka/units/archaic/krakenpeople/
    __init__.py   package docstring
    length.py     the shell and its relatives
    time.py       the bubble
```

A tradition whose units outgrow one module splits as [Splitting a unit module](splitting_a_unit_module.md) describes.
Package `__init__.py` files hold a docstring and nothing else, so importing one module never pulls in another.

## The module

Define the units, constructors, and table as [Adding a unit](adding_a_unit.md) describes.
Then register the table with the quantity type:

<!-- doc-test: skip an illustration of a module that does not exist in the library -->

```python
from kuchka.quantities import Length
from kuchka.quantities.base.units import extend_units

# Importing this module makes Length display in the units of its table.
extend_units(Length, KRAKEN_LENGTH_UNITS)
```

`extend_units` adds the units of the table to those `kuchka.units` bound, after the same kind and dimension checks, and records the table on the type.
The recorded table is how `parse` reads the spellings of an archaic unit once the caller allows archaic units, so a module that passes its units without the table can be displayed in but not parsed.
It is idempotent, so importing a module twice changes nothing.
A module may extend a type with a table that holds the units of another table of the same tradition, as the regional German miles do with the principal ones, because `parse` tells two units apart and not two tables.
Each quantity type needs its own call: `SamplingPeriod` shares the dimension of `Time` and gets a unit only where a module says so.

The bubble is a time, so it takes a second module of the same shape, with `TIME`, `Time`, and a scale of `6` seconds.

## Using the units

<!-- doc-test: skip an illustration of a module that does not exist in the library -->

```python
from kuchka.units.archaic.krakenpeople.length import Shell
from kuchka.units.archaic.krakenpeople.time import Bubble
from kuchka.units.length import CENTIMETRE

reef_wall = Shell(40)
reef_wall.to(CENTIMETRE)  # 120 cm
climb = reef_wall / Bubble(2)  # a Velocity
```

Archaic constructors build the ordinary quantity types, so a value combines with modern units and converts with `.to(UNIT)`.
Archaic units are unpublished: a value displayed in one copies freely, and it pickles after conversion to a published unit.

## Documenting the sources

The module docstring records where the definitions come from and where sources disagree.
A scale is the one historical definition the module adopts, and each distinct calibration is a separate unit.
Docstrings describe what a unit is and how it is used, in the style of [Writing documentation](writing_documentation.md) and [Writing unit documentation](writing_unit_documentation.md).

## Checklist

- [ ] a package docstring and a module per quantity,
- [ ] units, constructors, a `*_UNITS` table, and an `__all__`,
- [ ] `extend_units` for each quantity type the module serves,
- [ ] explicit imports in every doctest,
- [ ] sources and uncertainties in the module docstring,
- [ ] [tests](adding_tests.md): discovery covers the table, and the module adds the relationships it promises.
