# Chapter 3 (Methodology): proposed updates

**Status:** proposed text only. The thesis chapters are not modified. Every item is supported by the audit evidence cited.

## M-1 Runtime context available to REM (new paragraph, Sec. 3.4)

> At each proposed tool call, REM observes the tool name and its arguments, the trusted system prompt, the user's objective, every tool output (labelled untrusted), and the episode's history of proposed calls. It does not observe a structured representation of the operation the user intended, whether a user sentence is an instruction, a question or a report of a past event, or any explicit user authorization. REM's action evidence is therefore evidence about the *provenance* of argument values, not about the *authorization* of the action.

Evidence: `REM_AUTHORIZATION_AUDIT/03_AUTHORIZATION/REM_ARGUMENT_INTEGRITY_ANALYSIS.md`, "What runtime information REM receives".

## M-2 Three properties that are not interchangeable (new definitions box)

> *Argument provenance*: whether a value occurs in trusted or untrusted text. *Action authorization*: whether the user requested this operation. *Argument integrity*: whether the executed arguments equal those the user authorized. REM's features x^act_1 and x^act_2 measure argument provenance only. Neither authorization nor integrity is represented in the evidence vector.

## M-3 Number matching rule (Sec. 3.4.3), statement of current behaviour

> Numeric argument values are matched by value against numeric tokens extracted from context text. The implemented tokenizer recognises integers, plain decimals and one thousands group without decimals; a comma-grouped decimal such as "1,312.40" is not recognised as 1312.40 (a known deviation, recorded as a test; no comma-grouped decimal occurs in the AgentDojo banking corpus used here).

## M-4 Behavioural features carry action-type information (Sec. 3.5 / Table 3.9 commentary)

> Because the privilege map assigns value transfers the highest level among the tools usually called before them, x^beh_3 fires on the first value transfer of almost every episode (85% of legitimate and 84% of attack transfers in the corpus). It therefore encodes "this is a payment" more than "this payment is induced".

## M-5 Decision semantics and the Allow boundary (Sec. 3.7.5)

Add the closed form under the declared costs:

> Allow is selected only when p_t < C_esc / C_miss(k_t), i.e. p_t < 0.03 at tier 3 and p_t < 0.015 at tier 4 under the exploratory costs.

Also state that at tier 3 Block is unreachable because the measured r_mod(3) = 0 (decision regions: `02_DECISION_TRACING/REM_VERDICT_SEMANTICS.md`).

## M-6 Escalate versus Block (Sec. 3.8, Table 3.14 commentary)

> Escalate withholds the action pending review; Block prevents it. In the primary offline configuration there is no reviewer, so an escalated action is withheld and the task step does not complete. Escalate and Block are reported separately; neither is counted as the other.

## M-7 Known limitation (Sec. 3.13 or limitations list)

> REM cannot distinguish a transfer the user requested from a transfer whose recipient and amount merely occur in the user's words (for example a historical payment mentioned in a read-only request), nor an authorized amount from one the agent invents without copying it from a tool output.
