# Heart Organoid Literature Review Skill

## Overview

This skill provides comprehensive literature review capabilities for cardiac organoid research. It guides systematic literature searches, synthesis, and gap analysis in the cardiac organoid field.

## Skill Structure

```
lit-review/
├── skill.md                            # Main skill definition with frontmatter
├── README.md                           # This file
└── references/
    ├── field-landscape.md              # Major labs, methodologies, debates
    ├── foundational-papers.md          # Key papers and timeline
    ├── methodology-guide.md            # Protocols and techniques
    ├── search-strategies.md            # Search query patterns
    └── terminology.md                  # Cell types, markers, readouts
```

## Installation

1. Download the entire `lit-review` folder
2. Zip the folder: `zip -r lit-review.zip lit-review/`
3. Upload to Claude as a skill

## Usage

The skill automatically activates when you ask questions like:

- "Get me up to speed on cardiac organoids"
- "What's new in cardiac maturation?"
- "Review approaches for vascularization"
- "What are the gaps in immune-cardiac interactions?"
- "Compare Mendjan vs Mills approaches"

## Key Features

### 1. Field-Aware Search
- Always loads field context first (field-landscape.md)
- Searches from 3 major lab groups (Mendjan, Aguirre, Mills/Hudson)
- Uses optimized search strategies for each topic

### 2. Structured Outputs
- Standard literature summary
- Methodology comparison
- Gap analysis
- JSON output for hypothesis generation

### 3. Access Strategies
- PMC fallback for paywalled papers
- bioRxiv preprint searching
- Institutional summaries when full text unavailable

### 4. Quality Control
- Checklist for review completeness
- Multiple source verification
- DOI verification
- Tractability ratings for gaps

## Reference Materials

### field-landscape.md
Load first for any review. Contains:
- Tier 1 labs (Mendjan, Aguirre, Mills/Hudson)
- Methodological camps (self-organizing vs directed assembly)
- Active debates (maturation, chamber formation, vascularization)
- Key journals and hot topics

### foundational-papers.md
Essential citations:
- Mills 2017 (metabolic maturation)
- Hofbauer 2021 (cardioids)
- Lewis-Israeli 2021 (self-assembling organoids)
- Recent breakthroughs (2023-2025)

### methodology-guide.md
Protocols and techniques:
- Differentiation protocols (Wnt modulation, GiWi)
- Organoid formation (forced aggregation, EB, cardioids)
- Maturation strategies (pacing, mechanical, metabolic)
- Assessment methods (calcium imaging, MEA, force)

### search-strategies.md
Optimized queries:
- 5-phase search sequence
- Lab-specific shortcuts
- Topic-specific patterns
- Full-text access fallback strategy

### terminology.md
Field vocabulary:
- Cell types (iPSC, CM, CF, EC)
- Markers (pluripotency, cardiac progenitor, maturity)
- Functional readouts (electrophysiology, calcium, contractility)
- Organoid types (spheroid, cardioid, heart-on-chip)

## Example Workflow

```
User: "Get me up to speed on cardiac organoid maturation"

Skill:
1. Loads field-landscape.md
2. Identifies Mills/Hudson lab as leader
3. Searches recent papers (2024-2025)
4. Loads methodology-guide.md for context
5. Synthesizes findings
6. Identifies gaps
7. Outputs structured summary + JSON
```

## Integration with Other Skills

This skill outputs structured JSON that feeds into:
- **hypothesis-generation**: Uses gaps and methods to generate testable hypotheses
- **opentrons-protocol-gen**: Uses protocols for method context

## Tips for Best Results

1. **Be specific about your goal**: "Review for hypothesis generation" vs "Review for learning"
2. **Specify time constraints**: "24hr hackathon" vs "No time limit"
3. **Mention available resources**: "We have iPSC-CMs" vs "Starting from scratch"
4. **Let the skill clarify**: If your request is vague, it will ask clarifying questions

## Version

- **Version**: 1.0
- **Last Updated**: 2025-12-11
- **Maintained by**: Cardiac Organoid Research Community

## License

Open for research and educational use.
