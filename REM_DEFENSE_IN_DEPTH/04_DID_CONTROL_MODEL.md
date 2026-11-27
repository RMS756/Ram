# Defense-in-Depth threat and control model for REM (five layers, unchanged)

## 1. Attack chain under indirect prompt injection (AD-1)

| Step | What happens |
|---|---|
| T1 | Attacker content enters through a tool output (observation boundary TB-2) |
| T2 | The content contains an instruction, an attacker value (account, password, amount), or both |
| T3 | The agent proposes a state-changing call whose operation or arguments serve the attacker |
| T4 | The call crosses the action boundary (TB-3) and changes the bank state |

## 2. Controls mapped to the chain

| Control | Layer | Chain step observed | What it detects | What defeats it (evasion route) | Independent of |
|---|---|---|---|---|---|
| Provenance labels and entity extraction | Input & Context | T1 | Origin of every value | Nothing directly. All later signals inherit its errors. | — (foundation) |
| K2 instruction pattern x~ctx2~ | Detection | T2 | Imperative or tool-naming text in untrusted content | Paraphrase; injections without trigger words | **Not independent:** x~beh1~ is defined through it |
| x~ctx1~ classifier | Detection | T2 | Injected instructions (learned) | — | **Not implemented** |
| K3a x~beh1~ | Behavioral | T2→T3 | A call right after an instruction-bearing result | As K2 | Coupled to K2 |
| K3b x~beh2~ | Behavioral | T3 | Repeated identical calls | Avoid repetition | Yes |
| K3c x~beh3~ | Behavioral | T3 | First use of a higher privilege level in the episode | None in practice: any first state-changing call fires it, legitimate or not | Yes (low specificity) |
| K3d x~beh4~ | Behavioral | T3 | Tool transition unseen in benign data | Mimic benign tool order | Yes |
| K4 x~act1~ | Behavioral (action) | T3 | Key argument found only in untrusted content | Reformat the value (spaces, fragments); exact match fails | Yes |
| K5 x~act2~ | Behavioral (action) | T3 | Recipient absent from the user's request | Use a recipient the user named. In AgentDojo banking v1, only user_task_15 allows this. | Yes |
| K6 x~act3~ | Behavioral (action) | T3 | A sensitive value sent outward | Do not exfiltrate | Yes |
| K7 learned expected-loss decision | Decision Engine | T3→T4 | Combines K2–K6 with consequence tier and costs | Defeat enough of the evidence | Depends on K2–K6 |
| K8 predicates D1/D2 | Decision Engine | T3→T4 | Prohibited tools; missing evidence at high tiers | Not triggered by the benchmark's attacks | Yes |
| K9 enforcement | Mitigation | T4 | Withholds the call | Bypassing REM itself (excluded: AS-3) | Yes |

## 3. What Defense in Depth means for REM, operationally

REM has Defense in Depth against a threat if defeating any one control on the chain still leaves the threat stopped. This must hold for single controls and, more importantly, for evidence families, because an attacker's single change can silence several correlated signals. This is measured with three questions:

1. **Coverage.** How many independent controls fire on each attack call? (DiD-1, A1)
2. **Single-control evasion.** Is the decision preserved when one control is defeated? (DiD-1 A2; DiD-2)
3. **Family evasion.** Is it preserved when a family is defeated? (DiD-1 A3; DiD-2)

**Training-time ablation answers a different question:** is the control needed when nothing is evaded? Earlier chapters answered only that question.

## 4. Evidence status (after DiD-1 and DiD-2)

| Property | Status |
|---|---|
| Depth against a single evidence control | Validated, on recorded steps and in replay (development data) |
| Depth against one evidence family | Partial. Two families each cover most attacks, but each leaves one class of attack uncovered. |
| Depth against both families | None: REM falls to the no-defense level |
| Contribution of the Detection layer to depth | None measured |
| Depth of REM v1.1 | Lost: one family left |
