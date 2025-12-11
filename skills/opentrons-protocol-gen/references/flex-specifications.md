# Opentrons Flex Specifications

## Deck Layout

```
        BACK (away from user)
┌─────┬─────┬─────┬─────┐
│ A1  │ A2  │ A3  │ A4  │  ← Staging area (A4 off-deck)
├─────┼─────┼─────┼─────┤
│ B1  │ B2  │ B3  │ B4  │  ← Back row
├─────┼─────┼─────┼─────┤
│ C1  │ C2  │ C3  │ C4  │  ← Middle row
├─────┼─────┼─────┼─────┤
│ D1  │ D2  │ D3  │ D4  │  ← Front row
└─────┴─────┴─────┴─────┘
        FRONT (user side)

Trash: Fixed position (front right)
```

### Slot Naming Convention
- Letter = Row (A=back, D=front)
- Number = Column (1=left, 4=right)
- Slot "A1" is back-left, "D4" is front-right

### Deck Slot Compatibility

| Slot | Standard Labware | Modules | Notes |
|------|------------------|---------|-------|
| A1 | ✅ | ✅ | Back left |
| A2 | ✅ | ✅ | Back center-left |
| A3 | ✅ | ✅ | Back center-right |
| A4 | Staging only | ❌ | Off-deck staging |
| B1 | ✅ | ✅ | |
| B2 | ✅ | ✅ | |
| B3 | ✅ | ✅ | |
| B4 | Staging only | ❌ | Off-deck staging |
| C1 | ✅ | ✅ | Good for reservoirs |
| C2 | ✅ | ✅ | Central, easy access |
| C3 | ✅ | ✅ | Central, easy access |
| C4 | Staging only | ❌ | Off-deck staging |
| D1 | ✅ | ✅ | Front, good for plates |
| D2 | ✅ | ✅ | Front, good for plates |
| D3 | ✅ | ✅ | Front, good for plates |
| D4 | Staging only | ❌ | Off-deck staging |

### Height Restrictions
- Maximum labware height: ~100mm in most slots
- Modules add height—check clearance
- Tall tip racks (1000 µL) need clearance from pipette travel path

---

## Pipettes

### 96-Channel Pipette

**Two volume ranges** (separate pipettes, not adjustable):
| Model | Volume Range | Tip Type |
|-------|--------------|----------|
| Flex 96-Channel 1000 µL | 5-1000 µL | 1000 µL tips |
| Flex 96-Channel 50 µL | 1-50 µL | 50 µL tips |

**Capabilities**:
- Picks up entire 96-tip rack at once
- Transfers to/from entire 96-well plate at once
- Can do partial column pickup (8, 16, 24... tips)

**Best for**:
- Full-plate reagent additions
- Plate washes
- Plate-to-plate transfers

**Code example**:
```python
pip_96 = protocol.load_instrument(
    'flex_96channel_1000',  # or 'flex_96channel_50'
    mount='left'            # 96-channel only fits left mount
)
```

### 8-Channel Pipette

| Model | Volume Range | Tip Type |
|-------|--------------|----------|
| Flex 8-Channel 1000 µL | 5-1000 µL | 1000 µL tips |
| Flex 8-Channel 50 µL | 1-50 µL | 50 µL tips |

**Best for**:
- Row-by-row operations
- Serial dilutions
- Selective transfers

**Code example**:
```python
pip_8 = protocol.load_instrument(
    'flex_8channel_1000',   # or 'flex_8channel_50'
    mount='right'
)
```

### Single-Channel Pipette

| Model | Volume Range | Tip Type |
|-------|--------------|----------|
| Flex 1-Channel 1000 µL | 5-1000 µL | 1000 µL tips |
| Flex 1-Channel 50 µL | 1-50 µL | 50 µL tips |

**Best for**:
- Precise single-well additions
- Complex plate layouts
- Reagent prep

**Code example**:
```python
pip_single = protocol.load_instrument(
    'flex_1channel_1000',  # or 'flex_1channel_50'
    mount='right'
)
```

### Mount Positions
- **Left mount**: 96-channel pipette (only option for 96-ch)
- **Right mount**: 8-channel OR single-channel
- Can have 96-channel + 8-channel, OR 96-channel + single

---

## Modules

### Temperature Module (Gen 2)

**Specs**:
- Temperature range: 4°C to 95°C
- Accuracy: ±1°C
- Compatible labware: 96-well plates, tube racks

**Code example**:
```python
temp_mod = protocol.load_module(
    'temperature module gen2',
    slot='D1'
)
temp_plate = temp_mod.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt')
temp_mod.set_temperature(4)  # Keep reagents cold
```

