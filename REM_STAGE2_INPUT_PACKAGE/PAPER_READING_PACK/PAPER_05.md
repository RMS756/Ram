# PAPER_05 — NEXUS: Structured runtime safety for tool-using LLM agents

**Category:** B. Prior-art / competing approaches · **Stage 1 Ref ID:** REF-023 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 05 | This pack |
| Exact title (as cited) | *NEXUS: Structured runtime safety for tool-using LLM agents* | Ch2 reference list L267 and Ch3 reference list L1018 |
| Full authors (as cited) | Hossain, E., Nipu, M. M. H., Ornee, T. N., Rana, R., & Yousefi, N. | Ch2 reference list L267 and Ch3 reference list L1018 |
| Year (as cited) | 2026 | Ch2 reference list L267 and Ch3 reference list L1018 |
| Venue (as cited) | (arXiv:2607.19356) [Preprint]. arXiv. | Ch2 reference list L267 and Ch3 reference list L1018 |
| DOI | None recorded. Stage 2: Crossref has no registration for `10.48550/arXiv.2607.19356`. | Stage 2 Crossref check |
| arXiv ID | `2607.19356` | Chapter reference entry; Stage 1 reference master; Stage 2 index records |
| Official publisher / record URL | https://arxiv.org/abs/2607.19356 | Chapter reference entry (arXiv record) |
| Other recorded URL | https://arxiv.org/html/2607.19356 — arXiv HTML full-text rendering, recorded in `V1_NEXUS_DIRECT_VERIFICATION.md` as blocked in this environment | Repository records named in the value |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** PARTIALLY VERIFIED
- **Depth of reading:** **SOURCE TEXT READ IN STAGE 1 (full HTML) — not reproducible in this environment. METADATA CONFLICT: arXiv ID vs submission date. Four figures UNVERIFIED.**
- **Basis:** Stage 1 reference master: "Full HTML text read; arXiv identifier (2607) conflicts with the stated 25 May 2026 submission date". Stage 1 numerical audit: N038–N040 and N067 "Figure Read in Source? No". Stage 2: title, authors and ID confirmed in index records; full text unreachable.
- **Record conflict:** `V1_NEXUS_DIRECT_VERIFICATION.md` records V-1 as UNRESOLVED. It was written before the Stage 1 records were in the repository. Stage 1 claim audit rows Ch2-C024 and Ch2-C028 record the rule-cascade and expected-loss-objective sentences as supported ("content read in full").

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #17): §2.4.4 Integrated runtime layers (L65); §2.9 Probability Calibration (L126); §2.10 Runtime Decision and Mitigation (L132, L134, L136); §2.11 Explainability and Auditability (L144); §2.12 Evaluation Benchmarks and Datasets (L161); §2.13 Comparative Synthesis (L185)
- **Chapter 3** (reference #18): §3.7.2 Calibration on the logit (L356); §3.7.6 Explainability and audit record (L506); §3.13 Contribution and Novelty Boundaries (L883, L887)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-015** — **NEXUS** (Hossain et al., 2026) evaluates the plan an agent proposes before execution. | Ch2 §2.4.4 L65 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |
| **CM-016** — It combines deterministic safety rules, argument-level inspection, and a logistic-regression risk score over 99 plan features, including an irreversibility indicator and estimated cost. | Ch2 §2.4.4 L65 | follows | UNVERIFIED — figure not read in source |
| **CM-017** — The score is calibrated by Platt scaling, with isotonic regression also evaluated. | Ch2 §2.4.4 L65 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-018** — On a 128-instance held-out test set the expected calibration error fell from 0.085 for the raw model to 0.013 after Platt scaling, using a 60-instance calibration split. | Ch2 §2.4.4 L65 | follows | UNVERIFIED — figure not read in source |
| **CM-019** — The deployed policy selects among four interventions (allow, block, request confirmation, or request revision) through a rule cascade in which the calibrated score gates certain cases. | Ch2 §2.4.4 L65 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-020** — The paper also defines an expected-loss objective with fixed costs for each intervention. | Ch2 §2.4.4 L65 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-021** — The authors report a median decision latency of 0.205 ms and caution that results on their author-generated templates should be read as upper bounds rather than deployment estimates. | Ch2 §2.4.4 L65 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-043** — NEXUS calibrates its logistic-regression risk score with Platt scaling and reports ECE and Brier scores with a reliability diagram (Hossain et al., 2026). | Ch2 §2.9 L126 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |
| **CM-048** — The reviewed systems turn evidence into action in several ways: by rule verdicts with maximum-severity aggregation (C. Yang, 2026), by thresholds on a predicted probability (H. Wang et al., 2025), by a rule cascade ga… | Ch2 §2.10 L132 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |
| **CM-051** — NEXUS defines an expected-loss objective with fixed costs for allow, revise, confirm, and block (Hossain et al., 2026). | Ch2 §2.10 L134 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |
| **CM-052** — Its deployed policy, however, is a rule cascade in which the learned score adjudicates particular cases, not a per-decision minimization of conditional risk. | Ch2 §2.10 L134 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-053** — MI9 uses graduated containment (C. L. Wang et al., 2025); SafeAgent selects among sanitization, replanning, rollback, termination, argument rewriting, and human approval (H. Liu et al., 2026); AgentTrust distinguishes… | Ch2 §2.10 L136 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |
| **CM-056** — NEXUS traces each decision to a named rule, an argument-inspector finding, or a calibrated threshold crossing (Hossain et al., 2026). | Ch2 §2.11 L144 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |
| **CM-060** — \| NEXUS-Bench (Hossain et al., 2026) \| 300/63/128 train/validation/test synthetic instances and further splits \| — \| Author-generated templates; results described by the authors as upper bounds \| | Ch2 §2.12 L161 | table row | UNVERIFIED — figure not read in source |
| **CM-064** — \| NEXUS (Hossain et al., 2026) \| Rules, argument inspection, calibrated logistic score in a cascade \| ✓ \| ✓ \| ✓ \| ✓ (paired benign cases) \| ✓ \| — \| | Ch2 §2.13 L185 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |
| **CM-068** — Calibrated logistic risk scoring and a four-way intervention set appear in NEXUS. | Ch2 §2.13 L191 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-069** — Consequence-dependent control appears in H.-H. Chen (2026), NEXUS, AgentTrust, and SafeAgent. | Ch2 §2.13 L191 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-070** — Human review appears in several systems, and latency and component ablation are reported by AgentTrust and NEXUS. | Ch2 §2.13 L191 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-073** — NEXUS evaluates plans on author-generated templates and combines its calibrated score with rules through a cascade. | Ch2 §2.13 L193 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-094** — Calibrated logistic risk scores are already used in agent safety (Hossain et al., 2026). | Ch3 §3.7.2 L356 | cited | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |
| **CM-104** — Auditable decision records are provided by several existing systems (Hossain et al., 2026; C. Yang, 2026). | Ch3 §3.7.6 L506 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-115** — \| Calibrated logistic risk scores for agent safety; four-way intervention \| Hossain et al. (2026) \| | Ch3 §3.13 L883 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |
| **CM-119** — \| Consequence-aware and consequence-priced control \| H.-H. Chen (2026); Hossain et al. (2026); C. Yang (2026) \| | Ch3 §3.13 L887 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) · reference metadata conflict (OI-06) |

