# PAPER_06 — SafeAgent: A runtime protection architecture for agentic systems

**Category:** B. Prior-art / competing approaches · **Stage 1 Ref ID:** REF-032 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 06 | This pack |
| Exact title (as cited) | *SafeAgent: A runtime protection architecture for agentic systems* | Ch2 reference list L283 and Ch3 reference list L1028 |
| Full authors (as cited) | Liu, H., Ilyushin, E., Ni, J., & Zhu, M. | Ch2 reference list L283 and Ch3 reference list L1028 |
| Year (as cited) | 2026 | Ch2 reference list L283 and Ch3 reference list L1028 |
| Venue (as cited) | (arXiv:2604.17562) [Preprint]. arXiv. | Ch2 reference list L283 and Ch3 reference list L1028 |
| DOI | None recorded (arXiv preprint) | — |
| arXiv ID | `2604.17562` | Chapter reference entry; Stage 1 reference master |
| Official publisher / record URL | https://arxiv.org/abs/2604.17562 | Chapter reference entry (arXiv record) |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (full HTML text)**
- **Basis:** Stage 1: "Full HTML text read".

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #25): §2.4.4 Integrated runtime layers (L61); §2.5 Stateful and Trajectory-Aware Protection (L73); §2.10 Runtime Decision and Mitigation (L132, L136); §2.13 Comparative Synthesis (L186)
- **Chapter 3** (reference #23): §3.13 Contribution and Novelty Boundaries (L885)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-004** — **SafeAgent** (H. Liu et al., 2026) consists of a runtime controller that mediates actions in the agent loop and a context-aware decision core over persistent session state. | Ch2 §2.4.4 L61 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-005** — The core's operators for risk encoding, advantage–cost modeling, consequence simulation, and policy arbitration are realized through LLM reasoning rather than formal equations. | Ch2 §2.4.4 L61 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-006** — The action space includes context sanitization, replanning, rollback, session termination, tool-argument rewriting, and human approval. | Ch2 §2.4.4 L61 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-007** — SafeAgent was evaluated on ASB and InjecAgent using attack success rate and performance under no attack. | Ch2 §2.4.4 L61 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-008** — Its ablations show that a policy-weighting setting moves the system between safety-first and task-first operating points. | Ch2 §2.4.4 L61 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-009** — The paper does not address probability calibration and does not report latency, which its authors acknowledge as a limitation in terms of computational overhead. | Ch2 §2.4.4 L61 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-023** — SafeAgent treats security as a stateful decision problem over evolving interaction trajectories (H. Liu et al., 2026). | Ch2 §2.5 L73 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-048** — The reviewed systems turn evidence into action in several ways: by rule verdicts with maximum-severity aggregation (C. Yang, 2026), by thresholds on a predicted probability (H. Wang et al., 2025), by a rule cascade ga… | Ch2 §2.10 L132 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-053** — MI9 uses graduated containment (C. L. Wang et al., 2025); SafeAgent selects among sanitization, replanning, rollback, termination, argument rewriting, and human approval (H. Liu et al., 2026); AgentTrust distinguishes… | Ch2 §2.10 L136 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-054** — The second is how effective each intervention actually is: SafeAgent's ablations and the intervention-advantage argument of C. Zhang et al. (2026) both indicate that the value of an intervention depends on what it ach… | Ch2 §2.10 L138 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-065** — \| SafeAgent (H. Liu et al., 2026) \| LLM-based operators and policy arbitration \| — \| ✓ (LLM consequence simulation) \| ✓ \| ✓ \| — \| — \| | Ch2 §2.13 L186 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-069** — Consequence-dependent control appears in H.-H. Chen (2026), NEXUS, AgentTrust, and SafeAgent. | Ch2 §2.13 L191 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-076** — SafeAgent reasons about consequences through an LLM and does not report calibration or latency. | Ch2 §2.13 L193 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-079** — - **Relation to H.-H. Chen (2026), SafeAgent, and AgentTrust.** REM does not claim consequence-aware control, human escalation, or component ablation with latency as new. | Ch2 §2.15 L211 | named | NOT AUDITED AT CLAIM LEVEL |
| **CM-117** — \| Runtime interception; human review; graduated response \| H. Liu et al. (2026); C. Yang (2026); C. L. Wang et al. (2025) \| | Ch3 §3.13 L885 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |

## What to read in the paper

**Reading mode:** Read completely.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **The architecture: runtime controller and decision core.** Ch2 L61 and L73.
- **The operators (risk encoding, advantage–cost modeling, consequence simulation, policy arbitration) and whether they are LLM-realized.** Ch2 L61 says they are "realized through LLM reasoning rather than formal equations". No claim-level audit record.
- **The action space.** Ch2 L61 and L136 list six actions. No claim-level audit record.
- **Experiments and ablations (ASB, InjecAgent, policy weighting).** Ch2 L61 and L138. No claim-level audit record.
- **Limitations.** Ch2 L61 and L193 say the paper reports neither calibration nor latency. No claim-level audit record.

## Why this paper matters for understanding REM

Chapter 2 cites it for stateful decisions over session history and graduated recovery. Chapter 3 lists it as prior art for runtime interception, human review and graduated response.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
