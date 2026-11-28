# 02: Integration of recommendations A1–A7 into the thesis

**Source of the definitions.** `REM_LAYERED_FRAMEWORK_DESIGN_REVIEW/05_PROPOSED_REM_IMPROVEMENTS.md` (commit `6c52c90`), "Proposal A". The definitions are quoted or closely paraphrased below and are not reinterpreted.

**Status of every item:**
- **Applied in the working copy** (`thesis_working_copy/`). The full text of each edit is in 07 §1.
- Documentation only. No item adds a security capability, changes REM v1.0, changes a number, or needs an equation or an experiment.
- Each states only what the code and stored results show.

## 1. Integration table

| Rec. | Exact original definition (05, Proposal A) | Thesis location (working copy) | Already addressed in the humanized edition? | Proposed edit (smallest necessary) | Scientific justification and verification against REM v1.0 | Requires an experiment? | Status |
|---|---|---|---|---|---|---|---|
| **A1** Trust boundary | "Every context segment carries one of three labels: trusted (system prompt), semi-trusted (user request), untrusted (tool output). Derived content inherits the least-trusted label, and nothing is ever promoted. The action features compare a call's arguments against the trusted and untrusted segments. This comparison is the trust boundary at which REM operates." Related work: RAG instruction hierarchy, CaMeL capabilities, spotlighting | Ch. 3 §3.4.2, new paragraph "Where the trust boundary acts" (edit `A1`) | **Partly.** Table 3.3 (TB-1 to TB-4) and §3.4.2 define the labels. Neither says where the labels are consumed, nor relates them to the literature | One paragraph after §3.4.2 | `rem/algorithms/context/provenance.py` (labels, least-trusted inheritance); `rem/algorithms/behavior/evidence.py` (action features use the labelled segments); `pilot_e0.yaml` (D2 requires `x_act1` at tier ≥ 3). Saleem et al. and CaMeL cited at abstract or repository level only | No | Applied |
| **A2** Detection / decision / authorization | "REM v1.0 *estimates* whether a proposed call was induced by injected content and *decides* among four verdicts. **It does not authorize.** It has no representation of what the user permitted beyond the recipient-in-objective feature." Contrast with NEXUS (rules), Progent and CaMeL (policies), AIS (execution authority); explains `user_task_15` and the withholding of legitimate payments | Ch. 3 §3.2.2, new paragraph "Detection, decision and authorization" (`A2`). Ch. 1 §1.11, "What the thesis does not claim" (`A2-ch1`) | **Partly.** §3.2.2 separates estimation, decision and mitigation; "authorization" is not named. Ch. 1 already denies that the features "establish what the user authorized" | One paragraph; one bullet extended and one added | `x_act1` is the only user-request comparison (Table 3.6). There is no allow-list or policy in `rem/`. The finding of Ch. 4 §4.6.7 is cited for the consequence | No | Applied |
| **A3** Enforcement point | "The Mitigation layer is realized as an HTTP gateway at the tool boundary. Withheld calls never reach the backend. Any exception during evaluation withholds the call (fail-closed). A deployment simulation reproduced the in-process replay exactly on 3,334 recorded episodes, with a median REM time per call of about 0.2 ms." Limit: "the gateway was never connected to a live agent" | Ch. 3 §3.8, paragraph "Enforcement point" (`A3`). Ch. 4 §4.5.7 "Tool-call enforcement and runtime", paragraph "Enforcement through a gateway" (`A3-ch4`) | **No.** The gateway and its simulation are absent from every thesis edition | Two paragraphs | `rem/deployment/gateway.py` docstring (fail-closed rules). `results/deployment_sim/2026-11-05_full/RESULTS.md`: parity 0 mismatches for B0, B1 and REM; median 0.19 ms, p95 0.40 ms; 4xx on malformed or unknown requests. **Caveat stated in the text:** the simulation ran at commit `c30ad8a` (5 Nov), before `7c79883`. That commit is not in the shallow clone, so code identity cannot be checked; outcome identity with the re-executed replay is stated instead | No | Applied |
| **A4** Evidence dependencies and complementarity | "The dependency graph: action features and `x_beh1` and predicate D2 depend on Layer 1 labels; `x_beh1` depends on `x_ctx2`. The complementarity found in the evidence: action evidence carries most of the discrimination and measurably raises attack-call withholding on P3; behavioural evidence, under modelled suppression, is the only evidence against the credential-change objective." Wording to follow reconciliation R4-4 and R4-6 | Ch. 3 §3.6.2, paragraph "Dependencies among the evidence families" (`A4`). Ch. 4 §4.5.10 (`R4-4`) and §4.5.12 (`R4-6`) | **Partly.** Ch. 4 §4.5.4 says Input & Context is not isolatable; complementarity is not stated | One paragraph, plus R4-4 and R4-6 | Table 3.6 definitions (`x_beh1` uses `x_ctx2`; `x_act*` use L1 entities). Numbers from [A21] and [D2] as reconciled | No | Applied |
| **A5** Implemented vs conceptual controls | "Add one table listing every control with its status: implemented and evaluated; implemented and not exercised; specified and not implemented. In particular: hygiene not exercised; `x_ctx1` not implemented; Modify mechanism not exercised; reviewer absent; CUSUM observe-only." | Ch. 3 §3.16 (chapter summary after the merge), **Table 3.17** (`A5`) | **Partly**, scattered across Ch. 1 ("does not demonstrate"), Ch. 3 §3.5 and Ch. 4 §4.5.4 | One table at the end of Ch. 3, so no existing table is renumbered | Each row cross-checked against Ch. 4 results and the code. CUSUM row: held-out false-alarm rate 0.106 vs target 0.05 (Ch. 4 §4.6.4) | No | Applied |
| **A6** Reporting conventions | "Following the CASCADE audit's lesson, state for every headline number: the verdict-to-outcome mapping (Modify, Escalate and Block all withhold); the population and its data history; the denominator; the kind of outcome (replay attack outcome, attack call executed, call-level withholding)." | Ch. 4 §4.3.3, paragraph "Reporting conventions" (`A6`) | **Partly.** §4.3.3 already distinguishes a released attack-labelled call from a committed change | One paragraph | Step-level semantics (Ch. 3 Table 3.11); idealized reviewer only where stated (Table 4.47). CASCADE audit cited at abstract level | No | Applied |
| **A7** Positioning against ablation methodology | "Cite the BARBICAN study ('Deletion is not substitution', preprint). It is independent evidence that deletion-based ablation of layered prompt-injection defenses can misattribute contributions. This supports, but does not prove, REM's removal-versus-suppression finding." | Ch. 2 new §2.11.7, "How layers are evaluated" (`A7`). Also qualifies the DiD-inserted §2.11.6 (`M1b`) | **No.** Neither study is in the bibliography | One section of about 1.5 pages, which also carries the related-work text of the review's 08-A | Abstract-level statements only, worded "reports" | No | Applied |

