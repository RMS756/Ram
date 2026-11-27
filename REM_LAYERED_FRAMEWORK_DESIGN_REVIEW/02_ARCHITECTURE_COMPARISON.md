# 02: Architecture comparison

**Rule.**
- A mechanism is described only as far as its source was read (levels F, R, C, O, S; `09`).
- "n.d." means not determined at that level. **It does not mean absent.**
- For REM, every statement refers to REM v1.0 as implemented (`rem/`) and evaluated (`REM_FINAL_SCIENTIFIC_RECONCILIATION_2026_11_28/`).
- **Status codes:**
  - I = implemented;
  - E = experimentally evaluated;
  - P = proposed only.

## 1. Framework by framework

### 1.1 REM v1.0 (baseline; code-level)

| Aspect | What it does | Status |
|---|---|---|
| Objective | Withhold attack-induced financial tool calls of an opaque banking agent before execution | I, E (replay) |
| Threat model | Indirect injection through tool outputs; single agent; non-adaptive attacker in the primary evaluation | — |
| Trust boundary | Three labels, trusted (system) > semi-trusted (user) > untrusted (tool output); least-trusted inheritance; no promotion (`rem/algorithms/context/provenance.py`) | I |
| Input inspection | Hygiene removes invisible and format characters from untrusted text | I; **not exercised** by the recorded data |
| Provenance | `x_act1`: a key argument occurs in untrusted text and not in trusted text (exact string after normalization). `x_act2`: recipient not in the user objective. `x_act3`: sensitive egress | I, E |
| Injection detection | `x_ctx2`: instruction-pattern indicator (template-matched). The classifier `x_ctx1` is not implemented | I, E (no measurable effect) |
| Behavioural monitoring | `x_beh1`–`x_beh4`: post-observation shift, repeated calls, privilege escalation, transition deviation from a benign reference | I, E |
| Tool / argument authorization | **None** in v1.0. No representation of what the user authorized beyond `x_act2` | — |
| Decision | Ridge LR → Platt calibration on the logit → consequence tier → predicates D1 / D2 → minimum expected loss over four verdicts | I, E |
| Enforcement | Step-level withhold or release, in the replay harness and in an HTTP **gateway** at the tool boundary (`rem/deployment/gateway.py`). Any evaluation exception withholds the call (**fail-closed**) | I. E in replay and in a deployment simulation with exact parity on 3,334 recorded episodes (`results/deployment_sim/2026-11-05_full/RESULTS.md`). **No live agent** |
| Output inspection | None | — |
| Human escalation | Escalate verdict exists. **No reviewer**, so it withholds. An "idealized reviewer" exists only as a replay counterfactual | I (semantics); not E as designed |
| Audit | Per-call audit record with verdict source, probability and linear attribution (audit only) | I, E |
| Evaluation | AgentDojo banking; NO-ADAPT replay; three populations; protocol-frozen ablations; one confirmatory run | E |
| Ablation | Enforcement and the learned pathway are necessary. Action evidence is measurable on P3 at call level. Behavioural evidence matters under modelled suppression. Detection and predicates show no measured effect | E |
| Limits | No live or adaptive evaluation; one benchmark; no authorization; Escalate untested as designed | — |

### 1.2 Agent-focused frameworks

**NEXUS** (C, O, S; repository read earlier)

| Aspect | Description |
|---|---|
| Objective and target | Runtime safety of tool-using agents. It monitors a structured plan representation **before tool execution** |
| Layers | Three logically independent signals under one intervention policy Π: nine deterministic rules (S); argument-level inspection; a Platt-calibrated logistic-regression risk score |
| Decision | Π chooses allow / block / request confirmation / request revision. The thesis, from the repository, records a rule-first cascade with loss-based thresholds |
| Human escalation | "Request confirmation" is an intervention |
| Evaluation | 128-instance synthetic benchmark; R-Judge; AgentHarm; an IPI set (0% ASR at 99% control allow); NEXUS-Stress. Reported against rule-only. Latency under 1 ms |
| Not determined | Provenance of argument values; trust boundaries; audit; failure handling; AgentDojo use |

**Progent** (F, R)

| Aspect | Description |
|---|---|
| Objective and target | Least privilege for tool calls |
| Mechanism | Symbolic policies over tool names and argument values, checked deterministically (JSON-schema validation) for every call. Policies are manual or LLM-generated, and LLM-updated with an SMT check: expansions need approval, narrowings apply automatically. A tool without a rule is blocked; a refusal returns an error to the agent |
| Evaluation | AgentDojo, ASB; adaptive attacks; ablations of the approver |
| Limits | Policy generation by an LLM is a trust point. The published manual banking policy is an allow-list of benchmark IBANs that excludes the attacker's (`REM_COMPARATIVE_EVALUATION_PHASE/02` §2) |

