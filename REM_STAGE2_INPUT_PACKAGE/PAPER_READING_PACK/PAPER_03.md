# PAPER_03 — Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection

**Category:** A. Foundations · **Stage 1 Ref ID:** REF-019 · **Read-only reading note.** Nothing in the thesis was changed.

## Bibliographic record

| Field | Value | Source of this field |
| --- | --- | --- |
| Paper number | 03 | This pack |
| Exact title (as cited) | *Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection* | Ch2 reference list L261 and Ch3 reference list L1010 |
| Full authors (as cited) | Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. | Ch2 reference list L261 and Ch3 reference list L1010 |
| Year (as cited) | 2023 | Ch2 reference list L261 and Ch3 reference list L1010 |
| Venue (as cited) | In *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security* (pp. 79–90). ACM. | Ch2 reference list L261 and Ch3 reference list L1010 |
| Pages | 79–90 | Chapter reference entry; Stage 1 metadata check |
| DOI | `10.1145/3605764.3623985` | Chapter reference entry; Crossref metadata confirmed in Stage 1 (reference master) |
| arXiv ID | Not recorded in the repository. Stage 1 read "an arXiv abstract", but its identifier was not recorded. | — |
| Official publisher / record URL | https://doi.org/10.1145/3605764.3623985 | Chapter reference entry (DOI resolver link) |
| Official PDF URL | Not recorded in any verification record | Search of all repository documents |
| Local copy | **PDF NOT LOCALLY AVAILABLE** | Repository search: no PDF of any cited paper is stored |

## Verification status

- **Reference status (THESIS_READING_INDEX.md):** VERIFIED
- **Depth of reading:** **ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED**
- **Basis:** Stage 1: "Crossref metadata and arXiv abstract".

## Where the thesis uses it

**Used in:** Both chapters.

- **Chapter 2** (reference #14): §2.3 Prompt Injection and Indirect Prompt Injection (L31)
- **Chapter 3** (reference #14): §3.1.5 Assumptions (L77); §3.3.3 Trust boundaries and untrusted content (L185)

Line numbers refer to `working/Chapter2_working.md` and `working/Chapter3_working.md`.

## Thesis claims that depend on it

Every sentence in the chapters that cites this paper, or continues a paragraph about it, with the audit record for that specific claim. **"NOT AUDITED AT CLAIM LEVEL" means no audit record checks that sentence against the paper.** It is not a finding that the paper does not support it. Full records are in `CLAIM_TO_PAPER_MAP.md`.

| Claim | Ch · § · line | Link | Status for this paper |
| --- | --- | --- | --- |
| **CM-001** — Greshake et al. (2023) demonstrated that adversarial instructions placed in data that an LLM-integrated application retrieves can compromise the application remotely, without direct access to its interface. | Ch2 §2.3 L31 | cited | NOT AUDITED AT CLAIM LEVEL |
| **CM-080** — \| AS-5 \| Tool outputs and retrieved content are untrusted by default. \| Scoping \| Follows from the indirect injection threat (Greshake et al., 2023) \| | Ch3 §3.1.5 L77 | table row | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |
| **CM-082** — The observation boundary matters because content arriving there enters after the user's request, which is the route exploited by indirect prompt injection (Greshake et al., 2023; OWASP Gen AI Security Project, 2025). | Ch3 §3.3.3 L185 | cited | SUPPORTED IN STAGE 1 RECORD — ABSTRACT/METADATA VERIFIED — FULL TEXT NOT VERIFIED |

## What to read in the paper

**Reading mode:** Read completely.

Section and page numbers are given **only where a Stage 1 or Stage 2 record documents them**. Anything else is described by content, because the paper's own section numbering is not recorded.

- **Abstract.** Stage 1 verified the chapter claims at this level.
- **The attack demonstrations (method and experiments).** Ch2 §2.3 cites the demonstration that instructions hidden in retrieved data can compromise an application remotely. Ch3 §3.1.5 (AS-5) and §3.3.3 build REM's scope and its observation trust boundary on it.
- **Whole paper, pp. 79–90.** This paper defines the threat REM is scoped to.

## Why this paper matters for understanding REM

This paper defines the threat REM is scoped to. Chapter 3 grounds its scoping assumption (§3.1.5) and the observation trust boundary (§3.3.3) in the indirect-injection attack it demonstrates.

## Retrieval

**PDF NOT LOCALLY AVAILABLE.** Retrieve it manually from the official record above. This working environment blocks arXiv, publisher and author-hosted domains, so the files here could not be downloaded.
