# Results and discussion — update draft

Insert Table R1, Table R2 and Figure `fig_security_utility_mode_a.png` from `04_RESULTS`, with the label "Mode A, recorded traces, NO-ADAPT; MELON not executed".

**Draft paragraph:**

> **B1 versus Full REM.** Full REM reduced replay ASR from 5.5% to 0.4%, while benign task success fell from 50.9% to 31.4%, relative to the internal baseline B1 (paired differences −5.1 points, 95% interval −13.0 to −0.7, and −19.5 points, −34.1 to −7.4). In 153 attacked episodes B1 was breached and Full REM was not; there was no reverse case. B1 and Full REM share the estimator, calibration and predicates, so the difference is attributed to the decision policy as a whole. **Calibration sensitivity on the evaluated data:** B1 re-run with uncalibrated probabilities and thresholds re-selected on development data reproduced every B1 verdict (6,762 held-out steps) and outcome (3,334 replay episodes). On this dataset and these metrics, calibration showed no improvement (ECE 0.044 calibrated against 0.042 uncalibrated; Brier 0.060 in both cases). Under the declared exploratory costs, Full REM's realized decision loss was lower (0.114 against 0.652). These costs are a declared preference, not a measurement of financial loss.

> **Deployment.** Run as a separate gateway service in front of a simulated banking API, REM reproduced every decision of the in-process evaluation (0 mismatches over 3,334 episodes in each of four configurations). It added a median 0.18 ms per call, and it added no model call. These figures concern a prototype on one machine.

> **Comparison with MELON.** A controlled comparison with MELON was implemented and verified locally but could not be executed (no model access and no spending authorisation). This thesis therefore makes no comparative claim about MELON.
