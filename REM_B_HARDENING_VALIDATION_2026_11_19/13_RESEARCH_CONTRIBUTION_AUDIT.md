# 13 Research contribution audit (Phase 10)

The approved thesis objectives are not modified. Novelty is judged against the verified literature of `REM_ARCHITECTURE_REDESIGN_STUDY_2026_11_18/02` (Progent, CaMeL, AgentDojo, MELON, Task Shield, AgentSpec, ShieldAgent, ProvenanceGuard, LlamaFirewall; Saltzer & Schroeder 1975; Dennis & Van Horn 1966; Hardy 1988). No new source was added in this study.

## 1. Did the improved architecture provide each property?

| Property | Evidence | Answer |
|---|---|---|
| Stronger authorisation integrity | Recorded traces: audited violations REM-B2 11 / 0 / 9 / 0 / 0 vs PG 161 / 36 / 125 / 0 / 0. Held-out probes: REM-B2 3 unauthorised (v2) and 4 (v3); PG 3 and 4, of different kinds. | **Partly.** On recorded traces, yes against an allow-list. On new requests, no: unauthorised releases remain. |
| Better legitimate-task preservation | H2: +83 tasks vs REM-B, +59 vs PG; intervals include 0; gains confined to two tasks | **Not established statistically**; task-specific |
| Better generalisation | Gains do not reach the 14 other user tasks; held-out probes found new failures in each round | **No** |
| Lower runtime cost | Median decision latency 0.28 ms (REM-B2) vs 0.20 ms (PG); p95 10.8 ms vs 0.69 ms; 0 model calls | **No** vs PG (slower); **yes** vs any model-based guard. There is no model call, but no model-based guard was measured here. |
| More interpretable enforcement | Every verdict has a deterministic source (front, object, contract, refund licence, delegated condition) and a ledger state | **Yes, qualitatively.** Not measured with users. |
| Measurable advantage over simpler policies | vs C1: +84 H2 tasks (interval lower bound 0), same security; vs PG: fewer violations, held-out failures on both | **Not established** under the pre-registered rules |

## 2. What kind of contribution remains

| Candidate type | Assessment |
|---|---|
| 1. An authorisation mechanism | **Not as a validated mechanism.** The instruction-, object- and amount-bound checks are sound principles (least privilege, complete mediation, capabilities). Their implementation through a hand-written request compiler failed held-out probes three times. Progent and CaMeL already provide per-call authorisation and value provenance; what REM-B adds (stateful, object-bound financial allowances) is an application of those principles, not a new principle. |
| 2. A provenance-aware enforcement method | **Weak.** R2 (system-of-record evidence) is a reasonable engineering choice (complete mediation against authoritative state). CaMeL's provenance tracking is the principled, stronger version. |
| 3. A hybrid learned / deterministic framework | **No.** Every learned placement tested (REM-A, REM-C, REM-C-T, REM-C-raw, REM-B2-HW, REM-B2-HR) is NULL, harmful or inconclusive. The stored score's review ranking even reverses between development populations. |
| 4. An empirical security–utility evaluation | **Yes: the strongest contribution.** It has five parts: (a) pre-registered, hash-frozen comparisons; (b) value / object integrity measured next to attack success, revealing 161 / 36 / 125 PG violations invisible to attack-success metrics; (c) the reachability and target-mismatch explanation of why a calibrated learned stage cannot add value behind deterministic authorisation; (d) three rounds of held-out probes showing that NL-request compilation is the security bottleneck of request-derived authorisation; (e) Progent's checker reproduced on 3,933 calls. |
| 5. A combination with demonstrated incremental value | **No.** Incremental value is shown only for R2 and R3 on two tasks, and the combination fails S4. |

## 3. Is the research gap still supported?

| Part of the gap | Status |
|---|---|
| Runtime mediation of financial agent actions is needed | **Supported**: B0 attacks 672 / 436 / 553 / 145 / 174 |
| Allow-list policies do not protect financial values | **Supported** on recorded traces (PG violations) |
| A calibrated, consequence-aware learned risk stage improves runtime decisions | **Not supported** in this setting; repeated null / negative results |
| Deriving per-request financial authorisation from natural-language requests can be made reliable with deterministic rules | **Not supported.** Each held-out round exposed new compiler errors. This is a **new, well-evidenced sub-gap**: verified compilation of user intent into authorisation policies. |

## 4. Changes that need supervisor approval `[SUPERVISOR DECISION REQUIRED]`

| Item | Why it needs approval |
|---|---|
| Moving from the approved pipeline (ridge → Platt → expected loss) to an authorisation-first verdict path | It changes the frozen REM pipeline (CLAUDE.md). The evidence (null learned stage) supports the move, but the authorisation-first candidates are NO-GO on held-out probes. |
| R3 (delegated judgement conditions) | It changes the semantics of conditional authority |
| Reframing the contribution as primarily an empirical security–utility evaluation with negative results | It changes the thesis's claimed contribution, not its objectives |
| A live-agent study and full-Progent comparison | They need backbones, repeats and a budget |
| Independent probes (authored by someone other than the designer) | They are needed before any validation claim |

## 5. Recommendation (not a decision)

1. **Keep REM v1.0 as the approved design.** Report the authorisation-first variants as exploratory, with their NO-GO results.
2. **Present the empirical findings as the contribution:**
   - deterministic mediation stops every recorded attack;
   - the learned stage is unreachable or harmful;
   - allow-lists miss value integrity;
   - request-compilation errors are the failure mode, found three times by held-out probes.
3. **Future work:** verified intent compilation (formal grammar with completeness checks, or user confirmation of the compiled policy), which is the natural next step and closest to Progent's policy-generation problem.
