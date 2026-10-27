# STAGE 2 — EDIT CHANGELOG

**Date:** 2026-09-22

Stage 2 made **two** edits to the chapter text. Both were applied to **copies** in
`revised_chapters/`. The Stage 1 working files were not modified.

| | Chapter 2 | Chapter 3 |
| --- | --- | --- |
| Source (unmodified) | `Chapter2_working.md` `1e59d4a74d9205a2` | `Chapter3_working.md` `5085e11732dee82f` |
| Stage 2 copy | `Chapter2_stage2.md` `cbd7083710eac456` | `Chapter3_stage2.md` `69b7551e302af3b6` |
| Words before → after | 7,936 → 7,938 | 12,894 → 12,954 |

The 9 Stage 1 corrections are carried through unchanged; Stage 2 edits are applied
on top of them.

---

## E-02 — Elkan (2001): page numbers added *(both chapters)*

**Reason:** Stage 1 recorded "page numbers unverified." dblp and the ACM Digital
Library (*Proceedings of the 17th IJCAI, Volume 2*, `10.5555/1642194.1642224`)
independently give pp. 973–978.

**Before**

> Elkan, C. (2001). The foundations of cost-sensitive learning. In *Proceedings of
> the Seventeenth International Joint Conference on Artificial Intelligence
> (IJCAI-01)*. https://cseweb.ucsd.edu/~elkan/rescale.pdf

**After**

> Elkan, C. (2001). The foundations of cost-sensitive learning. In *Proceedings of
> the Seventeenth International Joint Conference on Artificial Intelligence
> (IJCAI-01)* (pp. 973–978). https://cseweb.ucsd.edu/~elkan/rescale.pdf

Applied to one entry in each chapter's reference list. No in-text citation changed.

---

## E-05 — §3.11.3 Label construction: converted to prose *(Chapter 3)*

**Reason:** Task K. The three bolded items were not parallel list items but three
stages of one argument — what the rule matches, where it is known to be uncertain,
and how that uncertainty is measured. Label construction is the most contestable
methodological choice in the chapter, and a bulleted register understated the
reasoning. The Stage 1 lead-in paragraph (P-02) is retained above it, unchanged.

**Preserved verbatim:** every technical statement, the symbols `y_{t} = 1` and
`y_{t} = 0`, the matching criteria (tool name; attacker-controlled key argument;
attacker account identifier; attacker-specified password), the amount-alteration
example, the audit-on-manual-sample procedure, the disagreement-rate reporting, and
the **pending supervisor decision** flag on induced read steps.

**Nothing was added** beyond connective phrasing. Three clauses make explicit what
the original bullets left implicit and what the surrounding sections already state:
that the label records the attacker's objective being served rather than the
attacker's presence; that the induced-read case is recorded as open rather than
settled; and that a mechanical derivation fails systematically rather than randomly,
which is why the sample audit exists.

**Before**

```
- **Step labels.** In an attacked episode, a proposed tool call is labeled
  y_{t} = 1 if it matches a call in the injection task's reference solution on tool
  name and on the attacker-controlled key argument, such as the attacker account
  identifier or the attacker-specified password. All other proposed calls,
  including calls that continue the user's task in attacked episodes, are labeled
  y_{t} = 0, as are all calls in episodes without injection.
- **Induced read steps.** Some injection tasks include a read call in their
  reference solution. Whether such a read step is labeled y_{t} = 1 is pending
  supervisor decision, because it is induced but has no direct external effect.
- **Label audit.** Matching on arguments can mislabel steps, for example when an
  agent alters an amount. The derivation is therefore audited on a manually
  inspected sample of episodes, and the disagreement rate is reported.
```

**After**

```
In an attacked episode, a proposed tool call is labeled y_{t} = 1 if it matches a
call in the injection task's reference solution on tool name and on the
attacker-controlled key argument, such as the attacker account identifier or the
attacker-specified password. All other proposed calls are labeled y_{t} = 0. This
includes calls that continue the user's task inside an attacked episode, and it
includes every call in episodes without injection: what the label records is the
attacker's objective being served, not the attacker being present.

One case does not resolve cleanly under that rule. Some injection tasks include a
read call in their reference solution, and such a step is induced by the attacker
yet has no direct external effect. Whether it should be labeled y_{t} = 1 is
pending supervisor decision, and it is recorded here as open rather than settled by
the labeling rule.

Matching on arguments can also mislabel steps in its own right, for example when an
agent alters an amount before proposing the call. Because the derivation is
mechanical, its failures are systematic rather than random, so the labels are
audited against a manually inspected sample of episodes and the disagreement rate
is reported alongside the results.
```

---

# EDITS CONSIDERED AND DELIBERATELY NOT MADE

| # | Candidate | Why not |
| --- | --- | --- |
| **Platt (1999) reference** | Correct the entry | A genuine conflict (see report §B), but the fully-evidenced fix changes the year to 2000 and ripples through every in-text `(Platt, 1999)` in both chapters. The alternative fix needs a technical-report number that **could not be confirmed** — the only candidate appeared solely inside a query this audit wrote, so it was rejected rather than used. **Author decision.** |
| **NEXUS arXiv identifier** | "Fix" 2607 → 2605 | No such identifier was observed. The chapter's citation is correct; the conflict is in arXiv's own record. Changing it would fabricate a bibliographic record. |
| **§3.3.7 Security objectives** | Convert list to prose | Items are labelled SO-1…SO-6 and cross-referenced by label elsewhere. A labelled register is the correct format; conversion would damage the cross-references. |
| **§3.11.6 Leakage controls** | Convert list to prose | A register of five independently checkable pre-registered controls. The list form is what makes the leakage discipline auditable. |
| **S-07 eleven `**Synthesis.**` closers** | Vary the labels | Consistency across a literature review is defensible, and varying only some would be worse. Recommended to retain. Author decision. |
| **S-08 antithetical pairing** | Rephrase | The sentence is accurate, compact and carries a causal explanation. Rewriting it for rhythm would be editing for a detector, not a reader. |
| **S-09 First/Second/Third** | Rephrase | Standard academic enumeration of two genuinely different things. |
| **Four NEXUS numerical claims** | Adjust the figures | Source text is inaccessible. Figures must be confirmed against the paper or reattributed as author-reported — neither is an auditor's silent edit. |
| **Equation 3.1 Status line** | Soften wording | Recommended in the report (§F); left to the author because it is the author's claim about their own verification, not a factual error. |

---

# INTEGRITY

- [x] Source-of-truth files unmodified — Stage 1 digests re-verified after all work
- [x] All edits applied to copies under `revised_chapters/`
- [x] No Stage 1 correction discarded
- [x] No figure, DOI, identifier, page number or report number invented
- [x] Every edit is reversible from this changelog
