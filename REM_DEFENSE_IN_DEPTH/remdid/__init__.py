"""REM-DiD: proposed Defense-in-Depth research candidate for the five-layer REM architecture.

STATUS: [PROPOSED - EXPLORATORY]. Isolated from ``rem/`` (REM v1.0 is imported read-only and never modified).
Layer map (exactly five layers; audit is cross-cutting):
  L1 Input & Context  -> canonical, provenance, tae
  L2 Detection        -> detection
  L3 Behavioral       -> behavior
  L4 Decision Engine  -> decision (4A deterministic authorization, 4B = frozen REM v1.0 expected-loss decision)
  L5 Mitigation       -> enforcement (capability-bound gateway)
  cross-cutting       -> audit
"""
VERSION = "remdid-0.1-exploratory"
