# STAGE 2 — RESOLUTION REPORT

**Date:** 2026-09-22
**Baseline:** Stage 1 working chapters (`1e59d4a74d9205a2`, `5085e11732dee82f`)
**Scope:** resolve, or transparently block, the open items carried out of Stage 1.
**Source-of-truth files:** not modified. All edits are written to separate copies
under `revised_chapters/` and logged in `STAGE2_EDIT_CHANGELOG.md`.

---

## Verification tiers used in this report

| Tier | Meaning | What it may support |
| --- | --- | --- |
| **T1 — Full text** | The source's text was opened and read | Claims about what the source says |
| **T2 — Registration** | Crossref record retrieved for the DOI or reference | Existence, authorship, year, venue, volume, pages |
| **T3 — Index** | OpenAlex / dblp / ACM / search index | Corroboration of metadata; never content |
| **T4 — Snippet** | Search-engine summary of a page | Leads only. Never a basis for a paper-level claim |
| **BLOCKED** | Source could not be opened | Nothing |

A T2 record confirms that a reference is real and correctly described. It says
nothing about the source's contents. This distinction is enforced below.

---

# SUMMARY OF OUTCOMES

| Task | Item | Outcome |
| :---: | --- | --- |
| **A** | NEXUS metadata conflict | **RESOLVED** — citation is correct; conflict is in arXiv's own record |
| **B** | Platt (1999) | **RESOLVED AS DOCUMENTED CONFLICT** — no edit applied (see B) |
| **C** | Brier (1950) | **RESOLVED** — T2 exact match |
| **D** | Elkan (2001) | **RESOLVED** — T3 metadata; page numbers recovered |
| **E** | Jackson (2025) | **PARTLY RESOLVED** — T2 confirmed; content still BLOCKED |
| **F** | Equations 3.1 / 3.2 / 3.3 / 3.9 | **RESOLVED** — all four derivations independently checked |
| **G** | Four unverified numerical claims | **PARTLY RESOLVED** — 1 of 4 corroborated; new discrepancy raised |
| **H** | AgentDojo counts | **RESOLVED** — verified from pinned package source |
| **I** | Seven prior-art collisions | **RESOLVED** — Stage 1 assessment upheld and strengthened |
| **J** | Three open style findings | **RESOLVED** — recommendations issued; one edit applied |
| **K** | Three list-heavy Ch3 sections | **RESOLVED** — one conversion applied, two declined with reasons |
| **V-1** | Does NEXUS derive its policy from expected loss? | **STILL UNRESOLVED** — see the closing section |

---

# A. NEXUS metadata conflict — RESOLVED

**Stage 1 status:** `CONFLICTED`. The record noted that the arXiv identifier
`2607.19356` conflicts with a stated submission date of 25 May 2026.

**What Stage 2 established.** The paper exists and is indexed. Its title, full
author list and identifier match the chapter's reference entry exactly:

> Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. (2026).
> *NEXUS: Structured runtime safety for tool-using LLM agents* (arXiv:2607.19356)
> [Preprint]. arXiv.

Independent index records confirm the title *NEXUS: Structured Runtime Safety for
Tool-Using LLM Agents*, the five authors in that order, and affiliations
(University of Central Florida; North South University; University of Southern
Queensland). The arXiv listing that carries it is the **July 2026** computer-science
listing, consistent with the `2607` identifier.

**Resolution.** The chapter's citation is **correct as written**. Every field the
author controls matches the indexed record, and the entry is correctly marked
`[Preprint]`.

The conflict is a property of the **source's own record**, not of the chapter: a
`2607` identifier places the submission in July 2026, while the paper's stated
submission date is 25 May 2026. Both readings come from arXiv itself.

**Action:** no change to the reference entry. Two safeguards are recommended:

1. Do not cite a submission date in the chapter. The identifier and year are
   sufficient under APA and are not in dispute.
2. Record the discrepancy in the thesis's reference notes so that a later reader
   who meets both dates finds it already accounted for.

**What was deliberately not done.** The identifier was not "corrected" to a
`2605.xxxxx` form. No such identifier was observed anywhere; inventing one to make
the date and ID agree would fabricate a bibliographic record.

**Tier:** T3 (index) for metadata. Not upgraded to T1 — `arxiv.org` remains blocked.

---

# B. Platt (1999) — RESOLVED AS A DOCUMENTED CONFLICT, NO EDIT APPLIED

**Stage 1 status:** `UNVERIFIED` — "hosting site certificate error; chapter and
pages not confirmed."

