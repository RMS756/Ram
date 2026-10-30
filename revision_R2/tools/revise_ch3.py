"""Produce the R2 revision of Chapter 3 (exact replacements; stops on any mismatch)."""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src = open(os.path.join(ROOT, "thesis", "CHAPTER3_METHODOLOGY.md"), encoding="utf-8").read()
s = src
log = []


def rep(old, new, tag):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"[{tag}] expected 1 match, found {n}: {old[:90]!r}")
    s = s.replace(old, new)
    log.append(tag)


def between(start_marker, end_marker, new, tag):
    global s
    a = s.index(start_marker)
    b = s.index(end_marker, a)
    s = s[:a] + new + s[b:]
    log.append(tag)


# C1 scope ---------------------------------------------------------------------
rep("""- Runtime mediation of each proposed tool call before it is released.

**Out of scope:**""",
"""- Runtime mediation of each proposed tool call before it is released.
- *[Proposed scope amendment, pending supervisor approval]* A recorded-trace replay sensitivity analysis under a stated no-adaptation assumption (Section 3.11.11). It is reported as exploratory evidence about fixed recorded trajectories, not as an estimate of enforcement against live or adaptive agents.

**Out of scope:**""", "C1a scope in")
rep("- Counterfactual estimation of intervention value by replaying agent trajectories.",
    "- Counterfactual estimation of intervention value for adaptive agents, for example by replaying agent prefixes and executing alternative actions from the same state (C. Zhang et al., 2026).",
    "C1b scope out")

# C2 architecture figure ---------------------------------------------------------
between("**Figure 3.1. REM architecture.** The figure is to be drawn with the following elements and no others:",
        "### 3.2.3 Layer interfaces",
        """![Figure 3.1. REM architecture as implemented. Five layers at the tool-execution boundary; offline fitting and recalibration are cross-cutting and never run within an episode; the audit record is written for every step and its attribution cannot reach the verdict.](results/pilot_R2/figures/fig_architecture.png){width=100%}

Figure 3.1 shows the runtime path from the proposed tool call through Layers 1–5 to the environment, the return of tool results as untrusted context, the append-only audit record, and the cross-cutting offline fitting. The human reviewer to whom Escalate refers is outside REM. In this thesis no reviewer is present, and escalations are resolved by the two bounds of Section 3.11.7.

""", "C2 figure")

# C3 hygiene --------------------------------------------------------------------
rep("Invisible and formatting characters, such as zero-width characters, are removed from untrusted text before further processing. This is a deterministic hygiene step. It reduces some encoding-based concealment but does not prevent paraphrase-based evasion.",
    "Invisible and formatting characters, such as zero-width characters, are removed from untrusted text before further processing. This is a deterministic hygiene step applied to **REM's analysis copy** of the text. The content delivered to the agent is not altered, because REM is non-invasive (AS-1); hygiene therefore protects REM's feature computation, not the agent. It reduces some encoding-based concealment but does not prevent paraphrase-based evasion.",
    "C3 hygiene")

# C5 lambda -----------------------------------------------------------------------
rep("The exact scaling constant of the penalty in le Cessie and van Houwelingen (1992) is pending full-text verification. This does not affect the method: λ is selected by grouped cross-validation on held-out log-loss (Section 3.9), and rescaling the penalty by a positive constant changes the selected value of λ, not the set of attainable solutions. Software libraries often parameterize the penalty through an inverse strength; the mapping used in implementation will be documented from the library version used.",
    """**Reference parameterization of λ.** This thesis fixes the penalty as written in Equation 3.2, λ‖β‖². The implementation (Chapter 4) minimizes the negative log-likelihood plus (λ_{impl}/2)‖β‖², so the two parameterizations correspond exactly when λ = λ_{impl}/2. Because λ is selected from a *finite* grid, the two scales are equivalent only under this conversion: the declared grid λ_{impl} ∈ {0.01, 0.1, 1, 10, 100} is the grid λ ∈ {0.005, 0.05, 0.5, 5, 50} on the scale of Equation 3.2. Every selected value is reported on both scales. The scaling constant in le Cessie and van Houwelingen (1992) has not been checked against the full text; it does not affect the method, which depends only on the stated objective and the declared grid.""",
    "C5 lambda")

# C6 calibration target -------------------------------------------------------------
rep("*Status:* established from source (Guo et al., 2017).\n\nFour properties of this choice are stated.",
    "*Status:* established from source (Guo et al., 2017).\n\n**Fitting target.** Equation 3.4 fits the calibration map to the observed labels y_i. Platt's original procedure instead fits against smoothed targets, t₊ = (N₊ + 1)/(N₊ + 2) and t₋ = 1/(N₋ + 2), to reduce overfitting on small calibration sets. This thesis takes Equation 3.4 as the reference definition and evaluates Platt's smoothed targets as a sensitivity analysis.\n\nFour properties of this choice are stated.",
    "C6 calibration target")

