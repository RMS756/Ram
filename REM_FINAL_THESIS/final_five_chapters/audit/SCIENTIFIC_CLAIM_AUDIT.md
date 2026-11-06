# SCIENTIFIC CLAIM AUDIT — five-chapter thesis

**Scope.** `final_five_chapters/REM_THESIS_5CH_FINAL.docx` / `.pdf` (241 pages), generated from
`final_five_chapters/src/*.md`. Every quantitative claim was carried over from R5 unchanged;
`audit/qa_logs/content_preservation.txt` confirms that none of the 360 distinct numerical values
of R5 occurs fewer times in the new text. **No result was added, removed, rounded differently or
re-computed for this version.** New text adds only: background (§1.1.1–1.1.4), organisation
(§1.12), the live-harness design and status (§3.17, §4.12, §4.13), chapter summaries (§3.18, §4.18),
a Chapter 5 introduction and limitations summary (§5.1, §5.5), and six new figures (four diagrams,
one plot of declared equations, one chart of existing replay values).

**Evidence grades used below.**
- **Implemented/tested:** code exists and automated tests pass (217 passed on 3 Nov 2026,
  `experiments/live/smoke_output/pytest_full_with_live.log`; 205 of them are the pre-live suite
  reported in Table 3.22 as run on 1 Nov 2026).
- **Exploratory (recorded traces):** computed from the recorded AgentDojo traces with declared
  exploratory design values (`pilot_e0_exploratory`); reproduced by re-execution with
  0 analytical differences (`verification/reproduction_comparison_R4.json`).
- **Assumption-driven:** depends on the NO-ADAPT replay assumption (the agent does not adapt to a
  refusal) or on an idealised reviewer.
- **Not executed:** design and code only; no result.
- **Record-level literature:** metadata/abstract verified, full text not read.

## 1. Chain from problem to conclusions

| Link | Thesis location | Content | Audit finding |
|---|---|---|---|
| Problem | §1.2 | Indirect prompt injection can lead a tool-using financial agent to propose an attacker-serving state-changing call | Supported by record-level literature (Greshake et al., 2023; Debenedetti et al., 2024; OWASP). Consistent with the threat model (§3.3). |
| Gap | §1.4, §2.13 | No prior work combining calibrated per-step probability, consequence-indexed expected-loss verdicts with four actions, and measured deterministic mitigation, on an open banking benchmark under a same-estimator baseline | A *combination* gap stated at record level. Chapter 2 itself lists close neighbours (NEXUS, AgentTrust, FinHarness, Chen 2026, Kanaker 2026), so the gap is narrow and not a "first" claim. The thesis does not claim novelty of any mechanism (§1.11, §3.13). |
| Aim | §1.5 | Derived from the objectives; adds nothing | Correctly labelled as derived. |
| Objectives O1–O3 | §1.6 | Approved proposal objectives (design; evaluate against attacks; compare with existing approaches) | Quoted, not reworded. Scope restriction (banking only) stated. |
| Research questions RQ1–RQ4 | §1.7 | Derived from objectives | **Marked [PD], not supervisor-confirmed (D-10 / RQ-CONFIRM).** |
| Methodology | Ch. 3 (§3.1–3.15) | Five layers; ridge LR; logit calibration; tiers; predicates; expected-loss verdict; deterministic mitigation; audit; nested grouped cross-fitting | Matches the frozen pipeline in `CLAUDE.md` (five layers; CUSUM observe-only; attribution audit-only; no forbidden component reintroduced). Design values declared exploratory. |
| Implementation | §3.16 | Software and verification | Implemented/tested. Injection classifier absent (stated). |
| Live design | §3.17 | Closed-loop AgentDojo harness: B0, B1, REM; fail-closed runner | Implemented/tested with scripted agents; **not executed with an LLM**. |
| Experiments | Ch. 4 (§4.1–4.11) | Offline classification, observe-only decisions, NO-ADAPT replay, ablations, observe-only CUSUM, loss grid, label checks, distributed-defense records | Exploratory; reproduced. |
| Live status | §4.12–4.13 | NOT EXECUTED; replay vs live | No live number appears anywhere in the thesis (checked: `LIVE_EXPERIMENT_RESULTS.md` states "NOT EXECUTED. NO LIVE RESULT EXISTS"). |
| Conclusions | Ch. 5 | RQ answers limited to the kinds of evidence; O1 achieved for banking; O2, O3 partly; central practical claim **unestablished** | Justified by the evidence and appropriately bounded (see §3 below). |

