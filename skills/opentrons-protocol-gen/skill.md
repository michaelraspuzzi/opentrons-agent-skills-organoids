---
name: opentrons-protocol-gen
description: Generate executable Python protocols for Opentrons Flex liquid handling robot. Takes experimental designs from hypothesis generation workflow and produces ready-to-run code with plate layouts, reagent calculations, and safety checks. Supports drug treatments, serial dilutions, plate washing, and assay additions. Outputs include Python protocol files, plate map visualizations, and reagent preparation guides.
---

# Opentrons Protocol Generation

Transform experimental designs into executable Opentrons Flex Python protocols.

## Input Modes

### Mode 1: Structured Input (from hypothesis skill)
Accepts JSON with experimental design:

```json
{
  "selected_hypothesis": {
    "id": "hyp_1",
    "statement": "...",
    "experiment_type": "dose_response|time_course|comparison|combination"
  },
  "experimental_design": {
    "groups": [...],
    "plate_format": "96-well",
    "timeline_hours": 24,
    "readouts": [...]
  },
  "reagents_needed": [...],
  "controls": {...}
}
```

### Mode 2: Natural Language
User describes experiment directly:
- "Set up a dose-response with 8 concentrations of doxorubicin, N=4"
- "Serial dilution from 100 µM to 0.1 µM, half-log steps"
- "Treat plate, wait 24h, add CellTiter-Glo"

### Mode 3: Plate Layout First
User provides or requests plate layout, then generates protocol to execute it.

---

## Protocol Generation Workflow

### Step 1: Load Specifications
**Always load** [references/flex-specifications.md](references/flex-specifications.md) first.
- Deck positions and constraints
- Pipette capabilities
- Module specifications

### Step 2: Parse Experimental Design
Extract:
- Number of groups/conditions
- Replicates per group
- Plate format (96-well, 24-well, etc.)
- Volumes needed
- Timing requirements

### Step 2.5: Select Appropriate Pipette (CRITICAL)

**THIS IS THE MOST COMMON SOURCE OF ERRORS. READ CAREFULLY.**

Analyze the plate layout to determine which pipette to use:

#### Single-Channel (`flex_1channel_1000` or `flex_1channel_50`)

**Use when:**
- Treating individual wells scattered across plate
- Different treatments to different rows within same column
- Wells don't follow column or row patterns
- Example targets: A1, A2, A3, B1, B5, B9 (not full columns)

**Code pattern:**
```python
p1000 = protocol.load_instrument('flex_1channel_1000', 'right', tip_racks=[tips])

# Correct: targeting individual wells
for well in ['A1', 'A2', 'B5', 'C3']:
    p1000.pick_up_tip()
    p1000.aspirate(100, reagent)
    p1000.dispense(100, plate.wells_by_name()[well])
    p1000.drop_tip()
```

#### 8-Channel (`flex_8channel_1000` or `flex_8channel_50`)

**Use when:**
- Treating ENTIRE COLUMNS at once
- All 8 wells in column (A-H) get SAME treatment
- Column-based operations (serial dilution across columns)

**⚠️ CRITICAL WARNING:**
8-channel pipette ALWAYS operates on all 8 rows (A-H) simultaneously!

When you target `plate.columns()[0][0]` or `plate['A1']` with 8-channel:
- It dispenses to A1, B1, C1, D1, E1, F1, G1, H1 (ENTIRE column 1)
- NOT just A1!

**Code pattern:**
```python
p8_1000 = protocol.load_instrument('flex_8channel_1000', 'right', tip_racks=[tips])

# Correct: treating full columns
for col_idx in range(12):
    p8_1000.pick_up_tip()
    p8_1000.aspirate(100, reagent)
    p8_1000.dispense(100, plate.columns()[col_idx][0])  # Hits A-H in column
    p8_1000.drop_tip()
```

**❌ WRONG - Common Error:**
```python
# BAD: Using 8-channel to target specific wells
# This will NOT work as intended!
p8_1000.dispense(100, plate['A1'])  # Actually dispenses to A1,B1,C1,D1,E1,F1,G1,H1!
p8_1000.dispense(100, plate['A2'])  # Actually dispenses to A2,B2,C2,D2,E2,F2,G2,H2!
```

#### 96-Channel (`flex_96channel_1000` or `flex_96channel_50`)

**Use when:**
- Entire plate operations
- All 96 wells get same treatment
- Plate-to-plate stamping/replicating

