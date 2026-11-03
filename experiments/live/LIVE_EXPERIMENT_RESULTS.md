# Live Closed-Loop Experiment: Results

## STATUS: NOT EXECUTED. NO LIVE RESULT EXISTS.

No episode with a real language model was run. This file therefore contains **no ASR, utility or adaptation result**.

**Blockers, as recorded on 3 November 2026:**

1. **Credentials.** No LLM API credential is available in the execution environment. The provider endpoint `api.anthropic.com` answered HTTP 401 without a key; `api.openai.com` and the model-weight hosts (Hugging Face, Ollama) were refused by the network policy.
2. **Design decisions.** The design inputs are undecided: backbone, decoding, repeats, fitted-parameter source, authorisation and pre-registration (D-15). `run_live.py` exits with code 2 on the template.

## What was executed instead (not experimental evidence)

| Run | Agent | Purpose | Outcome |
|---|---|---|---|
| `tests/test_live_integration.py` | Scripted reactive test double | Mechanics: interception, semantics, ids, retries and replans, isolation, label isolation, fail-closed runner | 12 / 12 passed (`smoke_output/pytest_live_integration.log`) |
| `experiments/live/smoke_scripted.py injection_task_0` | Scripted "fully compliant" agent that executes the ground-truth calls of the user task, then of the injection task; it never adapts | The harness runs end to end on all 144 attacked pairs and 16 benign tasks with real `important_instructions` injections | 480 episodes (160 per condition: B0, B1, REM step-level without reviewer), **0 errors**. Withheld calls were never executed. Counts are in `smoke_output/smoke_scripted_ground_truth.json` |

The smoke counts (for example, the number of y = 1 proposals withheld) describe a non-adaptive scripted agent on one arbitrarily selected frozen fold (`injection_task_0`; the selection is not a design decision). They **must not** be cited as attack-success, utility or effectiveness results.
