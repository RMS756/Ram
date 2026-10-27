# STAGE 3 — CHAPTER 2 DESIGN AND LITERATURE MATRIX

**Date:** 2026-09-19 · **Analysis only — no code modified**

Chapter 2 is organised by **research theme**, not as a list of papers. Every
section states purpose, sources, the exact prior-art relationship, and the
implication for REM.

> **Verification note.** Works marked ✅ were verified this session against a
> primary listing. Works marked ○ are named in the instruction and are real
> systems, but their bibliographic details were not independently re-checked
> here and must be verified before the chapter is submitted. `PIGuard` could not
> be confirmed at all and is marked ✗.

---

# C. FINAL CHAPTER 2 STRUCTURE

## 2.1 Introduction

**Purpose.** State the review's scope — runtime security for tool-using LLM
agents, with emphasis on financial agents — and the organising question: *given
a risk estimate, how is an intervention chosen, and does intervening help?*

**Implication for REM.** Frames the whole chapter around the
estimate → decide → intervene chain that Q1/Q2/Q3 later measure separately.

---

## 2.2 AI Agents and Security Characteristics

### 2.2.1 Agent Architecture
**Purpose.** Plan–act–observe loop; where a security layer can attach.
**Sources.** AgentTrust ✅, NEXUS ✅, CaMeL ○, Progent ○.
**Prior-art relationship.** Non-invasive attachment at the tool boundary is
**established** by AgentTrust and NEXUS.
**Implication.** REM's placement is conventional and **must not be claimed as a
contribution**.

### 2.2.2 Tool Use and External Environment
**Purpose.** Tool calls as the point where side effects become irreversible.
**Sources.** AgentTrust ✅ (file/shell/HTTP/DB side effects), Progent ○
(per-argument privilege), AgentDojo ✅.
**Prior-art relationship.** Argument-level inspection established by NEXUS and
Progent.
**Implication.** Grounds Group B/C features; argument-level provenance is
**not** REM's invention.

### 2.2.3 Multi-Step Execution
**Purpose.** Why single-event scoring is insufficient.
**Sources.** AgentTrust ✅ (RiskChain), DreamGuard ✅ (prefix risk), Corll ✅,
FinHarness ✅ (cross-turn drift).
**Prior-art relationship.** Multi-step monitoring is **thoroughly established**.
**Implication.** REM must not claim multi-step awareness. Only the **stated
false-alarm criterion** on the sequential statistic remains open.

### 2.2.4 Financial-Agent Characteristics
**Purpose.** What makes financial agents distinct — irreversibility,
authorisation state, monetary exposure, legitimate high-value workflows.
**Sources.** FinHarness ✅, ASB finance scenario ✅.
**Prior-art relationship.** FinHarness establishes the domain framing,
explicitly including the need to approve legitimate multi-step workflows.
**Implication.** REM's financial contribution must be the **decision-theoretic
use** of these properties (tier-indexed loss), not their identification.

---

## 2.3 Threat Landscape

| § | Topic | Purpose | Key sources | Prior-art relationship | Implication for REM |
| - | ----- | ------- | ----------- | ---------------------- | ------------------- |
| 2.3.1 | Prompt injection | Direct instruction override | AgentDojo ✅, LlamaFirewall ○ | Established threat class | Group A features |
| 2.3.2 | Indirect prompt injection | Injection via tool output | AgentDojo ✅, AgentDyn ✅ | Established; the primary REM threat | Motivates provenance labelling |
| 2.3.3 | Tool misuse | Legitimate tools, harmful use | ASB ✅, AgentHarm ○ | Established | Group B features |
| 2.3.4 | Privilege / authorisation | Exceeding granted authority | Progent ○, CaMeL ○ | Established | Group C authorisation state |
| 2.3.5 | Context integrity | Trust boundaries in context | CaMeL ○, taint-tracking literature ✅ | Established | Provenance labelling |
| 2.3.6 | Multi-step / trajectory attacks | Slow-burn, sub-threshold per step | **Corll ✅**, DreamGuard ✅ | Corll is the canonical slow-burn reference and **self-describes as a boundary result** | **The clause-C opening** |
| 2.3.7 | Financially consequential actions | Irreversible monetary harm | FinHarness ✅ | Established | Consequence tiers |

