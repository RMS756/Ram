# Deliverable 1: REM-X architecture specification (design only, nothing implemented)

**Status markers used throughout REM-X documents.**

| Marker | Meaning |
|---|---|
| [V1] | REM v1.0 component; implemented and experimentally evaluated (thesis Chapter 4) |
| [DiD-I] | Implemented in REM-DiD (`REM_DEFENSE_IN_DEPTH/remdid/`) and evaluated in DiD-3 replay (exploratory, NO-ADAPT, oracle authorization) |
| [DiD-T] | Implemented in REM-DiD, unit- or scenario-tested only |
| [X-P] | **Proposed for REM-X. Not implemented, not evaluated.** |
| [PA] | Adopted from prior art; not claimed as a contribution |

**Constraints.**
- REM v1.0 and REM-DiD are not modified.
- The thesis is not edited.
- No experiment was run for this design.
- The five layers are kept: Input & Context, Detection, Behavioral Analysis, Decision Engine, Mitigation.
- Audit, the transaction ledger, monitoring and offline fitting are **cross-cutting state and services, not layers**.

## 1. Design goal and stance

**Goal.** Protect the *financial transaction* end to end:
1. from where each sensitive value came from (L1),
2. through what the user authorized (L1/L4),
3. to what was finally executed and recorded (L5).

The design must keep legitimate tasks that rely on **untrusted but legitimate financial documents** (a bill, a landlord notice).

**Stance from the evidence so far:**
- **Deterministic authorization is the primary control.** In DiD-3, oracle authorization alone gave 0 attacks at 173 of 334 benign tasks.
- **Evidence controls are the second line,** for when authorization is broad or delegated. With authorization bypassed, the four evidence controls together gave 0 attacks; each alone gave 3–13.
- **The learned decision is not a primary decision-maker.** It added no security behind authorization in any of 36 cost cells, and cost up to 68 benign tasks (file 06).
- **The main utility problem is delegation, not risk estimation:**
  - blanket provenance completed 147 of 334 benign tasks;
  - "explicit-parameter" authorization 122;
  - the oracle 173.
- The tasks lost are those whose decisive parameters legitimately come from a document.

## 2. The ten requested enhancements: assessment

| # | Enhancement | Prior art (file 03) | Decision for REM-X | Why |
|---|---|---|---|---|
| E1 | Field-level data provenance and integrity tracking | CaMeL, Fides, RTBAS, PACT, AgentCap | **Keep** [DiD-I]; no new claim | Needed infrastructure; already implemented |
| E2 | Selective isolation of untrusted content | CaMeL quarantined LLM; Fides hiding; DRIFT isolator; PromptArmor | **Not in the minimal set.** Optional arm only | REM mediates a black-box agent. Isolating content means rewriting what the agent sees, which is a Modify-type mechanism that must be declared (CLAUDE.md MITIGATION LOCK). Utility effects are known to be negative in prior work |
| E3 | Financial semantic analysis | CaMeL Q-LLM structured extraction (LLM); ScopeGate economic checks | **Keep, narrowly:** deterministic, schema-based extraction of payee, amount and reference from a **named** document, used only for delegation (E6′) | Separates the document's *data fields* from *instructions* without a model in the decision path |
| E4 | Multi-step transaction and tool-call monitoring | Agent-Sentry (learned sequence bound); AGATE (effect ledger); AgentTrust | **Keep** [DiD-I] rules; ledger-based additions [X-P] | The behavioral rules alone covered the 17 collision calls (DiD-3) |
| E5 | Cross-call cumulative financial limits | AGATE ledger; ScopeGate ceiling; AgentCap budgets; AIS | **Keep** [DiD-T] cumulative TAE budget, extended to per-recipient and per-session envelopes [X-P] | Closes the "amount-to-trusted-recipient" single point of failure (DiD-3 scenario 15d) only if limits are declared |
| E6 | Intent-bound financial authorization | AIS (typed intent, mandate); AgentCap (declared intent); Progent | **Keep** [DiD-I] TAE / 4A. **Extend with E6′, evidence-gated source delegation** [X-P] | E6′ is REM-X's main candidate differentiator (§3) |
| E7 | Exact-action, single-use execution capabilities | AIS; AGATE; AgentCap; GuardRail | **Keep** [DiD-I] gateway | Adopted [PA] |
| E8 | Independent tool-boundary verification | AIS (EVM re-checks economic terms); AgentCap (token validation at the tool) | **Keep, strengthened** [X-P]: the adapter re-evaluates the authorization record's economic terms with its own key, independent of the decision engine | Makes enforcement independent of a faulty or compromised decision layer. Adopted from AIS [PA] |
| E9 | Atomic transaction-limit reservation | Standard two-phase reservation in transaction processing; AIS single-use authority | **Keep** [X-P]: reserve at decision, commit on confirmed execution, release when not executed | Required for cumulative limits to hold under concurrent or interleaved calls; an engineering property, not a novelty |
| E10 | Post-execution verification and reconciliation | AIS (replayable assurance, settlement); AGATE (forensic replay) | **Keep** [X-P]: compare the observed state change with the approved action; on mismatch, halt the session and record. **Detection, not reversal** | Execution assurance against adapter or tool faults. The threat is outside prompt injection proper |

