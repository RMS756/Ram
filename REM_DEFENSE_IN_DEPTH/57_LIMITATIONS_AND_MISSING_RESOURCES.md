# Deliverable 22: Complete limitations and missing-resource report

## 1. Missing resources (what blocked what)

| Resource | Blocks | Status |
|---|---|---|
| Network access to arxiv.org, openreview.net, satml.org, neurips.cc, alphaxiv.org (refused in this session) | Full-text reading of CaMeL (and its SaTML 2026 version), RTBAS, AgentCap, Narisetty, Fides; verification of CaMeL at SaTML and Fides at NeurIPS | **Blocked here.** The user's saved environment `ram-thesis-research` allows arxiv.org; a session started there can do it |
| RTBAS and AgentCap source code | Code-level inspection | No public repository found |
| Model API budget and authorization (live LLM agents) | Adaptive attacks; retry and tool-switching under adaptation; live utility | Not available; not run |
| Injection classifier weights (x~ctx1~, AgentDojo `transformers_pi_detector`) | Detection category 4 | Model download unavailable; decision D-8 open |
| Trusted approval interface | Non-oracle TAE issuance | Not in AgentDojo; only oracles evaluated |
| Second financial benchmark with argument-level tools | External validity | ASB's finance scenario has argument-less simulated tools, so it is incompatible |
| Two qualified human annotators | Label audit | Package ready (file 53); not performed |
| Untouched data | Confirmatory testing | None remains; everything is exploratory |

## 2. Methodological limitations

1. **NO-ADAPT replay.** The agent does not react to withheld calls, so retry, tool-switching and alternative-path behaviour is only what was recorded. **No claim of adaptive robustness.**
2. **Oracle authorization.** B2, B9 and X* use ground-truth parameters. The `explicit` mode shows the cost of refusing to invent unstated parameters. Real issuance quality is unknown. Earlier NL compilation attempts were NO-GO (REM-B2/B3).
3. **Modelled evasion** for PROV, BEH and LEARN (the control reports no evidence on attack calls). Real evasion was tested only for identifier reformatting (POP-R) and one declared paraphrase (POP-X), both conditional on unchanged agent behaviour.
4. **Detector design knowledge.** The detectors were written knowing the templates. Paraphrase and zero-width obfuscation show their fragility (SIG-2).
5. **Lineage is inferred,** not tracked through the agent. Collisions (`user_task_15`) and laundering through paraphrase are inherent limits.
6. **Benchmark narrowness:**
   - one suite and one attacker account (8 of 9 injection tasks);
   - no currency or source-account parameters;
   - 16 user tasks;
   - utility insensitive to read-only calls in replay.
7. **Labels** come from the reference rule (no human audit). The idealized-reviewer arms reveal label-0 calls that still contributed to attack success.
8. **Multiple comparisons.** 15 declared contrasts are Holm-corrected. Supplementary contrasts are unadjusted and descriptive.
9. **Prior-art depth.** Most systems are known at abstract or repository level (file 30). A full text could contain a bypass analysis like DiD-3's, which would narrow the contribution claim (file 35 §4).

## 3. Limitations of REM-DiD as a design

- **Amount attacks against a trusted recipient are covered only by authorization** (scenario 15d). There is no second line of defence for amounts.
- **Detection is not an independent layer.** Its sub-signals are highly correlated (phi 0.92–0.98); the only robust one keys on financial payloads and fires on 23% of legitimate documents.
- **Redundancy, not complementarity.** Behind bypassed authorization, PROV, DET and LEARN cover nearly the same calls. Distinct coverage exists for only 19 of 907 calls.
- **Over-blocking.** The full strict stack withholds 1,508 of 1,644 legitimate state-changing calls. Utility recovers only with authorization-first precedence (B9p: 172 benign) or an idealized reviewer.
- **Modify** has no safe mechanism. **Escalate** without a reviewer equals Block.
- **No recovery.** Prevention only.

## 4. Decisions required (supervisor)

| ID | Decision | Notes |
|---|---|---|
| SD-DID-1 | Adopt any REM-DiD element into REM (TAE input, 4A, precedence, new evidence rules, gateway)? | Each changes a frozen item |
| SD-DID-2 | Authorization source for a real deployment | Trusted UI, not NL compilation |
| SD-DID-3 | 4B's role behind authorization (strict vs pinned_release vs removal) | 4B adds no security here, at a cost of 68 benign tasks |
| SD-DID-4 | Modify mechanism | Still undeclared |
| SD-DID-5 | Whether to fund live adaptive evaluation | Not run |
| SD-DID-6 | Revised research-question wording | The PI's RQ in the task is recorded as [PD] |
