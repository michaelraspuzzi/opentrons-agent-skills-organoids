# Experimental Designs for Hackathon Settings

## Opentrons Flex Capabilities

### Pipetting
- **96-channel**: Entire plate in one aspiration (great for washing, adding reagents)
- **8-channel**: Row-by-row operations, serial dilutions
- **Single channel**: Precise additions, complex layouts

### Modules
- **Temperature module**: Keep reagents cold, temperature-sensitive assays
- **Heater-shaker**: Incubation at 37°C, mixing for resuspension
- **Magnetic module**: Bead-based purification, magnetic separation
- **Thermocycler**: PCR if needed

### Practical Throughput
- 96-well plate processing: 5-15 min for full plate treatment
- Serial dilution (8 concentrations): 10-15 min
- Plate washing (3x): 15-20 min
- Tip changes add time - plan accordingly

---

## Standard Experimental Designs

### Design 1: Dose-Response (Most Common)

**When to use**: Testing concentration-dependent effects

**Layout** (96-well plate):
```
    1   2   3   4   5   6   7   8   9  10  11  12
A  [C1][C1][C1][C2][C2][C2][C3][C3][C3][C4][C4][C4]
B  [C1][C1][C1][C2][C2][C2][C3][C3][C3][C4][C4][C4]
C  [C5][C5][C5][C6][C6][C6][C7][C7][C7][C8][C8][C8]
D  [C5][C5][C5][C6][C6][C6][C7][C7][C7][C8][C8][C8]
E  [Veh][Veh][Veh][Pos][Pos][Pos][ - ][ - ][ - ][ - ]
...
```

**Key parameters**:
- 6-8 concentrations (half-log spacing: 1, 3, 10, 30, 100, 300...)
- N=3-4 per concentration minimum
- Vehicle control (0) + positive control
- Total: 24-32 wells per compound

**Opentrons workflow**:
1. Prepare serial dilution in separate plate
2. Use 8-channel to transfer to cell plate by row
3. Incubate
4. Add readout reagent with 96-channel

---

### Design 2: Time-Course

**When to use**: Understanding kinetics, finding optimal timepoint

**Layout** (96-well, single treatment):
```
    1   2   3   4   5   6   7   8   9  10  11  12
A  [0h][0h][0h][0h][2h][2h][2h][2h][4h][4h][4h][4h]  Treated
B  [0h][0h][0h][0h][2h][2h][2h][2h][4h][4h][4h][4h]  Treated
C  [6h][6h][6h][6h][12h][12h][12h][12h][24h][24h][24h][24h]  Treated
D  [6h][6h][6h][6h][12h][12h][12h][12h][24h][24h][24h][24h]  Treated
E  [0h][0h][0h][0h][2h][2h][2h][2h][4h][4h][4h][4h]  Vehicle
...
```

**Key parameters**:
- 4-6 timepoints (0, 2, 4, 6, 12, 24h for 24h experiment)
- N=4 per timepoint
- Matched vehicle controls at each timepoint
- Stagger treatments so all end simultaneously

**Opentrons workflow**:
1. Treat wells at staggered times (Opentrons can run timed protocols)
2. At endpoint, process all wells together
3. Single readout plate

---

### Design 3: Factorial (Combination/Synergy)

**When to use**: Testing if two factors interact

**Layout** (2x2 factorial):
```
         Factor B -    Factor B +
Factor A -  [Control]    [B only]
Factor A +  [A only]     [A + B]
```

**96-well version** (2 factors, 2 levels each, N=6):
```
    1   2   3   4   5   6   7   8   9  10  11  12
A  [--][--][--][--][--][--][+B][+B][+B][+B][+B][+B]
B  [--][--][--][--][--][--][+B][+B][+B][+B][+B][+B]
C  [+A][+A][+A][+A][+A][+A][AB][AB][AB][AB][AB][AB]
D  [+A][+A][+A][+A][+A][+A][AB][AB][AB][AB][AB][AB]
```

**Key parameters**:
- 4 groups: Control, A only, B only, A+B
- N=6+ per group for interaction statistics
- Total: 24 wells minimum

**Analysis**: Two-way ANOVA, look for interaction term

---

### Design 4: Comparison (Head-to-Head)

**When to use**: Comparing methods, media, conditions

**Layout** (3 conditions):
```
    1   2   3   4   5   6   7   8   9  10  11  12
A  [C1][C1][C1][C1][C2][C2][C2][C2][C3][C3][C3][C3]
B  [C1][C1][C1][C1][C2][C2][C2][C2][C3][C3][C3][C3]
C  [C1][C1][C1][C1][C2][C2][C2][C2][C3][C3][C3][C3]
D  [C1][C1][C1][C1][C2][C2][C2][C2][C3][C3][C3][C3]
```

**Key parameters**:
- 2-4 conditions to compare
- N=8-16 per condition (more power for detecting differences)
- Same cell source, same passage

---

### Design 5: Mini-Screen (Compound Library)

**When to use**: Testing multiple compounds for hits

