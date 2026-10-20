# Writing documentation

A public name carries a docstring and a doctest.
A change that users notice carries a changelog line.
A concept that needs more than a docstring gets a page.

## What docstrings say

A docstring describes what something is and does.
It names the idea and leaves the history, the alternatives, and the tooling out.
It refers to concepts, not to other files, because a file name goes stale when the file moves.
Docstrings stay short enough to read in a terminal, and as long as the reasons for the definition need.

Unit modules follow the NumPy docstring style, with `units/mass.py` as the model: a summary line, `Parameters`, `Returns`, `Notes`, and `Examples`, and a `Sources` and `See Also` at the module level where they help.
A unit's note states its exact definition and relationships, and a module's note records where definitions come from and where sources disagree.

## Doctests

Every constructor has an example, and every example runs.
Doctests run in the module's own globals, so an example imports each unit it uses:

<!-- doc-test: skip an illustration of a docstring that does not exist in the library -->

```python
>>> from kuchka.units.length import CENTIMETRE
>>> Shell(10).to(CENTIMETRE)
30 cm
```

Write an expected result as the printed text, or as an equality check that prints `True`.
`just test` runs them with the rest of the suite.

## Examples

A small example in a docstring teaches one call.
A worked example that spans several files lives in `docs/examples/<name>/` with a `README.md` and the code, which can carry its own tests.
The examples are not run by the documentation tests, so they carry their own.

## Documentation pages

- Pages in `docs/` describe what the library does now, and the README carries the short version.
- Python blocks in a page run as written. A block that cannot run carries `<!-- doc-test: skip <reason> -->` on the line above it.
- Pages are formatted with `prettier`, so tables are column-aligned; `just` has the recipe.
- A new page is linked from the README or from its section's overview.

## Changelog

Entries are short, in the style of the release notes: a few lines about what changed for a user, with no account of how it got there.

## Checklist

- [ ] a docstring on every public name, in the NumPy style, with sources where a definition has them,
- [ ] a doctest per constructor, with its imports,
- [ ] a page or example when a concept needs one, with skip markers where a block cannot run,
- [ ] `prettier` applied, and the page linked,
- [ ] a changelog line.
