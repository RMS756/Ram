# Proposed AA-REM design

[PROPOSED — SUPERVISOR APPROVAL REQUIRED]

This is Candidate A: an exact-contract authorization gate, implemented independently from `rem/`. It is a research prototype, not the approved replacement for the frozen risk-based method.

## Five-layer mapping

1. Input & Context: the trusted host supplies immutable `Contract`/`Grant` objects; tool returns enter a separate evidence store. Legacy traces supply **no structured grants**. Free text and benchmark ground truth never become grants automatically.
2. Detection: schema/type checks and canonical value comparison; separately typed external-field bindings require a contract-pinned digest.
3. Behavioral Analysis: one-use grant reservation before execution; a committed grant cannot fund a duplicate or replanned transfer. Blocking a proposal never disables a tool class for the episode.
4. Decision Engine: categorical positive/contradiction/insufficient evidence, with the explicit order below.
5. Mitigation: release original call, execute verified replacement, withhold for review, or block current call; audit records the decision.

## Rule order and semantics

- Six declared banking read tools are allowed by the simulated deployment policy. This grants neither arbitrary file access nor data-egress safety in a general application; production resource-level read permission is outside scope.
- Unknown mutation tools or invalid arguments: Block.
- No structured contract: Escalate; no reviewer means no execution, not task success.
- A supplied contract is a complete operation scope. A different operation contradicts it: Block. Incomplete natural-language intent is represented by no grant, not guessed scope.
- All executable fields must match a resolved, unspent grant, including subject/date/transaction ID when present. No wildcard subject is allowed, because it could carry sensitive data.
- Exactly one matching grant: Allow, or Modify if representation differs and trusted arguments must replace it.
- If the only differences are recipient and/or amount and a single complete grant independently supplies the correction: Modify using **the entire authorized argument map**. Missing delegated evidence or ambiguous repair never fabricates a value.
- Otherwise Block; unresolved evidence or multiple exact grants cause Escalate.
- Reserve permission before execution. A failure can leave outcome uncertain, so automatic retry does not restore a permission token. This can reduce utility and needs explicit future review handling.

External data can supply an amount or recipient only through a field explicitly delegated by trusted host policy to an independently pinned artifact. Its mere occurrence in a document is neither permission nor automatic evidence of attack. The JSON binding is intentionally narrow; arbitrary prose interpretation and semantic dataflow tracking are not implemented.

## Departures from frozen design

Every following item is [PROPOSED — SUPERVISOR APPROVAL REQUIRED]: replace the candidate's risk estimator/calibrator/expected-loss path with deterministic permission rules; introduce structured grants; require complete argument constraints; execute exact-value Modify; add one-use reservations; declare a banking read permission; exclude all task-15 and unknown-version traces for the new analysis. Original REM still runs with its original code/configs/results. No change is made to official equations, chapters or status registers.

Trust boundary: the agent and external tools cannot construct contracts or mutate trusted host memory. The `source` string documents a host assertion; it is **not cryptographic authentication**. There is no natural-language parser, remote identity service or signed-contract verifier. Concurrency and durable atomic reservation require additional production infrastructure. No production safety guarantee is claimed.
