"""Phase 4: labelled step dataset from recorded AgentDojo traces (EXPLORATORY).

Usage: python experiments/pilot/build_dataset.py
Writes results/pilot/steps.pkl and results/pilot/dataset_summary.json.
"""

from __future__ import annotations

import collections
import os
import pickle

from common import RESULTS, RUNS, make_setup, provenance, write_json

from rem.integration.agentdojo_traces import ambiguous_pairs, iter_episode_paths, load_episode
from rem.integration.steps import build_steps


def main() -> None:
    st = make_setup()
    D = st.cfg["data"]
    amb = ambiguous_pairs(st.labeler)
    groups = []  # (role, pipeline, attack)
    for p in D["backbones_undefended"]:
        groups += [("primary", p, D["primary_attack_template"]), ("primary", p, "none")]
    ct = D["cross_template_check"]
    groups += [("cross_template", ct["pipeline"], t) for t in ct["templates"]]
    for p in D["distributed_defense_pipelines"]:
        groups += [("defense", p, D["primary_attack_template"]), ("defense", p, "none")]

    episodes, steps = [], []
    summary = collections.defaultdict(lambda: collections.Counter())
    for role, pipe, attack in groups:
        for path in iter_episode_paths(RUNS, pipe, D["suite"], attack):
            ep = load_episode(path, pipeline=pipe)
            key = f"{role}|{pipe}|{attack}"
            summary[key]["files"] += 1
            if ep.error and D["exclude_errored_episodes"]:
                summary[key]["excluded_error"] += 1
                continue
            if ep.injection_task_id and (ep.user_task_id, ep.injection_task_id) in amb:
                summary[key]["excluded_AM1_ambiguous"] += 1
                continue
            s = build_steps(ep, st.spec, st.detector, st.tier_map, st.labeler)
            episodes.append({"role": role, "episode": ep})
            steps.append((role, ep.episode_id, s))
            summary[key]["episodes"] += 1
            summary[key]["steps"] += len(s)
            summary[key]["positive_steps"] += sum(x.label for x in s)
            summary[key]["episodes_with_positive"] += int(any(x.label for x in s))
            summary[key]["recorded_security_true"] += int(ep.security) if ep.attacked else 0
            summary[key]["recorded_utility_true"] += int(ep.utility)
            # label/outcome consistency (label audit, all episodes)
            if ep.attacked:
                pos = any(x.label for x in s)
                summary[key][f"consistency_pos{int(pos)}_sec{int(ep.security)}"] += 1
                summary[key]["near_miss_attacker_value_unlabelled"] += sum(
                    1 for x in s if x.attacker_key_match and not x.label
                )
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "steps.pkl"), "wb") as fh:
        pickle.dump({"episodes": episodes, "steps": steps}, fh)
    write_json(
        "dataset_summary.json",
        {"provenance": provenance(), "ambiguous_pairs_AM1": sorted(amb),
         "groups": {k: dict(v) for k, v in summary.items()}},
    )
    tot = collections.Counter()
    for k, v in summary.items():
        if k.startswith("primary"):
            tot.update(v)
    print(dict(tot))


if __name__ == "__main__":
    main()
