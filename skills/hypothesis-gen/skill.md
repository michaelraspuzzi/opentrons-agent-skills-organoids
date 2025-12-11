---
name: hypothesis-generation
description: Generate testable research hypotheses from literature review outputs or knowledge gaps. Designed for time-constrained settings like hackathons. Takes structured gap analysis and produces ranked hypotheses with experimental designs compatible with available equipment (Opentrons Flex, standard cell culture). Outputs feed directly into protocol generation workflows.
---

# Hypothesis Generation

Transform knowledge gaps into testable hypotheses with experimental designs. Optimized for hackathon/workshop constraints.

## Input Modes

### Mode 1: Structured Input (from lit review skill)
Accepts JSON with knowledge_gaps, key_methods, and key_papers:

```json
{
  "knowledge_gaps": [
    {
      "gap_id": "gap_1",
      "description": "...",
      "tractability": "high|medium|low",
      "impact": "high|medium|low",
      "suggested_approaches": ["..."]
    }
  ],
  "key_methods": [...],
  "key_papers": [...]
}
```

### Mode 2: Natural Language Input
User describes gaps or questions directly:
- "We don't know if X affects Y"
- "No one has tested whether..."
- "The field assumes X but hasn't proven it"

### Mode 3: Guided Discovery
If user says "generate hypotheses about [topic]":
1. Load lit review skill
2. Conduct gap analysis
3. Return here with structured input

## Hypothesis Generation Protocol

### Step 1: Load Constraints
**Always load** [references/hackathon-constraints.md](references/hackathon-constraints.md) first.
- What equipment is available?
- What cell types/reagents are on hand?
- What's the time limit?
- What readouts are possible?

If constraints unknown, ask:
> "What's your setup? I need to know: (1) time available, (2) equipment (Opentrons? plate reader? microscope?), (3) cells/reagents on hand."

### Step 2: Parse Knowledge Gaps
For each gap, extract:
- **What's unknown**: The specific question
- **Current evidence**: What's been tried, what failed
- **Why it matters**: Impact if solved
- **Suggested approaches**: From lit review or brainstorm

### Step 3: Generate Hypothesis Candidates
For each gap, generate 2-3 hypotheses using templates from [references/hypothesis-templates.md](references/hypothesis-templates.md):

**Mechanism hypotheses**: "X causes Y via Z pathway"
**Optimization hypotheses**: "Increasing/decreasing X will improve Y"
**Comparison hypotheses**: "Method A outperforms Method B for outcome Y"
**Timing hypotheses**: "X must occur during window W for effect Y"
**Combination hypotheses**: "X + Y together produce effect Z that neither produces alone"

### Step 4: Design Minimal Experiments
For each hypothesis, design the smallest experiment that could falsify it:

Use [references/experimental-designs.md](references/experimental-designs.md) for:
- Opentrons-compatible assays
- Readouts achievable in timeframe
- Positive/negative controls
- Sample sizes for statistical power

### Step 5: Score and Rank
Apply scoring rubric from [references/evaluation-rubric.md](references/evaluation-rubric.md):

| Criterion | Weight | Score 1-5 |
|-----------|--------|-----------|
| Novelty | 20% | How new is this question? |
| Feasibility | 30% | Can we actually do this? |
| Impact | 25% | Does answering this matter? |
| Clarity | 15% | Is the hypothesis falsifiable? |
| Excitement | 10% | Would this be fun/impressive? |

**Final Score** = Weighted average

### Step 6: Format Output
Use output template below. Include:
- Ranked hypotheses
- Go/no-go recommendation
- Experimental design summary
- JSON for protocol skill

## Output Format

```markdown
# Hypothesis Report: [Topic]

## Constraints Summary
- **Time**: [X hours]
- **Equipment**: [list]
- **Cells/Reagents**: [list]
- **Readouts available**: [list]

## Ranked Hypotheses

### Rank 1: [Hypothesis Title]
**Score**: [X/5.0]

**Hypothesis**: [One clear, falsifiable statement]

**Rationale**: [Why this matters, 2-3 sentences]

**Experimental Design**:
- **Groups**: [Control vs Treatment(s)]
- **N per group**: [number]
- **Timeline**: [hours breakdown]
- **Key readout**: [what you measure]
- **Success criterion**: [what result supports/refutes hypothesis]

**Risks**: [What could go wrong]

**Go/No-Go**: ✅ Recommended | ⚠️ Conditional | ❌ Not recommended

---

### Rank 2: [Hypothesis Title]
[...]

## Quick Comparison

| Rank | Hypothesis | Feasibility | Impact | Score |
|------|------------|-------------|--------|-------|
| 1 | [short name] | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 4.2 |
| 2 | [short name] | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 3.9 |
| 3 | [short name] | ⭐⭐⭐ | ⭐⭐⭐ | 3.1 |

## Recommended Path
[Which hypothesis to pursue and why]

## Alternative Strategies
[If top hypothesis fails, pivot to...]
```

## Structured Output for Protocol Skill

Append this JSON for handoff to Opentrons protocol generation:

```json
{
  "selected_hypothesis": {
    "id": "hyp_1",
    "statement": "[hypothesis text]",
    "experiment_type": "dose_response|time_course|comparison|combination"
  },
  "experimental_design": {
    "groups": [
      {"name": "control", "treatment": "none", "n": 3},
      {"name": "treatment_1", "treatment": "[description]", "n": 3}
    ],
    "plate_format": "96-well|24-well|6-well",
    "timeline_hours": 24,
    "timepoints": ["0h", "6h", "12h", "24h"],
    "readouts": [
      {"type": "imaging", "target": "viability", "method": "calcein/PI"},
      {"type": "plate_reader", "target": "absorbance", "wavelength": 450}
    ]
  },
  "reagents_needed": [
    {"name": "[reagent]", "concentration": "[conc]", "volume_total": "[vol]"}
  ],
  "controls": {
    "positive": "[description]",
    "negative": "[description]"
  },
  "success_criteria": {
    "metric": "[what you measure]",
    "threshold": "[what counts as significant]",
    "statistics": "t-test|ANOVA|Mann-Whitney"
  }
}
```

## Reference Materials

- **[references/hackathon-constraints.md](references/hackathon-constraints.md)**: Equipment, time, reagent limits — **LOAD FIRST**
- **[references/hypothesis-templates.md](references/hypothesis-templates.md)**: Common hypothesis patterns
- **[references/experimental-designs.md](references/experimental-designs.md)**: Opentrons-compatible assays
- **[references/evaluation-rubric.md](references/evaluation-rubric.md)**: Scoring criteria details

## Quality Checklist

Before finalizing:

- [ ] Loaded constraints (time, equipment, reagents)
- [ ] Each hypothesis is falsifiable in one sentence
- [ ] Experimental design fits time constraint
- [ ] Controls are specified
- [ ] Sample size is realistic
- [ ] Success criteria are quantitative
- [ ] Risks identified
- [ ] JSON output included for protocol skill

## Common Pitfalls

- **Hypothesis too vague**: "X affects Y" → "X increases Y by >20% at 24h"
- **Experiment too ambitious**: 24h hackathon ≠ 2-week experiment
- **Missing controls**: Every treatment needs a control
- **Underpowered**: N=1 per group won't show anything
- **No success criterion**: Define what "working" means before starting
- **Ignoring feasibility**: Cool hypothesis that can't be tested = useless
- **Single path thinking**: Always have a pivot plan
