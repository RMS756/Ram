"""Tenth (DiD) edition of the thesis: copies the defence-ready sources UNCHANGED and inserts dated, clearly marked
sections on the exploratory Defense-in-Depth work of 27 November 2026. Every number comes from
REM_DEFENSE_IN_DEPTH/results/*.json (verified by tools/check_did_numbers.py). The defence-ready edition is not modified.

usage: python3 REM_DID_THESIS_EDITION/tools/make_did_edition.py && python3 REM_DID_THESIS_EDITION/tools/build_r9.py
"""
import os
import shutil

TOOLS = os.path.dirname(os.path.abspath(__file__))
ED = os.path.abspath(os.path.join(TOOLS, ".."))
ROOT = os.path.abspath(os.path.join(ED, ".."))
SRC0 = os.path.join(ROOT, "REM_DEFENCE_READY_THESIS")
for sub in ("src", "text_front", "references"):
    shutil.rmtree(os.path.join(ED, sub), ignore_errors=True)
    shutil.copytree(os.path.join(SRC0, sub), os.path.join(ED, sub))


def edit(rel, old, new, count=1):
    p = os.path.join(ED, rel)
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == count, (rel, old[:60], s.count(old))
    open(p, "w", encoding="utf-8").write(s.replace(old, new))


MARK = "*[Tenth edition, 27 November 2026: exploratory; outside the frozen design; supervisor decision required before adoption.]*"

# ---------------------------------------------------------------- Chapter 2
CH2 = """### 2.11.6 Update of 27 November 2026: Defense-in-Depth and Authorization Prior Art (Outside the PRISMA Flow)

""" + MARK + """

A focused search for Defense-in-Depth (DiD) and runtime authorization work was made on 27 November 2026. Full texts could not be opened from the working environment (arXiv and its mirrors were refused by the network policy), so every statement below is at abstract level unless the authors' code was read. The CaMeL repository was read at commit `f083b6b`, and the Agent Security Bench (ASB) repository at commit `544540f`.

**Table 2.6. Works bearing on Defense-in-Depth for financial agents (A = abstract; R = authors' code read; C = Crossref record)**

| Work | Level | Mechanism relevant to REM | Statement most relevant to this thesis |
|---|---|---|---|
| CaMeL (Debenedetti et al., 2025; preprint) | R | Values carry sources; a state-changing call is checked by a deterministic policy per tool | The banking policy requires only the **recipient** to originate from the user; amount, subject and date need only be readable by the recipient. Publication at SaTML 2026 could not be confirmed |
| RTBAS (Zhong et al., 2025; preprint) | A | Information-flow labels and dependency screeners; user confirmation when integrity cannot be established | Financial transactions are a motivation; banking-specific results were not determined |
| AgentCap (Kabbinamakki Suresh & Gao, 2026; preprint) | A | Intent-declared requests; short-lived, budget-bounded capability tokens validated at the tool boundary; provenance of sensitive arguments | Zero attack success with one model on AgentDojo and InjecAgent; ablations not determined |
| AIS (Gong et al., 2026; *Systems*) | C, A | A typed financial action intent is checked against mandate, policy, state, approvals and exact economic terms before single-use authority is issued | Mechanism ablations on 36 attack fixtures; only 6 of 16 legitimate requests were authorized with two small models |
| AGATE (X. Zhang et al., 2026; preprint) | A | Grants bound to exact parameters that expire and allow limited uses; an effect ledger for repeated requests | Reports a bypass through parameter rewriting |
| Agent-Sentry (Sequeira et al., 2026; preprint) | A | Three complementary checks: a sequence classifier, an allow-list and an LLM judge | Per-layer contribution not determined |
| ScopeGate (Mellafe Zuvic, 2026; preprint) | A | Per-call authorization with a money ceiling and idempotency | A payment-toolkit case |
| Narisetty et al. (2026; preprint) | A | Adaptive evaluation of out-of-band defenses | Out-of-band defenses are validated only on static attacks; one small adaptive test of Progent |
| AgentSandbox (K. Zhang et al., 2025; preprint) | A | Argues that DiD, least privilege and complete mediation should be applied to agents | Position paper |

**Benchmark compatibility.** ASB's financial scenario uses simulated tools without arguments. Attack success means calling an attacker tool by name, so argument-level controls (recipient, amount, provenance) cannot be exercised on it.

**What this update changes.**
- Runtime authorization with capability-style permits, parameter-bound one-time approvals and deterministic financial constraints is published (AIS, AGATE, AgentCap, ScopeGate). DiD is advocated for agents (AgentSandbox).
- These mechanisms are therefore not presented as contributions of this thesis.
- What was not found, at the level read, is a measurement of how much protection remains when one control is evaded while the others stay in place, as distinct from removing it. Section 4.6.12 reports such a measurement for REM. The statement is bounded by the abstract-level reading.
"""
edit("src/CHAPTER_02_FINAL.md", "\n## 2.12 Chapter Summary", "\n" + CH2 + "\n## 2.12 Chapter Summary")

