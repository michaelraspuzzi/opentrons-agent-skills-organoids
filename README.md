# Opentrons Agent Skills for Cardiac Organoid Research

**Complete AI-powered workflow: Literature Review → Hypothesis Generation → Protocol Generation**

This repository contains three interconnected Claude Skills that automate the entire research workflow from literature synthesis to executable Opentrons Flex protocols for cardiac organoid experiments.

## 🎯 What This Does

```
User: "Help me design a hackathon experiment on cardiac organoids"
                          ↓
[lit-review] → Synthesizes field knowledge, identifies gaps
                          ↓
[hypothesis-gen] → Generates ranked, testable hypotheses
                          ↓
[opentrons-protocol-gen] → Creates executable Python protocols
                          ↓
                 Ready-to-run protocol
```

## What's Here

```
skills/                              # Claude Skills (upload as ZIP files)
├── lit-review/
│   ├── skill.md                     # Systematic literature synthesis
│   └── references/                  # Field landscape, papers, methods, terminology
├── hypothesis-gen/
│   ├── skill.md                     # Hypothesis generation with scoring
│   └── references/                  # Constraints, templates, designs, rubric
└── opentrons-protocol-gen/
    ├── skill.md                     # Opentrons Flex protocol generation
    └── references/                  # Specs, templates, labware, examples

protocols/                           # Example protocols (debugging journey)
├── test-1-dox-dose-response.py     # First attempt (has bugs)
├── test-2-inflammatory-challenge.py # Second attempt (has bugs)
└── test-3-inflammatory-challenge-FIXED.py  # Fixed by Claude Code ✅

output/                              # Generated outputs & validation
├── skills-workflow-output.md        # Complete workflow example
├── simulator-output-test3.txt       # Successful simulation run
└── LLM-as-judge-perplexity.md      # External scientific validation ✅

SKILLS_SUMMARY.md                    # Complete documentation
validate_protocol.py                 # Simple validation script
```

## The Story

### 1. Skills Generate Complete Workflow

**lit-review skill** synthesizes cardiac organoid research:
- Loads field landscape (Mendjan, Aguirre, Mills/Hudson labs)
- Searches PubMed/bioRxiv with optimized queries
- Identifies knowledge gaps
- Outputs structured JSON for hypothesis generation

**hypothesis-gen skill** creates testable hypotheses:
- Loads hackathon constraints (24h, Opentrons available)
- Generates hypotheses using 8 templates
- Scores with 5-criterion rubric (Novelty, **Feasibility**, Impact, Clarity, Excitement)
- Designs Opentrons-compatible experiments
- Outputs JSON for protocol generation

**opentrons-protocol-gen skill** generates executable protocols:
- **Critical**: Automatic pipette selection validation
- Volume capacity checking (no overflow)
- Reagent calculations (overage + dead volume)
- Complete output: Python + plate map + reagent guide

### 2. External Validation: LLM-as-Judge

**Perplexity AI independently assessed the generated hypothesis** ([LLM-as-judge-perplexity.md](output/LLM-as-judge-perplexity.md)):

> **"This is not naive nonsense—it's a well-conceived experiment at the intersection of immunology and cardiac physiology, grounded in recent literature."**

Key findings:
- ✅ Immune-cardiac axis is a legitimate research frontier
- ✅ Cytokine-calcium disruption proven in 2D, logical next step in 3D organoids
- ✅ Pre-made organoids + calcium imaging = hackathon feasible
- ✅ Clinical relevance: HFpEF, myocarditis, drug screening

**Bottom line**: "For a freshman, this shows exceptional scientific maturity. I'd fund it."

### 3. Protocols Had Bugs

**Test 1 & 2** had critical issues:

| Issue | Problem | Impact |
|-------|---------|--------|
| 8-channel with individual wells | `plate['A1']` with 8-channel dispenses to A1-H1 | Wrong wells treated |
| Duplicate apiLevel | In both metadata and requirements | Protocol won't load |
| Missing trash bin | Flex requires explicit trash | Runtime error |

### 4. Claude Code Fixed Them

Using the Opentrons simulator (`opentrons_simulate`), Claude Code:
1. Identified all errors
2. Changed to single-channel pipette (correct for scattered wells)
3. Fixed apiLevel location
4. Added trash bin
5. Validated with simulator

**Test 3** passes simulation and is ready for hardware ✅

## Quick Start

### Upload the Skills

