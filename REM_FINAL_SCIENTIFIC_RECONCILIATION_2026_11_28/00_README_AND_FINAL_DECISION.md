# REM final scientific reconciliation (28 November 2026)

**Purpose.** Reconcile the conclusions of the independent audit (`REM_INDEPENDENT_AUDIT_2026_11_27/`) with the stored experimental evidence, so that one internally consistent scientific position goes to the supervisor and into the thesis revision.

**What was not done:**
- no experiment run;
- no artifact, result, protocol, earlier audit or thesis file changed;
- no new algorithm, version, decision engine or dataset;
- no comparative result introduced.

**What was done:**
- Every number used was read from stored result files, or from the per-episode recomputation made on 27 Nov.
- New reads on 28 Nov:
  - `REM_ABLATION_STUDY/02_IMPLEMENTATION_AUDIT.md` and `01_ABLATION_PROTOCOL.md`: dependencies, arm definitions, data history;
  - `REM_FINAL_THESIS_COMPLETION_2026_11_19/03_ABLATION_RESULTS.csv` and its protocol: calibration and threshold arms;
  - `REM_DEFENSE_IN_DEPTH/05_DID_RESULTS.md` and `results/did2_results.json`: suppression arms, counts checked against the JSON;
  - line-level diffs of the three thesis editions.

## Files

| File | Content |
|---|---|
| `01_RECONCILIATION_OF_FINDINGS.md` | Items 1–6:<br>component-by-component evidence with metrics kept apart;<br>ablation scope;<br>utility floor (P1 only);<br>literature gap;<br>methodology wording;<br>RQ basis;<br>list of superseded 27 Nov audit statements |
| `02_CORRECTED_SCIENTIFIC_POSITION.md` | The twelve required elements: problem, gap, aim, objectives, RQ1–RQ5, primary contribution, secondary contributions, novelty statement, exact REM v1.0 architecture, evidence map, limitations, ten examiner questions |
| `03_THESIS_ALIGNMENT_AND_EDITION_MERGE.md` | Title discrepancy; humanized vs DiD edition differences; recommended base and merge plan; Chapter 5 consequential edits |
| `04_PROPOSED_REPLACEMENT_PARAGRAPHS.md` | Exact replacement and insertion text:<br>Chapter 1: R1-1 to R1-6;<br>Chapter 4: R4-1 to R4-9<br>Each with its section and line location in the humanized sources |

## The reconciled position in brief

**Primary contribution (examined, not assumed).** Does REM v1.0's five-layer layering produce defense in depth? On replayed AgentDojo banking traces: **only narrowly.**
- **Necessary components:**
  - enforcement;
  - the combined learned pathway (estimator, calibration and expected loss, removed together).
- **The pathway acts on two evidence families that cover different attack classes:**
  - **Action/provenance evidence:** a measurable call-level effect on P3 (−9.12 pp [−23.45, −0.74]); outcome effects unresolved.
  - **Behavioural evidence:** removal costs no measured security, but test-time suppression (exploratory) lets the credential-change objective through.
- **No measurable effect:** context detection and the predicates.
- **Low specificity:** on P1, benign completion equals that of withholding every state-changing call. This is established on **P1 only**.

**Secondary contributions (qualified):**
- simple rules match the learned decision's replay security;
- replay-evaluation observations;
- the confirmed utility effect of removing behavioural evidence. This is **not** a recommendation to adopt it.

**Novelty.**
- No mechanism or architectural novelty is claimed. Substantial prior-art overlap exists: NEXUS (peer reviewed), Spotlight-Guard (peer reviewed), AIS (peer reviewed), Agent-Sentry, Progent, ROPE, AGATE.
- The empirical evaluation gap is retained only with its reading-level qualification.

**Methodology wording.**
- "Protocol-frozen paired ablation", on data examined during development.
- "Confirmatory" applies only to the 11 Nov run.

## Final decision

| Decision | Outcome | Basis |
|---|---|---|
| Evaluated research artifact | **REM v1.0, unchanged.** Trees: `rem/` `cd11e32…`, `experiments/pilot/` `b05d33a…`. Config sha256 `8e1aa107…` | Only fully evaluated and reproduced configuration. No existing evidence compels a change (02 §9) |
| REM v1.1 | Reported as a confirmed utility result; not adopted | Security effect unresolved; exploratory loss of coverage under suppression |
| REM-DiD, REM-X | Not part of the artifact. REM-DiD stays as a labelled exploratory section; REM-X as future work at most | Oracle authorization; design only |
| Research questions | RQ1–RQ5 of 02 §5 [PD]. Withhold-everything comparison limited to P1 | Each has an existing experiment and metric |
| Additional analysis | **None required.** Extending the withhold-everything comparison to P2/P3 needs one offline replay arm, **not run** | Instruction; 01 §6 |
| Thesis title | **[SUPERVISOR DECISION REQUIRED]**: printed "Runtime Evaluation and Mitigation (REM): A Security Framework for Financial AI Agents" vs stated topic "Defense in Depth for Financial AI Agents Against Indirect Prompt Injection". Title not changed | 03 §1 |
| Base edition | **Humanized edition**, merged with the DiD edition's five insertions (two sentences qualified). No overlapping edits | 03 §2–3 |
| Comparative claims | None of superiority or inferiority against MELON, Progent, ROPE, DRIFT or others | No controlled comparison exists |

## Supervisor decisions still required

1. Official title wording.
2. Adoption of RQ1–RQ5 (they replace the [PD] RQ1–RQ4).
3. Base-edition choice and merge.
4. REM v1.1 adoption (unchanged status).
5. Approval of the exploratory design values (unchanged status).
