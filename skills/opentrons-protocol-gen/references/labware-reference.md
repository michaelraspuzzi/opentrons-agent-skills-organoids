# Labware Reference

## 96-Well Plates

### Standard Cell Culture Plates

| Labware Name | Well Volume | Best For |
|--------------|-------------|----------|
| `corning_96_wellplate_360ul_flat` | 360 µL | General cell culture, imaging |
| `nest_96_wellplate_200ul_flat` | 200 µL | Assays, smaller volumes |
| `nest_96_wellplate_2ml_deep` | 2000 µL | Deep well, reagent storage |

### PCR Plates

| Labware Name | Well Volume | Best For |
|--------------|-------------|----------|
| `opentrons_96_wellplate_200ul_pcr_full_skirt` | 200 µL | PCR, fits on modules |
| `nest_96_wellplate_100ul_pcr_full_skirt` | 100 µL | Low volume PCR |

### Specialty Plates

| Labware Name | Well Volume | Best For |
|--------------|-------------|----------|
| `corning_96_wellplate_360ul_flat_white` | 360 µL | Luminescence assays |
| `corning_96_wellplate_360ul_flat_black` | 360 µL | Fluorescence assays |

---

## 24-Well and 6-Well Plates

| Labware Name | Well Volume | Wells |
|--------------|-------------|-------|
| `corning_24_wellplate_3.4ml_flat` | 3.4 mL | 24 |
| `corning_6_wellplate_16.8ml_flat` | 16.8 mL | 6 |

**Note**: 8-channel and 96-channel pipettes don't align with 24-well or 6-well spacing. Use single-channel for these plates.

---

## Reservoirs

### 12-Column Reservoirs

| Labware Name | Well Volume | Total Volume | Best For |
|--------------|-------------|--------------|----------|
| `nest_12_reservoir_15ml` | 15 mL | 180 mL | Multiple reagents, serial dilution source |
| `usascientific_12_reservoir_22ml` | 22 mL | 264 mL | Larger volumes |

### Single-Trough Reservoirs

| Labware Name | Total Volume | Best For |
|--------------|--------------|----------|
| `nest_1_reservoir_195ml` | 195 mL | Large volume single reagent (media, PBS) |
| `agilent_1_reservoir_290ml` | 290 mL | Very large volumes |

### Choosing Reservoir Type

| Use Case | Recommended |
|----------|-------------|
| Single reagent, large volume | Single trough |
| Multiple reagents | 12-column |
| 8-channel serial dilution | 12-column |
| 96-channel full plate addition | Single trough OR 12-column |

---

## Tip Racks

### Flex-Specific Tips (Required for Flex)

| Labware Name | Volume | Tips | Compatible Pipettes |
|--------------|--------|------|---------------------|
| `opentrons_flex_96_tiprack_50ul` | 50 µL | 96 | 50 µL pipettes |
| `opentrons_flex_96_tiprack_200ul` | 200 µL | 96 | 1000 µL pipettes (for small vols) |
| `opentrons_flex_96_tiprack_1000ul` | 1000 µL | 96 | 1000 µL pipettes |

### Filter Tips

| Labware Name | Volume | Tips | When to Use |
|--------------|--------|------|-------------|
| `opentrons_flex_96_filtertiprack_50ul` | 50 µL | 96 | Volatile/hazardous liquids |
| `opentrons_flex_96_filtertiprack_200ul` | 200 µL | 96 | Cross-contamination prevention |
| `opentrons_flex_96_filtertiprack_1000ul` | 1000 µL | 96 | Biohazards |

---

## Tube Racks

### 1.5/2.0 mL Tubes

| Labware Name | Tube Type | Tubes |
|--------------|-----------|-------|
| `opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap` | 1.5 mL Eppendorf | 24 |
| `opentrons_24_tuberack_nest_1.5ml_snapcap` | 1.5 mL NEST | 24 |
| `opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap` | 2.0 mL Eppendorf | 24 |

### 15/50 mL Tubes

