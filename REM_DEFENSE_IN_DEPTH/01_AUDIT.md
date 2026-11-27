# Audit of the REM research project (27 November 2026)

Branch `claude/rem-algorithm-implementation-3ktvze`, created from commit `7b50067` plus the humanized edition (`f59ff5c`). Every study folder, the original thesis, the source code and the experimental records were left untouched. New work is confined to `REM_DEFENSE_IN_DEPTH/`.

## 1. Inventory

| Asset | Location | State |
|---|---|---|
| Thesis, defence-ready edition | `REM_DEFENCE_READY_THESIS/` | Unchanged. 272 pages; 498 table cells verified against raw records |
| Thesis, humanized edition | `REM_HUMANIZED_THESIS/` | Language-edited copy (118 logged edits); numbers, citations and tables verified identical |
| Framework | `rem/`: about 5,200 lines in 29 modules | Five layers implemented, except the injection classifier x~ctx1~ (D-8). Fail-closed configuration. |
| Configuration of record | `configs/exploratory/pilot_e0.yaml` | Declared, not approved (SD-FREEZE) |
| Experiment code | `experiments/`: 20 study packages | Each study imports `rem/` unchanged |
| Studies with protocols | 23 `REM_*` folders, 16 of which hold committed protocols or hashes | Protocol-before-scoring practice is consistent from 11 November 2026 onward |
| Recorded data | AgentDojo repository `runs/` at commit `089ed468`, AgentDojo 0.1.35 | Present and readable. The step dataset rebuilds bit-identically (Section 3). |
| Tests | `tests/`: 857 tests | **0 failures, 0 errors, 28 skipped** (run of 27 November 2026) |
| Git history | 136 commits on this branch | — |

## 2. Status of every REM control

The five classes requested: **I** = implemented; **I-NE** = implemented but not independently evaluated; **P** = proposed; **V** = experimentally validated (development data, replay); **R** = requires new data or resources.

| Layer | Control | Status before this audit | Evidence |
|---|---|---|---|
| Input & Context | Provenance labeling (trusted, semi-trusted, untrusted) | I, I-NE | No experiment removes it: every evidence feature depends on it (Section 4.5.4) |
| Input & Context | Invisible-character hygiene of REM's copy | I | A1h: changes 0 of 16,727 outputs |
| Input & Context | Entity extraction | I, I-NE | As above |
| Detection | Instruction-pattern indicator x~ctx2~ | I, V (no effect) | A2a, A2b: no outcome change |
| Detection | Injection classifier x~ctx1~ | **P, R** | Not implemented (D-8) |
| Behavioral Analysis | History features x~beh1–4~ | I, V | A3a: removing them raises utility and changes no attack count. **This audit adds:** they carry depth (Section 5). |
| Behavioral Analysis | Action/provenance features x~act1–3~ | I, V | A3b: discrimination 0.938 against 0.799; more attack calls without them |
| Decision Engine | Ridge estimate + Platt calibration | I, V | A4c: calibration changes no attack outcome |
| Decision Engine | Consequence tiers + expected-loss verdict | I, V | A4d: thresholds admit 153 more attacks, at 19.5 points more benign completion |
| Decision Engine | Predicates D1/D2 | I, V (no effect) | A4b. They fix no attack-labeled verdict (DiD-1, A6) |
| Decision Engine | Audit record, linear attribution | I | Audit-only by design; additivity checked as a test invariant |
| Mitigation | Step-level enforcement | I, V | A5 (shadow mode): without enforcement, protection is zero |
| Mitigation | Modify/Escalate as distinct effects | I, I-NE | They coincide without a reviewer (A4e). **R:** a reviewer or a live agent is needed. |
| Cross-cutting | CUSUM (observe-only) | I | Observe-only result reported; never in the verdict path |
| — | REM v1.1 (behavioral family removed) | P | GO on the confirmatory rule (utility). **This audit adds:** it loses depth under evasion (Section 5). |
| — | Live closed-loop evaluation | **R** | Needs a model and a budget |

## 3. Reproducibility checks performed in this audit

| Check | Result |
|---|---|
| Rebuild of the labeled step dataset from the recorded runs with the unchanged pilot code | `dataset_summary.json` identical on every field: 6,762 steps, 921 attack-labeled |
| Re-run of pilot E0, cross-fitting, r~mod~ and observe-only stages in an isolated directory | `e0_pilot.json`, `e1_crossfit.json` and `e2_e5_e6_observe_only.json` identical to `results/pilot_R4/`: 0 differing fields |
| Replay gates of DiD-2 | REM 11, P1 12, P2 12, B0 672 of 2,979; REM 105 of 334 benign; probe REM 11, P1 191, P2 12, B0 553 of 2,645. All equal to the stored values. |

## 4. Gaps found

1. **"Five layers" has never been shown to give Defense in Depth.** All earlier ablations remove a component and *refit* the model (training-time ablation). None asks what happens when an attacker defeats a control at test time, which is the Defense-in-Depth question. This gap is addressed by DiD-1 and DiD-2.
2. **The Detection layer has no independent signal.** Its only implemented indicator, x~ctx2~, also feeds x~beh1~ (coupling 1, Section 4.5.4), and its classifier is absent.
3. **No control is specific to credential-change attacks** apart from the behavioral and provenance signals (Section 5).
4. **The decision to adopt REM v1.1** was evaluated only on attack counts without evasion.
5. **Modify, Escalate, the label audit and live evaluation** remain blocked by missing resources (R), as before.

## 5. Results of the new experiments

See `05_DID_RESULTS.md`.
