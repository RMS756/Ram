# REM authorization root-cause report (for the supervisors)

**Thesis:** Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents (Rawan Al-Lahham)

**Audit:** 8 November 2026, read-only on REM code. No model refit, no tuning, no change to defaults, no push.

**Scope of evidence:** offline recorded-trace replay (step level, NO-ADAPT) and synthetic call-level probes. No live agent and no MELON run.

## Executive summary

1. **The original results reproduce exactly.**
   - Recomputed from per-episode outcomes, original REM gives 11 / 2,979 successful attacks and 105 / 334 benign successes.
   - The refit reproduces the frozen model state byte for byte, and the frozen bundle `983c5b0d…` is unchanged.
2. **REM withholds legitimate payments mainly through an interaction of features and the declared cost grid, which the no-reviewer setting turns into non-execution.**
   - Under the declared costs, a transfer is allowed only if its calibrated probability is below 0.03 (≤ 1,000) or 0.015 (> 1,000).
   - The first transfer of an episode already scores about 0.03 from features that describe *being a payment* (privilege rise, repeated-call floor). It scores more after a file read, and much more when its arguments come from a document, as they do in 74% of the benchmark's legitimate transfers.
   - Escalate then withholds the call, because no reviewer exists.
3. **REM does not represent financial authorization.**
   - Its action evidence measures argument *provenance*.
   - It cannot tell a requested transfer from an unrequested transfer whose recipient and amount appear in the user's words.
   - It cannot tell an authorized amount from one the agent invents.
4. **One verified implementation defect was found (F-IMPL-1, comma-grouped decimals).**
   - It explains two probe outcomes. It does not occur anywhere in the evaluation corpus.
   - Correcting it is a design-controlled change, because it alters features and so requires a refit.
5. **Neither the parser nor gating is worth adopting.**
   - Gating's fixture failures are explained exactly by the mechanism in point 3.
   - The parser's reported corpus effect is not explained by the defect this audit found, and is statistically undetectable.

## Answers to the ten questions

**1. Why does the original REM withhold legitimate payments?**

Fold-0 trace of a legitimate first payment after a file read (`02_DECISION_TRACING/REM_DECISION_TRACE.csv`), using fold-0 coefficients:

| Logit term | Value |
|---|---|
| intercept | −5.643 |
| x_beh2 = 1/3 (always ≥ 1/3) | +0.428 |
| x_beh3 (privilege rise) | +1.534 |
| x_beh4 (`read_file → send_money` not in this fold's benign reference) | +1.049 |
| **logit s** | **−2.632** |

- Calibrated p = σ(0.959·s + 0.161) = **0.086**.
- At tier 3 the risks are: Allow = 10p = 0.86; Escalate = 0.30; Modify = 0.5(1−p) = 0.457; Block = 1−p = 0.914.
- Escalate has the lowest risk and is chosen. Under no reviewer it withholds the call.
- Without a preceding file read, p = 0.033, still above 0.03. With arguments copied from a document (x_act1, x_act2), p reaches 0.46–0.84.

At corpus level (observe mode, frozen fold scorers, `logs/corpus_diagnostics.json`):
- 95.5% of the 89 legitimate value transfers lie at or above their tier's Allow boundary.
- In replay, REM released 4 of 89 (B1: 51).

**2. Which layer contributes most directly?**
- **Layer 4 (Decision)**, through the declared cost ratio C_esc / C_miss, sets the very low Allow boundary.
- **Layers 2/3 (Detection, Behaviour)** place every first payment at or above it, by features that encode action type (x_beh3) and document-sourced arguments (x_act1, x_act2).
- **Layer 5** turns Escalate into non-execution, as specified, because no reviewer exists.
- There is no single-layer cause.
  - Removing the reviewer's absence restores benign successes to 166 / 334. That is the largest single lever, but it is an evaluation assumption, not a fix.
  - Removing x_beh3 and x_beh4 (gating) releases unsafe calls.

**3. Can the current features distinguish authorization from provenance?**
- **No.** No feature represents the requested operation or the mood of the request.
- R1/R2 (read-only requests) yield a `send_money` with exactly the feature vector of a legitimate payment.
- Logical case D ("show the payment details …") is identical to case A ("transfer …").

**4. Is the model overestimating transfer risk?**
- **Not established.** Calibration is good overall (pooled ECE 0.044, Brier 0.060).
- The reference labels define a legitimate transfer as one that is not an injection-task match. In this benchmark, legitimate transfers genuinely share most of their features with attacks (pattern beh3 + act1 + act2 is the most common in both).
- p ≈ 0.3 for such steps may well be calibrated. The model is not overconfident; it lacks separating evidence.

**5. Is the expected-loss rule producing excessive Escalate or Block decisions?**
- **Relative to the costs, no:** the argmin is exact, with 0 recomputation mismatches and 0 ties.
- **Relative to usability, yes:** 18% of all legitimate steps are escalated (1,049 / 5,777).
- With the declared C_esc = 0.3 and C_miss(3) = 10, escalation is optimal whenever p > 0.03. This is a **verified policy/utility trade-off** that follows from the declared exploratory costs (SD-1, not supervisor-approved).

**6. Does the mitigation implementation behave as specified?**
- **Yes.** Allow releases. Escalate withholds pending review. Block and Modify withhold only the current call at step level.
- The episode-level variant is separate and labelled.
- Escalate is never counted as Block (`02_DECISION_TRACING/REM_VERDICT_SEMANTICS.md`).

**7. Are there implementation bugs?**
- **One verified defect, F-IMPL-1:**
  - the number tokenizer (`rem/algorithms/context/provenance.py:123`) reads "1,312.40" as 1312, contrary to the declared value-matching rule;
  - it affects the probes SUB-A2 and P5 and no corpus text (0 / 825);
  - it is recorded as a strict xfail, not corrected.
- **No defect** was found in tier selection, cost ordering, calibration application, argmin, tie handling or mitigation.

**8. Are there conceptual limitations?**
Yes, five:
1. no authorization signal;
2. no argument-integrity comparison;
3. x_beh3 conflates "payment" with "escalation of privilege";
4. x_beh4 makes first-payment verdicts fold-dependent (folds 0–5 withhold, folds 6–8 sometimes release, including unsafe R2);
5. in this benchmark, legitimate payments are themselves document-driven, so provenance is a weak signal of attack.

**9. What can be resolved without changing the approved design?**
- Documentation and reporting: items M-1 to M-7, R-1 to R-6, D-1 to D-6 (`05_THESIS_REVISIONS/`).
- Reporting the idealized-reviewer bound beside the no-reviewer result.
- Reporting verdict types.
- Pinning the defect with a test, which is done.
- Nothing that changes a verdict can be done without a design decision.

**10. What requires supervisor approval?**
- Correcting F-IMPL-1, which needs a refit, a new bundle and a re-run.
- Any change to the costs, tiers or amount limit (SD-1). Note that tuning them on this corpus would be inadmissible.
- Any feature change (the cue, the parser, a redefinition of x_beh3 or x_beh4, or a new authorization feature).
- Introducing a review channel or user confirmation.
- Any authorization-aware design extension (section G).

## Findings by class

| ID | Finding | Class |
|---|---|---|
| F-IMPL-1 | Comma-grouped decimal tokenisation violates the declared numeric matching rule | **Verified implementation defect** (no corpus impact; probe impact) |
| F-FEAT-1 | No feature encodes action authorization; read-only-to-payment conversions are indistinguishable from authorized payments | **Verified feature limitation** |
| F-FEAT-2 | No argument-integrity check; an invented amount or recipient is not detected unless copied from untrusted text | **Verified feature limitation** |
| F-FEAT-3 | x_beh3 fires on 85% of legitimate and 84% of attack transfers (action-type proxy) | **Verified feature limitation** |
| F-FEAT-4 | First-payment verdict depends on the fold's benign reference (x_beh4) | **Verified feature limitation** |
| F-POL-1 | Allow requires p < C_esc / C_miss(k) = 0.03 / 0.015; with no reviewer, Escalate withholds; 4 / 89 legitimate transfers released | **Verified policy/utility trade-off** |
| F-POL-2 | With an idealized reviewer, benign successes reach 166 / 334 at unchanged attacks | **Verified policy/utility trade-off** (bound, not deployable) |
| H-1 | The cue had no effect because its information is redundant with x_act2 and is constant within user tasks | **Hypothesis requiring further testing** |
| H-2 | The parser's 6 recovered / 2 lost come from a code path other than comma-grouped decimals | **Hypothesis requiring further testing** (needs Codex's diff) |
| U-1 | How a runtime monitor without a structured intent channel can establish financial authorization | **Unresolved scientific issue** |

