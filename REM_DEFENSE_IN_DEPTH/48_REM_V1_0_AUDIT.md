# Deliverable 2: REM v1.0 audit (the original, experimentally evaluated architecture)

**REM v1.0 is unchanged.** `rem/` has no commit in this track. The details are in `01_AUDIT.md`, `20_ARCHITECTURE_CURRENT_V1_0.md`, `05_DID_RESULTS.md` and `08_SIG1_RESULTS.md`. This file is the summary.

## 1. What v1.0 is (from code)

| Layer | Implemented controls | Independently evaluated? |
|---|---|---|
| 1 Input & Context | Segment trust labels; exact-string entity matching (x~act1~, x~act2~) | Yes: DiD-2 reformatting probe (P1 rises from 12 to 191 attacks) |
| 2 Detection | x~ctx2~ = union of 6 patterns, episode-level | Yes: SIG-1. A template fingerprint; recall 0 on `direct` and `ignore_previous`; no measurable contribution |
| 3 Behavioral | x~beh1–4~ (x~beh1~ duplicates x~ctx2~: correlation 1.00) | Yes: DiD-2 family evasion raises attacks from 11 to 131 |
| 4 Decision | D1/D2 predicates; ridge LR → Platt on the logit → consequence tier → expected-loss verdict | Ablations (thesis §4.5) |
| 5 Mitigation | Step-level withhold; Modify ≡ Escalate ≡ withhold without a reviewer | Gateway simulation (fail-closed) |

## 2. Verified results (replay, NO-ADAPT, AgentDojo 0.1.35 banking v1; reproduced exactly in this track)

| Measure | Value |
|---|---|
| Successful attacks | 11 / 2,979 (undefended: 672) |
| Benign tasks completed | 105 / 334 (undefended: 175) |
| Legitimate state-changing steps withheld (observe-only analysis) | 1,325 / 1,665 |
| Single-control evasion | Tolerated (DiD-1) |
| Behavioral family evaded | 131 attacks |
| Action family evaded | 90 attacks |
| Both families evaded | 669 attacks |

## 3. Weaknesses found (motivating REM-DiD)

1. No representation of what the user authorized. REM can only estimate risk.
2. Exact matching of identifiers.
3. Detection adds nothing.
4. Depth comes from low-specificity behavioral signals, which also cause over-blocking.
5. Escalate and Modify are not distinct without a reviewer.

## 4. Level reached (task §3 scale)

- **Layered architecture: yes.**
- **Defense in Depth:** partly. Two evidence families each contribute, and Detection does not.
- **Resilient Defense in Depth:** to single-control loss, yes (DiD-1); to family loss, no (DiD-2).
