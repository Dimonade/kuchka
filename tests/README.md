# Tests

Run everything with `uv run pytest`, and the doctests with `uv run pytest --doctest-modules src/kuchka`.
`just test` does both.
The whole suite takes about twenty seconds.

## Layout

| Directory      | What it holds                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------- |
| `contract/`    | What every quantity type, unit, and family must satisfy, discovered from the library                  |
| `units/`       | The unit machinery: tables, spellings, prefixes, applicability, and the identity of a unit            |
| `quantities/`  | One module per quantity, in the package its type lives in, or a package where a quantity is large     |
| `behaviour/`   | How quantities behave in general: arithmetic, comparison, display, numeric limits, division by zero   |
| `registry/`    | The kind registry: registration, specialisations, contested kinds, and the result type of `*` and `/` |
| `api/`         | The public surface: exports, generated API, naming, and static typing                                 |
| `integration/` | Scenarios that cross several quantities and the text boundary, written as a reader would use them     |
| `docs/`        | Runs the code blocks of the documentation                                                             |
| `support/`     | Discovery of types and units, values, strategies, and made-up types for tests                         |

## What a test is for

1. **Discover the contract.** A contract test takes its cases from the library: the quantity types from the class hierarchy, the units from the published `*_UNITS` tables.
   A type or a unit added later is covered without an edit, and a hand-written list that mirrors the implementation is a list that goes stale.
2. **Parametrize over what can differ.** A type, a family, or a unit is an axis; a magnitude, a pickle protocol, or a bad input fed to the same code is not.
   Loop over those inside the test, and put the input in the assertion message.
3. **Property tests draw their subject.** A Hypothesis test takes the family or the unit as a strategy (`sampled_from`), so one test covers all of them.
   It does not run once per unit.
4. **A hand-written expectation is an independent oracle.** The prefixed scales in `units/prefix_scales.py`, the notations in `units/notations.py`, and the physical relationships are written from the physics, not computed by the code under test.
   Anything else that is derived from the implementation checks the implementation against itself.
5. **One concern per module.** A comment that divides a file in sections is a sign the file is two files.
   A comment above a test says why; it does not say where we are.
6. **Say it once.** A property that holds for every type has a test in `contract/`, and a quantity module does not repeat it.
   `contract/test_overloads.py` holds the product and quotient relationships against the `@overload` declarations, so a quantity module does not restate `A * B = C`.

## Imports

Unit constructors, constants, and tables come in by module, and a quantity is imported by name:

```python
from kuchka import Torque
from kuchka.units.kinematics import angular_velocity
from kuchka.units.mechanics import torque

shaft = torque.NewtonMetre(20) * angular_velocity.RevolutionPerMinute(3000)
```

A module comes in from the package that holds it, and a long module name may be shortened (`from kuchka.units.kinematics import acceleration as acc`).
A module that a local variable shadows takes a `_units` suffix.
Lists of names and cases are alphabetical, and `ruff` keeps the imports sorted.

## Where a new test goes

- It holds for every type or unit: `contract/`, discovered through `tests/support/`.
- It is about one quantity: `quantities/test_<quantity>.py`, or `quantities/<package>/test_<quantity>.py` when the type lives in a themed package such as `mechanics`.
- It needs two or more quantities to make sense: `integration/`.
- It is an example in the documentation: write it in the document, and `docs/` runs it.

## The documentation tests

`docs/` runs the Python blocks of the README and of `docs/concepts` in order, in one namespace per document.
A bare comparison must come out as its comment says (`# False`, or true when there is none), and a line whose comment names an error in backticks, or says `# rejected`, must raise.
A block that cannot run as written carries `<!-- doc-test: skip <reason> -->` on the line above it.
The doctests in `src/kuchka` run with `--doctest-modules`, and the worked examples under `docs/examples` have tests next to them.

## What is still decided by hand

The excluded tables and documents are named, with the reason, where they are excluded.