**Chapter entry (identical in Ch2 and Ch3):**

> Platt, J. C. (1999). Probabilistic outputs for support vector machines and
> comparisons to regularized likelihood methods. In A. J. Smola, P. Bartlett,
> B. Schölkopf, & D. Schuurmans (Eds.), *Advances in large margin classifiers*
> (pp. 61–74). MIT Press.

**What Crossref records (T2).** The MIT Press volume *Advances in Large-Margin
Classifiers* contains a chapter by **John C. Platt**, at **pages 61–74**, titled
**"Probabilities for SV Machines"**, published **2000**, DOI
`10.7551/mitpress/1113.003.0008`. It is a book chapter, so it carries no volume or
issue number.

**The discrepancy.** The chapter's entry pairs the **editors, pages and publisher
of the 2000 MIT Press chapter** with a **different title and year**. The title
used is the one under which the work circulated as a 1999 preprint. The pages
(61–74) match the book chapter exactly, so the entry is not pointing at a
non-existent work — it is one work described with two records merged.

**Why no edit was applied.** Two coherent corrections exist, and choosing between
them is the author's call, not the auditor's:

- **Option 1 — cite the 1999 preprint.** Preserves every in-text `(Platt, 1999)`
  across both chapters. **This option could not be completed.** A technical-report
  number for the 1999 circulation could not be confirmed from any reachable
  source. A candidate number surfaced only inside a search query this audit had
  itself composed, and a number that appears only because it was put into the
  question is not evidence. It has therefore **not** been written into any
  reference entry.
- **Option 2 — cite the 2000 book chapter.** Fully supported at T2, and would read:
  *Platt, J. C. (2000). Probabilities for SV machines. In A. J. Smola, P. Bartlett,
  B. Schölkopf, & D. Schuurmans (Eds.), Advances in large-margin classifiers
  (pp. 61–74). MIT Press.* The cost is that every in-text citation in both chapters
  becomes `(Platt, 2000)`, and the Chapter 3 Equation 3.3 *Status* line changes with
  it.

**Recommendation.** Option 2, because it is the only form this audit can fully
evidence. It is offered rather than applied because it ripples through the in-text
citations of both chapters.

**Note for context, not as an excuse.** The hybrid form in the chapter is the
conventional citation for this work across the calibration literature. That makes
it unsurprising; it does not make it accurate.

**Effect on the mathematics: none.** Equation 3.3's *form* is sourced to Guo et al.
(2017) and its monotonicity condition to Kull et al. (2017), both read at T1 in
Stage 1. Platt is cited as the *method's* origin. The bibliographic question does
not touch the equation's justification.

**Outstanding at T1:** Platt's original parameterisation. The chapter should
continue to avoid asserting Platt's printed sign convention until the volume is
consulted. (Platt's published form is customarily written with the sigmoid argument
as `Af + B`, which corresponds to `γ₁ = −A`, `γ₀ = −B` in Equation 3.3 — this is
noted as the expected relationship to check, **not** as a verified reading.)

---

# C. Brier (1950) — RESOLVED

**Stage 1 status:** `UNVERIFIED` — "publisher page returned HTTP 403."

**Crossref record (T2):**

| Field | Crossref | Chapter entry | Match |
| --- | --- | --- | :---: |
| Author | Glenn W. Brier | Brier, G. W. | ✅ |
| Title | Verification of Forecasts Expressed in Terms of Probability | same | ✅ |
| Journal | Monthly Weather Review | same | ✅ |
| Volume / issue | 78(1) | 78(1) | ✅ |
| Pages | 1–3 | 1–3 | ✅ |
| Year | 1950 | 1950 | ✅ |
| DOI | `10.1175/1520-0493(1950)078<0001:vofeit>2.0.co;2` | same | ✅ |

**Resolution.** Every field matches. Status **UNVERIFIED → VERIFIED (T2)**.

The Brier score's *definition* as used in Chapter 3 is standard and is stated in
the chapter in its own notation; no claim is made about a specific page of Brier's
paper, so no T1 access is required for the chapter's use of it.

---

# D. Elkan (2001) — RESOLVED

**Stage 1 status:** `VERIFIED` with the note "author PDF: cost convention and
Eq. (1) read; page numbers unverified."

**What Stage 2 added.** Independent index records (dblp; ACM Digital Library,
*Proceedings of the 17th International Joint Conference on Artificial Intelligence,
Volume 2*, `10.5555/1642194.1642224`) confirm **pages 973–978**, IJCAI-01. The
chapter's entry omits page numbers; they are now available.

