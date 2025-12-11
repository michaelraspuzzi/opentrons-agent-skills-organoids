# Protocol Templates

## Template 1: Serial Dilution (8-Channel)

**Use case**: Creating concentration series in columns

```python
from opentrons import protocol_api

metadata = {
    'protocolName': 'Serial Dilution',
    'apiLevel': '2.16'
}

requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A1')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'B1')
    dilution_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 'D1')

    # Pipette
    p8 = protocol.load_instrument('flex_8channel_1000', 'right', tip_racks=[tips])

    diluent = reservoir['A1']
    stock = reservoir['A2']

    # Add diluent to columns 2-12 (columns 1-11 in 0-indexed)
    p8.pick_up_tip()
    for col_idx in range(1, 12):
        p8.aspirate(180, diluent)
        p8.dispense(180, dilution_plate.columns()[col_idx][0])
    p8.drop_tip()

    # Add stock to column 1
    p8.transfer(200, stock, dilution_plate.columns()[0][0], new_tip='always')

    # Serial dilution: 1:3 (60 µL into 180 µL)
    for col_idx in range(11):  # 0-10 (columns 1-11)
        p8.pick_up_tip()
        p8.aspirate(60, dilution_plate.columns()[col_idx][0])
        p8.dispense(60, dilution_plate.columns()[col_idx + 1][0])
        p8.mix(3, 100, dilution_plate.columns()[col_idx + 1][0])
        p8.drop_tip()
```

---

## Template 2: Individual Well Treatments (Single-Channel)

**Use case**: Different treatments to scattered wells

```python
from opentrons import protocol_api

metadata = {
    'protocolName': 'Individual Well Treatment',
    'apiLevel': '2.16'
}

requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A1')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'B1')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')

    # Pipette
    p1 = protocol.load_instrument('flex_1channel_1000', 'right', tip_racks=[tips])

    # Define treatments
    treatment_map = {
        'A1': reservoir['A1'],  # Treatment 1
        'A2': reservoir['A1'],  # Treatment 1
        'B3': reservoir['A2'],  # Treatment 2
        'C5': reservoir['A3'],  # Treatment 3
        # ... etc
    }

    # Apply treatments
    for well_name, source in treatment_map.items():
        p1.pick_up_tip()
        p1.aspirate(100, source)
        p1.dispense(100, plate.wells_by_name()[well_name])
        p1.blow_out()
        p1.drop_tip()
```

---

## Template 3: Full Plate Addition (96-Channel)

**Use case**: Same reagent to all 96 wells

```python
from opentrons import protocol_api

metadata = {
    'protocolName': 'Full Plate Reagent Addition',
    'apiLevel': '2.16'
}

requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'A1')
    reservoir = protocol.load_labware('nest_1_reservoir_195ml', 'B1')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')

    # Pipette
    p96 = protocol.load_instrument('flex_96channel_1000', 'left', tip_racks=[tips])

    # Add 100 µL to all wells
    p96.pick_up_tip()
    p96.aspirate(100, reservoir['A1'])
    p96.dispense(100, plate['A1'])
    p96.blow_out()
    p96.drop_tip()
```

---

## Template 4: Row-Specific Treatments (Single-Channel)

**Use case**: Different treatments by row within columns

```python
from opentrons import protocol_api

metadata = {
    'protocolName': 'Row-Specific Treatment',
    'apiLevel': '2.16'
}

requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A1')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'B1')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')

    # Pipette - MUST use single-channel for row-specific!
    p1 = protocol.load_instrument('flex_1channel_1000', 'right', tip_racks=[tips])

    treatment_1 = reservoir['A1']
    treatment_2 = reservoir['A2']

    # Rows A-D get treatment 1, rows E-H get treatment 2
    for col in range(12):  # All 12 columns
        for row in ['A', 'B', 'C', 'D']:
            well = f'{row}{col+1}'
            p1.transfer(100, treatment_1, plate.wells_by_name()[well], new_tip='always')

        for row in ['E', 'F', 'G', 'H']:
            well = f'{row}{col+1}'
            p1.transfer(100, treatment_2, plate.wells_by_name()[well], new_tip='always')
```

---

## Template 5: Plate-to-Plate Transfer (96-Channel)

**Use case**: Copy entire plate to another plate

```python
from opentrons import protocol_api

metadata = {
    'protocolName': 'Plate-to-Plate Transfer',
    'apiLevel': '2.16'
}

requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A1')
    source_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'C1')
    dest_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')

    # Pipette
    p96 = protocol.load_instrument('flex_96channel_1000', 'left', tip_racks=[tips])

    # Transfer 50 µL from source to destination
    p96.pick_up_tip()
    p96.aspirate(50, source_plate['A1'])
    p96.dispense(50, dest_plate['A1'])
    p96.drop_tip()
```

---

## Template 6: Module Usage (Heater-Shaker)

**Use case**: Incubate with temperature and shaking

```python
from opentrons import protocol_api

metadata = {
    'protocolName': 'Heater-Shaker Incubation',
    'apiLevel': '2.16'
}

requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A1')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'B1')

    # Heater-Shaker
    hs_mod = protocol.load_module('heaterShakerModuleV1', 'D1')
    hs_plate = hs_mod.load_labware('nest_96_wellplate_200ul_flat')

    # Pipette
    p96 = protocol.load_instrument('flex_96channel_1000', 'left', tip_racks=[tips])

    # Open latch for pipetting
    hs_mod.open_labware_latch()

    # Add reagent
    p96.pick_up_tip()
    p96.aspirate(100, reservoir['A1'])
    p96.dispense(100, hs_plate['A1'])
    p96.drop_tip()

    # Close latch and incubate
    hs_mod.close_labware_latch()
    hs_mod.set_and_wait_for_temperature(37)
    hs_mod.set_and_wait_for_shake_speed(500)
    protocol.delay(minutes=30)

    # Stop and open
    hs_mod.deactivate_shaker()
    hs_mod.deactivate_heater()
    hs_mod.open_labware_latch()
```

---

## Template 7: Distribute (Multi-Dispense)

**Use case**: One source to many destinations efficiently

```python
from opentrons import protocol_api

metadata = {
    'protocolName': 'Distribute Reagent',
    'apiLevel': '2.16'
}

requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A1')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'B1')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')

    # Pipette
    p1 = protocol.load_instrument('flex_1channel_1000', 'right', tip_racks=[tips])

    # Distribute 50 µL to first 12 wells
    destinations = plate.wells()[:12]

    p1.distribute(
        50,                    # Volume per well
        reservoir['A1'],       # Source
        destinations,          # List of destination wells
        new_tip='once'         # Use same tip for all
    )
```

---

## Template 8: Consolidate (Many-to-One)

**Use case**: Pool multiple wells into one

```python
from opentrons import protocol_api

metadata = {
    'protocolName': 'Consolidate Samples',
    'apiLevel': '2.16'
}

requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

def run(protocol: protocol_api.ProtocolContext):
    # Labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'A1')
    source_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'C1')
    tube_rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 'D1')

    # Pipette
    p1 = protocol.load_instrument('flex_1channel_1000', 'right', tip_racks=[tips])

    # Consolidate first 12 wells into tube A1
    sources = source_plate.wells()[:12]

    p1.consolidate(
        30,                    # Volume from each well
        sources,               # List of source wells
        tube_rack['A1'],       # Destination
        new_tip='once'         # Use same tip for all
    )
```
