# STAGE 3 — PRIOR-ART ANALYSIS AND POSITIONING

**Date:** 2026-09-19
**Baseline:** commit `f46c126`, working tree clean, 154/154 tests passing
**Nature:** analysis only. **No code, test or configuration was modified.**

---

# A. CURRENT-STATE AUDIT

## A.1 Repository state

| Item | State |
| ---- | ----- |
| HEAD | `f46c126` (Stage 2 audit) |
| Working tree | Clean (`git status --porcelain` empty) |
| Test suite | **154 collected / 154 executed / 154 passed / 0 failed / 0 skipped** |
| Composition | 43 frozen-math + 20 contract-compliance + 91 other |
| Source modules | 14 under `rem/` |
| Configuration | 7 files, 46 parameters — 27 FROZEN, 19 UNVERIFIED |
| Mathematical operations | 19, all cited, all `AWAITING REGISTRY ID` |

## A.2 What is implemented

| Layer | Component | Status |
| ----- | --------- | ------ |
| L1 Input & Context | Contracts + `Provenance` enum + `Evidence` type | Contracts only; **no feature extractor** |
| L2 Detection | `RidgeLogisticRegression` | **Implemented**; λ and feature set unresolved |
| L3 Behavioral Analysis | Contract only | **No algorithm** |
| cross-cutting | `PlattLogitCalibrator` | **Implemented** |
| L4 Decision Engine | `ExpectedLossDecisionEngine` | **Implemented**; loss grid and tiers unresolved |
| L5 Mitigation | `DeterministicMitigationEngine` | **Implemented**; Modify mechanism unresolved |
| audit-only | `LinearShapleyAttributor` | **Implemented** |

## A.3 §24 consistency audit — the `detect()` question

The instruction asks specifically whether any `detect()` uses a fixed threshold
such as 0.5 to determine the final verdict.

```console
$ grep -rn "def detect" rem/
rem/core/interfaces.py:196:    def detect(
rem/algorithms/detection/ridge_logistic.py:360:    def detect(...)

$ grep -rnE "(>=|>) *0\.5|0\.5 *(<=|<)" rem/
  NONE
```

`ridge_logistic.py:380` returns `label="unthresholded"`, with an inline comment
stating that the verdict comes from the expected-loss rule and that applying 0.5
would be an invented operating point.

> **FINDING: NO INCONSISTENCY.** The Detection Layer emits evidence (`s_t`,
> `p̃_t`) and no class decision. The Decision Engine determines the verdict.
> This already satisfies §8 and §24. The only `0.5` literals in `rem/` are the
> p50 percentile level and the ½ in `(λ/2)‖β‖²` — neither is a threshold.

## A.4 Consistency audit — remaining items

| Check | Finding |
| ----- | ------- |
| Five-layer architecture | ✅ `Layer.FROZEN_LAYERS` has exactly 5; no feedback member; test-enforced |
| Feedback treatment | ✅ No feedback layer, no `FeedbackSink`; test greps pipeline source |
| Calibration implementation | ✅ Platt-on-logit, smoothed targets verified verbatim against Platt (1999) |
| Decision policy | ✅ `argmin_v R_t(v)`; full risk table recorded; ties raise |
| Mitigation implementation | ✅ Canonical step-level semantics; mapping immutable |
| Feature definitions | ⚠️ **None exist** — `FeatureVector` is a contract only |
| Equation/implementation consistency | ✅ 19 operations, each carrying statement + citation |
| Threshold usage | ✅ No decision threshold anywhere |

## A.5 New information from this instruction

| Item | Previous status | Now |
| ---- | --------------- | --- |
| Project scope | UNVERIFIED (SD-5) | **Financial agent — stated explicitly in §27** |
| Feature set | UNVERIFIED | **Partially specified** — three conceptual groups (§7) |
| SHAP role | FROZEN audit-only | **Proposed downgrade to optional** — see §C.3 conflict |
| Validation source | Unresolved | FinVault **withdrawn**; alternatives named |
| Novelty basis | Implicit | **Explicitly integration/evaluation, not algorithmic** |

---

# B. VERIFIED PRIOR-ART ANALYSIS

## B.1 Citation verification

Every arXiv identifier supplied was checked this session. **All resolve to the
described work.** Titles and mechanisms below are as returned by the sources,
not from memory.

