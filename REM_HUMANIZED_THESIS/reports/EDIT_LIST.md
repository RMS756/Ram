# Complete list of edits (humanization and corrections)

Generated from `edits/*.txt` by `tools/make_edit_list.py`. Category A: editorial; B: evidence-based correction. Every edit is an exact, unique replacement applied to the snapshot `orig_src/` by `tools/apply_edits.py`.

## 00_front_abstract.txt

### 1. `text_front/front_matter.md` (category A)

**Before:**

> This document is the **draft for supervisor review** dated 26 November 2026 (ninth edition, revised after a final academic review: the eighth edition of 19 November 2026 with a comparison with existing security frameworks and an ablation study of REM's five layers at component level, both requested by the supervisors; the earlier editions are preserved unchanged). It is prepared for discussion.

**After:**

> This document is the **draft for supervisor review** dated 26 November 2026. It is the ninth edition: the eighth edition of 19 November 2026, extended with a comparison with existing security frameworks and a component-level ablation study of REM's five layers (both requested by the supervisors) and revised after a final academic review. The earlier editions are preserved unchanged. The document is prepared for discussion.

### 2. `text_front/front_matter.md` (category A)

**Before:**

> - **New in this edition.** Section 4.4 is rewritten as a comparison with existing security frameworks: selection criteria, a fifteen-dimension architectural comparison, Progent's published banking policy decided by Progent's own code on three populations, and DRIFT and MELON at the level of architecture and code (DRIFT's official code executed with a scripted agent only). Section 4.5 is rewritten as an ablation study of the five layers, with a layer-to-implementation mapping, every variant compared with the full framework on the same episodes, and a statement of which layers could be isolated (only the Mitigation layer as a whole; the Input & Context layer only indirectly). All numbers of both sections were recomputed from the stored per-episode records. The units of the earlier Sections 4.4 and 4.5 are kept inside the new sections. Tables and figures of Chapter 4 are numbered sequentially; the correspondence with the eighth edition's numbers is listed in `REM_DEFENCE_READY_THESIS/THESIS_REVISION_LOG.md`, and the supplement's numbers are those of the fifth edition, as before.

**After:**

> - **New in this edition.** Section 4.4 is rewritten as a comparison with existing security frameworks. It gives the selection criteria, an architectural comparison on fifteen dimensions, the results of Progent's published banking policy decided by Progent's own code on three populations, and a comparison with DRIFT and MELON at the level of architecture and code (DRIFT's official code was executed with a scripted agent only). Section 4.5 is rewritten as an ablation study of the five layers. It maps each layer to its implementation, compares every variant with the full framework on the same episodes, and states which layers could be isolated: only the Mitigation layer as a whole, and the Input & Context layer only indirectly. All numbers of both sections were recomputed from the stored per-episode records. The units of the earlier Sections 4.4 and 4.5 are kept inside the new sections. Tables and figures of Chapter 4 are numbered sequentially. The correspondence with the eighth edition's numbers is listed in `REM_DEFENCE_READY_THESIS/THESIS_REVISION_LOG.md`; the supplement keeps the numbers of the fifth edition, as before.

### 3. `text_front/front_matter.md` (category A)

**Before:**

> **New in the eighth edition.** A final ablation of REM v1.0 under a protocol committed before scoring (now in Section 4.5.7); a comparison with the four distributed defenses through their authors' recorded runs and REM's replay on the same task pairs (now in Section 4.4.7); and a summary of the exploratory redesign studies of 18 and 19 November 2026, which were not adopted (now in Section 4.5.8).

**After:**

> **New in the eighth edition.** Three additions: a final ablation of REM v1.0 under a protocol committed before scoring (now in Section 4.5.7); a comparison with the four distributed defenses, through their authors' recorded runs and REM's replay on the same task pairs (now in Section 4.4.7); and a summary of the exploratory redesign studies of 18 and 19 November 2026, which were not adopted (now in Section 4.5.8).

### 4. `text_front/front_matter.md` (category A)

**Before:**

> The fourth edition adds a third revision of that rule, which repairs two further defects, and is shorter: the extension study is reported in three compact sections, background material of the literature review that lies outside the evaluated threat model and the design text of the unexecuted live evaluations are no longer reproduced, and the table of contents lists two heading levels.

**After:**

> The fourth edition adds a third revision of that rule, which repairs two further defects. It is also shorter. The extension study is reported in three compact sections; background material of the literature review that lies outside the evaluated threat model, and the design text of the unexecuted live evaluations, are no longer reproduced; and the table of contents lists two heading levels.

### 5. `text_front/front_matter.md` (category A)

**Before:**

> The fifth edition adds the study of 16 November 2026: the Progent paper read in full, and learned, statistically calibrated and policy-engine decisions compared behind the permission guard, which show that the guard used alone gives the same outcomes.

**After:**

> The fifth edition adds the study of 16 November 2026. In it, the Progent paper was read in full, and learned, statistically calibrated and policy-engine decisions were compared behind the permission guard; the comparison shows that the guard used alone gives the same outcomes.

### 6. `text_front/abstract_en.md` (category A)

**Before:**

> This thesis designs, implements and evaluates the Runtime Evaluation and Mitigation (REM) framework, a five-layer runtime layer placed at the tool-execution boundary.

**After:**

> This thesis designs, implements and evaluates the Runtime Evaluation and Mitigation (REM) framework, a runtime security framework of five layers placed at the tool-execution boundary.

### 7. `text_front/abstract_en.md` (category A)

**Before:**

> Removing calibration left the attack count unchanged and changed five benign outcomes, and Modify, Escalate and Block had identical effect. A final ablation committed before scoring confirmed, with paired intervals, that the learned decision accounts for all 661 attacks that REM stops (672 succeed without any defense) and admits none, at a cost of 22.5 percentage points of benign task completion, and that calibration and Modify change no attack outcome.

**After:**

> Removing calibration left the attack count unchanged and changed five benign outcomes. Modify, Escalate and Block had identical effects. A final ablation, committed before scoring, showed with paired intervals that the learned decision accounts for all 661 attacks that REM stops (672 succeed without any defense) and admits none. Its cost is 22.5 percentage points of benign task completion. Calibration and Modify change no attack outcome.

### 8. `text_front/abstract_en.md` (category A)

**Before:**

> with lower benign task completion; this comparison is descriptive, because the defenses' runs are closed-loop and REM's is a replay.

**After:**

> with lower benign task completion. This comparison is descriptive, because the defenses' runs are closed-loop and REM's is a replay.

### 9. `text_front/abstract_en.md` (category A)

**Before:**

> admitted no attack and completed more tasks under attack than REM on all three populations; its list of permitted recipients contains values specific to the benchmark.

**After:**

> admitted no attack and completed more tasks under attack than REM on all three populations. Its list of permitted recipients, however, contains values specific to the benchmark.

### 10. `text_front/abstract_en.md` (category A)

**Before:**

> it raised task completion by 7.5 percentage points (95% interval 1.2 to 16.0) with 1 successful attack against 3 of 2,065, meeting the pre-declared decision rule; the security difference is not resolved statistically.

**After:**

> it raised task completion by 7.5 percentage points (95% interval 1.2 to 16.0), with 1 successful attack against 3 of 2,065. This met the pre-declared decision rule, but the security difference is not resolved statistically.

### 11. `text_front/abstract_en.md` (category A)

**Before:**

> gave exactly GV's outcomes, except one threshold that lost tasks, because every attack-labeled call was stopped before any of them was consulted.

**After:**

> gave exactly GV's outcomes, except one threshold that lost tasks. The reason is that the guard stopped every attack-labeled call before any of these components was consulted.

### 12. `text_front/abstract_en.md` (category A)

**Before:**

> whose amounts the request does not determine; the learned decision behind it again changed nothing.

**After:**

> whose amounts the request does not determine. The learned decision behind it again changed nothing.

### 13. `text_front/abstract_en.md` (category A)

**Before:**

> did not hold; a second version repaired both on the diagnostic cases without changing any recorded outcome, and withheld one further legitimate test case.

**After:**

> did not hold. A second version repaired both on the diagnostic cases without changing any recorded outcome; it withheld one further legitimate test case.

### 14. `text_front/abstract_en.md` (category A)

**Before:**

> The results are exploratory and come from replay, not from live agents; a closed-loop harness and integrations with the MELON and DRIFT defenses are implemented and were not executed with a language model.

**After:**

> The results are exploratory and come from replay, not from live agents. A closed-loop harness and integrations with the MELON and DRIFT defenses are implemented but were not executed with a language model.

## 01_ch1.txt

### 15. `src/CHAPTER_01_FINAL.md` (category A)

**Before:**

> The thesis designs a decision layer at the action boundary, and evaluates it on recorded agent behavior in a banking environment against threshold and rule baselines.

**After:**

> The thesis designs a decision layer at the action boundary and evaluates it on recorded agent behavior in a banking environment, against threshold and rule baselines.

### 16. `src/CHAPTER_01_FINAL.md` (category A)

**Before:**

> **One versioned amendment is proposed.** The evaluation found that the behavioral evidence group lowers legitimate task completion without a measured security benefit, and a confirmatory run on recordings unread until then supported removing it for task completion; its effect on security is not resolved (Chapter 4, Section 4.6.8).

**After:**

> **One versioned amendment is proposed.** The evaluation found that the behavioral evidence group lowers legitimate task completion without a measured security benefit. A confirmatory run on recordings unread until then supported removing it for task completion, but its effect on security is not resolved (Chapter 4, Section 4.6.8).

### 17. `src/CHAPTER_01_FINAL.md` (category A)

**Before:**

> **Proposed contribution.** The contribution proposed at the design stage was empirical and integrative: the design and evaluation, on an open and executable banking benchmark under indirect prompt injection, of a non-invasive five-layer runtime layer that combines provenance-based action evidence, a calibrated per-step probability of adversarial inducement, verdict selection by minimum conditional risk with losses declared per consequence tier, and deterministic mitigation.

**After:**

> **Proposed contribution.** The contribution proposed at the design stage was empirical and integrative. It was the design and evaluation of a non-invasive runtime framework of five layers that combines provenance-based action evidence, a calibrated per-step probability of adversarial inducement, verdict selection by minimum conditional risk with losses declared per consequence tier, and deterministic mitigation. The framework was to be evaluated on an open and executable banking benchmark under indirect prompt injection.

### 18. `src/CHAPTER_01_FINAL.md` (category A)

**Before:**

> 2. **A controlled evaluation protocol.** It isolates the decision rule from the estimator, holds out whole attack objectives, adds a double holdout of user task and attack objective, compares the learned policy with rules that use no model and with one published policy replayed in the same harness, and includes one confirmatory run under a pre-committed protocol. *Evidence:* Chapters 3 and 4.

**After:**

> 2. **A controlled evaluation protocol.** The protocol isolates the decision rule from the estimator and holds out whole attack objectives, with a double holdout of user task and attack objective. It compares the learned policy with rules that use no model and with one published policy replayed in the same harness. It also includes one confirmatory run under a pre-committed protocol. *Evidence:* Chapters 3 and 4.

### 19. `src/CHAPTER_01_FINAL.md` (category A)

**Before:**

> Against the strongest simple rule it has fewer successful attacks, while the difference in completed tasks is not resolved; against a fixed-list policy from Progent's repository nothing is resolved.

**After:**

> Against the strongest simple rule it has fewer successful attacks, while the difference in completed tasks is not resolved. Against a fixed-list policy from Progent's repository, no difference is resolved.

### 20. `src/CHAPTER_01_FINAL.md` (category A)

**Before:**

> An external review then found that the guard accepted computed amounts it never computed and read a percentage coefficient as an amount; a typed amount verifier repairs both, at the cost of the tasks whose amounts the request does not determine.

**After:**

> An external review then found that the guard accepted computed amounts it never computed and read a percentage coefficient as an amount. A typed amount verifier repairs both defects, at the cost of the tasks whose amounts the request does not determine.

### 21. `src/CHAPTER_01_FINAL.md` (category A)

**Before:**

> The four defenses distributed with the benchmark are compared through their authors' recorded runs and REM's replay on the same task pairs; the comparison is descriptive.

**After:**

> The four defenses distributed with the benchmark are compared through their authors' recorded runs and REM's replay on the same task pairs. This comparison is descriptive.

### 22. `src/CHAPTER_01_FINAL.md` (category A)

**Before:**

> - any closed-loop comparison with a published defense: the four distributed defenses are compared through their authors' recorded runs against REM's replay, which is descriptive (Chapter 4, Section 4.4.7); MELON and DRIFT were not run with a language model (their official code was executed only with scripted agents); the one published policy that was replayed, decided by its authors' own code, has no successful attack and completes more tasks than REM (Chapter 4, Section 4.4.7).

**After:**

> - any closed-loop comparison with a published defense. The four distributed defenses are compared through their authors' recorded runs against REM's replay, which is descriptive (Chapter 4, Section 4.4.7). MELON and DRIFT were not run with a language model; their official code was executed only with scripted agents. The one published policy that was replayed, decided by its authors' own code, has no successful attack and completes more tasks than REM (Chapter 4, Section 4.4.7).

### 23. `src/CHAPTER_01_FINAL.md` (category A)

**Before:**

> **What the thesis does not claim:** a new algorithm; the first runtime guardrail, calibrated agent risk score or consequence-aware controller; that calibration improves control; robustness against adaptive adversaries; any prevention guarantee; that the tested features establish what the user authorized; that the permission rule of the extension generalizes beyond the benchmark's requests; or validity in production financial deployment. Each constituent mechanism is established and attributed to its source (Chapter 2, Table 2.2).

**After:**

> **What the thesis does not claim:**
> 
> - a new algorithm;
> - the first runtime guardrail, calibrated agent risk score or consequence-aware controller;
> - that calibration improves control;
> - robustness against adaptive adversaries;
> - any prevention guarantee;
> - that the tested features establish what the user authorized;
> - that the permission rule of the extension generalizes beyond the benchmark's requests;
> - validity in production financial deployment.
> 
> Each constituent mechanism is established and attributed to its source (Chapter 2, Table 2.2).

## 02_ch2.txt

### 24. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> All 104 reports sought for retrieval (45 database, 59 other-methods) were therefore *not retrieved*, and eligibility was assessed on **records**:

**After:**

> All 104 reports sought for retrieval (45 database, 59 other-methods) were therefore *not retrieved*. Eligibility was assessed on **records**:

### 25. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> No meta-analysis was possible, because the studies differ in agents, attacks, benchmarks, success definitions and metrics; the synthesis is qualitative and structured by theme, and author-reported figures

**After:**

> No meta-analysis was possible, because the studies differ in agents, attacks, benchmarks, success definitions and metrics. The synthesis is qualitative and structured by theme, and author-reported figures

### 26. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> **Why agents change the problem.** Three structural properties distinguish agent security from the security of a stand-alone model: several input channels of different trustworthiness enter the same context; state persists across a trajectory, so content read at one step can shape an action several steps later; and outputs include tool calls with external effects. Benchmark studies show that these properties matter empirically (Wei et al., 2026; Ruan et al., 2024). Tool-channel threats, memory poisoning and multi-step drift lie outside the threat model evaluated in this thesis and are not reviewed further here; the included studies that address them are listed in the evidence matrix of Appendix S-A.

**After:**

> **Why agents change the problem.** Three structural properties distinguish agent security from the security of a stand-alone model:
> 
> - several input channels of different trustworthiness enter the same context;
> - state persists across a trajectory, so content read at one step can shape an action several steps later;
> - outputs include tool calls with external effects.
> 
> Benchmark studies show that these properties matter empirically (Wei et al., 2026; Ruan et al., 2024). Tool-channel threats, memory poisoning and multi-step drift lie outside the threat model evaluated in this thesis and are not reviewed further here. The included studies that address them are listed in the evidence matrix of Appendix S-A.

### 27. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> *Input- and model-level protection* (detectors of embedded instructions, input transformation, and training the model to follow only the prompt channel) reports strong in-distribution results but acts on text, not on actions, and has been bypassed by adaptive attacks (J. Shi et al., 2026; Y. Zhang et al., 2024). *System-level and information-flow defenses* change the architecture so that untrusted data cannot steer control flow; their guarantees hold for the threat models their authors formalized, and one such design was later defeated by new attacks (Y. Wu et al., 2025; E. Li et al., 2026).

**After:**

> *Input- and model-level protection* includes detectors of embedded instructions, input transformation, and training the model to follow only the prompt channel. It reports strong in-distribution results, but it acts on text rather than on actions, and adaptive attacks have bypassed it (J. Shi et al., 2026; Y. Zhang et al., 2024). *System-level and information-flow defenses* change the architecture so that untrusted data cannot steer control flow. Their guarantees hold for the threat models their authors formalized, and new attacks later defeated one such design (Y. Wu et al., 2025; E. Li et al., 2026).

### 28. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> Their limits recur: judgment by a language model adds latency and can vary between runs, accuracies are measured on the authors' own benchmarks, and the verified records do not report calibrated probabilities that could be combined with the consequence of an action, with the single exception of NEXUS (Section 2.8.3).

**After:**

> Their limits recur. Judgment by a language model adds latency and can vary between runs, and accuracies are measured on the authors' own benchmarks. Apart from NEXUS (Section 2.8.3), the verified records do not report calibrated probabilities that could be combined with the consequence of an action.

### 29. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> **Attribution for audit.** For a linear model under feature independence, the Shapley attribution of a feature is its coefficient times the feature's deviation from a reference, and on the log-odds of a logistic model the decomposition is exact (Lundberg & Lee, 2017).

**After:**

> **Attribution for audit.** For a linear model under feature independence, the Shapley attribution of a feature is its coefficient times the feature's deviation from a reference. On the log-odds of a logistic model, the decomposition is exact (Lundberg & Lee, 2017).

### 30. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> with a comment citing legal, intellectual-property and affiliation reasons rather than an error in the benchmark; its OpenAlex record carries no retraction flag, and the withdrawal notice could not be re-checked on 28 October 2026 because arXiv was unreachable.

**After:**

> with a comment citing legal, intellectual-property and affiliation reasons rather than an error in the benchmark. Its OpenAlex record carries no retraction flag. The withdrawal notice could not be re-checked on 28 October 2026, because arXiv was unreachable.

### 31. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> The specific combination that REM implements (Gap A) was not found in the examined records, but the thesis does not rest its originality on that absence: a combination this specific is easy to miss in a record-level review, and closely related designs exist (NEXUS, AgentTrust, SafeAgent).

**After:**

> The specific combination that REM implements (Gap A) was not found in the examined records. The thesis does not, however, rest its originality on that absence. A combination this specific is easy to miss in a record-level review, and closely related designs exist (NEXUS, AgentTrust, SafeAgent).

### 32. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> At abstract level none of them compares a learned decision behind such a check with the check used alone, so the evidence gap stands; request-derived argument checking is not itself a gap.

**After:**

> At abstract level, none of them compares a learned decision behind such a check with the check used alone, so the evidence gap stands. Request-derived argument checking is not itself a gap.

### 33. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> **Selection.** The search of OpenAlex on 25 September 2026 identified 320 records. (A simulation study added in a supplementary update of 2 November 2026 is discussed separately at abstract level in Section 2.11.3; it does not change these counts.) After deduplication, 219 were screened, and 45 were assessed for eligibility at record level.

**After:**

> **Selection.** The search of OpenAlex on 25 September 2026 identified 320 records. After deduplication, 219 were screened, and 45 were assessed for eligibility at record level.

### 34. `src/CHAPTER_02_FINAL.md` (category A)

**Before:**

> Of these, 10 are HIGH, 36 MODERATE and 25 LIMITED record-visible evidence.

**After:**

> Of these, 10 are HIGH, 36 MODERATE and 25 LIMITED record-visible evidence. A simulation study added in a supplementary update of 2 November 2026 is discussed separately, at abstract level, in Section 2.11.3; it does not change these counts.

## 03_abstract_ar.txt

### 35. `text_front/abstract_ar.md` (category A)

**Before:**

> وهو طبقة تشغيلية من خمس طبقات توضع عند حدّ تنفيذ الأدوات.

**After:**

> وهو إطار أمني تشغيلي من خمس طبقات يوضع عند حدّ تنفيذ الأدوات.

### 36. `text_front/abstract_ar.md` (category A)

**Before:**

> النتائج استكشافية ومستمدة من إعادة التشغيل لا من وكلاء أحياء؛ وقد نُفّذ إطار اختبار حلقي مغلق

**After:**

> النتائج استكشافية ومستمدة من إعادة التشغيل لا من تشغيل حيّ للوكلاء. وقد نُفّذ إطار اختبار حلقي مغلق

### 37. `text_front/abstract_ar.md` (category A)

**Before:**

> أن كل أثر مقيس في النتائج يأتي من القرار المتعلَّم وهو يعمل من خلال التنفيذ في طبقة التخفيف: ففي وضع المراقبة دون تنفيذ لم تحمِ الأحكام نفسها شيئاً، وأدّت إزالة

**After:**

> أن كل أثر مقيس في النتائج يأتي من القرار المتعلَّم وهو يعمل من خلال التنفيذ في طبقة التخفيف. ففي وضع المراقبة دون تنفيذ لم تحمِ الأحكام نفسها شيئاً، وأدّت إزالة

### 38. `text_front/abstract_ar.md` (category A)

**Before:**

> مع إنجاز أقل للمهام السليمة؛ وهذه المقارنة وصفية لأن تشغيلات الدفاعات

**After:**

> مع إنجاز أقل للمهام السليمة. وهذه المقارنة وصفية، لأن تشغيلات الدفاعات

## 04_ch3.txt

### 39. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> At each step, REM executes Layer 1; then Layers 2 and 3, each computing its evidence from Layer 1's output without using the other's; then Layer 4; then Layer 5, before the proposed action is released to the environment. Layers 2 and 3 are independent computations, not concurrent ones: the implementation evaluates them one after the other in the same process (Section S-3.15). They share the declared instruction-pattern set as a resource, not each other's output. The Detection and Behavioral Analysis Layers compute their evidence independently; they are combined only in the Decision Engine. This independence allows an evidence group to be removed in ablation without changing the computation of the other.

**After:**

> At each step, REM executes the layers in this order, before the proposed action is released to the environment:
> 
> - Layer 1;
> - Layers 2 and 3, each computing its evidence from Layer 1's output without using the other's;
> - Layer 4;
> - Layer 5.
> 
> Layers 2 and 3 are independent computations, not concurrent ones: the implementation evaluates them one after the other in the same process (Section S-3.15). They share the declared instruction-pattern set as a resource, but neither uses the other's output. The Detection and Behavioral Analysis Layers compute their evidence independently, and it is combined only in the Decision Engine. This independence allows an evidence group to be removed in ablation without changing the computation of the other.

### 40. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> Because λ is selected from a *finite* grid, the two scales are equivalent only under this conversion: the declared grid λ~impl~ ∈ {0.01, 0.1, 1, 10, 100} is the grid λ ∈ {0.005, 0.05, 0.5, 5, 50} on the scale of Equation 3.2.

**After:**

> Because λ is selected from a *finite* grid, the two scales are equivalent only under this conversion. The declared grid λ~impl~ ∈ {0.01, 0.1, 1, 10, 100} is the grid λ ∈ {0.005, 0.05, 0.5, 5, 50} on the scale of Equation 3.2.

### 41. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> - **A predicate fixes the verdict.** s~t~ and p~t~ may still be computed and stored for audit, but they are marked as not used, and the audit record contains no risk table: the field is recorded as *not applicable* (Section 3.7.6).

**After:**

> - **A predicate fixes the verdict.** s~t~ and p~t~ may still be computed and stored for audit, but they are marked as not used. The audit record then contains no risk table; the field is recorded as *not applicable* (Section 3.7.6).

### 42. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> The direction of the effect of this imputation on the estimated probability is that of minus the indicator's fitted coefficient; it is not fixed by the definition, and fitted coefficients of REM can be negative (for example x^beh^~2~ in one fold of the pilot).

**After:**

> The imputation moves the estimated probability in the direction of minus the indicator's fitted coefficient. That direction is not fixed by the definition, because fitted coefficients of REM can be negative (for example x^beh^~2~ in one fold of the pilot).

### 43. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> It has the form of the standard two-class cost-sensitive threshold for zero-cost correct decisions, which Elkan (2001) obtains from the same expected-cost criterion; the printed threshold expression in that paper could not be inspected directly during verification, so the derivation above stands on Equation 3.8 alone.

**After:**

> It has the form of the standard two-class cost-sensitive threshold for zero-cost correct decisions, which Elkan (2001) obtains from the same expected-cost criterion. The printed threshold expression in that paper could not be inspected directly during verification, so the derivation above stands on Equation 3.8 alone.

### 44. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> The adversarial Modify entry is a derivation. Under the stated assumption A-Mod — whether Modify neutralizes an adversarially induced action is independent of x~t~ given the tier, and the attack fails with probability 1 − r~mod~(k) — the law of total expectation gives:

**After:**

> The adversarial Modify entry is a derivation. It rests on assumption A-Mod: whether Modify neutralizes an adversarially induced action is independent of x~t~ given the tier, and the attack fails with probability 1 − r~mod~(k). Under A-Mod, the law of total expectation gives:

### 45. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> The two semantics can release different actions even when the agent never retries a call or adapts: under the episode-level variant, Block adds every tool of 𝒯~R~ to the restriction set S, and Modify adds the tool class of a~t~, so a later, *different* state-changing call is refused even when its own verdict is Allow.

**After:**

> The two semantics can release different actions even when the agent never retries a call or adapts. Under the episode-level variant, Block adds every tool of 𝒯~R~ to the restriction set S, and Modify adds the tool class of a~t~. A later, *different* state-changing call is then refused even when its own verdict is Allow.

### 46. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> **Final ablation (added 19 November 2026).** A separately pre-registered study (Chapter 4, Section 4.5.7) repeats ablations 1–4 and 6 in replay with paired intervals and adds two arms, each changing only the decision: Modify removed from the verdict set, so that the expected loss is minimized over Allow, Escalate and Block; and the learned decision removed, so that only the predicates D1 and D2 act and every other call is allowed.

**After:**

> **Final ablation (added 19 November 2026).** A separately pre-registered study (Chapter 4, Section 4.5.7) repeats ablations 1–4 and 6 in replay with paired intervals. It adds two arms, each changing only the decision:
> 
> - Modify removed from the verdict set, so that the expected loss is minimized over Allow, Escalate and Block;
> - the learned decision removed, so that only the predicates D1 and D2 act and every other call is allowed.

### 47. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> The training targets of the last three arms were obtained by *prefix branching*: each recorded episode was replayed once with every call released and once with one call withheld and all others released, and the benchmark's attack and task outcomes of the two replays were compared. The intervention-value rule is **derived, not quoted**: C. Zhang et al. (2026) define the value of an intervention as the difference between the expected utility of intervening and of continuing and select the action with the highest expected utility; the rule above writes those two utilities in REM's declared costs for the two actions release and withhold.

**After:**

> The training targets of the last three arms were obtained by *prefix branching*. Each recorded episode was replayed once with every call released and once with one call withheld and all others released, and the benchmark's attack and task outcomes of the two replays were compared. The intervention-value rule is **derived, not quoted**. C. Zhang et al. (2026) define the value of an intervention as the difference between the expected utility of intervening and of continuing, and select the action with the highest expected utility. The rule above writes those two utilities in REM's declared costs for the two actions, release and withhold.

### 48. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> **Definition.** REM v1.1 is REM v1.0 with the behavioral evidence group removed from the evidence vector: x~t~ = [x^ctx^; x^act^], without x^beh^~1~ to x^beh^~4~. Nothing else changes. The estimator is the ridge logistic regression of Equations 3.1 and 3.2, refitted on the reduced vector by Procedure 3.1; the calibration is that of Equations 3.3 and 3.4; the consequence tiers, the predicates, the loss structure of Table 3.10, the verdict rule of Equations 3.6 and 3.7, the mitigation semantics and the audit record are those of v1.0.

**After:**

> **Definition.** REM v1.1 is REM v1.0 with the behavioral evidence group removed from the evidence vector: x~t~ = [x^ctx^; x^act^], without x^beh^~1~ to x^beh^~4~. Nothing else changes:
> 
> - the estimator is the ridge logistic regression of Equations 3.1 and 3.2, refitted on the reduced vector by Procedure 3.1;
> - the calibration is that of Equations 3.3 and 3.4;
> - the consequence tiers, the predicates, the loss structure of Table 3.10, the verdict rule of Equations 3.6 and 3.7, the mitigation semantics and the audit record are those of v1.0.

### 49. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> **E. Direct-value constraint and the guard used alone.** On 16 November 2026 a constraint was added after two fixture failures: when the request states an amount directly for an account and an operation ("send 27.35 to A"), only that amount is accepted for that call, and a number whose format is ambiguous ("1,250") is not resolved, so the call is withheld.

**After:**

> **E. Direct-value constraint and the guard used alone.** On 16 November 2026 a constraint was added after two fixture failures. When the request states an amount directly for an account and an operation ("send 27.35 to A"), only that amount is accepted for that call. A number whose format is ambiguous ("1,250") is not resolved, so the call is withheld.

### 50. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> **Version 2** requires the recognized expression to cover the whole amount phrase and accepts a call only on one instruction whose effect, account, own condition and own amount all license it; it evaluates the verifier only after the front and the rule release the call (`PROTOCOL_AMENDMENT_V2.md`).

**After:**

> **Version 2** requires the recognized expression to cover the whole amount phrase. It accepts a call only on one instruction whose effect, account, own condition and own amount all license it, and it evaluates the verifier only after the front and the rule release the call (`PROTOCOL_AMENDMENT_V2.md`).

### 51. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> The Decision Engine estimates a calibrated probability of adversarial inducement by ridge logistic regression with a logistic calibration on the logit, assigns a declared consequence tier, applies policy predicates, selects a verdict by minimizing conditional risk under tier-indexed losses, and writes an audit record whose linear attribution never influences the verdict.

**After:**

> The Decision Engine estimates a calibrated probability of adversarial inducement by ridge logistic regression with a logistic calibration on the logit. It then assigns a declared consequence tier, applies policy predicates and selects a verdict by minimizing conditional risk under tier-indexed losses. It also writes an audit record whose linear attribution never influences the verdict.

### 52. `src/CHAPTER_03_FINAL.md` (category A)

**Before:**

> **What the comparison isolates.** REM and the baseline share the estimator, the calibration and the predicates. They differ in two respects: REM's losses depend on the consequence tier, and REM's expected-loss rule can choose Escalate, whereas the baseline can escalate only through D2.

**After:**

> **What the comparison isolates.** REM and the baseline share the estimator, the calibration and the predicates. They differ in two respects. REM's losses depend on the consequence tier, and REM's expected-loss rule can choose Escalate, whereas the baseline can escalate only through D2.

## 05_ch5.txt

### 53. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> One published deterministic policy was replayed on the recorded episodes, decided by its authors' own code; its list of recipients is informed by the benchmark.

**After:**

> One published deterministic policy was replayed on the recorded episodes, decided by its authors' own code. Its list of recipients is informed by the benchmark.

### 54. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> The exploratory permission rule of Chapter 4, Section 4.6.9, is a first step that compiles such a statement from the request text; it needs requests written and reviewed by other people (the authoring instructions and a sealed scorer are in the repository), a decision on subjective conditions, and a live-agent evaluation.

**After:**

> The exploratory permission rule of Chapter 4, Section 4.6.9, is a first step that compiles such a statement from the request text. It needs requests written and reviewed by other people (the authoring instructions and a sealed scorer are in the repository), a decision on subjective conditions, and a live-agent evaluation.

### 55. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> DRIFT's official code already runs on the benchmark version used here with a scripted agent; a live run needs a model credential, an approved budget and a decision on the benchmark version, because DRIFT's defaults and its authors' runs use banking v1.2.

**After:**

> DRIFT's official code already runs on the benchmark version used here with a scripted agent. A live run needs a model credential, an approved budget and a decision on the benchmark version, because DRIFT's defaults and its authors' runs use banking v1.2.

### 56. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> Against the strongest simple rule it had fewer successful attacks, with completed tasks not resolved; a published fixed list of payees also had no successful attack.

**After:**

> Against the strongest simple rule it had fewer successful attacks, with the difference in completed tasks not resolved. A published fixed list of payees also had no successful attack.

### 57. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> gave exactly the outcomes of the guard used alone (GV), except one threshold that lost tasks, because every attack-labeled call was stopped before any of them was consulted.

**After:**

> gave exactly the outcomes of the guard used alone (GV), except one threshold that lost tasks. The reason is that the guard stopped every attack-labeled call before any of these components was consulted.

### 58. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> An external review then showed that the guard accepted computed amounts it never computed; a typed verifier repairs this, and the price is that payments whose amount the request does not determine are withheld.

**After:**

> An external review then showed that the guard accepted computed amounts it never computed. A typed verifier repairs this; the price is that payments whose amount the request does not determine are withheld.

### 59. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> It does so by withholding broadly, and calibration, Modify, the predicates and context evidence change no attack outcome. Across the five layers, every measured outcome effect comes from that decision acting through enforcement: in shadow mode the same verdicts protect nothing, and the Input & Context layer's labels matter through the action/provenance evidence built on them.

**After:**

> It does so by withholding broadly. Calibration, Modify, the predicates and context evidence change no attack outcome. Across the five layers, every measured outcome effect comes from that decision acting through enforcement. In shadow mode the same verdicts protect nothing, and the Input & Context layer's labels matter through the action/provenance evidence built on them.

### 60. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> at a lower completion of benign tasks; because their runs are closed-loop and REM's is a replay, this places REM among them without ranking it.

**After:**

> at a lower completion of benign tasks. Because their runs are closed-loop and REM's is a replay, this places REM among them without ranking it.

### 61. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> admits no attack and completes more tasks under attack than REM on all three populations; its list of permitted recipients is informed by the benchmark, so this, too, is not a ranking.

**After:**

> admits no attack and completes more tasks under attack than REM on all three populations. Its list of permitted recipients is informed by the benchmark, so this, too, is not a ranking.

### 62. `src/CHAPTER_05_FINAL.md` (category A)

**Before:**

> - **That behavioral evidence helps.** It did not; removing it raised task completion, and that gain met the pre-declared decision rule.

**After:**

> - **That behavioral evidence helps.** It did not. Removing it raised task completion, and that gain met the pre-declared decision rule.

## 06_appendices.txt

### 63. `src/APPENDICES_FINAL.md` (category A)

**Before:**

> **Table A.1. Notation used in this chapter**

**After:**

> **Table A.1. Notation used in the methodology chapter**

### 64. `src/APPENDICES_FINAL.md` (category A)

**Before:**

> are defined where they are used. Each symbol has one meaning throughout the chapter.

**After:**

> are defined where they are used. Each symbol has one meaning throughout the methodology chapter.

### 65. `src/APPENDICES_FINAL.md` (category A)

**Before:**

> **Table A.3. Provenance of the equations in this chapter**

**After:**

> **Table A.3. Provenance of the equations in the methodology chapter**

### 66. `src/APPENDICES_FINAL.md` (category A)

**Before:**

> The procedure has known optimality properties in sequential change detection: Lorden (1971) proposed stopping rules that are asymptotically optimal in a defined sense, and Moustakides (1986) showed Page's stopping time to be optimal in a stronger sense.

**After:**

> The procedure has known optimality properties in sequential change detection. Lorden (1971) proposed stopping rules that are asymptotically optimal in a defined sense, and Moustakides (1986) showed Page's stopping time to be optimal in a stronger sense.

### 67. `src/APPENDICES_FINAL.md` (category A)

**Before:**

> **Implementation conventions.** Four conventions in the implementation differ in form from the equations as printed; none changes their meaning:

**After:**

> **Implementation conventions.** Four conventions in the implementation differ in form from the equations as printed. None changes their meaning:

## 07_ch4a.txt

### 68. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Section 4.5 reports the ablation study of REM's five layers: a layer-to-implementation mapping, the pre-registered ablations of 19 and 21 November 2026 with every variant compared with the full framework on the same episodes, and the ablations of exploratory extensions that are not part of REM v1.0.

**After:**

> Section 4.5 reports the ablation study of REM's five layers. It gives a layer-to-implementation mapping and the pre-registered ablations of 19 and 21 November 2026, in which every variant is compared with the full framework on the same episodes, followed by the ablations of exploratory extensions that are not part of REM v1.0.

### 69. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> - **Tests.** On 13 November 2026 the suite of 280 tests gave 278 passed, 1 skipped and 1 expected failure; on 16 November 2026 the suite of 502 tests gave 500 passed, 1 skipped and the same expected failure.

**After:**

> - **Tests.** On 13 November 2026 the suite of 280 tests gave 278 passed, 1 skipped and 1 expected failure. On 16 November 2026 the suite of 502 tests gave 500 passed, 1 skipped and the same expected failure.

### 70. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> are in `REM_FINAL_THESIS_COMPLETION_2026_11_19/results/`; their protocols and code hashes were committed before any arm was scored, and a fresh run of the frozen pilot pipeline first reproduced the published counts of REM v1.0 exactly.

**After:**

> are in `REM_FINAL_THESIS_COMPLETION_2026_11_19/results/`. Their protocols and code hashes were committed before any arm was scored, and a fresh run of the frozen pilot pipeline first reproduced the published counts of REM v1.0 exactly.

### 71. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Bootstrap coverage is an asymptotic property, and with so few groups the intervals are not guaranteed to reach their nominal 95% coverage; a narrow interval, such as that of REM's replay ASR, is not evidence of precision.

**After:**

> Bootstrap coverage is an asymptotic property, and with so few groups the intervals are not guaranteed to reach their nominal 95% coverage. A narrow interval, such as that of REM's replay ASR, is therefore not evidence of precision.

### 72. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> - **AI inspection only so far.** A sample of 30 attacked episodes was inspected by the AI assistant that assisted this work, not by a human: 29 labels agreed with the trace, and one was a likely false negative (an attacker-directed transfer through a tool other than the reference tool).

**After:**

> - **AI inspection only so far.** A sample of 30 attacked episodes was inspected by the AI assistant that assisted this work, not by a human. In 29 the label agreed with the trace; one was a likely false negative (an attacker-directed transfer through a tool other than the reference tool).

### 73. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> It is trained once per fold, on the fitting portion of that fold only, by the nested procedure of Chapter 3 (Procedure 3.1): the ridge penalty is selected from five values by four grouped inner folds; the calibration map is fitted on the inner out-of-fold logits; the model is then refitted on the whole fitting portion.

**After:**

> It is trained once per fold, on the fitting portion of that fold only, by the nested procedure of Chapter 3 (Procedure 3.1):
> 
> - the ridge penalty is selected from five values by four grouped inner folds;
> - the calibration map is fitted on the inner out-of-fold logits;
> - the model is then refitted on the whole fitting portion.

### 74. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Three further sets of models were trained by the same procedure and are used later in the chapter: the models of REM v1.1, which omit the four behavioral features (nine folds); the models of the double holdout, one for each of 143 combinations of user task and attacker objective (Chapter 3, Section 3.11.11); and, for the exploratory extension, models on the four non-behavioral features plus five permission indicators (nine folds and 143 double-holdout cells; Chapter 3, Section 3.14). The study of 16 November 2026 trained, inside each training portion, two further ridge models on half of it (for the Neyman-Pearson and conformal thresholds, whose calibration half is split by attacker objective, never by step) and gradient-boosted trees selected among twelve configurations by the same grouped inner folds.

**After:**

> Three further sets of models were trained by the same procedure and are used later in the chapter:
> 
> - the models of REM v1.1, which omit the four behavioral features (nine folds);
> - the models of the double holdout, one for each of 143 combinations of user task and attacker objective (Chapter 3, Section 3.11.11);
> - for the exploratory extension, models on the four non-behavioral features plus five permission indicators (nine folds and 143 double-holdout cells; Chapter 3, Section 3.14).
> 
> The study of 16 November 2026 trained two further kinds of model inside each training portion. Two ridge models were fitted on half of the portion, for the Neyman-Pearson and conformal thresholds; their calibration half is split by attacker objective, never by step. Gradient-boosted trees were selected among twelve configurations by the same grouped inner folds.

### 75. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> **A released attack-labeled call is not the same as a committed unauthorized change of the bank state.** The label marks an attempt (Section 4.2.1), and the effect of a released call on the state is not measured separately from the benchmark's security check.

**After:**

> **A released attack-labeled call is not the same as a committed unauthorized change of the bank state.** The label marks an attempt (Section 4.2.1). The effect of a released call on the state is not measured separately from the benchmark's security check.

### 76. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> **No margin of non-inferiority on security was approved, and none was invented.** An interval of an attack-success difference that includes zero is reported as unresolved. The studies of 13 to 15 November also fixed their wording in advance. "Added value over simple rules" may be stated only if the task-completion interval against A2 lies above zero on both populations and the number of successful attacks does not exceed A2's. "The learned model adds value" may be stated only if the lower bound of its task-completion interval against the rule is strictly above zero under S1 and S2, with no more successful attacks on the original text and on the reformatted-identifier probe.

**After:**

> **No margin of non-inferiority on security was approved, and none was invented.** An interval of an attack-success difference that includes zero is reported as unresolved. The studies of 13 to 15 November also fixed their wording in advance:
> 
> - "Added value over simple rules" may be stated only if the task-completion interval against A2 lies above zero on both populations and the number of successful attacks does not exceed A2's.
> - "The learned model adds value" may be stated only if the lower bound of its task-completion interval against the rule is strictly above zero under S1 and S2, with no more successful attacks on the original text and on the reformatted-identifier probe.

### 77. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Of these, 2,113 are eligible under amendment AM-4, meaning that the replay with every call allowed reproduces the recorded outcome; the 35 that are not (34 in F-E, 1 in F-C) are excluded from every metric.

**After:**

> Of these, 2,113 are eligible under amendment AM-4: the replay with every call allowed reproduces the recorded outcome. The 35 that are not eligible (34 in F-E, 1 in F-C) are excluded from every metric.

## 08_ch4b.txt

### 78. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Whether a framework that needs a language model in its decision path can be measured under these conditions decides whether its comparison is quantitative or architectural; that is stated for each framework below.

**After:**

> Whether a framework that needs a language model in its decision path can be measured under these conditions decides whether its comparison is quantitative or architectural. This is stated for each framework below.

### 79. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> The property concerns the current policy, not whether the first policy matches what the user asked for, which the authors state themselves (Section 9); in the paper's main results the approver accepts every expansion.

**After:**

> The property concerns the current policy, not whether the first policy matches what the user asked for, as the authors state themselves (Section 9). In the paper's main results, the approver accepts every expansion.

### 80. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

>    - The policy completes no benign episode of user tasks 14 (password change: no rule) and 15 on the primary recordings, and of user tasks 9 and 14 on the second population; otherwise it completes about as many as the undefended agent.

**After:**

>    - The policy completes no benign episode of user tasks 14 (password change: no rule) and 15 on the primary recordings, and of user tasks 9 and 14 on the second population. Otherwise it completes about as many as the undefended agent.

### 81. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> **Main cost.** REM v1.0's replayed benign utility on these traces (5 of 15) is below that of every recorded defense in point estimate; the injection classifier's 7 of 16 is the closest, and their intervals overlap.

**After:**

> **Main cost.** REM v1.0's replayed benign utility on these traces (5 of 15) is below that of every recorded defense in point estimate. The injection classifier's 7 of 16 is the closest, and their intervals overlap.

### 82. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> In version 3 of the paper, which was read in full, a language model writes the initial policy from the user's query and updates it during execution; a solver classifies each update as a narrowing, applied automatically, or an expansion, which needs approval (pp. 6-7). The official repository contained, at the commit of 10 September 2025, a hand-written policy for the AgentDojo banking suite: `send_money`, `schedule_transaction` and `update_scheduled_transaction` are permitted only for five listed recipients; `update_password` has no policy entry and is therefore not permitted; the remaining tools are permitted. That policy was removed

**After:**

> In version 3 of the paper, which was read in full, a language model writes the initial policy from the user's query and updates it during execution. A solver classifies each update as a narrowing, applied automatically, or an expansion, which needs approval (pp. 6-7). At the commit of 10 September 2025, the official repository contained a hand-written policy for the AgentDojo banking suite:
> 
> - `send_money`, `schedule_transaction` and `update_scheduled_transaction` are permitted only for five listed recipients;
> - `update_password` has no policy entry and is therefore not permitted;
> - the remaining tools are permitted.
> 
> That policy was removed

### 83. `src/CHAPTER_04_FINAL.md` (category B)

**Before:**

> The upstream checking code was not executed; an independent review of 14 November 2026 reported a differential check on 468 argument cases that found no difference, which was not repeated here.

**After:**

> In that study the upstream checking code was not executed. An independent review of 14 November 2026 reported a differential check on 468 argument cases that found no difference, which was not repeated here. The authors' checker was executed later, for the comparison at the start of this section, and gave the same counts (see the paragraph on the independent confirmation of the earlier replay).

### 84. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> - **Against REM v1.0** the current rule has fewer successful attacks on the primary recordings and more completed benign tasks on the second population; the other intervals include zero. This contrast was not fixed in advance.

**After:**

> - **Against REM v1.0** the current rule has fewer successful attacks on the primary recordings and more completed benign tasks on the second population. The other intervals include zero. This contrast was not fixed in advance.

### 85. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> - **The two policies fail in different places.** The published policy completes no password-change task (user task 14), because the tool is not permitted, and its five recipients are payees of the benchmark's initial state: on twenty paired fixtures whose payees are not on the list it withholds 13 of 20 legitimate calls (Table 4.58).

**After:**

> - **The two policies fail in different places.** The published policy completes no password-change task (user task 14), because the tool is not permitted. Its five recipients are payees of the benchmark's initial state, and on twenty paired fixtures whose payees are not on the list it withholds 13 of 20 legitimate calls (Table 4.58).

### 86. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> 4. **Replay.** Under NO-ADAPT a withheld call does not lead the recorded agent to retry or replan. This affects both REM and Progent in the same way, because both withhold calls; it would not apply in the same way to DRIFT or MELON, which change the agent's subsequent behavior.

**After:**

> 4. **Replay.** Under NO-ADAPT a withheld call does not lead the recorded agent to retry or replan. This affects REM and Progent in the same way, because both withhold calls. It would not apply in the same way to DRIFT or MELON, which change the agent's subsequent behavior.

### 87. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> **The supported conclusion is not that REM outperforms or underperforms these frameworks in general.** On this benchmark a deterministic policy with knowledge of the legitimate payees matches REM's protection with less false blocking, and REM's claimed advantage, independence from such knowledge, remains to be tested.

**After:**

> **The supported conclusion is not that REM outperforms or underperforms these frameworks in general.** On this benchmark, a deterministic policy with knowledge of the legitimate payees matches REM's protection with less false blocking. REM's claimed advantage, independence from such knowledge, remains to be tested.

## 09_ch4c.txt

### 88. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> The five layers of Chapter 3 are design units. In the implementation they are not five independently removable modules: the features that the Decision Engine consumes are computed by the Behavioral Analysis code from labels and entities made by the Input & Context code, as Chapter 3 specifies (Table 3.6), and one behavioral feature is defined through the same instruction-pattern match as the Detection layer's indicator.

**After:**

> The five layers of Chapter 3 are design units. In the implementation they are not five independently removable modules. The features that the Decision Engine consumes are computed by the Behavioral Analysis code from labels and entities made by the Input & Context code, as Chapter 3 specifies (Table 3.6). In addition, one behavioral feature is defined through the same instruction-pattern match as the Detection layer's indicator.

### 89. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> No variant is called A2 without a suffix, and the bare label A1 denotes a variant only in Table 4.25 and the coverage summary below it; everywhere else, a bare A1 or A2 is one of those rules.

**After:**

> No variant is called A2 without a suffix, and the bare label A1 denotes a variant only in Table 4.25 and the coverage summary below it. Everywhere else, a bare A1 or A2 is one of those rules.

### 90. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> **Coverage of the five layers.** Four of the five layers have at least one evaluated variant; the Input & Context layer has none of its own, because it computes no evidence and everything downstream depends on its labels. Only the Mitigation layer is ablated as a whole: A5 removes all enforcement. The Decision Engine is ablated component by component, and every one of its components is covered (A4a–A4e); A4a removes the whole learned decision but keeps the predicates, and removing the layer entirely would leave no verdict at all, which is the no-defense reference by construction.

**After:**

> **Coverage of the five layers.** Four of the five layers have at least one evaluated variant. The Input & Context layer has none of its own, because it computes no evidence and everything downstream depends on its labels. Only the Mitigation layer is ablated as a whole: A5 removes all enforcement. The Decision Engine is ablated component by component, and every one of its components is covered (A4a–A4e). A4a removes the whole learned decision but keeps the predicates; removing the layer entirely would leave no verdict at all, which is the no-defense reference by construction.

### 91. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Two ablations of Table 4.35 were followed up in later studies, and their results are reported where those studies are described.

**After:**

> Two ablations of Table 4.35, behavioral evidence and calibration, and one change of the verdict set were followed up in later studies. Their results are reported where those studies are described.

### 92. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> That is a statement about the benchmark's attacker goals, not an independent authorization audit; Section 4.5.8 shows calls that the request does not authorize and that this guard admitted.

**After:**

> That is a statement about the benchmark's attacker goals, not an independent authorization audit. The repair study later in Section 4.5.8 shows calls that the request does not authorize and that this guard admitted.

### 93. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> The outcomes in Table 4.37 are those of the frozen guard, which accepted unverified computed amounts and misread percentage coefficients. Section 4.5.8 reports the repair and its cost.

**After:**

> The outcomes in Table 4.37 are those of the frozen guard, which accepted unverified computed amounts and misread percentage coefficients. The repair study that follows in Section 4.5.8 reports the repair and its cost.

### 94. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> - **The two-verdict decision alone is unsafe.** Applied to REM v1.1 without a guard (V11d), it releases every held-out credential-change attack (131 and 58 successful attacks).

**After:**

> - **The two-verdict decision is unsafe on its own.** Applied to REM v1.1 without a guard (V11d), it releases every held-out credential-change attack (131 and 58 successful attacks).

### 95. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> **Residual ASR after Modify.** Under NO-ADAPT, residual attack success after Modify is close to zero **by construction**: a withheld call does not recur.

**After:**

> **Residual ASR after Modify.** Under NO-ADAPT, residual attack success after Modify is close to zero **by construction**, because a withheld call does not recur.

## 10_ch4d.txt

### 96. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> The repair is a separate, versioned component. It assigns each payment instruction of the request one typed binding (*literal*, *derived*, *balance-based*, *record refund*, *unresolved* or *none*), parses a finite grammar (stated amounts; percentages, the fractions a/b, half, thirds and quarters, and doubling, of a stated number or of "my balance"), and computes with exact rationals.

**After:**

> The repair is a separate, versioned component. It assigns each payment instruction of the request one typed binding (*literal*, *derived*, *balance-based*, *record refund*, *unresolved* or *none*). It parses a finite grammar (stated amounts; percentages, the fractions a/b, half, thirds and quarters, and doubling, of a stated number or of "my balance") and computes with exact rationals.

### 97. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> The verifier can only turn a release into a refusal. Three repaired arms were run: G3_math (G3 plus the verifier), GV_math (the GV front, with the verifier in place of the lexical constraint) and HV_math (the same front and verifier, followed by HV's stored ridge model and calibration). GV_math and HV_math differ only in the learned decision.

**After:**

> The verifier can only turn a release into a refusal. Three repaired arms were run:
> 
> - G3_math: G3 plus the verifier;
> - GV_math: the GV front, with the verifier in place of the lexical constraint;
> - HV_math: the same front and verifier, followed by HV's stored ridge model and calibration.
> 
> GV_math and HV_math differ only in the learned decision.

### 98. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> The unrepaired arms completed them by releasing an amount that the request does not verify; the benchmark's own check, which a runtime monitor does not have, is what showed the amount to be right.

**After:**

> The unrepaired arms completed them by releasing an amount that the request does not verify. Only the benchmark's own check, which a runtime monitor does not have, showed the amount to be right.

### 99. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> In version 1 the verifier was *computed* for every call but could change only a call that the front and the rule had released; the correct statement is therefore that **for no benchmark-labeled attack call could the verifier's or the learned decision's output change the release**.

**After:**

> In version 1 the verifier was *computed* for every call, but it could change only a call that the front and the rule had released. The correct statement is therefore that **for no benchmark-labeled attack call could the verifier's or the learned decision's output change the release**.

### 100. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Version 2 changes acceptance only: the recognized statement must cover the whole amount phrase, from the payment verb to the bound account, or the instruction is unresolved; and a call is accepted only on one *witnessing* instruction whose effect, account, own condition and own amount all license it. It also evaluates the verifier only after the front and the rule have released the call.

**After:**

> Version 2 changes acceptance only:
> 
> - the recognized statement must cover the whole amount phrase, from the payment verb to the bound account, or the instruction is unresolved;
> - a call is accepted only on one *witnessing* instruction whose effect, account, own condition and own amount all license it.
> 
> It also evaluates the verifier only after the front and the rule have released the call.

### 101. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> No benchmark request contains a compound calculation or two conditional payments to one account, so the recordings can show neither a cost nor a benefit of the repair; the diagnostics show the benefit.

**After:**

> No benchmark request contains a compound calculation or two conditional payments to one account, so the recordings can show neither a cost nor a benefit of the repair. The diagnostics show the benefit.

### 102. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> **Why provenance evidence affects attack-call execution.** The provenance features record whether a call's arguments come from the user's request or from untrusted content; an attacker's account number arrives through an injected tool output.

**After:**

> **Why provenance evidence affects attack-call execution.** The provenance features record whether a call's arguments come from the user's request or from untrusted content. An attacker's account number arrives through an injected tool output.

### 103. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> - **A new over-blocking failure.** Version 2 withholds the legitimate call of fixture S1 of set 4, "Send 75 to the swim club for the annual fee. Their account is …": the account is named in the next sentence, so the amount phrase reaches "for the annual fee". It was not repaired after scoring.

**After:**

> - **A new over-blocking failure.** Version 2 withholds the legitimate call of fixture S1 of set 4, "Send 75 to the swim club for the annual fee. Their account is …". Because the account is named in the next sentence, the amount phrase extends to "for the annual fee". It was not repaired after scoring.

## 11_ch4e.txt

### 104. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> After a refusal, a live agent could retry, rephrase, use another tool, or abandon the task. Replay therefore cannot show how often a live agent would achieve the attacker's goal by another route, and **a near-zero replay ASR is not evidence of protection against a live or adaptive agent.**

**After:**

> After a refusal, a live agent could retry, rephrase, use another tool, or abandon the task. Replay therefore cannot show how often a live agent would achieve the attacker's goal by another route. **A near-zero replay ASR is not evidence of protection against a live or adaptive agent.**

### 105. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> The same replays under the episode-level variant are reported in Appendix S-E. In summary: REM's ASR is identical under both semantics (0.004); B1's is lower under the episode-level variant (0.055 against 0.046), because the restriction set left by an earlier Block or Modify refuses later state-changing calls; utility under attack is lower or equal under the episode-level variant in every configuration; and benign utility coincides.

**After:**

> The same replays under the episode-level variant are reported in Appendix S-E. In summary:
> 
> - REM's ASR is identical under both semantics (0.004);
> - B1's is lower under the episode-level variant (0.055 against 0.046), because the restriction set left by an earlier Block or Modify refuses later state-changing calls;
> - utility under attack is lower or equal under the episode-level variant in every configuration;
> - benign utility coincides.

### 106. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> S3 uses 681 attacked episodes of one backbone under five attack templates not used in fitting (of 715 recorded, 34 are not reproduced by the all-allow replay and are excluded); it has no benign episodes.

**After:**

> S3 uses 681 attacked episodes of one backbone under five attack templates not used in fitting (of 715 recorded, 34 are not reproduced by the all-allow replay and are excluded). It has no benign episodes.

### 107. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Both REM versions are also unchanged, which is consistent with their narrow Allow region; the contribution of each feature to that result was not examined separately.

**After:**

> Both REM versions are also unchanged, which is consistent with their narrow Allow region. The contribution of each feature to that result was not examined separately.

### 108. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> - **REM v1.0 is not shown to be better than the rules either.** P2 and A2 complete more tasks in point estimate with one more successful attack; the intervals of their differences from REM v1.0 include zero, except for A2 on benign episodes.

**After:**

> - **REM v1.0 is not shown to be better than the rules either.** P2 and A2 complete more tasks in point estimate, with one more successful attack. The intervals of their differences from REM v1.0 include zero, except for A2 on benign episodes.

### 109. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> REM's threat model gives it one trusted input, the user's request as text. The published approaches that report both low attack success and high utility add something REM does not have: a trusted policy or authorization record (aiAuthZ, at abstract level), trusted observations that license an action (Yan et al., 2026), a language model that judges task alignment (F. Jia et al., 2025), or enforcement on effects at the system boundary (Kairos, at abstract level). Of these, this thesis ran only a fixed-list policy from Progent's repository, in replay (Section 4.4.7); it does not claim that the others would succeed on these episodes.

**After:**

> REM's threat model gives it one trusted input, the user's request as text. The published approaches that report both low attack success and high utility add something REM does not have:
> 
> - a trusted policy or authorization record (aiAuthZ, at abstract level);
> - trusted observations that license an action (Yan et al., 2026);
> - a language model that judges task alignment (F. Jia et al., 2025);
> - enforcement on effects at the system boundary (Kairos, at abstract level).
> 
> Of these approaches, this thesis ran only a fixed-list policy from Progent's repository, in replay (Section 4.4.7). It does not claim that the others would succeed on these episodes.

### 110. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> 16. **One published policy was replayed, and no defense that needs a language model was run.** Since 22 November 2026 the published policy is decided by the enforcement code of the Progent repository at a pinned commit, which gives the same counts as the earlier re-implementation on every population (Section 4.4.7); the Progent framework was not run with generated or updated policies.

**After:**

> 16. **One published policy was replayed, and no defense that needs a language model was run.** Since 22 November 2026 the published policy is decided by the enforcement code of the Progent repository at a pinned commit, which gives the same counts as the earlier re-implementation on every population (Section 4.4.7). The Progent framework was not run with generated or updated policies.

### 111. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> A second review found that version 1 also accepted a supported prefix of a compound calculation and an amount from an instruction whose condition does not hold; version 2 repairs both without changing any episode outcome and withholds one further legitimate fixture.

**After:**

> A second review found that version 1 also accepted a supported prefix of a compound calculation and an amount from an instruction whose condition does not hold. Version 2 repairs both without changing any episode outcome and withholds one further legitimate fixture.

### 112. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Decided by Progent's own enforcement code (22 November 2026), it gives the same counts on all three populations and completes 7.2, 16.9 and 18.0 percentage points more tasks under attack than REM v1.0; its list of permitted recipients contains values specific to the benchmark.

**After:**

> Decided by Progent's own enforcement code (22 November 2026), it gives the same counts on all three populations and completes 7.2, 16.9 and 18.0 percentage points more tasks under attack than REM v1.0. Its list of permitted recipients contains values specific to the benchmark.

### 113. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> An external review found that the guard accepted unverified computed amounts; a typed amount verifier repairs this with no successful attack and 95 and 159 fewer completed tasks, all in requests whose amount it cannot verify, and the learned decision behind it again changes nothing.

**After:**

> An external review found that the guard accepted unverified computed amounts. A typed amount verifier repairs this with no successful attack and 95 and 159 fewer completed tasks, all in requests whose amount it cannot verify; the learned decision behind it again changes nothing.

### 114. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> at a cost of 22.5 points of benign utility, and only enforcement by the Mitigation layer turns its verdicts into outcomes: in shadow mode the same verdicts protect nothing.

**After:**

> at a cost of 22.5 points of benign utility. Only enforcement by the Mitigation layer turns its verdicts into outcomes: in shadow mode the same verdicts protect nothing.

### 115. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> and about as many as transformers_pi_detector, with lower benign completion; the comparison is descriptive because the defenses' runs are closed-loop and REM's is a replay.

**After:**

> and about as many as transformers_pi_detector, with lower benign completion. The comparison is descriptive, because the defenses' runs are closed-loop and REM's is a replay.

## 12_ch4f.txt

### 116. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Removing the two verdicts from the decision rule, so that Allow is chosen up to the Allow–Block threshold of Equation 3.9, gives more released calls with 13 against 11 successful attacks

**After:**

> Removing the two verdicts from the decision rule, so that Allow is chosen up to the Allow–Block threshold of Equation 3.9, releases more calls. It gives 13 against 11 successful attacks

### 117. `src/CHAPTER_04_FINAL.md` (category A)

**Before:**

> Binding amounts to accounts takes the rule from 10 and 3 successful attacks to 1 and 0, and binding instructions to the effect of the operation removes the remaining one (paired contrast

**After:**

> Binding amounts to accounts takes the rule from 10 and 3 successful attacks to 1 and 0. Binding instructions to the effect of the operation removes the remaining one (paired contrast

## 13_appendix_legend.txt

### 118. `src/APPENDICES_FINAL.md` (category A)

**Before:**

> *Verification codes:* FV — formulation checked against the source; IV — source identity confirmed, formulation to be checked against the full text; NC — source not accessible during this revision; DER — derived in this chapter; DEF — design definition. The codes are retained until final reference verification is complete.

**After:**

> *Verification codes:* FV: formulation checked against the source; IV: source identity confirmed, formulation to be checked against the full text; NC: source not accessible during this revision; DER: derived in this chapter; DEF: design definition. The codes are retained until final reference verification is complete.