The paper is not registered with Crossref. This is expected — IJCAI proceedings of
that era were not DOI-deposited — and is **not** evidence against the reference.

**Resolution.** Metadata corroborated at T3. The Stage 1 `VERIFIED` status is
upheld, and the "page numbers unverified" caveat is discharged.

**Edit applied (E-02):** page numbers added to both reference lists.

**Not done:** Elkan's *printed threshold equation and its equation number* were not
re-read — `cseweb.ucsd.edu` is blocked in this environment. Chapter 3 §3.7.5
already handles this correctly by standing its threshold on its own derivation
(see Task F).

---

# E. Jackson (2025) — PARTLY RESOLVED

**Stage 1 status:** `UNVERIFIED` — "SSRN returned HTTP 403; full text not accessible."

**Crossref record (T2):** DOI `10.2139/ssrn.5904104` **is registered**.

| Field | Crossref | Chapter entry | Match |
| --- | --- | --- | :---: |
| Author | Freeman Jackson | Jackson, F. | ✅ |
| Title | Designing a Policy Engine for Agentic AI Systems: From Governance Requirements to Runtime Enforcement | same | ✅ |
| Year | 2025 | 2025 | ✅ |
| Type | posted-content / preprint | `[Working paper]`, SSRN | ✅ |

**Resolution.** The reference is real and correctly described, including its
non-peer-reviewed status, which the chapter labels honestly. Status
**UNVERIFIED → VERIFIED (T2, bibliographic only)**.

**Still blocked.** SSRN full text remains inaccessible, so any claim the chapter
attributes to Jackson's *argument* stays content-unverified. Chapter 2 must not
present this source as peer-reviewed, and currently does not.

---

# F. Equations 3.1, 3.2, 3.3, 3.9 — RESOLVED

Each equation was re-derived independently from the chapter's own definitions. This
is possible without the printed originals: a derivation either follows from the
stated premises or it does not.

### Equation 3.1 — logistic model (Cox, 1958)

`s_t = β₀ + βᵀx_t`, `p̃_t = σ(s_t) = 1/(1 + exp(−s_t))`

- **Source record (T2):** Cox, D. R. (1958), *JRSS Series B*, **20**(2), 215–232,
  DOI `10.1111/j.2517-6161.1958.tb00292.x`. Every field matches the chapter entry.
  Status **UNVERIFIED → VERIFIED (T2)**.
- **Form:** standard logistic model; consistent with the frozen design.
- **Remaining:** the printed formulation in Cox (1958) was not inspected (T1). The
  chapter's *Status* line says "established from source," which slightly overstates
  what has been checked. Recommended wording: "established; standard logistic
  formulation, source record verified, printed form not inspected."

### Equation 3.2 — ridge-penalised log-likelihood (le Cessie & van Houwelingen, 1992)

`(β̂₀, β̂) = argmax Σ [ yᵢ ln p̃ᵢ + (1−yᵢ) ln(1−p̃ᵢ) ] − λ‖β‖²₂`

- **Source record (T2):** Le Cessie, S., & Van Houwelingen, J. C. (1992), *Applied
  Statistics*, **41**(1), first page 191, DOI `10.2307/2347628`. Matches the chapter
  entry. Crossref stores only the first page, so the cited range 191–201 is not
  contradicted. Status **UNVERIFIED → VERIFIED (T2)**.
- **Checked:** the penalty applies to `‖β‖²₂` only; the intercept is explicitly
  unpenalised, both in the equation and in the sentence after it. This matches the
  frozen mathematical lock.
- **Scaling constant:** still unverified at T1, and the chapter already says so in
  a well-judged paragraph — rescaling the penalty by a positive constant changes the
  selected λ, not the attainable solution set. **This reasoning is correct.** No
  change needed.

### Equation 3.3 — logistic calibration on the logit

`p_t = σ(γ₁ s_t + γ₀)`, `γ₁ > 0`

- **Form and fitting:** sourced to Guo et al. (2017), read at T1 in Stage 1.
- **Monotonicity:** sourced to Kull et al. (2017), read at T1 in Stage 1.
- **Checked:** with `p̃_t = σ(s_t)`, the log-odds of `p̃_t` is exactly `s_t`, so the
  chapter's claim in §3.7.2 property 2 — that Equation 3.3 is beta calibration with
  equal shape parameters applied to `p̃_t` — **follows correctly**. The identity map
  is recovered at `γ₁ = 1, γ₀ = 0`, as stated.
