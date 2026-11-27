# 06: Final REM version selection

## 1. Candidates

| # | Candidate | Implemented? | Evaluated how |
|---|---|---|---|
| 1 | **REM v1.0 unchanged** | Yes (`rem/`, `configs/exploratory/pilot_e0.yaml`, `experiments/pilot/`) | NO-ADAPT replay on P1, P2, P3; offline classification; observe-only analysis; pre-registered ablation; **re-run in this audit** |
| 2 | REM v1.0 + a subset of REM-DiD (TAE authorization, field provenance, permits, behaviour rules) | Yes, as a separate package `REM_DEFENSE_IN_DEPTH/remdid/` | Exploratory replay (DiD-3) with **oracle** authorization; unit and scenario tests |
| 3 | REM v1.0 + a subset of REM-X | **No.** Design documents only | None |
| 4a | REM v1.1 (v1.0 without behavioural evidence) | Yes (same code, `no_beh` fit) | Confirmatory replay on unread P3 recordings (GO on utility); post-hoc evasion arm |
| 4b | Request-derived guards (G1, GV / HV, REM-B, REM-B2, REM-B3) | Yes, in `experiments/*` | Development replay, author-written probes. REM-B2 and REM-B3 were declared **NO-GO** by their own frozen criteria |

## 2. Assessment

| Criterion | 1 REM v1.0 | 2 v1.0 + REM-DiD subset | 3 v1.0 + REM-X | 4a REM v1.1 | 4b Request-derived guards |
|---|---|---|---|---|---|
| Scientific justification | Frozen design; the object of every comparison | Each component is adopted from prior art; the authorization depends on an **oracle** issuing channel that does not exist in the benchmark | None (design; D1 found unsafe and non-novel, Amendment 01) | One pre-declared modification, confirmed for utility | Best development results, but repeated held-out failures (intent compilation) |
| Implementation maturity | High; fail-closed; tested | Medium: new package; trusted issuance simulated | None | High (same code) | Medium: several revisions after external defect reports |
| Experimental support | Highest: three populations, pre-registered ablation, confirmatory base, fresh reproduction | Exploratory only; oracle; data used before | None | Confirmatory for utility; security unresolved; **loss of depth under modelled evasion (653 vs 90)** | Development data; no confirmatory run; NO-GO outcomes |
| Security effectiveness (replay) | 11 / 2,979 (P1); 3 / 2,065 (P3) | 0 attacks, **with oracle authorization**; not attributable to a realistic channel | — | 11 / 2,979; 1 / 2,065 | 0 on development data; held-out probe failures |
| Benign utility (replay) | 105 / 334 = **replay floor** (02 §1.3) | 173 / 334 with the oracle; 122 with explicit authorization | — | 140 / 334 (P1); 25 / 48 (P3) | Higher than REM in point estimate |
| Reproducibility | **Re-run identically** in this audit | Raw data stored; pinned | — | Stored results; protocol commit absent from this repository | Stored results |
| Architectural clarity | Clear, five layers | Adds an authorization record, permits and a ledger; more complex | — | Clear | Adds a compiler and an authority front |
| Complexity | Moderate | High | — | Lower | High |
| Defensibility in an examination | **High**, if presented as what it is (C1–C3 in 05) | Low: the examiner's question "who issues the authorization?" has no answer in the evaluation | None | Medium: a GO on utility, but the security depth question is open | Low to medium: NO-GO decisions are on record |

## 3. Recommendation

**Select candidate 1: REM v1.0, unchanged, as the final thesis artifact.**

**Exact version:**
- Code and configuration are identical in every commit from `7c79883` to `e50fbdd`. No commit touches them.
- Tree hashes:
  - `rem/` `cd11e3232071a4545e89d0259b75267c295aca5f`;
  - `configs/` `af409a442366a8a17f8f9077d7aadcd51171ccb5`;
  - `experiments/pilot/` `b05d33ae754416858b1051952c432cf0e0d72197`.
