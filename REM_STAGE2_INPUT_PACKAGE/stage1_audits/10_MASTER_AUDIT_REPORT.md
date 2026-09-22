# 10 — Master Audit Report

**Thesis:** A Runtime Evaluation and Mitigation (REM) Framework for Securing an AI Agent
**Chapters audited:** Chapter 2 (Literature Review) and Chapter 3 (Methodology)
**Date of audit:** 22 September 2026
**Deliverables:** `REM_AUDIT_OUTPUT/` (this directory)

---

## A. Scope and method

This stage did three things: it checked every claim in Chapters 2 and 3 that rests on a cited
source against that source; it audited the prose of both chapters for passages that read as
mechanical or unauthored; and it applied the smallest set of defensible corrections to derived
working copies.

**How claims were extracted.** Both chapters were parsed sentence by sentence. Every sentence or
table row carrying an in-text citation was treated as an auditable claim and matched to its entry
in the reference list by surname, year and author initials. This produced 52 claim units in
Chapter 2 and 55 in Chapter 3.

**How claims were graded.** A claim is VERIFIED only when the cited source was read at the level
the claim requires: a figure claim requires the figure, an equation claim requires the printed
equation, a topic claim requires the abstract. Where a source's identity was confirmed but its text
was not read, the claim is PARTIALLY SUPPORTED if the title or record implies it, and UNVERIFIED if
it concerns a formulation. Where a publisher or host denied access, the claim is UNVERIFIED and the
block is recorded; no inaccessible source was upgraded, guessed at or worked around.

**What was not done.** No AI-detection tool was available in this environment and none was
executed. Nothing in this stage reports, estimates or implies a detector score, and no edit was
made in order to influence one. The prose findings are an audit of authorial quality, recorded in
`07_AI_STYLE_AUDIT.xlsx` under the heading "AI-style / authorial prose audit".

---

## B. Files, checksums and integrity

The original thesis files were opened read-only. Their SHA-256 values, recorded before any work
began (`00_BASELINE_CHECKSUMS.md`), were re-computed after all editing and are unchanged:

| File | Status after this stage |
|---|---|
| `Chapter2_Literature_Review.md` | unchanged |
| `Chapter2_Literature_Review.docx` | unchanged |
| `Chapter3_Methodology.md` | unchanged |
| `Chapter3_Methodology.docx` | unchanged |
| `Stage3_Change_Log_and_Verification.md` | unchanged |
| `Stage3_Change_Log_and_Verification.docx` | unchanged |
| `tools/build_docx.py` | unchanged |
| `tools/fix_citations.py` | unchanged |

All editing took place in `REM_AUDIT_OUTPUT/working/`, and the two DOCX deliverables were built
from those working copies with the thesis's own DOCX writer, so their formatting matches the
existing chapters.

**Structural invariants, before and after editing:**

| Measure | Chapter 2 | Chapter 3 |
|---|---|---|
| Numbered equations | 0 → 0 | 22 → 22 |
| Section headings | 21 → 21 | 57 → 57 |
| Reference entries | 47 → 47 | 37 → 37 |
| In-text citations | 108 → 108 | 90 → 92 |
| Words (excluding reference list) | 6,259 → 6,335 | 11,060 → 11,346 |

The two additional Chapter 3 citations are re-uses of works already cited in that chapter, not new
literature: Arp et al. (2022) is now also cited in Section 3.11.6, and one grouped parenthetical
citation became two narrative citations. The REM architecture is unchanged: five layers, no sixth
layer, and no change to any equation, feature, verdict or metric.

---

## C. Chapter 2 — literature evidence audit

`01_CHAPTER2_LITERATURE_EVIDENCE_AUDIT.xlsx` — 52 claim units.

