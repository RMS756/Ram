# 06: Research questions, methods, data and findings: alignment

## 1. Status of the research questions

| Source | Content | Status |
|---|---|---|
| Approved proposal | Objectives **O1–O3** (thesis Ch. 1 §1.6). No RQ wording | Approved |
| Thesis, all current editions | **RQ1–RQ4**, derived from O1–O3 (Ch. 1 §1.7; Ch. 3 S-3.1.3) | Author's derivation. Approval status of the RQ wording **not recorded** in the repository |
| Reconciliation `5d7828c` 02 §5, and this task's starting point | **RQ1–RQ5** | [PD]. **SUPERVISOR DECISION REQUIRED** (08, D2) |

**The working copy keeps RQ1–RQ4.** Restructuring to RQ1–RQ5 renumbers about 16 cross-references in five chapters (§4), and the supervisor has not approved it. The complete replacement text is in 07 §2, ready to apply.

## 2. Alignment of the proposed RQ1–RQ5 with the evidence

| RQ (proposed) | Evidence | Method | Result (stored, reconciled) | Conclusion that does not exceed the evidence | Data history / protocol status |
|---|---|---|---|---|---|
| **RQ1** Discrimination and calibration of the ridge estimator over provenance, context, behavioural and action evidence at the tool-call boundary | `results/pilot/e1_crossfit.json` (reproduced 27 Nov) | Nested grouped cross-fitting, 9 folds by attack objective; ROC-AUC, AP, ECE | ROC-AUC 0.938 [0.908, 0.961]; AP 0.719; ECE 0.044; credential-change fold ECE 0.189 | Separates recorded attack attempts from legitimate calls on held-out objectives; one provenance feature alone has recall 0.971 at FPR 0.147 | Development (P1); configuration committed before held-out predictions (not a formal pre-registration) |
| **RQ2** REM vs no defense, consequence-independent thresholds and deterministic rules; P1 only, vs withhold-all | Thesis Table 4.46; [A21]; `confirmatory_results.json`; DiD-3 raw (B1 vs F-GW) | Paired replay on identical episodes | P1: ASR 22.6% → 0.4%; B1 thresholds 5.5%; benign 52% → 31%. P3: rules ≈ REM in security, equal or higher completion (not resolved). P1: benign set identical to withhold-all | REM lowers replay attack success at a large cost in completion; it is not shown to beat simple rules | (a)–(b) development; (c) rules declared in the 11 Nov protocol; (d) **exploratory re-analysis, P1 only** |
| **RQ3** Component-level ablation of REM v1.0 | [A19] `dc8407d` (P1); [A21] `93e6630` (P1–P3) | Protocol-frozen paired ablation; grouped bootstrap (Field & Welsh, 2007); exact McNemar (unclustered) | Enforcement and pathway necessary; action evidence −9.12 pp [−23.45, −0.74] on P3; context and predicates null; calibration null on attacks | 05 A–B. The estimator is not isolated; Input & Context not removable on its own | **Protocol-frozen** (commits precede scoring) on **data examined during development**. Not called "pre-registered" |
| **RQ4** Test-time evidence suppression (exploratory, idealized) | DiD-2 (`2547854`; post-hoc arms `e3e7488`) | Label-conditioned suppression in replay | Behavioural 131; action 90; both 669; v1.1 + action suppression 653 | Removal and suppression can disagree; suppression is not an adaptive attacker | **Exploratory**; post-hoc arms marked; P1 and the reformatting population |
| **RQ5** Effect of removing behavioural evidence on task completion and replay attack outcomes, on recordings unread before the run | Confirmatory run of 11 Nov (P3, 2,113 episodes); thesis §4.6.8 | Pre-declared decision rule; paired grouped bootstrap | Completion +7.5 pp [1.2, 16.0]; attacks 1 vs 3 of 2,065 | The completion gain met the pre-declared rule. **The security difference is not resolved; this is neither non-inferiority nor equivalence.** RQ4 shows a loss of coverage under suppression | **Confirmatory by design.** The protocol's freeze commit is **not in this repository's history** (reconciliation 02 §5), so the order of protocol and data opening rests on the thesis's own record. Not called pre-registered |

**Original RQ3** ("residual attack success after the Modify mechanism"): cannot be answered by replay, because a withheld call does not recur, so residual success is near zero by construction. The reconciliation removes it from the RQs. Its answerable parts (per-call time; the equivalence of Modify, Escalate and Block without a reviewer) move to RQ2 and RQ3.

**Every proposed RQ has evidence, a method and a result.** RQ4 and RQ2(d) are exploratory and must be labelled so wherever they are answered.

## 3. Methodology checks applied in the working copy

| Check | Result |
|---|---|
| "Pre-registered" used for protocols that were only committed before scoring | **15 occurrences replaced** (`T1`–`T10`, `C5-1`, `C5-5`, `C5-8`, `R1-6b`, `R4-8`); 0 remain |
| Repeated runs of the same task pairing described as independent observations | Not found in the edited text. The bootstrap is grouped by injection task and user task, as stated in Ch. 4 §4.3.4 |
| Replay described as live deployment | No. The gateway text (`A3`, `A3-ch4`) states simulation on recorded traffic |
| RQ5 described as security non-inferiority or equivalence | No. Ch. 1 item 4 and Ch. 5 already say "not resolved statistically" |
| Withhold-all reference described as useful completion | No. `R4-5` and `R1-6a` say it completes no state-changing task |

## 4. Cross-references to change if RQ1–RQ5 is approved

Locations in the working copy (`thesis_working_copy/src`):

| File | Lines | Content |
|---|---|---|
| Ch. 1 | 108–111 | RQ list |
| Ch. 1 | 113 | "bear on RQ2 and RQ4" |
| Ch. 2 | 43, 45, 51 | "RQ1–RQ4", SRQ mapping |
| Ch. 3 | 16 | "research questions RQ1–RQ4" |
| Ch. 3 | 664 | "primary comparator for RQ2" |
| Ch. 4 | 1582, 1619, 1657 | Headings 4.6.1–4.6.3 |
| Ch. 4 | 1730 | "RQ3 quantities" |
| Ch. 5 | 19–22 | RQ answer table: add an RQ5 row; split RQ4 into RQ3 and RQ4 |

The mapping is in 07 §2.
