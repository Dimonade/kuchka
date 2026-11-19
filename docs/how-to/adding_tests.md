# Adding tests

New work ships with tests, and the suite does most of the testing for a new unit or type on its own.

## What discovery covers

The shared suites find the library's contents by walking it:

- every concrete quantity type, whatever its shape, gets the generic property and contract suites,
- every published `*_UNITS` table gets the conversion, scaling, and spelling suites, and a check that its families of prefixed units have no gap,
- every quantity type is checked for ladders: it has them, matching its families of prefixed units, or says in the coverage test why it has none, and every laddered type gets the property suite of `auto_scale()`,
- every archaic `*_UNITS` table gets constructor, spelling, iteration, and pickling checks,
- the export tests compare each package's `__all__` with its parts, and the generated API is compared with the committed one.

Add to these suites by adding to the library: a new unit in a table is tested the moment it exists.

## What to add

Write what discovery cannot know:

- **A promised relationship.** A unit's scale against the unit it derives from:

  <!-- doc-test: skip an illustration of a test for a module that does not exist in the library -->

  ```python
  from kuchka.units import length
  from kuchka.units.archaic.krakenpeople import length as kraken_length


  def test_a_shell_is_three_centimetres() -> None:
      assert kraken_length.Shell(1) == length.Centimetre(3)
  ```

- **An alias.** That the second name builds the same value, and that the display symbol stays the original.
- **A multiple or prefix.** The exact scale: `Krakententacle(3)` equals `Shell(43)`.
- **New arithmetic.** A product or quotient a dimension gains, and the result type it returns.
- **A relation between kinds.** A specialisation's conversions, and the listed set of shared dimensions in the kind catalogue test, which changes on purpose when a dimension gains a kind.
- **A new helper or mechanism.** Its own behaviour, including the refusals.

## Conventions

- Tests import by module, from the package that holds it: `from kuchka.units import length`, `from kuchka.units.mechanics import force`, shortened when the name is long.
- Long lists of units and quantities are alphabetical.
- A test module is named for the topic it covers. A test that seals a fix lives with its topic, and no catch-all file collects the rest.
- A banner comment is a single `# Descriptive banner, ends with dot.` line, and a file that needs banners splits into modules.
- Expected values are written out as independent literals, so a test never agrees with the implementation merely because both share a mistake.
- A test is worth writing when no other test already covers its behaviour.

## Running them

`just test` runs the doctests and the test suite.
`just check` runs the generated-API check, `ruff`, `mypy --strict`, and `ty`.
The doctests are the examples of [the unit documentation](writing_unit_documentation.md).

## Checklist

- [ ] a promised relationship per unit that derives from another,
- [ ] a test for each alias, multiple, or prefix,
- [ ] tests for new arithmetic and relations,
- [ ] the shared-dimension list updated when a dimension gains a kind,
- [ ] `just test` and `just check` clean.