## 2. What A1–A7 do not do

- **No runtime security improvement:** REM v1.0 is unchanged (`rem/` tree `cd11e32…`).
- **B1–B7 are not integrated as features.** They appear only as future work, with the review's classification:
  - existing Ch. 5 items 2 (≈B3), 6 (≈B4) and 7 (≈B1);
  - new items 15 (B2), 16 (B5) and 17 (B7), edit `FW`;
  - B6 is not added, because it would bring in the source authors' scores (review 06 §3).

| Item | Classification (review 05) |
|---|---|
| B1 Canonical identifiers | Future implementation |
| B2 Field-level provenance | Future implementation |
| B3 Independent authorization of financial arguments | Future research |
| B4 Reviewer for Escalate | Future research |
| B5 Economic limits | Future research |
| B6 Drift signals | Future research only, under 06's conditions |
| B7 Reachability test | Future research. Ch. 5 item 17 notes that Table 4.34 already reports a reachability analysis **for the learned decision only** |

## 3. Additional corrections applied together with A1–A7

These come from the reconciliation (`5d7828c`, 04), not from A1–A7:
- `R1-1` … `R4-9`;
- the Chapter 5 consequential edits `C5-*`;
- the abstract corrections `AB-*`;
- the terminology edits `T*`.

They are listed in 07 and 10.
