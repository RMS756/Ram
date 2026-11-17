**F. Typed verification of request-derived amounts (17 November 2026; proposed, exploratory).** An external review found two defects:
- the extension accepted any amount when the request asked for a computed one ("send half of 100 to A");
- the direct-value constraint of paragraph E read a percentage coefficient as the amount ("send 25 percent of 200 to A" released 25 and withheld 50).

Both defects are kept in the frozen modules and are documented in Chapter 4 (Section 4.5.90).

A separate verifier gives each payment instruction of the request one typed binding: a stated amount, an amount derived by a supported expression, an amount based on the balance, the amount of an incoming record to be refunded, *unresolved*, or *none*. It parses a finite, declared grammar and computes with exact rationals. No rounding, currency or tolerance rule is assumed. An unresolved amount is withheld (Escalate, with no reviewer); a computed amount that differs is blocked. The verifier can only turn a release into a refusal.

The grammar, its evidence rules and its known limits are specified in `REM_REPAIR_STUDY_2026_11_17/AMOUNT_GRAMMAR.md`. The arithmetic is elementary and is not presented as a contribution. **GV_math** is GV with this verifier in place of the lexical constraint of paragraph E. **HV_math** adds HV's stored learned decision behind it, so the two differ only in that decision.
