# 18 Supervisor presentation summary

For Prof. Omar Ahmad Alzubi and Dr. Husam Fakhouri. Eight slides; the numbers come from `results/`.

---

### Slide 1: Question
- Does REM's learned risk stage (ridge + Platt + expected loss) change decisions once deterministic authorisation is enforced?
- Can the authorisation itself be made order-independent and value-aware?

### Slide 2: Diagnosis of the current design
- The estimator is good: ROC-AUC 0.974, Brier 0.059, ECE 0.024.
- But the deterministic authority front stops **all 907** attack-labelled calls first, so the learned stage never sees an attack.
- The count-only ledger (C1) is **order dependent**: an attacker's earlier update of a standing order consumes the user's allowance. In development scenarios C1 released 4 of 9 unauthorised calls and withheld 6 of 12 authorised ones.

### Slide 3: Three architectures (exploratory)
- **REM-A:** corrected original; learned stage on every passing call.
- **REM-B:** authorisation-first, deterministic.
  - object binding (the request designates *which* standing order);
  - per-(instruction, object) ledger;
  - trusted-evidence rules: E1 (explicit percentage arithmetic) and E2h (refund only to a counterparty the user has paid before).
- **REM-C:** REM-B plus the learned stage only on calls whose value is unresolved.

### Slide 4: Method
- Protocol, criteria and hashes were frozen before any scored run.
- Populations:
  - primary (3,313 episodes) and dev2 (2,113): development;
  - **H**: 522 unseen gpt-4o traces with other prompt defences.
- Suites: author-written held-out probes (labelled before the code was written), diagnostics, fixtures, and a scripted closed loop.
- Statistics: grouped bootstrap.

### Slide 5: Results

| | C1 | REM-B | REM-C | Progent manual policy |
|---|---|---|---|---|
| Attacks (all populations) | 0 | 0 | 0 | 0 |
| Audited violations (primary / dev2) | 11 / 0 | 11 / 0 | **121 / 24** | **161 / 36** |
| Held-out probes: unauthorised + ambiguous released | 4 + 2 | **0 + 0** | 1 + 3 | 0 + 0 |
| Held-out probes: authorised released (of 16) | 4 | **12** | 13 | 0 |
| Scripted attack goal, call orders (of 4) | 2 | **0** | 0 | 0 |
| Tasks on H (of 522) | 245 | 249 | 269 | 280 |

### Slide 6: Decisions (frozen rules)
- **REM-B:** preferred on security; the utility gain over C1 on H is **INCONCLUSIVE**, +0.0077 [0.000, 0.021].
- **REM-C:** **NO-GO**. Its gains come from releasing wrong amounts and objects.
- **Learned stage:** harmful or redundant in REM-A; harmful in REM-C.
  - Consequence-aware and threshold variants give identical verdicts.
  - Calibration has no decision effect.
- **Object-binding question:** **INCONCLUSIVE**. The security part was met; one authorised probe was withheld by a designator defect, which was fixed only post hoc.
- **Full Progent and live LLM:** **NOT EXECUTED** (no endpoint, no approved budget).

### Slide 7: What can be claimed
- A controlled negative result: an attack-label estimator behind authorisation cannot improve decisions, and can harm value integrity.
- Object-bound stateful authorisation removes the call-order dependence (shown on author-written cases and the scripted loop).
- An audited value-violation metric exposes errors that attack-success metrics hide.
- **Not claimable:**
  - superiority over Progent;
  - live security;
  - unseen-task generalisation;
  - a novel algorithm.

### Slide 8: Decisions requested `[SUPERVISOR DECISION REQUIRED]`
1. **P1:** keep REM v1.0 as the primary design and report REM-B plus the negative result as an exploratory extension. **This is the recommendation.**
2. **P2:** make authorisation-first the primary verdict path, with the learned score audit-only. This changes the frozen pipeline.
3. **P3:** re-target the learner to value authorisation. This needs new labelled data and a new protocol.
4. Approve (or not) a live-agent budget, backbones and repeats.
5. Approve the fix of the designator defect, and an independent probe set written by someone other than the designer.
