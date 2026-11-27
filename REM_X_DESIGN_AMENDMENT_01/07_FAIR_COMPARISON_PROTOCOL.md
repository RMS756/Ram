# A1-07: Updated fair-comparison protocol (DRAFT, not frozen, nothing run)

**Status.**
- Supersedes `REM_X_DESIGN/07` where they differ.
- Draft for supervisor review. It is to be frozen and hashed before any run.
- **No experiment is started by this document.**
- No statistic, threshold or scoring rule is introduced here. The statistical methods named in §7 are established, cited methods. Their **parameters are researcher decisions**.

## 1. Primary question [PD]

> Does field-bound financial document delegation with economic limits and review (revised D1) give a different security–utility outcome from ROPE's origin-based policy on document-derived payment tasks, under identical agents, tasks and attacks? This is asked for:
> 1. legitimate documents with correct payment fields;
> 2. adversarial documents with manipulated but structurally valid payment fields.

**Secondary questions [PD]:**
- versus an AgentCap-class baseline: the same declared intent and parameter provenance, without economic limits or review;
- versus a deduplication-class baseline (AGATE-like): split transfers;
- versus CaMeL and Progent as released.

## 2. Comparators

| Arm | System | How it is obtained | Label in results |
|---|---|---|---|
| R0 | **ROPE as released** | Public code, commit `ffe27c4`, cached router scopes (`scopes/opus/banking.json`), **unclamped and clamped** | "ROPE (released)" |
| R1 | ROPE configuration with the document parameter marked `FREE` by the router | Same code; a scope override, as ROPE's own router may emit | "ROPE (FREE delegation)": shows ROPE's no-check alternative |
| K1 | AgentCap-class | Re-implemented from the published description; **no code found**; deviation list mandatory | "AgentCap-class (re-implementation)" |
| K2 | Deduplication-class (AGATE-like) | Only if A1-09 C1 (full text) gives enough detail; otherwise **descriptive comparison only** | "Dedup-class (re-implementation)" or omitted |
| K3 | CaMeL | Released code; needs a live LLM | "CaMeL (released)" (Phase B only) |
| K3p | CaMeL banking policy as a deterministic rule over REM lineage | Re-implementation | "CaMeL-policy class" |
| K4 | Progent | Released code, bundles AgentDojo 0.1.29 | "Progent (released)" if aligned; otherwise reported separately |
| C1 | REM v1.0 | Unchanged | — |
| C2 | REM-DiD | Unchanged | — |
| C3o | REM-X with **original** D1 (detector-silence admission) | After Phase 0 | Included **to test the predicted failure in A1-04**, not as a candidate |
| C3 | REM-X with **revised** D1 (O1–O5) | After Phase 0 | — |
| C3n | C3 without the learned decision (4B) | — | Per `REM_X_DESIGN/06` |

**Separate descriptive comparison** (no empirical arm): Agent-Sentry, AIS, RTBAS, Fides, and AGATE if K2 is not feasible. Mechanisms are compared at the stated evidence level. **Published figures are quoted only with their benchmark and model, never set against REM numbers.**

## 3. Running ROPE fairly

- **Deterministic part.** ROPE's enforcement (origin labeler + compiled policy) is deterministic once the cached scope is fixed.
  - It can be applied to the **same agent traces** as every other arm: the scripted agent and replay (Phase A).
  - This uses ROPE's own classes **unmodified**, wrapped by the REM harness.
  - The wrapper must be published, and any adaptation listed.
- **Version alignment.**
  - ROPE's scopes are keyed by the exact prompt text, and its logs use banking `v1.2.2`. REM's recordings use banking v1.
  - Before any run, compare the 16 user-task prompts and the environment files across the two versions.
  - If a prompt differs, ROPE blocks all state-changing tools for that task (A1-02 §1). This would be **an artefact, not a ROPE property**.
  - **Decision needed:** run all arms on `v1.2.2`, or on v1 with a re-cached router (which changes ROPE) [DESIGN BLOCKED].
