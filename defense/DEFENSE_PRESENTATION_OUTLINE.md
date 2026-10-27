# Defense Presentation Outline (draft, ~20 minutes, 16 slides)

Status: DRAFT. Results slides present the EXPLORATORY pilot. The confirmatory evaluation is pending supervisor decisions.

| # | Slide | Content | Source |
|---|---|---|---|
| 1 | Title | Provisional title; candidate, supervisor, reviewer; department | Front matter |
| 2 | Problem | Tool-using financial agents can be steered by injected content into transfers, payee changes and credential changes | Ch. 1.1–1.2 |
| 3 | Gap | No reviewed system combines a calibrated per-step probability, consequence tiers and four-verdict expected-loss selection at the tool boundary, evaluated against a same-estimator baseline | Ch. 2; novelty audit |
| 4 | Objectives and RQs | O1–O3 (approved); RQ1–RQ4 marked [PD] | Ch. 1.6–1.7; Ch. 3.1 |
| 5 | Architecture | Five layers, no sixth; runtime pipeline diagram; offline fitting is cross-cutting | Ch. 3.2 |
| 6 | Decision rule | R(v) = (1−p)L(v,0,k) + pL(v,1,k); Table 3.13; Eq. 3.9 thresholds; feasible set; predicates | Ch. 3.7 |
| 7 | What is *not* new | Table 3.16: Cox, le Cessie, Platt, Elkan, Chow, Lundberg, Page | Ch. 3.13 |
| 8 | Implementation | Placement inside AgentDojo's tool executor (AS-1); fail-closed configuration; 192 tests | Ch. 4 |
| 9 | Pilot design | 21 real-agent backbones, 3,334 episodes, 6,762 steps; pre-registration; grouped cross-fitting; grouped bootstrap | Ch. 5.2 |
| 10 | RQ1 | ROC-AUC 0.94 on unseen attacker objectives; cross-template and leave-one-backbone-out; reliability figure; calibration adds nothing; fold 7 under shift | Ch. 5.4; Fig. 5.1 |
| 11 | RQ2 observe-only | Verdict profile REM vs B1; escalations; 33/180 vs 132/180 benign state-changing releases | Ch. 5.5 |
| 12 | RQ2/RQ3 replay | ASR and utility with intervals, labelled [REPLAY — SC-7]; the reviewer bounds | Ch. 5.6; Fig. 5.2 |
| 13 | RQ4 ablations | Action evidence dominates; context makes no difference; behavioural costs utility; tiers drive the trade-off | Ch. 5.7 |
| 14 | Validity | NO-ADAPT; SC-7; labels; user_task_15 version effect; one run per configuration; single benchmark | Ch. 5.9; validity report |
| 15 | Contributions and limits | Composition, evaluation protocol, measured trade-off; explicitly not claimed: new method, prevention guarantee, adaptive robustness | Ch. 6.4–6.5 |
| 16 | Decisions and next steps | SC-1 to SC-7, SD-FREEZE, reviewer model; live runs | Ch. 6.6; decisions register |

Backup slides:
- per-fold table (5.4);
- E6 grid;
- A2 CUSUM;
- distributed defenses (recorded);
- equation provenance table;
- reproduction command.
