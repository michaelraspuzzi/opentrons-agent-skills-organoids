# Hypothesis Evaluation Rubric

## Scoring Overview

Each hypothesis is scored on 5 criteria. Final score = weighted average.

| Criterion | Weight | What It Measures |
|-----------|--------|------------------|
| Novelty | 20% | How new/unexplored is this question? |
| Feasibility | 30% | Can we actually test this with available resources? |
| Impact | 25% | Does the answer matter to the field/application? |
| Clarity | 15% | Is the hypothesis specific and falsifiable? |
| Excitement | 10% | Would this be compelling to present/publish? |

---

## Detailed Scoring Criteria

### Novelty (20%)

| Score | Description | Examples |
|-------|-------------|----------|
| 5 | No one has tested this; novel connection | "Does factor X affect cardiac organoids?" (X never studied in this context) |
| 4 | Tested in related system, not this one | "Does maturation approach from skeletal muscle work in cardiac?" |
| 3 | Partially explored, gaps remain | "Concentration range not fully characterized" |
| 2 | Well-studied, incremental question | "Does known drug work at slightly different concentration?" |
| 1 | Already definitively answered | "Does CHIR induce mesoderm?" (yes, established) |

**Questions to ask**:
- Has this exact question been published?
- Would the answer surprise experts?
- Does this challenge assumptions?

---

### Feasibility (30%) — HIGHEST WEIGHT

| Score | Description | Examples |
|-------|-------------|----------|
| 5 | Straightforward with available resources | "Drug treatment + viability readout" |
| 4 | Achievable but requires some optimization | "New staining protocol needs testing" |
| 3 | Possible but risky; may need troubleshooting | "siRNA knockdown in difficult cell type" |
| 2 | Ambitious; likely needs more time | "Multi-day treatment in 24h hackathon" |
| 1 | Not possible with current setup | "Requires equipment we don't have" |

**Feasibility checklist**:
- [ ] Cells available and ready?
- [ ] Reagents on hand?
- [ ] Equipment available?
- [ ] Timeline fits constraint?
- [ ] Expertise to troubleshoot?

---

### Impact (25%)

| Score | Description | Examples |
|-------|-------------|----------|
| 5 | Field-changing; would be published in top journal | "First demonstration of adult-level maturation" |
| 4 | Significant advance; strong publication | "New mechanism for known phenomenon" |
| 3 | Useful contribution; publishable | "Optimization that improves reproducibility" |
| 2 | Incremental; supplements existing work | "Confirmation of previous findings" |
| 1 | Limited interest outside this project | "Works only in our specific conditions" |

**Impact assessment**:
- Who would care about this result?
- Does it enable new experiments?
- Does it solve a practical problem?

---

### Clarity (15%)

| Score | Description | Examples |
|-------|-------------|----------|
| 5 | Crystal clear; single interpretation | "Drug X reduces beating rate by >30% at 10 µM within 6h" |
| 4 | Clear with minor ambiguity | "Drug X affects beating" (how much? what counts?) |
| 3 | Testable but needs refinement | "Maturation improves" (what metric?) |
| 2 | Vague; multiple interpretations | "Cells respond differently" |
| 1 | Not falsifiable | "System is complex" |

**Clarity checklist**:
- [ ] Specific outcome stated?
- [ ] Measurable endpoint defined?
- [ ] Success criterion quantified?
- [ ] Timeframe specified?

---

### Excitement (10%)

| Score | Description | Examples |
|-------|-------------|----------|
| 5 | Would make headlines; paradigm shift | "Organoids predict patient outcomes" |
| 4 | Impressive demo; great for presentations | "Live imaging of chamber formation" |
| 3 | Solid science; respectable | "Systematic optimization" |
| 2 | Necessary but boring | "Confirming reagent concentrations" |
| 1 | Tedious; no one wants to hear about it | "Failed replication attempt" |

**For hackathons especially**: Excitement matters for presentations and engagement.

---

## Scoring Calculation

### Example Scoring

**Hypothesis**: "AMPK activation (AICAR 1mM) increases cardiomyocyte sarcomere length by >20% within 24h"

| Criterion | Score | Reasoning |
|-----------|-------|-----------|
| Novelty | 4 | Tested in heart field but not this specific organoid system |
| Feasibility | 5 | Drug treatment + imaging, straightforward |
| Impact | 4 | Would validate maturation approach, publishable |
| Clarity | 5 | Specific drug, concentration, metric, timeframe |
| Excitement | 3 | Solid but not flashy |

**Calculation**:
- Novelty: 4 × 0.20 = 0.80
- Feasibility: 5 × 0.30 = 1.50
- Impact: 4 × 0.25 = 1.00
- Clarity: 5 × 0.15 = 0.75
- Excitement: 3 × 0.10 = 0.30

**Final Score**: 0.80 + 1.50 + 1.00 + 0.75 + 0.30 = **4.35/5.0**

---

## Go/No-Go Decision Framework

### ✅ Recommended (Score ≥ 3.5)
- Proceed with this hypothesis
- High confidence of success
- Worth the investment

### ⚠️ Conditional (Score 2.5-3.5)
- Proceed only if:
  - Top hypothesis fails
  - Have extra time
  - Specific concerns addressed
- List conditions for proceeding

### ❌ Not Recommended (Score < 2.5)
- Do not pursue
- Feasibility concerns dominate
- Better options available

---

## Red Flags (Automatic Downgrades)

These issues should lower feasibility to 2 or below regardless of other scores:

| Red Flag | Why It Matters |
|----------|----------------|
| Requires cells we don't have | Can't test without samples |
| Timeline exceeds available time | Won't finish |
| Critical reagent unavailable | Experiment won't work |
| No clear readout | Can't measure outcome |
| Requires expertise we lack | Can't troubleshoot |
| Ethical/safety concerns | Shouldn't proceed |

---

## Comparative Ranking

When ranking multiple hypotheses:

1. **Calculate scores** for all candidates
2. **Sort by total score** (highest first)
3. **Check for red flags** (eliminate if present)
4. **Consider complementarity**: Can Hypothesis 2 serve as backup if H1 fails?
5. **Assess resource conflicts**: Do they compete for same equipment/cells?

### Ranking Table Template

| Rank | Hypothesis | Nov | Feas | Imp | Clar | Exc | Total | Go/No-Go |
|------|------------|-----|------|-----|------|-----|-------|----------|
| 1 | [Name] | 4 | 5 | 4 | 5 | 3 | 4.35 | ✅ |
| 2 | [Name] | 5 | 4 | 4 | 4 | 4 | 4.15 | ✅ |
| 3 | [Name] | 3 | 3 | 5 | 3 | 4 | 3.55 | ⚠️ |
| 4 | [Name] | 5 | 2 | 4 | 4 | 5 | 3.55 | ❌ (feas) |

---

## Hackathon-Specific Adjustments

For 24-hour hackathons, weight feasibility even higher:

| Setting | Novelty | Feasibility | Impact | Clarity | Excitement |
|---------|---------|-------------|--------|---------|------------|
| Standard | 20% | 30% | 25% | 15% | 10% |
| Hackathon | 15% | 40% | 20% | 15% | 10% |
| Publication-focused | 25% | 20% | 30% | 15% | 10% |

**Hackathon mantra**: "Done is better than perfect. Feasibility is king."