**Agent-Sentry** (O, S)

| Aspect | Description |
|---|---|
| Layers | (1) A structural classifier, learned from benign executions, over action sequences and the provenance of function arguments. (2) A deterministic allow-list of (tool, argument, value) seen in benign runs, accepted only from trusted sources. (3) An LLM judge for residual ambiguous cases |
| Evaluation | AgentDojo, AgentDyn. Figures differ across versions |
| Not determined | Per-layer ablation; failure handling |

**MELON** (O, R)

| Aspect | Description |
|---|---|
| Mechanism (code level) | After each tool turn:<br>- makes the agent's next LLM call;<br>- makes a second, masked call with a task-neutral prompt and all tool outputs packed into one file;<br>- embeds both runs' tool calls with an external embedding model;<br>- flags an attack if any original call is highly similar to a masked-run call (threshold hard-coded in the code) |
| On detection | Stops the episode and redacts the last tool output |
| Requirements | Extra LLM calls and an embedding API per step |
| Evaluation | AgentDojo |
| Limits (code) | Runs unmodified only on AgentDojo ≤ 0.1.29; hard-coded embedding model and key placeholder; per-process state leak without isolation (`REM_MELON_COMPARISON_2026_11_19/02`) |

**CaMeL** (R, S)

| Aspect | Description |
|---|---|
| Mechanism | A privileged LLM writes a program from the trusted query. A quarantined LLM parses untrusted data. An interpreter propagates capabilities (sources, readers) and checks a per-tool policy before each state-changing call |
| Banking policy | In code: the recipient must come from the user; other fields need readers |
| Fit with REM | Requires replacing the agent's control flow |

**AgentDojo** (O, L)
- An executable benchmark: user tasks, injection tasks, tools, state-based utility and security checks.
- It ships four defenses.
- It is static; adaptive attacks are possible but not default.

### 1.3 Layered LLM and RAG frameworks

**Intelligent Multilayer DiD** (C, O; full text not read)

| Aspect | Description |
|---|---|
| Objective and target | Local LLMs in air-gapped networks, against direct injection, RAG-based indirect injection and reasoning-mediated multi-turn bypass |
| Layers | Five, grounded in MITRE ATLAS. Only L4 (inference) is characterized in the abstract: it computes a "semantic drift score" from Sentence-BERT embeddings, comparing the policy-approved initial intent with an ordered trajectory of observed events (retrieval queries, tool calls, action arguments, summaries, outputs) |
| The authors' own framing | The score is "neither a new embedding algorithm nor standalone evidence of malicious intent" |
| Evaluation | 1,600 public benchmark instances; precision, recall, F1, false-positive rate, balanced accuracy; comparison with Prompt Guard, Llama Guard, NeMo Guardrails |
| Observability study | Recall falls as intermediate events are removed |
| Not determined | Layers L1–L3 and L5; enforcement on tool calls; financial tasks; adaptive attacks |

**PromptGuard** (C, O, S)

| Aspect | Description |
|---|---|
| Layers | Four: (1) input gatekeeping (regex and a small BERT-type classifier) detects injection intent; (2) structured prompt formatting enforces structural integrity; (3) semantic output validation with a critic; (4) adaptive response refinement of user-facing output |
| Evaluation | PromptBench, InjectBench, TruthfulQA; reported up to 67% reduction in injection success, detection F1 0.91, latency increase below 8% |
| Not present | Tools and actions |

**Layered RAG chatbot framework** (O, arXiv version)

| Aspect | Description |
|---|---|
| Layers | Three:<br>(1) input screening by a rule library and a fine-tuned semantic anomaly classifier;<br>(2) **a provenance-based instruction hierarchy during context assembly**, so retrieved content cannot override operator policy;<br>(3) an output audit by a policy rule engine and a semantic drift detector |
| Continuous loop | Logs support retraining |
| Evaluation | 5,080 samples, three models; ASR, false-positive rate, latency |
| Ablation | The authors report complementary layers |

**CASCADE** (through its audit only, O)

| Aspect | Description |
|---|---|
| Layers | Local rules → embedding similarity → optional local LLM review; verdicts allow / review / block |
| Audit findings | The binary convention for "review" changes the false-positive rate from 11.70% to 1.51%; review refers 68.5% of traffic to a human; corpus wrappers determine the label; the published description does not identify what ran; the LLM review changes no binary outcome |

