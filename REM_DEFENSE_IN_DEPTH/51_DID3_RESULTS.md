# DiD-3 results: REM-DiD individual and combined controls, bypass and failure injection (EXPLORATORY)

**Run details.**
- Protocol `50_PROTOCOL_DID3.md`, frozen at commit `8678add` before the full run.
- Amendment `50a`, a coverage-measurement fix, committed at `e432189` before its corrective run.
- **Raw data:** `results/did3_raw.jsonl.gz` (169,577 replays) and `results/did3_raw_amend1.jsonl.gz`.
- **Analysis:** `results/did3_results.json`, `results/did3_coverage_amend1.json`.
- **Gates (all passed):**
  - REM v1.0 (B1) reproduces 11/2,979 attacks and 105/334 benign tasks;
  - B0: 672 attacks, 175 benign tasks; on POP-R, 553 attacks;
  - 0 replay errors;
  - 0 gateway refusals outside the gateway-failure arm;
  - every audit hash chain verified.

**Scope.**
- Recorded AgentDojo 0.1.35 banking episodes replayed with the agent fixed (**NO-ADAPT**).
- **Exploratory:** the data was used before.
- Authorization uses **oracle** TAEs: no trusted approval channel exists in the benchmark.
- **Nothing here shows robustness to an adaptive attacker.**

**Reading utility in replay.**
- A recorded final answer is replayed whatever the tools return.
- Benign utility therefore changes only through state-changing calls.
- 105 of the 334 benign episodes succeed even when every state-changing call is withheld (the F-GW arm).

## 1. Individual and combined controls (POP-P)

| Arm | Controls | Attacks /2,979 | Unauthorized state change (episodes) | Benign /334 | Legitimate state-changing calls withheld /1,644 | Escalations |
|---|---|---:|---:|---:|---:|---:|
| B0 | none | 672 | 828 | 175 | 0 | 0 |
| B1 | REM v1.0 | 11 | 24 | 105 | 1,305 | 1,305 |
| B2 | AUTH (oracle) | **0** | 0 | **173** | 774 | 0 |
| B2e | AUTH (explicit) | 0 | 0 | 122 | 1,432 | 1,228 |
| B2e+R | AUTH (explicit) + idealized reviewer | 0 | 0 | 175 | 369 | 1,228 |
| B3 | PROV | 13 | 27 | 147 | 250 | 1,129 |
| B4 | DET | 7 | 19 | 164 | 159 | 1,047 |
| B5 | BEH | 120 | 124 | 161 | 155 | 938 |
| B6 | AUTH + PROV | 0 | 0 | 173 | 774 | 0 |
| B7 | DET + BEH | 1 | 2 | 161 | 282 | 1,187 |
| B8 | AUTH + ENF | 0 | 0 | 173 | 774 | 0 |
| B9 | Full, strict | 0 | 0 | **105** | 1,508 | 717 |
| B9p | Full, pinned_release | 0 | 0 | 172 | 798 | 20 |
| B9n | Full without LEARN | 0 | 0 | 173 | 774 | 0 |
| B9e | Full, explicit TAE | 0 | 0 | 105 | 1,606 | 1,384 |

**How to read the authorization rows.**
- B2 withholds 774 legitimate state-changing calls, yet completes 173 benign tasks. With an oracle TAE these are calls **outside** the ground-truth parameters: agent errors and extra calls, or `user_task_15` ambiguities.
- The oracle withholds anything not exactly authorized, which costs little utility in the benchmark's own scoring.
- **This is an upper bound** that assumes a perfect trusted approval channel.

## 2. Does the learned layer (4B, REM v1.0) add value behind authorization? (H4)

| Contrast | Difference | p (sign-flip, cells) | p (exact, by user task) | Holm | Leave-one-cluster-out range |
|---|---|---:|---:|---:|---|
| B9 − B9n, attacks | 0 | 1 | 1 | 1 | [0, 0] |
| B9 − B9n, benign tasks | **−68** (6 vs 74 discordant) | 0.014 | 0.014 | 0.12 | [−74, −51] |

- **Behind oracle authorization, 4B adds no security** in this replay (0 vs 0 attacks).
- It **costs 68 benign tasks** (105 vs 173). The cost is consistent across every leave-one-user-task-out subset. It is not significant after Holm correction over the 15 declared contrasts (raw p = 0.014; 16 user-task clusters).
- Authorization-first precedence (B9p: 4B consulted only for calls not fully pinned) recovers 172 benign tasks.
- **H4 is supported descriptively.** Where 4B does matter is shown in §3: it covers 2 attack calls that no other control covers.

