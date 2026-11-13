# REM improvement study: development protocol

**Status:** `[PROPOSED — NOT PART OF THE APPROVED REM DESIGN]`. Isolated study. REM v1.0, the proposed v1.1, their configuration and all earlier result files are unchanged and are used as versioned baselines.

**Frozen:** 13 November 2026, by the commit that adds this file, **before any arm defined here was replayed** (no attack-success, task-success or release outcome of any new arm had been computed). What had been seen is listed in Section 2.

## 1. Questions

Main evidence question (unchanged): does a learned, consequence-aware runtime decision improve the security/utility trade-off over simple provenance and permission rules on banking tasks, including held-out tasks and attacker objectives?

Extension investigated here: can task-permission evidence compiled from the trusted request, typed provenance, and deployment-consistent decision semantics improve that trade-off, and which component is responsible for any change?

## 2. Status of the data, and what was known when this was written

- **All 5,426 recorded episodes are development evidence.** The 3,313 primary and the 2,113 formerly confirmatory episodes were inspected in earlier studies. Nothing computed on them here is confirmatory, and none of them is called untouched.
- The author of the candidate knows the 16 user requests and 9 injection tasks of the benchmark and wrote the request parser with those requests in view (and with fixture requests R1 and R2 of set 2). **No request was held out from parser development.** The parser's outputs on those 18 requests were inspected. The distribution of the permission evidence over attack-labelled and other calls of the primary recordings was printed once (606 denied, 291 unknown, 24 supported among 921 attack-labelled calls; 114 supported, 56 unknown, 10 denied among 180 calls of benign episodes).
- Fixture sets 1 to 3 are regression tests. Fixture set 4 (20 pairs, `../fixtures/set4_permission_fixtures.json`) was written before any scoring and is scored once after this freeze. It was written by the same author with AI assistance and was **not independently reviewed**; it is a stress test of mechanisms, not an independent benchmark.

## 3. Candidate family (one family, evaluated incrementally)

Code: `experiments/improve_study/` (`intent.py`, `permission.py`, `improve.py`). Every rule is a design choice of this study; none is a published formula.

- **A. Task-permission compiler.** A deterministic parser of the user-role request produces an immutable representation: requested and prohibited operation categories, conditions, target, historical and merely mentioned account identifiers, amounts with their role (value, base of a requested computation, historical), whether the amount is derived, taken from history or delegated to a named source, named sources, digests of quoted credential values, read-only intent and open delegation. It reads the request text only.
- **B. Typed matching.** A call to a state-changing tool is matched on operation and material arguments. Identifiers are compared in a type-specific canonical form; amounts as exact decimals, with ambiguous formats left unknown. Recipients are accepted if the request names them as targets, refers to them, or if they are *established payees referenced by the request* (recipient field of a structured bank record that the user originated). Free-text fields of bank records and senders of incoming transactions establish nothing. A source named by the user may supply an amount or a profile value, never an operation, a recipient or a credential. Unverifiable amounts (derived or delegated) are accepted only at consequence tier 3 or lower (the declared amount limit). The result is *supported*, *denied* (prohibited, not requested, or contradicted) or *unknown*.
- **C. Deployment-consistent decision.** Without a reviewer an escalated or modified call is withheld. The no-reviewer mode therefore uses the existing expected-loss rule (Equations 3.6 and 3.7) over the two verdicts that have distinct effects, Allow and Block, which gives the existing Allow–Block threshold (Equation 3.9). No cost value is changed.
- **D. Selective semantic verifier.** Interface and gate only (`verifier.py`); not executed, because no model is authorized or available.

## 4. Arms