## 2. Quantitative claims (headline set) and their grade

| Claim (as stated) | Location | Source file | Grade |
|---|---|---|---|
| 21 real LLM agents; 3,334 episodes; 6,762 proposed tool calls | Abstract; §4.2 | `results/pilot_R2/dataset_summary.json` (21 primary groups; 19×159 + 156 + 157 = 3,334 episodes, re-checked in this pass) | Exploratory (data description) |
| Pooled ROC-AUC 0.938 on held-out attacker objectives; 0.86–0.98 per held-out objective | Abstract; §4.4; Table 5.1 | `e1_crossfit.json` | Exploratory |
| ECE 0.044; no calibration improvement observed | §4.4; Table 5.1 | `e1_crossfit.json` | Exploratory; "no improvement observed" is not a claim of no effect |
| Action evidence dominates; behavioral features not attack-specific in this benchmark | Abstract; §4.7 | `e1_crossfit.json`, `feature_firing_rates.json` | Exploratory |
| Intervention on 97.3% of attack steps and 22.7% of legitimate steps (REM) vs 74.0% / 5.6% (B1) | Abstract; §4.5 | `e2_e5_e6_observe_only.json` | Exploratory, under declared costs |
| Replay ASR 0.004 (REM) vs 0.055 (B1, step-level) and 0.046 (B1, episode-level) | Abstract; §4.6 | `e4_e5_enforcement_replay.json` | **Assumption-driven (NO-ADAPT)** |
| Benign-utility cost −18 to −20 points without reviewer, ≈ 0 with idealised reviewer | Abstract; §4.6; Table 5.1 | `e4_e5_enforcement_replay.json` | Assumption-driven (reviewer bound) |
| r_mod and residual ASR ≈ 0 | §4.6; Table 5.1 | `e4_rmod_and_replay_validity.json` | Assumption-driven, stated as such |
| Escalation on 19.6% of steps (0.196, Table 4.5) | Table 5.1 (RQ3 row); §4.5 | `e2_e5_e6_observe_only.json` (`escalation_rate` 0.19565) | Exploratory, **observe-only** (Table 5.1 lists it in the RQ3 row whose evidence column reads "Replay; runtime measurement"; the value itself is observe-only, as §4.5 states) |
| Complete-call processing median 0.21–0.28 ms, p95 0.49–0.70 ms | §3.16.14; Table 3.25; Table 5.1 | `results/pilot_R4/e4_e5_enforcement_replay.json` | Implementation measurement in one configuration; not full-system latency |
| A re-execution of the full pipeline in a fresh environment reproduced every analytical result (R5 wording "independent re-execution" **corrected in this version**) | Abstract; §4.2; §4.6 memory note | `verification/reproduction_comparison_R4.json` (diff_analytical = 0 in every file) | Re-execution of the project's own code from a clean state, **not an independent replication by another team**. R5 called it "independent"; under the rule "never claim independent validation unless independently reproduced" the word was removed from the abstract (English and Arabic) and from §3.16.2 (Table 3.18), §3.16.11.2, §4.2 and §4.6. |
| 205 tests (Table 3.22, §3.18, §5.4) | Ch. 3, Ch. 5 | `verification/pytest_R4.txt` | Accurate for the pre-live suite; the current suite is 217 (with 12 live-integration tests, Table 3.26). |

**Statistical significance.** The thesis reports bootstrap intervals and descriptive comparisons
only. No significance test is claimed, and none was added in this version. Repeated episodes of the
same task pairing are not treated as independent (grouped resampling by attacker objective / task).

## 3. Conclusions and whether they are justified

| Conclusion | Justified? | Basis / limit |
|---|---|---|
| Tool-boundary evidence separates attack attempts from legitimate calls on unseen attacker objectives in AgentDojo banking | Yes, as exploratory | Held-out predictions; one benchmark, one suite, recorded traces |
| Calibration produced no observed improvement | Yes | Observed only; small calibration sets |
| Expected-loss verdicts with tier-indexed costs intervene more than the same-estimator baseline, at a utility cost | Yes, as exploratory | Under declared exploratory costs, not approved ones |
| REM reduces attack success in a non-adaptive replay | Yes, **conditional on NO-ADAPT** | Replay assumption stated everywhere the number appears |
| REM protects a live or adaptive agent | **Not claimed; not justified** | Live experiment not executed |
| REM is superior to published defenses | **Not claimed** | No shared-protocol comparison |
| REM introduces a new algorithm | **Not claimed** | §1.11, §3.13, §5.4 state the opposite |

