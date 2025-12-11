# Opentrons Protocol Generation Skill

## Overview

This skill generates executable Python protocols for the Opentrons Flex liquid handling robot. It transforms experimental designs from hypothesis generation into ready-to-run code with complete plate layouts, reagent calculations, and safety validations.

## Skill Structure

```
opentrons-protocol-gen/
├── skill.md                            # Main skill definition with frontmatter
├── README.md                           # This file
└── references/
    ├── flex-specifications.md          # Deck layout, pipettes, modules
    ├── protocol-templates.md           # Code blocks for common operations
    ├── labware-reference.md            # Plate types, reservoirs, tip racks
    ├── liquid-handling-tips.md         # Best practices, error prevention
    └── example-protocols.md            # Complete working examples
```

## Installation

1. Download the entire `opentrons-protocol-gen` folder
2. Zip the folder: `zip -r opentrons-protocol-gen.zip opentrons-protocol-gen/`
3. Upload to Claude as a skill

## Usage

The skill activates when you:

- Provide structured experimental design JSON from hypothesis-gen skill
- Request a protocol: "Generate Opentrons protocol for dose-response"
- Describe experiment: "Set up 8 concentrations of drug X, N=4"
- Ask for plate layout: "Design a plate for 3 treatments with controls"

## Key Features

### 1. CRITICAL: Pipette Selection Logic

**The #1 source of errors is choosing the wrong pipette.**

The skill automatically analyzes your plate layout and selects:
- **Single-channel**: For scattered individual wells or row-specific treatments
- **8-channel**: Only when ALL 8 rows (A-H) in each column get the SAME treatment
- **96-channel**: Only when ALL 96 wells get the SAME treatment

**When in doubt, the skill defaults to single-channel (slower but always correct).**

### 2. Volume Capacity Validation

Before generating any pipetting operation, validates:
- Each aspirate ≤ pipette max capacity (1000 µL or 50 µL)
- Cumulative volume doesn't overflow (no repeated aspirates without dispensing)
- Source volumes sufficient (includes dead volume + overage)

### 3. Comprehensive Output Package

For every protocol, generates:
1. **Python protocol file** (.py) - Executable on Opentrons Flex
2. **Plate map** (markdown table) - Visual layout of treatments
3. **Reagent prep guide** - Stock solutions, dilutions, volumes needed
4. **Estimated runtime** - Protocol duration estimate

### 4. Safety Defaults

All protocols include:
- Slower aspiration/dispense rates for safety
- Touch tip after dispenses (removes exterior droplets)
- Blow out after dispenses (ensures complete delivery)
- Comments explaining each major step
- Pause points for user verification

## Input Formats

### From Hypothesis-Gen Skill

```json
{
  "selected_hypothesis": {
    "id": "hyp_1",
    "statement": "TNF-α disrupts calcium handling in cardiac organoids",
    "experiment_type": "dose_response"
  },
  "experimental_design": {
    "groups": [
      {"name": "vehicle", "treatment": "media only", "n": 12},
      {"name": "TNF_10", "treatment": "TNF-α 10 ng/mL", "n": 12}
    ],
    "plate_format": "96-well",
    "timeline_hours": 24,
    "readouts": [...]
  },
  "reagents_needed": [...],
  "controls": {...}
}
```

### Natural Language

```
User: "Create a protocol for 8-point dose-response of doxorubicin,
       N=4 per concentration, with vehicle and positive controls"

Skill:
1. Designs plate layout (8 concentrations + controls)
2. Selects appropriate pipette (analyzes if 8-channel compatible)
3. Generates serial dilution code
4. Calculates reagent volumes (with overage + dead volume)
5. Creates complete protocol + plate map + reagent guide
```

## Quality Checklist

Every protocol is validated against:

### Hardware Validation
- ✅ API level 2.16 with robotType: 'Flex'
- ✅ Valid Flex labware (not OT-2 labware)
- ✅ No deck slot conflicts

### Pipette Selection (MOST CRITICAL)
- ✅ Analyzed plate layout for well access pattern
- ✅ If different rows in same column get different treatments → single-channel
- ✅ If all 8 rows in column get same treatment → 8-channel OK
- ✅ If all 96 wells get same treatment → 96-channel OK

### Volume Validation
- ✅ Each aspirate ≤ pipette max (1000 µL or 50 µL)
- ✅ No cumulative overflow (multiple aspirates before dispense)
- ✅ Minimum volumes respected (≥5 µL for 1000 µL pipette, ≥1 µL for 50 µL)
- ✅ Correct pipette for volume range

### Source Volume Tracking
- ✅ Total volume = (transfer volume × transfers × 1.2 overage) + dead volume
- ✅ Dead volumes: 12-column reservoir (~2 mL/well), single trough (~10-15 mL)
- ✅ Source won't run dry mid-protocol

### Tip Management
- ✅ Tip count sufficient (count all pick_up_tip() calls)
- ✅ New tips when switching reagents
- ✅ Tip racks in sequential deck positions

