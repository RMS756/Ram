# Progent: full-text reading note and paper-to-code differences

**Document read.** *Progent: Securing AI Agents with Privilege Control*. Tianneng Shi, Jingxuan He, Zhun Wang, Hongwei Li, Linyu Wu, Wenbo Guo, Dawn Song (UC Berkeley; UC Santa Barbara; National University of Singapore). arXiv:2504.11703**v3** [cs.CR], dated 14 May 2026. 17 pages. Uploaded file sha256 `cd38f8f70cd172572b01d9d15a9c4fd87751692e155f0e1d9c003b4903520e62`. All 17 pages were read, including Appendices A to G.

**Publication status.** Every page of the uploaded version is headed "Preprint". Appendix B mentions "the ethics guidelines on the conference website" (p. 14) without naming a venue. **No peer-reviewed venue is stated in the document, and none is asserted here.** It is cited as an arXiv preprint, version 3.

**Kinds of evidence in this note.** [P] = stated in the paper, with page. [C] = read in the official repository `github.com/sunblaze-ucb/progent` (code inspection; the code was not executed). [R] = reproduced by execution in this project. [X] = proposed or not done.

---

## 1. Policy representation and enforcement

- **Where it acts.** At the tool-call level, between the agent and its tools, with no change to the agent's internals [P, p. 2, Section 2.2 p. 3, Section 7 p. 7].
- **Language** [P, Figure 2, p. 5; Section 4.1]. A policy is a list of rules. A rule is `E t when {e_i}, fallback f`: an effect `E` (allow or forbid), a tool `t`, a conjunction of conditions over the tool's arguments, and a fallback. Conditions are boolean expressions over the arguments: literals, array access, array length, and/or/not, the comparisons `<`, `<=`, `==`, membership `in`, and regular-expression `match`. **Conditions range over the arguments of the current call only; the language has no term for the history of executed calls** [P, Figure 2b].
- **Fallbacks** [P, p. 5]. Terminate execution; ask the user; or return a message. The paper's default is the third: the agent receives "The tool call is not allowed due to {reason}. Please try other tools or arguments and continue to finish the user task: {o0}." and continues.
- **Enforcement** [P, Algorithm 2, p. 6; Section 4.2]. For a call to tool `t`: take the rules for `t`, put forbid rules before allow rules, apply the first rule whose conditions hold; if none applies the call is blocked by default. The decision is deterministic.
- **Implementation** [P, Section 7, p. 7]. Policies are JSON Schema; enforcement uses the `jsonschema` library; the comparison of two policies uses the Z3 solver. A sample policy is in Appendix C, Figure 9 (p. 14).
- **Generic policies** [P, Section 7 pp. 7-8; Algorithm 4, p. 8]. Hand-written, fixed for the whole execution, evaluated before the task-specific policy; several stakeholders' policies are layered by priority.

## 2. Policy generation, updates and the approver

- **Initial policy** [P, Section 5, p. 7; prompt in Figure 15, p. 16]. A language model writes it from the list of tools and the user's query only, which the threat model treats as trusted.
- **Update** [P, Section 5, p. 7; Algorithm 3, p. 6; prompts in Figures 16 and 17]. Two sub-steps. First, a model decides whether an update is needed from the tools, the query and the current call, **without the tool's result**. If so, a model proposes a new policy from the tools, the query, the call, its result and the current policy.
- **Narrowing or expansion** [P, Section 4.3, p. 6, Equations 1 to 4]. With `A(P)` the set of calls a policy allows (Eq. 1), the new policy is a narrowing if `A(P') ⊆ A(P)` and an expansion otherwise. The check is reduced per tool to an implication between two formulas over the arguments (Eq. 4) and decided by the SMT solver.
- **What happens next** [P, Algorithm 3 lines 7-9; Section 7 "Approver Module", p. 8]. A narrowing is applied automatically. An expansion needs approval. The approver is configurable: approve all, deny all, per-tool rules, or human review.
- **Default in the experiments** [P, Section 8.1, p. 8; Section 8.2, p. 9]. gpt-4o is both the agent and the policy model, and the approver **always accepts expansions** ("Auto-Approve"), which the authors call the worst case.
- **Share of expansions** [P, p. 4 and p. 10]. On AgentDojo, 6% of updates were expansions.

