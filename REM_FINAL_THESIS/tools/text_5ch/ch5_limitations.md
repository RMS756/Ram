The limitations are discussed in full in Section 4.17. In summary, the conclusions of this thesis are bounded by:

1. **Design status.** Costs, tiers, predicates, the feature set and the label rule are declared exploratory values, not approved ones.
2. **No live evaluation.** Enforcement was estimated only by replay under NO-ADAPT. The closed-loop harness is implemented and tested but was not executed with a language model (Section 4.12).
3. **One benchmark and one attack family for fitting**, one attacker identity, and historical model snapshots.
4. **Labels** that are reference-matched attempt labels, ambiguous for one user task in early suite versions, and not audited by a human.
5. **Statistics**: nine attacked groups, one run per configuration, and no correction for multiple comparisons.
6. **Reviewer**: escalation outcomes are bounded by an idealized reviewer and by no reviewer; no real reviewer was modeled.
7. **Missing component**: no injection classifier was available for the Detection Layer.
8. **Literature**: the review was conducted at record level, without full-text screening.
