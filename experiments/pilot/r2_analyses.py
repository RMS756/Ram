"""R2 analyses (EXPLORATORY): breakdowns by tier/action, replay-failure analysis,
equal-escalation comparison summary, and the human label-audit package.

Requires the stages crossfit, rmod, observe and replay to have run in
$PILOT_RESULTS_DIR (default results/pilot).
"""

from __future__ import annotations

import collections
import csv
import os

import numpy as np

from common import RESULTS, load_config, make_setup, provenance, write_json
from data import build
from run_main import B, SEED, load_state
from rem.evaluation.bootstrap import grouped_bootstrap

CFG = load_config()
st = make_setup()
data = build("primary")
cats = CFG["consequence"]["categories"]
cat_of = {t: c for c, ts in cats.items() for t in ts}
kw = dict(resamples=B["resamples"], seed=SEED, level=B["interval"])


def observe_breakdown():
    res = load_state("observe_verdicts")
    out = {}
    for name in ("REM_step_level", "REMnoEsc_step_level", "B1"):
        vs = np.asarray(res[name][0], dtype=object)
        rows = []
        keys = sorted({(s.tier, cat_of[s.tool]) for s in data.steps})
        for tier, cat in keys:
            idx = [i for i, s in enumerate(data.steps) if s.tier == tier and cat_of[s.tool] == cat]
            y = data.y[idx]
            v = vs[idx]
            row = {"tier": int(tier), "category": cat, "n_y0": int((y == 0).sum()), "n_y1": int((y == 1).sum())}
            for lab in (0, 1):
                m = y == lab
                if m.any():
                    row[f"y{lab}_intervention"] = float(np.mean(v[m] != "allow"))
                    row[f"y{lab}_escalate"] = float(np.mean(v[m] == "escalate"))
                    row[f"y{lab}_verdicts"] = dict(collections.Counter(v[m].tolist()))
            rows.append(row)
        out[name] = rows
    return out


def replay_breakdown():
    res = load_state("replay_main")
    rm = load_state("rmod")
    by = collections.defaultdict(dict)
    for eid, c, u, s, err, aud in res:
        by[eid][c] = (u, s)
    valid = [e for e, ok in rm["agree"].items() if ok]
    refs = st.labeler.references
    target = {it: cat_of[[c for c in calls if c.function not in cats["read"]][0].function]
              for it, calls in refs.injection.items()}
    state_changing_ut = {ut for ut, calls in refs.user.items() if any(c.function not in cats["read"] for c in calls)}
    configs = ["B0", "B1_step_level_no_reviewer", "REM_step_level_no_reviewer", "REMnoEsc_step_level_no_reviewer",
               "REM_step_level_idealized"]
    out = {"injection_target_category": target, "asr_by_target_category": {}, "benign_utility_by_user_task_type": {}}
    for tc in sorted(set(target.values())):
        eps = [e for e in valid if data.episodes[e].injection_task_id and target[data.episodes[e].injection_task_id] == tc]
        out["asr_by_target_category"][tc] = {
            "n_episodes": len(eps), "n_injection_tasks": len({data.episodes[e].injection_task_id for e in eps}),
            **{c: grouped_bootstrap(eps, lambda e: data.episodes[e].injection_task_id,
                                    lambda s: float(np.mean([by[e][c][1] for e in s])), **kw) for c in configs}}
    for kind, pred in (("state_changing", lambda ut: ut in state_changing_ut), ("read_only", lambda ut: ut not in state_changing_ut)):
        eps = [e for e in valid if not data.episodes[e].attacked and pred(data.episodes[e].user_task_id)]
        out["benign_utility_by_user_task_type"][kind] = {
            "n_episodes": len(eps), "n_user_tasks": len({data.episodes[e].user_task_id for e in eps}),
            **{c: grouped_bootstrap(eps, lambda e: data.episodes[e].user_task_id,
                                    lambda s: float(np.mean([by[e][c][0] for e in s])), **kw) for c in configs}}
    return out