| Labware Name | Tube Type | Tubes |
|--------------|-----------|-------|
| `opentrons_15_tuberack_falcon_15ml_conical` | 15 mL Falcon | 15 |
| `opentrons_6_tuberack_falcon_50ml_conical` | 50 mL Falcon | 6 |

---

## Module-Compatible Labware

### Temperature Module

| Labware Name | Compatible |
|--------------|------------|
| `opentrons_96_wellplate_200ul_pcr_full_skirt` | ✅ |
| `opentrons_24_aluminumblock_nest_1.5ml_snapcap` | ✅ |
| `opentrons_96_aluminumblock_generic_pcr_strip_200ul` | ✅ |

### Heater-Shaker Module

| Labware Name | Compatible |
|--------------|------------|
| `opentrons_96_wellplate_200ul_pcr_full_skirt` | ✅ |
| `nest_96_wellplate_200ul_flat` | ✅ |
| `corning_96_wellplate_360ul_flat` | ✅ |
| `nest_96_wellplate_2ml_deep` | ✅ |

### Magnetic Module

| Labware Name | Compatible |
|--------------|------------|
| `nest_96_wellplate_2ml_deep` | ✅ (common for bead work) |
| `nest_96_wellplate_100ul_pcr_full_skirt` | ✅ |

### Thermocycler

| Labware Name | Compatible |
|--------------|------------|
| `opentrons_96_wellplate_200ul_pcr_full_skirt` | ✅ |
| `nest_96_wellplate_100ul_pcr_full_skirt` | ✅ |

---

## Loading Labware in Code

### Basic Loading

```python
# Load on deck slot
plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')

# Load on module
temp_mod = protocol.load_module('temperature module gen2', 'C1')
temp_plate = temp_mod.load_labware('opentrons_96_wellplate_200ul_pcr_full_skirt')
```

### Loading Multiple Tip Racks

```python
# Load multiple tip racks for long protocols
tip_racks = [
    protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A1'),
    protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A2'),
    protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A3'),
]

# Assign all to pipette
pipette = protocol.load_instrument('flex_8channel_1000', 'right', tip_racks=tip_racks)
```

---

## Well Addressing

### By Name

```python
well_a1 = plate.wells_by_name()['A1']
well_h12 = plate.wells_by_name()['H12']
```

### By Index

```python
first_well = plate.wells()[0]    # A1
last_well = plate.wells()[95]    # H12
```

### By Row

```python
row_a = plate.rows()[0]          # All wells in row A (A1-A12)
row_a = plate.rows_by_name()['A']
```

### By Column

```python
column_1 = plate.columns()[0]     # All wells in column 1 (A1-H1)
column_1 = plate.columns_by_name()['1']
```

---

## Volume Calculations

### Dead Volume in Reservoirs

Always account for dead volume (liquid pipette can't reach):

| Reservoir Type | Dead Volume per Well |
|----------------|---------------------|
| 12-column (15mL) | ~2 mL |
| Single trough | ~10-15 mL |
| Deep well plate | ~100 µL |

### Calculate Required Volume

```
Required = (volume_per_transfer × num_transfers × 1.2) + dead_volume

Example:
- 100 µL per well
- 96 wells
- 20% overage
- 2 mL dead volume

Required = (100 × 96 × 1.2) + 2000 = 11,520 + 2000 = 13,520 µL = 13.5 mL
```

---

## Common Labware Combinations

### Drug Treatment Protocol
```
- 1× Tip rack 200 µL (A1)
- 1× 12-column reservoir (B1) - media, drugs
- 1× 96-well cell culture plate (D1)
```

### Serial Dilution Protocol
```
- 2× Tip racks 200 µL (A1, A2)
- 1× 12-column reservoir (B1) - diluent
- 1× 96-well plate for dilutions (B2)
- 1× 96-well cell plate (D1)
```

### Viability Assay Protocol
```
- 2× Tip racks 1000 µL (A1, A2)
- 1× Single trough reservoir (B1) - CellTiter-Glo
- 1× 96-well cell plate (C1)
- 1× 96-well white plate for reading (D1)
```