## 3. The formal guarantee and its scope

- **Statement** [P, Section 6, p. 7, Equations 5 and 6]. Every automatically applied update satisfies `A(P') ⊆ A(P)`, so between approved expansions the allowed set only shrinks. The authors call this *monotonic confinement*: "the agent's action space cannot increase without explicit approval".
- **What it is a statement about.** The set of calls allowed by the *current policy*. It says nothing about whether the initial policy, written by a language model, matches what the user meant; the paper says so itself: with incorrect approvals or ambiguous initial tasks "Progent may permit policies that exceed minimal privilege" [P, Section 9, p. 11].
- **Under the default configuration** the approver accepts every expansion [P, p. 8], so in the reported main results the guarantee constrains nothing beyond what the policy model proposes. It has force under Auto-Deny and Manual Approval.
- **Out of scope by the authors' own statement** [P, Section 3.2 p. 5; Section 9 pp. 11-12]: attacks that stay within least privilege (for example preference manipulation), attacks on text outputs that trigger no dangerous call, and multimodal agents.
- **Threat model** [P, Section 3.2, pp. 4-5]. The user's query is benign; the attacker controls tool observations; the attacker cannot change the model or its system prompt.

**Policy conformance is not authorization.** A call that conforms to the policy is one the policy allows. Whether the user authorized that amount, that account for that operation, under that condition, once, is a separate question that the guarantee does not address.

## 4. Evaluation reported in the paper

- **Benchmarks** [P, Section 8.1, p. 8]. AgentDojo (banking, Slack, travel, workspace) and ASB (ten agent scenarios, five attack templates). Metrics: utility without attack, utility under attack, attack success rate.
- **Instantiation on AgentDojo** [P, p. 8]. Generic policies allow non-sensitive read-only tools; task-specific policies are generated and updated by the model. The authors "intentionally refrain from manually forbidding any tools or tool call arguments in this mode".
- **Main result, AgentDojo, all four suites together** [P, Figure 3, p. 9; p. 2]. No defense: utility 79.4 without attack and 54.0 under attack, attack success 39.9. Progent: 76.3, 61.3 and 1.0.
- **ASB** [P, Figure 4, p. 9]. No defense 78.2, 71.1, 70.3; Progent 78.2, 69.7, 3.9. With hand-written policies the authors state that attack success can be reduced to 0% [P, p. 9].
- **No banking-only figure is reported.** The word "banking" occurs in the description of the suites (p. 8) and of a multi-agent system (p. 11) only. No result for hand-written AgentDojo policies is reported in this version.
- **Compared defenses** [P, p. 8; Figure 3]. repeat_user_prompt, spotlighting_with_delimiting, tool_filter, transformers_pi_detector, DataSentinel, LlamaPromptGuard2.
- **Adaptation after a refusal.** The agent receives the fallback message and continues [P, p. 5; Figure 1, p. 3]. The evaluation is therefore a live, closed-loop one, bounded by `max_steps` (Algorithms 1 and 3).
- **Experimental details** [P, Appendix D, p. 14]. Model checkpoints are listed. Two travel injection tasks (preference attacks) are excluded; the results of one Slack injection task were corrected by hand because the benchmark's check counts a blocked call as a success.
- **Integration** [P, Section 7 p. 7; Section 8.3 pp. 10-11; Appendix F pp. 15-16]. Library mode and proxy mode; a LangChain middleware; a wrapper for the OpenAI Agents SDK; OpenHands and AutoGen through the proxy; AgentDojo migrated to MCP servers. Reported attack success about 1% across these (Figure 8).

## 5. Ablations the paper already contains

Progent has an ablation section. No gap may be claimed from its absence.