- Configuration `configs/exploratory/pilot_e0.yaml`, sha256 `8e1aa107…5e11d0`, matches the recorded provenance.
- The originating commit recorded in the results (`aa66f22`) is not in this repository's history.
- Inputs: AgentDojo 0.1.35; runs at `089ed468`.

**Components retained (all of REM v1.0):**
- provenance labelling;
- context evidence `x_ctx2`;
- behavioural evidence `x_beh1–4`;
- action evidence `x_act1–3`;
- ridge LR;
- Platt calibration on the logit;
- consequence tiers;
- predicates D1/D2;
- expected-loss verdict;
- step-level mitigation;
- audit record;
- CUSUM observe-only.

**Why nothing is removed:**
- Removing the components the ablation shows to have no effect would create a *new* version. That is a design change requiring a supervisor decision (CLAUDE.md change control), and it is not needed to establish the contribution.
- Their lack of effect **is the finding (C1)**. It is reported, not engineered away.

**Excluded from the final architecture** (they may be reported as exploratory analyses, clearly labelled):

| Excluded | Reason |
|---|---|
| REM v1.1 | Reported as the confirmed **utility** result of one modification. Not selected, because its security effect is unresolved and the post-hoc evasion arm suggests lost depth. Adoption remains a supervisor decision (thesis D-decision, already pending) |
| REM-DiD (`remdid/`) | Its authorization layer has no realistic issuer in the evaluation. Its replay numbers rest on an oracle. **DiD-1 and DiD-2, which analyse REM v1.0 itself, may stay as exploratory evidence about v1.0.** DiD-3 (the REM-DiD candidate) should appear, if at all, as future-work evidence, not as part of the thesis artifact |
| REM-X and Amendment 01 | No implementation, no evidence. At most one future-work paragraph |
| G1, GV/HV, REM-A/B/C, REM-B2/B3, C1 contracts, E1/E2, the authorization-generalization candidate | Exploratory development lines; several with NO-GO or INCONCLUSIVE decisions. **Their consistent finding** (learned stages add nothing behind deterministic authority; intent compilation fails on held-out probes) **may be cited as supporting evidence for C2 and C5.** They are not the artifact |

**Results supporting the decision (all verified in 02):**

| Result | Source |
|---|---|
| Fresh reproduction of REM v1.0 | 02 §1.1 |
| P1: 11 / 2,979 attacks; 105 / 334 benign | 02 §1.2 |
| P3: 3 / 2,065 attacks; 18 / 48 benign | 02 §1.2 |
| Ablation: identical episode sets across arms | 02 §1.2 |
| Confirmatory contrast | 02 §2 |

## 4. Limitations to acknowledge with this choice

1. **Replay only.** All security and utility outcomes are NO-ADAPT replays of recorded trajectories:
   - no live agent;
   - no adaptive attacker;
   - a refused call cannot redirect the agent.
2. **Benign utility equals the floor.** REM v1.0's benign completion on P1 equals that of withholding every state-changing call. REM completes **no** benign task that needs a write in P1. This is not stated explicitly in the defended thesis (02 §1.3).
3. **One benchmark, one domain.** AgentDojo banking v1: 16 user tasks, 9 injection tasks; 8 of the 9 injection tasks use one attacker IBAN. All residual attacks are one collision task.
4. **Exploratory design values.** Costs, tiers and thresholds come from the exploratory configuration. The result files carry the label "SUPERVISOR DECISION REQUIRED".
5. **Template-tuned detector.** `x_ctx2`'s patterns match the `important_instructions` template (`configs/exploratory/pilot_e0.yaml:94-97`). It had no outcome effect, so this does not inflate a result, but it must be disclosed.
6. **Pre-registration before 17 Nov not verifiable from this repository's git history.**

**Unresolved by this audit (supervisor decisions):**
- whether REM v1.1 is adopted;
- the title and topic wording (01 §2);
- which thesis edition (humanized or DiD) is the base for submission.
