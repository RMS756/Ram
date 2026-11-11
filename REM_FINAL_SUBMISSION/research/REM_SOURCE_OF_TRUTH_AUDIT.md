# REM source-of-truth audit

**Date:** 11 November 2026. **Repository:** `RMS756/Ram`, inspected locally at `/home/user/Ram` after `git fetch --all`. Only files that exist in a branch are listed; nothing is assumed from earlier conversations.

## 1. Branches

| Branch | Head | Date | Content | On GitHub |
|---|---|---|---|---|
| `claude/rem-algorithm-implementation-3ktvze` | `2c915bf` | 11 Nov | designated development branch; contains everything up to the authorization-generalization study | yes |
| `claude/rem-authz-generalization-study` | `2c915bf` | 11 Nov | same head | yes |
| `claude/rem-final-thesis-nov20` | this branch | 11 Nov | final study and final thesis work (`REM_FINAL_SUBMISSION/`) | **no (local only)** |
| `claude/rem-r4-corrections-3ktvze` | `9fddfa7` | 3 Nov | R4/R5 thesis, five-chapter build | yes |
| `claude/rem-authorization-audit` | `4989306` | 8 Nov | authorization failure audit | no (contained in `2c915bf`) |
| `claude/melon-rem-extension` | `cfb4f40` | 6 Nov | MELON integration; review copy | no (contained in `2c915bf`) |
| `claude/rem-offline-validation-melon-prep` | `d8799f9` | 6 Nov | squashed copy of the previous branch | no (local only; content contained in `2c915bf`) |
| `codex/rem-ollama-pilot` | `fca0319` | 3 Nov | local Ollama feasibility pilot | yes |
| `codex/rem-authorization-generalization-experiment` | `e8fade5` | 11 Nov | Codex's authorization candidate; based on `9fddfa7` | yes |
| `codex/rem-multiple-candidates-v2` | `c9851fc` | 11 Nov | Codex's four candidates; based on `9fddfa7` | yes |
| `claude/rem-thesis-lit-review-merge-j1px4f`, `claude/rem-thesis-revision-r2-j1px4f` | `f13f113`, `7e19265` | 27–28 Oct | historical (R1, R2) | yes |

The Codex branches were read and not modified. They do not contain the work on the `claude/` branches after 3 November. The commit `bb4218d` named in an earlier message exists in no branch, locally or on GitHub.

## 2. Authoritative state of each item

