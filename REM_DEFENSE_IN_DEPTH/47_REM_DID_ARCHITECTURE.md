# Deliverable 3: REM-DiD, the strengthened five-layer architecture (research candidate)

**Versions.**
- **REM v1.0:** the original, experimentally evaluated architecture. `rem/` is unchanged. Described in file 48; diagram `figures/fig_rem_v1_0_current.png`.
- **REM-DiD:** the proposed candidate, isolated in `remdid/`. It is **exploratory**, it is not adopted, and every structural change needs a supervisor decision. Diagrams:
  - as implemented: `figures/fig_rem_did_implemented.png`;
  - the original proposal: `figures/fig_rem_did_proposed.png`.
- **Results are never merged:** REM v1.0's results stay in the thesis; REM-DiD's are in `51_DID3_RESULTS.md`.

**Status codes:**
- [E] implemented, unit-tested and evaluated in DiD-3 replay;
- [T] implemented and tested only;
- [P] proposed, not implemented;
- [v1] REM v1.0 component, used unchanged.

## 1. Layer responsibilities (each answers a different question)

| Layer | Question | Controls | Trust boundary it protects |
|---|---|---|---|
| 1 Input & Context | Where did each value come from; what did the user authorize? | [v1] segment labels; [E] field-level provenance and canonical lineage (file 41); [E] TAE with integrity (file 42; **oracle issuer**); [P] trusted approval interface | Untrusted content → arguments; user → authorization record |
| 2 Detection | Is there instruction-like adversarial content, and is it linked to this call? | [v1] x~ctx2~; [E] D_role, D_override, D_fin, call-linked evidence, explicit unavailability (file 43); [P] classifier x~ctx1~ | Untrusted content → agent |
| 3 Behavioral Analysis | Does the sequence of actions look like an attack? | [v1] x~beh1–4~ (inside 4B); [E] R_newpayee, R_redirect, R_repeat, R_switch; [T] R_retry (file 45); [P] workflow sequence model | Agent → sequence of state changes |
| 4 Decision Engine | Authorized? Evidence of induction? Consequence? Which intervention? | [E] 4A non-compensatory authorization; [v1] 4B expected-loss verdict; [E] precedence, most restrictive wins (file 44) | Decision independent of the model's own choice |
| 5 Mitigation | Is exactly the decided call, and nothing else, executed? | [E] capability gateway, argument-bound single-use permits, re-validation before execution, fail-closed; [T] attenuation (file 46); [P] reviewer channel, declared Modify, recovery | Decision → external financial effect |
| Cross-cutting | — | [E] hash-chained per-decision audit; [v1] CUSUM observe-only; [v1] offline fitting | Not a layer |

## 2. Security decision flow for one proposed call

1. **Input & Context.** On every executed tool result, L1 segments and labels the output; L2 runs its detectors on the untrusted segments.
2. **Decision Engine.** On a proposed call:
   1. 4B (v1.0) computes p, tier and its verdict. It always runs, so that v1.0's history stays identical.
   2. For a state-changing call, 4A matches the TAE. The outcome is one of authorized, violation, no entry, unspecified, unverifiable, or unavailable.
   3. For sensitive values **not pinned** by a verified entry: L1 lineage (PROV), L2 call-linked evidence (DET) and L3 rules (BEH) are evaluated. An unavailable input means Escalate (fail-safe).
3. **Decision Engine.** Precedence takes the maximum severity over all active rules.
4. **Mitigation.**
   - Allow → permit → gateway re-validation → execution.
   - Escalate → withheld; a reviewer, if present, decides.
   - Block → not executed.
5. **Behavioral Analysis.** L3 records the call (released or withheld) for its sequence rules.
6. **Cross-cutting.** The audit record holds every rule that fired, the decisive rule(s), lineage, authorization result, mechanism and latency.

## 3. What is retained, changed or new, compared with REM v1.0

- **Retained unchanged:**
  - the five layers;
  - ridge logistic regression → Platt on the logit → consequence tier → expected-loss verdict (as 4B);
  - the four verdict names;
  - step-level semantics;
  - CUSUM observe-only;
  - attribution audit-only.
- **New (proposed changes to frozen design items; each needs a supervisor decision):**
  - TAE input;
  - 4A authorization ahead of the learned decision;
  - new evidence rules (PROV, DET sub-signals, BEH rules);
  - precedence;
  - gateway permits.
- **Not done:**
  - no sixth layer;
  - no change to REM v1.0's features or models;
  - no Modify mechanism;
  - no LLM anywhere in the decision path.

## 4. What the evidence supports (from `51_DID3_RESULTS.md`)

- **Layered:** yes.
- **DiD:** partly. Four evidence controls each protect when authorization is bypassed, but they are largely redundant, not complementary.
- **Resilient DiD:**
  - holds for the loss of PROV or DET and for every single injected failure;
  - does **not** hold for the loss of BEH or LEARN;
  - non-adaptive replay only.
