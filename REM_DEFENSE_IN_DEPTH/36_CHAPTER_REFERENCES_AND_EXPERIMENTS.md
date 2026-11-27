# Recommended references per thesis chapter, and experiments needed to establish the contribution

## 1. Recommended references per chapter (five-chapter thesis)

**Status column:**
- **In** = already in `REM_DEFENCE_READY_THESIS/references/REFERENCES_FINAL.md`;
- **Add** = recommended addition;
- **Fix** = the existing entry or citation needs correction.

Level is the evidence level from file 30. **No reference marked Add may be inserted into the thesis until its full text has been read** (file 35 §4). Until then it can only be cited for what its abstract says, and marked as such.

| Chapter | Purpose | Reference | Status | Level |
|---|---|---|---|---|
| 1 Introduction | Threat definition | Greshake et al. 2023 (AISec) | In | A |
| 1 | Benchmark and banking setting | Debenedetti et al. 2024, AgentDojo (NeurIPS D&B) | In | A, L |
| 1 | DiD as a design principle for agents | K. Zhang et al. 2025, *LLM agents should employ security principles* (preprint) | Add | A |
| 1 | Why static evaluation is insufficient | Narisetty et al. 2026 (preprint) | Add | A |
| 2 Literature review | System-level and IFC defenses | CaMeL (arXiv v2; **SaTML 2026 not confirmed**) | In; keep as preprint | R |
| 2 | | Costa et al., Fides | **Fix:** "to appear, NeurIPS 2026" per the authors' institution, once the proceedings record is verified; currently cited as a preprint | W, A |
| 2 | | Zhong et al. 2025, RTBAS (preprint) | **Fix:** RTBAS is named in §2.6.1 and Table 2.2 of the defence-ready thesis **without an author-year citation, and it has no reference-list entry**. Add both | A |
| 2 | Privilege control | Shi et al., Progent v3 (preprint) | In. **Do not use the title "Programmable Privilege Control for LLM Agents"** unless citing the version that carries it | F |
| 2 | Capability authorization | Kabbinamakki Suresh & Gao 2026, AgentCap (preprint) | Add | A |
| 2 | Financial authority separation | Gong, Samawi & Medda 2026, AIS, *Systems* 14(10) 1329 (peer reviewed) | Add (the closest peer-reviewed financial work) | C, A |
| 2 | Parameter-bound grants, effect ledger | X. Zhang et al. 2026, AGATE (preprint) | Add | A |
| 2 | Provenance vs authorization | P. Wang, Li & Tian 2026, AuthGraph (preprint) | Add | A |
| 2 | Layered complementary checks | Sequeira et al. 2026, Agent-Sentry (preprint) | Add | A |
| 2 | Money ceiling and idempotency in payment agents | Mellafe Zuvic 2026, ScopeGate (preprint) | Add | A |
| 2 | Authority confusion; runtime layer vs prompt policy | Qin et al. 2026, AIRGuard (preprint) | Add | A |
| 2 | Deterministic-first, risk-cannot-override ordering | Karnawat et al. 2026, GuardRail (Zenodo report; no measurements) | Add only with that caveat, or omit | A |
| 2 | Benchmarks | H. Zhang et al. 2025, ASB (ICLR) | In | A |
| 2 | Provenance | She et al., ProvenanceGuard | **Fix:** now ASE 2026, DOI 10.1145/3832783.3837535 (the thesis cites a preprint) | A |
| 2 | Configuration comparison | Kanaker et al. 2026 | In | A |
| 3 Methodology | Replay as a method | Kekatos et al. 2026 (In); Lesnikov 2026, ASC (Add, preprint): replay of AgentDojo ground-truth traces | In / Add | A |
| 3 | Adaptive-evaluation requirements, as a stated limitation | Narisetty et al. 2026; Progent App. E | Add / In | A / F |
| 3 | Independent protection layers and common-cause failure (conceptual origin of evasion-conditioned testing) | **To be identified** from the safety-engineering literature (file 35 §4.2); none verified here | Gap in sources | — |
| 4 Results | Context only; no numeric comparison | Progent (F); CaMeL, Fides, AgentCap, AuthGraph (author-reported figures, not compared) | In / Add | F / A |
| 5 Conclusion and future work | TAE and authorization future work | AIS, AGATE, AgentCap, GuardRail | Add | C, A |
| 5 | Adaptive and live evaluation | Narisetty et al.; AdapTools (EMNLP 2026) | Add | A |

