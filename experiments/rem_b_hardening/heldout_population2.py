"""Second held-out recorded-trace population H2 (REM-B hardening study). Selection rule fixed BEFORE any arm is run on it.

Sources (AgentDojo's own recorded banking runs; checked by repository search on 19 November 2026):
  H2a  claude-3-sonnet-20240229-repeat_user_prompt x {important_instructions (attacked), none (benign)}
       -> never loaded by any REM code or study before (pristine).
  H2b  gpt-4o-2024-05-13 x {direct, ignore_previous, important_instructions_no_names, injecagent, tool_knowledge}
       (attacked only; its benign runs are in the primary population)
       -> loaded once on 11 November 2026 as the "cross_template" role of the pilot (configs/exploratory/pilot_e0.yaml)
          and of REM_Authorization_Generalization_Study, for OLDER arms only; never used to design or score C1, REM-B or
          any mechanism of this study. Disclosed as previously used, not pristine.
Excluded by rule: the denial-of-service attack families (captcha_dos, dos, felony_dos, offensive_email_dos,
swearwords_dos): their objective is to stop the agent, not an unauthorised state change, which is outside the threat
model (03 of the redesign study).
Episode rules (identical to the earlier populations, improve.load_fresh): errored episodes excluded; ambiguous
(user, injection) pairs of the reference labeller excluded; fold of an attacked episode = its injection task; benign by the
round-robin user-task assignment. Eligibility (at report time): the B0 replay reproduces the recorded utility and security.
What H2 is: unseen agent traces AND unseen attack phrasings (H2b) of the SAME 16 user tasks and 9 injection tasks.
What H2 is not: unseen tasks or unseen attack objectives.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "improve_study"))

SOURCES = {
    "H2a-0": ("claude-3-sonnet-20240229-repeat_user_prompt", ["important_instructions"], True),
    "H2b-0": ("gpt-4o-2024-05-13", ["direct", "ignore_previous", "important_instructions_no_names", "injecagent", "tool_knowledge"], False),
}


def load_heldout2(st, data):
    import improve as I
    saved = dict(I.FRESH)
    try:
        I.FRESH.clear()
        I.FRESH.update(SOURCES)
        return I.load_fresh(st, data)
    finally:
        I.FRESH.clear()
        I.FRESH.update(saved)
