# A1-04: Revised security and trust assumptions for D1 (document delegation)

**Status.**
- Design-only, [X-P]. Nothing here is implemented or tested.
- All requirements are stated **in words**. No scoring function, threshold or probability model is introduced (see A1-11).
- Where a requirement needs a numeric value (for example a limit), it is marked **[DESIGN BLOCKED]**.

## 1. The flaw in the original condition

Original D1 condition (c), `REM_X_DESIGN/01` §3:

> "no detector fires on the source segment that carries the value"

**Why the absence of an alert proves nothing about the value.**
1. **Detectors look for instructions, not for false data.** REM's detectors (pattern, role, override, financial-directive) are designed to recognise instruction-like adversarial text. A forged payment field ("IBAN: XX…") contains no instruction. Its silence is the *expected* behaviour on a fully malicious document.
2. **Prior evidence.**
   - AutoDojo (arXiv 2606.15057, level S) reports a bill injection with no explicit instruction sentence that passed an injection detector and led the agent to pay the attacker.
   - REM-DiD's own SIG-2 study found the pattern, role and override detectors fall to zero recall under paraphrase, and every detector failed under zero-width obfuscation (`REM_DEFENSE_IN_DEPTH/43`).
3. **In indirect prompt injection, the attacker controls the document.** Detection asks "does this text try to steer the agent?" Authorization needs "is this the payee the user intends to pay?" Nothing inside an attacker-controlled document can answer the second question.
4. **A correct parser does not help.** Deterministic extraction guarantees only that the tool argument equals what the document's field says. It does **not** show the field is genuine.

**Conclusion.**
- Detector output may **raise** suspicion and lead to escalation.
- The absence of an alert must **never** count as evidence of authenticity or authorization.
- Original D1 would admit an attacker's payee from any well-formed forged invoice. **Its earlier implied claim of "zero successful attacks, including attacks injected into the delegated document" is withdrawn.**

## 2. Case analysis

**Column meanings.**
- *Original D1* is the behaviour of the design in `REM_X_DESIGN/01`.
- *Revised model* refers to the outcomes defined in §3.

| # | Case | Original D1 | Revised model | Residual risk |
|---|---|---|---|---|
| 1 | Fake IBAN placed in a valid-looking invoice field (genuine IBAN replaced) | **Admitted**: unique field, extraction succeeds, no instruction text | Payee not confirmed by any independent trusted reference → **Delegation requiring additional approval**. If the payee *name* matches a known payee but the account differs → **Suspicious** | Depends on the reviewer. A reviewer shown only the document cannot tell either |
| 2 | Modified amount in a genuine invoice (payee genuine) | Admitted if within caps | Payee verified; amount **cannot be authenticated from the document**. Within the user-declared envelope → may be **Verified bounded delegation**; otherwise **Rejected** | Loss **bounded by the envelope, not prevented**. Must be reported as bounded exposure, not as zero attacks |
| 3 | Duplicate beneficiary fields | Undefined (parser might take the first) | **Ambiguous / unverifiable.** The parser must report multiplicity and never choose | None, if multiplicity detection is correct |
| 4 | Two conflicting payment amounts | Undefined | **Ambiguous / unverifiable** | As case 3 |
| 5 | Instruction-free data manipulation | Admitted (detectors silent) | Decided by independent payee verification and economic limits, **not** by detection | As cases 1–2 |
| 6 | Unicode and formatting obfuscation (zero-width characters, homoglyphs, mixed scripts, unusual spacing) | Depends on canonicalization; detectors fail (SIG-2) | Any character outside the declared canonical alphabet of the field → **Ambiguous**. Mixed-script or confusable characters in a payee field → **Suspicious** | Canonicalization defects; needs a published confusables reference (see §5) |
| 7 | Document structure mimicry (an added "IBAN:" line formatted like a real field) | Admitted if it is the only line; ambiguous if it duplicates a real one | Duplicate → **Ambiguous**; sole line → same as case 1 | As case 1 |
| 8 | Malicious document from a source the user explicitly named | **Admitted**: naming the source was treated as authorizing its content | Naming a source records the user's **intent** to pay *that* bill. It is not evidence of the bill's **integrity**. Without source identity and integrity evidence → **Delegation requiring additional approval** | Depends on the reviewer; or on an authenticated document channel, which AgentDojo lacks |
| 9 | Parser extracts a field correctly from compromised content | Admitted | Correct extraction gives field binding only. Acceptance needs the evidence in §4 | As case 1 |

## 3. Revised decision model: five outcomes, decided by affirmative evidence

