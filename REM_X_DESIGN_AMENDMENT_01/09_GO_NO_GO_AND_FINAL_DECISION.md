# A1-09: Revised GO / CONDITIONAL GO / NO-GO, and answers to the final questions

**Scope.** This is a design assessment, not an implementation decision. It supersedes `REM_X_DESIGN/10`.

## 1. Recommendation

| Scope | Before | Now | Reason |
|---|---|---|---|
| REM-X design as the basis for further work | CONDITIONAL GO | **CONDITIONAL GO, narrowed** | Keep the five layers, adopted mechanisms and revised D1 (O1–O5). Drop D1 as a contribution |
| D1 as originally specified (detector-silence admission) | Candidate differentiator | **NO-GO** | Unsafe (A1-04) |
| D1 revised as an *architectural contribution* | — | **NO-GO** | Implementation variant of ROPE-style delegation plus established controls (A1-05) |
| D1 revised as a *design element* to be compared empirically with ROPE | — | **CONDITIONAL GO** (design only) | Measurable question (A1-02 §4, A1-07 §1) |
| D2 | Adoption | **Unchanged: adoption, no claim** | A1-10 |
| D3 as novel method | Candidate | **NO-GO** as novelty; **GO as an evaluation requirement** [PD] | A1-10 |
| Phase 0 / Phase A | Conditional | **Not started; still conditional** on C1–C6 | Per the instruction, no implementation |
| Any superiority claim | NO-GO | **NO-GO** | No comparable run |
| New mathematics | — | **NO-GO** without a cited source or decision | A1-11 |

## 2. Conditions

