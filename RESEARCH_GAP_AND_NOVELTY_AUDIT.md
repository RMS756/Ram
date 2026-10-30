# Research Gap and Novelty Audit

Date: 27 Oct 2026. Inputs:
- Chapter 2 systematic review (`chapter2/CHAPTER2_SYSTEMATIC_REVIEW.md`, gap map `chapter2/CHAPTER2_RESEARCH_GAP_MAP.md`);
- prior-art reconciliation (`STAGE2_5_PRIOR_ART_RECONCILIATION.md`, `STAGE2_5_REM_VS_PRIOR_ART_MATRIX.md`, `STAGE3_PRIOR_ART_AND_POSITIONING.md`);
- Chapter 3 Table 3.16;
- the exploratory pilot (`EXPERIMENT_VALIDITY_REPORT.md`).

**Rule applied.** A claim of novelty survives only if:
1. no reviewed work already does the same thing; and
2. the claim is narrow enough to be checked against the review's search record.

Anything else is downgraded to "composition", "application" or "evidence". The review's corpus and search dates bound what "no reviewed work" means. A newer or unindexed work may exist, so every surviving claim carries the qualifier "among the works identified by the Chapter 2 search".

## 1. Mechanisms — none is novel

| Mechanism | Prior work | Verdict |
|---|---|---|
| Logistic regression; ridge penalty | Cox (1958); le Cessie & van Houwelingen (1992) | Not novel |
| Logistic calibration on the logit | Platt (1999/2000); Guo et al. (2017) | Not novel |
| Expected-cost decision | Elkan (2001) | Not novel |
| Reject/abstain option | Chow (1970) | Not novel (conceptual basis for Escalate only) |
| Linear Shapley attribution | Lundberg & Lee (2017) | Not novel; audit-only |
| CUSUM | Page (1954); Basseville & Nikiforov (1993) | Not novel; optional, observe-only |
| Argument provenance at the tool boundary | She et al. (2026), ProvenanceGuard | Not novel |
| Calibrated logistic risk score with a four-way intervention set | Hossain et al. (2026), NEXUS | Not novel as such |
| Runtime interception with a review verdict | C. Yang (2026), AgentTrust; H. Liu et al. (2026), SafeAgent | Not novel |
| Consequence-dependent control | H.-H. Chen (2026) | Not novel as a principle |

## 2. Candidate contributions after narrowing

| # | Claim as first phrased (rejected wording) | Narrowed claim | Status |
|---|---|---|---|
| C1 | "A novel cost-sensitive framework for agent security" | Per-step selection among four verdicts by minimizing conditional risk under a calibrated probability and *tier-indexed* losses, with a feasible verdict set and a dominance check, at the tool boundary of an *executing* financial agent | **Composition**, not a new method. The closest prior work (NEXUS) defines an expected-loss objective but deploys a rule cascade at plan level; the NEXUS reading rests on a Stage 1 analysis that could not be reproduced (OI-01). Survives as "a specified composition", qualified |
| C2 | "REM outperforms existing defenses" | — | **Rejected.** No shared evaluation exists with any system in §1. The pilot compares only with B1 (same estimator) and with recorded outcomes of four AgentDojo defenses, which is not a controlled comparison |
| C3 | "Calibration improves runtime security decisions" | — | **Rejected by the pilot.** Calibration produced no measurable gain (ECE 0.044 vs 0.042 uncalibrated) and did not repair miscalibration on an unseen attack category. Consistent with C. Zhang et al. (2026) |
| C4 | "Behavior-aware detection" (title wording) | Behavioral evidence is part of the specified evidence vector | **Weakened by the pilot.** The behavioral group lowered benign utility without a measured security benefit. The title's "behavior-aware" should be reviewed (TITLE decision) |
| C5 | "Evaluation protocol isolating the decision rule" | REM and B1 share estimator and calibration; nested grouped cross-fitting holds out whole attacker objectives; costs varied over a declared grid with misspecification | **Methodological contribution** (design of the evaluation), with precedent for grouped evaluation in Arp et al. (2022). Survives, qualified |
| C6 | — | Measured protection–utility trade-off of consequence-tiered verdicts, bounded between no reviewer and an oracle reviewer, on 6,762 real-agent steps | **Evidence contribution** (exploratory). Depends on SC-7 (replay out of scope) |
| C7 | — | The user_task_15 / attacker-IBAN collision in AgentDojo banking | **Not a contribution.** The collision exists in suite versions v1 and v1.1 and was changed upstream: from v1.1.1 the landlord IBAN is `CA133012400231215421872` (checked in the installed package, 27 Oct 2026). It matters to this pilot only because 16 of the 21 recorded backbones used the colliding prompt. It is reported as a validity issue of mixing recorded trace versions |

## 3. Gap statement (as supported)

Among the works identified by the Chapter 2 search, no system was found that combines:
- calibrated per-step probability estimation;
- declared consequence tiers;
- four-verdict expected-loss selection at the tool boundary of an executing financial agent;
- an evaluation against a same-estimator, consequence-independent baseline.

The gap is compositional and evaluative, not methodological. The pilot adds evidence that the composition behaves as designed, and that its practical value depends on two things the reviewed work also leaves open:
- how escalations are resolved;
- how decision costs are set.

## 4. Required follow-ups before submission

1. Re-run the Chapter 2 search to its cut-off date for newer runtime-agent-security work, and update §1.
2. Resolve OI-01 (NEXUS reading) or drop the comparison detail.
3. (Done) C7 was checked against later suite versions and found to have been fixed upstream in v1.1.1.
4. Settle the title wording ("behavior-aware") in view of C4.