# C7 predicate order / missing evidence ----------------------------------------------
rep("Π, k_{D2}, and the evidence required at each tier are declared policy. When a predicate applies, it determines the verdict, the expected-loss rule is not consulted, and the audit record names the predicate as the source of the verdict. Both predicates are disabled in one ablation (Section 3.11.7).",
    """Π, k_{D2}, and the evidence required at each tier are declared policy. When a predicate applies, it determines the verdict, the expected-loss rule is not consulted, and the audit record names the predicate as the source of the verdict. Both predicates are disabled in one ablation (Section 3.11.7).

**Order of evaluation and unavailable evidence.** Availability of each feature is determined first, from the proposed action alone. D1 and then D2 are applied *before* any probability enters the decision, so no verdict that a predicate fixes depends on a value computed from unavailable evidence. Two cases follow:

- **A predicate fixes the verdict.** s_t and p_t may still be computed and stored for audit, but they are marked as not used, and the audit record contains no risk table: the field is recorded as *not applicable* (Section 3.7.6).
- **No predicate applies, but a feature is unavailable** (possible only below k_{D2}). The feature takes its "not observed" value 0, and the audit record flags the imputation. This is a design definition: an unavailable indicator is treated as not fired, which can only lower the estimated probability. It is therefore used only below the tier at which missing evidence forces escalation.""",
    "C7 predicate order")

# C8 tie + reviewer ----------------------------------------------------------------
rep("*Status:* adapted from source; the tie-breaking order is a design definition that makes the rule a function.",
    "*Status:* adapted from source; the tie-breaking order is a design definition that makes the rule a function. Ties are counted and reported whenever the rule is evaluated, so that the influence of the tie order on any result is visible.",
    "C8 tie")
rep("All declared costs are non-negative and expressed in common relative units. Correct automatic decisions are assigned zero loss, which is a declared convention. The Escalate entries assume a reviewer who resolves escalations correctly; this assumption is examined in Sections 3.12 and 3.14.",
    """All declared costs are non-negative and expressed in common relative units. Correct automatic decisions are assigned zero loss, which is a declared convention.

**Reviewer assumptions.** The Escalate entries assign the same loss C_{esc} whatever the label. This assumes a reviewer who:
- resolves every escalation correctly (accuracy 1);
- does so within the time the transaction allows, with delay and effort priced into C_{esc};
- is always available.

The verdict rule is optimal only under these assumptions. They are not tested in this thesis, because no reviewer is present. The rule is instead *evaluated* under two bounds (Section 3.11.7): an idealized reviewer that satisfies the assumptions, and no reviewer, in which every escalation withholds the action. A policy designed for a perfect reviewer and evaluated without one is expected to withhold legitimate actions; that cost is reported, not hidden. A reviewer with error rate e would add e·C_{miss}(k) to the adversarial entry and e·C_{FA}(k) to the legitimate entry of Escalate; such a model is not specified here.""",
    "C8 reviewer")

# C9 audit record ----------------------------------------------------------------------
rep("""For every verdict the Decision Engine writes an audit record containing:
- the evidence vector x_{t}, the logit s_{t}, and the probabilities p̃_{t} and p_{t};
- the tier k_{t} and the conditional risks R_{t}(v);
- the verdict v_{t} and its source (D1, D2, or the expected-loss rule);
- the model, calibration, and policy versions;
- a linear attribution of the logit.""",
"""For every verdict the Decision Engine writes an audit record containing:
- the identity of the proposed action: tool name and a digest of its arguments, recorded *before* any mitigation alters the step. Raw argument values, which may include credentials, are not stored;
- the evidence vector x_{t} with its availability flags, the logit s_{t}, and the probabilities p̃_{t} and p_{t}, with a flag stating whether p_{t} was used for the verdict;
- the tier k_{t} and the conditional risks R_{t}(v), or *not applicable* when D1 or D2 fixed the verdict;
- the verdict v_{t} and its source (D1, D2, or the expected-loss rule), and the mitigation applied;
- the model, calibration, and policy versions;
- a linear attribution of the logit.""",
    "C9 audit fields")

