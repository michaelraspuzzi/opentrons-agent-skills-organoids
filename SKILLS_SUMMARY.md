# Opentrons Cardiac Organoid Skills - Complete Package

## Overview

Three interconnected Claude skills for cardiac organoid research workflow:
**Literature Review → Hypothesis Generation → Protocol Generation**

---

## ✅ Skill 1: lit-review

**Purpose**: Systematic literature synthesis for cardiac organoid field

### Structure
```
lit-review/
├── skill.md                            # Main skill with frontmatter
├── README.md                           # Usage documentation
└── references/
    ├── field-landscape.md              # Major labs, debates, journals
    ├── foundational-papers.md          # Key papers (2017-2025)
    ├── methodology-guide.md            # Differentiation, maturation protocols
    ├── search-strategies.md            # Optimized PubMed/bioRxiv queries
    └── terminology.md                  # Cell types, markers, readouts
```

### Key Features
- Always loads field-landscape.md first (Mendjan, Aguirre, Mills/Hudson labs)
- 5-phase search strategy (context → lab-specific → topic → gaps → preprints)
- Fallback access strategy (PMC → bioRxiv → abstract)
- Outputs structured JSON for hypothesis-gen skill

### Triggers
- "Get me up to speed on cardiac organoids"
- "What's new in cardiac maturation?"
- "Review approaches for [topic]"
- "What are the gaps in [area]?"

---

## ✅ Skill 2: hypothesis-gen

**Purpose**: Transform knowledge gaps into ranked, testable hypotheses

### Structure
```
hypothesis-gen/
├── skill.md                            # Main skill with frontmatter
├── README.md                           # Usage documentation
└── references/
    ├── hackathon-constraints.md        # 24h hackathon defaults (Opentrons, cells, readouts)
    ├── hypothesis-templates.md         # 8 patterns (mechanism, optimization, comparison...)
    ├── experimental-designs.md         # 5 designs (dose-response, time-course, factorial...)
    └── evaluation-rubric.md            # 5-criterion scoring (novelty, feasibility, impact...)
```

### Key Features
- 5-criterion scoring rubric (Feasibility weighted 30% - highest)
- Hackathon-optimized (24h timeline, Opentrons-compatible)
- Opentrons-specific experimental designs
- Outputs JSON for protocol generation

### Triggers
- "Generate hypotheses about [topic]"
- "We don't know if X affects Y"
- Takes JSON from lit-review skill

---

## ✅ Skill 3: opentrons-protocol-gen

**Purpose**: Generate executable Opentrons Flex Python protocols

### Structure
```
opentrons-protocol-gen/
├── skill.md                            # Main skill with frontmatter
├── README.md                           # Usage documentation
└── references/
    ├── flex-specifications.md          # Deck layout, pipettes, modules (API 2.16)
    ├── protocol-templates.md           # 8 templates (serial dilution, washing, etc.)
    ├── labware-reference.md            # Plates, reservoirs, tips (Flex-specific)
    ├── liquid-handling-tips.md         # Pipette selection rules, volume validation
    └── example-protocols.md            # Complete working protocols
```

### Key Features
- **CRITICAL**: Automatic pipette selection validation
  - Single-channel for scattered wells or row-specific treatments
  - 8-channel only when ALL 8 rows get same treatment
  - 96-channel only for full-plate operations
- Volume capacity validation (no overflow, cumulative checks)
- Reagent calculations (overage + dead volume)
- Complete output package (Python + plate map + reagent guide)

### Triggers
- "Generate Opentrons protocol for [experiment]"
- "Set up dose-response with 8 concentrations"
- Takes JSON from hypothesis-gen skill

---

## Complete Workflow Example

