# 04: REM improvement matrix

**Class.**

| Class | Meaning |
|---|---|
| 1 | Documentation improvement |
| 2 | Architectural clarification |
| 3 | Implementation improvement |
| 4 | New security capability |
| 5 | Future research |

**Recommendation.**

| Code | Meaning |
|---|---|
| **CT** | Recommended for current thesis documentation |
| **FI** | Recommended for a future REM implementation |
| **FR** | Recommended for future research only |
| **NR** | Not recommended |

**Constraint.** No proposal below introduces an equation, score, threshold or algorithm. Where a source framework uses mathematics (for example a drift score or a similarity threshold), the proposal records that it is **not** adopted (06).

| ID | Existing framework | Specific mechanism | Security problem addressed | Potential REM application | REM layer | Expected benefit | New data? | New experiments? | Mathematical changes? | Class | Rec. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | Layered RAG framework (instruction hierarchy); CaMeL (capabilities); Spotlight-Guard (spotlighting) | Explicit separation of trusted instructions from retrieved content | Untrusted content treated as instruction | **REM already implements** three trust labels with least-trusted inheritance and no promotion. Document them as an explicit trust boundary, with a diagram of which segments each feature reads | 1 | Clearer justification. **No security change** | No | No | No | 1 | **CT** |
| D2 | NEXUS (rules vs risk score); AIS (inference vs authority); Progent | Separation of *detection* from *authorization* | Conflating "suspicious content" with "unauthorized action" | State explicitly that REM v1.0 estimates the probability of attack inducement and **does not authorize**. It knows where values came from, not what the user authorized | 2, 4 | Correct positioning; explains the `user_task_15` residual and the low specificity | No | No | No | 2 | **CT** |
| D3 | AIS; AgentCap; ClawGuard | External enforcement point independent of the agent | The agent executing its own calls | **REM already implements** a fail-closed HTTP gateway at the tool boundary, with exact replay parity on 3,334 recorded episodes. Document it as the Mitigation layer's enforcement point and state that it was never run with a live agent | 5 | Credibly documents existing enforcement | No | No | No | 1 | **CT** |
| D4 | Agent-Sentry (sequence + provenance); Multilayer DiD (observability) | Complementary evidence families | One evidence family failing | Document the dependency graph: action features depend on Layer 1 labels; `x_beh1` depends on `x_ctx2`. Document the DiD-2 finding that behavioural and action evidence cover different attack classes | 1→3, 4 | Explains where depth exists and where it does not | No | No | No | 1 | **CT** |
| D5 | NEXUS (confirm); CASCADE (review) | Human escalation as a separate outcome | High-impact actions needing approval | State that Escalate is a design slot with **no reviewer**, so it coincides with Block. Report the idealized-reviewer replay only as a counterfactual bound | 4, 5 | Honest semantics | No | No | No | 1 | **CT** |
| D6 | CASCADE audit (reporting checklist) | Stating the decision convention behind each metric | Headline numbers depending on how "review" is counted | State in Chapter 4 how Allow / Modify / Escalate / Block map onto "withheld", and which population, metric and denominator each number uses | — | Comparable, auditable numbers | No | No | No | 1 | **CT** |
| D7 | BARBICAN ("Deletion is not substitution") | Substitution and suppression in addition to deletion when attributing layer contributions | Misattribution by removal ablation | Cite as independent support for REM's removal-versus-suppression finding (DiD-2) | — | Stronger related-work positioning for the primary contribution | No | No | No | 1 | **CT** |
| I1 | ROPE (fails closed on non-canonical values); REM-DiD (canonical IBANs) | Canonical comparison of financial identifiers | Reformatted identifiers defeating exact-string provenance | Canonicalize IBANs and amounts before `value_occurs_in`. DiD-2 showed the exact-match rule P1 rises from 12 to 191 attacks under reformatting, while REM v1.0 stays at 11 because of `x_act2` | 1, 3 | Robustness of provenance evidence | No | Yes (POP-R replay; regression of P1–P3) | No (normalization rule only) | 3 | **FI** |
| I2 | ROPE (origin labels with platform metadata); REM-DiD (field-level provenance) | Source identity per tool output and field, not only per channel | Free-text fields (subjects, file bodies) vs typed fields treated alike | Record tool and field of each segment; keep the trust labels | 1 | Finer provenance; prerequisite for authorization | No | Yes | No | 3 | **FI** |
| N1 | Progent; ClawGuard; CapLite; AIS; NEXUS rules | Model-independent argument authorization of financial calls (recipient, amount, operation) derived from trusted input | Authorized vs unrequested payments (the limit REM's evidence cannot cross) | A deterministic authority check before the learned decision, as in exploratory GV/G1. **Not part of REM v1.0** | 4 (+1) | Large in exploratory replay. Limited by natural-language intent compilation (REM-B hardening: a new compiler error in each held-out probe round) | Trusted authorization input (absent in AgentDojo) | Yes, including held-out phrasing and live agents | No (rules) | 4 | **FR** |
| N2 | NEXUS (confirm); AIS (approvals); A-VIP (surfaces unauthorized spending) | Human confirmation for high-impact operations | Irreversible financial actions | Give Escalate a real reviewer channel | 5 | Realizes the four-verdict design | Reviewer study | Yes (human study; ethics) | No | 4 | **FR** |
| N3 | AIS (mandates); AGATE (grants); ScopeGate (ceiling) | Cumulative and per-payee economic limits | Split transfers; amount escalation to trusted recipients | Not in REM v1.0. Values are [DESIGN BLOCKED] | 4 | Bounds loss | Declared limits | Yes (author-written fixtures) | No (limits are policy values, not models) | 4 | **FR** |
| N4 | CaMeL (readers); Fides (labels) | Information-flow control on outputs and arguments | Exfiltration through payment subjects | Outside the current threat model's evaluation | — | Covers an attack class REM does not evaluate | New attack set | Yes | No | 5 | **FR** |
| N5 | Multilayer DiD (drift score); MELON (masked re-execution) | Trajectory or goal-drift signals from embeddings or extra LLM runs | Goal drift without obvious content | Would add an embedding model or LLM to the evidence path. MELON's and the drift score's thresholds are their authors' | 3 | Unknown on REM's data | Embedding model or LLM | Yes | **Yes** (the authors' scores; full texts unread) | 5 | **FR** (only under 06's rules); an LLM in the *decision* path is **NR** (CLAUDE.md forbids LLM-based decision arbitration) |
| N6 | BARBICAN (constant-verdict mutants as a CI gate) | Test that each stage's verdicts can reach the output | Dead or redundant stages | A test that substitutes constant verdicts per component in replay | — | Engineering assurance of layer reachability | No | Yes (offline) | No | 5 | **FR** |
| X1 | PromptGuard (adaptive response refinement); RAG output audit | Output moderation of generated text | Harmful text output | Not applicable to tool-call authorization | — | None for REM's threat | — | — | — | — | **NR** |
| X2 | Any framework with more layers | Adding a sixth layer | — | Violates the frozen five-layer architecture. Layer count is not protection | — | None | — | — | — | — | **NR** |
| X3 | Agent-Sentry, DEFER1 | LLM judge for residual cases | Ambiguous cases | LLM-based decision arbitration is a forbidden reintroduction (CLAUDE.md) | 4 | — | — | — | — | — | **NR** |

**Phrase required by the task, applying to D1–D7, I1, I2, N1–N4 and N6:**

> This improvement can be implemented as an architectural, deterministic, or policy-based control and does not require a new mathematical model.