## Proposed corrective actions (none implemented)

| Action | Scientific justification | Expected impact | Risks | Design-lock change? | Retraining? | New independent data? |
|---|---|---|---|---|---|---|
| A1. Document limitations and report verdict types, the reviewer bound and the fixture counts | faithful reporting | none on results; clearer claims | none | No | No | No |
| A2. Correct F-IMPL-1 as a separately labelled system | implementation should match the declared rule | none on the corpus (0 affected texts) unless refitting shifts coefficients; fixes 2 probe cases | silently mixing fixed and unfixed results | **Yes** (feature values change) | Yes (refit, new bundle) | Recommended |
| A3. Supervisor-approved costs and tiers (SD-1), set *a priori* from financial policy, not tuned on this corpus | the Allow boundary is a direct function of the costs | could change the trade-off in either direction | tuning to the corpus is invalid; would need new data | **Yes** | No | **Yes** |
| A4. A review or confirmation channel, evaluated with a non-ideal reviewer model | Escalate is designed for review | recovers utility as far as reviewers are accurate | reviewer cost, latency, rubber-stamping | **Yes** (evaluation protocol; possibly architecture) | No | Yes (reviewer study) |
| A5. **Authorization-aware extension**: a deterministic, structured intent record supplied by the trusted user interface (operation, payee, amount, one-time) and checked for argument integrity at Layer 1/2 | separates authorization from provenance; addresses F-FEAT-1 and F-FEAT-2 at their source | could release authorized payments and catch unrequested or invented ones | needs a trusted intent channel, which AgentDojo lacks; may become a new architecture element; must not be an LLM judge | **Yes**: future research proposal only | Possibly (new feature) | **Yes**: new benchmark tasks with explicit intents |

The following are **not** recommended: gating (rejected); the request cue (no benefit); LLM-based authorization judging (forbidden by the design lock); lowering C_miss or raising C_esc on this corpus (data-dependent tuning).

## Recommendation

**Option 1 now: retain the current REM design and document its limitations.**
- No verdict-relevant implementation defect affects the evaluation corpus.
- The withholding of legitimate payments is a verified consequence of the frozen features, the declared costs and the no-reviewer assumption, not of an error.
- Every remedy that would change verdicts alters the scientific design.

**Option 3 as future work: present the authorization-aware extension (A5) to the supervisors as a separate proposal.**
- The core finding (provenance ≠ authorization) cannot be addressed by re-weighting the existing evidence. The gating experiment demonstrates this.

**Option 2 (correcting F-IMPL-1) is optional and should be decided explicitly.**
- It is a genuine defect but has no effect on the corpus.
- If approved, run it as a separately labelled, refitted system.
