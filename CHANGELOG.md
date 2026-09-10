# Changelog

All notable changes to kuchka are documented here.

The format tries to follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
See the `Stability` section in `README.md` for what versioning means before `0.2.0`.

## [0.1.2] - Unreleased, available on `develop`

### Added

#### Area and Volume families

- `SquareMillimetre`/`SquareCentimetre`/`SquareMetre`/`SquareKilometre`, plus `Hectare`, `Acre`, and `SquareInch`.
  `Length * Length -> Area` and `Area / Length -> Length`.
- `CubicMillimetre`/`CubicCentimetre`/`CubicMetre`, plus `Litre` and its own `Microlitre`/`Millilitre`/`Kilolitre` prefixes.
  `Area * Length -> Volume`, `Length * Area -> Volume`, and both inverses (`Volume / Length -> Area`, `Volume / Area -> Length`).

#### New Temporals

- `Minute` and `Hour` for `Time`.

#### New Charge units

- `MilliampereSecond`, `MilliampereHour`, and `AmpereHour`.

#### New Energy units

- `WattHour` and `MilliwattHour`.

## [0.1.1] - 2026-09-9

### Added

#### `Prefix` constructor for internal unit creation.

Internally used registry that allows reusing the same names, magnitudes, symbols and names across all units.
Serves to avoid manual rolling, reduce typos, reduce visually hard to verify magnitude strings.
Migrate most (aspiring to all) units to the registry.
Some compound units (m/s, kS/s, etc.) require additional review with regard to this change.

### Fixed

#### `Kelvin`, `Celsius`, `TemperatureDelta`, `KELVIN`, `CELSIUS` split and exposed

These objects were clumped together in `quantities/thermal.py`.
Now they are split correctly and exposed as first class API.

#### Coherent `__init__` and `__all__` definitions

Properly exposed API of all units, quantities, utility methods and definitions.

## [0.1.0] -- initial release

Base version.
