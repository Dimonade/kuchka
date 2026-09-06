# Changelog

All notable changes to kuchka are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
See the `Stability` section in `README.md` for what versioning means before `0.2.0`.

## Unreleased

- `Area` family.
- `MilePerHour` unit.
- `Modular` / `Cyclic` category for, for instance, angles.
- Adding additional magnitudes to units where it makes practical sense.
- `ConvertibleToTime` protocol/trait.
- `Instant`
- Migrate internal units definitions to use `Prefix`.

## [0.1.1]

### Added: `Prefix` constructor for internal unit creation.

Internally used registry that allows reusing the same names, magnitudes, symbols and names across all units.
Serves to avoid manual rolling, reduce typos, reduce visually hard to verify magnitude strings.

## [0.1.0] -- initial release

Base version.