| Ablation | Finding | Where |
|---|---|---|
| Approver configuration: Disable Update, Auto-Deny, Auto-Approve, Manual Approval | Attack success 2.5, 0.7, 1.0 and 0.0 (no defense 39.9). Auto-Deny is the most secure automatic setting; Auto-Approve has more utility than Disable Update; Manual Approval reaches 0 | Section 8.2, pp. 9-10; Figure 5 |
| Initial policy only (no updates) | Attack success 39.9 to 2.5 | Section 5, p. 7 |
| Share of expansions | 6% of updates | pp. 4, 10 |
| Policy model: gpt-4o, claude-sonnet-4, gemini-2.5-flash, gpt-4.1 | Below 5% for all; 1% for the best | Section 8.2, p. 10; Figure 6 |
| Agent model: gpt-4o, claude-sonnet-4, gemini-2.5-flash, gpt-4.1, Meta-SecAlign-70B | Lower attack success for every agent; 6.8 to 0.5 and 4.8 to 0.3 for the two already robust agents | Section 8.2, p. 10; Figure 7 |
| Adaptive attacks under Auto-Approve: "If-then-else", "Allow attack tool call", AgentVigil | Attack success 0.5, 4.2 and 0.9 against 1.0 | Appendix E, pp. 14-15; Figure 10 |
| Hand-written policies on ASB | Attack success 0% (stated) | p. 9 |
| Agent frameworks and a multi-agent system | About 1% | Section 8.3; Figure 8 |

## 6. Paper version, current code and the pinned comparator

Repository history read [C]: `585ff0f` (17 Apr 2025, init), `9befb41` (10 Sep 2025), `8a8eb89` (13 May 2026), `5be7b63` (24 Sep 2026, adds the MIT licence), `b02783b` (26 Oct 2026), `0d7ea07` (15 Nov 2026, head when read).