**Two principles:**
- Each outcome is decided by **which affirmative evidence is present**, not by the absence of alerts.
- Detector findings can only move a case **towards** more restriction.

| Outcome | Required evidence, all of it (stated in words) | Proposed REM verdict [PD] |
|---|---|---|
| **O1 Verified bounded delegation** | (i) The user's trusted instruction delegates **these fields** of **this operation** to **this source**. (ii) The value is extracted from exactly one schema-declared field, in canonical form, with no competing candidate. (iii) **The payee is confirmed by an independent trusted reference** (§4.2), not by the document. (iv) The amount and cumulative totals lie within the user-declared economic envelope. (v) No detector raises evidence on the source, and no detector is unavailable. (vi) Execution goes through a single-use permit with an independent adapter re-check | Allow |
| **O2 Delegation requiring additional approval** | (i), (ii), (iv) hold, but (iii) does not: the payee is new or unconfirmed | Escalate: withhold pending review; show the reviewer the exact extracted payee, amount and source location |
| **O3 Ambiguous or unverifiable document** | (ii) fails (no field, several candidates, conflicting values, non-canonical characters), or a required detector or reference lookup is unavailable | Escalate |
| **O4 Suspicious document** | Any affirmative suspicion. A detector fires on the source. The payee name matches a known payee but the account differs. Confusable or mixed-script characters appear in a payee field. The document's values contradict the user's own records | Escalate, marked suspicious. **Whether suspicion should instead lead to Block is a supervisor decision** |
| **O5 Rejected transaction** | The operation or field was not delegated; the amount or cumulative total exceeds the envelope; the payee is on a deny list; the permit or adapter check fails | Block: prevent execution of the current proposed action |

**Notes on the verdicts.**
- Verdicts keep the frozen semantics:
  - Allow releases the current action;
  - Escalate withholds it pending review;
  - Block prevents the current action.
- No episode-level restriction is introduced.
- **Precedence:** the most restrictive applicable outcome wins.

**Where this leaves the AgentDojo bill task (user_task_0).** There is no independent payee reference and no reviewer, so the bill task falls under **O2**. **Automatic completion is not possible under the revised model.** This is the same practical outcome as ROPE's refusal, except that the call is withheld for review rather than refused.

## 4. Required evidence, defined in words

### 4.1 Source identity

Evidence that the document comes from the party it claims to come from. Examples:
- a signature by the issuer, verified against a key the user or bank already trusts;
- retrieval from an authenticated system of record, such as the bank's own e-invoice inbox.

**What does not count:**
- a file name;
- a sender name written inside the document;
- the fact that the user named the file.

**In AgentDojo banking, no such evidence exists.** Files are plain strings.

### 4.2 Payee confirmation by an independent trusted reference

Evidence, **not taken from the document**, that the extracted account belongs to the payee the user intends. Candidate references:
- the user's own past payments to that account (ROPE's "me"/record admission is the precedent);
- a payee directory maintained by the user;
- a pinned value in the authorization record;
- a bank payee-verification service (name-to-account check).

**For the last item:** the operational details of such services must be taken from their published specifications, not assumed.

### 4.3 Document integrity

Evidence that the content was not altered after issuance. **Without a source-identity mechanism (4.1) this cannot be established.** A hash of the document taken when the agent reads it proves only that the agent saw *this* content.

### 4.4 Field uniqueness

Exactly one candidate value for each delegated field:
- at the schema-declared location;
- in canonical form;
- with no other value of the same type in the document that could be read as that field.

The parser **reports** multiplicity; it never chooses.

### 4.5 Economic validation

The amount, its currency, the per-call value and the cumulative committed-plus-reserved value lie within limits the **user** declared.

**This limits loss. It does not verify the amount.** The limit values are **[DESIGN BLOCKED]** (A1-09).

### 4.6 Consistency checks

For example, line items adding up to the stated total. These may raise suspicion when they fail. **They are not evidence of authenticity when they pass:** a forger can make a consistent invoice.

## 5. Consequences for claims

1. **No zero-attack claim for document-derived payees.** Under O2, security equals the reviewer's ability to detect the forgery. The DiD-3 idealized reviewer is an upper bound and **does not model** a human looking at a well-formed forged bill.
2. **Amounts.** For document-derived amounts with a verified payee, the claim is **bounded exposure**: no transfer beyond the declared envelope. It is not prevention.
3. **Detector role.** Escalation trigger only (O4). Never a release condition.
4. **Character confusables.** Judging "confusable" or "mixed-script" characters must use a published reference (for example the Unicode Consortium's security mechanisms for identifiers). It must not use an invented list. The choice is [DESIGN BLOCKED] until a reference is selected and verified.
