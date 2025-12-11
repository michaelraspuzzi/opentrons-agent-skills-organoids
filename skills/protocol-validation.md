---
name: protocol-validation
description: Validate Opentrons protocols before running on hardware. Performs static analysis to catch common errors like pipette-layout mismatches, volume issues, and API errors. Run protocols through simulator for complete validation.
---

# Protocol Validation

Validate Opentrons Flex protocols before running on hardware.

## Validation Layers

### Layer 1: Static Analysis (Quick)
Check code structure without execution:
- Python syntax validation
- Required imports present
- Metadata/requirements structure
- Run function defined

### Layer 2: Logic Analysis (Deep)
Analyze protocol logic:
- Pipette type matches well access pattern
- Volume calculations within capacity
- Tip usage calculations
- Source volume depletion tracking

### Layer 3: Simulator (Complete)
Run through official Opentrons simulator:
```bash
opentrons_simulate protocol.py
```

## Critical Checks

### 1. Pipette-Layout Compatibility

**The #1 most common error:**

```python
# Check if 8-channel is used with individual wells
if 'flex_8channel' in pipette_type:
    if '.wells_by_name()' in code:
        ERROR: "8-channel pipette with individual well access"
        FIX: "Use flex_1channel_1000 or redesign plate layout"
```

**Rule:** 8-channel pipettes dispense to ALL 8 rows simultaneously.
- `plate['A1']` with 8-channel → affects A1, B1, C1, D1, E1, F1, G1, H1

### 2. Flex-Specific Requirements

```python
# Must have requirements dict (not just metadata)
if 'requirements' not in protocol:
    ERROR: "Missing requirements dict for Flex"

# Must have robotType
if 'robotType' not in requirements:
    ERROR: "Missing robotType in requirements"

# apiLevel should be in requirements only
if 'apiLevel' in metadata AND 'apiLevel' in requirements:
    ERROR: "Duplicate apiLevel - put in requirements only"

# Must have trash bin
if 'load_trash_bin' not in code:
    ERROR: "Missing trash bin - required for Flex"
```

### 3. Volume Validation

```python
# Single aspirate within capacity
if aspirate_volume > pipette_max:
    ERROR: f"Aspirate {aspirate_volume} µL exceeds capacity"

# Cumulative volume in tip
cumulative = sum(aspirates_before_drop)
if cumulative > pipette_max:
    ERROR: f"Cumulative {cumulative} µL exceeds capacity"
```

### 4. Tip Usage

```python
tips_needed = count_pick_up_tip()
tips_available = tip_racks * 96

if tips_needed > tips_available:
    ERROR: f"Need {tips_needed} tips, only {tips_available} available"
```

## Error Messages and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `NoTrashDefinedError` | Missing trash bin | Add `protocol.load_trash_bin('A3')` |
| `MalformedPythonProtocolError: apiLevel in both` | Duplicate apiLevel | Remove from metadata, keep in requirements |
| 8-channel wrong wells | Individual well access | Use single-channel pipette |
| Volume exceeds capacity | Too much in tip | Aspirate less or change pipette |

## Validation Workflow

```
1. Read protocol file
         ↓
2. Static analysis (syntax, structure)
         ↓
3. Logic analysis (pipette, volumes, tips)
         ↓
4. Run simulator: opentrons_simulate protocol.py
         ↓
5. Review simulator output for errors/warnings
         ↓
6. ✅ Pass → Ready for hardware
   ❌ Fail → Fix and re-validate
```

## Using the Simulator

### Setup (One-time)
```bash
# Requires Python 3.10+
python3.10 -m venv venv-opentrons
source venv-opentrons/bin/activate
pip install opentrons
```

### Run Simulation
```bash
source venv-opentrons/bin/activate
opentrons_simulate your_protocol.py
```

### Interpret Output

**Success:**
```
Picking up tip from A1 of Opentrons Flex 96 Tip Rack...
Aspirating 100.0 uL from A1 of NEST 12 Well Reservoir...
Dispensing 100.0 uL into A1 of Corning 96 Well Plate...
```

**Error:**
```
NoTrashDefinedError: No trash container has been defined
MalformedPythonProtocolError: apiLevel in both dicts
```

## Automated Validation Script

```python
#!/usr/bin/env python3
"""Quick protocol validator for common issues."""

import sys
import ast

def validate(filepath):
    with open(filepath) as f:
        code = f.read()

    errors = []

    # Check 1: 8-channel with wells_by_name
    if 'flex_8channel' in code and '.wells_by_name()' in code:
        errors.append("8-channel pipette with individual well access")

    # Check 2: Missing trash bin
    if 'load_trash_bin' not in code and 'Flex' in code:
        errors.append("Missing trash bin for Flex protocol")

    # Check 3: Duplicate apiLevel
    if code.count("'apiLevel'") > 1:
        errors.append("apiLevel appears multiple times")

    return errors

if __name__ == '__main__':
    errors = validate(sys.argv[1])
    for e in errors:
        print(f"❌ {e}")
    if not errors:
        print("✅ Basic checks passed - run simulator for full validation")
```

## Best Practices

1. **Always run simulator** before hardware
2. **Check pipette-layout match** first - most common error
3. **Verify Flex requirements** (trash bin, requirements dict)
4. **Review full simulator output** - don't just check for errors
5. **Test with actual volumes** - simulator catches capacity issues