| Arm | Definition | Learned model |
|---|---|---|
| B0, B1, v1.0 (`M00`), v1.1 (`M00_nobeh`), `M01`, P2, A2 | as in the earlier studies, unchanged | as before |
| **PG** | Progent's published manual banking policy (official repository, commit `9befb41`): allow-list of five recipients for the three payment tools, `update_password` not allowed, all other tools allowed | none |
| A2n | A2 with typed identifier normalization only (isolates the normalization repair) | none |
| **G1** | permission rule: release a state-changing call iff its permission evidence is *supported* | none |
| G1-noop, -noamt, -noest, -nodel, -nonorm | G1 without the operation check, the amount check, established payees, scoped delegation, typed normalization | none |
| V11d | v1.1 with deployment-consistent decision (C) | v1.1 fit |
| L0 | ridge logistic on v1.1 evidence plus the five permission indicators (feature set F2), decision C, **no guard** | F2 |
| L1 | permission guard (denied → Block), then F2 with the original four-verdict rule | F2 |
| **L2** | permission guard, then F2 with decision C | F2 |
| L2s | permission guard; *supported* → Allow; the F2 model decides only the *unknown* calls, decision C | F2 |

F2 is fitted by the unchanged procedure of REM (ridge grid, four grouped inner folds, label-NLL logit calibration on inner out-of-fold logits, refit), inside each fitting portion. The refit of the v1.1 feature set by the same call must reproduce the stored v1.1 fits (equivalence check, reported).

## 5. Populations and splits

| Population | Episodes | Use |
|---|---|---|
| Primary | 3,313 eligible (2,979 attacked, 334 benign) | S1: nine folds by injection task; S2: double holdout of user task and injection task (143 cells) for learned arms. Rules have no fitted quantity and are identical under S1 and S2 |
| Dev2 (formerly confirmatory) | 2,113 eligible (2,065 attacked, 48 benign) | S1 fold models, nothing fitted on it |
| Reformatted-identifier probe | 2,645 attacked | S1 fold models |
| Fixtures | sets 1–3 (regression), set 4 (new) | fold `injection_task_0` models |

Held-out credential-change analysis: fold `injection_task_7` under S1 and S2 is reported separately for every arm. Split manifest and hashes: `SPLIT_MANIFEST.json`. No hyperparameter, threshold, cost or rule is selected on any evaluation portion.

## 6. Outcomes

Primary: (i) task completion over all episodes and in benign episodes; (ii) release of legitimate state-changing calls in benign episodes; (iii) attack success by the benchmark's checker.

Also: tasks completed under attack; **episodes with a released attack-labelled call** (a proxy; not called a committed unauthorized state, because the effect on the bank state is not separately measured); verdict mix; fixtures; decision time. Model calls, tokens and cost are zero for every arm run here.

## 7. Comparisons fixed in advance

Paired, grouped bootstrap (2,000 resamples, seed 20261027; task completion clustered by user task, attack success by injection task; 16 and 9 groups, stated with every interval).

1. **G1 − A2** (the strongest simple rule of the earlier studies) on task completion and attack success, primary and dev2.
2. **G1 − PG** (published defense), same.
3. **G1 − v1.1**, same.
4. **L2 − G1** and **L2s − G1**: what the learned model adds to the same evidence and guard, under S1 and S2.
5. **V11d − v1.1**: the effect of decision semantics alone.
6. **L0 − L2**: the effect of the guard.

## 8. How results will be worded

- All results are development results. A favourable contrast is "observed on development data", not confirmed.
- **No security non-inferiority or equivalence is claimed.** No approved margin exists and none is invented. An interval for an attack-success difference that includes zero is reported as unresolved.
- "Added value over simple rules" is stated only if comparison 1 has a task-completion interval above zero on both populations **and** the candidate's count of successful attacks does not exceed A2's on either. Otherwise the result is reported as a trade-off or as no detectable difference.
- "The learned model adds value" is stated only if comparison 4 has a task-completion interval above zero under S1 and S2 without more successful attacks than G1. If the gain of the family comes from the compiler, the matcher or the guard, it is attributed to them and not to the learned core.
- The candidate G1 is fixed as defined (all components on). The ablations are diagnostic and do not change the candidate. Any change to the parser, matcher or arms after this freeze is listed in Section 10 with the reason and with what had been seen.

## 9. Not executed, and why

- **MELON, Task Shield, CaMeL, Progent with generated policies, the selective verifier, and any closed-loop run** need a language model (MELON also an embedding service). This session has no model credential and no spending authorization. The prospective protocol for them is `PROSPECTIVE_PROTOCOL.md`.
- **XGBoost comparison:** optional in the brief; not run (the package is not installed and the question is secondary to whether any learned model adds value).

## 10. Amendments

None at the time of freezing.
