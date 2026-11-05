# Literature Review — update draft (for §2.6 / §2.13; to be merged when the chapter is edited)

**Status:** draft text. Every statement is limited to the evidence level shown. No new reference is introduced: MELON (Zhu, Yang, et al., 2025) and FinHarness (H. Jia et al., 2026) are already in the reference list.

**Proposed addition (one paragraph, §2.13 closest prior work):**

> Two published systems are closest to the placement and domain of REM. MELON (Zhu, Yang, et al., 2025) detects indirect prompt injection by re-executing the agent's next step with the user's request masked, and it stops the agent when the tool calls proposed with and without the request are similar. Its public implementation, inspected for this thesis, compares embeddings of the proposed calls with a fixed cosine-similarity cut-off and replaces the agent's proposed calls with a stop message. It therefore makes a binary decision that does not depend on the consequence of the action. FinHarness (H. Jia et al., 2026) wraps a financial agent with query and tool monitors and a risk-routed cascade of LLM judges, and it reports results on FinVault, whose preprint was withdrawn (Section 2.10.2). No public implementation of FinHarness was found. REM shares the runtime placement with both and the financial domain with FinHarness. It differs in deciding per call from a calibrated probability and consequence-tiered expected loss, without additional model calls.

**Do not add:** benchmark numbers from either paper next to REM's; any "first" claim.
