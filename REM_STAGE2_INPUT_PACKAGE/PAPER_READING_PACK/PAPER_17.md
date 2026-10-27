# PAPER_17 — AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents

**Category:** D. Financial-agent evaluation · **Stage 1 Ref ID:** REF-014 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 17 | This pack |
| Exact title (as cited) | *AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents* | Ch2 reference list L255 and Ch3 reference list L1002 |
| Full authors (as cited) | Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. | Ch2 reference list L255 and Ch3 reference list L1002 |
| Year (as cited) | 2024 | Ch2 reference list L255 and Ch3 reference list L1002 |
| Venue (as cited) | (arXiv:2406.13352). arXiv. | Ch2 reference list L255 and Ch3 reference list L1002 |
| DOI | None recorded | — |
| arXiv ID | `2406.13352` | Chapter reference entry; Stage 1 reference master |
| Official publisher / record URL | https://arxiv.org/abs/2406.13352 | Chapter reference entry (arXiv record). `STAGE2_FINAL_ALGORITHM_MATHEMATICAL_DECISION_REPORT.md` names the venue as NeurIPS 2024 Datasets & Benchmarks; the chapter entry does not, and Stage 1 did not verify it. |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED (benchmark source code inspected separately)**
- **Basis:** Stage 1: "arXiv abstract; banking suite read in the public repository". Stage 2: agentdojo 0.1.35 package source from PyPI inspected (16 user tasks, 9 injection tasks, 11 tools, 144 combinations).

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #11): §2.3 Prompt Injection and Indirect Prompt Injection (L33); §2.12 Evaluation Benchmarks and Datasets (L156)
- **Chapter 3** (reference #10): §3.3.1 Protected system (L168); §3.11.1 Environment and instrumentation (L645)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-002** — AgentDojo (Debenedetti et al., 2024) provides 97 realistic tasks and 629 security test cases across environments that include e-banking, and it measures both utility and security. | Ch2 §2.3 L33 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-003** — Its authors report that current models fail many tasks even without attacks and that existing attacks break some security properties but not all. | Ch2 §2.3 L33 | follows | NOT AUDITED AT CLAIM LEVEL |
| **CM-059** — \| AgentDojo (Debenedetti et al., 2024) \| 97 tasks and 629 security test cases across environments including e-banking; extensible to new tasks, defenses, and adaptive attacks \| Yes \| Open source; security and util… | Ch2 §2.12 L156 | table row | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-081** — The evaluation instance is an agent operating the AgentDojo banking environment (Debenedetti et al., 2024), described in Section 3.11.2. | Ch3 §3.3.1 L168 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-106** — REM is evaluated in the banking environment of AgentDojo (Debenedetti et al., 2024), an open-source framework that evaluates both the utility and the security of LLM agents. | Ch3 §3.11.1 L645 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-107** — Security is determined by checks on the environment state before and after an episode, and utility by task-specific checks. | Ch3 §3.11.1 L645 | follows | NOT AUDITED AT CLAIM LEVEL |

## What to read in the paper

**Reading mode:** Targeted reading.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **Abstract.** 97 tasks and 629 security test cases (N015, N016, N055, N056; Stage 1: verified at abstract level).
- **How utility and security are evaluated (checks on environment state).** Ch3 L645. The follow-on sentence has no claim-level audit record.
- **The banking suite description and any versioning discussion.** OI-14: the benchmark version is not pinned, and task content differs between versions.
- **Results on current models without attacks.** Ch2 L33 ("fail many tasks even without attacks"). No claim-level audit record.

## Why this paper matters for understanding REM

REM is evaluated in its banking suite (Ch3 §3.3.1, §3.11.1), and the task, tool and combination counts in Chapter 3 come from it. The paper describes the benchmark; the exact benchmark version used remains open (OI-14).

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
