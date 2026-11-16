# Addendum to the protocol: proposals from Progent's related work (Section 11 of the task, received 16 November 2026)

**Status:** `[PROPOSED - EXPLORATORY]`. Committed locally **after** every result of `PROTOCOL.md` was read and **before** either arm below was replayed. The frozen modules, the first results and `guards.py` are unchanged; the new code is in `cedar_front.py`, `guards_s11.py` and `cs_run_s11.py`.

## 1. What was known when this was written

All results of the main study (`results/results.json`), in particular:

- the guard used alone (GV) has the same outcomes as HV on every population, the probe and all 43 fixtures; behind the authority front the learned score changed no decision;
- on the primary recordings every attack-labelled call to a restricted tool is stopped by the front (921 of 921 recorded steps by the offline evidence), so **no attack-labelled call reaches the stage at which a learner, a cutoff or a provenance rule acts**;
- behind the front the primary recordings have 989 calls whose value the request confirms and 145 whose value it does not; among the 145, REM's provenance indicator fires for 28; for 55 of the 989 the indicator is unavailable, and the declared predicate D2 withholds those in GV, L4 and HV.

It follows that **neither arm below can show a security gain on the existing recordings**. The addendum measures something else: decision parity for the first, and the utility cost of a provenance rule for the second.

## 2. Sources read for this addendum

| Work | What was read | Not read |
|---|---|---|
| Cedar | Official documentation source, `github.com/cedar-policy/cedar-docs` at `4091567` (13 Nov 2026), "How Cedar authorization works" (request model, algorithm, default deny, forbid overrides permit, skip on error, policy evaluation) | The Cedar paper cited by Progent; no academic claim about Cedar is made |
| FIDES | The authors' tutorial repository `github.com/microsoft/fides` at `669c046` (30 May 2025): README and the text of `Tutorial.ipynb` (planning loop, lattices, labelled values, dynamic taint tracking, policies on labelled traces) | The paper, arXiv:2505.23643 (host blocked) |
| CaMeL | The authors' repository `google-research/camel-prompt-injection`, read in the earlier study (README and interpreter structure) | The paper, arXiv:2503.18813 (host blocked) |
| IsolateGPT | Nothing | Paper and code not read; only a design-level remark is made, marked as unverified |

## 3. Arms

| Arm | Exactly what changes relative to GV | What stays fixed | Kind of study |
|---|---|---|---|
| **GVc** | The release decision of each restricted call is taken by nine Cedar policies (one permit, eight forbids) over a typed context that REM computes: authority, permission status, effect, binding, condition, fulfilment, direct-value outcome, declared predicate. A wrapper withholds on any authorizer error, on request-validation failure and on any answer other than Allow | Every constraint; evidence; mitigation | Policy-engine implementation study |
| **GVp** | One added rule: a restricted call that passes the front with status *unknown* is released only if the provenance indicator x_act1 is available and does not fire; otherwise Escalate (withheld, no reviewer) | Front, direct-value constraint, predicates | Additional-enforcement study (rule only) |

The learned counterpart with the same provenance input already exists: HV's estimator has x_act1 to x_act3 among its nine inputs. GV (no provenance input, no learner), GVp (provenance rule, no learner) and HV (provenance as learned evidence) form the matched set asked for in Section 11.5.

Not built, with reasons (`11_RELATED_WORK_PROPOSALS.md`): information-flow labels propagated through the planner (FIDES proper), a control/data-flow interpreter (CaMeL proper), application isolation or a review workflow (IsolateGPT), policies generated or updated by a model, an SMT check of policy expansion.

## 4. Evaluation and hypotheses

Same populations, probe, fixtures and statistics as `PROTOCOL.md`. Neither arm has a fitted quantity, so S2 equals S1.

- **GVc.** Every restricted call of every replay has the same release decision as under GV, and no authorizer error occurs. Any difference is investigated call by call before anything is said about Cedar. Reported: calls decided by Cedar, errors, decision time.
- **GVp.** No change in successful attacks (none is possible on these recordings); fewer legitimate calls released and no more completed tasks than GV; no change in unsafe fixture releases (GV has none); possibly more legitimate fixture calls withheld.

## 5. Wording

Decision parity shows that Cedar can carry these constraints. It is not a security or utility improvement, and Cedar is not credited with any guarantee about intent, history or policy expansion. A provenance rule that costs tasks and removes no attack on these recordings is reported as such; that is not evidence that provenance has no value against attacks the recordings do not contain.
