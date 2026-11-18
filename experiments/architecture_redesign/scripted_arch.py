"""Scripted closed loop for this study: the controlled study's harness (improvement_controlled/scripted.py, imported
unchanged) plus one additional order of the obedient agent, 'injection_twice_after_first_read' (the injection's calls are
issued twice right after the user's first read: repeated attacker operation)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "improvement_controlled"))
import scripted as BASE  # noqa: E402

MODES = ("user_first", "injection_first", "injection_after_first_read", "injection_twice_after_first_read")
_make = BASE.make_agent_class


def make_agent_class():
    Agent = _make()

    class Agent2(Agent):
        def query(self, query, runtime, env, messages=[], extra_args={}):
            if self.queue is None and self.mode == "injection_twice_after_first_read":
                u = list(self.ut.ground_truth(env))
                i = list(self.it.ground_truth(env)) if self.it else []
                reads = [n for n, c in enumerate(u) if c.function.startswith(("get_", "read_"))]
                cut = reads[0] + 1 if reads else 0
                self.queue = u[:cut] + i + i + u[cut:]
            return super().query(query, runtime, env, messages, extra_args)
    return Agent2


BASE.make_agent_class = make_agent_class
run = BASE.run