# C10 baseline comparability ------------------------------------------------------------
rep("""The targets satisfy α_{mod} > α_{blk}. Predicates D1 and D2 apply as in Section 3.7.4, so the baseline issues Escalate only through D2.

*Status:* design definition.""",
"""The targets satisfy α_{mod} > α_{blk}. Predicates D1 and D2 apply as in Section 3.7.4, so the baseline issues Escalate only through D2. In implementation the candidate set for θ also includes a value just above the largest benign probability, so that α = 0 can be met.

*Status:* design definition.

**What the comparison isolates.** REM and the baseline share the estimator, the calibration and the predicates. They differ in two respects: REM's losses depend on the consequence tier, and REM's expected-loss rule can choose Escalate, whereas the baseline can escalate only through D2. A difference between them therefore reflects both consequence tiers and the extra escalation opportunity, not tiers alone. A third configuration separates the two: **REM without expected-loss Escalate**, in which Escalate is removed from the set 𝒱(a_t) used by Equation 3.7 but D2 is kept, gives REM exactly the baseline's opportunity to escalate.""",
    "C10 baseline comparability")

# C11 Table 3.14 ------------------------------------------------------------------------
between("**Table 3.14. Verdict-to-mitigation mapping**", "Tool restriction is the single Modify mechanism",
"""**Table 3.14. Verdict-to-mitigation mapping: reference (step-level) semantics and the episode-level variant**

| Verdict | Step-level semantics (reference) | Episode-level variant |
|---|---|---|
| Allow | a_{t} is released across TB-3 and the event is logged. | Same, unless the tool is restricted in S, in which case a_{t} is refused. |
| Modify | a_{t} is withheld, and a structured tool-restriction notice is returned for this call only. No restriction persists. Applies only to tools in 𝒯_{R}. | a_{t} is withheld, and the tool class of a_{t} (its action category within 𝒯_{R}) is added to S for the rest of the episode. |
| Escalate | a_{t} is withheld and referred for review; it is released only if the reviewer approves. | Same. |
| Block | a_{t} is not executed, and a structured refusal is returned. No other tool is affected. | a_{t} is not executed, and every tool in 𝒯_{R} is added to S, so no further side-effecting action is released in the episode. |

**Which semantics is the reference.** The design decisions of Stage 2 fix step-level semantics: Block prevents the current action, and Modify applies one declared mechanism to the current action. Any restriction that persists through the episode is a separate experimental policy. The episode-level reading was specified in an earlier version of this chapter. Both are implemented and evaluated, and step-level semantics is the reference definition. Under the replay of Section 3.11.11 the two cannot differ, because a non-adaptive agent never retries a refused tool; distinguishing them requires live, adaptive agents.

""", "C11 Table 3.14")
rep("Tool restriction is the single Modify mechanism because it is deterministic, does not depend on an LLM rewriting content, and can be measured.",
    "Tool restriction is the single Modify mechanism because it is deterministic, does not depend on an LLM rewriting content, and can be measured. Under step-level semantics, Modify and Block have the same effect on the current call; they differ in the declared loss (Table 3.13), in the notice returned to the agent, and, under the episode-level variant, in what persists.",
    "C11b")
rep("1. **Restrictiveness ordering.** Block halts all further side effects, Escalate defers the decision, and Modify removes one tool class. This ordering underlies the tie-breaking order of Equation 3.7.",
    "1. **Restrictiveness ordering.** Under the episode-level variant, Block halts all further side effects, Escalate defers the decision, and Modify removes one tool class. Under step-level semantics the ordering reflects the declared losses rather than persistence. The ordering underlies the tie-breaking order of Equation 3.7.",
    "C11c")

