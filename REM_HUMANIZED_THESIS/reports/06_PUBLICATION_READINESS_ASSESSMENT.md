# Publication readiness assessment

This is a candid assessment. It gives no acceptance probability, venue ranking or readiness score, and nothing here guarantees publication in any journal.

## Current state in one paragraph

As a master's thesis, the work is coherent, carefully reported and defensible: claims are bounded and the numbers are verified against raw records. As it stands, it is **not ready for submission to a strong international journal**. This is not because of the writing. Three things stand in the way:
1. the evidence comes from offline replay of one benchmark suite;
2. the framework's mechanisms are all published;
3. the review of related work is record-level.

A journal paper is feasible if it is built around the evaluation finding rather than the framework, and if the missing evidence is added.

## Strengths a reviewer would recognize

1. **A clear, falsifiable question.** Does a learned, consequence-aware runtime decision add value over simple provenance or authorization rules?
2. **Strong controls:**
   - a baseline sharing the same estimator;
   - model-free rules;
   - a published policy decided by its authors' code;
   - held-out attack objectives and a double holdout.
3. **Pre-registration:** protocols committed before scoring, and one confirmatory run on unread recordings.
4. **Negative results reported as results**, with paired intervals and discordant counts.
5. **Reproducibility:** pinned versions, seeds and hashes, a 498-cell number check, and exact re-execution.
6. **A useful component-level ablation:** shadow mode against enforcement, and reachability of the learned decision.

## Weaknesses that would block acceptance

| Weakness | Why a reviewer would object | What would address it |
|---|---|---|
| Offline replay under NO-ADAPT only | Protection against agents that adapt to refusals is not measured, and Modify, Escalate and Block cannot differ | Closed-loop runs with at least one LLM agent and repeated runs (H-12) |
| One benchmark suite, one attacker account | Results may be specific to AgentDojo banking v1. A single attacker account favors allow-list rules. | A second suite or benchmark with varied attacker accounts (H-13) |
| No novel mechanism | Closely related designs exist (NEXUS, CASEL, AgentTrust, PROVISO) | Frame the paper as an evaluation and negative-result study, not a new framework |
| Record-level literature review | Recall of known prior art was low; several close works are known only from abstracts | A full-text related-work section, including LLM-based detectors (H-8, H-9) |
| No LLM-based defense compared under the same conditions | A reviewer will ask how REM compares with MELON, DRIFT, PromptArmor or Task Shield | Part of H-12 |
| Labels not human-audited | Proxy labels drive every metric | H-11 |
| Declared, unapproved costs | Over-blocking may be a cost artifact | Cost sweep (H-10) |
| Statistics with 9 and 16 clusters | Intervals are descriptive; no multiplicity policy | Permutation tests and a stated multiplicity policy (H-14) |

## Suggested shape of a journal paper (for the supervisor's consideration)

- **Working title:** *Does a learned, consequence-aware runtime decision beat simple rules for securing tool-using financial agents? A controlled evaluation.*
- **Core content:**
  - the evaluation protocol;
  - REM against rules and Progent's policy on identical episodes;
  - the component ablation (where protection and over-blocking come from);
  - the confirmatory run;
  - the limits of provenance evidence (the reformatting probe and the paired fixtures).
- **Add before submission:** H-10, H-11 and H-14 (all offline). Add H-12 and H-13, or present the limits of replay as the paper's explicit scope and target a venue that accepts benchmark-replay evaluations.
- **Leave out, or treat as a separate short paper:** the request-compiler extension and the redesign studies. They are exploratory and rely on development data.

## What would not help

- **Rewording the results more favorably.** The value of the work is that its negative findings are trustworthy.
- **Adding references without reading them.**
- **More experiments that do not address the weaknesses above.** Further arms on the same recordings would add researcher degrees of freedom, not evidence.
