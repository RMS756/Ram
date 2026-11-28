## 2. Not applied: text that needs a supervisor decision first

### 2.1 Research questions RQ1–RQ5 [SUPERVISOR DECISION REQUIRED] (08, D2)

**Location:** Ch. 1 §1.7, the bullets RQ1–RQ4 and the paragraph after them that begins "No research question was added after the pilot." The source is reconciliation 04, R1-4. RQ5 is worded so that it does not imply non-inferiority.

**Replace the four bullets with:**

> - **RQ1 (estimation).** How well does a ridge logistic regression estimator, using provenance, context, behavioral and action evidence at the tool-call boundary, discriminate attack-induced proposed calls when whole attack objectives are held out, and how well calibrated are its probabilities under grouped cross-fitting? *Evidence:* offline classification of recorded calls (development data).
> - **RQ2 (protection and cost).** In recorded-trace replay, how do REM v1.0's attack outcomes, benign task completion and task completion under attack compare with no defense, with a consequence-independent threshold policy on the same estimator, and with simple deterministic rules; and, on the primary population, with withholding every state-changing call? *Evidence:* replay on three populations; rule baselines declared in the protocol of 11 November 2026; a re-analysis on the primary population only.
> - **RQ3 (layering and depth).** Which components of REM v1.0's layered architecture are necessary for its replay protection, and which add only cost, under protocol-frozen paired component-level ablation? *Evidence:* two protocol-frozen ablations on three populations of recordings that had been examined before.
> - **RQ4 (removal versus suppression; exploratory).** Does REM v1.0's protection persist when one evidence family is suppressed at test time rather than removed, and do the two kinds of test agree? *Evidence:* modelled suppression in replay on the primary population.
> - **RQ5 (confirmatory).** Does removing the behavioral evidence group change task completion and replay attack outcomes on recordings that had not been read before the run? *Evidence:* the confirmatory replay of 11 November 2026, with a decision rule declared before the data were opened. The security difference is reported as an interval; it is not a test of non-inferiority or equivalence.

**Replace the paragraph that follows with:**

> RQ1 and RQ2 (first three comparisons) correspond to the original RQ1 and RQ2. The original RQ3 on mitigation is answered in part under RQ2 (per-call processing time) and RQ3 (the equivalence of Modify, Escalate and Block without a reviewer). Residual attack success against an adapting agent cannot be answered with replay and is not posed. RQ3 and RQ4 refine the original RQ4. RQ5 states the question of the confirmatory evaluation reported in Chapter 4, Section 4.6.8. RQ2 (the withhold-everything comparison), RQ3 and RQ4 were posed after the pilot. The analyses that answer them were run under protocols committed before their arms were scored, on data examined during development, and are reported as such.

**Consequential renumbering:** 06 §4 lists the locations.

| Old | New |
|---|---|
| Ch. 4 §4.6.1 "RQ1" | Unchanged |
| §4.6.2 "RQ2" | Unchanged |
| §4.6.3 "RQ2 and RQ3" | "RQ2" |
| "RQ3 quantities" (Ch. 4 §4.6.3) | "Quantities of the original RQ3 (per-call time; verdict equivalence)" |

Chapter 5 table: the RQ4 row splits into RQ3 (ablation: the C5-3 wording) and RQ4 (suppression: the DiD §4.6.12 result); a new RQ5 row takes the confirmatory result now in the RQ4 row ("the gain in task completion … met the pre-declared decision rule …; the security difference is not resolved").

### 2.2 Title [SUPERVISOR DECISION REQUIRED] (08, D1)

**No text is proposed.** The printed title stays: "Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents". The researcher's stated topic is "Defense in Depth for Financial AI Agents Against Indirect Prompt Injection". The working copy's content is valid under either wording (05 A). The title is in the build scripts (`TITLE` in `build_wc.py`) and in the front matter's committee page.

### 2.3 Kull wording [after source check] (08, D7)

**Location:** Ch. 3 §3.7.2, property 2: "Kull et al. (2017) prove that beta calibration with equal shape parameters equals logistic calibration applied to the log-odds of a score."

If the AISTATS paper states the identity without a proof, replace "prove" with "show". Not applied, because the full text was not read.

### 2.4 Holm citation [after source check] (08, D9)

**Location:** the DiD-inserted §3.15 ("Clustered sign-flip permutation tests with Holm correction") and §4.6.12. Add "(Holm, 1979)" and its reference entry once the JSTOR record is verified. Not applied.
