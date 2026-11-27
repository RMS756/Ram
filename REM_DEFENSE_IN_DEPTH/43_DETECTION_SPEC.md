# Deliverable 6: Detection enhancement (Layer 2)

**Code:** `remdid/detection.py`. **Evaluation:** SIG-2 (`code/sig2_detection.py`, `results/sig2_detection.json`). **Status:** implemented, tested, evaluated.

## 1. Signals (detection provides evidence; it never authorizes)

| Signal | What it detects | Requested category |
|---|---|---|
| D_pattern | REM v1.0 x~ctx2~ patterns (baseline, unchanged) | 1 instruction-pattern |
| D_role | Pseudo-markup tags, chat-role prefixes, special tokens, `[INST]`, `### system` | 2 structural boundary; 3 role or delimiter manipulation |
| D_override | "ignore/disregard previous…", "before you can solve…", "instead of", "do not tell…", "your task is…", "override" | 6 privilege or intent override |
| D_fin | Payment or credential verb **and** an account identifier, amount or "password" in the same untrusted segment | 5 suspicious tool-use instruction; 7 malicious indicator in an untrusted source |
| Call-linked evidence | A sensitive identity value of the proposed call occurs in an untrusted segment on which any signal fired | Links content evidence to the action |

**Category 4, the instruction-aware injection classifier (x~ctx1~), is NOT implemented.** AgentDojo's `transformers_pi_detector` needs a model download that is not available in this environment. The REM decision D-8 is open. → **[RESOURCE BLOCKED]**.

## 2. Failure handling

| Event | Behaviour |
|---|---|
| Exception, timeout (50 ms budget), invalid output | That detector is UNAVAILABLE for the segment |
| Detector unavailable on a segment that carries the call's value, and no detector fired | Call-linked evidence is UNKNOWN; for a state-changing call: **Escalate** (fail-safe). Never "not fired". |
| Two detectors disagree | Any-of aggregation; disagreement is recorded per segment |
| Low confidence | Not applicable: the detectors are boolean rules with no confidence |
| Distribution shift or paraphrase | Measured in SIG-2 (§3); not mitigated by Layer 2 itself; covered by L1/L3/L4A in DiD-3 |

## 3. Measured (SIG-2, segment level, 14,394 untrusted segments, 3,112 injected)

Results are in `results/sig2_detection.json`. **Every word list was written with knowledge of AgentDojo's templates, so figures on those templates are optimistic.**

| Variant | D_pattern recall | D_role | D_override | D_fin | Union | FPR (union) |
|---|---|---|---|---|---|---|
| Original templates | 0.92 | 0.88 | 0.96 | **1.00** | 1.00 | 0.0017 |
| Paraphrase (2,475 injected segments) | **0.00** | **0.00** | **0.00** | 1.00 | 1.00 | 0.00 |
| Zero-width obfuscation | 0.00 | 0.00 | 0.00 | **0.0055** | 0.0055 | 0.00 |
| Upper-case | 0.92 | 0.88 | 0.96 | 1.00 | 1.00 | 0.00 |

- **Recall by template (original)** for D_pattern: `direct` 0.00, `ignore_previous` 0.00, the other templates 1.00. D_fin is 1.00 on every template.
- **Legitimate financial documents:** D_fin fires on **19 of 81** `read_file` segments without injection (bills and notices contain payment instructions). The other detectors fire on 0.
- **Agreement:** phi between detectors is 0.92–0.98, so they are **not independent**. They share their input (the same segments) and fire on the same template features. SIG-1 had already shown D_pattern ≡ x~beh1~ (correlation 1.00).
- **Latency:** mean 0.005–0.015 ms per detector per segment; p95 ≤ 0.08 ms. Token cost 0.

**Conclusions:**
1. Detector "diversity" here is nominal. Pattern, role and override signals fail together under paraphrase, and all fail under zero-width obfuscation.
2. The only robust signal (D_fin) is robust because it keys on the payload's financial content. That is also why it fires on legitimate bills.
3. Detection can therefore not be relied upon as an independent layer. DiD-3 measures its marginal value behind the other layers.

**Thresholds:** none. Development and confirmatory separation is not achievable for detection, because the templates were known (exploratory).