## 2. Experiments needed to establish the contribution

Each experiment needs a protocol committed before it runs, as in the DiD track. **Decision gates** say what result would change the contribution statement (file 35 §6).

| ID | Purpose (gap) | Hypothesis | Data | Analysis | Decision gate | Feasibility |
|---|---|---|---|---|---|---|
| **E0** | Literature check (file 35 §4) | — | Full texts of the 10 works in file 35 §4.1 | Record, per paper, any test-time evasion analysis with the other controls fixed | If one exists for agents under injection, drop G1 from the claim | Needs a session in the `ram-thesis-research` environment (arXiv allowed) |
| **E1** | G1: replace modeled evasion with real evasion (= DiD-3) | Real paraphrased injections without trigger words leave REM's protection unchanged (detection adds nothing), while mimicking the benign tool order degrades the behavioral family as modeled | Deterministic rewrites of the injected texts in the recorded runs, built like POP-R | Paired replay; exact McNemar against REM on the original texts; grouped bootstrap | If real evasion of a family has less effect than modeled evasion, report "modeled evasion is conservative" | Offline; protocol drafted in file 06 |
| **E2** | G5 and interaction with deterministic authorization (= TASK 2 F1) | With oracle-TAE constraints (4A), the learned decision (4B) adds no security. Its value, if any, is in the regime where the TAE is broad | Arms: oracle-TAE 4A alone; 4A + 4B; broad TAE ("any known payee, up to X") with 4A alone and 4A + 4B; under evasion of each REM family | Paired replay; attacks, benign tasks, legitimate steps released | If 4B adds nothing in either regime, the thesis states that authorization subsumes the learned decision on this benchmark | Offline; **broad-TAE bounds (X) are design values that must be declared by the supervisor, not chosen** |
| **E3** | G1 for comparators | Single-control defenses (P1, P2, the Progent manual policy) have no depth: evading their one input defeats them | Same evasion conditions applied to the comparators, in replay | As E1 | Comparative depth table | Offline; partly done (P1 rises from 12 to 191 under reformatting) |
| **E4** | Replication (development-data concern) | DiD-2 orderings hold on a second population | Cross-template or held-out injection tasks already in the records | Same as DiD-2 | Mismatch → report as population-dependent | Offline |
| **E5** | G3, G4: redundancy and cost of depth | The controls that provide depth are the ones that withhold legitimate steps | Per-control attribution of every withheld legitimate step; correlation matrix of all signals | Descriptive; conditional coverage | Supports or refutes "depth and over-blocking share a source" | Offline |
| **E6** | Sensitivity of the depth conclusions to the loss values (= DiD-5) | Orderings are stable across a declared loss grid | Same replay, other loss settings | Rank stability | — | **[DESIGN BLOCKED]**: the loss grid is not frozen (CLAUDE.md). Supervisor decision required |
| **E7** | Adaptive attacker (stated limitation) | — | Live agents with the Narisetty protocol | — | — | **R:** needs model-API budget and explicit authorization; not run |
| **E8** | Financial properties that the benchmark does not cover | — | Fixtures for amount substitution with an allowed recipient; cumulative limits (injection_task_6 pattern); recurring redirection | Fixture pass/fail | — | Offline for fixtures; **limit values are design values → [DESIGN BLOCKED] until declared** |

**Minimum set before the contribution statement may be used:** E0, E1, E2 and E5. E3 and E4 strengthen it. E6 and E8 need declared design values. E7 is outside the present resources.
