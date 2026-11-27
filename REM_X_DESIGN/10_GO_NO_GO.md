# Deliverable 10: GO / CONDITIONAL GO / NO-GO recommendation

## 1. Recommendation

| Scope | Recommendation | Reason |
|---|---|---|
| REM-X **design** (files 01–09) as the basis for further work | **CONDITIONAL GO** | Coherent with the five layers and the frozen pipeline. Only one candidate architectural differentiator (D1) and one methodological one (D3). Every other mechanism is adopted, and is labelled as adopted |
| **Phase 0:** implement D1, the ledger with atomic reservation, the adapter re-check and reconciliation in a **new** package (REM v1.0 and REM-DiD untouched) | **CONDITIONAL GO**, after conditions C1–C4 | Small, deterministic, testable components; no model in the decision path |
| **Phase A:** scripted agent + NO-ADAPT replay; E-AC; ablation and failure-independence protocol | **CONDITIONAL GO**, after the protocol is frozen and C1–C5 are met | No budget needed. Answers Q1–Q3 under stated limits |
| **Phase B:** live LLM agents; adaptive attacks against live agents | **NO-GO until funded and specified** | Needs backbones, repeats and budget: all unresolved |
| **Any superiority claim** over AgentCap, Agent-Sentry, AIS, Progent, Fides, CaMeL or RTBAS | **NO-GO now** | No comparable run exists. Published metrics are not comparable. Most prior systems have no runnable code |
| **Novelty claim** for D1 | **NO-GO until C1** | Bounded by abstract-level reading of AgentCap and AIS; ROPE is close |
| Changing 4B's role or scope in the thesis | **NO-GO without supervisor decision** | Frozen pipeline (file 06) |
| Isolation (E2) or any Modify-type content rewriting | **NO-GO** for the minimal set | No declared Modify mechanism (MITIGATION LOCK) |

## 2. Conditions

| ID | Condition | How it is met |
|---|---|---|
| C1 | Full-text verification of AgentCap, AIS, ROPE, Agent-Sentry and RTBAS for delegation, cumulative limits and evasion testing | Read in the environment with paper access (arXiv and mirrors were blocked here); update file 03 cell by cell, with evidence levels |
| C2 | Comparator availability settled | Ask the AgentCap, Agent-Sentry and RTBAS authors for code. Check Progent against AgentDojo 0.1.35. Write the K1 deviation list |
| C3 | Supervisor decisions on the blocked items (§3) | Written decision, recorded before freezing |
| C4 | A trusted approval channel assumed or simulated, and stated | An oracle or explicit authorization record. The limitation is stated in every table |
| C5 | Protocols 07 and 08 frozen, hashed and committed before any run | As for DiD-3 (`50_PROTOCOL_DID3.sha256`) |

## 3. Design-blocked items

## DESIGN BLOCKED

**Item:** Economic envelope values: per-call, per-recipient and per-session limits; the first-payee cap; currency policy.

**Why required:** D1 condition (d), the cumulative limits (E5) and atomic reservation cannot be evaluated without them.

**Current source status:** Not specified in the Stage 2 report or the proposal. The REM-DiD cost-sensitivity `amount_limit` grid (100 / 1,000 / 10,000) is an exploratory tier boundary, not an authorization limit.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

## DESIGN BLOCKED

**Item:** Definition of the document-delegated task subset, and the delegation grammar (which fields may be delegated, to which sources).

**Why required:** H-AC1 is measured on this subset.

**Current source status:** Not specified anywhere; must be fixed by reading the task definitions before any run.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

## DESIGN BLOCKED

**Item:** Role and scope of 4B (frozen learned decision) in REM-X.

**Why required:** File 06 recommends tighten-only, consulted for calls not fully pinned. This narrows the frozen pipeline's scope.

**Current source status:** The frozen pipeline places 4B on the primary path; no decision on narrowing it.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

## DESIGN BLOCKED

**Item:** LLM backbones, number of repeats, and budget for Phase B; AgentDojo version for any additional suite.

**Why required:** Live and adaptive-agent evaluation.

**Current source status:** Listed as unresolved in CLAUDE.md (DATA / EVALUATION LOCK).

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES

## DESIGN BLOCKED

**Item:** Extended financial suite (`banking-fin-ext`): tasks, injection tasks, and utility and security functions.

**Why required:** Threats X1–X7 are not in AgentDojo banking v1.

**Current source status:** Not written. It must be frozen and reviewed before defenses are run on it.

**Safe action:** STOP — do not choose a value.

**Supervisor decision needed:** YES (scope); content by the researcher with second-person review

## DESIGN BLOCKED

**Item:** Whether REM-X enters the thesis as "future work evaluated" or "future work proposed".

**Why required:** Determines what Chapter 5/6 may state.

**Current source status:** No decision.

**Safe action:** STOP — do not edit the thesis.

**Supervisor decision needed:** YES

## 4. Answer to the final objective

**Question.** The smallest scientifically defensible set of architectural innovations that *could* let REM outperform existing agent-security architectures in:
- financial transaction integrity;
- indirect prompt-injection resistance;
- benign utility.

**The set:**
1. **D1, evidence-gated source delegation.** This is the only candidate that targets the utility loss measured in REM-DiD (oracle 173 vs blanket provenance 147 vs explicit-parameter authorization 122 benign tasks of 334) without loosening security by construction.
2. **The economic envelope enforced through one ledger with atomic reservation and an independent adapter re-check** (D2, adopted). It closes the amount-to-trusted-recipient single point of failure, and gives D1's caps a place to be enforced.
3. **Evasion-based failure-independence testing** (D3, methodological). It is what makes a defense-in-depth claim checkable.

**Nothing else in E1–E10 is needed to test these claims.**

**Whether REM-X actually outperforms anything is unknown** until E-AC is run under identical conditions. The present evidence supports only:
- a design hypothesis;
- the narrower, already-measured findings of REM-DiD (exploratory, NO-ADAPT, oracle authorization).
