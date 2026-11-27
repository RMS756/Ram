# A. Current architecture: REM v1.0 as implemented

This is a description of what exists. Every statement is traceable to code under `rem/`, to the configuration of record `configs/exploratory/pilot_e0.yaml`, or to a measured result.

## Pipeline (frozen order, `rem/core/pipeline.py`)

provenance labeling → context, behavioral and action evidence → ridge logistic regression → Platt calibration on the logit → consequence tier → policy predicates → expected-loss Bayes verdict → deterministic mitigation → audit record.

## Layer by layer

| Layer | Implemented mechanism | Code | Measured behavior |
|---|---|---|---|
| **1. Input & Context** | Provenance labels per segment (trusted ≻ semi-trusted ≻ untrusted); content derived from several segments inherits the least-trusted label; invisible-character hygiene on REM's copy; entity extraction (IBAN-like identifiers, amounts, passwords, profile values, tool names) | `rem/algorithms/context/provenance.py`, `rem/algorithms/behavior/evidence.py` | Foundation of the action evidence. Not separately removable. The exact-string match is defeated by reformatting (probe). |
| **2. Detection** | x~ctx2~: union of 5 declared regular expressions and tool-name mentions over untrusted segments added since the last decision point | `rem/algorithms/detection/instruction_patterns.py` | Content-level precision 1.00 and recall 1.00 on the fitting template. Recall 0.00 on two other templates. Duplicated by x~beh1~ (correlation 1.00). **No measurable contribution** to outcomes (A2a, A2b, DiD-2). x~ctx1~ classifier **not implemented** (D-8). |
| **3. Behavioral Analysis** | History: x~beh1~ (shift after a pattern-matching result), x~beh2~ (repeats), x~beh3~ (privilege escalation), x~beh4~ (transition unseen in benign data). Action: x~act1~ (key argument only in untrusted content), x~act2~ (recipient not in the user objective), x~act3~ (sensitive egress) | `rem/algorithms/behavior/evidence.py` | Two families. Each alone covers most attacks; both are needed (DiD-2: 131 and 90 attacks when one is evaded; 669 when both are). Low specificity (x~beh3~ fires on 71% of legitimate state-changing calls). |
| **4. Decision Engine** | Ridge logistic estimate (9 parameters), logit calibration, declared consequence tiers (1–4), predicates D1 (prohibited tool) and D2 (missing required evidence at high tier), expected-loss verdict over Allow/Modify/Escalate/Block with tier-indexed declared costs; linear attribution in the audit only | `rem/algorithms/detection/ridge_logistic.py`, `calibration/`, `decision/`, `a3.py` | Accounts for all 661 prevented attacks. Withholds 81.5% of legitimate state-changing calls. D1/D2 fix no attack-labeled verdict. |
| **5. Mitigation** | Step-level semantics: Allow releases; Block withholds the current call; Escalate withholds pending review; Modify withholds with a tool-restriction notice for this call only. No episode-level persistence in the reference semantics. | `rem/core/mitigation.py`, `rem/integration/agentdojo_replay.py`, `rem/deployment/gateway.py` | Enforcement carries all protection (shadow mode: none). Without a reviewer, Modify, Escalate and Block coincide. |
| Cross-cutting | Offline fitting and recalibration (nested grouped cross-fitting); append-only audit record; optional observe-only CUSUM | `rem/evaluation/`, `rem/core/audit.py`, `rem/algorithms/behavior/cusum.py` | Not a layer |

## What REM v1.0 does not have

- No trusted representation of what the user authorized. Its only trusted input is the request text.
- No authorization check at all: D1 is a static list, and D2 checks only that evidence is available.
- No detection signal tied to a specific call.
- No tracking of retries or alternative attempts after a refusal. x~beh2~ counts identical repeats, and replay cannot exercise adaptation.
- No independent Modify mechanism. Tool restriction for one call has the same effect as Block.

## Diagram

See `figures/fig_rem_v1_0_current.png`.
