# Discussion chapter: proposed updates

## D-1 Excessive withholding

> REM's low attack success in replay is achieved largely by withholding high-consequence actions. Under the declared costs an Allow verdict for a value transfer requires a calibrated probability below 0.03 (tier 3) or 0.015 (tier 4), while the first transfer of an episode receives 0.031–0.033 from the intercept, the repeated-call term and the privilege-rise feature alone in six of the nine folds (0.013–0.030 in the other three), and 0.05–0.09 after a file read whenever that transition is absent from the fold's benign reference. In this configuration REM therefore behaves, for first payments, close to "escalate every payment"; whether that is acceptable depends on the availability and cost of review.

## D-2 Financial authorization semantics

> Financial authorization concerns whether the account holder requested a specific operation with specific parameters. REM's evidence describes where argument values came from. These coincide only when the attacker's values are copied from untrusted content; they diverge when legitimate tasks take their values from documents (common in the benchmark: 74% of legitimate transfers had a recipient or amount drawn from a tool output) and when unrequested actions reuse values the user mentioned.

## D-3 Argument substitution

> REM detects substitutions copied from untrusted text in probability (12 of 14 substituted payments in the probes), but its decisions do not release the corresponding legitimate payment, and it cannot detect substituted values that appear nowhere or that coincide with values in the trusted text. REM has not solved argument substitution.

## D-4 Why provenance matching is insufficient

> The two repairs explored post hoc illustrate the gap: removing behavioural evidence that is not corroborated by provenance evidence released legitimate payments, but also released payments the user had explicitly not requested, because their arguments were fully "trusted". A requested operation family, or trusted provenance of the arguments, does not establish authorization of a particular call.

## D-5 Security versus usability

> The idealized-reviewer bound (166 of 334 benign successes at unchanged attack counts) shows that REM's ranking is informative but that, without review, the cost model converts uncertainty about high-consequence actions into withholding. Lowering that cost requires evidence of authorization, not lower costs or suppressed evidence.

## D-6 Threats to validity (add)

- Offline step-level recorded-trace replay under NO-ADAPT; no live agent was executed.
- Post-hoc arms on a single reused corpus; no multiplicity correction.
- Declared exploratory costs and tiers (SD-1).
- Fold dependence of the first-payment verdict.
- Fixture probes written by one informed author.
- Candidate code not available to the audit.
- The parser-boundary deviation is absent from the corpus but present in realistic invoices.
