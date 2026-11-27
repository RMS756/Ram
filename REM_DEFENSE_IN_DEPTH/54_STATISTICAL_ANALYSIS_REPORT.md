# Deliverable 17: Statistical analysis report (DiD-3)

**Analysis code:** `code/did3_analyze.py`. **Output:** `results/did3_results.json` (`declared_contrasts`, `supplementary_contrasts_unadjusted`).

## 1. Design and dependence

- **Unit:** an episode is one recorded run replayed with the agent fixed.
- **Episodes are not independent.** Each (user task × injection task) cell holds up to 21 runs: different backbones on the same task pair.
- **Clusters:**
  - attacked episodes: 144 cells within **9 injection-task clusters**;
  - benign episodes: **16 user-task clusters**.
- **Pairing:** every arm replays the same episodes, so contrasts are paired.

## 2. Methods (declared in the protocol before the run)

| Method | Use |
|---|---|
| Cluster-level sign-flip permutation (20,000 Monte Carlo sign vectors over cells; seed 20261027) | Primary p for each contrast |
| Exact sign-flip at the top cluster level (9 injection tasks: 512 vectors; 16 user tasks: 65,536) | Robustness to within-injection-task dependence. Minimum two-sided p is 2/512 = 0.0039 |
| Leave-one-cluster-out range | Sensitivity of every contrast to a single injection or user task |
| Grouped bootstrap 95% intervals (2,000 resamples, by injection task or user task) | Per-arm counts |
| Holm correction over the 15 declared contrasts | Family-wise error |
| Exact McNemar at episode level | Continuity with DiD-2 only. **Ignores clustering; not used for inference** |

## 3. Results of the declared contrasts

| Contrast | A − B | p (cells) | p (exact, top cluster) | Holm | Leave-one-out range | Reading |
|---|---:|---:|---:|---:|---|---|
| X0 vs X-all, attacks | −174 | <0.0001 | 0.0039 | <0.0001 | [−172, −138] | Remaining controls protect (H1) |
| X-only-PROV vs X-all | −161 | <0.0001 | 0.0039 | <0.0001 | [−159, −128] | PROV protects alone |
| X-only-DET vs X-all | −167 | <0.0001 | 0.0039 | <0.0001 | [−165, −133] | DET protects alone |
| X-only-BEH vs X-all | −171 | <0.0001 | 0.0078 | <0.0001 | [−171, −135] | BEH protects alone |
| X-only-LEARN vs X-all | −163 | <0.0001 | 0.0039 | <0.0001 | [−161, −129] | LEARN protects alone |
| X-PROV vs X0 | 0 | 1 | 1 | 1 | [0, 0] | Resilient |
| X-DET vs X0 | 0 | 1 | 1 | 1 | [0, 0] | Resilient |
| X-BEH vs X0 | +6 | 0.25 | 0.25 | 1 | [4, 6] | Strict criterion fails; not distinguishable from 0 |
| X-LEARN vs X0 | +1 | 1 | 1 | 1 | [0, 1] | Strict criterion fails |
| B9 vs B9n, attacks | 0 | 1 | 1 | 1 | [0, 0] | 4B adds no security behind the oracle TAE |
| B9 vs B9n, benign | −68 | 0.014 | 0.014 | 0.12 | [−74, −51] | 4B costs utility; not significant after Holm |
| B9 vs B1, attacks | −11 | 0.12 | 0.125 | 0.97 | [−11, −7] | REM-DiD removes v1.0's 11 residual attacks; with 9 clusters this is not significant |
| B9 vs B1, benign | 0 | 1 | 1 | 1 | [0, 0] | Same utility (both at the 105 floor) |
| B9e vs B9, benign | 0 | 1 | 1 | 1 | [0, 0] | — |

"<0.0001" means no permuted statistic reached the observed one in 20,000 draws.

## 4. Interaction analysis

| Question | Answer | Basis |
|---|---|---|
| Do controls reinforce each other? | Yes in aggregate: 4 controls → 0 attacks; each alone → 3–13 | X arms |
| Do they provide independent evidence? | Largely not | Call-level coverage Jaccard 0.84–0.99; detector phi 0.92–0.98 |
| Do they duplicate the same signal? | Largely yes. PROV and DET cover nearly the same calls (Jaccard 0.99), because both key on the attacker identifier in untrusted text | — |
| Do they create conflicting decisions? | No by construction (most restrictive wins). Conflicts between rule verdicts are recorded per call in the audit | — |
| Do they increase false positives? | Yes. Legitimate state-changing calls withheld: 774 with AUTH alone (oracle); 1,508 with the full strict stack; 1,351 in X0 | §1 table of file 51 |
| Do they reduce benign utility? | 4B costs 68 tasks behind AUTH; PROV, DET and BEH cost nothing behind a pinning TAE (B9n = B2 = 173) but cost tasks alone (B3 147, B4 164, B5 161) | — |

**Synergy is not claimed from visual differences.** The one test that would show synergy (X0 < each X-only arm) holds descriptively: 0 vs 3–13. The differences X-only-c − X0 were not declared as contrasts, so no p-value is reported for them.

## 5. Limits of inference

- Nine injection-task clusters bound every attack contrast. The exact test cannot go below p = 0.0039.
- Data reuse: all results are exploratory.
- Replay determinism: there is no stochastic variation across repeats, so repeats would add nothing. Variation comes only from the 21 backbones' recorded behaviours.
