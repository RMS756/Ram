# PAPER_18 — FinHarness: An inline lifecycle safety harness for finance LLM agents

**Category:** D. Financial-agent evaluation · **Stage 1 Ref ID:** REF-025 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 18 | This pack |
| Exact title (as cited) | *FinHarness: An inline lifecycle safety harness for finance LLM agents* | Ch2 reference list L271 and Ch3 reference list L1020 |
| Full authors (as cited) | Jia, H., Liu, Y., Chong, B., Yang, Y., Chen, Y., Liang, J., Li, Q., Lu, H., Xu, K., Zheng, H., Zhang, C., Peng, H., & Yu, P. S. | Ch2 reference list L271 and Ch3 reference list L1020 |
| Year (as cited) | 2026 | Ch2 reference list L271 and Ch3 reference list L1020 |
| Venue (as cited) | (arXiv:2605.27333) [Preprint]. arXiv. | Ch2 reference list L271 and Ch3 reference list L1020 |
| DOI | None recorded (arXiv preprint) | — |
| arXiv ID | `2605.27333` | Chapter reference entry; Stage 1 reference master |
| Official publisher / record URL | https://arxiv.org/abs/2605.27333 | Chapter reference entry (arXiv record) |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
- **Basis:** Stage 1: "arXiv abstract (components and numbers)".

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #19): §2.5 Stateful and Trajectory-Aware Protection (L73); §2.7 Financial-Agent Security Requirements (L97); §2.10 Runtime Decision and Mitigation (L132); §2.13 Comparative Synthesis (L183)
- **Chapter 3** (reference #19): §3.13 Contribution and Novelty Boundaries (L889)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-022** — FinHarness (Jia et al., 2026) tracks user intent across multiple interactions in its Query Monitor. | Ch2 §2.5 L73 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-033** — FinHarness (Jia et al., 2026) is the closest domain-specific runtime system. | Ch2 §2.7 L97 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-034** — It combines a Query Monitor that tracks intent across interactions, a Tool Monitor that assesses each proposed action, and a Cascade that routes verification between lighter and more capable judges. | Ch2 §2.7 L97 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-035** — Its authors report that the routed configuration reduced attack success from 38.3% to 15.0% while largely preserving benign approval, with 4.7 times fewer calls to the advanced judge. | Ch2 §2.7 L97 | follows | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-036** — FinHarness addresses it directly, and consequence pricing has been proposed by H.-H. Chen (2026). | Ch2 §2.7 L110 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-048** — The reviewed systems turn evidence into action in several ways: by rule verdicts with maximum-severity aggregation (C. Yang, 2026), by thresholds on a predicted probability (H. Wang et al., 2025), by a rule cascade ga… | Ch2 §2.10 L132 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-062** — \| FinHarness (Jia et al., 2026) \| Monitors and judge cascade \| — \| — \| — \| ✓ (benign approval) \| — \| ✓ \| | Ch2 §2.13 L183 | table row | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-071** — Financial runtime safety is addressed by FinHarness. | Ch2 §2.13 L191 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-075** — FinHarness addresses the financial domain with monitors and judges rather than a calibrated probability and declared losses. | Ch2 §2.13 L193 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-121** — \| Runtime protection of financial agents \| Jia et al. (2026) \| | Ch3 §3.13 L889 | table row | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |

## What to read in the paper

**Reading mode:** Targeted reading.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **Abstract.** Stage 1 verified the components and the 38.3% → 15.0% result (N049, N050) at this level.
- **The Query Monitor, Tool Monitor and Cascade.** Ch2 L73 and L97.
- **Evaluation results.** Ch2 L97 also states "4.7 times fewer calls to the advanced judge". That figure has no numerical-audit row of its own.

## Why this paper matters for understanding REM

This is the closest runtime system built specifically for financial agents. Chapter 3 lists it as prior art, so "runtime protection of financial agents" is not claimed as new.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
