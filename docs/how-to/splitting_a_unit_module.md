# Splitting a unit module

A unit module is one file per quantity.
It outgrows its file when its units fall into groups a reader looks up separately, or when its docstrings and tables run to a thousand lines.
Splitting turns the module into a package of leaf modules, and keeps the import and export rules intact.

## A worked case

The German miles began as one file of 27 units, because every state defined its own mile.
Four miles recur across sources and maps: the geographic, the Prussian land mile, the Reichsmeile, and the Austrian mile.
They stayed in `meile`, and the 23 regional miles moved to `regional_meilen`.
Both files hold the same things as before: units, constructors, a table, and an `__all__`.

## The rules that carry over

- **Each leaf owns one hand-written `__all__`** naming exactly what it defines.
- **A package composes its parts.** In the main library, a mid-level package adds `__all__ += part.__all__` for each leaf, and `kuchka.units` imports the leaves directly.
- **A joint table lives where both halves are visible.** `GERMAN_MEILE_UNITS` holds the principal miles, `GERMAN_REGIONAL_MEILE_UNITS` the regional ones, and `GERMAN_MEILE_UNITS_ALL` joins them in the regional module. Building the joint table checks that no spelling is claimed twice.
- **Each constructor lives in one module**, and its doctest moves with it, with its imports.

## Archaic packages

An archaic package's `__init__.py` holds a docstring and nothing else.
Importing `meile` then makes `Length` display in the four principal miles, and importing `regional_meilen` makes it display in all 27, because that module registers the joint table.

## Main-library packages

A split of a published module also touches the places that list modules:

- the imports in `kuchka/units/__init__.py` (the module import and the wildcard import, and the `__all__ +=` line),
- `tools/generate_api.py` finds leaves by walking the tree, so `just generate-api` picks the new files up,
- the package list in the export test grows by the new package.

## Checklist

- [ ] one hand-written `__all__` per leaf,
- [ ] a joint table where the parts meet, when a caller wants every spelling,
- [ ] imports and exports updated for a published module,
- [ ] doctests moved with their constructors, each with its imports,
- [ ] a [test](adding_tests.md) that the parts share no unit and the joint table is their union.
