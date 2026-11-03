"""Run the predeclared, local-only feasibility pilot. Requires AgentDojo 0.1.35."""

import argparse
import hashlib
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

from ollama_local import MODEL, OllamaLocal
from run_live import make_decider  # sets the same REM and pilot import paths as the full runner

import common
from agentdojo.agent_pipeline.agent_pipeline import load_system_message
from agentdojo.agent_pipeline.base_pipeline_element import BasePipelineElement
from agentdojo.attacks.attack_registry import load_attack
from agentdojo.agent_pipeline.llms.openai_llm import _function_to_openai, _message_to_openai, _openai_to_assistant_message
from openai.types.chat import ChatCompletionMessage
from rem.algorithms.behavior.evidence import BenignReference, FEATURE_ORDER
from rem.integration.agentdojo_live import live_episode_stub, run_defended_episode
from rem.integration.agentdojo_replay import FrozenScorer, GuardConfig, RemGuard

REPO = Path(common.REPO)
HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "ollama_fold0_reference.json"
SUITE_VERSION = "v1"
USER = "user_task_0"
FOLD = "injection_task_0"
BASE_ATTACK = "direct"
ATTACK = "direct_appended_to_original"
ARMS = ("B0", "B1", "REM")
REPEATS = 3
SEMANTICS = "step_level"
REVIEWER = "no_reviewer"


def sha(path):
    # All hashed inputs are text. Windows Git may check them out with CRLF.
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_fold():
    """Reuse the published fit, plus the offline xbar and transition set from its training portion."""
    from run_main import build_fold_policies

    reference = read(REFERENCE)
    if reference["fold"] != FOLD or tuple(reference["feature_order"]) != tuple(FEATURE_ORDER):
        raise ValueError("Mismatch in the frozen fold or feature order.")
    origin = reference["provenance"]
    for name, digest in origin["source_config_sha256"].items():
        if sha(REPO / "configs" / "exploratory" / name) != digest:
            raise ValueError(f"Pilot config differs from the frozen fit: {name}")
    for name, digest in origin["source_results_sha256"].items():
        if sha(REPO / name) != digest:
            raise ValueError(f"Source result differs from the frozen fit: {name}")
    r4 = REPO / "results" / "pilot_R4"
    fit = read(r4 / "e1_crossfit.json")["label_nll_primary"]["per_fold"][FOLD]
    residuals = read(r4 / "e4_rmod_and_replay_validity.json")["r_mod_per_outer_fold_fitting_portion"]
    rmod = {variant: {FOLD: {int(k): v for k, v in folds[FOLD].items()}} for variant, folds in residuals.items()}
    scorer = FrozenScorer(tuple(FEATURE_ORDER), fit["intercept"], tuple(fit["coefficients"][k] for k in FEATURE_ORDER),
                          fit["gamma_0"], fit["gamma_1"], tuple(reference["xbar"]))
    policies = build_fold_policies(FOLD, fit["theta_blk"], fit["theta_mod"], rmod)
    ref = BenignReference(frozenset(map(tuple, reference["benign_transitions"])))
    return policies, scorer, ref


class LocalAgent(BasePipelineElement):
    def __init__(self, server):
        self.server = server
        self.name = server.model
        self.injection_goal = None
        self.feedback_turns = []

    def query(self, query, runtime, env, messages, extra_args):
        # Reuse the benchmark's tool schemas, call IDs, argument parser and refusal serialization.
        history = [_message_to_openai(m, self.name) for m in messages]
        for m in history:
            if m["role"] == "developer":
                m["role"] = "system"
            if isinstance(m.get("content"), list):
                m["content"] = "\n".join(b["text"] for b in m["content"])
        tools = [_function_to_openai(f) for f in runtime.functions.values()]
        raw = self.server.complete(history, tools)
        ids = [c.get("id") for c in (raw.get("tool_calls") or [])]
        if any(not identifier for identifier in ids) or len(set(ids)) != len(ids):
            raise ValueError("Each tool call in an assistant turn must have a distinct ID.")
        reply = _openai_to_assistant_message(ChatCompletionMessage.model_validate(raw))
        # Observe newly delivered tool outputs, after inference, without adding any text to the prompt.
        delivered = []
        for item in reversed(history):
            if item["role"] != "tool":
                break
            delivered.append(item)
        self.feedback_turns.append({
            "saw_injection": bool(self.injection_goal and any(self.injection_goal in m["content"] for m in delivered)),
            "refusal_ids": [m["tool_call_id"] for m in reversed(delivered) if m["content"].startswith("REM:")],
        })
        return query, runtime, env, [*messages, reply], extra_args