| Claimed ID | Resolves to | Verified |
| ---------- | ----------- | -------- |
| arXiv:2605.04785 | *AgentTrust: Runtime Safety Evaluation and Interception for AI Agent Tool Use* (Chenglin Yang, 6 May 2026) | ✅ |
| arXiv:2607.19356 | *NEXUS: Structured Runtime Safety for Tool-Using LLM Agents* | ✅ |
| arXiv:2608.05695 | *DreamGuard: Efficient Runtime Guardrail for LLM Agents via Risk-Aware World Model* | ✅ |
| arXiv:2605.27333 | *FinHarness: An Inline Lifecycle Safety Harness for Finance LLM Agents* (Jia, Liu, Chong et al., 26 May 2026) | ✅ |
| arXiv:2606.20746 | *Amplify, Don't Create: Temporal Accumulation for Slow-Burn Prompt Injection* (J. Alex Corll, 17 Jun 2026) | ✅ |
| arXiv:2606.21399 | *Calibration Is Not Control: Why LLM-Agent Oversight Needs Intervention* (Zhang, Wan, Yu et al., 19 Jun 2026) | ✅ |
| arXiv:2607.22868 | *What Can Be Enforced? A Theory of Certified Runtime Safety for Tool-Using Agents* (Shawn Ray, 24 Jul 2026) | ✅ |
| arXiv:2602.03117 | *AgentDyn: A Dynamic Open-Ended Benchmark for Evaluating Prompt Injection Attacks of Real-World Agent Security System* | ✅ |

**No citation in this analysis is fabricated.** Where a detail could not be
confirmed it is marked `NOT REPORTED` or `NOT INDEPENDENTLY VERIFIED`.

## B.2 What each verified work actually owns

### AgentTrust (arXiv:2605.04785)

Real-time interception evaluating each proposed action **before execution**,
returning a structured `TrustReport` with a **four-valued verdict: allow, warn,
block, review**. Components: shell deobfuscation normalizer, **SafeFix**
(safer-alternative suggestions), **RiskChain** (multi-step attack chains),
cache-aware LLM-as-Judge for ambiguous inputs. Ships an MCP server.

> **Collision severity: HIGH.** Owns pre-execution interception, four-valued
> verdicts, multi-step chain detection, and a Modify-equivalent (SafeFix).

### NEXUS (arXiv:2607.19356)

Structured-plan safety monitor applying a **formal intervention policy** over
**four actions: allow, block, request confirmation, request revision**.
Combines deterministic safety rules, argument-level inspection, and a
**Platt-scaled logistic-regression risk score** over a 9-dimensional plan
feature vector (plan length, irreversibility, per-category step counts,
sensitivity, cost, tool diversity, delete side-effect indicator). Reports
F1 0.949 and 4-class intervention accuracy 0.6406 on a 128-instance synthetic
benchmark. **Platt was selected over isotonic because it achieved the lowest
ECE and was less prone to overfitting on a small calibration split.**

> **Collision severity: CRITICAL — the closest work to REM.** NEXUS
> independently arrives at: calibrated logistic regression + rules +
> pre-execution inspection + four-action runtime intervention. Its four actions
> map almost exactly onto REM's Allow/Block/Escalate/Modify. Its feature vector
> already includes irreversibility and sensitivity — two of REM's proposed
> Group C features.

### DreamGuard (arXiv:2608.05695)

Proactive guardrail with a **risk-aware world model** maintaining a compact
**recurrent latent state** over the trajectory, predicting future latent states
to derive **immediate-hazard and prefix-risk** evidence. Fuses multi-horizon
signals into pre-execution intervention decisions. Four benchmarks plus online
evaluation; **25 ms average end-to-end latency per call**.

> **Collision severity: HIGH on trajectory-awareness.** Owns trajectory-aware
> *forward* risk estimation. Note its 25 ms latency sets a concrete comparator
> REM must be able to match or beat.

### FinHarness (arXiv:2605.27333)

Inline safety harness wrapping a finance agent end-to-end: **Query Monitor**
(single-turn intent + cross-turn drift), **Tool Monitor** (each prospective tool
call), **Cascade** (per-step risk integration, adaptive routing between
lightweight and advanced LLM judges). Fired risk factors are re-injected as
ex-ante evidence so the agent can refuse, re-plan or approve. Explicitly
motivated by needing to *simultaneously* block unauthorised actions and approve
legitimate multi-step business workflows.