1. **The manual banking policy is not a configuration of the uploaded paper.** At `9befb41` the banking suite defines, under `# manual policies`, a list of five trusted recipients for `send_money`, `schedule_transaction` and `update_scheduled_transaction`, unconstrained entries for the read tools and `update_user_info`, and no entry for `update_password`; `agentdojo/run.sh` sets `SECAGENT_GENERATE="False"` and logs to `logs/no-update`. At `8a8eb89`, one day before version 3 of the paper, that block is gone: the banking suite keeps only the generic policy (`update_always_allowed_tools(["get_most_recent_transactions"], allow_all_no_arg_tools=True)`) and `run.sh` sets `SECAGENT_UPDATE="True"`. The comparator PG of this project is the policy of `9befb41`. **It is a published artefact of the repository at an earlier date; version 3 of the paper neither describes nor evaluates it.** Which earlier paper version it accompanied was not verified.
2. **Where the subset check runs** [C, `secagent/tool.py`, `generate_update_security_policy`]. The check is called only when `SECAGENT_ONLY_ALLOW_NARROW` is true (the paper's Auto-Deny). In the default configuration the generated policy replaces the previous generated policy directly. For Auto-Approve the resulting policy is the same as "classify, then approve everything"; the classification itself is not executed on that path.
3. **The implemented check was weaker than the property it stands for until 15 November 2026** [C, commit `0d7ea07`, message and diff]. Its message states that the translation to solver constraints ignored JSON Schema keywords it did not translate, so that under Auto-Deny replacing `{"const": "a"}` by `{"const": "b"}` was accepted as a narrowing. The fix refuses untranslated keywords. The function's documentation at head lists remaining limitations: type changes are not detected by default; nested and mixed-type arrays are not searched; objects are not modelled; regular expressions are translated over ASCII only; some constructs make the check undecided. **Monotonic confinement is a property of the procedure as specified in Section 6; the released code approximates it.**
4. **Benchmark version.** The repository bundles AgentDojo 0.1.29 at all three commits [C]. This project's recordings are from 0.1.35; the eleven banking tools have the same parameters in both (checked in the first study).
5. **Licence.** MIT from `5be7b63` on; no licence file at `9befb41`. This project reads two source files of `9befb41` as data to obtain the policy, with attribution, and copies no code.

## 7. What REM could reuse, and what REM does not implement

| Element of Progent | In REM today | Reuse |
|---|---|---|
| Deterministic allow/forbid rules over arguments with regular expressions and enumerations | No policy language; REM's predicate D1 prohibits tools | Could be adopted as the format of declared policies (attribution; MIT for code after 24 Sep 2026) |
| Narrowing/expansion check by SMT | Not implemented. REM's request compiler runs once and never widens | Relevant only if REM ever updates permissions during an episode |
| Policy generation and update by a language model | Not implemented; REM compiles the request with a deterministic parser | Would need a model; a different design |
| Fallback message that lets the agent continue | Not evaluated: all REM results are replay without adaptation | Needs a live harness (blocked) |
| Generic policies with priorities; approver module | D1/D2 predicates only; no reviewer in any experiment | Design-level |
| Integration with LangChain, OpenAI Agents SDK, MCP proxy | Not implemented | Later phase, own protocol |

What REM's extension has that the paper does not describe: a typed link between amount and account, the effect of the operation (immediate transfer, creation or modification of a standing order), evaluation of a stated balance condition, a record of executed payments (fulfilment), consequence tiers with declared costs, and a learned estimator. Whether any of this matters in practice is an empirical question (Section 8).

## 8. Page-anchored comparison

| Dimension | Progent (paper v3) | REM v1.0 / v1.1 | G3 | L4 | HV |
|---|---|---|---|---|---|
| Enforcement point | Tool call [P, p. 2] | Tool call | same | same | same |
| Source of the constraint | Policy written by a language model from the query, then updated; optional hand-written generic policy [P, pp. 7-8] | Evidence about provenance of arguments; no representation of the request | Deterministic parser of the request | G3's evidence | L4 plus a direct-amount constraint |
| Decision | Deterministic rule match; default block [P, Alg. 2] | Calibrated probability, tiers, expected loss, four verdicts | Rule: release iff supported | Authority guard, then ridge model and two-verdict expected loss | as L4, then value constraint |
| Updates during the episode | Yes; narrowing automatic, expansion by approval [P, Alg. 3] | None | None | None | None |
| State across calls | Not in the policy language [P, Fig. 2b]; the model may rewrite the policy | Behavioral features (v1.0) | Executed payments are tracked | same | same |
| Amount tied to account; operation effect; balance condition | Expressible per rule as conditions on arguments if the model writes them; not evaluated as such in the paper | No | Yes | Yes | Yes, plus directly stated amounts |
| Formal property | Monotonic confinement [P, Section 6] | None | None | None | None |
| Reviewer | Approver module; auto-approve in the main results [P, p. 8] | Escalate verdict; no reviewer in any experiment | none | none | none |
| Evaluation mode | Live agents, closed loop, four models and several frameworks [P, Section 8] | Recorded-trace replay, no adaptation [R] | replay [R] | replay [R] | replay [R] |
| Banking evidence | None separately; four suites pooled [P, Fig. 3] | Banking only [R] | banking only [R] | banking only [R] | banking only [R] |
| Ablations | Yes [P, Section 8.2, Appendix E] | Yes (thesis, Section 4.5) | Yes | Yes | follow-up of one constraint |
| What was run in this project | Only the manual banking policy of `9befb41`, as data, in replay [R]. The framework itself, generated policies, updates and approvers: not run [X] | all arms [R] | [R] | [R] | [R] |

## 9. A narrow question that the sources leave open

Tool-boundary enforcement, task-aware policies, least privilege, dynamic updates and ablation studies are all in Progent; none is new in REM. What neither the paper nor this project has measured is narrower:

> For financial actions, when strong deterministic authorization constraints are already in place, does a documented learned or statistically calibrated decision on the remaining uncertain calls add measurable utility without losing security, compared with the constraints alone?

This is a research question, not an established gap or contribution. The present study measures it on development data only (`03_RESULTS.md`). A second open question, whether typed and stateful financial authorization prevents policy-conformant but unauthorized calls (a wrong amount to an allowed account; a repeated payment) that an argument allow-list admits, cannot be answered fairly with the present fixtures, whose accounts lie outside the allow-list of the one Progent policy that can be run here.
