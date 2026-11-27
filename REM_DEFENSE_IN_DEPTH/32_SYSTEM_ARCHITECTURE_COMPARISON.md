# System-by-system technical comparison (18 attributes)

**Notation:**
- **n.d.** = not determined: the abstract or repository is silent and the full text was not read. **n.d. never means "absent".**
- Evidence levels are as in file 30. Progent is the only system read in full (F).
- Greshake et al., AgentDojo and ASB are an attack study and two benchmarks. They are compared in `31_PRIOR_ART_LITERATURE_MATRIX.md`, not here.
- Narisetty et al. is an evaluation of Progent, summarized in the last section.
- REM v1.0 is included for comparison, from its code and this track's experiments.

| Attribute | RTBAS | CaMeL | Progent (v3) | AgentCap | Fides (Costa et al.) | REM v1.0 |
|---|---|---|---|---|---|---|
| 1 Threat model | Prompt injection via tool outputs, causing harmful actions or confidential-data leaks (A) | Injection via untrusted data; user query trusted (R) | User query benign; attacker controls tool observations; cannot change model or system prompt (F §3.2) | Indirect injection converts influence over reasoning into unauthorized effects (A) | Prompt injection; confidentiality and integrity (A) | Indirect injection in tool outputs; user request trusted; REM protected (AS-1, AS-3) |
| 2 Attack assumptions / adaptivity | n.d. | n.d. | Static benchmark attacks plus three adaptive attacks (F App. E) | n.d.; "controlled adversarial scenarios" (A) | n.d. | Recorded attacks; agent not adaptive (NO-ADAPT replay); evasion modeled by feature suppression, one real reformatting evasion |
| 3 Architecture | Tool-based agent with IFC labels, dependency screeners and a confirmation step (A) | Privileged LLM plans from the trusted query; quarantined LLM reads untrusted data; custom interpreter (R) | Policy rules, LLM policy generation and update, SMT check, approver, enforcement at tool call (F) | MCP wrapper, policy engine, capability-token issuer, tool-side validator, trust state (A; trust state S) | Planner with label tracking and hiding primitives (A) | Five layers: Input & Context, Detection, Behavioral Analysis, Decision Engine, Mitigation |
| 4 Trust boundaries | Between tool outputs and actions, by labels (A) | Between trusted query and untrusted data; untrusted data cannot change control flow (R) | Between agent and tools; trusted query vs untrusted observations (F) | Between model and tools: the model selects, AgentCap authorizes (A) | Label-based (A) | Segment-level trust labels; REM between agent and tools |
| 5 Provenance mechanism | Labels on tool outputs; screeners decide which labelled inputs a call depends on (A) | Capabilities attached to values: sources and readers (R) | **None** in the policy language (F, Fig. 2b) | Provenance of **security-sensitive arguments** checked by policy (A); mechanism n.d. | Integrity and confidentiality labels (A) | Least-trusted inheritance on segments; exact-string entity matching (reformatting defeats it) |
| 6 Information-flow control | Yes, adapted IFC (A) | Yes, data and control flow by construction (R) | No (F) | n.d. beyond argument provenance | Yes; dynamic taint tracking with a formal characterization of what it can enforce (A) | No formal IFC; provenance used as evidence (features) |
| 7 Authorization model | Auto-execute if integrity and confidentiality are preserved; otherwise ask the user (A) | Security policies on tool calls over value capabilities (R); authoring n.d. | Allow/forbid rules over arguments; LLM-written, optionally hand-written generic policies; expansion needs approval (F) | Intent declared per request; constraints on trust, prerequisites, mutually exclusive authority; capability tokens (A). **Who declares the intent (model or trusted party): n.d.** | Deterministic policies (A); authoring n.d. | Predicate D1 (prohibited tools); no representation of what the user authorized |
| 8 Detection | No injection detector stated; screeners judge dependency, not injection (A) | None (by design) (R) | None (F) | n.d. ("suspicious requests" update trust: S) | None stated (A) | x~ctx2~ pattern detector (6 patterns); SIG-1 found it is a template fingerprint |
| 9 Behavioral monitoring | n.d. | None stated (R) | None; no history term in the policy language (F) | Per-agent trust score from suspicious requests and execution outcomes (S) | n.d. | History features x~beh1–4~ (x~beh1~ duplicates x~ctx2~) |
| 10 Decision process | Rule over labels and screener output (A) | Deterministic policy check by the interpreter (R) | Deterministic first-match; default block (F, Alg. 2) | Deterministic policy plus trust threshold (A; threshold S) | Deterministic policy (A) | D1/D2 predicates, then ridge LR → Platt → tier → expected-loss verdict |
| 11 Enforcement location | Before tool execution (A) | Interpreter, at tool call (R) | At each tool call (F) | MCP wrapper; tokens validated at the tool boundary (A) | At tool call (A) | Before each tool call (replay harness; gateway simulation) |
| 12 Fail-safe behaviour | User confirmation when safety cannot be established (A) | n.d. (S: policy violation stops the call; user-confirmation details n.d.) | Default block; fallback message lets the agent continue (F) | Revocation or sandboxing on low trust (S) | n.d. | Gateway fails closed; D2 escalates on missing evidence; `DesignNotSpecifiedError` |
| 13 Adaptive-attack evaluation | n.d. | n.d. | Yes (F) | n.d. | n.d. | No (NO-ADAPT) |
| 14 Benchmark coverage | AgentDojo (A) | AgentDojo (R/S) | AgentDojo, ASB, AgentPoison; frameworks (F) | AgentDojo, InjecAgent (A) | AgentDojo (A) | AgentDojo 0.1.35, banking v1 only |
| 15 Financial task coverage | Motivation (A) | Banking suite in tables (S) | Banking pooled with other suites; no banking-only result (F) | n.d.; banking policy analysis (S) | Per-suite appendix (S) | Banking only |
| 16 Security metrics | "Prevents all targeted attacks" (A) | 0 attacks with policies (S) | Attack success 39.9 → 1.0 (F) | Attack success reduced in every setting; 0 with GPT-5.4 (A) | 0 policy-violating injections with checks (S) | Attack success 672 → 11 of 2,979 attacked episodes (replay) |
| 17 Benign utility | "2% loss under attack" (A) | 77% vs 84% (S, v2) | 79.4 → 76.3 without attack (F) | "Preserving all legitimate operations exercised" in controlled scenarios (A) | "Broad range of tasks" (A); per-suite S | Benign tasks completed 175 → 105 of 334 (replay) |
| 18 Stated limitations | n.d. | n.d. | Initial policy may exceed least privilege; attacks within least privilege out of scope (F §9) | n.d. | n.d. | One benchmark; replay; detector gap; over-blocking; no reviewer |

## Narisetty et al. (2026): the adaptive evaluation of an out-of-band defense

- **What was evaluated:** Progent, on AgentDojo, with a self-hosted Qwen2.5-7B agent over three runs (A).
- **Attack:** one hand-crafted black-box adaptive template.
- **Results:** attack success 25.8% without the defense, 4.2% with it, and 2.6% under the adaptive attack (A).
- **Authors' own scope:** they call this "one small-scale data point on a weak model", and say that a white-box attack and extension to CaMeL and others remain open (A).
- **What it does not do (A):** it does not evaluate combinations of controls, or the effect of bypassing one control while another stays in place.
- **Why it matters here:** it is the clearest published warning that out-of-band defenses are validated only on static attacks. REM's replay results carry the same limitation, more strongly, because the REM agent does not adapt at all.