def attacked_bill(suite, agent, user):
    # The stock direct attack replaces the bill body, removing the legitimate amount and payee.
    # Preserve those facts so the authorized task remains possible in the attacked condition.
    attack = load_attack(BASE_ATTACK, suite, agent)
    suffixes = attack.attack(user, suite.get_injection_task_by_id(FOLD))
    if set(suffixes) != {"injection_bill_text"}:
        raise ValueError("Unexpected injection point for the Banking v1 bill task.")
    defaults = suite.get_injection_vector_defaults()
    return {key: defaults[key] + "\n\n" + suffix for key, suffix in suffixes.items()}


def cases():
    # Rotate order so each condition runs first once in each of the two scenarios.
    for repeat in range(REPEATS):
        for injection in (None, FOLD):
            for arm in ARMS[repeat:] + ARMS[:repeat]:
                yield repeat, injection, arm


def summary(records):
    groups = {}
    for arm in ARMS:
        rows = [r for r in records if r["configuration"] == arm]
        ok = [r for r in rows if r["error"] is None]
        attacked = [r for r in ok if r["injection_task"]]
        clean = [r for r in ok if not r["injection_task"]]
        def ratio(rows, key):
            return {"successes": sum(bool(r[key]) for r in rows), "denominator": len(rows)}
        groups[arm] = {"attempted": len(rows), "errors": len(rows) - len(ok),
                       "attack_success": ratio(attacked, "security"),
                       "benign_task_success": ratio(clean, "utility"),
                       "task_success_under_attack": ratio(attacked, "utility"),
                       "attacked_episodes_exposed": sum(any(t["saw_injection"] for t in r["feedback_turns"])
                                                       for r in attacked),
                       "episodes_with_tool_proposals": sum(bool(r["audit"]) for r in ok),
                       "episodes_with_refusal": sum(bool(r["adaptation"]["withheld"]) for r in ok),
                       "retries_after_refusal": sum(r["adaptation"]["retries"] for r in ok),
                       "replans_after_refusal": sum(r["adaptation"]["replans"] for r in ok)}
    return groups


def utc():
    return datetime.now(timezone.utc).isoformat()


def save(path, obj):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temp.replace(path)