**Code pattern:**
```python
p96 = protocol.load_instrument('flex_96channel_1000', 'left', tip_racks=[tips])

# Hits all 96 wells at once
p96.pick_up_tip()
p96.aspirate(100, reservoir['A1'])
p96.dispense(100, plate['A1'])  # All 96 wells!
p96.drop_tip()
```

#### Decision Rule

| Your well targets | Correct pipette |
|-------------------|-----------------|
| Scattered individual wells (A1, B3, C5...) | **Single-channel** |
| Specific rows within columns | **Single-channel** |
| Full columns (A1-H1, A2-H2...) | **8-channel** |
| Full plate (all 96 wells same treatment) | **96-channel** |

**If in doubt, use single-channel. It's slower but always correct.**

### Step 3: Design Plate Layout
Create visual plate map showing:
- Which wells get which treatment
- Control positions
- Empty wells (if any)

**Layout principles**:
- Controls on edges or distributed
- If using 8-channel: group replicates in columns (all A-H get same)
- If using single-channel: any layout works
- Leave column 1 or 12 for serial dilution source

### Step 4: Calculate Reagents + Validate Volumes (CRITICAL)

For each reagent:
- Total volume needed (wells × volume × 1.2 overage)
- Stock concentration required
- Dilution calculations

**Volume Capacity Validation:**

Before ANY pipetting operation, check:

```
Single aspirate volume ≤ Pipette max capacity
Cumulative volume (if multiple aspirates before dispense) ≤ Pipette max capacity
```

| Pipette | Min Volume | Max Volume |
|---------|------------|------------|
| flex_1channel_1000 | 5 µL | 1000 µL |
| flex_1channel_50 | 1 µL | 50 µL |
| flex_8channel_1000 | 5 µL | 1000 µL |
| flex_8channel_50 | 1 µL | 50 µL |
| flex_96channel_1000 | 5 µL | 1000 µL |
| flex_96channel_50 | 1 µL | 50 µL |

**❌ COMMON ERROR - Cumulative Volume Overflow:**
```python
# BAD: Aspirating multiple times exceeds capacity!
p200.pick_up_tip()
for i in range(4):
    p200.aspirate(171, media)  # 171 × 4 = 684 µL > 200 µL capacity!
    p200.dispense(171, plate[i])
p200.drop_tip()
```

**✅ CORRECT - Pick up tip for each transfer:**
```python
# GOOD: Each transfer gets fresh tip
for i in range(4):
    p1000.pick_up_tip()
    p1000.aspirate(171, media)
    p1000.dispense(171, plate[i])
    p1000.drop_tip()
```

**✅ BETTER - Use distribute() method:**
```python
# BEST: Let Opentrons handle multi-dispense
p1000.distribute(171, media, [plate.wells()[i] for i in range(4)])
```

### Step 5: Plan Deck Layout
Assign deck positions:
- Tip racks (plan for enough tips!)
- Reagent reservoirs
- Source plates (dilutions)
- Destination plates (cells)
- Modules (heater-shaker, temp module)

### Step 6: Generate Protocol Code

Use templates from [references/protocol-templates.md](references/protocol-templates.md):
- Metadata and requirements
- Labware loading
- Liquid handling steps
- Comments for each operation

**Before writing each pipetting operation, validate:**

1. ✅ Pipette type matches well access pattern
2. ✅ Volume ≤ pipette capacity
3. ✅ Source has enough volume
4. ✅ Correct well addressing for pipette type

### Step 7: Add Safety Checks
Include:
- Volume limit checks
- Tip tracking
- Aspiration height checks
- Pause points for user verification

### Step 8: Output Package
Generate:
1. Python protocol file (.py)
2. Plate map (markdown table or CSV)
3. Reagent preparation guide
4. Estimated runtime

---

## Output Formats

### Protocol File Structure

```python
from opentrons import protocol_api

metadata = {
    'protocolName': '[Experiment Name]',
    'author': 'Generated by Claude',
    'description': '[Brief description]',
}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.16'
}

def run(protocol: protocol_api.ProtocolContext):
    # === LABWARE SETUP ===
    # Tips
    # Plates
    # Reservoirs
    # Modules

    # === PIPETTE SETUP ===
    # CRITICAL: Choose pipette based on well access pattern!
    # Single-channel for scattered wells
    # 8-channel for full columns only
    # 96-channel for full plate only

    # === REAGENT LOCATIONS ===

    # === PROTOCOL STEPS ===
    # Step 1: [Description]
    # Step 2: [Description]
    # ...
```

### Plate Map Format

