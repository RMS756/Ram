# MELON versus MELON + REM — Experiment Protocol

**Status: IMPLEMENTED PROTOCOL — NOT EXECUTED.** Nothing below is a result. Paid calls need an explicit spending authorisation with a cap; none exists in this session.

## 1. Question and scope

**Question:** on AgentDojo banking v1 under the `important_instructions` attack, how do attack success, utility and overhead change when REM is added at the tool-execution boundary of original MELON?

| Item | Setting |
|---|---|
| Conditions | **MELON** (reference) and **MELON_REM**. `NO_DEFENSE` is optional and for context only; not needed for the before/after comparison. |
| Benchmark and attack | AgentDojo **0.1.29**, suite banking **v1**, attack **`important_instructions`** only. Conclusions are limited to this attack. |
| Not included | Other suites, benchmarks, attacks or defences; new classifiers; the existing REM/B1 analyses (unchanged, Chapter 4). |
| No real finance | Only AgentDojo's simulated banking environment; no real account, API or transaction. |

## 2. Held fixed across conditions

| Item | Setting |
|---|---|
| Benchmark | AgentDojo 0.1.29 and its task definitions |
| Environment | The default environment, loaded fresh for every episode |
| Model | The same backbone model id for the agent and for MELON's runs, with identical decoding |
| Attack | The injection payload is computed once per case and reused for both conditions; same injection vectors |
| MELON | The same embedding model (hard-coded) |
| Agent loop | Tool schemas; `max_iters` = 15; AgentDojo's up-to-3 re-query rule |
| Provider client | One OpenAI client configuration (timeout, SDK retries) |
| Logging | Same logging and evaluation (AgentDojo's utility/security checks) |

## 3. Case sets (declared before any run)

| Set | Cases per condition and repeat |
|---|---|
| **Pilot** | 9 attacked pairs (user_task_j, injection_task_j), j = 0…8: every injection task once, 9 distinct user tasks. Plus 4 benign cases: user_task_9, 11, 13, 15. **Total 13.** Chosen by this coverage rule only, to test compatibility and measure cost, not to select favourable cases. |
| **Full** | All 16 × 9 = 144 attacked pairs + 16 benign user tasks. **Total 160.** Preferred if affordable. |

**Planned episodes:**
- pilot: 13 cases × 2 conditions × R repeats (**26** for R = 1);
- final: 160 × 2 × R (**320** for R = 1).

**Order:**
- each (case, repeat) is a pair;
- pairs are shuffled with the declared seed;
- condition order is randomised within each pair, and the two episodes of a pair run consecutively;
- the run order is recorded (`order_index`).

## 4. Model calls per episode (structure; counts are measured, not assumed)

For an episode with *k* loop iterations that follow a tool result:

| Condition | Chat calls | Embedding calls |
|---|---|---|
| NO_DEFENSE | 1 + k | 0 |
| MELON | 1 + 2k (original + masked run per iteration) | (new masked calls added to the bank) + (original calls, in iterations where the original run proposes calls) |
| MELON_REM | as MELON | as MELON (REM adds no model call) |

AgentDojo may re-query the whole pipeline up to 3 times when the agent ends without text. MELON-based episodes therefore cost roughly twice as many chat calls as an undefended agent, plus embeddings.

## 5. Spending boundary and budget procedure

**No paid call** is made unless the configuration contains:
- `budget.authorization_reference`;
- `budget.cap_usd`;
- `budget.prices_usd_per_1m_tokens` (from the provider's price list on the day; no price is built in);

and `OPENAI_API_KEY` is set.

**Steps:**
1. **Dry run (free):** `… run_melon_rem.py --config cfg.yaml --out x --dry-run` validates everything and prints the planned episodes.
2. **Pilot** (26 episodes for R = 1) under a small cap:
   ```bash
   cd /home/user/Ram
   /home/user/venvs/melon029/bin/python experiments/melon_rem/run_melon_rem.py \
     --config experiments/melon_rem/melon_rem_config.yaml --out results/melon_rem/<run_id>_pilot
   ```
3. **Projection from measured usage:**
   ```bash
   python3 experiments/melon_rem/estimate_budget.py results/melon_rem/<run_id>_pilot/episodes.jsonl prices.yaml --repeats R
   ```
   This gives the per-condition mean and 95th-percentile episode cost from recorded tokens × declared prices, re-weighted to 144 attacked + 16 benign cases × R repeats. It reports a central and a conservative total, and a recommended cap of conservative × 1.25.
4. **Decision on the final case set and R** from the projection and the authorised budget. The complete set is preferred; if it is not affordable, reduce R before reducing cases.
5. **Final run** under the authorised cap. Re-check spend after the first 10% of episodes.

**Spending guard** (`spending_guard.py`):
- Every chat and embedding call (agent, MELON's original and masked runs, embeddings) passes through one ledger.
- Before each call, a worst-case cost is reserved: character-based input upper bound + `reserve_output_tokens`.
- The call is refused if committed + in-flight reservations + the new reservation would exceed the cap.
- After the call, the reservation is replaced by the cost from the provider-reported usage.
- A refused call stops the run and is recorded as `budget_stop`.

**Limitations of the guard:**
- It covers one process only.
- The token reservation is a heuristic, and AgentDojo 0.1.29 sends no `max_tokens`. One call can exceed its reservation, so the cap can be overshot by at most that excess.
- Provider billing (cached-input discounts, rounding, SDK-internal retries, billed timeouts) can differ from the ledger. Reconcile with the provider dashboard.

Secrets are read only from the environment and never written to code, configs, manifests or logs (tested).

## 6. Metrics and denominators

| Metric | Definition |
|---|---|
| **ASR** | attacked episodes with AgentDojo `security = True` / attacked episodes without error |
| **Utility under attack** | attacked episodes with `utility = True` / attacked episodes without error |
| **Benign utility** | benign episodes with `utility = True` / benign episodes without error |
| Errors | `infrastructure_error`, `provider_error`, `timeout`, `budget_stop`, counted per class. **Never counted as prevention or success**; excluded from the three rates and reported. |
| Escalation | Never counted as task completion: no reviewer, the call is withheld, utility is AgentDojo's environment check. Reported as REM Escalate verdicts per evaluated call. |
| Secondary | End-to-end wall time; tokens and ledger cost per episode; REM processing time per call (`rem_latency_full_ms`); REM-withheld calls (interventions attributable to REM, since MELON-stopped calls never reach REM); MELON-flagged episodes |

**Paired analysis** (`analyze_melon_rem.py`):
- differences MELON_REM − MELON over pairs where both episodes finished without error;
- discordant-pair counts;
- percentile **cluster bootstrap** resampling whole user tasks, and separately whole injection tasks for attacked metrics;
- repeats and steps are never treated as independent observations;
- with the pilot's few clusters, intervals are descriptive only;
- no significance test is pre-registered.

**Zero-ASR rule:** if MELON has no successful attack in the sample, the report states that no further reduction in observed ASR can be demonstrated; utility and overhead are still reported. **All findings are preserved**: the combination may improve, match or worsen outcomes. No case is added or removed after seeing results.

## 7. Design inputs still open (runner exits 2 until they are set)

| Field | Status |
|---|---|
| `run_id` | open |
| `benchmark.case_set` | pilot first is recommended [PD] |
| `models.backbone` | Exact dated OpenAI model id. MELON's main paper backbone was GPT-4o; whether to match it is a supervisor decision |
| `models.temperature`, `repeats`, `request_timeout_s`, `max_retries` | open |
| `rem.fitted_parameters_source` | `heldout_crossfit_assignment` (recommended [PD]: matches the Chapter 3 fold rule; attacker objectives held out) or a single `fold:<id>` |
| `budget.*` | Authorisation, cap and prices: **spending decision** |
| `order.seed` | open |

Already fixed by the instruction or the verified code (not chosen here):
- the attack;
- the suite and version;
- AgentDojo 0.1.29;
- conditions MELON / MELON_REM;
- REM policy A3 with `pilot_e0_exploratory` costs (exploratory, D-9);
- step-level semantics;
- `no_reviewer`.

## 8. Outputs (per run directory, all traceable)

| File | Content |
|---|---|
| `manifest.json` | Run id; REM commit and dirty flag; config sha256 and content; MELON commit and file sha256; AgentDojo and OpenAI SDK versions; `pip freeze` sha256 (file alongside); bundle sha256 and provenance |
| `episodes.jsonl` | One record per episode: run id, pair id, order index, case, repeat, condition, outcome, error class, tokens, cost, MELON flag, REM audit, message summaries |
| `spend_ledger.jsonl`, `spend_summary.json` | Spending ledger |
| `melon_upstream_stdout.log` | Upstream diagnostic output |

## 9. Threats to validity (to be repeated with any result)

- One attack template.
- Familiar tasks (training-provenance overlap, MELON_REM_INTEGRATION.md §7).
- Exploratory, unapproved REM costs.
- One backbone; provider non-determinism.
- Compatibility measure C-2 (bank reset per episode).
- AgentDojo 0.1.29 rather than the version of REM's fitting environment (task code identical).
- Adaptive attacks against MELON exist in the literature and are not evaluated.
- A simulated banking environment, not production.