> **Collision severity: CRITICAL on domain and evaluation.** Owns inline
> financial-agent security with per-step risk **and** the joint
> security/benign framing. REM cannot claim clause E.

### Corll, *Amplify, Don't Create* (arXiv:2606.20746)

Proxy-side temporal accumulator reducing **frozen per-event scores** to **peak
and CUSUM persistence statistics**, targeting attacks distributed across a
trajectory with each event below threshold. On concentrated attacks,
trajectory-level accumulation beats the per-event foil under a clustered
bootstrap (gap +0.092, 95% CI [+0.025, +0.155]); persistence and peak are
statistically tied.

> **Explicitly self-limited:** *"This is a boundary result, not a deployable
> detector."* Combined with the absence of a calibrated false-alarm criterion,
> **this is the one genuine opening REM has.**

### Calibration Is Not Control (arXiv:2606.21399)

Argues runtime oversight is commonly framed as scalar risk prediction —
estimate failure likelihood, intervene when it crosses a threshold — but the
relevant question is **whether an available intervention would improve the
outcome**. Central claim: *two trajectory prefixes can have the same risk
estimate while requiring different actions, because one remains recoverable and
the other does not.*

> **Dual significance — both threat and support.**
> **Threat:** REM must not present calibration quality as evidence of control
> quality, and must evaluate them separately.
> **Support:** REM's decision rule is *not* the scalar-threshold framing this
> paper criticises — `R_t(v)` is action-dependent, so different actions can win
> at identical `p_t` when `k_t` differs. **This is a direct argument for
> grounding the consequence tier `k_t` in recoverability/reversibility**, and
> Stage 2 had already flagged reversibility as a leading tier candidate.

### What Can Be Enforced? (arXiv:2607.22868)

Theory of certified runtime safety. Three results: (1) a deterministic gate
enforces exactly the nonempty safety policies whose good prefixes its register
model recognises, with nontriviality undecidable for two decrementable counters
but in PSPACE for a separable monotone fragment; (2) under a fixed exogenous
law, **Neyman-Pearson gives the exact false-block/miss frontier** and conformal
calibration gives a finite-sample marginal certificate; (3) **once blocking
changes future proposals, static scores and ungated trajectories need not
identify the closed-loop frontier.**

> **Result (3) is a serious methodological threat to REM's evaluation design.**
> REM fits on, and evaluates against, trajectories. If REM's own blocking alters
> subsequent agent behaviour, offline metrics computed on ungated trajectories
> do **not** identify closed-loop performance. This must be stated as a limitation
> and, where possible, addressed by an online/gated evaluation arm.
> Result (2) also means the operating-point baseline has a principled
> characterisation (Neyman-Pearson) rather than being arbitrary.

### Rule/policy and privilege systems

| System | What it owns |
| ------ | ------------ |
| **CaMeL** | Isolation via two LLM calls — a planner producing a data-flow graph from the user prompt alone, and an executor restricted to that graph |
| **Progent** | Per-agent privilege policy restricting which tools may be called and which argument values they may carry |
| **AgentSpec** | Rule-based monitor against interpretable safety constraints; manually engineered symbolic constraints |
| **GuardAgent** | Rule-based monitor; validator agent generating executable guards before tool calls |
| **ShieldAgent** | Markov logic networks — probabilistic rule-relevance evaluation |
| **LlamaFirewall** | Open-source guardrail system; Alignment Checking component for IPI |
| **ProbGuard / Pro2Guard** (arXiv:2508.00500) | Probabilistic runtime monitoring via probabilistic model checking; learned transition dynamics + verifiable safety properties |
| **PIGuard** | `NOT INDEPENDENTLY VERIFIED` in this session — no confirming source retrieved |

---

# F. PRIOR-ART COLLISION MATRIX