## 4. Contribution table

| Claimed Contribution | Supporting Source | Experiment | Evidence Strength | Limitation |
|---|---|---|---|---|
| C1. Specified and implemented five-layer composition (provenance evidence; ridge LR with logit calibration; tiers and predicates; four-verdict expected-loss rule; deterministic mitigation; audit record with non-influencing attribution); fail-closed on undeclared design values | Ch. 3 §3.1–3.10, §3.16; code in `rem/`; constituent mechanisms attributed (Cox 1958; le Cessie & van Houwelingen 1992; Platt; Guo et al. 2017; Elkan 2001; Chow 1970; Lundberg & Lee 2017) | Unit and integration tests (205 pre-live; 217 total) | Strong for "implemented and behaves as specified"; none for security effectiveness by itself | Injection classifier absent; design values exploratory; no mechanism is new |
| C2. Evaluation protocol isolating the decision rule (same estimator, calibration and predicates for REM, B1 and REM-noEsc; nested grouped cross-fitting holding out attacker objectives; all fitting in-fold) | §3.11–3.12; `experiments/pilot/` | E0–E6 pilot; exact re-execution | Strong for internal validity of the comparison on recorded data | One benchmark/suite; label rule automatic (no human audit); user_task_15 collision handled post hoc (§4.10) |
| C3. Exploratory evidence on 21 real agents: discrimination on unseen objectives (AUC 0.938), no observed calibration benefit, behavioral evidence not attack-specific, quantified protection–utility trade-off and its dependence on reviewer and costs | Ch. 4 §4.3–4.9; `results/pilot_R2/` | Offline, observe-only, NO-ADAPT replay, ablations, loss grid | Moderate as exploratory evidence; reproduced | Replay assumes no adaptation; costs not approved; no per-backbone conclusion; no live enforcement |
| C4. Closed-loop live-agent harness (B0/B1/REM) with fail-closed runner and analysis code | §3.17; `rem/integration/agentdojo_live.py`; `experiments/live/` | 12 integration tests; scripted ground-truth smoke run (480 episodes, 0 errors) | Strong for harness correctness under scripted agents | **Not executed with an LLM; no live result.** Smoke-run counts are harness checks, not results |
| C5. Record-level systematic review and comparison with closest prior work | Ch. 2; Appendix 2A; Table 4.17 | — | Record-level (metadata/abstract) | No full texts verified; 2 citation conflicts/withdrawn; 21 partial records (REFERENCES_AUDIT.md) |

## 5. Integrity checks performed in this pass

- No experimental result fabricated or altered: numeric preservation check (0 values lost);
  new chart Figure 4.3 reads `results/pilot_R2/e4_e5_enforcement_replay.json` directly
  (`tools/figures_5ch.py`).
- No live result claimed: grep of the five chapters for live outcome numbers finds none; §4.12
  and Table 4.13 state NOT EXECUTED.
- Simulated runs not called live: the scripted smoke run is described as a harness check (§3.17,
  Table 3.26, `experiments/live/LIVE_EXPERIMENT_TEST_REPORT.md`).
- Forbidden reintroductions (`CLAUDE.md`): none found. CUSUM remains observe-only (§4.8);
  attribution remains audit-only; no risk = p × S, no Σ|β|, no ρ, no LLM arbitration, no sequence
  model, no beta/isotonic/temperature calibration adopted.
- Cross-references: three double-renumbered references found and fixed in this pass (see
  THESIS_SOURCE_MAP.md); 0 unresolved after the fix.
- Overclaim removed: "independent re-execution" (6 places: abstract EN/AR, §3.16.2 Table 3.18, §3.16.11.2, §4.2, §4.6) reworded to "re-execution … in a fresh
  environment (by this project, not an external replication)"; no number changed.
- Metadata: supervisor roles follow the student's latest instruction and conflict with earlier
  drafts; flagged (UNRESOLVED_SUPERVISOR_DECISIONS.md, N-1).
