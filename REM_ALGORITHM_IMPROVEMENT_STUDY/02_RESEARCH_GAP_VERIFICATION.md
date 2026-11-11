# Research gap verification

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

The broad claim that authorization-aware or provenance-aware runtime checking is new is **not defensible**. The narrower empirical question is whether explicit authorization contracts improve the security–utility trade-off over REM and a simple provenance rule on held-out banking workloads. This study does not establish that improvement.

## Verified prior-art overlap

- [PROVISO v1](https://arxiv.org/html/2610.27115v1), §3.1 and §6 limitations: distinguishes licensed operations/targets from external argument support. It fits each benchmark separately and does not study transfer of one controller across tasks. Its AgentDojo candidate-selection setting rolls out two continuations and uses a single agent backbone. These are relevant limitations, not proof that REM fills them.
- [AgentBoundary v1](https://arxiv.org/html/2609.33658v1), §3–5: separates apparent risk and permissibility with matched executable task families. It is an evaluation framework with a mitigation experiment, not a drop-in banking authorization controller. REM's current data lack this matched authorization annotation.
- [Task Shield, ACL 2025](https://aclanthology.org/2025.acl-long.1435/), §3–4 and Appendix B: checks whether instructions and calls contribute to user tasks. This directly overlaps user-intention alignment. It relies on model-generated checking; the exact-grant engineering candidate is not its reproduction.
- [CaMeL](https://arxiv.org/html/2503.18813), §5.2–5.4: policies/capabilities and data/control separation substantially predate this study. Exact contracts here borrow the policy idea without reproducing its interpreter or claiming its guarantees.
- [ProvenanceGuard](https://arxiv.org/html/2607.01236v2), §3–4: distinguishes tool, parameter and interpretation misalignment. This is the agent guardrail paper, not similarly named RAG/factuality systems.
- [NEXUS](https://arxiv.org/html/2607.19356), §4: structured plans, argument inspection and graded intervention; overlaps REM's architecture and rules.
- [Kairos](https://arxiv.org/html/2610.18457v1), §III: system-boundary effect mediation and policy/oracle decisions with deferred speculative effects; stronger confinement assumptions than this Python banking adapter.
- [MELON, ICML 2025](https://proceedings.mlr.press/v267/zhu25z.html), §3: masked re-execution and tool comparison; tests dependence on the user request through another model execution, unavailable in these recorded traces.

## Defensible scope

Explicit contracts separate positive permission, contradiction and insufficient evidence. The executable schema checks, exact-value repair and one-use reservations are engineering choices. None is claimed as a novel mathematical algorithm. Claims of cross-benchmark transfer, adaptive robustness, institutional deployment or priority over the above work are unsupported.

The source register contains retrieval URLs and full-text hashes. Review focused on methodology, required inputs and limitations; it is not a complete independent audit of every appendix result. No new mathematical learning method was adopted from these papers, so no unread or unverified equation was inserted in the candidate.