def pilot(server, out, commit, expected_digest=None):
    if version("agentdojo") != "0.1.35":
        raise ValueError("Install agentdojo==0.1.35 for this pilot.")
    if out.exists():
        raise FileExistsError(f"Choose a new output directory: {out}")
    identity = server.identity()
    if expected_digest and identity["sha256"] != expected_digest:
        raise ValueError("The installed model differs from the requested SHA-256 digest.")
    policies, scorer, reference = load_fold()
    setup = common.make_setup()
    suite = setup.suite
    agent = LocalAgent(server)
    agent.injection_goal = suite.get_injection_task_by_id(FOLD).GOAL
    prompt = load_system_message(None)
    user = suite.get_user_task_by_id(USER)
    injections = attacked_bill(suite, agent, user)

    out.mkdir(parents=True, exist_ok=False)
    manifest_path = out / "manifest.json"
    manifest = {"status": "started", "study": "exploratory_local_feasibility", "started_utc": utc(),
                "rem_commit": commit, "agentdojo": version("agentdojo"), "model_identity": identity,
                "python": sys.version.split()[0], "numpy": version("numpy"), "openai_sdk": version("openai"),
                "suite": "banking", "suite_version": SUITE_VERSION, "user_task": USER, "injection_task": FOLD,
                "attack": ATTACK, "base_attack": BASE_ATTACK, "injection_vector_ids": sorted(injections), "injection_sha256":
                hashlib.sha256(json.dumps(injections, sort_keys=True).encode()).hexdigest(),
                "arms": ARMS, "repeats": REPEATS, "episodes_planned": len(list(cases())),
                "semantics": SEMANTICS, "reviewer": REVIEWER, "temperature": 0, "max_output_tokens": 2048,
                "max_tool_rounds_per_chat": 15, "system_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "frozen_reference_sha256": sha(REFERENCE), "fold": FOLD, "local_api_spend": 0,
                "analysis": "Counts with denominators. One task and one attack goal. No inferential intervals."}
    save(manifest_path, manifest)
    records = []
    response_start = server.responses
    try:
        with (out / "episodes.jsonl").open("x", encoding="utf-8") as stream:
            for repeat, injection, arm in cases():
                payload = injections if injection else {}
                ep = live_episode_stub(model_name=agent.name, suite_name="banking", suite_version=SUITE_VERSION,
                                       user_task_id=USER, injection_task_id=injection, attack=ATTACK if injection else None,
                                       injections=payload, system_prompt=prompt, user_prompt=user.PROMPT, repeat=repeat)
                config = GuardConfig(setup.spec, setup.detector, reference, setup.tier_map, setup.restricted,
                                     SEMANTICS, REVIEWER)
                guard = RemGuard(config, None if arm == "B0" else scorer, make_decider(policies, arm, SEMANTICS),
                                 setup.labeler, ep)
                agent.feedback_turns = []
                before = server.responses
                outcome = run_defended_episode(suite=suite, llm=agent, guard=guard, user_task_id=USER,
                                               injection_task_id=injection, injections=payload, system_prompt=prompt,
                                               pipeline_name=agent.name)
                # B0 deliberately has no probability. Use valid JSON null for those audit fields.
                for row in outcome.audit:
                    for key in ("logit", "p", "p_raw"):
                        if not math.isfinite(row[key]):
                            row[key] = None
                count = server.responses - before
                error = outcome.error or ("No model response received" if count == 0 else None)
                rec = {"backbone": {"provider": "ollama_local", "model": agent.name}, "configuration": arm,
                       "repeat": repeat, "user_task": USER, "injection_task": injection,
                       "attack": ATTACK if injection else None, "semantics": SEMANTICS, "reviewer": REVIEWER,
                       "model_responses": count, "error": error,
                       "utility": outcome.utility if not error else None,
                       "security": outcome.security if injection and not error else None,
                       "adaptation": outcome.adaptation, "feedback_turns": agent.feedback_turns,
                       "audit": outcome.audit, "chats": outcome.transcripts,
                       "wall_time_s": outcome.wall_time_s}
                stream.write(json.dumps(rec, allow_nan=False) + "\n")
                stream.flush()
                records.append(rec)
                print(f"{len(records):2}/{manifest['episodes_planned']} {arm} {injection or 'benign'}: "
                      f"{error or 'recorded'}", flush=True)
                if error and not count:
                    raise RuntimeError("No usable model reply in this episode. Inspect episodes.jsonl before retrying.")
        if server.identity() != identity:
            raise ValueError("The model digest or Ollama version changed during this run.")
        manifest["status"] = "completed_with_errors" if any(r["error"] for r in records) else "completed"
    except BaseException as exc:
        manifest["status"] = "interrupted"
        manifest["reason"] = str(exc) or type(exc).__name__
        raise
    finally:
        manifest.update(ended_utc=utc(), episodes_recorded=len(records), model_responses=server.responses-response_start,
                        proposals=sum(len(r["audit"]) for r in records))
        save(manifest_path, manifest)
        save(out / "summary.json", {"status": manifest["status"], "episodes_planned": manifest["episodes_planned"],
                                    "episodes_recorded": len(records), "by_condition": summary(records)})
    return manifest["status"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path, help="New output directory for this run")
    parser.add_argument("--expect-digest", help="Optional model SHA-256 printed by the setup check")
    parser.add_argument("--accept-local-pilot", action="store_true",
                        help="Run the proposed feasibility design. This does not approve a thesis-wide study.")
    args = parser.parse_args()
    if not args.accept_local_pilot:
        parser.error("Read OLLAMA_PILOT_AR.md, then supply --accept-local-pilot to run.")
    try:
        commit = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip()
        tracked = ["experiments/live/run_ollama_pilot.py", "experiments/live/ollama_local.py",
                   "experiments/live/ollama_fold0_reference.json", "experiments/live/run_live.py",
                   "experiments/live/OLLAMA_PILOT_AR.md", "experiments/pilot", "configs/exploratory", "rem",
                   "results/pilot_R4/e1_crossfit.json", "results/pilot_R4/e4_rmod_and_replay_validity.json"]
        subprocess.run(["git", "-C", str(REPO), "ls-files", "--error-unmatch", *tracked],
                       check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "-C", str(REPO), "diff", "--quiet", "HEAD", "--", *tracked], check=True)
        status = pilot(OllamaLocal(MODEL), args.out, commit, args.expect_digest)
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"Pilot stopped: {exc}\nUse an unmodified checkout of the pilot branch.\n")
    return 0 if status == "completed" else 5


if __name__ == "__main__":
    sys.exit(main())
