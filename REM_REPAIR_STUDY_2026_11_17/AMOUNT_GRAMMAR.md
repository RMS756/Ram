# Typed amount grammar (repair study, 17 November 2026)

Status: `[PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]`. This is the verbatim specification from the docstring of
`experiments/repair_study/amount_verifier.py`, frozen with `PROTOCOL.md`. The code is authoritative where the two differ.
No equation here is a research contribution. Each one is an elementary exact operation (multiplication of rationals).

```text
Typed verification of payment amounts against the trusted request (repair study, 17 November 2026).

Status: [PROPOSED - EXPLORATORY - NOT PART OF THE APPROVED REM DESIGN]. Deterministic; no model call; no fitted
quantity; no equation of this module is a research contribution: it applies elementary exact arithmetic (Python's
``fractions.Fraction`` over ``decimal.Decimal`` operands) to a finite, declared grammar. The frozen compiler,
matchers, direct-value constraint and every scored arm are unchanged and are imported, not edited.

Central rule: recognizing a calculation cue is not verification of the proposed amount. Each payment instruction of
the request (from the frozen revision-3 compiler) receives one AMOUNT BINDING:

  literal          the request states the final amount directly ("send 27.35 to A")
  derived          the request states a supported arithmetic expression whose operands are literals of the request
                   ("half of 100", "25 percent of 200", "3/4 of 80", "twice 40"); the result is computed exactly
  balance_expr     the same expressions with the operand "my (current|account) balance"; the operand is the most
                   recent successful get_balance result (a structured bank field), read at decision time
  record_refund    "refund / return / send back / pay back ... what <they> sent (me)" with no arithmetic cue: the amount
                   of the incoming structured transaction record(s) from the bound account
  unresolved       a calculation cue without a supported expression, an ambiguous number format, an operand that is not
                   available, a result that is not a finite decimal (rounding unspecified), or conflicting statements
  none             the request says nothing about the amount of this instruction (no constraint is added here)

ACCEPTED GRAMMAR (case-insensitive; NUM is a numeric token parsed by the frozen ``parse_amount``; CUR is $, €, £ or the
words dollars, euros, pounds, usd, eur, gbp):

  LITERAL      VERB [the | that | this | exactly | only | just] [CUR] NUM [CUR]          not followed by %, "percent", "per cent",
                                                                              "/", "of" or "times"
               (amount | sum | payment | transfer | refund) of [CUR] NUM
               and [CUR] NUM to ACCOUNT                                     (elided verb: "send 50 to A and 30 to B")
  PERCENT      P (% | percent | per cent) of [the] [CUR] OPERAND            P a NUM; result P x OPERAND / 100
  FRACTION     (half | a half | one half) of [the] [CUR] OPERAND             1/2
               (a third | one third) | two thirds | (a quarter | one quarter) | three quarters   1/3, 2/3, 1/4, 3/4
               a/b of [the] [CUR] OPERAND with integers 1 <= a <= b <= 99, b > 0
  MULTIPLE     (twice | double) [the amount of] [CUR] OPERAND                2 x OPERAND
  OPERAND      NUM | my [current | account] balance
  (a stated amount must be followed by the end of the sentence, punctuation, an account identifier, a capitalised word
   or a function word such as "to", "for", "now"; "send the 3 tickets" states no amount)
  VERB         send | transfer | pay | wire | remit | refund | reimburse | repay | give | return

  A literal or expression binds to the first account identifier that follows it in the same sentence; if none follows,
  to the last one before it; a sentence without an account identifier binds to the instruction without a target.
  Numbers inside quoted text, inside account identifiers, and inside the condition of the sentence are never operands.

  CALCULATION CUES, searched in the sentence after recognised statements are removed (an instruction with one of them and no supported expression or literal is UNRESOLVED):
  half, third, quarter, twice, double, percent, per cent, %, difference, share, split, divide, total, sum of, plus,
  minus, remaining, remainder, the rest, additional, extra, increase, decrease, discount, fee, vat, tax, interest,
  too much, too little, times, more, less, the same amount, as much as.

Rounding: no convention is assumed. A result that is not a finite decimal is unresolved. A finite result must be equal,
exactly, to the proposed amount; a proposed amount with fewer decimal places that lies within one unit of its last place
of the result (e.g. 70.46 for 70.455) is unresolved (withheld), not accepted and not called a mismatch.

Untrusted tool text never supplies an operand, a coefficient, an expected result or an account. The only values read
from tool outputs are structured bank fields: the number returned by get_balance and the ``sender`` and ``amount``
fields of transaction records returned by get_most_recent_transactions (never their free-text ``subject``).
```

## Operations used (exact rationals; no source claimed as novel)

| Expression | Value | Representation |
|---|---|---|
| `P % of X` | P × X / 100 | `Fraction(Decimal(P)) * Fraction(Decimal(X)) / 100` |
| `a/b of X` | a × X / b | `Fraction(a, b) * X` |
| half, a third, two thirds, a quarter, three quarters | 1/2, 1/3, 2/3, 1/4, 3/4 of X | `Fraction` constants |
| twice / double X | 2 × X | `Fraction(2) * X` |
| comparison | proposed == expected | exact rational equality; the proposed argument is parsed by the frozen `amount_of` |

## Status semantics

| Status | Meaning | Guard action |
|---|---|---|
| verified | proposed amount equals an amount the request determines | none (front decides) |
| mismatch | the request determines the amount(s) and the proposal equals none | Block (`amount_mismatch`) |
| unresolved | the request ties the amount to a calculation or value that cannot be verified here | Escalate (`amount_unresolved`): withheld; not completed work without a reviewer |
| unconstrained | the request states nothing about this amount | none |

## Known limits (written before scoring)

- Delegated values outside the grammar ("the amount I usually pay", "as in the file", "accordingly") are `none`. The verifier adds no constraint, and the frozen front's delegation and history evidence applies unchanged.
- English only. Number words ("fifty") are not parsed.
- A request whose amount depends on an unstated value ("send them the difference") is `unresolved`. Supporting it would need a declared rule for that value, and any such rule written from the benchmark texts would be fitted to them.
- Binding uses the account identifier nearest after the statement in the same sentence. Requests that name the payee only by name ("Apple", "my landlord") bind to the instruction without a target.
