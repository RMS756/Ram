# 4. Implementation, dependencies, commands and tests

**Status:** isolated, exploratory code. Nothing under `rem/` or `configs/` was edited.

## 4.1 Modules (`experiments/improve_study/`)

| File | Content | Executed? |
|---|---|---|
| `intent.py` | Request compiler (A): operation categories requested, prohibited or absent; conditions; account identifiers with role (target, historical, mentioned); amounts as exact decimals with role and ambiguity flag; amount modes (derived, history, delegated); named sources; SHA-256 digests of quoted credential values (raw value not kept); read-only and open-delegation flags. Input: the request text only | yes |
| `permission.py` | Typed matcher (B): `evaluate` returns *supported*, *denied* or *unknown* with component statuses; `Ledger` of structured bank records; `offline_permission` (recorded episodes) and `RuntimePermission` (guard path); five indicators for the learned arms (`q_sup`, `q_den`, `q_op`, `q_rec`, `q_amt`) | yes |
| `improve.py` | Arms, fitting of feature set F2 by the unchanged REM procedure, replay of all arms; decision variant C (two verdicts from the existing expected-loss rule) | yes |
| `progent_manual.py` | Comparator PG: Progent's published manual banking policy, read as data from the pinned upstream file | yes (this project's decision function; upstream code not executed) |
| `verifier.py` | Selective verifier (D): gate on permission status *unknown*; answer admissible only with verbatim request spans, never for a call whose operation is not requested or whose recipient or credential is unsupported; fail closed without a client; credentials redacted in the prompt; prompt version and hash | **interface and tests only; no model call** |
| `report.py`, `tables.py`, `failures.py`, `manifest.py` | Metrics and paired intervals; generated tables; failure analysis; split manifest and hashes | yes |

## 4.2 Environment

| Item | Version |
|---|---|
| Python | 3.11.17 |
| AgentDojo | 0.1.35 (banking suite v1); recordings from runs commit `089ed468…` |
| NumPy | 2.4.6 |
| PyYAML | 6.0.1 |
| pytest | 9.2.0 |
| Progent upstream | `sunblaze-ucb/progent` at `9befb41cbf992b49dbf035cbd3d53eb953d3b351`; `agentdojo/src/agentdojo/default_suites/v1/banking/task_suite.py` sha256 `43da7d02…fac0b6f`; `secagent/tool.py` sha256 `4e2a0a60…373635` |
| Hardware | one container, four worker processes, CPU only |
| Random seeds | bootstrap seed 20261027 (2,000 resamples); `PYTHONHASHSEED=0`; fitting is deterministic |

Model calls, tokens and cost: **zero** for every arm that was run.

## 4.3 Commands

```bash
export PYTHONHASHSEED=0
export PILOT_RESULTS_DIR=<pilot state>  AUTHZ_STATE=<state of the earlier study>  IMPROVE_STATE=<new state directory>
export PROGENT_UPSTREAM=<clone of github.com/sunblaze-ucb/progent>      # read with `git show`; never imported

python3 experiments/improve_study/manifest.py                 # split manifest and dataset hashes
python3 experiments/improve_study/improve.py evidence fit replay   # 152 fitting cells; 161,506 replays (about 6 minutes)
python3 experiments/improve_study/report.py                   # results/improvement_results.json
python3 experiments/improve_study/tables.py                   # results/tables.md
python3 experiments/improve_study/failures.py                 # results/failure_analysis.json
python3 -m pytest tests/test_improve_study.py -o addopts=""   # 35 tests
```

Dry-run commands for the arms that need a model (nothing is called): see `protocol/PROSPECTIVE_PROTOCOL.md`.

## 4.4 Tests

`tests/test_improve_study.py`, 35 tests, all passing. Full suite on 13 November 2026: **278 passed, 1 skipped, 1 expected failure**.

| Group | What is checked |
|---|---|
| Normalization | Identifier canonical form ignores spacing and hyphens only (one changed character does not match); amounts are exact decimals; `1,250` and `1.250` are left ambiguous |
| Compiler | Requested, prohibited and absent operations; target against historical identifiers; credential kept only as a digest (the raw value does not occur in the representation); immutability |
| Matching | Recipient or amount substitution is a hard denial; an untrusted file cannot grant an operation or a recipient; free-text fields and incoming senders of bank records establish nothing; scoped delegation supplies a profile value but never a credential; unverifiable amounts only below the declared limit; each ablation switch changes its own component |
| **Label isolation** | (i) static check that `intent.py`, `permission.py` and `verifier.py` contain no reference to task identifiers, labels, outcomes or injection content; (ii) an episode object whose every attribute except the request and the messages raises on access is processed without error; (iii) two episodes differing only in identifiers, labels and outcomes receive identical evidence; (iv) the compiler's only parameter is the request text |
| Verifier | Gate depends on permission status and not on a probability; fail closed without a client; an answer without verbatim request spans is rejected; a denied call is never sent; credentials are redacted from the prompt |
| Progent comparator | Policy read from the pinned commit and file hashes; decisions for allowed and disallowed recipients, omitted optional recipient, missing policy entry; a changed upstream file is rejected |
| Stored results | Frozen paths reproduce the earlier counts; no replay errors; rule arms are identical under both splits |

## 4.5 Leakage controls

- The defense interface receives the request, the tool call and the tool outputs. Reference solutions, attacker references, hidden labels, task identifiers and outcomes are not parameters of any function in the three defense modules (tests above).
- The learned arms are fitted inside each fitting portion by the unchanged procedure; no threshold, cost or rule was selected on an evaluation portion. The permission indicators are deterministic functions of the request and the history, so they carry no fitted quantity across splits.
- **Not controlled:** the parser was written by an author who knows all 16 requests and all 9 attacker objectives. This is a design-level exposure that splits cannot remove; it is why every result is called development evidence and why the prospective protocol requires request variants written by someone else.

## 4.6 Budget and configuration report for the arms that were not run

| Arm | Needs | Available | Blocker |
|---|---|---|---|
| MELON; MELON followed by G1 | agent model, embedding model, AgentDojo 0.1.29 | code integrated and tested with scripted agents (earlier work); pinned upstream `4d3cc9c` | no model credential; no spending authorization; embedding host not reachable |
| Task Shield | agent model; official code | no official repository was verified in this session | same; and the code would have to run unmodified |
| Progent with generated or updated policies | policy model (`SECAGENT_POLICY_MODEL`) | official code at HEAD `b02783b` | same |
| CaMeL | agent model; its interpreter | repository at `f083b6b` | same |
| Selective verifier (D) | one model call per call of *unknown* status | interface, gate and tests | same |
| Closed-loop runs of any arm | agent model | closed-loop executor from the earlier work | same |

Volume that a verifier run would have on the recorded data, counted from the stored audits of G1: 56 calls of unknown status among 178 legitimate state-changing calls of the benign primary episodes, and 290 of unknown status among the attack-labelled calls of the probe population. No price is assumed and no cost is computed here; the existing estimator (`experiments/melon_rem/estimate_budget.py`) takes measured token counts and prices as inputs once a model and a cap are approved.
