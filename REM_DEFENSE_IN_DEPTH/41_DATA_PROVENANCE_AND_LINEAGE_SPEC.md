# Deliverable 5: Data provenance and financial data lineage (Layer 1)

**Code:** `remdid/canonical.py`, `remdid/provenance.py`. **Tests:** `tests/test_remdid_components.py` (L1 group).

**Status:** implemented, unit-tested, evaluated in replay (DiD-3).

## 1. Source categories

| Category | Assigned to | Trust |
|---|---|---|
| `authenticated_user_instruction` | The user's request | Trusted |
| `authenticated_system_configuration` | System prompt | Trusted |
| `trusted_financial_system_field` | Typed fields of bank API results: `recipient`, `sender`, `iban`, `amount`, `balance`, `id`, dates, user info | Trusted origin |
| `trusted_authorization_envelope` | Pinned TAE fields | Trusted for authorization |
| `external_document` | `read_file` content (bills, notices) | Untrusted |
| `free_text_field_in_financial_record` | `subject` of a transaction: authentic record, attacker-writable text | Untrusted |
| `tool_output_unparsed` | Any output that cannot be parsed | Untrusted |

**Trust is about origin, not truth.**
- A trusted field can be stale or wrong. For example, the friend's IBAN in the history is authentic, but paying it is not thereby authorized.
- An untrusted value can be correct. For example, the bill's payee in `user_task_0` is legitimate.
- Authorization (Layer 4A) and provenance are therefore separate checks.

**Assumption AS-P1:** the typed fields of the banking API are authentic (system of record). Under this assumption the attacker can write only free text: transaction subjects and file contents. This holds in AgentDojo banking (L), but **not** for an attacker who can create real transactions with attacker-chosen typed fields.

## 2. Canonical forms (declared rules)

**IBAN-like identifiers.** These rules are applied:
- remove spaces, hyphens, dots, NBSP and zero-width characters;
- upper-case the result;
- require 2 letters, 2 digits and 10–30 alphanumerics.

Extraction from free text appends a separator-delimited group only if the group contains a digit or is an upper-case group of at most 4 letters. A following word is therefore never absorbed. This bug was found by unit test during development and fixed.

**Amounts.** Exact `Decimal` value, so that `98.70 == 98.7 == "$98.7"`.
- In typed records, amounts are read only from amount fields; dates and ids are never amount evidence.
- In free text, every number is a candidate.

**Free-text fields** (password, street, city, names) use whitespace- and case-normalized substring matching, with a minimum length of 3.

## 3. Lineage of a sensitive argument

Sensitive fields per operation:

| Operation | Fields |
|---|---|
| `send_money`, `schedule_transaction` | recipient, amount |
| `update_scheduled_transaction` | id, recipient, amount |
| `update_password` | password |
| `update_user_info` | first_name, last_name, street, city |

For each field the lineage record holds:
- canonical value;
- set of source categories in which the value occurs;
- transformations (`verbatim` / `canonicalized`);
- the segment indices.

**Status of a field's lineage:**

| Status | Meaning |
|---|---|
| `trusted_only` | Found only in trusted sources |
| `untrusted_only` | Found only in untrusted sources |
| `trusted_and_untrusted` | Found in both |
| `no_matching_source` | Not found anywhere: derived, computed or absent; never upgraded to trusted |
| `unparseable_value` | The value cannot be parsed |

The study's requirements are met as follows:
- copying and reformatting are traced, through canonical forms;
- passing a value between tools is traced: every executed tool output is segmented in order;
- conversion into tool arguments is traced at call time;
- summarization or paraphrase by the agent is **not** traced: there is no source match, so the status is MISSING (fail-safe for identity fields);
- combining several values is **not** traced: a computed amount is MISSING and is never "trusted".

## 4. Limitation (fundamental)

**REM mediates a black-box agent.** Lineage is **inferred** from the co-occurrence of canonical values with labelled segments. It is not tracked through the agent's computation, as CaMeL's interpreter tracks it.

- An attacker value that coincides with a trusted value cannot be distinguished. Example: `user_task_15`, where the user's new landlord **is** the attacker account.
- A trusted-looking value laundered through an untrusted path is not detected.

Real data-flow integrity needs either an interpreter architecture (CaMeL) or model-internal signals (RTBAS attention). Both are outside REM's black-box design.

## 5. Tests (L1 list of the study)

| Required test | Unit test | Scenario |
|---|---|---|
| Trusted source with unauthorized action | `test_trusted_source_value_is_trusted_but_not_authorized` | 03 |
| Untrusted source with authorized-looking recipient | — | 13, 18 |
| Reformatted IBAN | `test_canonical_iban_reformatted_equal`, `test_reformatted_iban_from_untrusted_field_is_untrusted` | 02 |
| Recipient substitution | `test_tae_violations` | 01 |
| Amount modification | `test_tae_violations` | 03 |
| Currency modification | `test_tae_violations` | 04 |
| Reused authorization | `test_tae_reuse_expiry_cross_session_tamper` | 06 |
| Expired authorization | same | 08 |
| Scope expansion | same (tamper), `test_gateway_attenuation_never_widens` | — |
| Missing provenance | `test_missing_provenance_for_unseen_value` | 14 |
| Conflicting provenance | `test_conflicting_provenance_is_mixed` | 13 |
| Derived values from multiple sources | `test_derived_amount_from_multiple_sources_is_never_trusted` | — |

**Provenance accuracy and lineage completeness on the benchmark** are measured indirectly. Every attack-labeled call's recipient in POP-P and POP-R originates only from untrusted segments, and the coverage analysis in `51_DID3_RESULTS.md` reports which calls PROV covers.

**No independent ground truth of true dataflow exists**, so provenance *accuracy* in the strict sense is not measurable here. This is a stated limitation.
