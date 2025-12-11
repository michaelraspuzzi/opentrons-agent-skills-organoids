# Hypothesis Generation Skill

## Overview

This skill transforms knowledge gaps from literature reviews into ranked, testable research hypotheses with complete experimental designs. Optimized for time-constrained settings like hackathons and workshops.

## Skill Structure

```
hypothesis-gen/
├── skill.md                            # Main skill definition with frontmatter
├── README.md                           # This file
└── references/
    ├── hackathon-constraints.md        # Equipment, time, reagent limits
    ├── hypothesis-templates.md         # Common hypothesis patterns
    ├── experimental-designs.md         # Opentrons-compatible assays
    └── evaluation-rubric.md            # Scoring criteria (5 dimensions)
```

## Installation

1. Download the entire `hypothesis-gen` folder
2. Zip the folder: `zip -r hypothesis-gen.zip hypothesis-gen/`
3. Upload to Claude as a skill

## Usage

The skill activates when you:

- Provide structured gap analysis from lit review
- Ask "generate hypotheses about [topic]"
- Describe a research question: "We don't know if X affects Y"
- Request experimental designs: "How can I test this in 24 hours?"

## Key Features

### 1. Constraint-Aware Design
- Always loads equipment/time constraints first
- Only proposes feasible experiments
- Flags resource conflicts

### 2. Multi-Mode Input
- **Mode 1**: Structured JSON from lit review skill
- **Mode 2**: Natural language descriptions
- **Mode 3**: Guided discovery (calls lit review skill)

### 3. Comprehensive Scoring
5-criterion evaluation rubric:
- **Novelty** (20%): How unexplored?
- **Feasibility** (30%): Can we do this?
- **Impact** (25%): Does it matter?
- **Clarity** (15%): Is it falsifiable?
- **Excitement** (10%): Is it compelling?

### 4. Ranked Output
- Top 3-5 hypotheses sorted by score
- Go/no-go recommendation for each
- Alternative strategies if top hypothesis fails

### 5. Protocol-Ready JSON
- Structured output feeds directly into opentrons-protocol-gen skill
- Includes experimental design, reagents, controls, success criteria

## Input Formats

### From Lit Review Skill
```json
{
  "knowledge_gaps": [
    {
      "gap_id": "gap_1",
      "description": "No immune cell integration in organoid models",
      "tractability": "high",
      "impact": "high",
      "suggested_approaches": ["macrophage co-culture", "cytokine treatment"]
    }
  ],
  "key_methods": [...],
  "key_papers": [...]
}
```

### Natural Language
```
User: "We don't know if inflammatory cytokines affect cardiac organoid calcium handling"

Skill:
1. Loads constraints
2. Generates hypothesis: "TNF-α treatment disrupts calcium transients in cardiac organoids within 24h"
3. Designs dose-response experiment
4. Scores and ranks
```

## Output Format

### Hypothesis Report
Each hypothesis includes:
- **Clear statement**: One falsifiable sentence
- **Rationale**: Why it matters (2-3 sentences)
- **Experimental design**: Groups, N, timeline, readouts
- **Success criterion**: What result supports/refutes
- **Risks**: What could go wrong
- **Go/No-Go decision**: ✅ ⚠️ ❌

### JSON for Protocol Skill
```json
{
  "selected_hypothesis": {...},
  "experimental_design": {
    "groups": [...],
    "plate_format": "96-well",
    "timeline_hours": 24,
    "readouts": [...]
  },
  "reagents_needed": [...],
  "controls": {...},
  "success_criteria": {...}
}
```

## Reference Materials

### hackathon-constraints.md
**Load first** for any hypothesis generation. Contains:
- Default 24h hackathon assumptions
- Equipment capabilities (Opentrons Flex modules)
- Cell types and reagents likely available
- Readouts achievable in timeframe
- What's feasible vs. not feasible

### hypothesis-templates.md
8 common patterns:
1. Mechanism (X causes Y via Z)
2. Optimization (changing X improves Y)
3. Comparison (A vs B for Y)
4. Timing (X during window W)
5. Combination (X+Y synergy)
6. Threshold (Y requires X > T)
7. Necessity/Sufficiency
8. Rescue (Z rescues defect D)

### experimental-designs.md
5 standard designs:
1. **Dose-response**: 6-8 concentrations, IC50 determination
2. **Time-course**: 4-6 timepoints, kinetics
3. **Factorial**: 2x2 combination/synergy
4. **Comparison**: Head-to-head, 2-4 conditions
5. **Mini-screen**: 20-30 compounds, single concentration

Plus readout protocols and Opentrons workflows.

### evaluation-rubric.md
Detailed scoring criteria:
- How to score each of 5 dimensions
- Example scored hypothesis
- Go/no-go decision framework
- Red flags that disqualify hypotheses
- Hackathon-specific weight adjustments

## Example Workflow

```
1. User completes lit review → identifies gap: "No immune-cardiac interaction studies"

2. User: "Generate hypotheses about immune effects on cardiac organoids"

3. Skill loads hackathon-constraints.md → sees 24h limit, Opentrons available, iPSC-CMs likely present

4. Skill generates 3 hypotheses:
   - Rank 1: TNF-α disrupts calcium handling (score 4.4)
   - Rank 2: Macrophage-conditioned media affects beating (score 4.1)
   - Rank 3: Doxorubicin dose-response validation (score 3.9)

5. Skill designs experiments for each using experimental-designs.md templates

6. Skill outputs hypothesis report + JSON for protocol generation

7. User selects Rank 1 → passes to opentrons-protocol-gen skill
```

## Integration with Other Skills

### Upstream (receives from):
- **lit-review**: Structured gap analysis as JSON input

### Downstream (sends to):
- **opentrons-protocol-gen**: Experimental design as JSON

## Quality Checklist

Before accepting hypothesis output:

- [ ] Constraints loaded (time, equipment, reagents)
- [ ] Each hypothesis is one falsifiable sentence
- [ ] Experimental design fits time constraint
- [ ] Controls specified (positive, negative, vehicle)
- [ ] Sample size realistic (N=3-6 per group)
- [ ] Success criteria quantitative (>20% change, p<0.05)
- [ ] Risks identified
- [ ] JSON output included

## Common Pitfalls Avoided

- ❌ Vague hypothesis → ✅ Specific, measurable outcome
- ❌ Too ambitious → ✅ Fits time constraint
- ❌ Missing controls → ✅ Vehicle + positive controls
- ❌ N=1 per group → ✅ N=4-6 minimum
- ❌ No success criterion → ✅ Quantitative threshold defined
- ❌ Ignoring feasibility → ✅ Equipment/reagent check
- ❌ Single hypothesis → ✅ Ranked alternatives + pivot plan

## Tips for Best Results

1. **Specify your constraints upfront**: "24h hackathon, Opentrons Flex, iPSC-CMs available"
2. **If unsure, let skill clarify**: It will ask about equipment/cells/time
3. **Consider complementary hypotheses**: Skill identifies backups if top choice fails
4. **Use scoring to justify decisions**: Quantitative rubric helps defend choices
5. **Trust the feasibility weighting**: It's 30% of score for a reason

## Version

- **Version**: 1.0
- **Last Updated**: 2025-12-11
- **Maintained by**: Cardiac Organoid Research Community

## License

Open for research and educational use.