### Heater-Shaker Module

**Specs**:
- Temperature range: 37°C to 95°C (heating only, no cooling)
- Shake speed: 200-3000 rpm
- Orbit: 3mm
- Has latch to secure plate

**Code example**:
```python
hs_mod = protocol.load_module(
    'heaterShakerModuleV1',
    slot='D1'
)
hs_plate = hs_mod.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt')

hs_mod.open_labware_latch()  # Must open before pipetting
# ... pipetting steps ...
hs_mod.close_labware_latch()
hs_mod.set_and_wait_for_temperature(37)
hs_mod.set_and_wait_for_shake_speed(500)
protocol.delay(minutes=5)
hs_mod.deactivate_shaker()
```

### Magnetic Module (Gen 2)

**Specs**:
- Engage height: 0-25mm (adjustable)
- For magnetic bead-based protocols

**Code example**:
```python
mag_mod = protocol.load_module(
    'magnetic module gen2',
    slot='C1'
)
mag_plate = mag_mod.load_labware('nest_96_wellplate_2ml_deep')
mag_mod.engage(height_from_base=6)  # Engage magnets
protocol.delay(minutes=2)            # Wait for beads
# Aspirate supernatant
mag_mod.disengage()                  # Release magnets
```

### Thermocycler Module

**Specs**:
- Temperature range: 4°C to 99°C (block), RT to 110°C (lid)
- Ramp rate: Up to 3°C/sec
- Takes two deck slots (A1 + B1)

**Code example**:
```python
tc_mod = protocol.load_module('thermocycler module gen2')
tc_plate = tc_mod.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt')

tc_mod.open_lid()
# ... load samples ...
tc_mod.close_lid()
tc_mod.set_lid_temperature(105)
tc_mod.set_block_temperature(95, hold_time_seconds=30)
```

---

## Tip Racks

### Available Tip Racks

| Labware Name | Volume | Tips per Rack |
|--------------|--------|---------------|
| `opentrons_flex_96_tiprack_50ul` | 50 µL | 96 |
| `opentrons_flex_96_tiprack_200ul` | 200 µL | 96 |
| `opentrons_flex_96_tiprack_1000ul` | 1000 µL | 96 |
| `opentrons_flex_96_filtertiprack_50ul` | 50 µL filter | 96 |
| `opentrons_flex_96_filtertiprack_200ul` | 200 µL filter | 96 |
| `opentrons_flex_96_filtertiprack_1000ul` | 1000 µL filter | 96 |

### Tip Usage Planning

| Pipette | Tips per Operation | Notes |
|---------|-------------------|-------|
| 96-channel | 96 tips | Full rack per pickup |
| 8-channel | 8 tips | One column per pickup |
| Single | 1 tip | One tip per pickup |

**Calculation example**:
- 96-channel: 5 full-plate operations = 5 tip racks
- 8-channel: 24 transfers (2 columns each) = 48 tips = 1 rack
- Single: 50 individual transfers = 50 tips = 1 rack

---

## Flow Rates

### Default Flow Rates (µL/sec)

| Pipette | Aspirate | Dispense | Blow Out |
|---------|----------|----------|----------|
| 1000 µL | 160 | 160 | 80 |
| 50 µL | 35 | 35 | N/A |

### Adjusting Flow Rates

```python
# Slow down for viscous liquids or gentle handling
pipette.flow_rate.aspirate = 50
pipette.flow_rate.dispense = 100

# Speed up for aqueous solutions
pipette.flow_rate.aspirate = 200
pipette.flow_rate.dispense = 300
```

---

## API Version

**Current for Flex**: `2.16`

```python
metadata = {
    'protocolName': 'My Protocol',
    'apiLevel': '2.16'
}

requirements = {
    'robotType': 'Flex',
    'apiLevel': '2.16'
}
```

**Always include both metadata and requirements for Flex protocols.**

---

## Common Deck Layouts

### Layout 1: Simple Drug Treatment
```
A1: Tip rack 200 µL
A2: Tip rack 200 µL (backup)
B1: Reservoir (media, drug)
C1: [empty]
D1: Cell plate (destination)
D2: [empty]
```

### Layout 2: Serial Dilution + Treatment
```
A1: Tip rack 200 µL
A2: Tip rack 200 µL
B1: Reservoir (media, diluent)
B2: Dilution plate (source)
C1: [empty]
D1: Cell plate 1
D2: Cell plate 2
```

### Layout 3: With Heater-Shaker
```
A1: Tip rack 200 µL
A2: Tip rack 200 µL
B1: Reservoir
C1: Heater-Shaker with plate
D1: Destination plate
```
