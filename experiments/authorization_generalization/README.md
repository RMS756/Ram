# Authorization-aware REM research candidate

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

This is an exact-contract engineering prototype, **not** an approved thesis replacement or a reproduction of PROVISO/Task Shield. Its benchmark evaluation did not demonstrate improvement. Read `../../REM_ALGORITHM_IMPROVEMENT_STUDY/07_EXPERIMENT_RESULTS.md`.

A trusted host constructs the contract independently of the agent and external documents:

```python
from experiments.authorization_generalization.authorization import Contract, Grant
from experiments.authorization_generalization.candidate_policy import AuthorizationPolicy

authorized = {
    'recipient': 'GB29NWBK60161331926819',
    'amount': 12.5,
    'subject': 'invoice',
    'date': '2026-11-11',
}
contract = Contract((Grant('user-confirmed-once', 'send_money', authorized, 'trusted_user'),))
policy = AuthorizationPolicy(contract)
decision = policy.decide('send_money', {**authorized, 'amount': 999})
assert decision.verdict.value == 'modify'
assert decision.args == authorized
# The host reserves before invoking the native tool with decision.args.
policy.reserve(decision)
```

There is no natural-language intent parser or authentication service. `source='trusted_user'` is metadata supplied by trusted host code, not proof of identity. Never expose Grant construction to the model. Never substitute task reference solutions for user authorization. Supplying a contract declares complete operation scope; unknown/incomplete natural-language intent is represented by an empty contract and requires review for mutations.

Externally supplied arguments require explicit `ExternalField` delegation with an independently trusted SHA-256 digest and exact JSON field. Source occurrence alone grants no permission. The checker has no numerical authorization score. The policy is single-threaded; a production executor requires durable atomic reservations and explicit review/failure handling.

The reproduction guide lists complete commands for data extraction, baseline reproduction, cohort refits, replay, unit/integration tests and comparisons. Optional pytest markers in the original repository may skip baseline smoke tests. Synthetic test outcomes are not efficacy results.
