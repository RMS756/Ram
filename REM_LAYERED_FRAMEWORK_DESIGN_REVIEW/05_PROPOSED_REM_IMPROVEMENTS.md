# 05: Proposed REM improvements

**Baseline.**
- REM v1.0 is unchanged: `rem/` tree `cd11e32…`; configuration sha256 `8e1aa107…`.
- Its evidence base is `REM_FINAL_SCIENTIFIC_RECONCILIATION_2026_11_28/`.

**Nothing below is implemented or evaluated.** No REM version is created. Proposal A changes documentation only; Proposal B is reserved for future work.

## Proposal A: minimal improvements (current thesis; documentation and clarification only)

Each item describes **what already exists** in REM v1.0 more precisely. **None adds a security capability or changes a result.**

**This improvement can be implemented as an architectural, deterministic, or policy-based control and does not require a new mathematical model.** (Applies to A1–A7.)

### A1. Make the trust boundary explicit (Chapter 3; class 1)

**State:**
- Every context segment carries one of three labels:
  - trusted: the system prompt;
  - semi-trusted: the user request;
  - untrusted: tool output.
- Derived content inherits the least-trusted label, and nothing is ever promoted (`rem/algorithms/context/provenance.py`).
- The action features compare a call's arguments against the trusted and untrusted segments. **This comparison is the trust boundary at which REM operates.**

**Related work.** The same principle appears as:
- the layered RAG framework's "provenance-based instruction hierarchy";
- CaMeL's capabilities;
- Spotlight-Guard's spotlighting.

REM enforces it on **action arguments**, not on prompt assembly.

### A2. Separate detection, decision and authorization in the text (Chapters 1, 3 and 5; class 2)

**State:**
- REM v1.0 *estimates* whether a proposed call was induced by injected content and *decides* among four verdicts.
- **It does not authorize.** It has no representation of what the user permitted beyond the recipient-in-objective feature.

This is the difference from:
- NEXUS (deterministic rules);
- Progent and CaMeL (policies);
- AIS (execution authority).

It explains two measured findings:
- the residual attacks in `user_task_15`;
- the withholding of most legitimate payments.

### A3. Document the enforcement point (Chapters 3 and 4; class 1)

**State:**
- The Mitigation layer is realized as an HTTP gateway at the tool boundary. Withheld calls never reach the backend. Any exception during evaluation withholds the call (fail-closed).
- A deployment simulation reproduced the in-process replay exactly on 3,334 recorded episodes, with a median REM time per call of about 0.2 ms.

**Limit to state:** the gateway was never connected to a live agent.

### A4. Document evidence dependencies and complementarity (Chapters 3 and 4; class 1)

**The dependency graph:**
- action features and `x_beh1` and predicate D2 depend on Layer 1 labels;
- `x_beh1` depends on `x_ctx2`.

**The complementarity found in the evidence:**
- **action evidence** carries most of the discrimination and measurably raises attack-call withholding on P3;
- **behavioural evidence**, under modelled suppression, is the only evidence against the credential-change objective.

Wording follows `REM_FINAL_SCIENTIFIC_RECONCILIATION_2026_11_28/04` R4-4 and R4-6.

### A5. Mark implemented vs conceptual controls (Chapter 3; class 1)

Add one table listing every control with its status: implemented and evaluated; implemented and not exercised; specified and not implemented. In particular:
- hygiene: not exercised;
- `x_ctx1`: not implemented;
- the Modify mechanism: not exercised;
- the reviewer: absent;
- CUSUM: observe-only.

### A6. Reporting conventions (Chapter 4; class 1)

Following the CASCADE audit's lesson, state for every headline number:
- the verdict-to-outcome mapping (Modify, Escalate and Block all withhold);
- the population and its data history;
- the denominator;
- the kind of outcome (replay attack outcome, attack call executed, call-level withholding).

### A7. Position the primary contribution against ablation methodology (Chapter 2; class 1)

Cite the BARBICAN study ("Deletion is not substitution", preprint). It is independent evidence that deletion-based ablation of layered prompt-injection defenses can misattribute contributions. This supports, but does not prove, REM's removal-versus-suppression finding.

## Proposal B: optional architectural improvements (future work; not implemented)

| # | Addition | Source framework and original mechanism (level) | Weakness it could address in REM | Expected benefit (unmeasured) | Implementation complexity | Required data and experiments | New mathematical methods? | Reserve for |
|---|---|---|---|---|---|---|---|---|
| B1 | **Canonical identifier comparison** in provenance evidence | ROPE: deterministic origin verifier, fails closed on reformatting (R). REM-DiD: canonical IBANs and amounts (implemented, exploratory) | Exact-string `x_act1` defeated by reformatting (DiD-2: P1 rule 12 → 191 attacks; REM v1.0 held at 11 through `x_act2`) | Robust provenance under formatting changes | Low | Replay on the reformatted population and P1–P3 regression | No (normalization rule) | **Future REM implementation** (would be a new version, needing approval) |
| B2 | **Field- and source-level provenance** | ROPE origin labels from platform metadata (R); CaMeL value sources (R) | Channel-level labels treat a typed bank field and a free-text subject alike | Finer evidence; prerequisite for B3 | Medium | Field-labelled tool outputs (AgentDojo returns YAML structures for many tools) | No | Future implementation |
| B3 | **Model-independent authorization of financial arguments** | Progent policies (F/R); AIS typed intent with exact economic terms (C/O/S); NEXUS deterministic rules (O); ClawGuard, CapLite (O) | REM cannot tell an authorized payment from an unrequested one (thesis finding) | Separation of authorization from risk estimation | High. Natural-language intent compilation failed on held-out phrasing in REM's own exploratory studies | A trusted authorization channel (absent in AgentDojo); held-out requests written by others; live agents | No (rules); compilation by an LLM would put a model in the authorization path | **Future research** |
| B4 | **Reviewer channel for Escalate** | NEXUS "request confirmation" (O); AIS approvals (O); A-VIP confirmation of unauthorized spending (O) | Escalate coincides with Block without a reviewer | The four-verdict design becomes testable | High (human-subject protocol, ethics) | Reviewer study | No | Future research |
| B5 | **Economic limits** (per call, per payee, cumulative) | AIS mandates; ScopeGate ceiling; AGATE grants (A) | Amount escalation to trusted recipients; split transfers (not exercised by AgentDojo banking) | Bounded loss | Medium | Author-written financial fixtures; declared limit values [DESIGN BLOCKED] | No (policy values) | Future research |
| B6 | **Goal-drift or trajectory signal** | Multilayer DiD drift score over Sentence-BERT embeddings (C/O); MELON masked re-execution with embedding similarity (R) | Injections that change the plan without instruction-like text | Unknown | Medium-high (embedding model or extra LLM runs) | Embeddings; live or replay; ablation | **Yes: the source authors' scores** (06 §3). Their definitions were not read in full | Future research only, under 06's conditions. **Not in the verdict path as an LLM arbiter** |
| B7 | **Layer-reachability test** (constant-verdict substitution per component) | BARBICAN study (O) | Components whose verdicts cannot change outcomes (as found for D1/D2) | Engineering assurance | Low | Offline replay | No | Future research (methodological) |

**Explicitly not recommended:**
- a sixth layer;
- output moderation or response refinement (PromptGuard, the RAG output audit), which have no role at the tool boundary;
- an LLM judge in the decision path (forbidden by the design lock);
- any learned trajectory model of the GRU, LSTM or Transformer type (forbidden).
