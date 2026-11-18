"""Held-out recorded-trace population H (selection rule fixed before any arm was run on it).

Source: AgentDojo's own recorded banking runs of gpt-4o-2024-05-13 with four in-pipeline prompt defences, which no REM
code had loaded before (checked by repository search: only cited as published counts):
  gpt-4o-2024-05-13-repeat_user_prompt, -spotlighting_with_delimiting, -tool_filter, -transformers_pi_detector
attacks: important_instructions (attacked) and none (benign).
Rules (same as the earlier fresh population, improve.load_fresh): errored episodes excluded; ambiguous (user, injection)
pairs of the reference labeller excluded; S1 fold of an attacked episode = its injection task; fold of a benign episode by
the round-robin user-task assignment over the folds. Eligibility (applied at report time, same rule as dev2): an episode is
kept iff the B0 replay reproduces its recorded utility and security without error.
What H is: unseen AGENT TRACES (other prompt defences inside the agent pipeline) of the SAME 16 user tasks and 9 attacks.
What H is not: unseen tasks or unseen attack objectives.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "improve_study"))

PIPELINES = ["gpt-4o-2024-05-13-repeat_user_prompt", "gpt-4o-2024-05-13-spotlighting_with_delimiting",
             "gpt-4o-2024-05-13-tool_filter", "gpt-4o-2024-05-13-transformers_pi_detector"]
ATTACKS = ["important_instructions"]


def load_heldout(st, data):
    import improve as I
    saved = dict(I.FRESH)
    try:
        I.FRESH.clear()
        for n, pipe in enumerate(PIPELINES):
            I.FRESH[f"H-{n}"] = (pipe, ATTACKS, True)
        return I.load_fresh(st, data)
    finally:
        I.FRESH.clear()
        I.FRESH.update(saved)
