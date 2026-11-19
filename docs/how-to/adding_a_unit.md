# Adding a unit

A unit belongs to one quantity type, such as `Length`, and measures in the canonical unit of that type: metres for a length, seconds for a time, kilograms for a mass.
Units for the main library live in a module of `kuchka.units`, placed as [Where the module goes](#where-the-module-goes) says.
Units of a historical or cultural system live under `kuchka.units.archaic` and follow [Adding archaic units](adding_archaic_units.md).
Both start the same way.

## Where the module goes

A base dimension (`length`, `mass`, `current`, `thermal`, `amount`, `luminous_intensity`) and an axis that is not a dimension of its own (`angular`, `solid_angle`, `proportion`, `logarithmic`) have a module at the top level of `kuchka.units`.
The time family is the `temporal` package, because its quantities share two dimensions.
Every other quantity lives in the themed package of the relation that defines it:

| Package                         | Holds                                                                                                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `geometry`                      | measures built from length alone: area, volume                                                                                                  |
| `kinematics`                    | motion: velocity, acceleration, angular velocity                                                                                                |
| `mechanics`                     | force and the work it does: force, torque, pressure, stress, density, energy, power, energy density                                             |
| _`mechanics`, continued_        | specific energy, specific power, momentum, impulse, velocity squared                                                                            |
| `electromagnetics`              | charge, voltage, resistance, conductance, capacitance, inductance                                                                               |
| _`electromagnetics`, continued_ | permittivity, permeability, AC power, magnetic flux, flux density, field strength, specific charge and current                                  |
| `information`                   | data and data rate                                                                                                                              |
| `chemistry`                     | what is measured per mole: molar mass, concentration, energy, flow rate, heat capacity, catalytic activity, and more                            |
| `photometry`                    | light as the eye sees it: flux, energy, exposure, illuminance, luminance, efficacy                                                              |
| `radiation`                     | radioactive activity, and the doses it deposits: absorbed dose, equivalent dose, exposure, their rates, and activity per volume, mass, and area |
| `thermodynamics`                | how heat changes a temperature: heating rate, heat capacity, specific heat capacity, entropy                                                    |

A quantity that fits two packages lives where its defining relation lives, and the other package imports it.
`Energy` is `Force * Length`, so it is in `mechanics`, and the electrical units reuse it for the watt-hour.
A package imports only from the top level and from the packages before it, in the order `RANK` fixes in `tests/units/test_package_layering.py`, and the test fails when an import runs the other way.

A package exists as soon as one quantity has its home in it.
A quantity with no package yet, such as a luminance, starts the package it belongs to, with its own `__init__.py` listing its leaves.

## Define the unit

<!-- doc-test: skip an illustration of a module that does not exist in the library -->

```python
from fractions import Fraction

from kuchka.dimensions import LENGTH
from kuchka.quantities import UnitDef

SHELL = UnitDef(
    "shell",
    "shell",
    Fraction(3, 100),  # metres, the canonical unit of length
    LENGTH,
    words=("shells",),
)
```

The arguments are the name, the display symbol, the scale in canonical units, and the dimension.
Arithmetic between a `Fraction` and a `Decimal` is not defined, so derive related scales from one `Fraction`.

## Spellings

Each unit is known by its symbol and name, and by extra spellings of two kinds:

- `aliases` are symbols, matched exactly after Unicode normalization, so case carries meaning (`mV` is not `MV`),
- `words` are names and spoken forms, matched without regard to case, with a trailing plural `s` tolerated.

A table refuses to build when one spelling could mean two units, so a clash surfaces when the module is imported.
`docs/concepts/unit_spellings.md` has the full rules.

## One unit under several names

The krakenpeople who live their whole life upside down call the shell the _llehs_, which is "shell" spelled backwards.
Three forms express "the same unit again", and the choice carries meaning:

1. **A plain alias**, when the second name is the same unit:

   <!-- doc-test: skip an illustration of a module that does not exist in the library -->

   ```python
   SHELL = UnitDef("shell", "shell", Fraction(3, 100), LENGTH, words=("shells", "llehs"))
   LLEHS = SHELL
   Llehs = Shell
   ```

   `Llehs(3)` builds the same value as `Shell(3)` and displays as `3 shell`, because the display symbol belongs to the definition.
   This is how `AmpereSecond` relates to `Coulomb`.

2. **An extra spelling only**, when the name is needed at a boundary and nowhere else: put it in `aliases` or `words` and add no constant.

3. **A separate definition with an identical scale**, when two naming traditions agree numerically but are different things.
   `Millilitre` and `CubicCentimetre` are separate for this reason.
   Pick this form when a unit would otherwise be recorded as someone else's alias.

## A type that reads another type's units

A specialisation measures what its principal kind measures.
The krakenpeople's **depth** is a length, so `Depth` reuses every unit of `Length` and mints no lookalike, the way `SamplingPeriod` reuses the units of `Time` and `Stress` those of `Pressure`.
The module sets the canonical unit from the principal kind and derives its table from the principal kind's table with `.map`, which wraps each constructor so that it reads its result through the conversion:

<!-- doc-test: skip an illustration of a module that does not exist in the library -->

```python
Depth._canonical_unit = METRE  # the principal kind's own unit


def _via_length(constructor):
    def read_as_depth(value):
        return constructor(value).to_depth()

    return read_as_depth


DEPTH_UNITS: UnitTable[Depth] = LENGTH_UNITS.map("DEPTH_UNITS", _via_length)
```

The source table is annotated `UnitTable[Length]`, which is what lets a type checker see `.map`.
The `_UNITS_OF` entry is `units_of(DEPTH_UNITS)`, and the derived table joins the derived-table cases in the unit tests, beside `SAMPLING_PERIOD_UNITS` and `STRESS_UNITS`.
A specialisation that needs a symbol of its own, such as the volt-ampere beside the watt, defines its own units instead.

## Multiples and prefixes

A unit defined as a multiple of another derives its scale from it:

<!-- doc-test: skip an illustration of a module that does not exist in the library -->

```python
KRAKENTENTACLE = UnitDef("krakententacle", "kt", Fraction(43, 3) * SHELL.scale, LENGTH)
```

Prefixed units have two helpers in `kuchka.internal.prefixes`:

- `with_prefix(prefix, base)` builds the unit for a prefix applied to any base `UnitDef`, with an SI prefix (`prefixes.KILO`, powers of ten) or an IEC binary one (`prefixes.KIBI`, powers of two), so the scale, the name, the symbol, and every pairing of prefix and base spellings follow from the two:

  <!-- doc-test: skip an illustration of a module that does not exist in the library -->

  ```python
  from kuchka.internal import prefixes

  KILOSHELL = with_prefix(prefixes.KILO, SHELL)  # 1000 shells, 30 m
  ```

- `prefixed_unit(prefix, name, symbol, dimension)` builds one for an SI unit that is not defined yet, and is what the SI modules use. It takes a `coherent_offset` for a dimension whose canonical unit is not the coherent SI unit: mass counts in kilograms, so every gram prefix carries `-3`.

`with_prefix` takes an affine base too, such as the degree Celsius, and keeps its offset, because a prefix changes the size of a unit and not where its scale starts.
It pairs every spelling of the base with the prefix, and `paired_aliases` and `paired_words` choose the spellings that take part when one of them reads as another unit once a prefix stands before it: `mC` would be a millicoulomb, so the Celsius units pair only `°C` and `° C`.

## Ladders

A family of prefixed units must hold every step of a thousand between its smallest and its largest member, and a test finds the families from the symbols and fails for a gap.
Each family is also a ladder, the run of units `auto_scale()` moves a measurement along, declared in the unit module beside the table and bound in the `_LADDERS_OF` block of `kuchka/units/__init__.py`:

<!-- doc-test: skip an illustration of a module that does not exist in the library -->

```python
KRAKEN_LENGTH_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (SHELL, KILOSHELL, MEGASHELL),
)
```

A ladder lists the units of one family, smallest first, and `bind_ladders` refuses a ladder of one unit, a unit the type does not display in, units that do not grow, a unit on two ladders, and a unit that starts away from zero.
A quantity that has two families, such as the joule and the watt-hour, has two ladders, and a unit stands on one of them.
A quantity whose units have no family of prefixes in steps of a thousand has no ladder, and gives its reason in the coverage test, which also fails for a prefixed unit that is on no ladder.
[Readable units](../concepts/auto_scaling.md) describes the rule that picks a unit.

## Constructor, table, and export

<!-- doc-test: skip an illustration of a module that does not exist in the library -->

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
    ...
    """
    return Length(to_exact(value) * SHELL.scale, SHELL)


KRAKEN_LENGTH_UNITS = unit_table(
    "KRAKEN_LENGTH_UNITS",
    {
        SHELL: Shell,
        KILOSHELL: Kiloshell,
    },
)
```

The `Examples` section shows at least two kinds of example, as [Writing unit documentation](writing_unit_documentation.md) describes.
Each module owns one hand-written `__all__` naming its constants, constructors, and tables.
A published module is exported the way its neighbours are, following the comment above `__all__` in `kuchka/units/__init__.py`.
A published unit also joins its type's table there (the `_TABLE_OF` block, which also lets `parse` read the type's units), and `just generate-api` promotes its constructor to the top level.

## Checklist

- [ ] the unit, with an exact scale and the spellings people use,
- [ ] a constructor with a docstring and [two kinds of example](writing_unit_documentation.md),
- [ ] a place in the module's `*_UNITS` table and `__all__`,
- [ ] a place on the `*_LADDERS` of a prefixed unit, with no step of a thousand left out of its family,
- [ ] a place in the right package, and its imports and `__all__ +=` lines,
- [ ] wiring: `_TABLE_OF` for a published unit, `extend_units` with the table for an archaic one,
- [ ] `just generate-api` for a published unit,
- [ ] [tests](adding_tests.md) for what discovery cannot know,
- [ ] a changelog line.