**Spotlight-Guard** (O)

| Aspect | Description |
|---|---|
| Layers | Three: spotlighting input isolation; LLM detection-and-quarantine; HMAC-based instruction integrity |
| Evaluation | 250 adversarial + 250 benign cases per configuration on 7B local models; ASR, benign success, detection metrics with bootstrap CIs; **component ablation**; an adaptive attack |

### 1.4 Financial

**AIS** (C, O, S)

| Aspect | Description |
|---|---|
| Objective | Separate probabilistic inference from execution authority in agentic finance |
| Mechanism | A typed financial action intent is validated by a deterministic control plane against agent identity, owner, mandate lineage, policy, state, approvals and exact economic terms. It then receives single-use authority. An EVM verifier accepts only tokens bound to permitted intent fields. Replayable assurance follows |
| Evaluation (S) | Token replays and recipient / rail substitutions rejected; model-in-the-loop tests blocked legitimate requests |
| Limit (S) | Reservation and consumption tracking not integrated into the EVM gate |

## 2. Cross-framework comparison

**Cell values:** Y = present at the level read; P = partial; — = not present at the level read; n.d. = not determined.

| Function | REM v1.0 | NEXUS | Progent | Agent-Sentry | MELON | CaMeL | Multilayer DiD | PromptGuard | RAG layered | CASCADE | Spotlight-Guard | AIS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Protects tool calls of an agent | Y | Y | Y | Y | Y | Y | P (observes tool events) | — | — | Y (MCP) | P | Y (financial authority) |
| Explicit trust boundary / provenance | Y (3 labels; argument occurrence) | n.d. | — | Y | — | Y (capabilities) | P (approved intent vs events) | n.d. | Y (instruction hierarchy) | n.d. | Y (spotlighting, HMAC) | P |
| Injection content detection | P (one indicator) | P (argument inspection) | — | P (judge) | Y (behavioural) | — | Y | Y | Y | Y | Y | — |
| Behavioural / sequence monitoring | Y (4 features) | n.d. | — | Y (learned) | Y (counterfactual) | Y (plan fixed) | Y (drift over trajectory) | — | P (drift on output) | — | — | — |
| Argument-level authorization independent of the model | **—** | Y (rules) | Y | Y (allow-list) | — | Y | n.d. | — | — | P (rules) | — | **Y** |
| Graded decision with escalation | Y (4 verdicts; no reviewer) | Y (4 interventions) | P (approval for expansions) | Y (judge) | — | — | n.d. | P (refinement) | — | Y (review) | P (quarantine) | P (approvals) |
| Enforcement before execution | Y (replay; gateway simulated) | Y | Y | Y | Y | Y | n.d. | — | — | Y | P | Y |
| Output inspection | — | — | — | — | — | Y (readers) | n.d. | Y | Y | Y (output guard) | — | — |
| Audit / replay record | Y | n.d. | n.d. | n.d. | — (code: none) | n.d. | n.d. | n.d. | Y (log loop) | Y (records) | n.d. | Y |
| Fail-closed stated | Y (gateway) | n.d. | Y (no rule → block) | n.d. | n.d. | Y | n.d. | n.d. | n.d. | n.d. | n.d. | Y |
| Benign utility measured | Y | Y | Y | Y | Y | Y | Y (false-positive rate) | P | Y (FPR) | Y (FPR, audited) | Y | P |
| Adaptive attacks | — (none run) | n.d. | Y | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | Y | n.d. |
| Per-layer ablation | Y (component-level) | Y (vs rule-only) | Y | n.d. | Y | P | Y (observability) | n.d. | Y | Y (by the audit) | Y | Y |
| Security independent of the LLM's reasoning | Y (no LLM) | Y | P (LLM writes policy) | P (LLM judge) | — (uses LLM) | P (P-LLM plans) | P (embeddings) | P (critic) | P (classifier) | P (LLM review) | P (LLM detector) | Y |

**What the comparison shows.**

1. **REM's distinctive gap.** It is the only agent-boundary system here with **no model-independent argument authorization**. Its protection comes from a learned risk decision over provenance and behaviour.
2. **What REM already has.** Explicit trust labels, a fail-closed external enforcement point and an audit record already exist in REM. They are under-documented as such, not missing.
3. **Different targets.** The LLM- and RAG-oriented frameworks (PromptGuard, the RAG framework, the Multilayer DiD framework) protect text generation. Their output layers have no counterpart in an action-boundary defense.
