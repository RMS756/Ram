# Validity, tests and recommendation

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

**333 tests passed with no skips**, including original regression tests, previous AA tests, 53 new policy tests and 5 evaluation-integrity tests. The final log records a dependency deprecation warning, not a failed check. No official code/config/result/thesis file changed.

The new tests cover fragmented/zero-width IBANs, token boundaries, legitimate values also present in external context, unknown provenance, amount-only attacks, full-request parsing/negation/quoting, unseen beneficiaries, incoming versus outgoing receipts, missing/untrusted/duplicate receipts, malicious metadata, malformed financial values, alternate tools, source separation, one-use retries, C4 ablations, actual repaired native execution and terminal no-tool recordings. Real artifact checks verify split separation, all 750 unchanged primary control outcomes against the previous study, metrics recomputation, run/sample counting and full-trace completion.

## Experimental safeguards

The protocol was frozen before new outcomes, but all retained data and previous findings were already known. Candidate engineering is informed by this corpus. It is **not an independent final held-out evaluation**. C4's narrow language grammar was informed by known task forms; no general semantic authorization claim follows.

Original ridge fitting/calibration/grid choices use fitting-only folds. r_mod is recomputed for each objective/task grouping from fitting-only original oracle-withholding runs. It remains a label-coverage/NO-ADAPT surrogate, not measured human intervention effectiveness. No test outcomes select penalties, candidate parameters, costs or numeric security thresholds. Missing calibration is not silently replaced with raw probabilities. All observed calibrated folds were available; no-tool terminal episodes require no scorer and remain in episode denominators.

Paired 2,000-resample percentile intervals use task clusters for benign utility, objective clusters for attacks and task-cluster attack sensitivity. Neither one-way grouping fully addresses crossed dependence; the small grid limits inference. Repeated steps, policy reruns and alternate horizons are not independent samples. Zero-event bootstrap intervals are degenerate descriptions, not upper population-risk bounds. No multiple-comparison significance claim is made.

Schemas and provenance are not complete authorization: C2 can miss actions with invented/unseen provenance, and C3 explicitly misses amount-only manipulation. C4's trusted host is assumed uncompromised, with genuine bank financial fields; the independent provider needs deployment-specific authentication. No real bank, LLM API, real human reviewer or cross-benchmark transfer was used.

## Recommendation

- Keep original REM reproducible and all candidates experimental.
- Treat C2's fragmented-argument handling as an engineering candidate for further validation. It matches simple provenance on the primary security/benign point and costs one attacked-task utility outcome, so no superiority claim is justified.
- Reject C3 as an adopted policy: benchmark ASR conceals a demonstrated threat gap.
- Do not call C1 a security-preserving improvement: the primary attack count increased.
- Evaluate C4 on a future *covered*, independently annotated workload; current zero coverage cannot support or refute its intended efficacy.

The source review favors a defensible empirical contribution about risk estimation, consequence-aware policy and intervention burden, rather than inventing a new mathematical method. Neither original thesis questions nor chapter wording are changed. Live testing remains optional within the user's stated scope, with the replay/adaptation limitation prominent.
