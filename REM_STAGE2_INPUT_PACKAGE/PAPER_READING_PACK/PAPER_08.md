# PAPER_08 — AgentTrust: Runtime safety evaluation and interception for AI agent tool use

**Category:** B. Prior-art / competing approaches · **Stage 1 Ref ID:** REF-053 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 08 | This pack |
| Exact title (as cited) | *AgentTrust: Runtime safety evaluation and interception for AI agent tool use* | Ch2 reference list L317 and Ch3 reference list L1054 |
| Full authors (as cited) | Yang, C. | Ch2 reference list L317 and Ch3 reference list L1054 |
| Year (as cited) | 2026 | Ch2 reference list L317 and Ch3 reference list L1054 |
| Venue (as cited) | (arXiv:2605.04785) [Preprint]. arXiv. | Ch2 reference list L317 and Ch3 reference list L1054 |
| DOI | None recorded (arXiv preprint) | — |
| arXiv ID | `2605.04785` | Chapter reference entry; Stage 1 reference master |
| Official publisher / record URL | https://arxiv.org/abs/2605.04785 | Chapter reference entry (arXiv record) |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (full HTML text)**
- **Basis:** Stage 1: "Full HTML text read".

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #42): §2.4.4 Integrated runtime layers (L63); §2.5 Stateful and Trajectory-Aware Protection (L77); §2.8 Detection and Classification Approaches (L114); §2.10 Runtime Decision and Mitigation (L132, L136); §2.11 Explainability and Auditability (L144); §2.13 Comparative Synthesis (L187)
- **Chapter 3** (reference #36): §3.7.6 Explainability and audit record (L506); §3.13 Contribution and Novelty Boundaries (L885, L887, L888)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-010** — **AgentTrust** (C. Yang, 2026) intercepts agent tool use through a pipeline of command normalization, pattern-based feature extraction, 170 configurable policy rules, analyzer-based risk scoring, session-based chain d… | Ch2 §2.4.4 L63 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-011** — Risk is aggregated by taking the maximum severity over the signals that fire, and the system returns one of four verdicts: allow, warn, block, or review. | Ch2 §2.4.4 L63 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-012** — Confidence is assigned by a step function of evidence strength rather than by probabilistic calibration. | Ch2 §2.4.4 L63 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-013** — The authors report component ablations with verdict accuracy, false-negative rate, and latency; a rule-only configuration reached 95.0% verdict accuracy and 73.7% risk-level accuracy at low-millisecond latency, and ve… | Ch2 §2.4.4 L63 | follows | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-014** — Reversibility is part of the labeling rubric. | Ch2 §2.4.4 L63 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-024** — AgentTrust's own ablation found that its session tracker had no measurable effect on either of its benchmarks (C. Yang, 2026), which suggests that single-action signals dominated the scenarios tested. | Ch2 §2.5 L77 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-037** — Rule- and pattern-based detectors, such as AgentTrust's regular-expression features and policies (C. Yang, 2026), are fast and inspectable but bounded by their rule coverage. | Ch2 §2.8 L114 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-048** — The reviewed systems turn evidence into action in several ways: by rule verdicts with maximum-severity aggregation (C. Yang, 2026), by thresholds on a predicted probability (H. Wang et al., 2025), by a rule cascade ga… | Ch2 §2.10 L132 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-053** — MI9 uses graduated containment (C. L. Wang et al., 2025); SafeAgent selects among sanitization, replanning, rollback, termination, argument rewriting, and human approval (H. Liu et al., 2026); AgentTrust distinguishes… | Ch2 §2.10 L136 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-057** — AgentTrust reports the rules that fired (C. Yang, 2026). | Ch2 §2.11 L144 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-066** — \| AgentTrust (C. Yang, 2026) \| Rules with maximum-severity aggregation \| — (heuristic confidence) \| ✓ (labeling rubric) \| ✓ \| — \| ✓ \| — \| | Ch2 §2.13 L187 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-069** — Consequence-dependent control appears in H.-H. Chen (2026), NEXUS, AgentTrust, and SafeAgent. | Ch2 §2.13 L191 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-070** — Human review appears in several systems, and latency and component ablation are reported by AgentTrust and NEXUS. | Ch2 §2.13 L191 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-077** — AgentTrust does not use a calibrated probability. | Ch2 §2.13 L193 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-079** — - **Relation to H.-H. Chen (2026), SafeAgent, and AgentTrust.** REM does not claim consequence-aware control, human escalation, or component ablation with latency as new. | Ch2 §2.15 L211 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-104** — Auditable decision records are provided by several existing systems (Hossain et al., 2026; C. Yang, 2026). | Ch3 §3.7.6 L506 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-117** — \| Runtime interception; human review; graduated response \| H. Liu et al. (2026); C. Yang (2026); C. L. Wang et al. (2025) \| | Ch3 §3.13 L885 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-119** — \| Consequence-aware and consequence-priced control \| H.-H. Chen (2026); Hossain et al. (2026); C. Yang (2026) \| | Ch3 §3.13 L887 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-120** — \| Component ablation with latency \| C. Yang (2026) \| | Ch3 §3.13 L888 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |

## What to read in the paper

**Reading mode:** Read completely.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **The interception pipeline and its 170 policy rules.** N033 (Stage 1: verified).
- **Risk aggregation, the four verdicts, and confidence assignment.** Ch2 L63 (maximum severity; allow/warn/block/review; step-function confidence). No claim-level audit record.
- **The component ablations and latency.** N034–N037 (95.0%, 73.7%, 96.7%, 630 scenarios; Stage 1: verified).
- **The session-tracker ablation.** Ch2 L77 says it had "no measurable effect". No claim-level audit record.
- **The labeling rubric (reversibility).** Ch2 L63. No claim-level audit record.

## Why this paper matters for understanding REM

This is prior art for interception, verdicts that include review, auditable rule output, and component ablation with latency, all of which Chapter 3 says REM does not claim as new. Its ablation finding that session tracking had no measurable effect is cited in Chapter 2 §2.5.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
