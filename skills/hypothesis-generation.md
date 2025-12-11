---
name: hypothesis-generation
description: Generate testable experimental hypotheses for cardiac organoid research. Takes research questions and outputs structured hypotheses with experimental designs, controls, and expected outcomes suitable for Opentrons automation.
---

# Hypothesis Generation for Cardiac Organoid Research

Generate testable experimental hypotheses from research questions, optimized for automated liquid handling.

## Input Modes

### Mode 1: Research Question
User provides a research question:
- "How does inflammation affect cardiac organoid function?"
- "What drugs protect against doxorubicin cardiotoxicity?"
- "Does hypoxia alter calcium handling in cardiomyocytes?"

### Mode 2: Drug/Compound Focus
User specifies compounds to test:
- "Test doxorubicin cardiotoxicity"
- "Evaluate TNF-α and IL-1β effects"
- "Screen these 10 compounds for cardioprotection"

### Mode 3: Phenotype Focus
User describes phenotype of interest:
- "Measure calcium transient changes"
- "Assess beating rate and contractility"
- "Evaluate cell viability and apoptosis"

## Output Format

```json
{
  "selected_hypothesis": {
    "id": "hyp_1",
    "statement": "Clear, testable hypothesis statement",
    "experiment_type": "dose_response|time_course|comparison|combination"
  },
  "experimental_design": {
    "groups": [
      {"name": "group_name", "treatment": "description", "n": 12}
    ],
    "plate_format": "96-well",
    "timeline_hours": 24,
    "readouts": [
      {"type": "plate_reader", "target": "calcium", "method": "Fluo-4 AM"}
    ]
  },
  "reagents_needed": [
    {"name": "reagent", "stock_conc": "10 mM", "working_conc": "10 µM"}
  ],
  "controls": {
    "negative": "Vehicle (media only)",
    "positive": "Known cardiotoxin or cardioprotectant"
  },
  "expected_outcomes": {
    "if_true": "Expected result if hypothesis is correct",
    "if_false": "Expected result if hypothesis is incorrect"
  }
}
```

## Experiment Types

### Dose-Response
- 5-8 concentrations (half-log or log spacing)
- Include vehicle control
- N=4-12 per concentration
- Ideal for IC50/EC50 determination

### Time Course
- Multiple timepoints (0, 6, 12, 24, 48h)
- Same treatment across timepoints
- Captures kinetic effects

### Comparison
- Multiple treatments at single concentration
- Head-to-head comparison
- Includes positive and negative controls

### Combination
- Drug combinations (synergy studies)
- Factorial design
- Includes single agents and combinations

## Quality Criteria

Good hypotheses should be:
- **Testable** in 24-48 hour timeframe
- **Measurable** with available plate reader assays
- **Relevant** to cardiac biology/toxicology
- **Automatable** on Opentrons Flex

## Common Readouts

| Readout | Method | Timepoint | Notes |
|---------|--------|-----------|-------|
| Calcium transients | Fluo-4 AM | Endpoint | 30 min load time |
| Cell viability | CellTiter-Glo | Endpoint | Luminescent |
| Apoptosis | Caspase-Glo | Endpoint | Luminescent |
| ROS | CellROX | Endpoint | Fluorescent |
| Mitochondria | TMRE | Endpoint | Fluorescent |

## Example Output

**Input:** "How does doxorubicin affect cardiac organoids?"

**Output:**
```json
{
  "selected_hypothesis": {
    "id": "hyp_1",
    "statement": "Doxorubicin induces dose-dependent cardiotoxicity in cardiac organoids, measurable through decreased calcium transient amplitude and reduced cell viability within 24 hours",
    "experiment_type": "dose_response"
  },
  "experimental_design": {
    "groups": [
      {"name": "vehicle", "treatment": "Media only", "n": 4},
      {"name": "dox_0.1", "treatment": "Doxorubicin 0.1 µM", "n": 4},
      {"name": "dox_0.3", "treatment": "Doxorubicin 0.3 µM", "n": 4},
      {"name": "dox_1", "treatment": "Doxorubicin 1 µM", "n": 4},
      {"name": "dox_3", "treatment": "Doxorubicin 3 µM", "n": 4},
      {"name": "dox_10", "treatment": "Doxorubicin 10 µM", "n": 4}
    ],
    "plate_format": "96-well",
    "timeline_hours": 24,
    "readouts": [
      {"type": "plate_reader", "target": "calcium", "method": "Fluo-4 AM"},
      {"type": "plate_reader", "target": "viability", "method": "CellTiter-Glo"}
    ]
  },
  "expected_outcomes": {
    "if_true": "IC50 between 0.5-3 µM, dose-dependent decrease in calcium amplitude",
    "if_false": "No concentration-dependent effect observed"
  }
}
```

## Handoff to Protocol Generation

Output JSON is designed to be directly consumed by the `opentrons-protocol-gen` skill for automated protocol creation.
