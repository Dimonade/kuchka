# Adding a dimension

A `Dimension` is a vector of exponents over the base quantities: time, length, mass, current, temperature, amount, luminous intensity, angle, solid angle, and information.
Two dimensions are equal when every exponent matches, and the arithmetic engine reads products and quotients straight off the exponents.

## Do you need one?

Most work needs no new dimension.
A product or quotient already has a dimension by exponent arithmetic, and a dimension with no registered type is reported as an `UnrepresentableDimensionError` when an operation lands on it.
Add a dimension when a quantity of that dimension deserves a type of its own.

The krakenpeople track **absement**: how far, and for how long, a thing is held away from where it started.
Two shells of displacement held for three bubbles make six shell-bubbles.
Absement is length times time, and the library does not register it today, so `Length * Time` raises until a type exists.
The page uses it as an illustration.

## Add the dimension

Dimensions live in `kuchka/dimensions.py`:

<!-- doc-test: skip a fragment of the dimensions module, not a program -->

```python
ABSEMENT = Dimension(length=1, time=1)
```

Include the name in the module's sorted `__all__`.
Use a name for what the dimension is, and give it a constant even when no type exists yet, so the type that arrives later has a place to point.

## Give it a quantity

A dimension on its own does nothing until a quantity type registers it.
[Adding a quantity](adding_a_quantity.md) covers the class, its registration, and its units.
Once `Absement` is registered as the first linear kind of `ABSEMENT`, it is the principal kind: arithmetic that produces that dimension returns it.

## What arithmetic needs

- The result registry is built from registrations, so `Length * Time` resolves to `Absement` and `Absement / Time` to `Length` once the type exists.
- Static typing needs `@overload`s on the operand classes, as `Length.__mul__` declares `Area` for `Length`. `just generate-overloads` writes them from the registry, `just check` fails when they are out of date, and a contract test compares them with the runtime results.
- A dimension that two linear kinds both claim must say how they relate, which `docs/concepts/dimensional_algebra.md` describes.

## Checklist

- [ ] the constant in `dimensions.py` and in its `__all__`,
- [ ] a quantity type registered for it ([Adding a quantity](adding_a_quantity.md)),
- [ ] `just generate-overloads`, for the products and quotients it produces,
- [ ] [tests](adding_tests.md) for the new arithmetic.

## Adding an axis

An axis is rarer than a dimension.
Add one when SI's own accounting folds two concepts into one dimension and a model needs to tell them apart: angle separates torque from energy, solid angle separates the lumen from the candela, and information separates a count of bits from a plain number and a data rate from a frequency.
An axis takes four edits in `kuchka/dimensions.py` and one in `kuchka/internal/symbols.py`:

<!-- doc-test: skip a fragment of the dimensions module, not a program -->

```python
class Dimension:
    ...
    # A field with a default of 0 leaves every existing dimension unchanged.
    information: int = 0

    def __mul__(self, other):
        ...
        information = self.information + other.information

    def __truediv__(self, other):
        ...
        information = self.information - other.information
```

- `__repr__` lists the axis with a label from `kuchka/internal/symbols.py`, so `DATA_RATE` shows as `T⁻¹ D¹`.
- The exponent-formatting test in `tests/behaviour/test_format.py` gives the new field an exponent, so the label and the superscripts are checked together.
- The dimension constants that use the axis (`DATA = Dimension(information=1)`) follow as described above.

Nothing else reads the fields one by one: equality, hashing, and the result registry compare whole dimensions.
