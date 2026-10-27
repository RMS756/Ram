# PAPER_09 — Calibration is not control: Why LLM-agent oversight needs intervention

**Category:** B. Prior-art / competing approaches · **Stage 1 Ref ID:** REF-058 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 09 | This pack |
| Exact title (as cited) | *Calibration is not control: Why LLM-agent oversight needs intervention* | Ch2 reference list L325 and Ch3 reference list L1056 |
| Full authors (as cited) | Zhang, C., Wan, Z., Yu, X., Wu, J., Wen, Q., Zhou, P., Zhao, W., & Tsang, I. | Ch2 reference list L325 and Ch3 reference list L1056 |
| Year (as cited) | 2026 | Ch2 reference list L325 and Ch3 reference list L1056 |
| Venue (as cited) | (arXiv:2606.21399) [Preprint]. arXiv. | Ch2 reference list L325 and Ch3 reference list L1056 |
| DOI | None recorded (arXiv preprint) | — |
| arXiv ID | `2606.21399` | Chapter reference entry; Stage 1 reference master |
| Official publisher / record URL | https://arxiv.org/abs/2606.21399 | Chapter reference entry (arXiv record) |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **SOURCE TEXT READ IN STAGE 1 — not reproducible in this environment (full HTML text)**
- **Basis:** Stage 1: "Full HTML text read".

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #46): §2.9 Probability Calibration (L126); §2.10 Runtime Decision and Mitigation (L132, L138); §2.13 Comparative Synthesis (L188, L191); §2.15 Positioning of REM (L210)
- **Chapter 3** (reference #37): §3.7.2 Calibration on the logit (L357); §3.7.7 Consequence-independent baseline policy (L525); §3.13 Contribution and Novelty Boundaries (L884); §3.14 Threats to Validity (L936)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-044** — C. Zhang et al. (2026) argue that oversight based on a scalar risk score routed through a threshold targets the wrong quantity: what matters for control is the *intervention advantage*, the expected utility gain from … | Ch2 §2.9 L126 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-045** — Two trajectory states can share a risk estimate while differing in whether they are recoverable. | Ch2 §2.9 L126 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-046** — In their experiments on ALFWorld, Platt scaling reduced the ECE of a confidence score from 0.463 to 0.006 while control regret under threshold routing remained unchanged at 0.318. | Ch2 §2.9 L126 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-047** — They propose an action-conditioned controller trained by replaying the agent from identical decision states and executing alternative actions. | Ch2 §2.9 L126 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-048** — The reviewed systems turn evidence into action in several ways: by rule verdicts with maximum-severity aggregation (C. Yang, 2026), by thresholds on a predicted probability (H. Wang et al., 2025), by a rule cascade ga… | Ch2 §2.10 L132 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-054** — The second is how effective each intervention actually is: SafeAgent's ablations and the intervention-advantage argument of C. Zhang et al. (2026) both indicate that the value of an intervention depends on what it ach… | Ch2 §2.10 L138 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-067** — \| C. Zhang et al. (2026) \| Action-conditioned intervention value \| Analyzed \| — \| — \| Regret \| — \| — \| | Ch2 §2.13 L188 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-072** — The limits of calibration for control are established by C. Zhang et al. (2026). | Ch2 §2.13 L191 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-078** — - **Relation to C. Zhang et al. (2026).** REM does not claim that calibration improves control. It reports calibration quality and control outcomes separately, and it acknowledges that a scalar probability cannot repr… | Ch2 §2.15 L210 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-095** — C. Zhang et al. (2026) show that recalibrating a scalar risk score can improve calibration error while leaving control regret under threshold routing unchanged, because a scalar probability does not represent whether … | Ch3 §3.7.2 L357 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-105** — This contrast is used in the ablation of Section 3.11.7 and is consistent with the finding of C. Zhang et al. (2026) that recalibration need not change threshold-routed control. | Ch3 §3.7.7 L525 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-116** — \| Distinction between calibration and control \| C. Zhang et al. (2026) \| | Ch3 §3.13 L884 | table row | SUPPORTED IN STAGE 1 RECORD — source text read in Stage 1 (not reproducible in this environment) |
| **CM-122** — A scalar probability cannot represent whether an adversarial trajectory remains recoverable, so REM inherits the limitation identified by C. Zhang et al. (2026); estimating intervention value by counterfactual replay … | Ch3 §3.14 L936 | cited | NOT AUDITED AT CLAIM LEVEL |

## What to read in the paper

**Reading mode:** Read completely.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **The argument that threshold routing of a scalar risk score targets the wrong quantity (intervention advantage).** Ch2 L126 and Ch3 L357. Both chapters concede this point. No claim-level audit record apart from the comparative-table row (Ch2-C052) and the novelty-boundary row (Ch3-C037).
- **The ALFWorld experiment.** Ch2 L126 quotes ECE 0.463 → 0.006 with control regret unchanged at 0.318. **None of these figures appears in the Stage 1 numerical audit.**
- **The action-conditioned controller trained by replay.** Ch2 L126. REM excludes counterfactual replay from scope (Ch3 L936).

## Why this paper matters for understanding REM

Both chapters concede its central point: recalibrating a scalar risk score need not improve threshold-routed control. REM states it inherits this limitation (Ch3 §3.14). The argument has to be understood to understand what REM does not claim.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
