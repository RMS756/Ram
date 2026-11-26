# Ablation layer-coverage matrix (final compliance audit, 26 November 2026)

Thesis: `REM_Master_Thesis_Defence_Ready.pdf`. Section numbers and printed page numbers are those of the corrected build.

**Classification scale (strict):**
- **Complete layer-level ablation:** every component of the layer is removed together in one arm.
- **Partial component-level ablation:** one or more components are removed, but not the whole layer together.
- **Indirect evaluation only:** the layer is never removed; its contribution is inferred through a variant of another layer.
- **Not evaluated.**

Every count below was recomputed from the stored per-episode records (`audit/number_verification.json`) and matches the printed tables (`audit/thesis_number_check.json`: 466 cells, 0 mismatches). Primary population: 2,979 attacked and 334 benign episodes. Offline replay (NO-ADAPT), step-level mitigation, no reviewer.

## Matrix

| Layer | Design components (Chapter 3) | Variants run | What exactly is removed | Classification | Evidence (primary population) |
|---|---|---|---|---|---|
| **1 Input & Context** | Hygiene; provenance labels; entity extraction | **None isolates the layer.** A1h is a check, not an arm. A3b (Layer 3) removes the only route by which the labels enter the estimator. | Nothing in Layer 1 is removed | **Indirect evaluation only** | Hygiene changes 0 of 16,727 tool outputs, so disabling it cannot change any outcome. A3b: ROC-AUC 0.938 → 0.799; attack call executed in 49 against 24 attacked episodes (29 / 4, p < 0.001); attack goals 17 against 11 (unresolved, p = 0.15) |
| **2 Detection** | x_ctx1 injection classifier; x_ctx2 instruction-pattern indicator | A2a (x_ctx2); A2b (x_ctx2 plus x_beh1, coupled); A2c is not runnable | A2a: the one implemented feature. A2b: all of the implemented Detection signal, including its copy inside one behavioral feature. | **Partial component-level ablation.** Complete only for the implemented part; the designed classifier was never built (D-8). | A2a and A2b: attack goals unchanged (11; 0 / 0 discordant); benign tasks unchanged (105); tasks under attack +0.4 [−0.2, 1.4] (A2b) |
| **3 Behavioral Analysis** | x_beh1–x_beh4 (behavioral evidence); x_act1–x_act3 (action evidence, Table 3.6) | A3a (behavioral group); A3b (action group) | Each group alone. **Never both together.** | **Partial component-level ablation.** Both component groups are covered; a whole-layer arm was not run. | A3a: attack goals 11 (1 / 1); benign +10.5 [1.2, 22.6] (36 / 1, p < 0.001). A3b: as above. |
| **4 Decision Engine** | Estimator + calibration + expected-loss rule; tiers; predicates D1/D2; verdict set | A4a (learned decision); A4b (predicates); A4c (calibration); A4d (thresholds instead of expected loss); A4e (Modify) | Each component separately. A4a keeps the predicates. Removing the whole layer leaves no verdict, which is the no-defense reference by construction. | **Partial component-level ablation, with every component covered.** The whole-layer limit is the no-defense reference. | A4a: attack goals 672 against 11, +22.2 [14.6, 28.9] (661 / 0); benign +22.5 [8.0, 38.5]. A4d: 164 against 11, +5.1 [0.7, 13.1] (153 / 0). A4b, A4c, A4e: no attack outcome changed. |
| **5 Mitigation** | Step-level release or withhold | A5 (shadow mode: verdicts computed, nothing withheld) | The whole enforcement function | **Complete layer-level ablation** | Outcomes equal no defense on every episode (attack goals 672; benign 175). Same verdict as the enforcing framework on 6,654 of 6,684 calls. |
| Audit (cross-cutting, not a layer) | Linear Shapley attribution | none | — | Not evaluated (by design: audit-only, cannot change a verdict) | — |

## Why the Input & Context layer cannot be isolated

- **Chapter 3 says it computes no evidence.** Section 3.4: "It computes no risk evidence." Its outputs are labels and entities.
- **Its outputs are inputs, not evidence.** They feed x_act1–x_act3 and x_beh1 (Behavioral Analysis, Table 3.6) and predicate D2 (Decision Engine).
- **Removing it would mean fabricating values.** Every downstream feature and D2 would need substitute inputs (e.g. "everything trusted" or "everything untrusted"). That substitute is a design value that is not frozen. Choosing one is outside the scope of an ablation of the frozen design, and the CLAUDE.md design lock forbids it.
- **This is an architectural property, not an omission.** The thesis states it in Sections 4.5.1, 4.5.4, 4.5.5, 4.5.11 and 4.6.11 (threat 21).

## Can the study be presented as "an ablation study of the REM design"?

**Yes, with the isolation limits stated, and the corrected thesis states them.**

- **Coverage.**
  - Every implemented component that can change a verdict was removed at least once.
  - The only layer that can be removed as a whole without inventing inputs (Mitigation) was removed as a whole.
  - The two groups of each evidence-producing layer were removed separately.
- **Design.** Each variant is a configuration of the frozen harness, paired on identical episodes, with protocols committed before scoring.
- **What must not be claimed, and is no longer claimed after this audit:**
  - a "complete" ablation;
  - a "layer-wise" ablation without qualification;
  - that the Decision Engine was removed "as a whole functional unit". This wording was in Section 4.5.5 and has been corrected.

## Gaps that remain (stated as limitations, not fixed)

| Gap | Could existing evidence close it? | Decision |
|---|---|---|
| No arm removes A3a and A3b together (whole Behavioral Analysis evidence) | No. It needs a new refit of the estimator with only x_ctx2 and the intercept, which is a new experiment. | Stated as a limitation. Not strictly necessary: each group's effect is measured, and they act in opposite directions. |
| No direct Input & Context arm | No. It needs a design decision on substitute labels. | Stated as a methodological limitation (Sections 4.5.4 and 4.5.11; threat 21) |
| Detection classifier x_ctx1 absent | No | Stated (D-8; Sections 4.5.5 and 4.5.11) |
| One benchmark, replay only, development data, 9 attack and 16 task clusters | No | Stated (Sections 4.5.9 and 4.5.11) |
