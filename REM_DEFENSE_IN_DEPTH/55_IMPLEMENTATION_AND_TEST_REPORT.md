# Deliverables 13 and 18: Implementation and test report; bypass and failure-injection test suite

## 1. Code (isolated; `rem/` unchanged)

The diff of `rem/` from the start of this track (`407ef4a^`) to HEAD is 0 lines; `experiments/` and `configs/` are unchanged too.

| Module | Layer | Lines (approx.) | Purpose |
|---|---|---:|---|
| `remdid/canonical.py` | L1 | 90 | Canonical IBANs and amounts; extraction from free text |
| `remdid/provenance.py` | L1 | 220 | Source categories, field-level segmentation of tool outputs, lineage |
| `remdid/tae.py` | L1/L4A | 230 | TAE entries, HMAC integrity, session, expiry, uses, budget, matching |
| `remdid/oracle.py` | Evaluation | 70 | Offline TAE issuers (oracle, explicit, broad, none) |
| `remdid/detection.py` | L2 | 150 | Sub-detectors, failure isolation, call-linked evidence |
| `remdid/behavior.py` | L3 | 100 | Sequence rules |
| `remdid/decision.py` | L4 | 50 | Severity order, precedence |
| `remdid/enforcement.py` | L5 | 150 | Capability gateway, permits, hash-chained audit |
| `remdid/guard.py` | All | 220 | Composition per episode; failure and evasion injection |
| `remdid/replay.py` | Harness | 80 | Replay with the gateway in the execution path |

## 2. Tests

| Suite | Count | Result |
|---|---|---|
| Unit tests: `tests/test_remdid_components.py` | 24 | All pass |
| Scenario suite: `code/did3_scenarios.py` (15 attack scenarios with benign twins, plus 6 extras) | 36 runs | 0 of 15 attack scenarios executed; 0 of 15 benign twins wrongly withheld; extras as expected (fail-open 15d executes, as designed, to show what fail-safe prevents) |
| Replay gates (DiD-3) | 5 | All passed |

**Defects found by tests during development (fixed before the protocol freeze):**
1. The IBAN extractor absorbed the following word into the identifier.
2. Typed-field extraction treated dates and ids as amounts.
3. Scenario construction errors: a permit was not presented cross-session; a benign twin contained an unauthorized call.

**Defect found after the run:** the coverage measurement (amendment 50a; corrected).

## 3. Bypass and failure-injection test suite (deliverable 13)

| Kind | Where | Cases |
|---|---|---|
| Unit-level bypass | `tests/test_remdid_components.py` | Reformatting; zero-width characters; tampering; replay; expiry; cross-session; scope expansion; TOCTOU; permit reuse; detector failure; monitor failure |
| Scenario-level bypass and failure | `code/did3_scenarios.py` | The 18 threats of file 49 |
| Population-level bypass | `code/did3_run.py` | Modelled: X-* arms. Real: POP-R (reformatting) and POP-X (paraphrase) |
| Population-level failure injection | `code/did3_run.py` | F-DET, F-PROV, F-BEH, F-LEARN, F-AUTH, F-STORE, F-GW, F-AUDIT, fail-open counterfactuals |
| Detector robustness | `code/sig2_detection.py` | Original, paraphrase, zero-width, upper-case |

**Not covered:**
- Adaptive attacks: they need a live agent and model-API budget.
- Real (non-modelled) evasion of BEH and LEARN.
- Zero-width obfuscation in replay: it would need re-injection of transformed text, as was done for POP-X. Flagged as the next experiment.