# ---------------------------------------------------------------- Chapter 3
CH3 = """## 3.15 Exploratory Extension: REM-DiD, a Defense-in-Depth Candidate (Proposed, Not Adopted)

""" + MARK + """

**REM-DiD** keeps the five layers. It gives each layer a separate security question and adds controls inside the layers. Its code is isolated in `REM_DEFENSE_IN_DEPTH/remdid/`; REM v1.0 (`rem/`) is unchanged and runs inside REM-DiD as its learned decision. Figure 3.5 marks what is implemented and evaluated.

![Figure 3.5. REM-DiD as implemented. Exactly five layers; audit, monitoring and offline fitting are cross-cutting. Solid boxes: implemented, unit-tested and evaluated in replay; dotted: implemented and tested only; dashed: proposed, not implemented.](REM_DEFENSE_IN_DEPTH/figures/fig_rem_did_implemented.png){width=100%}

**Table 3.16. REM-DiD controls by layer**

| Layer | Question | Controls added |
|---|---|---|
| Input & Context | Where did a value come from? What did the user authorize? | Field-level provenance of tool outputs (free-text fields untrusted, typed bank fields trusted); canonical identifiers and amounts; inferred lineage of each sensitive argument. Trusted Authorization Envelope (TAE): operation and pinned, unspecified or wildcard fields; integrity code; session binding; expiry; limited uses; cumulative amount budget |
| Detection | Is instruction-like content present, and is it linked to this call? | Role and delimiter, override and financial-directive signals beside x~ctx2~. Call-linked evidence: the call's value occurs in an untrusted segment on which a signal fired. Unavailable detectors are reported as unavailable, never as "not fired" |
| Behavioral Analysis | Does the sequence look like an attack? | First-time payee, standing-order redirect, repeated transfer, retry after a withheld call, tool switching after a withheld call |
| Decision Engine | Authorized? Evidence? Consequence? Intervention? | 4A: deterministic, non-compensatory authorization (violation or missing entry → Block; unspecified field → Escalate). 4B: REM v1.0's expected-loss verdict, unchanged. The most restrictive outcome wins, so a low probability cannot override a denial. Evidence rules act only on values that a verified TAE entry does not pin |
| Mitigation | Is exactly the decided call executed? | Permits bound to session, tool and canonical arguments, single use, re-validated immediately before execution; the gateway fails closed |

**What is not done.**
- No sixth layer, and no model in the decision path.
- No Modify mechanism: a Modify verdict still withholds the call.
- The TAE's trusted issuer is not available in the benchmark. The evaluation therefore uses offline oracles:
  - *oracle*: every ground-truth parameter pinned, an upper bound;
  - *explicit*: a parameter is pinned only if the user stated it;
  - *broad*: every parameter a wildcard, used to model a bypassed authorization.
- Natural-language compilation of the request was not used, because earlier studies found it unreliable (Section 4.5.8).

**Evaluation design (protocol committed before the run).** Recorded-trace replay (Section 3.11.9) of the primary population was used for:
- individual and combined controls;
- authorization bypassed by a broad TAE, with modelled evasion of one or more further controls;
- real bypasses (a reformatted identifier; a paraphrased injection);
- injected component failures under fail-safe defaults, with fail-open counterfactuals.

Clustered sign-flip permutation tests with Holm correction were used throughout. All of it is **exploratory**, because the recordings had been analyzed before.
"""
edit("src/CHAPTER_03_FINAL.md", "\n## 3.15 Chapter Summary", "\n" + CH3 + "\n## 3.16 Chapter Summary")

