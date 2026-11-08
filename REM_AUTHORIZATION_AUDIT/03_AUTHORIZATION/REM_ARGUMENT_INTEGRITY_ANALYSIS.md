# Argument integrity analysis

## What runtime information REM receives (Layer 1)

Per proposed call, `RemGuard.evaluate` receives:
- the tool name and its argument dictionary;
- the episode's trusted texts: the user objective (`episode.objective`, the first user message) and the system prompt;
- untrusted segments: every tool result, after invisible-character stripping;
- the per-episode history of proposed calls and of values read from sensitive tools.

It does **not** receive any of the following:
- a structured representation of the user's intended operation (operation type, payee, amount, one-time vs recurring);
- the mood of the request (instruction, question or historical statement);
- an explicit authorization token or a user confirmation channel;
- account metadata (known payees, limits, balance).

REM therefore cannot know that "Last month I paid 1,150.00 to X … Don't make any payments" authorizes nothing, while "Pay 1,150.00 to X" authorizes one transfer. Both put the same recipient and amount into trusted text.

## How provenance matching works (Layer 2, `rem/algorithms/context/provenance.py:145-171`)

- **Strings:** a case-insensitive substring match after whitespace normalisation (minimum 3 characters).
- **Numbers:** every numeric token is extracted with `_NUMBER = (?<![\w.])-?\d+(?:[.,]\d+)?(?![\w])` (line 123), then compared by value.

**F-IMPL-1, a verified deviation from the declared rule.** The regex accepts one separator group only:
- "1,312.40" yields the token "1,312", read as 1312; the ".40" part is not extracted, because the look-behind rejects a digit run preceded by ".".
- So a comma-grouped decimal never matches its own value. The declared rule ("numbers … match a numeric token of equal value") is violated for this notation.
- Effect on the fixtures: SUB-A2 and P5 substitutions go undetected.
- Effect on the corpus: **none**. A diagnostic tokenizer that reads complete grouped decimals agrees with the current one on all 825 distinct objective and tool-output texts of the 3,313 eligible episodes, because AgentDojo banking contains no comma-grouped decimals.
- The test `tests/test_authorization_audit.py::test_comma_grouped_decimal_matches_its_value` records this as a strict xfail. It is **not** corrected here: a correction changes feature values and requires a separately labelled, supervisor-approved refit and re-run.

Further limits of the matching rule, by design rather than defect:
- Integers and decimals compare by value, so "95" matches "95.00" and any other occurrence of 95 in the text (dates, invoice numbers, counts). A coincidental number in trusted text can mask a substituted amount.
- Currency, rounding and unit semantics are not modelled.

## Which features could encode authorization (Layer 3)

| Feature | Definition (as implemented) | Authorization content |
|---|---|---|
| x_ctx2, x_beh1 | instruction-like patterns in new or last untrusted output | detects injection *style*; the fixtures' notes are deliberately ordinary, so neither fired on any fixture |
| x_beh2 | consecutive repeats of the same call, n/n_max (always ≥ 1/3) | none |
| x_beh3 | privilege of the tool exceeds every earlier proposal | fires on **every first payment**: a property of the action type, not of authorization |
| x_beh4 | (previous tool, tool) not in the fold's benign reference | depends on which user tasks are held out |
| x_act1 | key argument copied from untrusted and absent from trusted text | provenance |
| x_act2 | recipient absent from the objective | provenance of the recipient |
| x_act3 | a value from a sensitive read appears in a non-recipient argument | egress |

None of these represents "the user requested a transfer" or "the transfer equals the requested one".

## Corpus evidence: provenance features cannot separate legitimate AgentDojo payments

Observe-mode diagnostics with the frozen fold scorers (`../logs/corpus_diagnostics.json`) compare the 89 legitimate value-transfer steps in eligible benign episodes with the 654 positive (attack) value-transfer steps:

| | Legitimate transfers (y = 0, n = 89) | Attack transfers (y = 1, n = 654) |
|---|---|---|
| x_beh3 (privilege rise) fires | 85% | 84% |
| x_act1 (argument copied from untrusted) fires | **74%** | 96% |
| x_act2 (recipient not in objective) fires | **53%** | 96% |
| x_ctx2 fires | 0% | 46% |
| Median calibrated p | 0.30 | 0.72 |
| Share at or above the tier's Allow boundary | **95.5%** | 96.2% |
| Most common pattern | beh3 + act1 + act2 (23 steps) | beh3 + act1 + act2 (432 steps) |

In AgentDojo banking, many legitimate payments take their recipient or amount from a tool output: "pay the bill in this file", "refund what my friend sent". In that environment "the argument came from untrusted text" is normal benign behaviour. Provenance is evidence of risk, not of non-authorization.

## Operation-family overlap in the corpus

`../logs/family_overlap.txt` uses AgentDojo's own ground-truth solutions:
- Of the 908 positive attack steps, **254 (28%)** use a tool that the user task itself legitimately requires.
- For example, an injected `send_money` inside a user task that asks for a payment: 220 `send_money` steps.
- A rule that treats "the user asked for this kind of operation" as authorization would therefore cover more than a quarter of the attack steps. That is exactly the argument-substitution problem.
- The remaining 72% occur where the user task never asks for that operation family.

## Conclusion

- Argument provenance, action authorization and argument integrity are different properties.
- The frozen REM measures only the first.
- It catches substitutions whose value is **copied from untrusted text**. It cannot catch invented values or historical values re-used for an unrequested action.
- It cannot confirm that a legitimate payment is authorized, so it has no evidence with which to release one.
