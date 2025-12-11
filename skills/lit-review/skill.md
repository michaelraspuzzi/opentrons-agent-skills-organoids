---
name: heart-organoid-lit-review
description: Comprehensive literature review and synthesis for cardiac organoid research. Use when asked to review, summarize, or synthesize heart/cardiac organoid literature, iPSC-derived cardiomyocyte research, cardiac tissue engineering papers, organoid maturation techniques, disease modeling with cardiac organoids, drug screening applications, or identify research gaps in the cardiac organoid field. Produces structured outputs compatible with hypothesis generation workflows.
---

# Heart Organoid Literature Review

Systematic literature synthesis for the cardiac organoid field. This skill guides a complete review workflow from unstructured questions to structured, actionable outputs.

## Trigger Interpretation

Convert user input into an actionable review plan:

| User says | Review type | Action |
|-----------|-------------|--------|
| "Get me up to speed on cardiac organoids" | General overview | Load field-landscape.md → identify top 3-5 labs → find 2-3 recent papers each → synthesize |
| "What's new in [topic]?" | Topic deep-dive | Search "[topic] cardiac organoid 2024 2025" → focus on relevant labs from field-landscape.md |
| "Review maturation approaches" | Methodology comparison | Load methodology-guide.md → search comparison papers → use Methodology Comparison template |
| "Preparing for hackathon/workshop" | Practical protocol focus | Prioritize methods papers, recent protocols, equipment/reagent needs |
| "What are the gaps in [area]?" | Gap analysis | Search [area] + "limitations" + "challenges" → use Gap Analysis template |
| "Compare [X] vs [Y] approaches" | Head-to-head comparison | Search both, extract pros/cons, use Methodology Comparison template |
| "What's [Lab Name] working on?" | Lab-specific review | Search "[PI name] cardiac organoid" → find recent 3-5 papers → summarize focus |
| Vague/unclear request | Clarify first | Ask: "Are you looking for (a) general field overview, (b) specific topic deep-dive, (c) methodology comparison, or (d) gap analysis?" |

## Review Protocol (Follow These Steps)

### Step 1: Interpret and Scope
- Parse user request using Trigger Interpretation table above
- If unclear, ask ONE clarifying question
- Define: Topic? Time range? Depth needed?

### Step 2: Load Field Context
- **Always load** [references/field-landscape.md](references/field-landscape.md) first
- This provides: major labs, methodological camps, active debates, key journals
- Identify which labs/approaches are relevant to the query

### Step 3: Identify Key Sources (3-5 labs or 5-10 papers)
For lab-based reviews:
- Select 3-5 most relevant labs from field-landscape.md
- Search: "[PI name] cardiac organoid [topic] 2024 OR 2025"

For topic-based reviews:
- Search: "cardiac organoid [topic] review 2024"
- Search: "heart organoid [topic] site:pubmed.ncbi.nlm.nih.gov"

### Step 4: Retrieve Recent Publications (2-3 per lab or 5-10 total)
For each lab/topic:
1. Search for recent work (prioritize 2023-2025)
2. Note paper titles, authors, journals, DOIs
3. Attempt to fetch full text via web_fetch

**Access fallback strategy:**
- If journal paywalled → try PMC version (add "PMC" to search)
- If no PMC → try bioRxiv preprint version
- If no preprint → use PubMed abstract + search for institutional summaries
- If still blocked → note as "limited access" and find alternative papers

### Step 5: Extract Key Information
For each paper, extract:
- Main finding (1-2 sentences)
- Methodology used
- Disease/application if any
- Limitations acknowledged
- How it advances the field

### Step 6: Synthesize and Identify Gaps
- Group findings by theme
- Note contradictions or debates
- Identify at least 3 knowledge gaps
- Rate gaps by tractability and impact

### Step 7: Format Output
- Select appropriate template from Output Formats below
- Include structured JSON block for hypothesis skill handoff
- Verify all DOIs are complete

## Output Formats

### Standard Literature Summary
Use for general "what do we know about X" queries:

