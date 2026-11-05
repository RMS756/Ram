# Methodology — update draft

1. **Experimental configurations** (add to §3.11.7, keeping the existing B0/B1 text):
   - **REM-Lite (ablation).** Same features and fitted ridge model; uncalibrated probability p̃ = σ(s); Block/Modify thresholds selected on development data only (benign inner out-of-fold probabilities of each fold's fitting portion) at the declared operating points α_blk = 0.01 and α_mod = 0.05; same predicates and mitigation.
   - Because threshold selection by ranking is invariant to the strictly increasing calibration map (Section 3.7.7), REM-Lite is verdict-equivalent to B1. It is introduced to make explicit that the comparison REM vs B1 is the ablation of {calibration + expected-loss decision}.
   - **MELON (external baseline, live mode only).** The official implementation, unmodified. It needs AgentDojo 0.1.29; two compatibility measures apply identically to all conditions.
2. **Evaluation modes:** Mode A, recorded traces (offline held-out; NO-ADAPT replay; deployment simulation); Mode B, live LLM agent in the simulated AgentDojo banking environment (protocol only, not executed).
3. **Metrics:** unchanged definitions (§3.12). Add decision latency per call, end-to-end episode latency, and LLM calls added by the defence.
4. **No change** to the architecture, the equations, the cost matrix or the estimator.
