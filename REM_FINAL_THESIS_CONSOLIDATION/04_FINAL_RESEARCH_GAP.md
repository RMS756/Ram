# 04: Final research gap (evidence-based reassessment) [PD]

**Basis.**
- The literature at the levels recorded in 01: mostly abstract level; Progent and MELON read in full; Table 2.3 of the thesis.
- REM's stored evidence, as reconciled at `5d7828c`.

**Qualification.** Every statement about prior work is limited to **the studies examined, at the level read**. The review is not exhaustive, so "not found" never means "does not exist".

## 1. The six questions

| # | Question | Relevant prior work (level) | Verified evidence | What remains uncertain | What REM evaluated | Limits of REM's evidence | Gap defensible? |
|---|---|---|---|---|---|---|---|
| 1 | Comparable component-level ablation of layered agent defenses? | Spotlight-Guard (A): "a component ablation isolates each layer's contribution". Saleem et al. (A): layer ablation of a RAG chatbot pipeline. Progent (F): ablations of approver, model and attack. NEXUS (A): rule-only comparison. BARBICAN (A): stage-level deletion and substitution | **Yes, component- or layer-level ablations of layered injection defenses exist** | Their designs (paired? on agents executing financial calls?) are not read | Protocol-frozen, paired, component-level ablations of REM v1.0 on three AgentDojo banking populations (P1 3,313; P2 681; P3 2,113 episodes) | Data examined during development; the estimator is not isolated; Input & Context not removable; the classifier absent; replay | **Not as a general gap.** Only as "for a financial agent on an executable banking benchmark" |
| 2 | Removal distinguished from test-time evidence suppression? | BARBICAN (A): deletion vs **constant-verdict substitution** of one stage of an MCP gateway, with opposite attributions | **The general point is published** (deletion ≠ substitution). No study examined at the level read suppresses an **evidence family** of a learned tool-call decision while the others stay in place | Whether full texts contain such a test | DiD-2: modelled suppression of the behavioural, action and both families on P1. Removal: refit without the family | Suppression is idealized and label-conditioned (features set to not-fired on attack-labeled calls); exploratory; P1 only | **Yes, narrowly:** for evidence families of a learned decision at the tool-call boundary of a financial agent |
| 3 | Learned risk assessment vs deterministic rules on the same proposed calls? | NEXUS (A, R): calibrated LR vs rule-only on synthetic, R-Judge, AgentHarm and IPI benchmarks; its repository reports no binary-detection gain. Thesis Table 2.3 (F): none of the six full-text papers compares with parameter-free rules on the same trajectories | **Published outside finance** (NEXUS) | NEXUS's design details (not read) | REM vs rules A1 and A2, Progent's policy, B1 thresholds, on the same episodes (P1–P3) | Replay; rules partly written with knowledge of the benchmark | **Only for financial tool calls** on an executable banking benchmark; not in general |
| 4 | Attack outcomes and legitimate financial task completion jointly? | Spotlight-Guard (A): benign-task success; Saleem (A): FPR; Agent-Sentry (A): benign executions allowed; Progent (F): utility; AgentBoundary (F): over-defense at scale | **Joint security-utility reporting is common**, though not on banking tasks for most | Whether any reports a withhold-everything reference | Benign completion, completion under attack, legitimate state-changing calls released, **and the P1 identity with the withhold-everything arm** | The identity is shown on P1 only; replay | **Yes, as a specific contribution** (the withhold-everything reference), not as a general gap |
| 5 | Complementary protection between layers established experimentally? | Saleem et al. (A): "all three layers provide complementary protection … combined effect exceeds the sum" (RAG chatbot, text samples) | **A complementarity claim exists for a non-agent pipeline** | Its method; whether it holds for agents | Two evidence families cover different attack classes: removing action evidence lowers attack-call withholding on P3 (−9.12 pp [−23.45, −0.74]); suppressing behavioural evidence lets the credential-change objective succeed (11 → 131) | Suppression modelled; the action-removal effect on final outcomes not resolved; complementarity is within one decision and one enforcement point | **Yes, narrowly:** for a financial agent, and qualified as "within a shared learned decision and enforcement pathway" |
| 6 | Trade-off between attack prevention and blocking of legitimate operations? | AgentBoundary (F); CASCADE audit (A): referral conventions drive the FPR; Progent (F) | **The trade-off is widely reported** | — | REM: 11/2,979 attacks with 105/334 benign tasks on P1. B1 thresholds: more attacks, more tasks. Progent's policy: 0 attacks with more tasks (benchmark-specific list) | Replay; Modify, Escalate and Block equivalent without a reviewer | **No** as a gap. It is part of the evaluation, not a missing piece of knowledge |

## 2. Assessment of the candidate formulation

The candidate in the task asks whether individual components provide measurable and complementary protection under financial-agent conditions, and at what cost. It is **defensible only if narrowed**:

1. Ablating layered defenses, comparing learned scores with rules, and reporting the security–utility trade-off are **not gaps in general** (questions 1, 3, 4, 6).
2. What remains, among the studies examined, is the **combination**:
   - a financial agent;
   - an executable banking benchmark;
   - component removal against test-time suppression of evidence families;
   - complementarity between evidence families;
   - cost measured against a reference that executes no state-changing call.

## 3. Final recommended formulation [PD]

> Layered runtime defenses against indirect prompt injection, combining content inspection, provenance-aware, behavioral, learned and rule-based controls, have been proposed and, in several cases, ablated layer by layer. Among the studies examined, most of them at abstract level, the evidence remains limited on three questions for a financial agent acting on an executable banking benchmark:
> - which components of such a defense actually carry its protection, and whether removing a component and suppressing its evidence at test time lead to the same assessment;
> - whether a learned, consequence-aware decision adds value over simple deterministic rules on the same proposed financial calls;
> - what the measured protection costs in legitimate financial task completion, including against a reference that executes no state-changing call.

**Where it is used.** The working copy applies this wording, still marked as pending the supervisor's confirmation:
- Ch. 1 §1.4, edit `C-GAP1`, in the thesis's prose form;
- Ch. 2 §2.11.7 and §2.11.5, edits `A7` and `C-GAP2`;
- the Ch. 2 summary, edit `C-GAP3`.

**What it does not claim:**
- no architectural or mechanism novelty;
- no claim that no prior work exists;
- no claim of robust defense in depth.

**It would need revision if:**
- a full-text reading shows that Spotlight-Guard, Saleem et al. or BARBICAN suppress evidence families with the others fixed; or
- a study reports such an ablation for a financial agent on an executable benchmark.
