# PAPER_07 — Safeguarding LLM agents from misalignment through provenance analysis

**Category:** B. Prior-art / competing approaches · **Stage 1 Ref ID:** REF-045 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 07 | This pack |
| Exact title (as cited) | *Safeguarding LLM agents from misalignment through provenance analysis* | Ch2 reference list L301 and Ch3 reference list L1048 |
| Full authors (as cited) | She, Y., Liang, Y., & Kang, E. | Ch2 reference list L301 and Ch3 reference list L1048 |
| Year (as cited) | 2026 | Ch2 reference list L301 and Ch3 reference list L1048 |
| Venue (as cited) | (arXiv:2607.01236) [Preprint]. arXiv. | Ch2 reference list L301 and Ch3 reference list L1048 |
| DOI | None recorded (arXiv preprint) | — |
| arXiv ID | `2607.01236` | Chapter reference entry; Stage 1 reference master |
| Official publisher / record URL | https://arxiv.org/abs/2607.01236 | Chapter reference entry (arXiv record) |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
- **Basis:** Stage 1: "arXiv abstract (44.3% to 2.1%)".

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #34): §2.6 Tool-Use and Action-Boundary Security (L85); §2.8 Detection and Classification Approaches (L114); §2.11 Explainability and Auditability (L144); §2.13 Comparative Synthesis (L182)
- **Chapter 3** (reference #33): §3.13 Contribution and Novelty Boundaries (L886)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-025** — ProvenanceGuard (She et al., 2026) formulates misalignment detection as the question of whether a proposed tool call is supported by traceable evidence in the agent's context. | Ch2 §2.6 L85 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-026** — Compared with an LLM-as-a-judge baseline on Agent-SafetyBench, it reduced the error rate on misaligned traces from 44.3% to 2.1%. | Ch2 §2.6 L85 | follows | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-038** — Provenance analysis asks whether an action is supported by evidence (She et al., 2026). | Ch2 §2.8 L114 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-058** — ProvenanceGuard grounds decisions in traceable evidence (She et al., 2026). | Ch2 §2.11 L144 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-061** — \| ProvenanceGuard (She et al., 2026) \| Evidence support for tool calls \| — \| — \| — \| — \| — \| — \| | Ch2 §2.13 L182 | table row | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-118** — \| Provenance analysis of tool calls \| She et al. (2026); Debenedetti et al. (2025) \| | Ch3 §3.13 L886 | table row | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |

## What to read in the paper

**Reading mode:** Targeted reading.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **Abstract.** Stage 1 verified the formulation and the 44.3% → 2.1% result (N041, N042) at this level.
- **The problem formulation: whether a proposed tool call is supported by traceable evidence in the agent's context.** Ch2 §2.6, §2.8 and §2.11. This is prior art for REM's provenance labeling.
- **The comparison with an LLM-as-a-judge baseline on Agent-SafetyBench.** Ch2 L85.

## Why this paper matters for understanding REM

Provenance-based checking of tool calls is prior art for the provenance labeling at the start of REM's pipeline (Ch2 §2.6, §2.8; Ch3 §3.13).

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