| Item | Authoritative source | Status |
|---|---|---|
| Approved five-layer REM design | `CLAUDE.md` (design lock); `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md`; thesis Chapter 3 | Design locked by `CLAUDE.md`. **No supervisor approval of the Chapter 3 specification is recorded** (item SD-FREEZE). |
| Frozen REM implementation | `rem/` at `2c915bf`. Since the R4 thesis commit `9fddfa7` only three files were **added** (`rem/deployment/gateway.py`, `rem/integration/melon_rem.py`, `experiments/pilot/ablation_minimal.py`); no existing file under `rem/`, `configs/` or `experiments/pilot/` was modified. `git diff 4989306 HEAD -- rem/ configs/ experiments/pilot/ results/` is empty | Reproducible. 241 tests pass without study state. |
| Configuration | `configs/exploratory/pilot_e0.yaml` (sha256 `8e1aa107…`) | Declared exploratory values; not approved (D-9). |
| R4 experimental results | `results/pilot_R4/` (written by commit `6fc0952`, 1 November; thesis build `9fddfa7`, 3 November); reproduced on 8 and 11 November to the exact counts (11 / 2,979 and 105 / 334) | Exploratory; offline. |
| Five-chapter R5 thesis | `REM_FINAL_THESIS/final_five_chapters/` (`src/*.md`, `REM_THESIS_5CH_FINAL.docx/.pdf`, 241 pages), built 3–5 November | Latest complete thesis draft. Marked "draft for supervisor review". |
| Review copy | `REM_FINAL_THESIS/review_copy_2026-11-06/` | Adds the planned MELON subsection. |
| Modified Chapter 2 and Chapter 3 drafts | `chapter2/` (systematic review records, PRISMA files); Chapter 3 inside the five-chapter source. No separate later Chapter 3 draft exists in any branch. | — |
| November research updates | Chapter 2, Sections 2.13.6 and 2.13.7 (30 October and 2 November updates); `REM_Authorization_Generalization_Study/01`, `02` (six papers read in full on 11 November) | The six full-text readings are not yet in the thesis. |
| Authorization audit | `REM_AUTHORIZATION_AUDIT/` (`4989306`) | Complete. |
| Authorization-generalization study | `REM_Authorization_Generalization_Study/` (`cca4968` protocol, `2c915bf` results) | Complete; candidate rejected. |
| Final confirmatory study | `REM_FINAL_SUBMISSION/` (`19bd168` protocol, `907e6d2` results) | Complete; verdict GO for one modification. |
| MELON integration | `experiments/melon_rem/`, `rem/integration/melon_rem.py`; frozen bundle sha256 `983c5b0d…` (unchanged) | Implementation verified with scripted agents; **no real-model run**. |
| Live harness | `experiments/live/`, `rem/integration/agentdojo_live.py` | Implemented and tested with a scripted agent; **not executed with a model**. |
| Deployment simulation | `experiments/deployment_sim/`, `results/deployment_sim/` | Executed locally (gateway parity with replay); not a live agent. |
| University thesis template | **Not in the repository.** `audit/FORMATTING_AUDIT.md` records "Al-Balqa Applied University formatting guide: Not available". | **Blocking for final formatting.** The layout used is an assumed A4 thesis style. |
| Supervisor decision register | `SUPERVISOR_DECISIONS_REQUIRED.md`; `REM_FINAL_THESIS/final_five_chapters/audit/UNRESOLVED_SUPERVISOR_DECISIONS.md` | **No supervisor decision is recorded anywhere in the repository.** Every item is open. |

Planning files named in an earlier message (`REM_SOURCE_OF_TRUTH.md`, `REM_CUT_PLAN.csv`, `REM_CUT_PLAN_README.md`, `REM_SCOPE_AND_GAP_DECISION_MEMO.md`) exist in no branch.

## 3. Commit, version, date and dataset of every result set

| Result set | Commit | Run date | Dataset | Mode |
|---|---|---|---|---|
| Pilot R4 (thesis Chapter 4) | `6fc0952` (results), `9fddfa7` (thesis) | 1 Nov 2026 | AgentDojo banking suite v1, package 0.1.35, runs at `089ed468…`; 21 undefended backbones, `important_instructions`; 3,334 episodes, 6,762 steps; 3,313 replay-eligible | offline prediction and recorded-trace replay |
| Deployment simulation | `baffbed` | 5 Nov | same recordings | local gateway parity |
| Authorization audit | `4989306` | 8 Nov | same; 16 synthetic call fixtures | decision traces |
| Authorization-generalization study | `2c915bf` | 11 Nov | same 3,313 episodes; gpt-4o cross-template (681); reformatted-identifier probe (2,645); fixtures sets 1–2 | replay; double holdout |
| Confirmatory study | `907e6d2` (protocol `19bd168`) | 11 Nov | 2,113 episodes from five pipelines never read before; fixture set 3 | replay; frozen models |
| Codex small cohort | `c9851fc` (Codex) | 11 Nov | 135 attacked and 15 benign, one Llama-3.3-70B pipeline, v1.2.1 | replay; reported by Codex, **not reproduced here** |
| MELON | `cfb4f40` | 5 Nov | none | scripted integration tests only |

Environment for all replays: Python 3.11.17, numpy 2.4.6, seed 20261027, `PYTHONHASHSEED=0`.

## 4. Preservation

The original implementation, configuration, `results/pilot_R4/`, the MELON bundle and all earlier thesis versions (R2–R5, five-chapter build, review copy) are unchanged by the final work. New material is confined to `REM_FINAL_SUBMISSION/` and `experiments/authz_study/confirm_a.py`.
