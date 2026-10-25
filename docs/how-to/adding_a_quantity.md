# Adding a quantity

A quantity type is a class that values are built from, such as `Length` or `Voltage`.
It owns one dimension, shares one implementation of arithmetic, conversion, and comparison with every other type, and differs from its neighbours in its dimension and its operator overloads.

## The class

The krakenpeople's absement is a linear quantity of the dimension [Adding a dimension](adding_a_dimension.md) introduced:

<!-- doc-test: skip an illustration of a module that does not exist in the library -->

```python
class Absement(LinearQuantity):
    """How far, and for how long, something is held away from where it started."""

    dimension: ClassVar[Dimension] = ABSEMENT
    __slots__ = ()

    # ... @overloads for Absement / Time -> Length and Absement / Length -> Time ...


_register(ABSEMENT, Absement)
```

The shape decides the base class: `LinearQuantity` for most, and the affine, modular, and logarithmic shapes of `docs/concepts/quantity_shapes.md` for temperatures, angles, and decibels.
A concrete type must declare `__slots__` and a `Dimension`, and it registers itself once, at import, because the registry closes when `kuchka` finishes importing.
That makes a quantity a change to the library's source.

## Principal, specialisation, contested

A dimension can have several kinds, and registration says how a new one relates to those already there:

| Relation       | Meaning                                                           | Declared by                              |
| -------------- | ----------------------------------------------------------------- | ---------------------------------------- |
| principal      | the linear kind arithmetic returns for the dimension              | the first registration, with no relation |
| specialisation | a role of an existing kind of the same dimension and shape        | `specialisation_of=` the principal kind  |
| contested      | linear kinds on equal footing, so arithmetic cannot pick a result | `contested_with=` the other kind         |

`Absement` is the first linear kind of its dimension, so it is the principal.
The krakenpeople also speak of **depth**, a length measured downward from the surface.
It has the dimension of length and no arithmetic of its own, so it is a specialisation:

<!-- doc-test: skip an illustration of a module that does not exist in the library -->

```python
_register(LENGTH, Depth, specialisation_of=Length)
```

A specialisation records meaning and shape and converts no value.
Moving between it and its principal kind is explicit, with named conversions in the `to_x` and `from_x` style (`Time.to_sampling_period()`, `SamplingPeriod.to_time()`).
`SampleRate`, `BaudRate`, and `Activity` are specialisations of `Frequency`, `ApparentPower` and `ReactivePower` of `Power`, and `Stress` of `Pressure`.
A role takes part in arithmetic only when it is scaled by a dimensionless value, divided by itself, or multiplied by its reciprocal.
Every other product goes through the conversion first, so `Stress * Area` is refused with a hint and `stress.to_pressure() * area` is a `Force`.
A `_rule` names a result for the kinds that arithmetic reaches, which a role is not, so a role takes no rule.
A real contested pair is `Pressure` and `EnergyDensity`: neither is principal, and a result in that dimension raises `AmbiguousKindError` naming the candidates.
A second linear kind that states no relation is refused when the module is imported.

## Units

A type needs units before it can display anything:

1. a module in `kuchka.units`, in the package [its dimension belongs to](adding_a_unit.md#where-the-module-goes), with the unit definitions, a `*_UNITS` table, and an `__all__`,
2. the canonical unit, with scale 1, set in that module as `Absement._canonical_unit = METRE_SECOND`,
3. an entry in the `_UNITS_OF` block of `kuchka/units/__init__.py`, which binds the table to the type.

A type shares units with another type of its dimension only where a table says so, as `Time` and `SamplingPeriod` share the second.
[Adding a unit](adding_a_unit.md) describes the module.

## Exports

A type lives in the package of the relation that defines it, the same placement as its units ([where the module goes](adding_a_unit.md#where-the-module-goes)), with one module per type.
Types share a module only when they construct one another when the code runs, as the time types do, and as `Pressure` and `Stress` do through `to_stress()`.
A module imports, when it is imported, only from the top level and from the packages before its own, and a test fails when one does not.
An overload may name a type of any package, because a type checker reads it and nothing runs it.

A new leaf module is exported the way its neighbours are, following the comment above `__all__` in `kuchka/units/__init__.py`.
Then run `just generate-api`, which promotes the constructors and the type to the top level.

## Checklist

- [ ] the dimension ([Adding a dimension](adding_a_dimension.md)),
- [ ] the class, with `__slots__`, a docstring, and `@overload`s,
- [ ] `_register(...)`, stating a relation when another linear kind exists,
- [ ] a unit module with a canonical unit and a table, and its `_UNITS_OF` entry,
- [ ] the three export lines and `just generate-api`,
- [ ] [tests](adding_tests.md), including the shared-dimension list when a dimension gains a second kind,
- [ ] a changelog line.