## What to read in the paper

**Reading mode:** Read completely.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **The risk scorer and its features.** N038 ("99 plan features") is UNVERIFIED (OI-02).
- **The calibration setup and results.** N039 and N040 (ECE 0.085 → 0.013, 128-instance test set, 60-instance calibration split) are UNVERIFIED (OI-03, OI-04). Ch2 L65 also says isotonic regression was evaluated; that has no claim-level audit record.
- **The definition of the expected-loss objective, and the specification of the deployed intervention policy.** OI-01 (V-1). Chapter 2 says NEXUS defines an expected-loss objective, but that its deployed policy is a score-gated rule cascade and "not a per-decision minimization of conditional risk". This is the point on which Chapter 2 separates REM from NEXUS.
- **How decisions are traced for audit.** Ch2-C031 (Stage 1: supported).
- **Benchmark construction and splits.** N067 (300/63/128) is recorded both as supported (Ch2-C039) and as UNVERIFIED (N067) in different Stage 1 workbooks (OI-05).
- **Latency, and the authors' caveat on upper bounds.** The 0.205 ms median latency (Ch2 L65) has no claim-level or numerical audit record.
- **Front matter and version history.** OI-06: the identifier 2607 conflicts with the stated 25 May 2026 submission date.

## Why this paper matters for understanding REM

This is the prior system closest to REM. It combines rules, argument inspection, a Platt-calibrated logistic risk score, four interventions and a defined expected-loss objective, and REM concedes several of these elements. Chapter 2 separates REM from it on one point: NEXUS's deployed policy is a score-gated rule cascade, not a per-decision minimization of conditional risk. That point cannot be re-checked in this environment (OI-01), and four of the figures quoted from it are unverified (OI-02 to OI-05).

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
