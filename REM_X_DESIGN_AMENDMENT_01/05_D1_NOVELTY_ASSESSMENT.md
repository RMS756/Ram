# A1-05: Revised novelty assessment of D1

**Question.** Is the following combination materially different from ROPE and the other prior work?
1. explicit user delegation to a particular financial document;
2. limited to individually specified fields;
3. deterministic schema-based extraction;
4. exact provenance binding between the document field and the tool argument;
5. financial limits and first-payee restrictions;
6. independent execution authorization.

**Basis.** ROPE at code and log level (R). AGATE, AgentCap, Agent-Sentry and AIS at A/S level. **No novelty is claimed below.** The table records what is and is not established at the levels read.

## 1. Element by element

| # | Element | Closest prior art (level) | Assessment |
|---|---|---|---|
| 1 | Explicit user delegation to a named source | ROPE `named_source`, chosen from the trusted request (R) | **Exists.** ROPE delegates to an authenticated structured sender, not to a document. The *object* of delegation differs, but per A1-04 a document cannot carry trust by itself, so this difference does **not** yield a safe new capability |
| 2 | Per-field delegation | ROPE per-parameter markers (`SOURCED`, `FREE`, `CONST`) (R); CaMeL per-value capabilities (R) | **Exists** at the parameter level |
| 3 | Deterministic schema extraction | CaMeL quarantined LLM (model-based, R); the invoice-agent practitioner project (strict schema, S, non-scholarly) | Deterministic extraction **from banking documents in an agent-security defense** was not found at the levels read. It is an implementation choice, and per A1-04 it provides binding, not authenticity |
| 4 | Exact field-to-argument binding | ROPE: item-level substring (R); AIS typed intent fields (A) | A **refinement** of ROPE's matching rule |
| 5 | Financial limits; first-payee restriction | AIS exact economic terms and mandate (A); ScopeGate money ceiling (A); AgentCap budgets (A); REM-DiD first-payee rule [DiD-I] | **Exists** |
| 6 | Independent execution authorization | AIS EVM verifier (A); AgentCap tool-boundary tokens (A); AGATE adapters (A) | **Exists** |

## 2. Is D1 different from ROPE, or an implementation variant?

**Original D1** (admit a document-derived payee on extraction plus no alert):
- This was a real behavioural difference from ROPE: it admits values ROPE refuses.
- **It is unsafe** (A1-04 §1–2). The difference therefore cannot be a contribution.

**Revised D1** (O1–O5):
- Automatic admission of a payee requires an independent trusted reference. This is essentially ROPE's own record/named-source admission, applied with field-level binding.
- What remains distinct from ROPE:
  - (a) field-level rather than item-level binding;
  - (b) amount and cumulative control, which ROPE's banking table lacks;
  - (c) withholding for review instead of refusal;
  - (d) explicit ambiguity outcomes.
- **(a) and (d) are implementation refinements. (b) is a scope extension using established controls. (c) is REM's existing verdict semantics.**

**Verdict at the present evidence level.** Revised D1 is **an implementation variant of origin-based delegation (ROPE), combined with established financial limits and REM's existing four-verdict semantics. It is not a distinct architectural mechanism.**

This could change only if ROPE's full paper (including v2) or the full texts of AgentCap and AIS show something different. A finding there would make D1 **less** distinct, not more.

## 3. What could still be a measurable contribution (not a novelty claim)

1. **An empirical result.** Comparing, under identical conditions, how much refusal-based origin enforcement (ROPE as released) and review-based enforcement with economic limits (revised D1) each cost in utility and allow in attacks. Document-derived payment tasks, legitimate and manipulated, would be reported separately with and without a reviewer. **This would be evidence, not a mechanism.**
2. **A documented negative result.** Detector silence is not usable as an admission condition for document-derived financial values. This would be demonstrated on structurally valid forged fields. **It supports existing concerns (AutoDojo, level S) rather than being a new finding,** unless the full texts show nobody has measured it.