**Layout** (24 compounds, N=3):
```
    1   2   3   4   5   6   7   8   9  10  11  12
A  [1 ][1 ][1 ][2 ][2 ][2 ][3 ][3 ][3 ][4 ][4 ][4 ]
B  [5 ][5 ][5 ][6 ][6 ][6 ][7 ][7 ][7 ][8 ][8 ][8 ]
C  [9 ][9 ][9 ][10][10][10][11][11][11][12][12][12]
D  [13][13][13][14][14][14][15][15][15][16][16][16]
E  [17][17][17][18][18][18][19][19][19][20][20][20]
F  [21][21][21][22][22][22][23][23][23][24][24][24]
G  [Veh][Veh][Veh][Veh][Pos][Pos][Pos][Pos][ - ][ - ][ - ][ - ]
H  [Veh][Veh][Veh][Veh][Pos][Pos][Pos][Pos][ - ][ - ][ - ][ - ]
```

**Key parameters**:
- 20-30 compounds feasible in hackathon
- N=3 minimum (N=4 preferred)
- Vehicle + positive control (N=8 each)
- Single concentration (typically 10 µM)

---

## Readout-Specific Protocols

### Viability Assays

**CellTiter-Glo (ATP, luminescence)**
- Add 1:1 with media
- Shake 2 min
- Incubate 10 min RT
- Read luminescence
- **Time**: 15-20 min
- **Opentrons**: 96-channel add reagent, heater-shaker mix

**Calcein/PI (live/dead, fluorescence)**
- Add dye mix (1:500 each)
- Incubate 30 min at 37°C
- Read: Calcein Ex/Em 494/517, PI Ex/Em 535/617
- **Time**: 45 min
- **Opentrons**: Add dye, return to incubator, read on plate reader

**MTT/XTT (metabolic, absorbance)**
- Add reagent (10% v/v)
- Incubate 2-4 hours
- Read absorbance 450-570 nm
- **Time**: 3-5 hours
- **Opentrons**: Add reagent, incubate off-deck

### Calcium Imaging

**Fluo-4 (single wavelength)**
- Load cells: 2-5 µM Fluo-4 AM, 30 min, 37°C
- Wash 2x PBS
- Image or plate reader kinetic mode
- **Time**: 1 hour setup + imaging
- **Opentrons**: Add dye, wash steps

**Calcium transient recording**
- Requires microscope with video
- 10-30 second recordings
- Analysis: peak amplitude, transient duration, decay rate
- **Manual step**: Microscopy

### Morphology/Staining

**Live imaging**
- Brightfield/phase: immediate
- Hoechst (nuclei): 15 min incubation
- **Time**: Minutes to 30 min

**Fixed staining (if time permits)**
- Fix: 4% PFA, 15 min
- Permeabilize: 0.1% Triton, 10 min
- Block: 1% BSA, 30 min
- Primary antibody: 1-2 hours (or overnight - too long for hackathon)
- Secondary: 1 hour
- **Time**: 3-4 hours minimum (primary shortcut)

### Beating Analysis

**Video-based**
- Record brightfield video (10-30 sec, 30 fps)
- Analysis: Manual count or automated (python/MATLAB)
- Metrics: beats per minute, regularity, amplitude
- **Time**: Minutes per well
- **Throughput limited by microscopy**

---

## Sample Size Guidelines

| Effect Size | Required N (per group) | Total Wells (2 groups) |
|-------------|------------------------|------------------------|
| Large (50%+ change) | 3-4 | 6-8 |
| Medium (25-50%) | 6-8 | 12-16 |
| Small (10-25%) | 12-16 | 24-32 |

**Hackathon rule of thumb**: N=4-6 per group, focus on large effects

---

## Opentrons Protocol Templates

### Template 1: Drug Treatment + Endpoint Readout

```
1. Aspirate media from wells (8-channel or 96-channel)
2. Add treatment media (pre-prepared dilution plate)
3. Incubate X hours (off-deck)
4. Add readout reagent (96-channel)
5. Incubate Y minutes
6. Transfer to read plate or read in place
```

### Template 2: Serial Dilution

```
1. Add diluent to columns 2-12 (180 µL each)
2. Add concentrated compound to column 1 (200 µL)
3. Serial transfer 20 µL: 1→2, 2→3, ... , 11→12
4. Mix each column after transfer
5. Transfer diluted compounds to cell plate
```

### Template 3: Plate Washing (3x)

```
Repeat 3 times:
1. Aspirate media (leave 20 µL to avoid drying)
2. Add 200 µL wash buffer
3. Wait 30 sec
```

---

## Troubleshooting Common Issues

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| High well-to-well variability | Edge effects, uneven seeding | Use inner wells only; check seeding |
| No drug effect | Concentration too low, wrong timepoint | Increase conc; check literature EC50 |
| All cells dead | Drug toxic, contamination | Add lower concentrations; check sterility |
| Plate reader inconsistent | Bubbles, condensation | Centrifuge plate; wipe bottom |
| Opentrons misses wells | Calibration off | Re-calibrate; check tip pickup |
