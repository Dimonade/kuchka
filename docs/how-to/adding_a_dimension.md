# Adding a dimension

A `Dimension` is a vector of exponents over the base quantities: time, length, mass, current, temperature, amount, luminous intensity, and angle.
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
- Static typing needs `@overload`s on the operand classes, as `Length.__mul__` declares `Area` for `Length`. A contract test compares the declared overloads with the runtime results.
- A dimension that two linear kinds both claim must say how they relate, which `docs/concepts/dimensional_algebra.md` describes.

## Checklist

- [ ] the constant in `dimensions.py` and in its `__all__`,
- [ ] a quantity type registered for it ([Adding a quantity](adding_a_quantity.md)),
- [ ] `@overload`s on the operand classes for the products and quotients it produces,
- [ ] [tests](adding_tests.md) for the new arithmetic.