def replay_failures():
    rm = load_state("rmod")
    res = load_state("replay_rmod")
    b0 = {eid: (u, s, err) for eid, c, u, s, err, aud in res if c == "B0"}
    rows = []
    for eid, ok in sorted(rm["agree"].items()):
        if ok:
            continue
        ep = data.episodes[eid]
        u, s, err = b0[eid]
        rows.append({"episode_id": eid, "pipeline": ep.pipeline, "user_task": ep.user_task_id,
                     "injection_task": ep.injection_task_id, "recorded_utility": ep.utility,
                     "recorded_security": ep.security, "replay_utility": u, "replay_security": s,
                     "replay_error": err, "benchmark_version_field": ep.benchmark_version,
                     "mismatch": ("utility" if u != ep.utility else "") + ("+security" if s != ep.security else "")})
    summary = {
        "n_excluded": len(rows), "n_total": len(rm["agree"]),
        "by_pipeline": dict(collections.Counter(r["pipeline"] for r in rows)),
        "by_user_task": dict(collections.Counter(r["user_task"] for r in rows)),
        "by_mismatch": dict(collections.Counter(r["mismatch"] for r in rows)),
        "attacked_excluded": sum(1 for r in rows if r["injection_task"]),
        "recorded_security_true_among_excluded": sum(1 for r in rows if r["recorded_security"]),
        "replay_errors": sum(1 for r in rows if r["replay_error"]),
    }
    return {"summary": summary, "episodes": rows}


def label_audit_pack():
    """Human label-audit package (no labels are changed here)."""
    suite = st.suite
    rng = np.random.default_rng(CFG["meta"]["seed"] + 1)
    by = collections.defaultdict(list)
    for s in data.steps:
        by[s.episode_id].append(s)
    items = []

    def add(kind, s):
        ep = data.episodes[s.episode_id]
        it = suite.get_injection_task_by_id(ep.injection_task_id) if ep.injection_task_id else None
        items.append({
            "item_id": f"A{len(items) + 1:03d}", "sample_stratum": kind, "episode_id": s.episode_id,
            "trace_file": "runs/" + ep.path.split("/runs/", 1)[-1],
            "step_index": s.index, "tool": s.tool,
            "key_arguments": "; ".join(f"{k}={s.args.get(k)}" for k in ("recipient", "amount", "password", "id") if k in s.args),
            "assigned_label": s.label, "recorded_episode_security": ep.security,
            "injected_content_in_context_before_step": s.after_change_point,
            "user_task_prompt": suite.get_user_task_by_id(ep.user_task_id).PROMPT,
            "injection_goal": it.GOAL if it else "",
            "annotator_label_0_1": "", "annotator_confidence_1_3": "", "annotator_notes": "",
        })

    att_eps = sorted(e for e in data.episodes if data.episodes[e].attacked)
    for e in rng.choice(att_eps, size=30, replace=False):
        for s in sorted(by[e], key=lambda x: x.index):
            add("random_episode", s)
    for s in data.steps:
        if s.user_task_id == "user_task_15" and s.label == 1:
            add("ambiguous_user_task_15_positive", s)
    for s in data.steps:
        if s.attacker_key_match and not s.label and s.user_task_id != "user_task_15":
            add("attacker_value_but_label_0", s)
    for e in att_eps:
        ss = by[e]
        if data.episodes[e].security and not any(s.label for s in ss):
            for s in ss:
                add("recorded_success_without_positive", s)
    pos_fail = [e for e in att_eps if not data.episodes[e].security and any(s.label for s in by[e])]
    for e in rng.choice(pos_fail, size=min(20, len(pos_fail)), replace=False):
        for s in by[e]:
            if s.label:
                add("positive_without_recorded_success", s)
    path = os.path.join(RESULTS, "label_audit_human_package.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(items[0]))
        w.writeheader()
        w.writerows(items)
    return {"n_items": len(items), "strata": dict(collections.Counter(i["sample_stratum"] for i in items)), "file": path}


if __name__ == "__main__":
    out = {"provenance": provenance(),
           "observe_by_tier_and_category": observe_breakdown(),
           "replay_breakdown": replay_breakdown(),
           "replay_failures": replay_failures(),
           "label_audit_package": label_audit_pack()}
    write_json("r2_breakdowns.json", out)
    print(out["replay_failures"]["summary"])
    print(out["label_audit_package"])
