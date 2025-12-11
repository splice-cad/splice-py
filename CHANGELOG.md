# Changelog

All notable changes to splice-py will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-12-11

### Added
- `BundleLabel` class for heat-shrink label printing with styling options
- `LabelSettings` class for global label display configuration
- `Harness.add_label()` method for adding labels to connectors and cables
- `Harness.remove_label()` method for removing labels
- `Harness.get_labels()` method for retrieving labels with optional filtering
- Auto-designator label generation with `auto_designator=True`
- Label styling options: width_mm, font_size, text_color, background_color
- Cable label support with `cable_end` parameter (start/end/both)
- Wire-specific labels via `wire_keys` parameter
- Labels export in JSON format (`bundle_labels` and `label_settings`)
- Comprehensive test suite with 144 tests (86% code coverage)
- Test fixtures in `tests/conftest.py`

### Changed
- Moved from beta to stable release

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
