# Hack Prep Ideas - Cell Cultivation & Organoid Challenges

## Current Equipment
- Opentrons Flex + Gripper
- 1-channel & 8-channel pipettes
- 50µL, 200µL, 1000µL tips
- 3D printers
- **No reagents or specialized labware yet**

---

## What You Can Do NOW (Tip Racks Only)

### Gripper Choreography
- Move tip racks around the deck
- Test gripper calibration
- Practice `move_labware(use_gripper=True)`
- **Protocol: test-6-gripper-tip-rack-demo.py**

---

## What You Can Do With Water + Food Coloring

### Protocol Ideas

**"Cell Seeding Simulator"**
- Water + food coloring as "cell suspension"
- Practice precise volume dispensing (50-200µL)
- Different "densities" = different color concentrations
- Teaches: consistent dispensing, avoiding bubbles, tip touch

**"Media Exchange Trainer"**
- Aspirate from top of well (leave bottom 20µL = "cells")
- Dispense fresh "media" gently down the side
- Teaches: z-height control, gentle flow rates

**"Serial Dilution for Dose Response"**
- Practice half-log dilutions with colored water
- Teaches: mixing, serial transfer, concentration gradients

**"96-Well Art"**
- Draw patterns, logos, or gradients
- Great for demos
- Teaches: well mapping, multi-channel pipetting

---

## Gripper Workflow Ideas

**"Plate Shuttle"**
- Move plates between slots
- Simulates: incubator staging, thermocycler loading
- Teaches: deck planning, gripper calibration

**"Full Workflow Simulation"**
1. Pipette "cells" into plate
2. Gripper moves plate to "incubator staging"
3. Pause (simulates incubation)
4. Gripper returns plate
5. Pipette "media exchange"

---

## 3D Printable Labware

### Priority Prints

| Item | Why | Source |
|------|-----|--------|
| 15mL/50mL Tube Rack | Hold reagent tubes | [tyhho GitHub](https://github.com/tyhho/OT-2_3D_Designs) |
| Reservoir Adapter | Use any container | STLFinder |
| Plate Lid Holder | Keep lids sterile | Custom design |

### Resources
- [Opentrons 3D Printing Directory](https://opentrons.com/archives/resource/opentrons-3d-printing-directory)
- [STLFinder Opentrons models](https://www.stlfinder.com/3dmodels/opentrons/)
- [iGEM Marburg hardware](https://2019.igem.org/Team:Marburg/Hardware)
- [Labware Creator](https://labware.opentrons.com/#/create) - make JSON definitions for custom labware

---

## Challenge-Specific Practice

### For Cell Cultivation Challenge

**Timing Protocol**
- Practice scheduling (media change every 24h)
- Use `protocol.delay()` or pauses
- Log timestamps with `protocol.comment()`

**Contamination Prevention Drill**
- Always use fresh tips
- Touch nothing outside wells
- Practice sterile technique patterns

**Volume Accuracy Test**
- Dispense known volumes of colored water
- Weigh results (1µL water ≈ 1mg)
- Tune flow rates

### For Organoid Hack

**Gentle Handling Protocol**
- Ultra-slow flow rates (50 µL/s aspirate, 75 µL/s dispense)
- Higher z-offset to avoid disturbing "organoids"
- Practice with small beads or seeds as organoid simulants

**Matrix Gel Simulation**
- Cold honey or thick syrup behaves like Matrigel
- Practice dispensing viscous liquids
- Learn temperature-dependent handling

**Multi-Plate Workflow**
- Simulate splitting organoids across plates
- Gripper moves source plate, then destination plates
- Practice maintaining orientation/tracking

---

## Supplies to Get (Cheap/Available)

**For demos:**
- Food coloring (red, blue, yellow, green)
- Water
- Any 96-well plates (even old/used ones)

**For advanced practice:**
- Small beads or chia seeds (organoid simulants)
- Honey or corn syrup (Matrigel simulant)
- Kitchen scale (volume verification)

---

## Protocol Build Order

1. **test-6-gripper-tip-rack-demo.py** - Works now with tip racks only
2. **test-7-seeding-simulator.py** - Need 96-well plate
3. **test-8-media-exchange.py** - Need plate + reservoir
4. **test-9-full-workflow.py** - Full simulation

---

## Useful Links

- [Opentrons Tutorial (serial dilution)](https://docs.opentrons.com/v2/tutorial.html)
- [Moving Labware docs](https://docs.opentrons.com/v2/moving_labware.html)
- [Gripper documentation](https://docs.opentrons.com/flex/labware/gripper/)
- [Cell Culture Protocol Library](https://protocol-delivery.protocols.opentrons.com/categories/Cell%20Culture/)
- [Protocol Designer (no-code)](https://designer.opentrons.com/)