---

## 2.4 Runtime Defense Mechanisms

### 2.4.1 Rule / Policy Enforcement
**Sources.** AgentSpec ○, GuardAgent ○, ShieldAgent ○, Progent ○, NEXUS ✅.
**Relationship.** Deterministic rules are a **standard component**; NEXUS
combines them with a learned score exactly as REM proposes.
**Implication.** Rules+learned-score composition is **not novel**.

### 2.4.2 Prompt / Context Guardrails
**Sources.** LlamaFirewall ○, PromptGuard 2 ✅.
**Relationship.** Established. PromptGuard 2 22M (DeBERTa-xsmall, 19.3 ms at 512
tokens on A100) is usable off-the-shelf.
**Implication.** Supports §8's fixed-feature-extractor approach — **no new
detector should be trained**.

### 2.4.3 Tool / Privilege Control
**Sources.** Progent ○, CaMeL ○.
**Relationship.** Established; persistent-policy approaches.
**Implication.** REM's step-level mitigation is deliberately *weaker in scope*;
the lock forbids episode-level restriction without separate specification.

### 2.4.4 Action / Trajectory Guardrails
**Sources.** AgentTrust ✅, DreamGuard ✅, ProbGuard ✅, FinHarness ✅.
**Relationship.** **Densely occupied.** DreamGuard owns learned forward risk;
ProbGuard owns probabilistic model checking.
**Implication.** REM must position as *lightweight and auditable*, not as more
capable. DreamGuard's 25 ms is the latency comparator.

### 2.4.5 Learned Risk Estimation
**Sources.** **NEXUS ✅**, ShieldAgent ○, ProbGuard ✅, DreamGuard ✅.
**Relationship.** **The critical subsection.** NEXUS already uses Platt-scaled
logistic regression over a 9-dimensional feature vector including
irreversibility and sensitivity.
**Implication.** REM's estimator is **established prior art**. This must be
stated plainly in Chapter 2, not buried.

### 2.4.6 Runtime Mitigation
**Sources.** AgentTrust ✅ (SafeFix), NEXUS ✅ (revision/confirmation requests),
FinHarness ✅ (evidence re-injection).
**Relationship.** Modify-style remediation is **established**.
**Implication.** REM must not claim Modify as new; must cite SafeFix explicitly.

---

## 2.5 Benchmarks and Evaluation

| Benchmark | Status | Character | Relevance to REM |
| --------- | ------ | --------- | ---------------- |
| **AgentDojo** ✅ arXiv:2406.13352 | 36 releases, 0.1.0 (Jun 2024) → 0.1.35 (Oct 2025) | 97 tasks, 629 security cases, 4 suites (**Banking**, Slack, Workspace, Travel); executable | Primary candidate; Banking suite fits the financial scope. **Version must be pinned** |
| **ASB** ✅ arXiv:2410.02644 | Published | 10 scenarios incl. **finance**, 10 agents, 400+ tools, 27 attack/defense methods, 7 metrics | Financial subset candidate |
| **RAS-Eval** ✅ arXiv:2506.15253 | Published | 80 test cases, 3,802 attack tasks, 11 CWE categories; **real execution**, JSON/LangGraph/MCP | Execution-grounded candidate |
| **InjecAgent** ○ | Named | IPI-focused | Supporting |
| **AgentHarm** ○ | Named | Harmfulness-focused | Supporting |
| **AgentDyn** ✅ arXiv:2602.03117 | Verified | Dynamic open-ended IPI benchmark | Supporting; dynamic complement |
| **FinVault v2** | ⚠️ **WITHDRAWN** | — | **Must NOT be the sole or an unquestioned validation source.** May be referenced only as withdrawn |

**Purpose.** Establish that no single benchmark simultaneously provides
execution grounding, a financial domain, and a benign set — motivating a
multi-source evaluation.