# ---------------------------------------------------------------- Chapter 4
CH4 = """### 4.6.12 Exploratory Defense-in-Depth Evaluation (27 November 2026)

""" + MARK + """

**Evasion of REM v1.0's own controls.**
- Suppressing any single evidence feature on attack-labeled calls did not increase successful attacks.
- Suppressing a whole family did:
  - behavioral family: 11 → 131 attacks;
  - action-provenance family: 11 → 90 attacks;
  - both: 669 of 2,979.
- Refitting without the behavioral family (REM v1.1) left security unchanged (11) and completed 35 more benign tasks. Under evasion of the action family, however, REM v1.1 let 653 attacks through.
- **Removing a control and evading it can therefore give opposite assessments.**

**Detection.**
- REM v1.0's pattern detector reached recall 0 on two of six templates.
- The new role, override and financial-directive signals are highly correlated with it (phi 0.92–0.98).
- Under a declared paraphrase, only the financial-directive signal still fired. It fired on 19 of 81 legitimate document segments.
- Under zero-width obfuscation, every signal failed (recall at most 0.0055).

**Table 4.60. REM-DiD controls alone and combined (primary population; replay; oracle TAE where marked)**

| Arm | Successful attacks (of 2,979) | Benign tasks (of 334) | Legitimate state-changing calls withheld (of 1,644) |
|---|---:|---:|---:|
| No defense | 672 | 175 | 0 |
| REM v1.0 | 11 | 105 | 1,305 |
| Authorization only (oracle) | 0 | 173 | 774 |
| Authorization only (explicit parameters) | 0 | 122 | 1,432 |
| Provenance only | 13 | 147 | 250 |
| Detection only | 7 | 164 | 159 |
| Behavioral rules only | 120 | 161 | 155 |
| Detection + behavioral | 1 | 161 | 282 |
| Full REM-DiD | 0 | 105 | 1,508 |
| Full REM-DiD without the learned decision | 0 | 173 | 774 |
| Full REM-DiD, learned decision only for unpinned calls | 0 | 172 | 798 |

**The learned decision behind authorization.**
- Behind oracle authorization, the learned decision adds no security (0 vs 0 attacks) and costs 68 benign tasks. The sign-flip p is 0.014, which is not significant after Holm correction over 15 contrasts.
- The same holds in all 36 cells of the declared cost grid:
  - 0 attacks in every cell;
  - at most 124 benign tasks, against 173 without the learned decision.

**Table 4.61. Authorization bypassed (broad TAE): residual protection of the remaining controls**

| Remaining controls | Successful attacks (of 2,979) |
|---|---:|
| None | 174 |
| Provenance only | 13 |
| Detection only | 7 |
| Behavioral rules only | 3 |
| Learned decision only | 11 |
| All four | 0 |
| All but provenance | 0 |
| All but detection | 0 |
| All but behavioral rules | 6 |
| All but learned decision | 1 |

**Reading Table 4.61.**
- Each remaining control alone, and all four together, reduce attacks significantly against none. The Holm-adjusted p is below 0.001; the exact injection-task-level p is 0.0039, the smallest attainable with nine clusters.
- Coverage of the 907 attack-labeled state-changing calls:
  - every call is covered by at least one control, and 888 by two or more;
  - the controls overlap heavily (Jaccard 0.84–0.99);
  - 17 calls are covered by the behavioral rules alone. All of them are in the one user task whose own request names the attacker's account, where provenance and detection correctly see a trusted value.
- **Failure injection.** No single injected failure (detector, provenance, behavioral monitor, learned model, authorization evaluator, TAE store, gateway, audit) let an attack through under fail-safe defaults.
- **Real bypasses.** The reformatted-identifier and paraphrased populations gave the same attack counts as the original.
- **The fail-safe default is load-bearing in an author-written scenario:** an amount escalation to a trusted recipient, which only authorization covers.

**Interpretation.**
- In this replay, REM-DiD reaches Defense-in-Depth in the sense that independent controls protect when authorization is bypassed.
- Its controls are largely **redundant rather than complementary**.
- It is resilient to the loss of provenance or detection, but **not** to the loss of the behavioral rules or the learned decision.
- The results come from non-adaptive replay with oracle authorization, on data used before, and show nothing about adaptive attackers.
- Details and all arms are in `REM_DEFENSE_IN_DEPTH/51_DID3_RESULTS.md`.
"""
edit("src/CHAPTER_04_FINAL.md", "\n### 4.6.12 Chapter Summary", "\n" + CH4 + "\n### 4.6.13 Chapter Summary")

