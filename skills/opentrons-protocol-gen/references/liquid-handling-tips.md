# Liquid Handling Best Practices

## CRITICAL: Pipette Selection (Read First!)

**The #1 source of protocol errors is using the wrong pipette type.**

### 8-Channel Pipette Behavior

When you use an 8-channel pipette and target ANY well (e.g., `plate['A1']`):
- It dispenses to **ALL 8 WELLS IN THAT COLUMN** (A1, B1, C1, D1, E1, F1, G1, H1)
- NOT just the single well you specified!

**This is correct 8-channel usage:**
```python
# All 8 wells in column 1 get the same treatment
p8.transfer(100, reagent, plate.columns()[0][0])  # Hits A1-H1
```

**This is WRONG 8-channel usage:**
```python
# Trying to treat A1 and A2 differently - WILL NOT WORK
p8.transfer(100, treatment_1, plate['A1'])  # Hits A1,B1,C1,D1,E1,F1,G1,H1!
p8.transfer(100, treatment_2, plate['A2'])  # Hits A2,B2,C2,D2,E2,F2,G2,H2!
```

### When to Use Each Pipette

| Situation | Use This | Why |
|-----------|----------|-----|
| Different treatments to individual wells | **Single-channel** | Only option for scattered wells |
| Rows A-D get X, rows E-H get Y | **Single-channel** | 8-channel can't split rows |
| All wells in columns get same treatment | **8-channel** | Efficient for column operations |
| Entire plate gets same treatment | **96-channel** | One operation for all wells |

### Quick Decision Rule

**If your plate map shows different treatments in different ROWS within the same COLUMN → you MUST use single-channel.**

---

## Core Principles

### 1. Always Calculate Overage
Never prepare exactly the volume needed. Pipettes lose small amounts.

| Transfer Type | Overage |
|---------------|---------|
| Single transfers | +10% |
| Multiple from same source | +20% |
| Viscous liquids | +30% |
| 96-channel from reservoir | +25% |

### 2. CRITICAL: Respect Volume Capacity

**Never aspirate more than the pipette can hold!**

| Pipette | Min | Max |
|---------|-----|-----|
| flex_1channel_1000 / flex_8channel_1000 / flex_96channel_1000 | 5 µL | 1000 µL |
| flex_1channel_50 / flex_8channel_50 / flex_96channel_50 | 1 µL | 50 µL |

**Common Error - Cumulative Overflow:**
```python
# ❌ WRONG: Aspirating 4 times without dispensing = 684 µL total!
p200.pick_up_tip()
for i in range(4):
    p200.aspirate(171, media)  # Cumulative: 171, 342, 513, 684 µL - OVERFLOW!
    p200.dispense(171, plate[i])
p200.drop_tip()

# ✅ CORRECT: Fresh tip for each transfer
for i in range(4):
    p1000.pick_up_tip()
    p1000.aspirate(171, media)
    p1000.dispense(171, plate[i])
    p1000.drop_tip()

# ✅ BEST: Use distribute() method
p1000.distribute(171, media, [plate.wells()[i] for i in range(4)])
```

### 3. Account for Dead Volume
Liquid the pipette can't reach at the bottom.

| Labware | Dead Volume |
|---------|-------------|
| 12-well reservoir | ~2 mL per well |
| Single trough | ~10-15 mL |
| 96-well plate | ~20-50 µL per well |
| 1.5 mL tube | ~50 µL |
| 15 mL tube | ~500 µL |

### 4. Tip Changes Matter
When to change tips:

| Situation | Change Tips? |
|-----------|--------------|
| Different reagents | ✅ Always |
| Same reagent, different destinations | Usually no |
| Treatment → control wells | ✅ Always |
| Aspirating from cells | ✅ Always (contamination) |
| Serial dilution transfers | ✅ At each step OR use same tip with mixing |

---

## Aspiration Best Practices

### Aspiration Height

```python
# Default: bottom of well
pipette.aspirate(100, well)  # Aspirates from bottom

# Specify height from bottom
pipette.aspirate(100, well.bottom(z=2))  # 2mm above bottom

# From top (for very full wells)
pipette.aspirate(100, well.top(z=-5))  # 5mm below top
```

**Guidelines**:
- Cells at bottom: Aspirate from z=2mm or higher
- Clear liquid: z=1mm is usually safe
- Nearly empty well: Be careful not to aspirate air

### Aspiration Speed

```python
# Slow down for:
pipette.flow_rate.aspirate = 50  # µL/sec

# - Viscous liquids (glycerol, Matrigel)
# - Avoiding bubbles
# - Not disturbing cells
# - Small volumes (<10 µL)

# Speed up for:
pipette.flow_rate.aspirate = 200  # µL/sec

# - Aqueous buffers
# - Large volumes
# - Time-sensitive protocols
```

### Pre-Wetting Tips