```markdown
# Literature Review: [Topic]

## Executive Summary
[2-3 sentences: current state, key consensus, major uncertainty]

## Key Findings

### [Theme 1]
[Finding with citation]
- Supporting evidence
- Contradicting evidence or limitations

### [Theme 2]
[...]

## Methodological Landscape
[Brief comparison of approaches used]

## Knowledge Gaps
1. [Gap 1]: [Why it matters] - Tractability: [High/Medium/Low]
2. [Gap 2]: [Why it matters] - Tractability: [High/Medium/Low]
3. [Gap 3]: [Why it matters] - Tractability: [High/Medium/Low]

## Suggested Next Steps
[For hypothesis generation]
```

### Methodology Comparison
Use when comparing protocols, techniques, or approaches:

```markdown
# Methodology Comparison: [Topic]

## Overview
[What's being compared and why]

## Comparison Matrix

| Approach | Lab/Source | Advantages | Limitations | Best For |
|----------|------------|------------|-------------|----------|
| [Method 1] | [Lab] | ... | ... | ... |
| [Method 2] | [Lab] | ... | ... | ... |

## Detailed Analysis
[Per-method breakdown with citations]

## Recommendations
[When to use which approach]
```

### Gap Analysis
Use when explicitly looking for research opportunities:

```markdown
# Research Gap Analysis: [Topic]

## Current State Summary
[What's established]

## Identified Gaps

### Gap 1: [Title]
- **What's missing**: [Description]
- **Why it matters**: [Impact]
- **Tractability**: [Easy/Medium/Hard]
- **Required resources**: [Equipment, expertise]
- **Relevant citations**: [Papers that hint at this gap]

### Gap 2: [Title]
[...]

## Prioritized Opportunities
[Ranked by impact × tractability]
```

## Structured Output for Hypothesis Skill

Always append this JSON block when review will feed into hypothesis generation:

```json
{
  "review_type": "summary|methodology|gap_analysis",
  "topic": "[specific topic]",
  "knowledge_gaps": [
    {
      "gap_id": "gap_1",
      "description": "[what's unknown]",
      "tractability": "high|medium|low",
      "impact": "high|medium|low",
      "suggested_approaches": ["approach 1", "approach 2"]
    }
  ],
  "key_methods": [
    {
      "name": "[method name]",
      "lab": "[originating lab]",
      "best_for": "[use case]",
      "limitations": "[key limitation]"
    }
  ],
  "key_papers": [
    {
      "citation": "[Author et al., Year]",
      "doi": "[DOI]",
      "relevance": "[why this matters]"
    }
  ]
}
```

## Reference Materials

Load these as needed:

- **[references/field-landscape.md](references/field-landscape.md)**: Major labs, methodological camps, debates, journals — **LOAD FIRST for any review**
- **[references/foundational-papers.md](references/foundational-papers.md)**: Landmark papers and timeline (load for historical context)
- **[references/terminology.md](references/terminology.md)**: Cell types, markers, readouts (load when clarifying terms)
- **[references/methodology-guide.md](references/methodology-guide.md)**: Protocols, maturation approaches (load for methods questions)
- **[references/search-strategies.md](references/search-strategies.md)**: Optimized search queries (load before intensive searching)

## Quality Checklist

Before finalizing any review:

- [ ] Loaded field-landscape.md for context
- [ ] Searched multiple sources (PubMed, bioRxiv, Google Scholar)
- [ ] Included papers from last 2 years
- [ ] Attempted full-text access with fallback strategy
- [ ] Noted contradictory findings
- [ ] Identified at least 3 knowledge gaps with tractability ratings
- [ ] Verified DOIs are complete and correct
- [ ] Included structured JSON block if for hypothesis generation

## Common Pitfalls

- **Starting searches without field context**: Always load field-landscape.md first
- **Giving up on paywalled papers**: Use the fallback strategy (PMC → bioRxiv → abstract)
- **Over-relying on reviews**: Primary research often contradicts review claims
- **Ignoring negative results**: Papers showing what doesn't work are valuable
- **Missing preprints**: Cutting-edge work appears on bioRxiv first
- **Conflating 2D and 3D**: iPSC-CM monolayers ≠ cardiac organoids
- **Skipping the JSON output**: Hypothesis skill needs structured data