| Prior Work | What It Already Owns | What REM Must NOT Claim | Remaining REM Position |
| ---------- | -------------------- | ----------------------- | ---------------------- |
| **AgentTrust** (2605.04785) | Pre-execution runtime interception; four-valued verdict (allow/warn/block/review); SafeFix remediation; RiskChain multi-step detection; MCP integration | First runtime interception layer; first non-invasive layer; first four-valued policy; first Modify/remediation action; first multi-step monitor | REM's verdict set is *derived from expected loss*, not rule/judge assignment. The **derivation**, not the action set, is what differs |
| **NEXUS** (2607.19356) | Platt-calibrated logistic-regression risk score; deterministic rules; argument-level inspection; four-action intervention policy; plan features incl. irreversibility & sensitivity | First calibrated-LR runtime guard; first four-action intervention policy; novelty of Platt+LR; novelty of rules+LR composition | REM adds **explicit expected-loss decision theory with a consequence tier**, **sequential accumulation with a stated ARL**, and **execution-grounded financial validation**. NEXUS's benchmark is 128 synthetic instances |
| **DreamGuard** (2608.05695) | Trajectory-aware forward risk via recurrent world model; prefix-risk and immediate-hazard evidence; multi-horizon fusion; 25 ms latency | First trajectory-aware defense; novelty of prefix risk; novelty of proactive guardrails | REM is deliberately **non-recurrent and lightweight**; its sequential component is a stated-ARL change detector, not a learned world model. This is a *simplicity/auditability* position, not a capability claim |
| **FinHarness** (2605.27333) | Inline financial-agent security; per-step tool-call risk; cross-turn drift; joint block-unauthorised / approve-legitimate framing; cascade judging | First financial inline security harness; novelty of joint security+benign evaluation; novelty of per-step financial risk | REM's financial contribution must be the **decision-theoretic use** of financial risk (tier-indexed loss), not the fact of operating on financial agents |
| **Corll** (2606.20746) | CUSUM/peak temporal accumulation over frozen per-event scores for slow-burn injection; clustered-bootstrap evaluation | First CUSUM-based agent security method; novelty of temporal accumulation | **The strongest remaining opening.** Corll self-describes as a boundary result and lacks a calibrated false-alarm criterion. REM may claim a **stated ARL / false-alarm-controlled** sequential component — *if it is actually implemented and evaluated* |
| **Calibration Is Not Control** (2606.21399) | The calibration≠control insight; recoverability as decision-relevant; critique of threshold-on-risk oversight | That good calibration demonstrates good control; that separating them is REM's insight | REM must **cite this as motivation** for separating Q1/Q2/Q3 and for grounding `k_t` in recoverability. Supports REM's action-dependent loss over thresholding |
| **What Can Be Enforced?** (2607.22868) | Theory of enforceable policies; Neyman-Pearson false-block/miss frontier; conformal certificates; closed-loop identifiability limits | That REM's guarantees are novel; that offline metrics identify closed-loop performance | REM must **adopt its caveat** as a stated limitation and use N-P to characterise the threshold baseline |
| **CaMeL** | Planner/executor isolation via data-flow graph | First data-flow-constrained agent execution | REM does not isolate execution; complementary, not competing |
| **Progent** | Per-agent privilege policy over tools and argument values | First privilege/tool-restriction control | REM's Modify/Block are step-level, not policy-persistent |
| **AgentSpec** | Interpretable symbolic safety constraints | First rule-based agent monitor | REM's rules (if any) are evidence, not the verdict |
| **ShieldAgent** | Markov logic networks for probabilistic rule relevance | First probabilistic rule evaluation | REM's probability is a calibrated posterior, used in expected loss |
| **GuardAgent** | Validator agent generating executable guards | First guard-generation approach | Not a REM mechanism |
| **LlamaFirewall** | Open-source guardrail, alignment checking | First open guardrail system | REM may *use* such a component as a feature extractor |
| **ProbGuard** (2508.00500) | Probabilistic model checking; learned transition dynamics; verifiable properties | First probabilistic runtime monitor; first proactive probabilistic enforcement | REM makes no verification claim |

---

# I. FINAL CAUTIOUS RESEARCH-GAP STATEMENT

## I.1 Assessment of the proposed conjunction A ∧ B ∧ C ∧ D ∧ E

§3 asks whether the conjunction remains defensible and instructs that it be
**weakened rather than forced** if evidence invalidates it. The evidence
requires weakening.

