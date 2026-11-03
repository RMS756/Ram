"""Live closed-loop REM evaluation in AgentDojo (B0 / B1 / REM / REMnoEsc).

STATUS: IMPLEMENTED; NEVER EXECUTED WITH A REAL MODEL in this repository. It needs (a) a configuration
with every design input decided (check_live_config.py), (b) an API credential for the chosen provider,
and (c) the frozen offline fit produced by experiments/pilot/run_all.sh (PILOT_RESULTS_DIR).

usage:
  PILOT_RESULTS_DIR=<dir with steps.pkl and state/> AGENTDOJO_RUNS=<runs> \
  python3 experiments/live/run_live.py --config experiments/live/live_config.yaml --out <output dir>

Exit codes: 0 done; 2 design inputs missing; 3 credential missing; 4 unsupported configuration value.

Nothing is fitted here. The estimator, calibration map, B1 thresholds, x-bar, benign transition set and
r_mod come from the frozen cross-fit state of ONE declared outer fold (config rem.fitted_parameters_source
= "fold:<injection_task_k>"); that choice is a design input (REQUIRED_FROM_DESIGN in the template).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pickle
import subprocess
import sys
import time

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "experiments", "pilot"))

from check_live_config import missing  # noqa: E402

SUPPORTED = {
    "configurations": {"B0", "B1", "REM", "REMnoEsc"},
    "mitigation_semantics": {"step_level", "episode_level"},
    "reviewer_model": {"idealized", "no_reviewer"},
    "costs_and_tiers": {"pilot_e0_exploratory"},
    "feature_set": {"pilot_e0_exploratory"},
    "label_rule": {"reference_match_pilot_e0"},
    "providers": {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY", "google": "GOOGLE_API_KEY"},
}


def fail(code: int, msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def as_list(v):
    return v if isinstance(v, list) else [v]


def validate(cfg: dict) -> None:
    gaps = list(missing(cfg))
    if gaps:
        for g in gaps:
            print(f"[DESIGN BLOCKED] {g}: not specified", file=sys.stderr)
        fail(2, f"{len(gaps)} required design inputs missing; the live evaluation must not start.")
    r = cfg["rem"]
    for key in ("configurations", "mitigation_semantics", "reviewer_model"):
        bad = set(as_list(r[key])) - SUPPORTED[key]
        if bad:
            fail(4, f"rem.{key}: unsupported values {sorted(bad)}")
    for key in ("costs_and_tiers", "feature_set", "label_rule"):
        if r[key] not in SUPPORTED[key]:
            fail(4, f"rem.{key} = {r[key]!r}: only {sorted(SUPPORTED[key])} is implemented (no other value is invented)")
    if not str(r["fitted_parameters_source"]).startswith("fold:"):
        fail(4, "rem.fitted_parameters_source must be 'fold:<outer fold id>' of the frozen cross-fit state")
    for b in as_list(cfg["models"]["backbones"]):
        if not isinstance(b, dict) or b.get("provider") not in SUPPORTED["providers"] or not b.get("model"):
            fail(4, f"models.backbones entry {b!r}: need provider in {sorted(SUPPORTED['providers'])} and an exact model id")
        if not os.environ.get(SUPPORTED["providers"][b["provider"]]):
            fail(3, f"credential {SUPPORTED['providers'][b['provider']]} is not set; no live call is made")
    if int(cfg["models"]["repeats_per_configuration"]) < 1:
        fail(4, "models.repeats_per_configuration must be >= 1")


def make_llm(backbone: dict, decoding: dict):
    provider, model = backbone["provider"], backbone["model"]
    temperature = decoding.get("temperature")
    if provider == "anthropic":
        from anthropic import Anthropic
        from agentdojo.agent_pipeline.llms.anthropic_llm import AnthropicLLM
        return AnthropicLLM(Anthropic(), model, temperature=temperature)
    if provider == "openai":
        import openai
        from agentdojo.agent_pipeline.llms.openai_llm import OpenAILLM
        return OpenAILLM(openai.OpenAI(), model, temperature=temperature)
    if provider == "google":
        from agentdojo.agent_pipeline.llms.google_llm import GoogleLLM
        return GoogleLLM(model, temperature=temperature)
    raise AssertionError(provider)


def frozen_components(fold: str):
    """Policies and scorer of one outer fold, from the frozen pilot state (no refitting)."""
    import common
    import run_main as rm
    from data import build, reference_from_mask
    from rem.integration.agentdojo_replay import FrozenScorer
    from rem.algorithms.behavior.evidence import FEATURE_ORDER

    state = os.path.join(common.RESULTS, "state")
    fits = pickle.load(open(os.path.join(state, "crossfit.pkl"), "rb"))
    rmod = pickle.load(open(os.path.join(state, "rmod.pkl"), "rb"))["rmod"]
    if fold not in fits["label_nll_primary"].fits:
        fail(4, f"fold {fold!r} not in the frozen cross-fit state")
    pol = rm.build_policies(fits, rmod)[fold]
    ff = fits["label_nll_primary"].fits[fold]
    scorer = FrozenScorer(tuple(FEATURE_ORDER), ff.intercept, tuple(ff.coefficients), ff.gamma_0, ff.gamma_1, tuple(ff.xbar))
    data = build("primary")
    ref = reference_from_mask(data, data.fold != fold)
    return pol, scorer, ref


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))
    validate(cfg)

    import common
    from agentdojo.agent_pipeline.agent_pipeline import load_system_message
    from agentdojo.attacks.attack_registry import load_attack
    from agentdojo.task_suite.load_suites import get_suites
    from rem.algorithms.decision.consequence import ConsequenceTierMap  # noqa: F401  (via common.make_setup)
    from rem.core.results import Verdict
    from rem.integration.agentdojo_live import live_episode_stub, run_defended_episode
    from rem.integration.agentdojo_replay import GuardConfig, RemGuard

    st = common.make_setup()
    B, M, R = cfg["benchmark"], cfg["models"], cfg["rem"]
    suite = get_suites(str(B["suite_version"]))[B["suite"]]
    fold = str(R["fitted_parameters_source"]).split(":", 1)[1]
    pol, scorer, ref = frozen_components(fold)
    system_prompt = load_system_message(None)
    users = [t.ID for t in suite.user_tasks.values()] if B["user_tasks"] == "all" else as_list(B["user_tasks"])
    injs = [t.ID for t in suite.injection_tasks.values()] if B["injection_tasks"] == "all" else as_list(B["injection_tasks"])

    def decider(name, variant):
        if name == "B0":
            return lambda c: (Verdict.ALLOW, "allow_all", {})
        key = {"B1": "B1", "REM": f"A3_{variant}", "REMnoEsc": f"A3_noesc_{variant}"}[name]
        P = pol[key]

        def decide(c):
            d = P.decide(c.p, c.tier, c.tool, c.available)       # the label is never passed
            return d.verdict, d.source, {"tie": bool(getattr(d, "tie", False)), "risks": dict(getattr(d, "risks", {}) or {})}
        return decide

    os.makedirs(args.out, exist_ok=True)
    commit = subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"], text=True).strip()
    manifest = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "rem_commit": commit,
                "config_sha256": hashlib.sha256(open(args.config, "rb").read()).hexdigest(), "config": cfg,
                "frozen_fold": fold, "status": "LIVE RUN (real LLM calls)"}
    json.dump(manifest, open(os.path.join(args.out, "manifest.json"), "w"), indent=1, default=str)
    res_f = open(os.path.join(args.out, "episodes.jsonl"), "a", encoding="utf-8")
    for backbone in as_list(M["backbones"]):
        llm = make_llm(backbone, M["decoding"])
        for attack in as_list(B["attacks"]):
            cells = [(u, i) for u in users for i in injs] + [(u, None) for u in users]
            for rep in range(int(M["repeats_per_configuration"])):
                for u, i in cells:
                    target = type("T", (), {"name": backbone["model"]})()
                    injections = {}
                    if i is not None:
                        a = load_attack(attack, suite, target)
                        injections = a.attack(suite.get_user_task_by_id(u), suite.get_injection_task_by_id(i))
                    for conf in as_list(R["configurations"]):
                        for variant in as_list(R["mitigation_semantics"]):
                            for reviewer in as_list(R["reviewer_model"]):
                                ep = live_episode_stub(model_name=backbone["model"], suite_name=B["suite"],
                                                       suite_version=str(B["suite_version"]), user_task_id=u,
                                                       injection_task_id=i, attack=attack if i else None,
                                                       injections=injections, system_prompt=system_prompt,
                                                       user_prompt=suite.get_user_task_by_id(u).PROMPT, repeat=rep)
                                gc = GuardConfig(st.spec, st.detector, ref, st.tier_map, st.restricted, variant, reviewer)
                                g = RemGuard(gc, None if conf == "B0" else scorer, decider(conf, variant), st.labeler, ep)
                                out = run_defended_episode(suite=suite, llm=llm, guard=g, user_task_id=u,
                                                           injection_task_id=i, injections=injections,
                                                           system_prompt=system_prompt, pipeline_name=backbone["model"])
                                rec = {"backbone": backbone, "attack": attack if i else None, "user_task": u,
                                       "injection_task": i, "repeat": rep, "configuration": conf,
                                       "semantics": variant, "reviewer": reviewer, "utility": out.utility,
                                       "security": out.security, "error": out.error, "wall_time_s": out.wall_time_s,
                                       "adaptation": out.adaptation, "audit": out.audit, "messages": out.messages}
                                res_f.write(json.dumps(rec, default=str) + "\n")
                                res_f.flush()
    res_f.close()
    print("done:", args.out)


if __name__ == "__main__":
    main()
