# Cardiac Organoid Methodology Guide

## Differentiation Protocols

### Wnt Modulation Protocol (Most Common)

**Stage 1: Mesoderm induction (Days 0-2)**
- CHIR99021 (GSK3β inhibitor): 6-12 μM
- Activates Wnt signaling → mesoderm commitment
- Critical: Timing and concentration affect yield

**Stage 2: Cardiac specification (Days 3-5)**
- IWP2 or IWP4 (Wnt inhibitor): 5 μM
- Or C59, XAV939 (alternative Wnt inhibitors)
- Blocks Wnt → cardiac mesoderm

**Stage 3: Cardiomyocyte maturation (Days 5-15+)**
- Remove small molecules
- RPMI + B27 minus insulin (early)
- RPMI + B27 with insulin (later)
- Spontaneous beating typically day 8-12

### GiWi Protocol (Lian Protocol Variant)

- Uses Wnt activators then inhibitors in sequence
- Higher efficiency in some cell lines
- Day 0: CHIR (12 μM, 24h)
- Day 3: IWP2 (5 μM, 48h)
- More reproducible across cell lines

### Growth Factor Protocol (Older)

- Activin A → BMP4 → VEGF sequence
- Less reproducible, more expensive
- Historical importance but largely superseded

## Organoid Formation Methods

### Forced Aggregation (Most Reproducible)

**Protocol:**
1. Dissociate CMs to single cells (day 15-20)
2. Count and resuspend: 5,000-50,000 cells/aggregate
3. Centrifuge into ultra-low attachment plates
4. Culture 3-7 days for aggregation
5. Optional: Add CF/EC during aggregation

**Advantages:** Consistent size, reproducible
**Limitations:** Labor-intensive, variable cell ratios

### Embryoid Body (EB) Method

**Protocol:**
1. Form EBs from iPSCs first
2. Apply cardiac differentiation to EBs
3. Self-organizing but heterogeneous

**Advantages:** Mimics development
**Limitations:** Variable efficiency, mixed cell types

### Self-Organizing Cardioids (Hofbauer Method)

**Protocol:**
1. Aggregate iPSCs (day 0)
2. Staged growth factor treatment
3. FGF + BMP + Activin → cardiac mesoderm
4. Allow self-organization 15+ days
5. Results in chamber-like cavities

**Advantages:** Physiologically relevant structure
**Limitations:** Complex, variable outcomes

### Scaffold-Based Approaches

**Hydrogels:**
- Collagen, fibrin, Matrigel, or synthetic
- Cells seeded into or onto matrix
- Better ECM context

**Decellularized Matrix:**
- Heart ECM from cadaveric tissue
- Most physiologically relevant
- Limited availability

## Maturation Strategies

### Electrical Pacing

**Parameters:**
- Frequency: 1-6 Hz (typically start 1 Hz, increase)
- Pulse duration: 2-10 ms
- Voltage: 3-5 V/cm
- Duration: 1-2 weeks

**Effects:**
- Improved sarcomere organization
- Enhanced calcium handling
- Better electrophysiology

**Equipment:** Commercial systems (IonOptix, Aurora) or custom

### Mechanical Stimulation

**Parameters:**
- Strain: 5-10% stretch
- Frequency: 1-2 Hz
- Duration: 1-2 weeks

**Effects:**
- Cardiomyocyte alignment
- Increased force generation
- Structural maturation

**Platforms:** Flexcell, custom PDMS devices

### Metabolic Maturation

**Fatty Acid Supplementation:**
- Switch from glucose to FA-rich media
- Oleic acid, palmitic acid, linoleic acid
- Typically 100-200 μM total FA
- Start after day 20

**Effects:**
- Metabolic switch to oxidative phosphorylation
- Mitochondrial maturation
- More adult-like energetics

### Hormonal Treatment

**Thyroid Hormone (T3):**
- 10-100 nM T3
- Promotes MYH6→MYH7 switch
- Enhances mitochondrial biogenesis

**Dexamethasone:**
- 100-1000 nM
- Promotes maturation markers
- Often combined with T3

### Combined Approaches

**Electromechanical (Most Effective):**
- Combines pacing + stretch
- Synergistic maturation effects
- Closest to adult phenotype

**Media + Physical:**
- Fatty acid media during pacing
- Additive benefits

## Assessment Methods

### Structural Analysis

**Immunofluorescence:**
- Sarcomere: α-actinin, cTnT
- T-tubules: caveolin-3, BIN1
- Gap junctions: Connexin-43
- Quantify: Sarcomere length, alignment index

**Electron Microscopy:**
- Ultrastructure details
- T-tubule presence
- Mitochondrial morphology

### Functional Analysis

**Calcium Imaging:**
- Fluo-4, Fura-2, GCaMP (genetic)
- Measure transient amplitude, kinetics
- Detect arrhythmias

**Optical Mapping:**
- Voltage-sensitive dyes
- Conduction velocity
- Action potential characteristics

**Force Measurement:**
- Engineered heart tissues on posts
- Direct force readout
- Contractility drug responses

**MEA (Multi-electrode Array):**
- Field potential recordings
- Beat rate, rhythm
- QT-like intervals

### Molecular Analysis

**qPCR Panel:**
- Maturation: MYH7/MYH6 ratio
- Ion channels: SCN5A, KCNJ2
- Metabolism: PPARGC1A, CPT1B

**RNA-seq:**
- Global expression profiles
- Compare to adult tissue
- Pathway analysis

## Common Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Low CM yield | CHIR timing/conc | Optimize CHIR window |
| No beating | Over-differentiation | Shorten CHIR duration |
| Irregular beating | Immature or sick cells | Check calcium handling |
| Organoids fall apart | Insufficient ECM | Add Matrigel or collagen |
| Variable size | Seeding inconsistency | Use counting chamber, verify counts |
| Poor maturation | Insufficient time/stimuli | Extend culture, add pacing |