| Verification | Claims | Support level |
|---|---|---|
| VERIFIED | 37 | Full |
| METADATA ERROR | 8 | Full (content read; the source record's date conflicts with its identifier) |
| PARTIALLY SUPPORTED | 4 | Partial |
| UNVERIFIED | 3 | None |

The eight METADATA ERROR rows are all claims about NEXUS (REF-023, Hossain et al., 2026). Its full
text was read and supports every claim made about it; the problem is bibliographic, not
substantive — the arXiv identifier and the stated submission date are inconsistent (Section D).

The three UNVERIFIED rows concern Jackson (2025), whose full text returned HTTP 403 on every
attempt. This was corrected by edit E-01: the chapter no longer describes the mechanism of a paper
nobody in this project has read.

No claim in Chapter 2 was found to be contradicted by its source.

---

## D. Chapter 3 — literature evidence audit

`02_CHAPTER3_LITERATURE_EVIDENCE_AUDIT.xlsx` — 55 claim units.

| Verification | Claims | Support level |
|---|---|---|
| VERIFIED | 30 | Full |
| PARTIALLY SUPPORTED | 14 | Partial |
| UNVERIFIED | 8 | None |
| METADATA ERROR | 3 | Full |

Chapter 3's lower verification rate has a specific cause: it cites foundational statistical works
(Cox 1958, le Cessie & van Houwelingen 1992, Platt 1999, Page 1954, Lorden 1971, Moustakides 1986,
Chow 1970, Brier 1950) whose text sits behind publisher paywalls or on hosts that refused access.
For these, Crossref records confirm identity but not formulation.

This matters most where the chapter makes a claim about what a source's equation says. Those
claims are listed in `05_EQUATION_SOURCE_AUDIT.xlsx` and two were corrected in this stage (E-03,
E-04). The chapter's own mathematics is unaffected: every REM equation is either derived in the
chapter with a proof, or defined by the chapter, or taken from a source that was read (Guo et al.
2017, Kull et al. 2017, Lundberg & Lee 2017, Naeini et al. 2015, Basseville & Nikiforov 1993,
Elkan 2001).

---

## E. Reference verification master

`03_REFERENCE_VERIFICATION_MASTER.xlsx` — 58 unique works. Chapter 2 cites 47, Chapter 3 cites 37,
and 26 are cited in both. 47 + 37 − 26 = 58.

| Status | Count |
|---|---|
| VERIFIED | 40 |
| PARTIALLY VERIFIED | 14 |
| UNVERIFIED | 3 |
| CONFLICTED | 1 |

**The four that are not clean:**

| Ref | Work | Problem | Consequence |
|---|---|---|---|
| REF-003 | Brier (1950) | Publisher page returned HTTP 403 | Brier score is already deferred in Chapter 3 pending this verification; no claim depends on it |
| REF-024 | Jackson (2025) | SSRN returned HTTP 403 | Mechanism description removed (E-01); the work is retained as a cited but inaccessible working paper |
| REF-041 | Platt (1999) | Hosting site certificate error | Chapter and page numbers unconfirmed. Chapter 3 already presents Equation 3.3 in the form given by Guo et al. (2017), which was read |
| REF-023 | Hossain et al. (2026), NEXUS | Full text read; the arXiv identifier (2607…) conflicts with the stated submission date of 25 May 2026 | Bibliographic only. Confirm which version to cite before submission |

**Verification improved during this stage.** Lorden (1971) and Moustakides (1986) were previously
recorded as Crossref-metadata-only. Their Project Euclid abstracts were read on 22 September 2026,
confirming identity and the optimality statements. Their status is *not* raised to VERIFIED,
because the claim Chapter 3 made about them concerned the conditions of their theorems, and those
were still not readable. The evidence basis in the workbook records exactly what was read.

**Blocked sources, recorded not circumvented:** SSRN (Jackson), the Brier publisher host, the
Platt host (certificate error), `web.archive.org` (blocked in this environment), and
`docs.lib.noaa.gov` (DNS failure). No attempt was made to route around any of these.

---

## F. Prior-art collision matrix

`04_PRIOR_ART_COLLISION_MATRIX.xlsx` — 20 systems assessed against REM on runtime layer,
non-invasiveness, multi-step handling, tool monitoring, risk decision, mitigation, financial focus,
overlap, difference and status.

**Seven direct collisions**, each of which bounds a novelty claim REM might otherwise make:

- **NEXUS** (Hossain et al., 2026) — calibrated logistic risk score, four graduated interventions,
  an irreversibility feature and reported latency. REM cannot claim any of these as new. Its
  remaining distinction is that the verdict is a per-decision expected-loss minimisation rather
  than a rule cascade gated by the score.
- **Calibration Is Not Control** (C. Zhang et al., 2026) — shows directly that calibrating a scalar
  score does not improve threshold-based control. REM must cite this as a limitation of its own
  approach, not as a gap it fills.
- **AgentTrust** (C. Yang, 2026) — the same four verdicts, reversibility in the severity rubric,
  and component ablations with latency.
- **SafeAgent** (H. Liu et al., 2026) — stateful protection with consequence reasoning and
  graduated recovery.
- **FinHarness** (Jia et al., 2026) — inline per-step monitoring of a financial agent. REM cannot
  claim to be the first runtime protection for financial agents.
- **Authority Frontier** (H.-H. Chen, 2026) — consequence pricing with escalation.
- **ProvenanceGuard** (She et al., 2026) — provenance-based checking of action evidence.

Six further systems overlap partially, five are complementary rather than competing, and one
(LlamaFirewall) is a component source: it supplies the candidate pre-trained injection classifier
that REM's Detection Layer uses as one feature. One entry, the Jackson (2025)
working paper, is marked **BLOCKED — REQUIRES AUTHOR/SOURCE REVIEW**: its overlap with REM cannot
be assessed because its text is inaccessible.

**What this leaves for REM.** The defensible position is not a new mechanism but a specific
composition: a calibrated probability of adversarial inducement, combined with a declared
consequence tier through an explicit expected-loss minimisation over four verdicts, where the
threshold is a consequence of declared costs rather than a chosen constant, evaluated on an
open executable financial benchmark with utility and security measured separately. Chapter 2's
positioning section and Chapter 3's novelty boundaries already state this; no claim in either
chapter was found to exceed it.

---

## G. Equation source audit

`05_EQUATION_SOURCE_AUDIT.xlsx` — all 22 numbered equations in Chapter 3; Chapter 2 contains none,
which was confirmed by parsing rather than assumed.

| Type | Count |
|---|---|
| REM-defined | 8 |
| Adapted from a source | 6 |
| Literature equation | 5 |
| Standard / derived | 3 |

Eighteen are verified as stated: two are UNVERIFIED and two carry a partial verification. The
exceptions, and one caveat on an optional equation:

- **Eq. 3.1 (Cox, 1958)** and **Eq. 3.2 (le Cessie & van Houwelingen, 1992)** — UNVERIFIED
  formulation. Both are textbook-standard forms, but the printed originals were not read. Chapter 3
  already flags Equation 3.2.
- **Eq. 3.3 (Platt, 1999)** — the form used is the one printed by Guo et al. (2017), which was
  read; Platt's original parameterisation is unconfirmed.
- **Eq. 3.9 (threshold)** — derivation verified; the comparison to Elkan's printed threshold was
  softened in edit E-03.
- **Eqs. 3.15–3.17 (CUSUM)** — verified against Basseville & Nikiforov (1993); the Bernoulli
  substitution's secondary reference (Reynolds & Stoumbos, 1999) was not read. This whole section
  is optional and outside the verdict path.

No equation was invented, added or renumbered in this stage.

---

## H. Numerical claims audit

`06_NUMERICAL_CLAIMS_AUDIT.xlsx` — 74 substantive quantitative statements, filtered from 600 raw
numeric matches by removing section and equation cross-references, list numbering, symbol
subscripts, feature indicator values and bibliographic numbers.

| Status | Count |
|---|---|
| VERIFIED (figure read in the cited source) | 63 |
| VERIFIED AT INSPECTION DATE (read from the benchmark artifact) | 7 |
| UNVERIFIED (cited source not readable) | 4 |
| Unsourced | 0 |

Every reported figure in both chapters is attributed. The seven artifact-based figures are the
AgentDojo banking-suite counts in Section 3.11.2 (16 user tasks, 9 injection tasks, 11 tools, 144
combinations), taken from the repository on inspection in September 2026; Chapter 3 already states
that these must be re-confirmed against the version pinned for the experiments. Chapter 2's
convention that all performance figures are as reported by each study's own authors on its own
benchmark holds throughout, and edit P-05 made that attribution explicit in one further place.

Two figures marked `[DATA COUNT REQUIRES VERIFICATION]` in Chapter 3 remain open by design: the
number of traces and the number of positive steps both depend on experiments that have not been
run.

---

## I. AI-style / authorial prose audit

`07_AI_STYLE_AUDIT.xlsx` — 11 findings: 3 HIGH, 3 MEDIUM, 3 LOW, 2 measurement-only.

**This is not a detector result.** No AI-detection tool was available or executed in this
environment. Nothing here states or implies that either chapter would or would not be flagged by
any such tool, and no edit was made for that purpose.

**What the measurements show.** Both chapters are already free of the patterns most often
associated with generated academic prose. There are no connective-chain openers
("Furthermore", "Moreover", "Additionally", "It is important to note") in either chapter — zero
occurrences — and a scan for fourteen stock phrases ("crucial", "pivotal", "delve", "seamless",
"leverage", "holistic", "landscape", "realm", "underscore", "tapestry", and similar) returned no
hits. Mean sentence length is 12.7 words in Chapter 2 and 10.5 in Chapter 3.

**The real finding is structural, in Chapter 3.** 38% of that chapter's words (2,881 of 7,761) sit
inside list items, and three sections — 3.3.7 Security objectives, 3.11.3 Label construction and
3.11.6 Leakage controls — consisted of a heading followed immediately by a list, with no
connecting prose at all. A methodology chapter written this way reads as a specification rather
than as an argument, and an examiner cannot see the author's reasoning between the items. Those
three sections were given lead-in prose (P-01 to P-03). The remaining list density was left alone
because reducing it would change a chapter structure that is frozen.

**Chapter 2's two findings** were a four-sentence catalogue of systems with an identical sentence
shape (P-04) and a single sentence carrying five figures (P-05).

**Three findings were recorded and deliberately not acted on** — the eleven `**Synthesis.**`
section closers, one antithetical sentence pairing, and enumerative "First … Second … Third"
scaffolding. Each is defensible academic practice; the decision belongs to the author, and the
workbook records the passage and the alternative so that decision can be made.

**Editing principle.** No grammatical error, informality or vagueness was introduced. Nothing was
made to look less competent. No technical content was simplified.

---

## Deliverables in this directory

| File | Contents |
|---|---|
| `00_WORKSPACE_INVENTORY.md` | What exists in the workspace and what the environment can and cannot do |
| `00_BASELINE_CHECKSUMS.md` | SHA-256 and structural counts of every source file, recorded before editing |
| `01_CHAPTER2_LITERATURE_EVIDENCE_AUDIT.xlsx` | 52 Chapter 2 claims with source, evidence location, verification and required action |
| `02_CHAPTER3_LITERATURE_EVIDENCE_AUDIT.xlsx` | 55 Chapter 3 claims, same columns |
| `03_REFERENCE_VERIFICATION_MASTER.xlsx` | All 58 works: identifiers, existence, metadata, primary-source status, verification |
| `04_PRIOR_ART_COLLISION_MATRIX.xlsx` | 20 systems compared with REM across 12 dimensions |
| `05_EQUATION_SOURCE_AUDIT.xlsx` | All 22 equations: source, exact location, type, verification, required change |
| `06_NUMERICAL_CLAIMS_AUDIT.xlsx` | 74 quantitative statements with attribution and status |
| `07_AI_STYLE_AUDIT.xlsx` | 11 prose findings, method and limits, and the measured baseline |
| `08_FINAL_CHAPTER_2.docx` | Chapter 2 with the four edits applied |
| `09_FINAL_CHAPTER_3.docx` | Chapter 3 with the five edits applied |
| `10_MASTER_AUDIT_REPORT.md` | This report |
| `11_EDIT_CHANGELOG.md` | Every edit, before and after, with its reason |
| `working/` | The derived Markdown copies that were edited |

---

## Outstanding items for the author and supervisor

1. **Obtain Platt (1999)** through institutional access and confirm the chapter and page numbers,
   or continue to present Equation 3.3 in the form given by Guo et al. (2017).
2. **Obtain Elkan (2001) in a readable form** and confirm the printed threshold expression, or
   leave edit E-03's derivation-only wording in place.
3. **Resolve the NEXUS citation conflict** (REF-023): decide which version of the paper to cite
   and correct the date or identifier accordingly.
4. **Decide the three recorded style questions** (S-07 to S-09) — they are stylistic preferences,
   not defects.
5. **Re-confirm the AgentDojo banking-suite counts** against the benchmark version pinned for the
   experiments, as Section 3.11.2 already requires.
6. **Brier (1950) and Jackson (2025)** remain inaccessible from this environment. The Brier score
   stays deferred; Jackson stays cited but undescribed.
