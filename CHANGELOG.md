# Changelog

All notable changes to splice-py will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0b1] - 2025-11-03

### Added
- Initial project structure
- `Harness` class for creating harness designs
- `ComponentType` enum for component kinds
- `add_component()` method with unified API
- Auto-designator generation (X1, W1, F1, CB1, PS1, etc.)
- Wire and CableCore helper classes
- Connection API with PinRef, CoreRef, FlyingLead support
- JSON export matching Splice import schema
- Direct API upload to Splice with `upload()` method
- Validation system
- Support for all component categories (connectors, cables, fuses, relays, etc.)
- Design notes support
- Custom positioning support
- Full type hints for IDE autocomplete
- PyPI package publication