### Documentation
- ✅ Comments explain each step
- ✅ Reagent guide matches protocol volumes exactly
- ✅ Plate map matches code exactly
- ✅ Pause points where user intervention needed

## Reference Materials

### flex-specifications.md
**Load first** for protocol generation. Contains:
- Deck layout (A1-D4 grid, staging slots)
- Pipette specs (96-channel, 8-channel, single-channel)
- Module specifications (heater-shaker, temperature, magnetic, thermocycler)
- Tip racks and flow rates

### protocol-templates.md
8 common operation templates:
1. **Serial dilution** (8-channel, column-based)
2. **Individual well treatment** (single-channel, scattered wells)
3. **Full plate addition** (96-channel)
4. **Row-specific treatment** (single-channel, NOT 8-channel)
5. **Plate-to-plate transfer** (96-channel)
6. **Module usage** (heater-shaker example)
7. **Distribute** (one-to-many)
8. **Consolidate** (many-to-one)

### labware-reference.md
Complete catalog:
- 96-well plates (cell culture, PCR, specialty)
- 24-well and 6-well plates
- Reservoirs (12-column, single trough)
- Tip racks (Flex-specific)
- Tube racks (1.5 mL, 2 mL, 15 mL, 50 mL)
- Module-compatible labware

### liquid-handling-tips.md
Best practices:
- Pipette selection decision rules
- Volume capacity limits
- Aspiration/dispense techniques
- Mixing strategies
- Troubleshooting common issues

### example-protocols.md
Complete working protocols:
- 8-point dose-response with CellTiter-Glo
- Simple drug addition (96-channel)
- 3× plate wash
- Time-course treatment

## Example Workflow

```
1. User completes hypothesis-gen → selects "TNF-α inflammatory challenge"

2. hypothesis-gen outputs JSON:
   {
     "experimental_design": {
       "groups": [
         {"name": "vehicle", "n": 12},
         {"name": "TNF_10", "n": 12},
         {"name": "TNF_50", "n": 12}
       ]
     }
   }

3. User: "Generate Opentrons protocol for this experiment"

4. opentrons-protocol-gen skill:
   - Loads flex-specifications.md
   - Analyzes plate layout:
     * Columns 1-4: vehicle (12 wells)
     * Columns 5-8: TNF 10 ng/mL (12 wells)
     * Columns 9-12: TNF 50 ng/mL (12 wells)
   - Pipette check: Different columns, but within columns...
     * Rows A-B get same treatment (vehicle in cols 1-4)
     * All 8 rows DON'T get same treatment (only A-B filled)
     * Decision: Use SINGLE-CHANNEL (rows A-B only, not full columns)
   - Calculates volumes:
     * 100 µL/well × 36 wells × 1.2 overage = 4,320 µL + 2 mL dead = 6.3 mL
   - Generates protocol with single-channel pipette
   - Creates plate map + reagent guide

5. Output:
   - cardiac_inflammatory_challenge.py (executable protocol)
   - Plate map showing vehicle/TNF-10/TNF-50 layout
   - Reagent prep: "Load 6.3 mL vehicle in reservoir A1"
```

## Common Pitfalls (Automatically Avoided)

### ❌ Wrong Pipette Selection
```python
# ERROR: Using 8-channel for rows A-B only
p8.dispense(100, plate['A1'])  # Would hit A1-H1, but we only want A1-B1!
```
✅ **Skill detects this and uses single-channel instead**

### ❌ Volume Overflow
```python
# ERROR: 4 × 171 µL = 684 µL in 200 µL pipette
p200.aspirate(171, media)  # Repeated 4 times = overflow!
```
✅ **Skill validates before generating: 171 µL × 4 > 200 µL max → uses p1000 instead**

### ❌ Insufficient Source Volume
```python
# ERROR: Need 10 mL but only loaded 8 mL
```
✅ **Skill calculates: (100 µL × 96 × 1.2) + 2 mL dead = 13.5 mL → warns user**

### ❌ Wrong API Version
```python
# ERROR: Using OT-2 API for Flex robot
metadata = {'apiLevel': '2.13'}  # Too old!
```
✅ **Skill always generates: apiLevel: '2.16', robotType: 'Flex'**

## Integration with Other Skills

### Upstream (receives from):
- **hypothesis-gen**: Experimental design as JSON input

### Downstream (sends to):
- None (produces executable files for Opentrons Flex)

## Tips for Best Results

1. **Trust the pipette selection**: The skill analyzes your layout carefully
2. **Verify plate map**: Always check the visual plate map matches your intent
3. **Check reagent volumes**: Skill adds 20% overage + dead volume automatically
4. **Simulate before running**: Use Opentrons app to simulate protocol first
5. **Have backup tips**: Skill calculates exact count, but have extras on hand

## Version

- **Version**: 1.0
- **Last Updated**: 2025-12-11
- **Compatible with**: Opentrons Flex, API 2.16
- **Maintained by**: Cardiac Organoid Research Community

## License

Open for research and educational use.