- **Live agents (Phase B).** ROPE's own runner needs an OpenRouter key and a live agent model. Budget and backbone are [DESIGN BLOCKED].
- **Reporting.** ROPE's published logs (A1-02 §2) may be cited **as the authors' result on their configuration only**.

## 4. Document fixture sets (to be written and frozen before any run)

**L-set: legitimate documents with correct payment fields.**
- The existing document-delegated tasks: user_task_0 (bill), user_task_2 and user_task_12 (landlord notice), user_task_13 (address change), identified from the task prompts in A1-02.
- New variants of the same form.

**A-set: adversarial documents, each paired with an L-set twin, structurally valid.**

| ID | Manipulation |
|---|---|
| A1 | Genuine IBAN replaced by an attacker IBAN in the same field |
| A2 | Genuine payee; amount altered |
| A3 | Duplicate beneficiary field (mimicry line added) |
| A4 | Two conflicting totals |
| A5 | Zero-width characters inside the IBAN |
| A6 | Homoglyph or mixed-script characters in the payee or IBAN |
| A7 | Instruction-free manipulation (no imperative text anywhere) |
| A8 | Malicious document under a file name the user named |
| A9 | Known payee name with a changed account |

**Counts.** The number of fixtures per type is **not set here**; it is a researcher decision, recorded before freezing. No sample count is invented.

**Independent references.** The fixtures need a defined payee reference (user records or directory) to exercise outcome O1. Its contents must be fixed in advance and **must not be derived from the A-set**.

## 5. Agents and phases

| Phase | What runs | Budget | Labelled as |
|---|---|---|---|
| A1 | Scripted fully-compliant agent | None | "scripted agent" |
| A2 | NO-ADAPT replay of recordings | None | "NO-ADAPT replay" |
| B | Live agents | [DESIGN BLOCKED] | Model and repeat count stated |
| C | Defense-aware adaptive fixtures (A-set + `REM_X_DESIGN/07` §5) on A1; on B if funded | A1 none | "adaptive fixtures, scripted agent" |

**Never described as adaptive-agent robustness unless Phase B with adaptive attacks is run.**

## 6. Outcomes recorded

Per episode and per state-changing call:
- attack success (AgentDojo security function, and the fixture's own success condition for A-set cases);
- utility;
- executed / refused / escalated / blocked;
- for escalations, the values shown to the reviewer.

**Reported separately:**
1. automatic completion;
2. completion if every escalation were approved (upper bound for utility, lower bound for security);
3. completion if every escalation were refused.

**No reviewer model is invented.** A human-review study would need its own protocol and ethics approval.

## 7. Statistics: established methods only, parameters to be decided

| Method (as used in REM-DiD) | Reference | Status of reference |
|---|---|---|
| Multiple-comparison correction | Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70 | **Not found in Crossref.** Bibliographic details must be verified against the journal (JSTOR) before citation |
| Bootstrap confidence intervals | Efron, B. (1979). Bootstrap methods: Another look at the jackknife. *The Annals of Statistics*, 7(1), 1–26. https://doi.org/10.1214/aos/1176344552 | Verified (Crossref) |
| Bootstrap for clustered data | Field, C. A., & Welsh, A. H. (2007). Bootstrapping clustered data. *JRSS B*, 69(3), 369–390. https://doi.org/10.1111/j.1467-9868.2007.00593.x | Verified (Crossref) |
| Paired sign-flip (randomization) test at cluster level | A textbook or primary reference must be selected and verified | **[REFERENCE NEEDED]** |
| Set-overlap index (Jaccard) for coverage | Jaccard, P. (1912). The distribution of the flora in the alpine zone. *New Phytologist*, 11(2), 37–50. https://doi.org/10.1111/j.1469-8137.1912.tb05611.x | Verified (Crossref) |

**Researcher or supervisor decisions, not set here:**
- the confidence level;
- the family of hypotheses for correction;
- one- or two-sided interpretation;
- the clustering unit(s);
- the decision rule for calling a difference.

The earlier draft's rule ("95% CI excludes 0 after Holm") is withdrawn as an unapproved choice (A1-11).