> ⚠️ **One retrieved claim could not be cleanly verified.** A search result
> attributed a financial subset of "27 official attack + 26 official benign
> cases" to ASB, but the surrounding text referred to *Agent-SafetyBench*, a
> different benchmark. **This count is NOT INDEPENDENTLY VERIFIED and must not
> be cited until checked against the primary source.**

---

## 2.6 Probability Calibration and Decision Theory

### 2.6.1 Risk Estimation
**Sources.** Hoerl & Kennard (1970) ✅; Hastie et al. (2009) ⚠️ locators; NEXUS ✅.
**Relationship.** Logistic regression is textbook; its use as an agent risk
score is established by NEXUS.

### 2.6.2 Calibration
**Sources.** Platt (1999) ✅; NEXUS ✅.
**Relationship.** Platt scaling is established. **NEXUS independently selected
Platt over isotonic** because it achieved the lowest ECE and was less prone to
overfitting on a small calibration split — an empirical corroboration of REM's
frozen choice.
**Implication.** Strengthens REM's Platt selection; **also means the selection
cannot be claimed as a REM finding**. Beta calibration is discussed here but is
a forbidden reintroduction under the lock (see Conflict 1).

### 2.6.3 Expected Loss
**Sources.** Elkan (2001) ✅ — expected-cost rule and cost-matrix reasonableness
conditions `c(0,1) > c(1,1)`, `c(1,0) > c(0,0)`; Chow (1970) ✅ — reject option
with cost-derived threshold `t = (C_r − C_c)/(C_e − C_c)`.
**Relationship.** The decision principle is classical. Elkan is over **two**
class predictions, Chow adds **one** reject action; **REM's four-action,
tier-indexed loss is stated by neither.**
**Implication.** Chapter 2 must say *"method supported; REM-specific formulation
requires project-level justification."*

### 2.6.4 Calibration vs Control
**Sources.** **Calibration Is Not Control ✅ (2606.21399)**; What Can Be
Enforced? ✅ (2607.22868).
**Relationship.** The central methodological section. Establishes that
calibration quality does not imply control quality, and that **two prefixes with
equal risk may require different actions because one is recoverable and the
other is not**.
**Implication — two, both load-bearing:**
1. Mandates the **Q1/Q2/Q3 separation** in Chapter 4.
2. Provides the **principled argument for grounding `k_t` in recoverability**,
   which is REM's strongest available justification for the consequence tier.
   REM's action-dependent `R_t(v)` is *not* the scalar-threshold framing the
   paper criticises — this should be stated explicitly as REM's response.

### 2.6.5 Mitigation Effectiveness
**Sources.** AgentTrust ✅, FinHarness ✅, What Can Be Enforced? ✅.
**Relationship.** Measuring whether intervention reduces harm is distinct from
measuring detection.
**Implication.** Q3. Must carry the **closed-loop identifiability caveat**:
once blocking changes future proposals, static scores on ungated trajectories
need not identify the closed-loop frontier.

---

## 2.7 Financial-Agent Security

**Purpose.** The domain-specific literature and what it already settles.
**Sources.** FinHarness ✅, ASB finance scenario ✅, AgentDojo Banking suite ✅.
**Relationship.** FinHarness establishes inline financial-agent security with
per-step risk and joint security/benign evaluation.
**Implication.** REM's domain contribution is **narrow and must be stated
narrowly**: representing financial action risk as a *consequence tier indexing a
loss function*, rather than as another input feature.

---

## 2.8 Comparative Analysis

Contains the matrix in **E** below.

---

## 2.9 Research Gap

Carries the cautious statement from `STAGE3_PRIOR_ART_AND_POSITIONING.md` §I.2,
including the honest weakness statement: **REM's closest neighbour is NEXUS**,
and the distance is the decision-theoretic derivation, the consequence tier, the
ARL-controlled sequential component, and execution-grounded financial
validation — not the estimator or the action set.

## 2.10 Chapter Summary

---

# E. LITERATURE COMPARISON MATRIX

Values: **YES** · **NO** · **PARTIAL** · **NR** (not reported) · **NV** (not
independently verified this session). **No cell is manufactured.**

