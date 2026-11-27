# A1-11: Mathematical traceability audit of the REM-X documents

**Instruction (researcher, 27 Nov 2026).** No new equations, formulas, scoring functions, probability models, thresholds or statistical expressions may be invented. Existing REM v1.0 equations are used only as documented. Any other mathematics must come from a verifiable published source. New requirements are stated in words.

**Scope.** `REM_X_DESIGN/00`–`10` (commit `1e7dadb`) and this amendment package.

**Rule for the originals.**
- The original files are **not edited**; they are the committed historical record.
- Every item below is flagged, and **this audit supersedes the flagged wording**.
- When REM-X documents are next consolidated, flagged items must be replaced as shown.

## 1. Legitimate existing mathematics (kept, unchanged)

| Item | Where | Source |
|---|---|---|
| Ridge logistic estimate, Platt calibration on the logit, consequence tier, expected-loss verdict | `REM_X_DESIGN/05`, `06`, `09` (named, not restated) | REM v1.0 frozen pipeline (CLAUDE.md MATHEMATICAL LOCK; thesis). Used as documented; nothing added |

## 2. Reported numbers (kept: results, not equations)

These are measured outcomes or test statistics already produced in REM v1.0, REM-DiD and DiD-3, quoted with their source files:
- attack and benign-task counts;
- p-values (for example raw p = 0.014, Holm p = 0.12);
- Jaccard values 0.84–0.99;
- the exact-test floor 2/512.

They are **not new mathematics**. One caveat: Holm, the sign-flip test and Jaccard were **used** in REM-DiD. A1-07 §7 lists their references, and flags the Holm record and the sign-flip test as still needing verified citations.

## 3. Items I introduced without a traceable source: flagged

| # | Location | Introduced item | Problem | Replacement wording / action |
|---|---|---|---|---|
| M1 | `REM_X_DESIGN/04`, I-4.3 | "sum(committed) + sum(reserved) ≤ limit at every point" | An engineering constraint written as a formula | **Replace with words:** "At no time may the value already committed plus the value currently reserved exceed the limit the user declared, including when calls are interleaved." Cite the reservation pattern from an established transaction-processing reference [REFERENCE NEEDED]. Not a contribution |
| M2 | `REM_X_DESIGN/04`, I-3.1 | "signal-correlation audit (phi < 1 with every L2 signal)" | A threshold on a correlation coefficient that I chose | **Remove.** State the requirement in words: "Behavioral rules must not read content text. Whether any behavioral signal duplicates a detection signal is checked by inspecting their inputs." Any statistical duplication criterion needs an established reference or a researcher decision |
| M3 | `REM_X_DESIGN/04`, I-C.2 and §2 header; `REM_X_DESIGN/08` §5.1–5.2 | "covered by ≥ 2 controls with different inputs" | A numeric design threshold I introduced | **Replace with:** "No threat class should depend on a single control, or on controls that read the same input." The required number is a **supervisor decision** |
| M4 | `REM_X_DESIGN/08` §4 | "P(both miss) vs P(i misses) × P(j misses) … a ratio well above 1 indicates correlated failure" | An independence criterion and a probability expression I introduced | **Withdraw.** Report the observed counts of calls missed by each control and by each pair, without any derived independence statistic, unless one is taken from a cited source and approved |
| M5 | `REM_X_DESIGN/08` §4–5 | "Resilience (strict): attack increase = 0 for single evasion" | A pass criterion I introduced. (The DiD-3 protocol used the same criterion; that frozen protocol is not changed here) | **Replace with words:** "Report the change in successful attacks when one control is evaded. Whether any change is acceptable is a researcher decision recorded before the run" |
| M6 | `REM_X_DESIGN/07` §6 | "Advantage claimed only if the 95% CI of the paired difference excludes 0 in the predeclared direction after Holm correction" | A decision rule and confidence level I chose | **Withdraw** (A1-07 §7). The confidence level, family, sidedness and decision rule are researcher decisions |
| M7 | `REM_X_DESIGN/07` §8 | "grouped bootstrap 95% CIs" | Confidence level chosen by me | As M6; the method is cited (Field & Welsh, 2007), the level is a decision |
| M8 | `REM_X_DESIGN/02` §2, `Permit` | "budget = 1" | An engineering parameter (single use), written as an equation | **Replace with words:** "valid for one use". Single-use authority is adopted from AIS (A); not a contribution |
| M9 | `REM_X_DESIGN/01` §3 D1 (c); `REM_X_DESIGN/04` I-1.4 | "call-linked evidence = false" as an **admission condition** | A logical condition that is also **unsafe** (A1-04) | **Withdraw.** Detector evidence can only escalate |
| M10 | `REM_X_DESIGN/01` §3 D2 | "exactly one committed reservation and one permit … observed effect equals the approved terms" | An engineering invariant; acceptable in words, but must not be presented as a formal result | **Keep as descriptive engineering invariant**, labelled [X-P] and [PA] (AIS) |
| M11 | `REM_X_DESIGN/02` §2, FAR | "max per call, per recipient, per session" | Kinds of limit (descriptive), no values | **Keep as descriptive.** All values [DESIGN BLOCKED] |
| M12 | `REM_X_DESIGN/08` §3 | Arm counts ("36 arms", "15 pairs") | Simple counts of a declared design, not a model | Keep as counts. Their use depends on M3–M5 being redecided |

**Not found:** no new risk-scoring formula, weighting scheme, optimization function or probability model was introduced elsewhere in `REM_X_DESIGN/00`–`10` (scan of all files for comparison and arithmetic notation).

## 4. This amendment package

- A1-01 to A1-10 were written after the instruction, in words only.
- The only formulas named are established, cited methods in A1-07 §7, and their parameters are left to decision.
- The five outcomes O1–O5 (A1-04) are **descriptive categories decided by which evidence is present**. They are not a scoring rule.

## 5. Outside this audit

**REM-DiD documents and code were not audited here** (they are not to be modified). They may contain criteria of the same kind as M3–M5, for example the DiD-3 strict-resilience criterion. Auditing them is listed as an open item for the researcher (A1-09 §4).
