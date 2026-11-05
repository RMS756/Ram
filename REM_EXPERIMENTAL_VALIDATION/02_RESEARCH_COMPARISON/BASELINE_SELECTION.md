# Baseline Selection

| Candidate | Selected? | Reason |
|---|---|---|
| **No Defense** | Yes | Reference for ASR and utility. Executed in Mode A; ready for Mode B |
| **MELON (official code)** | Yes, as the **external baseline**, Mode B only | Published at ICML 2025, evaluated on AgentDojo, with public code. Integrated without modifying its algorithm (two compatibility measures: injected embedding client and per-episode state reset). It cannot be evaluated on recorded traces, and its live execution is blocked (credential, network, spending). **No MELON number exists in this project**, and none is taken from the paper into a comparison table |
| **FinHarness** | **No** | No official implementation located. A re-implementation from the paper would be speculative, and the instruction forbids it. It is discussed in the literature comparison only |
| **REM-Lite** | Yes (ablation) | Same features and ridge model; uncalibrated probability; fixed thresholds selected on development data at the declared operating points (α_blk = 0.01, α_mod = 0.05); same predicates and mitigation. **Shown verdict-identical to the thesis's B1** (6,762/6,762 steps; 3,334/3,334 replay episodes), because threshold selection by ranking is invariant to the strictly increasing calibration map |
| **Full REM** | Yes | Frozen exploratory configuration (step-level mitigation, no reviewer) |
| Distributed AgentDojo defences (tool filter, spotlighting, repeat prompt, PI detector) | Context only | Their recorded outcomes are in thesis §4.11; they are not re-run |

**Identifier mapping:**

| Supervisors' design | This package | Thesis |
|---|---|---|
| B0 | No Defense | B0 |
| B1 | MELON | — (the thesis's B1 is the threshold baseline, which equals REM-Lite in effect) |
| B2 | Full REM | REM |
| B3 | REM-Lite | ≡ B1 (verdict-identical) |

**What the REM-Lite ablation isolates:** the combined contribution of {calibration + expected-loss decision with consequence tiers and the Escalate option}. Because calibration does not change rank-based thresholds, REM-Lite's verdicts equal B1's, which *keeps* calibration. The measured difference therefore comes from the decision rule (tier-indexed costs and the Escalate option), not from calibration. Calibration's separate effect is measured by the existing ablation "calibration removed" inside Full REM's expected-loss rule (thesis Table 4.12): observe-only intervention 0.973 / 0.213, against Full REM's 0.973 / 0.227.