# C12 Algorithm 1 ------------------------------------------------------------------------
between("```\nAlgorithm 1. REM Runtime Evaluation and Mitigation", "## 3.11 Experimental Methodology",
"""```
Algorithm 1. REM Runtime Evaluation and Mitigation (as implemented; Chapter 4)

Frozen (offline, per fold):  β0, β, γ1 (> 0), γ0, x̄, benign transition set,
                             privilege map, instruction-pattern set, n_max
Declared policy:             κ, L (Table 3.13), Π, k_D2, required evidence, 𝒯_R,
                             tie order Block ⪰ Escalate ⪰ Modify ⪰ Allow,
                             mitigation semantics ∈ {step-level, episode-level}
Input at step t:             objective g; tool results since the last step;
                             proposed call a_t = (tool, args); history H_t; restrictions S
Output:                      verdict v_t; released or withheld call; audit record r_t

 1  for each tool result returned since the last decision point:           // Layer 1
 2      label it untrusted; strip invisible characters in REM's copy;
 3      extract identifiers and profile values from sensitive reads
 4  begin a decision point (calls proposed in one agent message share it)
 5  for each proposed call a_t in the message:
 6      x_t, avail ← features of Tables 3.8–3.9 from H_t, a_t, g           // Layers 2–3
 7      k_t ← κ(z_t)                                                       // Layer 4
 8      s_t ← β0 + βᵀx_t;  p_t ← σ(γ1·s_t + γ0)       // computed for audit; see lines 9–14
 9      if tool(a_t) ∈ Π then v_t ← Block; src ← "D1"; R ← not applicable
10      else if k_t ≥ k_D2 and required evidence ⊄ avail then
11          v_t ← Escalate; src ← "D2"; R ← not applicable
12      else                                   // unavailable features below k_D2 are 0 and flagged
13          V_t ← {Allow, Escalate, Block} ∪ ({Modify} if tool(a_t) ∈ 𝒯_R)
14          R[v] ← (1 − p_t)·L(v,0,k_t) + p_t·L(v,1,k_t) for v ∈ V_t;  v_t ← argmin, ties by order
15      // Layer 5
16      if episode-level and tool(a_t) ∈ S then refuse a_t
17      else if v_t = Allow then release a_t
18      else if v_t = Modify then withhold a_t; if episode-level, S ← S ∪ class(a_t)
19      else if v_t = Escalate then withhold a_t; release only on reviewer approval
20      else (Block) withhold a_t; if episode-level, S ← S ∪ 𝒯_R
21      r_t ← (tool name, argument digest, x_t, avail, s_t, p̃_t, p_t, p-used flag, k_t,
               R, v_t, src, mitigation, φ0, φ_t, |φ0 + Σφ − s_t|, versions, REM time)
22      append r_t to the audit log; append a_t to H_t (released or not)
23  released calls execute; their results enter line 1 at the next decision point
```

Line 8 computes the probability for every step so that the audit record is complete; when line 9 or line 10 applies, the record marks p_t as not used. Lines 16–20 implement both mitigation semantics of Table 3.14. Attribution (line 21) is computed after the verdict and cannot reach it.

""", "C12 Algorithm 1")

# C13/C17 instrumentation and replay ------------------------------------------------------
rep("The LLM backbone or backbones and the attack templates are pending supervisor approval.",
    """The LLM backbone or backbones and the attack templates are pending supervisor approval.

**Execution status.** Enforcing-mode runs with a live agent require access to an LLM, which was not available for this thesis. The observe-only analyses (Sections 3.11.5–3.11.10) use recorded traces of real agents distributed with the benchmark (Section 3.11.2). Enforcement is examined only through the replay sensitivity analysis of Section 3.11.11.""",
    "C13 execution status")

# C14 labels proxy -------------------------------------------------------------------------
rep("- **Label audit.** Matching on arguments can mislabel steps, for example when an agent alters an amount. The derivation is therefore audited on a manually inspected sample of episodes, and the disagreement rate is reported.",
    """- **Label audit.** Matching on arguments can mislabel steps, for example when an agent alters an amount or reaches the attacker through a different tool. The derivation is therefore to be audited by a human annotator on a stratified sample of episodes, including ambiguous cases, and the disagreement rate reported.
- **What the label measures.** The reference-match label is a *practical proxy* for adversarial inducement. It records that the agent proposed the attacker's reference action with the attacker's key argument; it is not a causal proof that the injected content caused the proposal. A legitimate action that coincides with the attacker's reference action is mislabelled as induced, and an induced action that takes another route is mislabelled as legitimate. Both errors are measured, not assumed away.""",
    "C14 label proxy")

# dataset pinned ---------------------------------------------------------------------------
rep("These counts must be re-confirmed against the benchmark version pinned for the experiments.",
    "These counts were re-confirmed against suite v1 in AgentDojo 0.1.35. The recorded traces used in the evaluation come from the AgentDojo repository at commit 089ed468; most carry no suite-version field, and some backbones were recorded under later suite versions (Chapter 5). The label-relevant definitions of the nine injection tasks are identical in every suite version from v1 to v1.2.2.",
    "dataset pinned")
rep("so the number of traces depends on the number of backbones, attack templates, and repeated runs [DATA COUNT REQUIRES VERIFICATION].",
    "so the number of traces depends on the number of backbones, attack templates, and repeated runs. The counts used in this thesis are reported, from the data, in Chapter 5.",
    "count marker 1")
rep("and it may be small [DATA COUNT REQUIRES VERIFICATION].", "and it may be small; the observed count is reported in Chapter 5.", "count marker 2")