```bash
cd skills/

# Create ZIP files for upload to Claude
zip -r lit-review.zip lit-review/
zip -r hypothesis-gen.zip hypothesis-gen/
zip -r opentrons-protocol-gen.zip opentrons-protocol-gen/
```

Then upload each `.zip` file to Claude's Skills interface.

### Run the Workflow

```
User: "Get me up to speed on cardiac organoid maturation"
→ lit-review skill activates → provides field overview + gap analysis

User: "Generate hypotheses about improving maturation in 24 hours"
→ hypothesis-gen skill activates → ranks hypotheses with experimental designs

User: "Create Opentrons protocol for the top hypothesis"
→ opentrons-protocol-gen skill activates → generates Python + plate map + reagent guide
```

### Test with Simulator

```bash
# Setup (requires Python 3.10+)
python3.10 -m venv venv-opentrons
source venv-opentrons/bin/activate
pip install opentrons

# Test any protocol
opentrons_simulate protocols/test-3-inflammatory-challenge-FIXED.py
```

### Validate Your Own Protocols

```bash
python validate_protocol.py your_protocol.py
```

## Key Learnings

### Pipette Selection Rule

**The #1 most common error:**

```python
# 8-channel pipettes dispense to ENTIRE COLUMN (A-H)
# If your wells are scattered, use single-channel!

# ❌ WRONG - treats A1, B1, C1, D1, E1, F1, G1, H1
p8_channel.dispense(100, plate['A1'])

# ✅ CORRECT - treats only A1
p1_channel.dispense(100, plate['A1'])
```

**opentrons-protocol-gen skill automatically detects this** and selects the correct pipette.

### Flex Protocol Requirements

```python
# 1. apiLevel in requirements ONLY
metadata = {'protocolName': '...'}  # No apiLevel here!
requirements = {'robotType': 'Flex', 'apiLevel': '2.16'}

# 2. Load trash bin
trash = protocol.load_trash_bin('A3')

# 3. Use Flex-specific labware
tips = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'A1')
```

## Simulator Output (Test 3)

```
PHASE 1: INFLAMMATORY TREATMENT ADDITION
Adding Vehicle control (media) - Rows A-B, Cols 1-6
Picking up tip from A1 of Opentrons Flex 96 Tip Rack 1000 µL on slot A1
Aspirating 100.0 uL from A1 of NEST 12 Well Reservoir 15 mL on slot B1
Dispensing 100.0 uL into A1 of Corning 96 Well Plate 360 µL Flat on slot D1
...
TREATMENT ADDITION COMPLETE
Total wells treated: 72
...
FLUO-4 ADDITION COMPLETE
```

Full output in [output/simulator-output-test3.txt](output/simulator-output-test3.txt)

## Complete Workflow Example

See [output/skills-workflow-output.md](output/skills-workflow-output.md) for a full end-to-end example:
- Literature review on immune-cardiac interactions
- 4 ranked hypotheses with experimental designs
- Complete Opentrons protocol with plate layouts and reagent guide

## Documentation

- [SKILLS_SUMMARY.md](SKILLS_SUMMARY.md) - Complete skills documentation
- [skills/lit-review/README.md](skills/lit-review/README.md) - Literature review skill guide
- [skills/hypothesis-gen/README.md](skills/hypothesis-gen/README.md) - Hypothesis generation guide
- [skills/opentrons-protocol-gen/README.md](skills/opentrons-protocol-gen/README.md) - Protocol generation guide

## Credits

- **Mendjan Lab (IMBA Vienna)** - Cardioid development methods
- **Aguirre Lab (Michigan State)** - Self-assembling heart organoids
- **Mills/Hudson Lab (QIMR Berghofer)** - Maturation protocols
- **Opentrons** - Open-source liquid handling platform
- Skills created using [Claude Projects](https://claude.ai)
- Protocols debugged using [Claude Code](https://claude.ai/code)
- Scientific validation by Perplexity AI (LLM-as-judge)

## Build & Share

This is a community resource. Feel free to:

1. **Fork this repo** and adapt for your research area
2. **Add new skills** (e.g., data analysis, figure generation)
3. **Improve existing skills** (new reference files, better templates)
4. **Share your protocols** (add to protocols/ with your debugging journey)
5. **Report issues** or suggest improvements

No formal contribution process—just build and share!

---

**Built with Claude Skills • Debugged with Claude Code • Validated by LLM-as-Judge**

*Last Updated: 2025-12-11 • Version 1.0*