| Clause | Verified status | Verdict |
| ------ | --------------- | ------- |
| **A** — calibrated adversarial-induction probability from context + behavioural/action evidence | **NEXUS owns this directly** (Platt-scaled LR over plan features incl. irreversibility, sensitivity) | ❌ **Not available** |
| **B** — explicit consequence-tiered expected-loss decision over 4 actions | NEXUS owns four-action *formal intervention policy*; AgentTrust owns four-valued verdicts. **No verified work derives the action from a tier-indexed expected-loss minimisation** | ⚠️ **Partially available** — the *derivation* and the *tier index*, not the action set |
| **C** — sequential accumulation with explicit false-alarm criterion / ARL | Corll owns CUSUM accumulation but **explicitly lacks a calibrated false-alarm criterion and self-describes as a boundary result** | ✅ **Available — strongest clause** |
| **D** — per-factor attribution | For a linear model this reduces to coefficient × centred feature. The instruction itself concedes this adds little | ❌ **Not a contribution** |
| **E** — execution-grounded financial validation with benign set, joint security+utility+latency | **FinHarness owns this directly** | ❌ **Not available** |

**Three of five clauses are unavailable as contributions.** A conjunction
asserted over A–E would not survive examination.

## I.2 Recommended gap statement

> REM composes established runtime-security mechanisms — rule/evidence
> extraction, ridge logistic regression, Platt calibration, and step-level
> mitigation — into a financial-agent runtime layer whose distinguishing
> property is **how the intervention is chosen rather than which interventions
> exist**: the action is selected by minimising a consequence-tiered expected
> loss over a calibrated posterior, and the sequential component is operated
> under an explicitly stated false-alarm criterion (ARL).
>
> No individual mechanism is claimed as new. Calibrated logistic regression with
> four-action intervention is established by NEXUS; four-valued pre-execution
> interception with remediation by AgentTrust; trajectory-aware risk by
> DreamGuard; inline financial security with joint security/benign evaluation by
> FinHarness; and CUSUM-style temporal accumulation by Corll.
>
> The contribution is therefore **integration and evaluation**, specifically:
> (i) making the intervention decision explicitly decision-theoretic and
> consequence-tiered rather than rule- or threshold-assigned; (ii) supplying the
> calibrated false-alarm criterion that Corll's temporal accumulation explicitly
> lacks; and (iii) reporting risk estimation, decision quality, and mitigation
> effectiveness as **three separately measured questions** rather than one
> aggregate score, as motivated by *Calibration Is Not Control*.

## I.3 Honest statement of weakness

Two caveats must appear in the thesis:

1. **REM's closest neighbour is NEXUS**, which already couples Platt-calibrated
   LR with four-action intervention and rules. REM's separation from NEXUS rests
   on the *decision-theoretic derivation*, the *consequence tier*, the *ARL-
   controlled sequential component*, and *execution-grounded financial
   validation* — not on the estimator or the action set. If the expected-loss
   layer and the ARL component are not both implemented and evaluated, **the
   remaining distance from NEXUS is small.**
2. **Closed-loop identifiability** (*What Can Be Enforced?*, result 3): because
   REM's blocking changes subsequent agent behaviour, offline metrics on ungated
   trajectories do not identify closed-loop performance. This bounds what any
   offline result can claim.

---

# §22. MUST NOT CLAIM

REM must **NOT** claim to be:

| # | Prohibited claim | Owned by |
| - | ---------------- | -------- |
| 1 | First runtime interception layer | AgentTrust (2605.04785) |
| 2 | First non-invasive agent security layer | AgentTrust; NEXUS |
| 3 | First multi-step security monitor | AgentTrust (RiskChain); FinHarness |
| 4 | First four-valued intervention policy | AgentTrust; NEXUS |
| 5 | First Modify / SafeFix action | AgentTrust (SafeFix) |
| 6 | First calibrated logistic-regression runtime guard | **NEXUS (2607.19356)** |
| 7 | First trajectory-aware agent defense | DreamGuard (2608.05695) |
| 8 | First financial inline security harness | FinHarness (2605.27333) |
| 9 | First CUSUM-based agent security method | Corll (2606.20746) |
| 10 | Novel use of Platt scaling | Platt (1999); NEXUS |
| 11 | Novel use of expected-loss decision theory | Elkan (2001); Chow (1970) |
| 12 | Novel SHAP/attribution method | Lundberg & Lee (2017); reduces to linear coefficients |
| 13 | That calibration quality demonstrates control quality | Refuted by 2606.21399 |
| 14 | Offline results identify closed-loop performance | Refuted by 2607.22868 result 3 |
| 15 | Novel prompt-injection detector | Uses an existing extractor as a fixed feature |
| 16 | "First", "novel", "unique", "no prior work" in any form without direct primary-source evidence | — |