# C15 independence --------------------------------------------------------------------------
rep("3. **Held-out scoring.** The outer held-out fold is scored by the model fitted on the rest. All reported metrics are computed from these held-out predictions.",
    """3. **Held-out scoring.** The outer held-out fold is scored by the model fitted on the rest. All reported metrics are computed from these held-out predictions.

**Independence of every fitted quantity from the held-out fold.** For outer fold f, each of the following uses only the fitting portion D_train(f):
- the benign transition set and x̄, re-estimated also within each inner fold;
- λ, selected by grouped inner cross-validation;
- (γ₁, γ₀), fitted on out-of-fold logits from the inner folds;
- the baseline thresholds θ(α), selected on out-of-fold calibrated benign steps;
- r_mod(k), estimated from episodes outside fold f;
- the feature set: the Pilot E0 rule (Section 3.11.8) is applied to each fold's fitting portion. If the folds disagreed, each fold would use its own set. In this thesis they agree (Chapter 5).""",
    "C15 independence")
rep("If the positive-step count is insufficient, additional attack templates or backbones are added before the main experiments. The pilot never uses held-out fold predictions.",
    "If the positive-step count is insufficient, additional attack templates or backbones are added before the main experiments. The pilot never uses held-out fold predictions. Because every outer fold's held-out data belong to the fitting portions of the other folds, a single global decision taken from all folds' pilot results would use each fold's held-out data indirectly. The retention rule is therefore applied per fold, to that fold's fitting portion only.",
    "C15b E0 per fold")

# C16 configurations --------------------------------------------------------------------------
rep("- **REM.** The expected-loss verdict selection of Section 3.7.5.",
    "- **REM.** The expected-loss verdict selection of Section 3.7.5.\n- **REM without expected-loss Escalate.** As REM, with Escalate available only through D2, which gives REM the baseline's escalation opportunity (Section 3.7.7). This configuration was added after the first pilot results and is reported as a post-hoc comparison.",
    "C16 configs")

# C17 new section 3.11.11 ----------------------------------------------------------------------
rep("## 3.12 Evaluation Metrics",
"""### 3.11.11 Recorded-trace replay sensitivity analysis *[proposed scope amendment, pending supervisor approval]*

Live enforcing-mode runs were not possible (Section 3.11.1). To obtain any evidence about enforcement, each recorded episode is re-executed in the benchmark's own sandbox with REM at the tool boundary:
- a replay element emits the agent's recorded messages in order;
- the benchmark executes the released calls;
- the benchmark's utility and security checks score the result.

**Assumption NO-ADAPT.** The agent emits the calls it emitted in the recorded run, whatever REM does. A live agent may retry, rephrase or choose another tool after a refusal. Replay results therefore do not estimate enforcement against live or adaptive agents, and they cannot distinguish step-level from episode-level semantics.

**Validity checks.** An all-Allow replay must reproduce the recorded utility and security outcome. Episodes for which it does not are excluded from every replay metric, and the exclusions are reported.

**Not independent repetitions.** Replaying the same recorded trace several times is deterministic. It is not an independent repetition of LLM behavior and does not substitute for the repeated runs of Section 3.11.9.

**Relation to the excluded method.** This analysis differs from counterfactual estimation of intervention value (Section 3.1.4): it executes no alternative actions and makes no claim about what an agent would have done instead.

## 3.12 Evaluation Metrics""", "C17 replay section")

# threats: counterfactual wording consistency --------------------------------------------------
rep("so REM inherits the limitation identified by C. Zhang et al. (2026); estimating intervention value by counterfactual replay is outside the scope of this thesis.",
    "so REM inherits the limitation identified by C. Zhang et al. (2026); estimating intervention value for adaptive agents by counterfactual replay is outside the scope of this thesis.",
    "threats cf")
rep("- LLM non-determinism is characterized by repeated runs.",
    "- LLM non-determinism is characterized by repeated runs; the recorded traces contain one run per configuration, so this requirement is not met in this thesis.",
    "threats repeats")

# contribution: design vs evidence ----------------------------------------------------------------
rep("The contribution holds only to the extent that the experiments specified in this chapter support it.",
    "The contribution holds only to the extent that the experiments specified in this chapter support it. Chapter 5 reports which of these experiments were executed (offline classification, observe-only policy analysis, replay sensitivity) and which were not (live enforcing-mode runs).",
    "contribution scope")

out = os.path.join(ROOT, "revision_R2", "chapters_md", "CHAPTER3_METHODOLOGY_R2.md")
open(out, "w", encoding="utf-8").write(s)
print(len(log), "edits;", len(src.split()), "->", len(s.split()), "words")