For accurate volumes, especially small ones:

```python
# Pre-wet by aspirating and dispensing 2-3 times
pipette.pick_up_tip()
for _ in range(3):
    pipette.aspirate(100, source)
    pipette.dispense(100, source)
# Now do actual transfer
pipette.aspirate(100, source)
pipette.dispense(100, destination)
```

---

## Dispensing Best Practices

### Touch Tip

Removes droplets clinging to tip exterior:

```python
pipette.dispense(100, well)
pipette.touch_tip()  # Touches sides of well
```

Use after:
- Dispensing viscous liquids
- Dispensing small volumes
- When droplet visible on tip

### Blow Out

Ensures all liquid exits tip:

```python
pipette.dispense(100, well)
pipette.blow_out()  # Pushes plunger past dispense point
```

Use after:
- Every dispense (safest)
- Viscous liquids
- When full volume critical

### Dispense Position

```python
# At bottom (default, may cause splashing)
pipette.dispense(100, well)

# Above liquid surface (prevents contamination)
pipette.dispense(100, well.top(z=-2))

# Just above bottom (gentle addition)
pipette.dispense(100, well.bottom(z=5))
```

---

## Mixing

### When to Mix

- After adding concentrated reagent
- Serial dilutions (critical!)
- After adding cells to media
- Before aspirating from settled solution

### Mix Parameters

```python
pipette.mix(
    repetitions=3,      # Number of up/down cycles
    volume=100,         # Volume to aspirate/dispense
    location=well       # Where to mix
)

# Or during transfer:
pipette.transfer(
    100,
    source,
    dest,
    mix_after=(3, 80)  # 3 cycles of 80 µL after dispense
)
```

**Volume rule**: Mix with ~80% of well volume or transfer volume

### Mixing Speed

```python
# Gentle mixing (cells, proteins)
pipette.flow_rate.aspirate = 50
pipette.flow_rate.dispense = 50
pipette.mix(3, 100, well)

# Vigorous mixing (buffer, small molecules)
pipette.flow_rate.aspirate = 200
pipette.flow_rate.dispense = 200
pipette.mix(5, 150, well)
```

---

## Advanced Techniques

### Transfer() Method

Convenience method that combines pick up tip, aspirate, dispense, and drop tip:

```python
pipette.transfer(
    100,                  # Volume
    source,               # Source well
    destination,          # Destination well
    new_tip='always',     # Tip strategy: 'always', 'once', 'never'
    mix_before=(3, 80),   # Mix before aspirating
    mix_after=(3, 80),    # Mix after dispensing
    blow_out=True,        # Blow out after dispense
    touch_tip=True        # Touch tip after dispense
)
```

### Distribute() Method

One source to many destinations:

```python
pipette.distribute(
    50,                     # Volume per destination
    source,                 # Source well
    [dest1, dest2, dest3],  # List of destinations
    new_tip='once',         # Use same tip for all
    disposal_volume=10      # Extra aspirated to avoid air
)
```

### Consolidate() Method

Many sources to one destination:

```python
pipette.consolidate(
    50,                     # Volume from each source
    [src1, src2, src3],     # List of sources
    destination,            # Destination well
    new_tip='once'          # Use same tip for all
)
```

---

## Troubleshooting

### Bubbles in Tips

**Causes**:
- Aspirating too fast
- Air gap in source

**Solutions**:
```python
pipette.flow_rate.aspirate = 50  # Slow down
pipette.aspirate(100, source.bottom(z=2))  # Aspirate higher
```

### Droplets on Tip Exterior

**Causes**:
- Viscous liquid
- Too fast dispense

**Solutions**:
```python
pipette.touch_tip()  # After dispense
pipette.flow_rate.dispense = 100  # Slow down
```

### Incomplete Dispense

**Causes**:
- Viscous liquid
- Surface tension

**Solutions**:
```python
pipette.blow_out()  # Force all liquid out
pipette.dispense(100, well.bottom(z=2))  # Dispense near bottom
```

### Volume Inaccuracy

**Causes**:
- No pre-wetting
- Wrong flow rate
- Volume near pipette limits

**Solutions**:
```python
# Pre-wet tips
for _ in range(3):
    pipette.aspirate(volume, source)
    pipette.dispense(volume, source)

# Use appropriate pipette for volume range
# 1-50 µL → use 50 µL pipette
# 50-1000 µL → use 1000 µL pipette
```

---

## Safety Checklist

Before running protocol:

- [ ] All volumes within pipette capacity
- [ ] Overage calculated (20% extra minimum)
- [ ] Dead volumes accounted for
- [ ] Tip count sufficient for protocol
- [ ] Flow rates appropriate for liquids
- [ ] Aspiration heights safe (not hitting bottom with cells)
- [ ] Mix steps included where needed
- [ ] Blow out after critical dispenses
- [ ] Touch tip for viscous liquids
