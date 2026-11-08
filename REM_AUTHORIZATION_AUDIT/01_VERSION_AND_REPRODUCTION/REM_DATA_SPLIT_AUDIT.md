# Data split audit

## Primary scheme (used for every reproduced count)

- **Attacked episodes:** the outer fold is the injection task (9 folds: `injection_task_0` … `injection_task_8`).
- **Benign episodes:** the outer fold is assigned to the user task round robin over the 9 folds (`experiments/pilot/data.py:51-56`). The assignment is stored in the frozen bundle under `benign_user_task_fold`. For example, `user_task_0` and `user_task_3` belong to fold `injection_task_0`.
- **Inner model selection:** 4-fold CV for λ, grouped by injection task (attacked) or user task (benign).
- **Calibration:** fitted on inner out-of-fold logits.
- **Benign transition reference (for `x_beh4`):** built from benign episodes outside the held-out fold (`reference_from_mask(data, data.fold != f)`).
- **Consequence for audit traces:** whether a transition such as `read_file → send_money` is "novel" depends on which user tasks fall into the held-out fold. In fold `injection_task_0` that transition is novel, because `user_task_0` ("pay the bill in the file") is held out. In folds 6, 7 and 8 it is not. This is a correct out-of-fold construction, but it makes the verdict on a first payment fold-dependent (`../03_AUTHORIZATION/REM_FOLD_SENSITIVITY.csv`).

## Sensitivity scheme (leave-whole-user-task-out)

- The repository fits this scheme only for probabilistic metrics (`run_main.py:168-180`). The pooled ROC-AUC in this audit's rerun was 0.9431, against 0.9383 primary.
- No enforcement replay under user-task folds exists in the repository.
- The enforcement counts reported for it (original 12 / 2,979 and 110 / 334) come from Codex and were not reproduced.
- Each scheme refits every fold, so counts from the two schemes are produced by different models. Report them side by side as a sensitivity analysis, never as one comparison.

## Data-reuse disclosure

- The same 3,313 episodes have been used for: the original evaluation; the ablations; REMnoEsc (post hoc, declared after R1 results); REM-Lite; the deployment simulation; and Codex's cue, parser and gating arms.
- None of those later arms has an independent confirmatory corpus.
- The fixtures are not a confirmatory corpus either (see `REM_EXPERIMENT_PROVENANCE.md`).

## Leakage check relevant to the fixtures

- The fixture tracer uses only fold `injection_task_0` artifacts from the frozen bundle, which was fitted without that fold's held-out episodes.
- No fixture was used to fit, calibrate, select λ, choose costs or choose thresholds.
- The fixtures share no account identifiers with AgentDojo: every IBAN-like string uses an unassigned country prefix.
