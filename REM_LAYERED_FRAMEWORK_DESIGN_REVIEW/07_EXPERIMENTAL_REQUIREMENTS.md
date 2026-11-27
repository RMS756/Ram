# 07: Experimental requirements

**Existing results versus proposed experiments.**
- **Existing REM results** (reproduced and reconciled) are listed only for reference, in §1.
- **Everything in §2 is a proposed future experiment.** None was run, and no expected numbers are given.

## 1. Existing evidence (unchanged)

| What | Status |
|---|---|
| Replay security, utility and call-level metrics for REM v1.0 on P1, P2, P3 | Existing |
| Protocol-frozen component-level ablations | Existing |
| Exploratory modelled suppression (DiD-2) | Existing |
| Confirmatory v1.1 run | Existing |
| Deployment-simulation parity and latency | Existing |
| Live agents | **None** |
| Adaptive attacks | **None** |
| Human reviewer | **None** |

## 2. Requirements per recommended change

| Change (04 / 05) | Needs an experiment? | What would need to be tested | Metrics | Design notes |
|---|---|---|---|---|
| A1–A7 / D1–D7 (documentation) | **No** | — | — | Text only |
| B1 / I1: canonical identifiers | Yes (offline) | Whether canonicalization changes provenance evidence and outcomes on reformatted and original populations | Attack outcomes; attack-call withholding; benign completion; completion under attack; false-positive blocking; latency | Paired replay against REM v1.0 on P1–P3 and the reformatted population. A changed REM is a new version, requiring supervisor approval |
| B2 / I2: field-level provenance | Yes (offline) | Separation of typed and free-text fields; effect on the user_task_15 collision | As above, plus per-injection-task breakdown | Same harness |
| B3 / N1: model-independent authorization | Yes (offline **and** live) | Authorization correctness on requests written by others (held-out phrasing); tool-call authorization accuracy; robustness across attack objectives | False-negative release; false-positive refusal; ASR; benign and under-attack completion | **A trusted authorization channel must be specified first** [DESIGN BLOCKED]. Earlier exploratory studies show held-out failure modes |
| B4 / N2: reviewer for Escalate | Yes (human study) | Reviewer accuracy on escalated financial calls, including well-formed forged values | Approve/deny accuracy; time; residual ASR | Needs an ethics protocol. Idealized-reviewer replay is only a bound |
| B5 / N3: economic limits | Yes (fixtures) | Split transfers; amount escalation to trusted recipients (not in AgentDojo banking) | Prevented exposure; legitimate payments refused | Limit values [DESIGN BLOCKED] |
| B6 / N5: drift signals | Yes | Only after 06's conditions are met | Component-level ablation; latency; behaviour across backbones | Requires embeddings or extra LLM calls |
| B7 / N6: reachability test | Yes (offline) | Whether each component's verdicts can reach an outcome | Release changes under constant substitution | Methodological |
| Any change claiming robustness | Yes (live, adaptive) | Behaviour of an agent that reacts to refusals; adaptive attacker | Closed-loop ASR and task completion; backbone variation | Backbones, repeats and budget [DESIGN BLOCKED]. Adaptive generation as in AutoDojo or Zhan et al. |

## 3. Rules for any future experiment

1. Freeze the protocol before scoring.
2. Pair arms on identical episodes.
3. Report replay and closed-loop results separately, and never as each other.
4. Report the verdict-to-outcome convention.
5. State each population's data history.
6. Use the existing statistical methods with their verified references (06 §2). Confidence levels and decision rules are researcher decisions.
7. **Do not produce synthetic illustrative numbers.**