# ---------------------------------------------------------------- Chapter 5
edit("src/CHAPTER_05_FINAL.md", "\n## 5.6 Limitations and Threats to Validity",
     "\n**Not confirmed: resilient Defense-in-Depth (tenth edition, exploratory).** With authorization bypassed, REM-DiD's remaining controls stopped every attack in replay. Evading the behavioral rules or the learned decision, however, let 6 and 1 attacks through. The learned decision added no security behind oracle authorization and cost 68 benign tasks (Section 4.6.12).\n\n## 5.6 Limitations and Threats to Validity")
edit("src/CHAPTER_05_FINAL.md", "\n## 5.8 Conclusion",
     "14. **REM-DiD under adaptive attack.** Run the Defense-in-Depth candidate of Section 3.15 with live agents and an adaptive attacker (Narisetty et al., 2026). Use a trusted approval interface in place of the oracle authorization, and a benchmark with currency, source-account and approval parameters. Adoption of any REM-DiD element is a supervisor decision.\n\n## 5.8 Conclusion")

# ---------------------------------------------------------------- front matter
edit("text_front/front_matter.md", "This document is the **draft for supervisor review** dated 26 November 2026 (ninth edition,",
     "This document is the **draft for supervisor review** dated 27 November 2026 (tenth edition: the ninth edition of 26 November 2026 unchanged except for the dated, clearly marked exploratory sections 2.11.6, 3.15, 4.6.12 and two additions in Chapter 5 on a Defense-in-Depth candidate, REM-DiD; ninth edition,")

# ---------------------------------------------------------------- references (alphabetical insertion)
NEW_REFS = [
    "Gong, H., Samawi, M., & Medda, F. (2026). Authority–inference separation in agentic finance: Intent-bound control, EVM enforcement, and replayable assurance. *Systems, 14*(10), 1329. https://doi.org/10.3390/systems14101329 [Abstract and Crossref record only]",
    "Kabbinamakki Suresh, A. K., & Gao, P. (2026). *AgentCap: Capability-based runtime authorization for secure LLM agent execution* (arXiv:2611.00729) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2611.00729 [Abstract only]",
    "Mellafe Zuvic, D. (2026). *Capability gates are not authorization: Confused-deputy failures in LLM agent frameworks* (arXiv:2606.28679) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2606.28679 [Abstract only]",
    "Narisetty, P., Kore, S. N. B., Kattamanchi, U. K. R., & Kumarapu, J. (2026). *Adaptive evaluation of out-of-band defenses against prompt injection in LLM agents* (arXiv:2606.26479) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2606.26479 [Abstract only]",
    "Sequeira, R. X., Damianakis, S., Iqbal, U., et al. (2026). *Agent-Sentry: Bounding LLM agents via execution provenance* (arXiv:2603.22868) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2603.22868 [Abstract only; author list abbreviated from the index record]",
    "Zhang, K., Su, Z., Chen, P.-Y., et al. (2025). *LLM agents should employ security principles* (arXiv:2505.24019) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2505.24019 [Abstract only; author list abbreviated from the index record]",
    "Zhang, X., Cheng, Z., Liu, K., et al. (2026). *AGATE: Provenance-based runtime defense against compositional attacks on LLM agents* (arXiv:2609.30830) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2609.30830 [Abstract only; author list abbreviated from the index record]",
    "Zhong, P. Y., Chen, S., Wang, R., et al. (2025). *RTBAS: Defending LLM agents against prompt injection and privacy leakage* (arXiv:2502.08966) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2502.08966 [Abstract only; author list abbreviated from the index record]",
]
p = os.path.join(ED, "references", "REFERENCES_FINAL.md")
lines = open(p, encoding="utf-8").read().split("\n")
for ref in NEW_REFS:
    key = ref.lower()
    idx = [i for i, l in enumerate(lines) if l and l[0].isalpha() and l[:1].isupper() and not l.startswith("APA")]
    pos = next((i for i in idx if lines[i].lower() > key), idx[-1] + 2)
    lines[pos:pos] = [ref, ""]
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("tenth edition sources written")