| Work | Runtime | Non-invasive | Context Detection | Tool/Action Analysis | Multi-step | Mitigation | Calibration | Decision Theory | Financial Domain | Benign Evaluation | Latency |
| ---- | ------- | ------------ | ----------------- | -------------------- | ---------- | ---------- | ----------- | --------------- | ---------------- | ----------------- | ------- |
| **AgentTrust** ✅ | YES | YES | PARTIAL (deobfuscation, LLM-judge) | YES | YES (RiskChain) | YES (SafeFix) | NR | NO (rule/judge assignment) | NO | NR | NR |
| **NEXUS** ✅ | YES | YES | PARTIAL (argument-level) | YES | PARTIAL (plan-level) | YES (revision/confirmation) | **YES (Platt)** | PARTIAL (formal intervention policy, not expected loss) | NO | NR | NR |
| **DreamGuard** ✅ | YES | YES | NR | YES | **YES (recurrent world model)** | YES (intervention) | NR | NO | NO | PARTIAL (safety–utility trade-off) | **YES (25 ms avg)** |
| **FinHarness** ✅ | YES | YES (inline wrapper) | YES (query monitor) | YES (tool monitor) | YES (cross-turn drift) | PARTIAL (evidence re-injection) | NR | NO (cascade routing) | **YES** | **YES** | NR |
| **Corll** ✅ | PARTIAL (proxy-side) | YES | NO (uses frozen scores) | PARTIAL (action edges) | **YES (CUSUM/peak)** | NO | **NO — no false-alarm criterion** | NO | NO | NR | NR |
| **Calibration Is Not Control** ✅ | N/A (position) | N/A | N/A | N/A | YES (prefixes) | N/A | **YES (subject)** | **YES (intervention value)** | NO | NR | NR |
| **What Can Be Enforced?** ✅ | N/A (theory) | N/A | N/A | YES (gates) | YES | YES (blocking) | YES (conformal) | **YES (Neyman-Pearson frontier)** | NO | NR | NR |
| **CaMeL** ○ | YES | NO (alters execution) | YES (data-flow) | YES | YES | YES (isolation) | NO | NO | NO | NV | NV |
| **Progent** ○ | YES | PARTIAL | NO | YES (argument values) | PARTIAL | YES (privilege) | NO | NO | NO | NV | NV |
| **AgentSpec** ○ | YES | YES | NO | YES | PARTIAL | YES | NO | NO | NO | NV | NV |
| **ShieldAgent** ○ | YES | YES | NO | YES | PARTIAL | YES | PARTIAL (MLN probabilities) | NO | NO | NV | NV |
| **GuardAgent** ○ | YES | YES | NO | YES | PARTIAL | YES | NO | NO | NO | NV | NV |
| **LlamaFirewall** ○ | YES | YES | YES (alignment check) | PARTIAL | PARTIAL | YES | NO | NO | NO | NV | NV |
| **ProbGuard** ✅ | YES | YES | NO | YES | YES (transition dynamics) | YES | PARTIAL (probabilistic) | PARTIAL (model checking) | NO | NV | NV |
| **PIGuard** ✗ | NV | NV | NV | NV | NV | NV | NV | NV | NV | NV | NV |
| **REM (proposed)** | YES | YES | YES (Group A) | YES (Group B) | PARTIAL (features + sequential statistic) | YES (canonical 4) | YES (Platt) | **YES (tier-indexed expected loss)** | **YES** | **YES** | To be measured |

## Reading the matrix

Three columns carry REM's entire position:

- **Decision Theory.** Only *What Can Be Enforced?* (theory, not a system) and
  *Calibration Is Not Control* (position paper) engage decision theory directly.
  **No deployed system in this table derives its action from a tier-indexed
  expected-loss minimisation.** This is REM's strongest structural distinction.
- **Calibration.** NEXUS already has it. REM gains nothing here.
- **Financial + Benign Evaluation.** FinHarness already has both. REM gains
  nothing here either.

The honest reading: **REM's distinguishing column is Decision Theory, supported
by a false-alarm-controlled sequential statistic.** Everything else in REM's row
is matched by at least one prior system.