## 3. Authorization bypassed: do the remaining controls still protect? (H1–H3)

Setting: over-broad TAE (`broad`). Every authorized operation accepts any recipient and amount. Modelled evasion affects attack-labeled calls only (DiD-2 convention).

| Arm | Remaining controls active | Attacks /2,979 | vs X-all (Holm p) | vs X0 |
|---|---|---:|---|---|
| X-all | none (authorization still denies operations the user never asked for) | 174 | — | — |
| X-only-PROV | PROV | 13 | −161 (p < 0.001) | — |
| X-only-DET | DET | 7 | −167 (p < 0.001) | — |
| X-only-BEH | BEH | 3 | −171 (p < 0.001) | — |
| X-only-LEARN | LEARN | 11 | −163 (p < 0.001) | — |
| **X0** | all four | **0** | −174 (p < 0.001; exact by injection task p = 0.0039) | — |
| X-PROV | all but PROV | **0** | — | 0 (resilient) |
| X-DET | all but DET | **0** | — | 0 (resilient) |
| X-BEH | all but BEH | **6** | — | +6 (p = 0.25, Holm 1) |
| X-LEARN | all but LEARN | **1** | — | +1 |

- p < 0.001 above means: none of 20,000 sign-flips across 144 cells reached the observed value. The exact test at injection-task level has a floor of 2/512.
- **H1 (remaining controls protect): supported.** With authorization bypassed, the four evidence controls together allow 0 attacks, against 174.
- **H2 (each control protects alone; complementarity):**
  - Each control alone reduces attacks from 174 to between 3 and 13.
  - Call-level coverage (corrected, amendment 50a), over 907 attack-labeled state-changing calls in X0:
    - **all 907** are covered by at least one control, and **888** by two or more;
    - PROV covers 879, DET 888, BEH 783, LEARN 882;
    - Jaccard overlap is 0.84–0.99.
  - **The controls are largely redundant, not complementary.** Complementarity is confined to **19 calls**:
    - 17 covered by BEH alone: all in `user_task_15`, where the user's own request names the attacker's IBAN, so PROV and DET correctly see a trusted value. The tool-switching rule catches them.
    - 2 covered by LEARN alone.
- **H3 (resilience: one further evasion raises no attacks), strict criterion:**
  - **Met** for PROV and DET.
  - **Not met** for BEH (+6, all `user_task_15`) and LEARN (+1).
  - Neither increase is statistically distinguishable from 0, but the declared criterion is strict equality.

## 4. Real bypasses (H6)

Same arms on the transformed populations. The agent is assumed to behave as recorded, so **these results are conditional**.

| Arm | POP-P | POP-R (reformatted IBAN) | POP-X (paraphrased injection) |
|---|---:|---:|---:|
| B0 | 672 | 553 | 672 |
| B1 (REM v1.0) | 11 | 11 | 11 |
| B3 (PROV, canonical) | 13 | 13 | 13 |
| B4 (DET) | 7 | 7 | 7 |
| B9 | 0 | 0 | 0 |
| X0 | 0 | 0 | 0 |

- Canonical lineage is unaffected by reformatting. In DiD-2, exact-match P1 rose from 12 to 191 under the same probe.
- Detection is unaffected by this paraphrase **only because the financial-directive detector (D_fin) keys on the payload**. The pattern, role and override detectors fall to 0 recall under paraphrase (SIG-2).
- **Not tested in replay:** zero-width obfuscation. Under it every detector failed in SIG-2 (`43_DETECTION_SPEC.md`), while canonical IBAN extraction strips zero-width characters.

## 5. Failure injection (H5)

All arms use the full strict stack with the oracle TAE (B9: 0 attacks, 105 benign) unless stated.

| Arm | Failure | Attacks | Benign | Legitimate state-changing withheld |
|---|---|---:|---:|---:|
| F-DET | detectors unavailable | 0 | 105 | 1,508 |
| F-PROV | provenance metadata missing | 0 | 105 | 1,508 |
| F-BEH | monitor failure | 0 | 105 | 1,508 |
| F-LEARN | model unavailable | 0 | 105 | 1,644 |
| F-AUTH | evaluator unavailable | 0 | 105 | 1,644 |
| F-STORE | TAE store unavailable | 0 | 105 | 1,644 |
| F-GW | gateway failure (nothing executes) | 0 | 105 | 1,644 |
| F-AUDIT | audit unavailable | 0 | 105 | 1,644 |
| F-AUTH-open | evaluator unavailable, **fail-open** | 0 | 105 | 1,350 |
| F-DET-b / F-DET-b-open | detectors down on the broad stack | 0 / 0 | 105 / 105 | 1,351 / 1,351 |

