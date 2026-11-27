# Implications, decisions required, and the next steps

## 1. Implications for the thesis

These are proposals and have not been applied: the thesis files are unchanged. A thesis change requires the supervisor's agreement, and the text would be added as a clearly dated new section.

| Thesis statement now | What the new evidence adds | Proposed change |
|---|---|---|
| Behavioral evidence lowers task completion without measured security benefit (Sections 4.5.7, 5.5) | That is true without evasion. Under evasion of the action family, the behavioral family is what keeps REM v1.0 at 90 successful attacks instead of 653. | Qualify: "without measured security benefit when no control is evaded" |
| REM v1.1 is recommended as a versioned amendment (Section 3.13) | v1.1 has no second evidence family left. Under action-family evasion it collapses to the no-defense level. | **[SUPERVISOR DECISION REQUIRED]** Keep v1.1 with this limitation stated, or keep v1.0 as the reference |
| Five-layer architecture (Chapter 3) | Depth is measured, not assumed. Two families give depth; Detection adds none. | Add a Defense-in-Depth evaluation section (DiD-1, DiD-2) to Chapter 4, and one limitation to Chapter 5 |
| Ablation described as component-level (Section 4.5) | The existing ablations are training-time ablations. Evasion is a distinct test. | Add the distinction explicitly |

## 2. Proposed enhancements (classification P; none implemented)

Each is a candidate for a separate pre-registered study. Each stays within the five layers and needs a supervisor decision before it becomes part of REM.

| ID | Proposal | Layer | Expected effect | What it needs |
|---|---|---|---|---|
| E1 | An independent Detection signal: implement x~ctx1~ (a fixed pre-trained injection classifier) | Detection | A third, independent family; it would test whether Detection can add depth | A classifier choice (D-8). Offline, no budget. |
| E2 | Canonicalize identifiers before the provenance match (already specified as future work item 7) | Behavioral (action) | Removes the reformatting route against K4 | Offline; the change has a spec |
| E3 | A credential-specific action control (for example, a password value whose provenance is untrusted content) | Behavioral (action) | Removes the single-family dependency of credential attacks found in DiD-2 | Design decision; offline evaluation |
| E4 | Raise the specificity of the behavioral family (x~beh3~ fires on 71% of legitimate state-changing calls) | Behavioral | Keeps depth with less over-blocking | Design decision |

## 3. Experiments that remain possible without new resources

| ID | Experiment | Status |
|---|---|---|
| DiD-3 | E-real evasions for the other families: paraphrased injections without trigger words (Detection), and the attacker mimicking the benign tool order (x~beh4~). Rewrite injected texts deterministically, as in the reformatting probe, then replay. | Can be pre-registered and run offline |
| DiD-4 | DiD-1 and DiD-2 on the second population (2,113 episodes) and under the double holdout (S2) | Can be run offline |
| DiD-5 | Cost-aware depth: the same evasions under the declared cost grid (H-10) | Can be run offline |

## 4. Requires new resources (R)

- Live closed-loop evaluation, which is the only test of adaptive evasion.
- A human label audit.
- A reviewer model, which would make Modify and Escalate distinct.
- A second benchmark.

## 5. Journal track (separate from the thesis)

**Working thesis of a paper:** "Five layers are not depth." The paper would make four claims:
1. Training-time ablation and test-time evasion give different verdicts on a runtime defense's components.
2. In REM, depth exists against single-control loss but rests on two low-specificity families.
3. The detection layer adds none.
4. Simplifying the defense for utility removes its depth.

This is a methodological contribution that does not depend on REM being better than other defenses. It requires DiD-3 and DiD-4 before submission, and live evaluation for a strong venue.
