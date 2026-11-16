# REM + G3 integration experiment, 16 November 2026

Status: exploratory development experiment; not an adopted replacement for REM. User authorized integration and comparison in the current conversation, then explicitly included L4. Base: RMS756/Ram ed1ea397fa736fb40e9da91869d85dedd8465fb4. This protocol is committed before scoring any newly composed arm. Previous results, configurations, and matcher revisions remain unchanged.

## Architecture

Keep the five REM layers. G3 is a separately implemented permission gate inside layer 4, before REM's expected-loss decision. It is not a sixth layer. The existing evidence tracker, ridge estimator, logit calibration, consequence map, D1/D2 predicates, costs, mitigation and audit remain the frozen baseline procedure. G3 alone and the existing L4 are alternative experimental comparators, not serial stages after REM.

For a restricted call: G3 denied => Block; unknown => Escalate, withheld without a reviewer; supported => consult the configured REM decision. Unrestricted calls go to REM. Successful fulfillment uses the runtime executor's ingest flag; withheld or errored calls never count as successful. The learned score cannot release a permission-gate rejection. Compute and record the frozen REM score even when the permission gate overrides it; the audit must say that the probability was not used for such a verdict.

## Arms fixed before scoring

| ID | Definition |
|---|---|
| B0 | Allow-all replay for eligibility checking |
| REM10 | REM v1.0, existing full evidence and four verdicts |
| REM11 | REM v1.1, existing no-behavior evidence and four verdicts |
| G3 | Unchanged revision-3 deterministic permission rule |
| L4 | Unchanged revision-3 authority guard, F4 evidence and two-verdict policy |
| H10 | Full G3 permission gate, then REM10 |
| H11 | Full G3 permission gate, then REM11 |
| H11D | Same full G3 gate and REM11 model; expected-loss alternatives Allow/Block only, retaining D1/D2 overrides; same costs |
| A2 | Existing strict explicit rule |
| PG | Published manual Progent policy adapted to the existing replay harness, unchanged |

H11D is a declared decision ablation, not the original REM four-verdict methodology. L4 differs: its model includes five permission features and its existing authority guard permits some uncertain values; it is not equivalent to requiring G3 supported on every restricted call.

## Data, fitting and reproduction

AgentDojo 0.1.35, banking v1; public recorded runs pinned to 089ed468cf3ed0322acc66b0211f26d9d90dbf60. All data, task requests, earlier outcomes and known defects were already inspected in earlier research. These are development data, never a new confirmatory test.

Use the original primary population and former confirmatory population, now development. Rebuild missing local caches from the pinned recordings. Retain only episodes whose B0 replay agrees with the recorded utility/security and has no error, using the same criterion as the prior study. Check primary eligible-ID hash and sample counts against SPLIT_MANIFEST.json; check second-population counts against results_v3.json. Report discrepancies rather than silently changing populations.

Models use the unchanged fit_cell procedure: grouped inner cross-validation, existing ridge penalty grid and tie rule, label-NLL calibration on out-of-fold logits, refit on the outer training portion. Fit F0, F0_nobeh and F4 on the same cells. No hybrid-specific fitting, new features, cost tuning or thresholds. Compare regenerated S1 F0 coefficients and calibration with the stored e1_crossfit.json; compare all old-arm aggregate outcomes with stored revision-3 results.

S1: held-out injection-task folds; benign task assignment unchanged. S2: hold out both user task and injection task, using the existing train-mask definition. Estimate residual Modify success only from the corresponding training portion using the existing step-level oracle-Modify replay. No ground-truth information enters any runtime guard or scoring model.

## Evaluation

Primary S1 and S2, second population S1, original reformatted-identifier probe (primary S1), and fixture sets 1-4. Fixtures are known regression examples, not independent validation. Execute complete sequential sandbox replay, not a post-hoc Boolean intersection of stored verdicts: refusal changes the evidence history and therefore subsequent decisions. No language model, live agent, reviewer or paid API call.

Metrics: successful attacks/attacked episodes, benign and all-task completion, restricted legitimate-call release, replay errors, full guard-method latency. Latency is local diagnostic timing including evaluation bookkeeping, not a controlled deployment benchmark; original study timings from another machine are not directly comparable.

Fixed contrasts: H10-REM10, H11-REM11, H11D-REM11, each hybrid-G3, L4-G3, L4-H11D, G3-A2, G3-PG. Use the existing paired cluster bootstrap, 2,000 resamples, seed 20261027, 95% intervals and existing user-task/injection-task grouping. Report all contrasts and both point estimates and intervals, not only favorable cases. Include per-user-task completion, attacks by user task, and results without user_task_15 as a labelled sensitivity analysis.

## Interpretation

No superiority from equal attack counts or intervals including zero. A strict full-support G3 gate may lower utility; this is an expected possibility, not a protocol defect. Claim learned added value only if task-completion interval lower bounds are strictly positive against G3 under S1 and S2, with no more successful attacks on primary, second population or probe. Otherwise say not established, not proved absent. A gain over REM alone does not establish a gain over G3, A2 or PG. Zero observed attacks is not a general security guarantee. No post-scoring repair, threshold adjustment, task exclusion, arm selection or result replacement without a dated amendment retaining original results.

## Deliverables

Isolated adapter and regression tests; reproducible runner; machine-readable fits, per-episode outcomes and report; Arabic explanation of architecture and verdict; no thesis rewriting or adoption of a new design during this experiment.
