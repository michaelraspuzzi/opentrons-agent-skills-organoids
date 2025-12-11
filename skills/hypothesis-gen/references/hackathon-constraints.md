# Hackathon Constraints Reference

## Default Assumptions (24-Hour AI Science Hackathon)

If not specified, assume these constraints:

### Time
- **Total duration**: 24 hours
- **Setup time**: 2-4 hours (protocol development, reagent prep)
- **Experiment runtime**: 12-18 hours max
- **Analysis time**: 2-4 hours
- **Buffer**: Always reserve 2 hours for troubleshooting

### Equipment (Monomer Bio Setup)

**Opentrons Flex**
- 96-channel pipette (1-50 µL or 5-1000 µL)
- 8-channel pipette
- Single-channel pipette
- Deck positions: 12 slots
- Modules available:
  - Temperature module (4-95°C)
  - Heater-shaker (37°C incubation, 200-3000 rpm)
  - Magnetic module (bead-based assays)
  - Thermocycler (if PCR needed)

**Plate Reader** (assume basic)
- Absorbance: 340-850 nm
- Fluorescence: Ex 340-700, Em 400-850
- Luminescence
- 96-well and 384-well compatible

**Microscopy** (assume basic)
- Brightfield
- Phase contrast
- Fluorescence (DAPI, GFP, RFP channels)
- 4x, 10x, 20x objectives

**Incubator**
- 37°C, 5% CO2
- Humidified

### Cell Types Likely Available

**Standard lines**:
- HEK293T (easy to transfect)
- HeLa (robust)
- iPSCs (if cardiac focus)
- iPSC-derived cardiomyocytes (if pre-differentiated)

**Cardiac-specific** (may need to confirm):
- iPSC-CMs (cryopreserved or fresh)
- Cardiac fibroblasts
- Endothelial cells (HUVECs)

### Reagents Likely Available

**Culture basics**:
- DMEM, RPMI
- FBS, B27
- Pen/Strep
- TrypLE, Accutase
- Matrigel, fibronectin

**Assay reagents**:
- Viability: Calcein-AM, PI, Hoechst, MTT/XTT
- Calcium: Fluo-4, Fura-2
- ATP: CellTiter-Glo
- Apoptosis: Caspase substrates, Annexin V

**Small molecules** (check availability):
- CHIR99021 (Wnt activator)
- IWP2/IWR1 (Wnt inhibitor)
- ROCK inhibitor (Y-27632)
- Standard drugs for cardiotoxicity (doxorubicin, etc.)

### Readouts Achievable in 24 Hours

| Readout | Time Required | Equipment | Notes |
|---------|---------------|-----------|-------|
| Cell viability | 30 min - 2h | Plate reader | Calcein, MTT, ATP assays |
| Morphology | Minutes | Microscope | Brightfield/phase |
| Fluorescent staining | 1-4h | Microscope | Fixed or live |
| Calcium transients | 30 min | Plate reader/microscope | Requires loaded cells |
| Beating rate | Minutes | Microscope + video | iPSC-CMs only |
| Gene expression (qPCR) | 4-6h | Thermocycler | If RNA extraction available |
| Protein (Western) | 8-12h | Gel system | Tight timeline |
| ELISA | 4-6h | Plate reader | If kit available |

### What's NOT Feasible in 24 Hours

❌ **iPSC differentiation** (takes 7-15 days)
❌ **Organoid formation from scratch** (takes 3-10 days)
❌ **Stable cell line generation** (weeks)
❌ **In vivo experiments** (not a hackathon thing)
❌ **RNA-seq with analysis** (sample prep alone takes hours)
❌ **Long-term culture experiments** (>24h timepoints)
❌ **CRISPR knockouts** (need selection)

### What IS Feasible in 24 Hours

✅ **Drug treatments on existing cells** (dose-response, time-course)
✅ **Acute toxicity assays**
✅ **Calcium imaging on pre-made iPSC-CMs**
✅ **Beating analysis on pre-made organoids**
✅ **Staining and imaging** (IF, live dyes)
✅ **siRNA knockdown** (if cells transfect easily, 24-48h effect)
✅ **Small molecule screening** (focused library, ~20-50 compounds)
✅ **Co-culture setup and short-term analysis**
✅ **Media condition comparisons**
✅ **Automation protocol development**

## Adjusting Constraints

### If More Time (48-72h)
- Can include longer drug treatments
- Possible siRNA knockdown + readout
- More complex staining protocols
- Repeat experiments for statistics

### If Less Time (12h)
- Focus on imaging-based readouts
- Pre-plate cells before hackathon starts
- Use endpoint assays only
- Reduce group numbers

### If Equipment Limited
- No plate reader → microscopy-based readouts
- No fluorescence → brightfield morphology, beating rate
- No Opentrons → manual pipetting (reduce N)

## Pre-Hackathon Checklist

To maximize hackathon productivity:

- [ ] Cells plated 24-48h before event
- [ ] Reagents aliquoted and ready
- [ ] Opentrons protocols pre-tested
- [ ] Plate layouts designed
- [ ] Analysis scripts ready
- [ ] Backup hypothesis identified