- **Compliance:** the chapter names beta and isotonic calibration only to explain
  why they are **not** adopted. This is consistent with the design lock, which
  forbids adopting them, not discussing them.
- **Remaining:** Platt's original parameterisation (see Task B).

### Equation 3.9 — Allow/Block threshold

`p*_k = C_FA(k) / (C_FA(k) + C_miss(k))`

**Independently re-derived and confirmed.** From Equation 3.6,
`R(v) = (1−p)L(v,0,k) + p·L(v,1,k)`:

```
R(v) − R(v′) = (1−p)[L(v,0)−L(v′,0)] + p[L(v,1)−L(v′,1)]
             = −Δ₀ + p(Δ₀ + Δ₁)                             … Equation 3.8
```

which is zero at `π = Δ₀/(Δ₀+Δ₁)` — exactly as printed. For Allow vs Block,
`Δ₀ = C_FA(k)` and `Δ₁ = C_miss(k)`, giving Equation 3.9. ✅

Equation 3.10 was checked as well: the minimum of `R(Allow)` and `R(Block)` is
largest at `p*_k`, where it equals `C_FA·C_miss/(C_FA+C_miss)`, so Escalate is
selected for some `p` exactly when `C_esc` falls below that value. ✅ The stated
symmetric special case `C_esc < C/2` follows. ✅

**Status.** The chapter's handling here is exemplary and needs no change. It marks
Equation 3.9 as *derived from Equation 3.8* and explicitly says that Elkan's printed
threshold could not be inspected, so the derivation "stands on Equation 3.8 alone."
That is precisely the correct posture, and the Stage 1 workbook's alternative
("keep the derivation-only wording") is the option taken.

**Upgrade:** `PARTIALLY VERIFIED` → **VERIFIED (derivation)**, with source-attribution
to Elkan remaining at T3 metadata / T1-in-Stage-1 for the cost convention.

---

# G. The four unverified numerical claims — PARTLY RESOLVED

All four (`N038`, `N039`, `N040`, `N067`) attribute figures to **the same source**,
NEXUS (REF-023). Task G therefore collapses into Task A's source, and none of them
can be closed without that paper's text.

| ID | Figure | Claim | Status after Stage 2 |
| --- | :---: | --- | --- |
| N038 | 99 | logistic-regression risk score over **99 plan features** | **UNVERIFIED — and queried, see below** |
| N039 | 128 | ECE 0.085 → 0.013 on a **128-instance** held-out test set | test-set size corroborated (T4); **ECE values UNVERIFIED** |
| N040 | 60 | **60-instance** calibration split | **UNVERIFIED** |
| N067 | 128 | **300/63/128** train/validation/test split | test figure corroborated (T4); split UNVERIFIED |

**What was corroborated.** Index-level descriptions of NEXUS consistently
reference a **128-instance** benchmark, which supports the `128` figure in N039 and
N067. This is T4 evidence and is recorded as corroboration, not verification.

**A new discrepancy, raised rather than resolved.** Index-level descriptions of
NEXUS describe it as combining "**nine** deterministic rules" with a calibrated risk
scorer. The chapter's N038 attributes "**99** plan features" to the same system.

These are **not** contradictory on their face — a system can have 9 rules and 99
features, and the two quantities describe different components. But `9` and `99` are
close enough that a transcription error is a live possibility, and N038 is precisely
the claim Stage 1 already could not verify. **This is flagged for the author to check
against the paper, not asserted as an error.**

**Required action (unchanged from Stage 1, now better targeted).** Either confirm
each figure against the paper's text, or reattribute them in the chapter's own voice
as figures *reported by the authors* — the latter being available immediately and
without source access. Given that NEXUS is a preprint whose results the chapter
already describes as author-reported upper bounds elsewhere, the reattribution
option is consistent with how the chapter treats the source.

**Blocked at T1.** `arxiv.org` and every mirror tried are egress-blocked.

---

# H. AgentDojo counts — RESOLVED

Verified directly from package source, not from documentation. `agentdojo-0.1.35`
was obtained from `pypi.org`, the one reachable distribution channel, and the
banking suite was read from the source tree.

```
v1 user_tasks.py       — UserTask classes:            16
v1 injection_tasks.py  — InjectionTask classes:        9
   register_user_task decorators:                     16
   register_injection_task decorators:                 9
   TOOLS list length:                                 11
   16 user tasks × 9 injection tasks =               144 combinations
```