---

# CONFLICTS WITH `CLAUDE.md` — CHANGE CONTROL REQUIRED

`CLAUDE.md` § CHANGE CONTROL forbids changing a FROZEN item during
implementation and requires that conflicts be stopped, quoted, explained and
marked. Three conflicts arise from this instruction.

## ⚠️ CONFLICT 1 — Beta calibration

**Instruction §11:** *"Investigate: Platt scaling, Beta calibration. Use evidence
to select the final approach."*

**`CLAUDE.md` § FORBIDDEN REINTRODUCTIONS:** *"beta calibration as the adopted
calibrator"* is explicitly removed.

**Consequence:** Beta calibration may be **discussed** in Chapter 2, but
**adopting** it would violate the lock. Relevant evidence: NEXUS selected Platt
over isotonic *because it achieved the lowest ECE and was less prone to
overfitting on a small calibration split* — a directly analogous situation.

**[SUPERVISOR DECISION REQUIRED]** — keep Platt (lock-compliant, and
independently corroborated by NEXUS's finding), or formally amend the lock.

## ⚠️ CONFLICT 2 — CUSUM in configuration C4

**Instruction §15:** configuration **C4 = C2 + CUSUM / Sequential Change
Detection with explicit false-alarm criterion**, to be evaluated as a candidate
final configuration.

**`CLAUDE.md` § FROZEN REM PIPELINE:** *"CUSUM is OPTIONAL and OBSERVE-ONLY.
CUSUM MUST NOT enter the core verdict path."* § FORBIDDEN REINTRODUCTIONS also
bars *"risk-based CUSUM"*.

**Consequence — and this is the pivotal one:** clause C is REM's **strongest
remaining contribution**, but under the current lock CUSUM cannot influence the
verdict. Two lock-compatible readings:

| Reading | Lock-compatible? | Contribution value |
| ------- | ---------------- | ------------------ |
| CUSUM statistic becomes an **evidence feature in `x_t`**, so it influences the verdict only through the calibrated posterior | ✅ Arguably yes — it is evidence, not a decision component | Moderate — still delivers the stated ARL that Corll lacks |
| CUSUM **gates or overrides** the verdict | ❌ No — this is CUSUM in the verdict path | Higher, but forbidden |
| CUSUM is **observe-only**, reported but never affecting anything | ✅ Yes, unambiguously | **Low — cannot support the clause-C claim** |

**[SUPERVISOR DECISION REQUIRED]** — REM's best available contribution and the
CUSUM lock are in tension. Reading 1 is the recommended compromise, but it
changes the meaning of "observe-only" and therefore needs explicit approval.

## ⚠️ CONFLICT 3 — SHAP status downgrade

**Instruction §14:** SHAP should be **optional supplementary analysis**, not core.

**`CLAUDE.md` § MATHEMATICAL LOCK:** *"Linear Shapley attribution is audit-only.
It MUST NOT affect the verdict."*

**Consequence:** "Audit-only" and "optional" are not the same status.
Audit-only is frozen and currently implemented; making it optional is a
*downgrade* of a frozen item. The instruction's technical premise is correct —
for a linear model `φᵢ = βᵢ(xᵢ − E[xᵢ])` is coefficient × centred feature — and
Stage 2 already recorded that it must not be claimed as novel.

**[SUPERVISOR DECISION REQUIRED]** — retain as frozen audit-only (no code
change, zero risk), or formally downgrade to optional. **Recommendation: retain.**
It is already implemented, costs `O(d)`, and removing it gains nothing.

## Non-conflicts confirmed

| Instruction | Lock | Status |
| ----------- | ---- | ------ |
| §1 five layers, feedback cross-cutting/offline | Identical | ✅ Consistent |
| §8 no 0.5 threshold in Detection | Consistent | ✅ Already implemented |
| §10 standard logistic regression, no REM-specific equation | Ridge LR *is* standard L2-penalised LR | ✅ Consistent |
| §12 expected-loss decision, no threshold rule | Identical to MATHEMATICAL LOCK | ✅ Consistent |
| §13 mitigation mapping to controls | Consistent with MITIGATION LOCK, subject to the unresolved Modify mechanism | ✅ Consistent |
| §9 no GRU/LSTM/Transformer first | Forbidden reintroduction | ✅ Consistent |
