# Writing documentation

A public name carries a docstring and a doctest.
A change that users notice carries a changelog line.
A concept that needs more than a docstring gets a page.

## What docstrings say

A docstring describes what something is and does.
It names the idea and leaves the history, the alternatives, and the tooling out.
It refers to concepts, not to other files, because a file name goes stale when the file moves.
Docstrings stay short enough to read in a terminal, and as long as the reasons for the definition need.

Unit modules follow the NumPy docstring style, with `units/mass.py` as the model, and [Writing unit documentation](writing_unit_documentation.md) describes their sections and the kinds of example they carry.

## Doctests

Every constructor has examples, and every example runs.
An example imports what it uses from the public paths, `kuchka` and `kuchka.units`, so a reader can copy it.
Each import line names one thing, as the source does, so that adding or removing an example touches only its own lines.
Write an expected result as the printed text, or as an equality check that prints `True`, and write an error in the traceback form with an ellipsis for the message.
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
- [ ] [two kinds of example](writing_unit_documentation.md) per constructor, with their imports,
- [ ] a page or example when a concept needs one, with skip markers where a block cannot run,
- [ ] `prettier` applied, and the page linked,
- [ ] a changelog line.