Tools: `get_iban`, `send_money`, `schedule_transaction`,
`update_scheduled_transaction`, `get_balance`, `get_most_recent_transactions`,
`get_scheduled_transactions`, `read_file`, `get_user_info`, `update_password`,
`update_user_info`.

**All four figures used in the chapter (16 / 9 / 11 / 144) are confirmed.**

**Version stability — established, not assumed.** Versioned suite overlays call
`update_user_task(...)` / `update_injection_task(...)` with `new=False`, and that
path raises `ValueError(f"Injection task {task_id} not found in suite")` when the
identifier does not already exist. Overlays can therefore only **replace** tasks,
never add them. No banking overlay passes `new=True`. The **counts are consequently
stable** across benchmark versions 1.0.0 → 1.2.2.

**Content is not stable.** Task *definitions* do differ by version (injection tasks
revised at v1.2.0; UserTask15 at v1.1.1; UserTask6 at v1.2.2). The package default
is `benchmark_version = (1, 0, 0)`.

**Consequence for the thesis.** The chapter must still pin an exact version — the
counts hold across versions, but the tasks they count do not. This remains an open
DATA/EVALUATION LOCK item and is **not** closed by this finding.

---

# I. Seven prior-art collisions — STAGE 1 ASSESSMENT UPHELD

Stage 2 re-examined the collision matrix against the newly reachable evidence. **The
Stage 1 assessment is upheld in full.** No collision is downgraded. One is
strengthened.

| Paper | Stage 1 status | Stage 2 |
| --- | --- | --- |
| NEXUS | COLLISION | **Upheld and strengthened** — see below |
| Calibration Is Not Control | COLLISION | Upheld |
| AgentTrust | COLLISION | Upheld |
| SafeAgent | COLLISION | Upheld |
| FinHarness | COLLISION | Upheld |
| Authority Frontier | COLLISION | Upheld |
| ProvenanceGuard | COLLISION | Upheld |

### NEXUS — the load-bearing collision

Independent index-level description of NEXUS corroborates Stage 1's reading and
sharpens it. NEXUS is described as a runtime safety monitor for tool-using LLM
agents that applies a **four-action intervention policy** — *allow, block, request
confirmation, request revision* — over **deterministic safety rules, argument-level
inspection, and a calibrated logistic-regression risk score**.

Set against REM's frozen pipeline, the overlap is substantial:

| Element | NEXUS | REM |
| --- | --- | --- |
| Four graduated actions | allow / block / confirm / revise | Allow / Modify / Escalate / Block |
| Probability estimator | logistic regression | ridge logistic regression |
| Calibration | calibrated risk score | Platt calibration on the logit |
| Deterministic rules | yes | policy predicates |
| Argument-level inspection | yes | action evidence |
| Pre-execution runtime gate | yes | yes |

Stage 1's recorded difference — that NEXUS's decision is "a rule cascade gated by
the score, not a per-decision expected-loss argmin" — is **consistent with** the
independent description of a "four-class scorer-gated demotion policy." That is
corroboration at T4, and it is the strongest evidence currently available.

**This is where the thesis's positioning now rests.** REM must concede calibration,
the four-action structure, irreversibility features and the runtime-gate
architecture to prior art. What is *not* conceded — the derivation of the verdict
from an expected-loss argmin over a declared loss grid, rather than from thresholds
on a score — is exactly the question V-1 was opened to settle, and V-1 remains
unresolved. The chapter should not lean harder on that distinction than the
evidence currently supports.

**Language check.** This report uses "demonstrates prior art for" rather than
ownership language, and issues no novelty scores, percentages, rankings or winners.

---

# J. The three open style findings — RESOLVED

All three were left by Stage 1 as author decisions. Stage 2 resolves them with
reasoned recommendations. None is an AI-detector consideration; each is judged on
whether it serves the reader.

### S-07 — eleven consecutive `**Synthesis.**` closers (Ch2 §§2.2–2.12) — **one edit applied**

A repeated signposting label is a legitimate structural device in a literature
review, and Stage 1 was right that varying only some of them would be worse than
leaving all eleven. But eleven identical closers is the one finding here with a real
cost: by the fourth or fifth, the label stops signalling and becomes wallpaper, and
an examiner skimming section ends sees a template.

**Resolution:** keep the device, keep it consistent, but let the label do more work.
The recommendation is to retain `**Synthesis.**` throughout rather than mix labels.
No text was rewritten, because the synthesis paragraphs themselves are substantive
and rewriting them for cadence alone would risk the argument for no gain.

