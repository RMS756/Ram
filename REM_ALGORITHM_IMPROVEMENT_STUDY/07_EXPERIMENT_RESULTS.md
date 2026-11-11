# Actual experimental results

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

## New consistent-version cohort — NO-ADAPT replay

| Policy | Native replay ASR | Benign task success |
|---|---:|---:|
| B0 | 73/135 (54.07%) | 9/15 (60.00%) |
| B1 | 31/135 (22.96%) | 9/15 (60.00%) |
| REM_R4 | 5/135 (3.70%) | 6/15 (40.00%) |
| x_act1 | 0/135 (0.00%) | 7/15 (46.67%) |
| AA_REM | 0/135 (0.00%) | 5/15 (33.33%) |

`REM_R4` here means the original policy **refitted on this smaller cohort**, not the historical published R4 rate. Same environment, agent recordings, retained tasks and outcome scorer are used for all five rows. Four AA component ablations also ran and have the same episode outcomes as AA_REM.

AA_REM minus refitted REM: benign success **−6.67 percentage points**, paired 95% task-bootstrap interval **[−20.00, 0.00]**; ASR **−3.70 points**, objective-bootstrap interval **[−11.11, 0.00]**. Against x_act1, ASR is identical while benign success is **−13.33 points**, interval **[−33.33, 0.00]**. These intervals are descriptive and depend on clustering; see the crossed-dependence limitation in protocol §metrics.

The x_act1 rule weakly dominates AA_REM in the observed security–utility plane. No evidence supports adoption of AA_REM as an improved REM algorithm. Zero observed attacks after withholding all mutations is not a novel security result.

## Why the candidate fails to improve utility

There are **zero independently verified structured grants** in these recordings. Of 442 offline decisions, 255 are permitted banking reads, 168 lack evidence and 19 fail mutation/schema checks. It never exercises positive transaction authorization or safe repair on benchmark data. Therefore this experiment tests missing-evidence behavior and cannot measure the intended benefits of accurate contract acquisition.

Offline diagnostics (attempt-label proxies): AA_REM recall 1.000, precision 0.5829, y=0 withheld rate 0.2342; x_act1 recall 1.000, precision 0.6337, y=0 withheld 0.1892. Refitted REM recall 0.9450, precision 0.5954. These are not independent authorization adjudications.

## Model quality and overhead

Refitted original REM calibrated ROC-AUC **0.88456**, average precision **0.74639**, ECE **0.08100**, binary Brier **0.09990**. Uncalibrated Brier is **0.09959**, so calibration does not improve this metric. Full model and ablation details are in `artifacts/model_metrics.json`.

Decision-only microbenchmark, 300 calls with tracemalloc enabled: median **0.007952 ms**, p95 **0.036967 ms**, peak traced allocation for the entire batch **16,030 bytes**. This excludes agent/tools and is not a full-pipeline or RSS memory comparison. Machine-specific measurements are descriptive.

## Historical reproduction

The complete original pipeline finished with exit code 0. Its replay ASR/benign utility match the historical files exactly: B0 22.5579%/52.3952%; B1 5.5052%/50.8982%; original REM no-reviewer 0.3693%/31.4371%; idealized reviewer utility 49.7006%. Of 6,207 shared JSON fields, 5,510 are exactly equal; 243 differ in provenance/timing/memory and 454 in numerical analytical values (maximum absolute difference 1.11e-14). These numerical differences are consistent with roundoff across Python/NumPy/BLAS versions, but the rerun is not bit-identical. The full difference listing and raw rerun outputs are archived. Final status is recorded in `artifacts/historical_reproduction_summary.json`. Historical rates must never be mixed with the new 150-episode cohort. See the reproduction guide.

## Evidence limits

ASR counts are native simulator outcomes with a fixed recorded actor. Refusals do not cause replanning. There is one historical backbone in the strict cohort, no human authorization labels, no real bank, no learned intervention outcomes and no adaptive attacker. The candidate should not replace the thesis method.
