# Results and discussion — update draft

Insert Table R1, Table R2 and Figure `fig_security_utility_mode_a.png` from `04_RESULTS`, with the label "Mode A, recorded traces, NO-ADAPT; MELON not executed".

**Draft paragraph:**

> **Ablation of the decision mechanism.** The ablated variant REM-Lite uses the same fitted model with uncalibrated probabilities and fixed operating-point thresholds selected on development data. It produced verdicts identical to those of the consequence-independent baseline B1 on all 6,762 held-out steps and all 3,334 replayed episodes, because rank-selected thresholds are unaffected by a strictly increasing calibration map. Relative to REM-Lite, Full REM reduced the replay attack success rate from 0.055 to 0.004 (paired difference −0.051, 95% interval −0.130 to −0.007). In 153 attacked episodes REM-Lite was breached and Full REM was not; there was no reverse case. The reduction came at a cost: benign utility fell by 0.195 (−0.341 to −0.074) and utility under attack by 0.151. The difference is therefore attributable to the expected-loss decision with consequence tiers and the Escalate option, not to calibration, which by itself showed no improvement (ECE 0.044 calibrated against 0.042 uncalibrated). Under the declared exploratory costs, Full REM's realized decision loss was lower (0.114 against 0.652). These costs are a declared preference, not a measurement of financial loss.

> **Deployment.** Run as a separate gateway service in front of a simulated banking API, REM reproduced every decision of the in-process evaluation (0 mismatches over 3,334 episodes in each of four configurations). It added a median 0.18 ms per call, and it added no model call. These figures concern a prototype on one machine.

> **Comparison with MELON.** A controlled comparison with MELON was implemented and verified locally but could not be executed (no model access and no spending authorisation). This thesis therefore makes no comparative claim about MELON.