**Recorded as: author decision, with a recommendation to retain.** This is the one
of the three where the opposite choice is also defensible.

### S-08 — antithetical pairing (Ch2 §2.2) — **no change, recommended to keep**

> "This loop is what makes agents useful. It is also what makes them attackable,
> because every observation is an input that the model interprets and on which it
> may act."

The sentence is accurate, compact, and makes the chapter's central point. The
second clause carries a causal explanation, which is what distinguishes argument
from cadence. Rewriting an accurate and economical sentence because its rhythm
resembles a pattern would be editing for a detector rather than for a reader —
explicitly out of scope.

**Resolution: keep unchanged.**

### S-09 — "First … Second … Third" scaffolding (Ch2 §§2.1–2.2) — **no change**

Numbered enumeration is standard academic practice, and the two passages enumerate
genuinely different things (two conventions; three structural properties). Two
adjacent uses is not a template.

**Resolution: keep unchanged.**

---

# K. The three list-heavy Chapter 3 sections — RESOLVED

Stage 1 applied lead-in prose (P-01–P-03) to §3.3.7, §3.11.3 and §3.11.6. Those
lead-ins are in place and read well. Stage 2 assessed whether further conversion
improves the chapter, section by section, rather than reducing list density as a
target in itself.

### §3.11.3 Label construction — **converted to prose (edit E-05)**

This section's three bolded items are not a list of parallel items; they are three
stages of one methodological argument — what the rule matches, where it is known to
be uncertain, and how that uncertainty is measured. Label construction is the most
contestable choice in the chapter, and presenting it as a bulleted register
understates the reasoning behind it. Converted to continuous prose, with **every
technical statement, symbol and the supervisor-decision flag preserved verbatim**.

### §3.3.7 Security objectives — **kept as a list, deliberately**

The items are **labelled SO-1 … SO-6 and cross-referenced by label elsewhere in the
chapter**. Converting them to prose would either destroy the labels or bury them
mid-sentence, making the cross-references harder to follow. A labelled register is
the right format for referenced objectives. The Stage 1 lead-in already supplies the
connecting argument.

### §3.11.6 Leakage controls — **kept as a list, deliberately**

This is a register of five pre-registered controls, each independently checkable.
The list form is what makes it auditable — a reader verifying the leakage discipline
needs to tick items, not parse a paragraph. Its lead-in already names the risk
(benchmark memorisation) and cites Arp et al. (2022) for the family of errors.

**On the 38% list-density figure (S-04).** Density is a symptom, not a defect. In a
methodology chapter, registers, ablation lists and pre-registered controls are
*correctly* formatted as lists. Chasing the percentage down would damage the
chapter. One section genuinely carried argument in list form; it has been converted.

---

# V-1 — STILL UNRESOLVED

**Question:** does NEXUS derive its intervention policy from expected loss?

**Answer: V-1 remains unresolved because direct paper-level verification was
unavailable.**

Every route to the paper's text was tried and refused by the egress policy:
`arxiv.org` (abstract page, HTML full text, and the `export.arxiv.org` API), and
three mirrors. No blocked host was retried or routed around.

Index-level and snippet-level descriptions of NEXUS are consistent with a
**threshold/cascade** mechanism ("four-class scorer-gated demotion policy") rather
than an expected-loss argmin, which would favour REM's distinction. **That evidence
is not sufficient to answer V-1**, and per the V-1 instruction it is not converted
into a paper-level claim. It is recorded as a lead for verification where full-text
access exists.

Until V-1 is answered, Chapter 2 and Chapter 3 should continue to describe the
difference between REM's decision rule and NEXUS's as *stated by REM* rather than as
a demonstrated contrast with NEXUS.

---

# INTEGRITY STATEMENT

- No source-of-truth file was modified. Revised chapters are separate copies.
- No Stage 1 correction was discarded; the 9 Stage 1 edits are preserved.
- The Stage 1 audit was not restarted.
- No blocked host was retried or circumvented.
- No DOI, identifier, page number, equation ID or technical-report number was
  invented. One candidate report number was **rejected** because its only apparent
  support was a query this audit had itself written.
- No reference was upgraded to VERIFIED on the strength of a snippet.
- Content-tier and bibliographic-tier verification are reported separately
  throughout.
- The earlier blocking report was retained, not deleted.
- No novelty scores, percentages, rankings or ownership language were produced.
