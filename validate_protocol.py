#!/usr/bin/env python3
"""
Opentrons Protocol Validator
This script validates Opentrons protocol files and checks for common issues.
"""

import sys
import ast
import importlib.util

def validate_protocol_file(file_path):
    """Validate an Opentrons protocol file."""
    print(f"\n{'='*60}")
    print(f"Validating protocol: {file_path}")
    print(f"{'='*60}\n")

    errors = []
    warnings = []

    # Read the file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ ERROR: Could not read file: {e}")
        return False

    # Check 1: Valid Python syntax
    print("✓ Checking Python syntax...")
    try:
        ast.parse(content)
        print("  ✓ Valid Python syntax")
    except SyntaxError as e:
        errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
        print(f"  ❌ Syntax error at line {e.lineno}: {e.msg}")

    # Check 2: Required imports
    print("\n✓ Checking required imports...")
    if 'from opentrons import protocol_api' in content or 'import opentrons' in content:
        print("  ✓ Opentrons imports found")
    else:
        warnings.append("No opentrons imports found - this may not be an Opentrons protocol")
        print("  ⚠ No opentrons imports found")

    # Check 3: Metadata
    print("\n✓ Checking metadata...")
    if 'metadata' in content:
        print("  ✓ Metadata defined")

        # Check for required metadata fields
        if 'apiLevel' in content or 'API_VERSION' in content:
            print("  ✓ API level specified")
        else:
            warnings.append("No apiLevel specified in metadata")
            print("  ⚠ No apiLevel specified")
    else:
        warnings.append("No metadata dictionary found")
        print("  ⚠ No metadata dictionary found")

    # Check 4: Run function
    print("\n✓ Checking run function...")
    if 'def run(' in content:
        print("  ✓ Run function defined")
    else:
        errors.append("No 'run' function found - required for protocol execution")
        print("  ❌ No 'run' function found")

    # Check 5: Common issues
    print("\n✓ Checking for common issues...")

    # Check for unmatched tips
    if 'pick_up_tip' in content:
        pick_ups = content.count('pick_up_tip')
        drop_tips = content.count('drop_tip')
        if pick_ups != drop_tips:
            warnings.append(f"Unmatched tip operations: {pick_ups} pick_up_tip vs {drop_tips} drop_tip")
            print(f"  ⚠ Unmatched tip operations: {pick_ups} pick_up vs {drop_tips} drop")
        else:
            print(f"  ✓ Tip operations balanced ({pick_ups} pick_up, {drop_tips} drop)")

    # Check for aspirate/dispense balance
    if 'aspirate' in content:
        aspirates = content.count('aspirate(')
        dispenses = content.count('dispense(')
        print(f"  ℹ Found {aspirates} aspirate and {dispenses} dispense operations")

    # Check for load_instrument
    if 'load_instrument' in content:
        print("  ✓ Instrument loading found")
    else:
        warnings.append("No instruments loaded")
        print("  ⚠ No instruments loaded")

    # Check for load_labware
    if 'load_labware' in content:
        print("  ✓ Labware loading found")
    else:
        warnings.append("No labware loaded")
        print("  ⚠ No labware loaded")

    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")

    if warnings:
        print(f"\n⚠ WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")

    if not errors and not warnings:
        print("\n✅ All checks passed! Protocol looks good.")
        return True
    elif not errors:
        print("\n✅ No errors found (only warnings).")
        return True
    else:
        print("\n❌ Validation failed with errors.")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_protocol.py <protocol_file.py>")
        sys.exit(1)

    protocol_file = sys.argv[1]
    success = validate_protocol_file(protocol_file)
    sys.exit(0 if success else 1)
