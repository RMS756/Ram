# 14 Architecture selection decision (Phase 11)

The decision applies the rules frozen in `08` (commit `6705c07`) to the frozen results. Post-hoc material (`08a`) is reported but not used.

## 1. Security constraints S1–S5

Abbreviations: **viol.** = audited value/object violations released; **unauth.** = unauthorised proposals released; **amb.** = ambiguous proposals released.

| Candidate | S1: 0 attacks (primary, dev2, probe, H) | S2: 0 attack-labelled calls released | S3: viol. ≤ C1 (primary 11, dev2 0, H 0) | S4: suites 0 unauth. / 0 amb.; fixtures 0 unsafe | S5: scripted goals ≤ C1 in every order | Result |
|---|---|---|---|---|---|---|
| **REM-A** | yes | yes | yes (11 / 0 / 0) | yes | yes (0 / 0 / 0 / 0) | **passes** |
| **REM-B** | yes | yes | yes (11 / 0 / 0) | yes | yes (0 / 0 / 0 / 0) | **passes** |
| **REM-C** | yes | yes | **no** (121 / 24 / 0) | **no**: probes 1 unauth. + 3 amb.; diagnostics 16 unauth.; generalisation 4 unauth. + 4 amb.; 1 unsafe fixture | yes | **NO-GO** |
| REM-C-T | yes | yes | **no** (121 / 24 / 0) | **no**: probes 2 unauth. + 3 amb.; others as REM-C | yes | **NO-GO** |
| REM-C-raw | yes | yes | **no** | **no** | yes | **NO-GO** |
| REM-B-R (upper bound; not deployable) | yes | yes | **no** (121 / 24 / 0) | **no** | yes | not a candidate |

**Statistical caveat on "0 attacks".** Zero observed attacks is not zero risk. The one-sided 95% upper bounds are about 3/2,979 (primary), 3/2,065 (dev2) and 3/469 (H).

## 2. Frozen questions

| Question (from `08`) | Result | Basis |
|---|---|---|
| **Object binding (REM-B vs C1)** | **INCONCLUSIVE** | **Met:** on HO1–HO7, 0 unauthorised and 0 ambiguous released; scripted ut15×it4 goal in 0 of 4 orders (C1: 2 of 4). **Not met:** not every authorised proposal released; HO4 withheld by a designator defect (`08a`). |
| **Utility endpoint, REM-B vs C1 on H** | **INCONCLUSIVE** | +0.0077 [0.0000, 0.0205]; primary +0.0060, dev2 +0.0644 (both ≥ 0); the lower bound on H is not > 0. |
| **Utility endpoint, REM-A vs C1 on H** | **INCONCLUSIVE** | +0.0057 [0.0000, 0.0176] (3 gained, 0 lost); primary +0.0054, dev2 +0.0412. This endpoint was pre-specified for every candidate but omitted from the runner's contrast list; it was computed afterwards with the same data, eligibility rules and bootstrap (`experiments/architecture_redesign/endpoint_supplement.py`, `results/endpoint_supplement.json`, `logs/endpoint_supplement.log`). |
| **Learned component, REM-A vs REM-B** | **harmful / redundant** (not NULL: verdicts did change) | It withheld 3 / 49 / 1 audited-correct calls (primary / dev2 / H), and 7 authorised probe or diagnostic proposals. It produced no beneficial change and changed no attack outcome. |
| **Learned component, REM-C vs REM-B** | **harmful** (released 110 + 24 audited violations; unsafe suite releases), although it also gained tasks (+77 / +72 / +20) | The utility gain is bought with value-integrity violations. Positive contribution would require no offsetting harmful changes, which is not the case. |
| **Consequence-aware vs consequence-independent (REM-C vs REM-C-T)** | **not distinguishable** on all replay populations (identical verdicts) | On the probes, REM-C-T releases one more unauthorised proposal. |
| **Calibration (REM-C vs REM-C-raw)** | identical verdicts everywhere | The Platt step does not change any decision here. |

## 3. Selection

**Rule (frozen).** Among the candidates satisfying S1–S5, prefer the simplest (REM-B < REM-A < REM-C), unless a more complex one has a GO against it on the H utility endpoint. If the preferred candidate's utility endpoint vs C1 is not GO, report *preferred on security, utility INCONCLUSIVE*.

**Application:**
- REM-A and REM-B pass S1–S5.
- REM-A has no GO against REM-B: it is −0.0019 [−0.0061, 0.0000] on H.
- REM-B's endpoint vs C1 is INCONCLUSIVE.

### Decision: **REM-B, preferred on security; utility INCONCLUSIVE.**

| Architecture | Decision |
|---|---|
| REM-A (corrected original with learned stage everywhere) | **NOT SELECTED.** It passes security, but its learned stage only removes correct releases. |
| **REM-B** (authorisation-first, deterministic) | **SELECTED (preferred on security, utility INCONCLUSIVE).** |
| REM-C (hybrid) | **NO-GO** |
| Full Progent comparison | **NOT EXECUTED** |
| Live LLM evaluation | **NOT EXECUTED** |

## 4. What the decision does not mean
- **It does not change the approved REM design.**
  - The frozen REM v1.0 pipeline (ridge → Platt → expected loss → mitigation) remains the approved design.
  - REM-B is a `[PROPOSED - EXPLORATORY]` architecture.
  - Adopting it requires a supervisor decision (`15`, change proposal).
- **It does not claim that ML is useless in general.** In this setting the learned estimator is never reached by an attack-labelled call, and its target (malicious influence) differs from the decision's need (authorisation of a value). Another placement or target was not tested.
- **It does not claim superiority over Progent.**
- **It does not claim generalisation beyond AgentDojo banking.**
