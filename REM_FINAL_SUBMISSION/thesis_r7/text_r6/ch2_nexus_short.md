NEXUS (Hossain et al., 2026; MODERATE EVIDENCE; PARTLY UNVERIFIED) is the closest prior art to REM's *decision* component. It entered the review as a preprint and has since been published in the Findings of IJCNLP-AACL 2026. **Its full text has not been read.** The statements below rest on the published abstract (A) and on the README of the authors' repository (R), which can differ from the paper.

- **Architecture (A, R).** A structured-plan safety monitor that combines deterministic rules, argument-level inspection and a *calibrated* logistic-regression risk score. It selects one of four interventions per plan: allow, block, request confirmation or request revision.
- **Decision policy (R only).** A rule-first cascade with two score thresholds chosen once by a safety–utility loss over a grid. Platt scaling is reported to reduce ECE from 0.085 to 0.013. Documents in the same repository give different thresholds, and the policy of the published paper was not read.
- **Results (A).** F1 0.949 and four-class intervention accuracy 0.6406 on a 128-instance synthetic benchmark; F1 0.861 against 0.849 for rules only on R-Judge; parity with rules only on AgentHarm; a median latency of 0.38 ms.
- **The scorer against the rules (R).** A working document of 23 May 2026 states that the learned scorer gives no gain in binary detection over the rules alone and contributes to the choice among interventions (0.6406 against 0.3672). This is the pattern this thesis measures for REM.

**What REM cannot claim.** NEXUS already provides calibrated logistic scoring, a formal policy over four graduated interventions, a loss criterion for its thresholds and sub-millisecond latency.

**Where the difference lies.**
- REM evaluates each proposed tool call during execution, with the episode history; NEXUS judges a plan.
- REM selects each verdict by minimum expected loss indexed by the call's consequence tier; NEXUS, according to its repository, uses a rule cascade.
- REM is evaluated by replaying recorded trajectories of real agents in an executable banking environment.

Whether these differences change outcomes was not tested: NEXUS was not run (Chapter 4, Section 4.4.5). The full R5 text of this section is in the supplement.