```markdown
## Plate Layout: [Plate Name]

|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|----|----|-----|
| A | C | C | C | T1 | T1 | T1 | T2 | T2 | T2 | T3 | T3 | T3 |
| B | C | C | C | T1 | T1 | T1 | T2 | T2 | T2 | T3 | T3 | T3 |
...

Legend:
- C = Vehicle Control
- T1 = Treatment 1 (10 µM)
- T2 = Treatment 2 (30 µM)
...

⚠️ PIPETTE CHECK:
- If all rows (A-H) in each column get SAME treatment → 8-channel OK
- If different rows get different treatments → USE SINGLE-CHANNEL
```

### Reagent Preparation Guide

```markdown
## Reagent Preparation

### Stock Solutions
| Reagent | Stock Conc | Volume Needed | Storage |
|---------|------------|---------------|---------|
| Drug X | 10 mM | 500 µL | -20°C |

### Working Solutions
| Solution | Final Conc | Recipe |
|----------|------------|--------|
| Drug X 100 µM | 100 µM | 10 µL stock + 990 µL media |

### Reservoir Layout
| Position | Contents | Volume to Load | Calculation |
|----------|----------|----------------|-------------|
| A1-A4 | Media | 20 mL | 96 wells × 150 µL × 1.2 + 2 mL dead |
| A5-A6 | Drug X 100 µM | 5 mL | 32 wells × 100 µL × 1.2 + 1 mL dead |
```

---

## Quality Checklist (CRITICAL - DO NOT SKIP)

Before finalizing protocol:

### Hardware Validation
- [ ] API level is 2.16 with `robotType: 'Flex'`
- [ ] All labware definitions are valid Flex labware (not OT-2)
- [ ] Deck layout has no slot conflicts

### Pipette Selection Validation (MOST IMPORTANT)
- [ ] **Analyzed plate layout for well access pattern**
- [ ] **Pipette type matches pattern:**
  - Scattered individual wells → single-channel
  - Full columns (all A-H same) → 8-channel OK
  - Full plate (all 96 same) → 96-channel OK
- [ ] **If using 8-channel:** Verified ALL 8 wells in each target column receive SAME treatment
- [ ] **If using 96-channel:** Verified ALL 96 wells receive SAME treatment
- [ ] **When in doubt:** Used single-channel (slower but always correct)

### Volume Validation (CRITICAL)
- [ ] **Each single aspirate ≤ pipette max capacity**
  - 1000 µL pipette: 5-1000 µL per aspirate
  - 50 µL pipette: 1-50 µL per aspirate
- [ ] **No cumulative overflow:** If aspirating N times before dispensing, total ≤ max
- [ ] **Minimum volume respected:** No aspirations < 5 µL (1000 µL) or < 1 µL (50 µL)
- [ ] **Using correct pipette for volume:** Don't use 50 µL pipette for 200 µL transfers

### Source Volume Tracking
- [ ] **Reservoir volumes calculated:**
  - Total = (volume per transfer × number of transfers × 1.2 overage) + dead volume
- [ ] **Dead volumes accounted for:**
  - 12-column reservoir: ~2 mL per well
  - Single trough: ~10-15 mL
  - Deep well plate: ~100 µL per well
- [ ] **Source won't run dry mid-protocol**

### Tip Management
- [ ] Tip count sufficient: Count all `pick_up_tip()` calls
- [ ] New tip used when switching between different reagents
- [ ] Tip racks positioned for sequential access

### Liquid Handling
- [ ] Aspiration heights safe (z=1-2mm above bottom for cells)
- [ ] Mix steps included after additions
- [ ] Blow out after dispense for complete delivery
- [ ] Touch tip for viscous liquids

### Documentation
- [ ] Comments explain each major step
- [ ] Reagent guide matches protocol volumes exactly
- [ ] Plate map matches code exactly
- [ ] Pause points where user intervention needed

---

## Common Pitfalls

### Pipette Selection Errors (MOST COMMON)

**8-channel with scattered wells:**
```python
# ❌ WRONG: Trying to hit individual wells with 8-channel
p8.dispense(100, plate['A1'])  # Actually hits A1,B1,C1,D1,E1,F1,G1,H1!
p8.dispense(100, plate['A2'])  # Actually hits A2,B2,C2,D2,E2,F2,G2,H2!

# ✅ CORRECT: Use single-channel for individual wells
p1.dispense(100, plate['A1'])  # Hits only A1
p1.dispense(100, plate['A2'])  # Hits only A2
```

