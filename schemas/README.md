# Reference JSON Schemas

This directory contains complete JSON schema examples exported from splice-py. These files demonstrate the full structure and format of harness data that can be imported into the Splice web application.

## Schema Files

### Power Distribution_schema.json
Industrial power distribution harness with:
- AC power input connector (X1)
- Power supply with custom pin names (PS1)
- Three circuit breakers with pin mappings (CB1, CB2, CB3)
- Output terminal blocks (X2, X3)
- 10 wire connections in AWG 14
- Demonstrates category-specific designators and pin mappings

### GNS430 NAV_schema.json
Aviation wiring harness for Garmin GNS430 NAV/COM radio with:
- 78-pin high-density connector (X1)
- 44-pin connector (X2)
- 25-pin D-SUB connector (X3)
- 9 signal connections with labels
- AWG 24 wires in multiple colors
- Demonstrates high pin-count connectors

### Power In_schema.json
Simple power input cable with:
- 4-pin power connector (X1)
- Flying lead terminations
- Red and black AWG 20 wires
- Demonstrates flying lead format

## Usage

These schemas serve as:

1. **Format reference** - See complete, real-world examples of the JSON structure
2. **Testing fixtures** - Use for validating import/export functionality
3. **Documentation** - Understand how complex harnesses are represented
4. **Templates** - Starting points for similar designs

## Related Documentation

- [JSON Schema Documentation](../docs/schema.md) - Detailed format specification
- [Examples Directory](../examples) - Python scripts that generate these schemas
- [Main README](../README.md) - Library documentation and usage

## Importing to Splice

To use these schemas in the Splice web application:

1. Visit [splice-cad.com](https://splice-cad.com)
2. Sign in or create an account
3. Click "Import" or drag and drop the JSON file
4. The harness will open in the visual editor

## Generating Updated Schemas

To regenerate these schemas from the Python examples:

```bash
cd examples
python3 power_distribution.py
python3 gns430_nav.py
python3 power_in.py

# Copy the generated JSON files to schemas directory
cp power_distribution.json ../schemas/"Power Distribution_schema.json"
cp gns430_nav.json ../schemas/"GNS430 NAV_schema.json"
cp power_in.json ../schemas/"Power In_schema.json"
```