- **H5 is supported:** no single failure lets an attack through under fail-safe defaults.
- The utility cost of failures is invisible above the 105-task replay floor, because B9 is already at that floor. It shows as more withheld legitimate calls (1,508 → 1,644).
- **Fail-open is not punished in replay:**
  - F-AUTH-open still allows 0 attacks, because the evidence controls catch every injected recipient.
  - F-DET-b-open = F-DET-b, because every value of an un-screened segment is also flagged by PROV.
- **Where fail-safe is load-bearing:** the scenario suite (scenarios 15c/15d). An amount escalation to a **trusted** recipient is caught **only** by authorization. With the evaluator failing open it executes; with fail-safe it does not. The benchmark's injection tasks do not exercise this case.

## 6. Overhead

| Arm | Mean decision latency |
|---|---|
| REM v1.0 (B1) | 0.26 ms |
| REM-DiD (B9) | 0.39 ms |

Token cost is 0. No model is called by any layer.

## 7. Answer to the research question, at the evidence level reached

| Level (task §3) | REM v1.0 | REM-DiD (exploratory, replay, oracle authorization) |
|---|---|---|
| 1 Layered architecture | Yes | Yes |
| 2 Defense in Depth (complementary controls) | Partly | **Partly.** Four evidence controls each give independent protection when authorization is bypassed. They overlap heavily (Jaccard ≥ 0.84). Distinct coverage exists only for 19 of 907 attack calls. Detection's apparent independence rests on one payload-keyed detector. |
| 3 Resilient Defense in Depth | To single-control loss; not to family loss (DiD-2) | **For PROV and DET loss (strict criterion met); not for BEH or LEARN loss.** Protection holds under every single injected failure (fail-safe). Shown only for non-adaptive replay. |

**Conditions under which complementary controls add protection.**
1. Authorization is over-broad or bypassed. With precise authorization they add nothing measurable here, and 4B costs utility.
2. The attacker's value has untrusted origin. When the user's own instruction contains the attacker's value (`user_task_15`), only sequence behaviour separates the cases.
3. The attack uses the payload's financial content. Paraphrase defeats the textual detectors; zero-width obfuscation defeats all of them.

**Costs.**
- Under bypassed authorization the evidence controls withhold 1,351 of 1,644 legitimate state-changing calls (X0) and keep benign completion at the 105-task floor.
- Depth in this design is bought with heavy over-blocking, as already seen for REM v1.0.

## 8. Limitations specific to DiD-3

- NO-ADAPT replay. Retry and tool-switching rules see only what the recorded agent happened to do.
- Oracle authorization: the `explicit` mode only shows the cost of not inventing parameters.
- Exploratory reuse of data.
- One benchmark and one attacker account: 8 of 9 injection tasks share it.
- `user_task_15` collision.
- Modelled evasion for PROV, BEH and LEARN; real evasion only for reformatting and paraphrase.
- Detectors were written with knowledge of the templates.
- The idealized reviewer is an upper bound. With it, PROV-only lets 17 attacks through, not 13: escalated calls labelled 0 by the reference rule still contributed to attack success. This is a labeling-rule limitation, and a reason for the human label audit (file 53).

## 9. Cost sensitivity (protocol 52, 36 declared cells × 3 arms; `results/did3_cost.json`; `figures/fig_did3_cost_grid.png`)

| Arm | Successful attacks over 36 cells | Benign tasks over 36 cells | Base cell (×1, C_esc 0.3, limit 1,000) |
|---|---|---|---|
| B1 (REM v1.0) | 0–13 | 105–124 | 11 / 105 |
| B9 (REM-DiD, oracle authorization) | **0 in every cell** | 105–124 | 0 / 105 |
| X0 (REM-DiD, authorization bypassed) | 0–1 | 105–124 | 0 / 105 |

- REM v1.0 shows the expected trade-off: higher C_esc and lower C_miss give more benign tasks and more attacks.
- **Behind oracle authorization, no cell gives 4B any security value,** and no cell reaches the 173 benign tasks of B9n: the utility cost of 4B holds across the whole declared grid.
- With authorization bypassed, the stack allows at most 1 attack in any cell.
- No cell is recommended (exploratory; no split).