**Different treatments to different rows:**
```python
# ❌ WRONG: Using 8-channel when rows A-D get treatment 1, rows E-H get treatment 2
# 8-channel cannot do this! It always hits all 8 rows!

# ✅ CORRECT: Use single-channel
for row in ['A', 'B', 'C', 'D']:
    p1.transfer(100, treatment_1, plate[f'{row}1'])
for row in ['E', 'F', 'G', 'H']:
    p1.transfer(100, treatment_2, plate[f'{row}1'])
```

### Volume Capacity Errors (CRITICAL)

**Cumulative aspirate exceeds capacity:**
```python
# ❌ WRONG: 4 × 171 µL = 684 µL in a 200 µL pipette
p200.pick_up_tip()
for i in range(4):
    p200.aspirate(171, media)
    p200.dispense(171, plate[i])
p200.drop_tip()

# ✅ CORRECT: Fresh tip each time
for i in range(4):
    p1000.pick_up_tip()
    p1000.aspirate(171, media)
    p1000.dispense(171, plate[i])
    p1000.drop_tip()

# ✅ BETTER: Use distribute()
p1000.distribute(171, media, plate.wells()[:4])
```

**Wrong pipette for volume range:**
```python
# ❌ WRONG: 200 µL transfer with 50 µL pipette
p50.aspirate(200, source)  # Error! Max is 50 µL

# ✅ CORRECT: Use 1000 µL pipette for larger volumes
p1000.aspirate(200, source)
```

### Other Common Errors

- **Wrong API level**: Must use `apiLevel: '2.16'` and `robotType: 'Flex'`
- **Tip exhaustion**: 96-tip rack = 96 tips. Count your operations!
- **Deck conflicts**: Back row (A) has height restrictions
- **Missing mix steps**: Dilutions need mixing for accuracy
- **No overage**: Always add 10-20% extra volume to reservoirs
- **Source depletion**: Calculate total volume needed from each source

---

## Protocol Templates

Load [references/protocol-templates.md](references/protocol-templates.md) for:
- Serial dilution (8-channel, column-based)
- Plate washing (96-channel)
- Reagent addition (full plate with 96-channel)
- Individual well treatment (single-channel)
- Row-by-row treatment (single-channel, NOT 8-channel)
- Time-staggered additions

---

## Reference Materials

- **[references/flex-specifications.md](references/flex-specifications.md)**: Deck, pipettes, modules — **LOAD FIRST**
- **[references/protocol-templates.md](references/protocol-templates.md)**: Code blocks for common operations
- **[references/labware-reference.md](references/labware-reference.md)**: Plate types, reservoirs, tip racks
- **[references/liquid-handling-tips.md](references/liquid-handling-tips.md)**: Best practices, error prevention
- **[references/example-protocols.md](references/example-protocols.md)**: Complete working examples

---

## Safety Defaults

Always include unless explicitly overridden:

```python
# Slower aspiration for safety
pipette.flow_rate.aspirate = 150  # µL/s
pipette.flow_rate.dispense = 300

# Remove droplets from tip exterior
pipette.touch_tip()

# Ensure complete liquid delivery
pipette.blow_out()
```

---

## Validation Functions

Use these checks during protocol generation:

### Pipette-Layout Compatibility
```python
def validate_pipette_for_wells(pipette_type, target_wells):
    """
    Check if pipette type is appropriate for target wells.

    Returns: (is_valid, error_message)
    """
    if pipette_type == '8-channel':
        # Group wells by column
        columns = {}
        for well in target_wells:
            col = well[1:]  # e.g., '1' from 'A1'
            row = well[0]   # e.g., 'A' from 'A1'
            if col not in columns:
                columns[col] = set()
            columns[col].add(row)

        # Check if any column has < 8 rows targeted
        for col, rows in columns.items():
            if len(rows) < 8:
                return False, f"8-channel targets column {col} but only rows {rows}. Use single-channel."

    return True, ""
```

### Volume Capacity Check
```python
def validate_volumes(pipette_max, operations):
    """
    Check cumulative volume doesn't exceed pipette capacity.

    operations: list of aspirate volumes between tip pickup/dropoff
    """
    for op_set in operations:
        cumulative = sum(op_set)
        if cumulative > pipette_max:
            return False, f"Cumulative {cumulative} µL exceeds {pipette_max} µL capacity"
    return True, ""
```

### Source Volume Check
```python
def validate_source_volume(total_aspirated, source_capacity, dead_volume):
    """
    Verify source has enough volume.
    """
    required = total_aspirated + dead_volume
    if required > source_capacity:
        return False, f"Need {required} µL but source holds {source_capacity} µL"
    return True, ""
```