```
┌─────────────────────────────────────────────────────────────────┐
│ USER: "Help me design a 24h hackathon experiment on cardiac    │
│        organoids. Focus on immune-cardiac interactions."        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ SKILL 1: lit-review                                             │
├─────────────────────────────────────────────────────────────────┤
│ 1. Loads field-landscape.md → identifies Mendjan, Aguirre,     │
│    Mills/Hudson as leaders                                      │
│ 2. Searches "cardiac organoid immune" + "macrophage heart"     │
│ 3. Identifies gap: "No immune cell integration in organoids"   │
│ 4. Outputs structured JSON:                                     │
│    {                                                             │
│      "knowledge_gaps": [                                         │
│        {                                                         │
│          "description": "No immune-cardiac crosstalk studies",  │
│          "tractability": "high",                                │
│          "impact": "high"                                        │
│        }                                                         │
│      ]                                                           │
│    }                                                             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ SKILL 2: hypothesis-gen                                         │
├─────────────────────────────────────────────────────────────────┤
│ 1. Loads hackathon-constraints.md → 24h, Opentrons available   │
│ 2. Generates 3 hypotheses:                                      │
│    Rank 1: "TNF-α disrupts calcium handling" (Score: 4.4/5.0)  │
│    Rank 2: "Macrophage-conditioned media affects beating"      │
│    Rank 3: "Doxorubicin dose-response validation"              │
│ 3. Designs experiment for Rank 1:                               │
│    - 5 groups: Vehicle, TNF 10, TNF 50, IL-1β 10, IL-1β 50    │
│    - N=12 per group                                             │
│    - Readout: Fluo-4 calcium imaging at 24h                     │
│ 4. Outputs JSON:                                                 │
│    {                                                             │
│      "experimental_design": {                                    │
│        "groups": [...],                                          │
│        "plate_format": "96-well",                               │
│        "timeline_hours": 24                                      │
│      }                                                           │
│    }                                                             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ SKILL 3: opentrons-protocol-gen                                 │
├─────────────────────────────────────────────────────────────────┤
│ 1. Loads flex-specifications.md                                 │
│ 2. Analyzes plate layout:                                       │
│    - Cols 1-6 rows A-B: Vehicle (12 wells)                     │
│    - Cols 7-12 rows A-B: TNF 10 ng/mL (12 wells)              │
│    - Cols 1-6 rows C-D: TNF 50 ng/mL (12 wells)               │
│    - Different rows within columns → USE SINGLE-CHANNEL         │
│ 3. Calculates volumes:                                          │
│    - 100 µL/well × 60 wells × 1.2 overage = 7,200 µL           │
│    - + 2 mL dead volume = 9.2 mL per treatment                  │
│ 4. Generates protocol:                                          │
│    - Python file with single-channel pipette                    │
│    - Plate map (markdown table)                                 │
│    - Reagent guide: "Load 9.2 mL vehicle in reservoir A1"      │
│ 5. Output: inflammatory_challenge.py (ready to run!)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Packaging for Upload

### Step 1: Create ZIP files

```bash
cd /Users/michaelraspuzzi/Documents/opentrons-cardiac/skills

# Package each skill
zip -r lit-review.zip lit-review/
zip -r hypothesis-gen.zip hypothesis-gen/
zip -r opentrons-protocol-gen.zip opentrons-protocol-gen/
```

### Step 2: Upload to Claude

1. Open Claude interface
2. Navigate to Skills section
3. Upload each .zip file individually:
   - lit-review.zip
   - hypothesis-gen.zip
   - opentrons-protocol-gen.zip

### Step 3: Test Workflow

```
User: "Get me up to speed on cardiac organoid maturation"
→ lit-review skill activates

User: "Generate hypotheses about improving maturation"
→ hypothesis-gen skill activates

User: "Create Opentrons protocol for the top hypothesis"
→ opentrons-protocol-gen skill activates
```

---

## Key Design Principles

### 1. Progressive Detail
- lit-review: Broad field understanding
- hypothesis-gen: Focused experimental question
- opentrons-protocol-gen: Exact implementation

### 2. Structured Handoffs
- Each skill outputs JSON for next skill
- No information loss between stages
- User can intervene at any stage

### 3. Safety-First
- opentrons-protocol-gen: Extensive validation before code generation
- Pipette selection, volume capacity, source volume checks
- Clear error messages if infeasible

### 4. Hackathon-Optimized
- All skills designed for 24h timeline
- Feasibility weighted heavily in scoring
- Only Opentrons-compatible designs suggested

### 5. Field-Specific
- Cardiac organoid-specific knowledge in lit-review
- Readouts specific to cardiac (calcium, beating, sarcomeres)
- Labs and methods from cardiac field

---

## Version History

- **v1.0** (2025-12-11): Initial release
  - 3 skills with complete reference libraries
  - Cardiac organoid focus
  - Opentrons Flex API 2.16 compatibility

---

## Maintenance Notes

### Updating lit-review
- Add new papers to foundational-papers.md
- Update field-landscape.md when new labs emerge
- Refresh hot topics annually

### Updating hypothesis-gen
- Adjust hackathon-constraints.md for different setups
- Add new experimental design templates as needed
- Revise evaluation rubric weights for different contexts

### Updating opentrons-protocol-gen
- Update flex-specifications.md if Opentrons releases new hardware
- Add new protocol templates for common operations
- Update labware-reference.md when new labware released

---

## Contact

Maintained by: Cardiac Organoid Research Community
Last Updated: 2025-12-11
License: Open for research and educational use
