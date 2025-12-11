# Hypothesis Templates for Cardiac Organoid Research

## Template Categories

### 1. Mechanism Hypotheses
**Pattern**: "[Factor X] [affects/regulates/causes] [Outcome Y] via [Pathway Z]"

**Examples**:
- "AMPK activation improves cardiomyocyte maturation via enhanced fatty acid oxidation"
- "WNT inhibition timing controls chamber specification through HAND1 expression"
- "Endothelial co-culture enhances sarcomere organization via LAMA5 secretion"

**Experiment types**: Inhibitor studies, pathway reporters, knockdown

**Hackathon-friendly version**: Test if blocking Z prevents X from affecting Y

---

### 2. Optimization Hypotheses
**Pattern**: "[Increasing/decreasing] [Variable X] will [improve/enhance/accelerate] [Outcome Y]"

**Examples**:
- "Increasing mechanical load will accelerate contractile maturation"
- "Reducing glucose concentration will shift metabolism toward fatty acid oxidation"
- "Optimizing cell seeding density will improve organoid reproducibility"

**Experiment types**: Dose-response, titration, parameter sweeps

**Hackathon-friendly**: 3-5 conditions spanning a range, single timepoint readout

---

### 3. Comparison Hypotheses
**Pattern**: "[Method/Condition A] [outperforms/differs from] [Method/Condition B] for [Outcome Y]"

**Examples**:
- "Chemical pacing outperforms electrical pacing for calcium handling maturation"
- "RPMI+B27 produces more mature cardiomyocytes than DMEM+FBS"
- "Self-organizing organoids show different drug responses than engineered tissues"

**Experiment types**: Head-to-head comparison, parallel conditions

**Hackathon-friendly**: 2-3 conditions, same readout, direct comparison

---

### 4. Timing Hypotheses
**Pattern**: "[Factor X] must be applied during [Time Window W] to achieve [Outcome Y]"

**Examples**:
- "CHIR treatment must occur between day 0-1 for efficient mesoderm induction"
- "Fatty acid supplementation has maximal effect after day 15 of differentiation"
- "Calcium channel maturation requires >7 days post-replating"

**Experiment types**: Time-course, window experiments

**Hackathon-friendly**: Pre-treated cells at different timepoints, single readout

---

### 5. Combination Hypotheses
**Pattern**: "[X] + [Y] together produce [Effect Z] that neither produces alone"

**Examples**:
- "AMPK activation + ERR agonism synergistically enhance maturation"
- "Mechanical stretch + electrical pacing together exceed either alone"
- "Endothelial + fibroblast co-culture produces effects absent in either alone"

**Experiment types**: Factorial design (2x2), synergy analysis

**Hackathon-friendly**: 4 groups: control, X only, Y only, X+Y

---

### 6. Threshold Hypotheses
**Pattern**: "[Outcome Y] requires [Variable X] above/below [Threshold T]"

**Examples**:
- "Spontaneous beating requires cardiomyocyte density >1000 cells/mm²"
- "Drug responses emerge only above a maturation threshold (T-tubule index >0.5)"
- "Cardiotoxicity manifests at doxorubicin concentrations >100 nM"

**Experiment types**: Dose-response with threshold identification

**Hackathon-friendly**: 5-6 concentrations/densities, binary or continuous readout

---

### 7. Necessity vs Sufficiency Hypotheses
**Pattern**: "[X] is [necessary/sufficient/both] for [Outcome Y]"

**Examples**:
- "Vascularization is necessary but not sufficient for adult-level maturation"
- "HAND1 expression is sufficient to induce chamber-like morphology"
- "Fatty acid metabolism is necessary for contractile force generation"

**Experiment types**: Knockout/inhibition (necessity), overexpression/addition (sufficiency)

**Hackathon-friendly**: Inhibitor = tests necessity; adding factor = tests sufficiency

---

### 8. Rescue Hypotheses
**Pattern**: "[Intervention Z] rescues [Defect D] caused by [Perturbation P]"

**Examples**:
- "Omega-3 supplementation rescues diabetic embryonic cardiomyopathy phenotype"
- "ROCK inhibition rescues dissociation-induced cell death"
- "BET inhibitor rescues DSP cardiomyopathy contractile dysfunction"

**Experiment types**: Perturbation + rescue, 3-group minimum

**Hackathon-friendly**: Control, perturbation, perturbation+rescue

---

## Cardiac-Specific Hypothesis Areas

### Maturation
- Metabolic switch hypotheses (glucose → fatty acid)
- Structural maturation (sarcomere, T-tubule)
- Functional maturation (force, calcium, conduction)
- Transcriptomic maturation (fetal → adult gene program)

### Chamber Development
- Anterior-posterior patterning
- Left-right asymmetry
- Chamber-specific gene expression
- Cavity formation mechanisms

### Disease Modeling
- Patient-specific phenotype recapitulation
- Drug-induced cardiotoxicity
- Genetic mutation effects
- Environmental factor effects (diabetes, hypoxia)

### Drug Discovery
- Compound screening optimization
- Therapeutic rescue identification
- Toxicity prediction
- Mechanism of action studies

## Converting Gaps to Hypotheses

### From Lit Review Gap → Hypothesis

| Gap | Possible Hypotheses |
|-----|---------------------|
| "Maturation plateau at fetal stage" | "Extended AMPK activation breaks maturation plateau" |
| "No immune cell integration" | "Macrophage co-culture improves injury response modeling" |
| "Variable organoid morphology" | "Precise cell seeding density reduces morphological variation" |
| "Limited vascularization" | "VEGF timing controls vascular network formation efficiency" |
| "Poor adult drug responses" | "Maturation protocol X produces clinically predictive drug responses" |

### Making Hypotheses Testable

**Vague** → **Testable**

| Vague | Testable |
|-------|----------|
| "Maturation improves with X" | "X increases sarcomere length by >20% at 48h" |
| "Drug affects beating" | "Drug reduces beating rate by >30% at IC50" |
| "Cells respond differently" | "Response EC50 differs >2-fold between conditions" |
| "Morphology changes" | "Circularity index increases from <0.7 to >0.85" |

## Hypothesis Checklist

Before finalizing a hypothesis, verify:

- [ ] **Falsifiable**: Can be proven wrong with data
- [ ] **Specific**: Includes measurable outcome
- [ ] **Bounded**: Has defined conditions/timeframe
- [ ] **Novel**: Not already definitively answered
- [ ] **Feasible**: Can be tested with available resources
- [ ] **Impactful**: Answer matters to the field
