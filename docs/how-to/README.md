# How to extend kuchka

These pages explain how to add to `kuchka`, and why each step is there.
They are short on purpose: each covers one task and links to the neighbours.

| I want to add...                          | Read                                                        |
| ----------------------------------------- | ----------------------------------------------------------- |
| a unit of an existing quantity            | [Adding a unit](adding_a_unit.md)                           |
| a historical or cultural measurement set  | [Adding archaic units](adding_archaic_units.md)             |
| a quantity, a type values are built from  | [Adding a quantity](adding_a_quantity.md)                   |
| a dimension, a vector of exponents        | [Adding a dimension](adding_a_dimension.md)                 |
| a product that crosses the angle axis     | [Adding a bridge](adding_a_bridge.md)                       |
| submodules for a unit module that outgrew | [Splitting a unit module](splitting_a_unit_module.md)       |
| tests for any of the above                | [Adding tests](adding_tests.md)                             |
| docstrings, doctests, examples, and pages | [Writing documentation](writing_documentation.md)           |
| a unit module's docstrings and examples   | [Writing unit documentation](writing_unit_documentation.md) |

## The cast

The examples are imaginary, so every step stands out from the real units it resembles.
The _krakenpeople_ of the deep trenches measure length in **shells** and time in **bubbles**:

| Unit   | Quantity | Definition                                                 |
| ------ | -------- | ---------------------------------------------------------- |
| shell  | length   | 3 cm                                                       |
| bubble | time     | the time an air bubble takes to burst at the surface, ~6 s |

Later pages add a few relatives (the `Llehs`, the `Kiloshell`, the `Krakententacle`) and a quantity of their own.
The code blocks illustrate the steps and carry a skip marker, so the documentation tests leave them unrun.

## The shape of every addition

1. **Define** the thing: a `Dimension`, a quantity class, or a `UnitDef`.
2. **Construct** it through a function that takes a plain number, since constructors are how numbers enter the library.
3. **Tabulate** units in a `*_UNITS` table, which maps every spelling to its constructor and refuses a spelling that could mean two units.
4. **Wire** it in: a published unit is bound to its quantity in `kuchka.units`, and an archaic unit registers itself when its module is imported.
5. **Test** it, which mostly happens by discovery.
6. **Document** it, with a docstring on every public name and examples of at least two kinds on every constructor.
7. **Check** the change with `just check` and `just test`, and record it in the changelog.

Scales stay exact throughout: a unit's scale is a `Fraction` (or an integer), and a related scale is derived from the scale it relates to, so the relationship is visible in the code.