## 3. Candidate differentiators (the smallest defensible set)

Everything above exists in some prior system. A **materially different integration** remains plausible in two places, and one methodological property can be added. None is claimed until measured (file 09).

### D1. Evidence-gated source delegation for legitimate untrusted financial documents [X-P]

**Problem.**
- Strict origin rules deny a bill's payee: CaMeL's banking policy requires a user-trusted recipient (code-level reading).
- REM-DiD's PROV rule escalates it.
- Over-broad authorization admits the attacker.

**Mechanism.**
1. The user's trusted instruction may delegate *specific fields* of *one operation* to a *named source*, for example: "pay the bill in `bill-december-2023.txt`" delegates payee and amount to that file. The delegation is recorded in the authorization record as `DELEGATED(source = file id, fields = {recipient, amount}, caps)`.
2. A delegated value is admitted only if **all** of the following hold:
   - (a) a deterministic schema parser extracts it from the named source's *data fields*, not from free text;
   - (b) the call's value equals the extracted value (canonical form);
   - (c) no detector fires on the source segment that carries the value (call-linked evidence = false). An *unavailable* detector counts as "cannot tell", which leads to Escalate;
   - (d) the value is within the declared caps (for example a first-payment cap for a never-seen payee), from the cumulative envelope (E5).
3. If any condition fails, the call is escalated, not blocked: the document may be legitimate.

**Closest prior art.**
- ROPE (abstract and repository level) admits values that trace to "a source the user named".
- CaMeL's quarantined LLM extracts structured values, but its banking policy still requires a trusted recipient.
- PACT binds argument roles to trust contracts.

**What would be different:**
- the conjunction of named-source delegation, **deterministic** extraction, **injection-evidence gating of the delegated source**, and economic caps;
- evaluated on tasks where attacks are injected *into the delegated documents themselves*, as in the AgentDojo `injection_bill_text` and `injection_landloard_notice` vectors.

**Measurable property.** Benign task completion on document-delegated tasks, clean and under attack, at zero successful attacks, compared with strict provenance and with a parameter-provenance authorization baseline (file 07, experiment E-AC).

### D2. One transaction ledger across authorization, enforcement and reconciliation [X-P; largely PA]

**Mechanism.** A single append-only ledger, cross-cutting state, records for each authorized operation:
- its envelope (exact terms or cumulative limits);
- reservations made by 4A;
- the permit issued by L5;
- the adapter's independent check (E8);
- the observed post-execution state (E10).

**Invariant:** for every executed state change there is exactly one committed reservation and one permit, and the observed effect equals the approved terms (economic conformance).

**Honest position.**
- AIS (peer-reviewed) already combines single-use authority, execution-bound checks and replayable assurance for financial actions.
- AGATE has an effect ledger.
- **D2 is an engineering adoption, not a contribution claim.** It is in the minimal set only because D1's caps and the amount-to-trusted-recipient gap need it.

### D3. Failure independence as a stated, tested design requirement [methodological]

**Requirement.**
- Every attack class in the threat matrix (file 04) must be covered by at least two controls whose inputs differ: not only different code.
- Resilience is tested by **test-time evasion with the other controls fixed**, besides removal (file 08).

**Evidence.**
- DiD-2 found that removal and evasion disagree on the same control.
- DiD-3 found heavy redundancy, with distinct coverage in only 19 of 907 calls.
- No prior system was found, at the level read, that states and tests this requirement. The claim is bounded by abstract-level reading.

## 4. What REM-X deliberately does not do

- No interpreter or re-architecture of the agent (CaMeL, Fides). REM remains a mediation layer for a black-box agent.
- No LLM in the decision path, and no LLM-generated policies (earlier REM studies: NL compilation was NO-GO).
- No learned primary decision (file 06).
- No reversal of executed transfers. E10 detects and halts; recovery is out of scope.
- No sixth layer.