| ID | Condition |
|---|---|
| C1 | Read the full texts of ROPE (v1 and v2), AGATE, AgentCap, Agent-Sentry and AIS. Update A1-01 cell by cell. Practical route: a session started in the `ram-thesis-research` environment (allows `arxiv.org`). AIS on `mdpi.com` needs that host allowed, or the arXiv version 2608.30519 |
| C2 | Settle comparator availability: ROPE public; AGATE, AgentCap and Agent-Sentry code not found (ask the authors); CaMeL and Progent public |
| C3 | Settle ROPE version alignment (banking `v1.2.2` scopes vs REM's banking v1 recordings) |
| C4 | Supervisor decisions on the blocked items in §3 |
| C5 | Choose and verify references for: the reservation pattern; the sign-flip test; Holm 1979 (not in Crossref); a character-confusables standard |
| C6 | Freeze and hash the protocol before any run |

## 3. Design-blocked items (new or changed)

## DESIGN BLOCKED

**Item:** Independent payee reference for outcome O1: what counts (user's past payments, payee directory, pinned value, bank verification service) and how its contents are fixed for evaluation.

**Why required:** Without it, every document-derived payee is O2 (review), and D1 gives no automatic utility.

**Current source status:** Not specified anywhere; AgentDojo banking provides only transaction history.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

## DESIGN BLOCKED

**Item:** Economic envelope values: per-call, per-recipient and per-session limits; first-payee restriction.

**Why required:** O1 and O5; amount and split-transfer threats.

**Current source status:** Unspecified (unchanged from `REM_X_DESIGN/10`).

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

## DESIGN BLOCKED

**Item:** Mapping of O4 (suspicious document) to Escalate or Block.

**Why required:** Verdict semantics are frozen; the choice changes outcomes.

**Current source status:** No decision.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

## DESIGN BLOCKED

**Item:** Statistical decision parameters: confidence level, hypothesis family, sidedness, clustering unit, decision rule; and the resilience and independence judgement (A1-11 M3–M7).

**Why required:** Any comparison.

**Current source status:** The earlier choices were withdrawn as unapproved.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

## DESIGN BLOCKED

**Item:** Benchmark version for all arms (banking v1 vs `v1.2.2`), and fixture counts for the L-set and A-set.

**Why required:** A fair ROPE comparison; no invented sample counts.

**Current source status:** Unresolved.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

Unchanged blocked items from `REM_X_DESIGN/10`: backbones and repeats; extended suite; role and scope of 4B; thesis positioning.

## 4. Answers to the final questions

**1. Is D1 genuinely different from ROPE, or an implementation variant?**
- **Original D1** differs from ROPE in what it admits: document-derived values on extraction and detector silence. That difference is **unsafe**, so it cannot be a contribution.
- **Revised D1** is, at the present evidence level, an **implementation variant** of ROPE's origin-based delegation:
  - field-level instead of item-level binding;
  - explicit ambiguity outcomes.

  It is combined with established economic limits and REM's existing Escalate verdict.
- This assessment rests on ROPE's code and logs (R) and A/S-level reading of the others. The full texts could narrow D1 further.

**2. Can D1 safely admit fields from an ordinary untrusted financial document?**
- **No, not automatically.**
- An ordinary document can **propose** a payee and amount, and D1 can bind them exactly and detect ambiguity.
- Acceptance of the **payee** requires independent affirmative evidence.
- Acceptance of an **amount** from such a document is only **bounded**, by the user-declared envelope. It is not verified.
- Absent independent evidence, the correct outcome is **review (Escalate)**. Security then depends on the reviewer.

**3. What evidence must exist before accepting a document-derived payee and amount?**

All of the following, stated in A1-04 §4:
- **Payee:**
  - the user's trusted delegation of that field of that operation to that source;
  - exactly one canonical candidate at the declared field location;
  - confirmation of the account by an independent trusted reference that is not the document (past payments, payee directory, pin, or a bank verification service);
  - no affirmative suspicion: detector evidence, a name/account mismatch with records, confusable characters.
- **Amount:**
  - exactly one canonical candidate;
  - within the per-call and cumulative limits the user declared;
  - or equal to an amount the user stated.

  Otherwise it is bounded exposure, or review.
- **Source identity and document integrity** (for example an issuer signature verified against a trusted key) would strengthen both. They are **not available** in AgentDojo banking.
- **In every case:** execution through a single-use permit with an independent execution-side re-check.

**4. What can REM-X potentially do better than ROPE and AGATE?** These are hypotheses to be measured, not claims.

| Versus | Potential advantages |
|---|---|
| **ROPE** | (a) **Amount and cumulative-exposure control**: ROPE's banking table guards recipients only. (b) **Field-level binding**: ROPE admits a value found anywhere in an admitted item. (c) **Review instead of refusal** for unverifiable but possibly legitimate document values, which can recover utility **only where a reviewer exists**. (d) **Ambiguity detection** for duplicate or conflicting fields. (e) **Execution-side re-check and reconciliation** |
| **AGATE** | (a) **Cumulative monetary exposure** rather than request deduplication. (b) Possibly fewer outright denials in legitimate file processing, by escalating instead; same reviewer caveat. (c) Financial typing of terms. Whether REM-X's canonical-argument permits avoid AGATE's parameter-rewriting bypass **cannot be judged** without AGATE's full text |

AGATE is broader in deployment (three production harnesses). **REM-X is narrower:** one benchmark, financial only.

**5. Which contribution claims are defensible now?**
- Only those in A1-08 §2:
  - the evaluated REM v1.0 results;
  - REM-DiD's exploratory findings with their limits;
  - a documented design analysis of document delegation.
- **No mechanism novelty claim is defensible.**

**6. What remains unknown?**
- The full texts of ROPE (incl. v2), AGATE, AgentCap, Agent-Sentry and AIS. In particular:
  - whether any already handles documents, amounts or cumulative exposure;
  - whether any evaluates per-component evasion.
- AGATE's matching rule, ledger semantics and parameter-rewriting case.
- Whether AgentCap's "budget" is monetary.
- Whether ROPE runs faithfully on REM's benchmark version.
- How a reviewer performs on well-formed forged documents. **No reviewer model is assumed.**
- All values in §3. Every comparative outcome: **nothing has been run.**
- Whether REM-DiD documents contain unsourced criteria of the kind flagged in A1-11 (not audited here).
