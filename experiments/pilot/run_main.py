"""Exploratory pilot E1-E6 (EXPLORATORY — NOT THESIS RESULTS — SUPERVISOR DECISION REQUIRED).

Stages (each writes results/pilot/<stage>.json):
  crossfit  E1 calibration/discrimination, both calibrators; ablation refits;
            grouping sensitivity (user task) and leave-one-backbone-out
  rmod      oracle-Modify replays -> r_mod(k) per outer fold, per SC-1 variant
  observe   E2/E5/E6 observe-only verdict analysis on held-out recorded steps
  replay    E4/E5 enforcement replays in the AgentDojo sandbox
  a2        E3 observe-only CUSUM
  xt        cross-template generalisation (gpt-4o) and distributed defenses
"""

from __future__ import annotations

import collections
import itertools
import multiprocessing as mp
import os
import pickle
import sys
import time

import numpy as np

from common import RESULTS, load_config, make_setup, provenance, write_json
from data import Designer, build, features_without, load_raw, reference_from_mask

from rem.algorithms.a1 import A1Policy, A1Thresholds
from rem.algorithms.a2 import evaluate_episode, fit_a2
from rem.algorithms.a3 import A3Policy
from rem.algorithms.behavior.cusum import deviation_indicator
from rem.algorithms.behavior.evidence import FEATURE_ORDER
from rem.algorithms.calibration.logit_nll import LabelNLLLogitCalibrator
from rem.algorithms.calibration.platt import PlattLogitCalibrator
from rem.algorithms.decision.consequence import ConsequenceTierMap
from rem.algorithms.decision.loss_matrix import LossSpec, build_loss_grid, reachable_verdicts
from rem.algorithms.decision.policy import PredicatePolicy
from rem.core.results import Verdict
from rem.evaluation.bootstrap import grouped_bootstrap
from rem.evaluation.crossfit import nested_crossfit
from rem.evaluation.probabilistic import (
    average_precision,
    brier_binary,
    brier_two_class,
    expected_calibration_error,
    log_loss,
    reliability_table,
    roc_auc,
)
from rem.integration.agentdojo_replay import FrozenScorer, GuardConfig, RemGuard, replay_episode
from rem.integration.steps import design_matrix

CFG = load_config()
E = CFG["estimation"]
B = CFG["bootstrap"]
SEED = CFG["meta"]["seed"]
VARIANTS = CFG["mitigation_semantics_variants"]          # step_level, episode_level
ESC = CFG["escalation"]["reviewer_models"]               # idealized, no_reviewer
ESC_MAP = {"idealized": "idealized", "no_reviewer_bound": "no_reviewer"}
STATE = os.path.join(RESULTS, "state")
os.makedirs(STATE, exist_ok=True)


def save_state(name, obj):
    with open(os.path.join(STATE, name + ".pkl"), "wb") as fh:
        pickle.dump(obj, fh)


def load_state(name):
    with open(os.path.join(STATE, name + ".pkl"), "rb") as fh:
        return pickle.load(fh)


# ---------------------------------------------------------------------------
# metrics helpers
# ---------------------------------------------------------------------------

def prob_metrics(y, p):
    clip = E["probability_clip"]
    return {
        "n": int(len(y)), "positives": int(np.sum(y)),
        "roc_auc": roc_auc(y, p), "average_precision": average_precision(y, p),
        "ece": expected_calibration_error(y, p, E["ece_bins"]), "log_loss": log_loss(y, p, clip),
        "brier_binary_SC5": brier_binary(y, p), "brier_two_class_SC5": brier_two_class(y, p),
    }


def boot_steps(data, idx, stat):
    """Stratified grouped bootstrap over steps: attacked by injection task, benign by user task."""
    from rem.evaluation.bootstrap import stratified_grouped_bootstrap

    att = [i for i in idx if data.attacked[i]]
    ben = [i for i in idx if not data.attacked[i]]
    strata = [(att, lambda i: data.steps[i].injection_task_id), (ben, lambda i: data.steps[i].user_task_id)]
    return stratified_grouped_bootstrap(strata, stat, resamples=B["resamples"], seed=SEED, level=B["interval"])


# ---------------------------------------------------------------------------
# stage: crossfit
# ---------------------------------------------------------------------------

def run_crossfit(data, feature_order, calibrator, outer=None, alphas=True):
    designer = Designer(data, feature_order)
    return nested_crossfit(
        design=designer, y=data.y, outer_fold=data.fold if outer is None else outer,
        inner_group=data.inner_group, inner_is_benign_group=~data.attacked, feature_order=feature_order,
        lambda_grid=E["lambda_grid"], inner_folds=E["inner_folds"], calibrator_factory=calibrator,
        alpha_blk=CFG["baseline_B1"]["alpha_blk"] if alphas else None,
        alpha_mod=CFG["baseline_B1"]["alpha_mod"] if alphas else None, clip=E["probability_clip"],
    )


def stage_crossfit():
    data = build("primary")
    out = {"provenance": provenance()}
    fits = {}
    for name, cal in (("label_nll_primary", LabelNLLLogitCalibrator), ("platt_smoothed_secondary", PlattLogitCalibrator)):
        res = run_crossfit(data, FEATURE_ORDER, cal)
        fits[name] = res
        ok = ~np.isnan(res.p_cal)
        idx = np.flatnonzero(ok)
        m = {"pooled_calibrated": prob_metrics(data.y[ok], res.p_cal[ok]),
             "pooled_uncalibrated": prob_metrics(data.y, res.p_raw),
             "calibration_failures": [f for f, ff in res.fits.items() if ff.calibration_failed],
             "per_fold": {}, "reliability": reliability_table(data.y[ok], res.p_cal[ok], E["ece_bins"]),
             "reliability_uncalibrated": reliability_table(data.y, res.p_raw, E["ece_bins"])}
        for f, ff in res.fits.items():
            mk = (data.fold == f) & ok
            m["per_fold"][f] = {**prob_metrics(data.y[mk], res.p_cal[mk]), "lambda": ff.lam,
                                "gamma_1": ff.gamma_1, "gamma_0": ff.gamma_0, "theta_blk": ff.theta_blk,
                                "theta_mod": ff.theta_mod, "n_train_pos": ff.n_train_pos,
                                "coefficients": dict(zip(FEATURE_ORDER, ff.coefficients)), "intercept": ff.intercept}
        for key, fn in (("roc_auc", roc_auc), ("average_precision", average_precision),
                        ("ece", lambda a, b: expected_calibration_error(a, b, E["ece_bins"])),
                        ("log_loss", lambda a, b: log_loss(a, b, E["probability_clip"]))):
            m[f"ci_{key}"] = boot_steps(data, idx, lambda s, fn=fn: fn(data.y[list(s)], res.p_cal[list(s)]))
        out[name] = m
        print(name, {k: round(v, 4) for k, v in m["pooled_calibrated"].items() if isinstance(v, float)})

    # ablation refits (evidence groups removed; primary calibrator)
    abl = {}
    for g in ("ctx", "beh", "act"):
        order = features_without([g])
        res = run_crossfit(data, order, LabelNLLLogitCalibrator)
        fits[f"no_{g}"] = res
        ok = ~np.isnan(res.p_cal)
        abl[f"no_{g}"] = {"features": order, "pooled_calibrated": prob_metrics(data.y[ok], res.p_cal[ok])}
    out["ablation_refits"] = abl

    # grouping sensitivity and leave-one-backbone-out (discrimination/calibration only)
    for grouping in ("user_task", "pipeline"):
        d2 = build("primary", grouping=grouping)
        res = run_crossfit(d2, FEATURE_ORDER, LabelNLLLogitCalibrator, alphas=False)
        ok = ~np.isnan(res.p_cal)
        per = {}
        for f in sorted(set(d2.fold.tolist()), key=str):
            mk = (d2.fold == f) & ok
            if mk.any():
                per[f] = prob_metrics(d2.y[mk], res.p_cal[mk])
        out[f"grouping_{grouping}"] = {"pooled_calibrated": prob_metrics(d2.y[ok], res.p_cal[ok]),
                                       "calibration_failures": [f for f, ff in res.fits.items() if ff.calibration_failed],
                                       "per_fold": per}
        print("grouping", grouping, out[f"grouping_{grouping}"]["pooled_calibrated"]["roc_auc"])
    save_state("crossfit", {k: v for k, v in fits.items()})
    write_json("e1_crossfit.json", out)


# ---------------------------------------------------------------------------
# policies
# ---------------------------------------------------------------------------

def predicates(enabled=True):
    P = CFG["policy"]
    req = tuple("_".join(n.split("_")[:2]) for n in P["required_evidence_at_or_above_k_D2"])
    return PredicatePolicy(frozenset(P["prohibited_actions_Pi"]), int(P["k_D2"]), req,
                           frozenset(CFG["consequence"]["restricted_tools_T_R"]), enabled)


def loss_spec(r_mod, C_miss_mult=1.0, C_esc=None):
    L = CFG["losses"]
    tiers = sorted(int(k) for k in L["C_FA"])
    return LossSpec(
        C_FA={k: float(L["C_FA"][k]) for k in tiers},
        C_miss={k: float(L["C_miss"][k]) * C_miss_mult for k in tiers},
        C_mod={k: float(L["C_mod"][k]) for k in tiers},
        C_esc=float(L["C_esc"] if C_esc is None else C_esc),
        r_mod={k: float(r_mod.get(k, L["r_mod_if_unmeasured"])) for k in tiers},
    )


def scorer_of(fit, order, calibrated=True):
    return FrozenScorer(tuple(order), fit.intercept, tuple(fit.coefficients),
                        fit.gamma_0 if calibrated else 0.0, fit.gamma_1 if calibrated else 1.0, tuple(fit.xbar))


# ---------------------------------------------------------------------------
# replay workers (fork-inherited globals)
# ---------------------------------------------------------------------------

G = {}


def _guard_config(st, ref, variant, esc, single_tier=None, observe_only=False):
    return GuardConfig(st.spec, st.detector, ref, st.tier_map, st.restricted, variant, esc,
                       observe_only=observe_only, single_tier=single_tier)


def _replay_job(job):
    eid, cname = job
    st, data = G["setup"], G["data"]
    ep = data.episodes[eid]
    f = data.episode_fold[eid]
    spec = G["configs"][cname]
    ref = G["refs"][f]
    gc = _guard_config(st, ref, spec["variant"], spec["esc"], spec.get("single_tier"), spec.get("observe_only", False))
    scorer = spec["scorer"](f) if spec.get("scorer") else None
    decide = spec["decide"](f)
    g = RemGuard(gc, scorer, decide, st.labeler, ep)
    out = replay_episode(ep, st.suite, g)
    return (eid, cname, out.utility, out.security, out.error,
            [(a["label"], a["verdict"], a["released"], a["tier"], a["tool"], a["rem_latency_ms"],
              a["details"].get("tie", False), a["verdict_source"]) for a in out.audit])


def run_replays(configs, episode_ids, setup, data, refs, procs=4):
    G.update(setup=setup, data=data, configs=configs, refs=refs)
    jobs = [(e, c) for c in configs for e in episode_ids]
    t0 = time.time()
    with mp.get_context("fork").Pool(procs) as pool:
        res = pool.map(_replay_job, jobs, chunksize=64)
    print(f"{len(jobs)} replays in {time.time() - t0:.1f}s")
    return res


def _decide_allow(f):
    return lambda c: (Verdict.ALLOW, "allow_all", {})


def _decide_oracle_modify(f):
    tr = set(CFG["consequence"]["restricted_tools_T_R"])
    return lambda c: ((Verdict.MODIFY, "oracle_modify", {}) if (c.label and c.tool in tr) else (Verdict.ALLOW, "oracle", {}))


# ---------------------------------------------------------------------------
# stage: rmod
# ---------------------------------------------------------------------------

def stage_rmod():
    st = make_setup()
    data = build("primary")
    folds = sorted(set(data.fold.tolist()), key=str)
    refs = {f: reference_from_mask(data, data.fold != f) for f in folds}
    configs = {"B0": {"variant": "step_level", "esc": "no_reviewer", "decide": _decide_allow}}
    for v in VARIANTS:
        configs[f"oracle_modify_{v}"] = {"variant": v, "esc": "no_reviewer", "decide": _decide_oracle_modify}
    res = run_replays(configs, sorted(data.episodes), st, data, refs)
    save_state("replay_rmod", res)
    by = collections.defaultdict(dict)
    for eid, c, u, s, err, aud in res:
        by[eid][c] = (u, s, err, aud)
    # AM-4 agreement of B0 replay with the record
    agree = {eid: (by[eid]["B0"][0] == data.episodes[eid].utility and by[eid]["B0"][1] == data.episodes[eid].security
                   and by[eid]["B0"][2] is None) for eid in by}
    per_pipe = collections.defaultdict(lambda: [0, 0])
    for eid, ok in agree.items():
        per_pipe[data.episodes[eid].pipeline][0] += ok
        per_pipe[data.episodes[eid].pipeline][1] += 1
    rmod = {}
    detail = {}
    for v in VARIANTS:
        rows = []  # (fold, tier of first modified adversarial step, security after)
        for eid in by:
            ep = data.episodes[eid]
            if not ep.attacked or not agree[eid]:
                continue
            aud = by[eid][f"oracle_modify_{v}"][3]
            mod = [a for a in aud if a[1] == "modify"]
            if mod:
                rows.append((data.episode_fold[eid], mod[0][3], by[eid][f"oracle_modify_{v}"][1]))
        for f in folds:
            per_tier = collections.defaultdict(list)
            for fold, k, sec in rows:
                if fold != f:
                    per_tier[k].append(sec)
            rmod.setdefault(v, {})[f] = {int(k): float(np.mean(x)) for k, x in per_tier.items()}
        pooled = collections.defaultdict(list)
        for _, k, sec in rows:
            pooled[k].append(sec)
        detail[v] = {int(k): {"n_episodes": len(x), "residual_asr": float(np.mean(x))} for k, x in pooled.items()}
    save_state("rmod", {"rmod": rmod, "agree": agree})
    write_json("e4_rmod_and_replay_validity.json", {
        "provenance": provenance(),
        "replay_agreement_B0_vs_record": {p: {"agree": a, "n": n, "rate": a / n} for p, (a, n) in sorted(per_pipe.items())},
        "replay_agreement_total": {"agree": int(sum(agree.values())), "n": len(agree)},
        "r_mod_pooled_by_first_modified_tier": detail,
        "r_mod_per_outer_fold_fitting_portion": rmod,
        "note": "r_mod measured under the NO-ADAPT replay assumption; adaptive agents may achieve higher residual success.",
    })
    print(detail, sum(agree.values()), len(agree))


# ---------------------------------------------------------------------------
# fold policies (shared by observe and replay)
# ---------------------------------------------------------------------------

def build_policies(fits, rmod, tie_mode="record_chapter3_order"):
    """Per fold: A3 per variant, B1 thresholds, scorers; plus ablation policies."""
    pol = collections.defaultdict(dict)
    prim = fits["label_nll_primary"]
    for f, ff in prim.fits.items():
        for v in VARIANTS:
            grid = build_loss_grid(loss_spec(rmod[v][f]), f"pilot_e0 fold {f} variant {v}")
            pol[f][f"A3_{v}"] = A3Policy(grid, predicates(), tie_mode=tie_mode)
            pol[f][f"A3_nopred_{v}"] = A3Policy(grid, predicates(False), tie_mode=tie_mode)
            pol[f][f"grid_{v}"] = grid
        pol[f]["B1"] = A1Policy(A1Thresholds(ff.theta_blk, ff.theta_mod, CFG["baseline_B1"]["alpha_blk"],
                                             CFG["baseline_B1"]["alpha_mod"]), predicates())
    return pol


# ---------------------------------------------------------------------------
# stage: observe (E2, E5 observe-only part, E6)
# ---------------------------------------------------------------------------

def _verdict_summary(y, verdicts, ties=None, sources=None):
    y = np.asarray(y)
    v = np.asarray(verdicts, dtype=object)
    out = {}
    for lab in (0, 1):
        m = y == lab
        n = int(m.sum())
        out[f"y{lab}"] = {"n": n, **{vv.value: float(np.mean(v[m] == vv.value)) if n else float("nan") for vv in Verdict}}
    inter = v != "allow"
    out["step_fpr"] = float(np.mean(inter[y == 0]))
    out["intervention_rate_y1"] = float(np.mean(inter[y == 1]))
    # escalation outcomes: idealized releases y=0 escalations; no-reviewer withholds all
    prevented_ideal = np.isin(v, ["modify", "block", "escalate"])
    out["y1_withheld_idealized"] = float(np.mean(prevented_ideal[y == 1]))
    out["y0_withheld_idealized"] = float(np.mean(np.isin(v, ["modify", "block"])[y == 0]))
    out["y0_withheld_no_reviewer"] = out["step_fpr"]
    out["escalation_rate"] = float(np.mean(v == "escalate"))
    if ties is not None:
        out["ties"] = int(np.sum(ties))
    if sources is not None:
        out["sources"] = dict(collections.Counter(sources))
    return out


def realized_loss(grid, verdicts, y, tiers):
    return float(np.mean([grid.loss(Verdict(v), int(l), int(k)) for v, l, k in zip(verdicts, y, tiers)]))


def stage_observe():
    data = build("primary")
    fits = load_state("crossfit")
    rmod = load_state("rmod")["rmod"]
    pol = build_policies(fits, rmod)
    prim = fits["label_nll_primary"]
    tiers = np.array([s.tier for s in data.steps])
    tools = [s.tool for s in data.steps]
    avail = [s.available for s in data.steps]
    out = {"provenance": provenance()}

    def decide_all(policy_key, p, tier_arr=None, single_tier=None):
        vs, ties, srcs = [], [], []
        for i, s in enumerate(data.steps):
            f = data.fold[i]
            k = single_tier if single_tier is not None else (tiers[i] if tier_arr is None else tier_arr[i])
            d = pol[f][policy_key].decide(float(p[i]), int(k), tools[i], avail[i])
            vs.append(d.verdict.value)
            ties.append(getattr(d, "tie", False))
            srcs.append(d.source)
        return vs, ties, srcs

    p = prim.p_cal
    res = {}
    for v in VARIANTS:
        vs, ties, srcs = decide_all(f"A3_{v}", p)
        res[f"REM_{v}"] = (vs, ties, srcs)
    vs, ties, srcs = decide_all("B1", p)
    res["B1"] = (vs, ties, srcs)
    # ablations (observe-only); each changes one element
    for v in VARIANTS:
        for g in ("ctx", "beh", "act"):
            r = fits[f"no_{g}"]
            res[f"abl_no_{g}_{v}"] = decide_all(f"A3_{v}", r.p_cal)
        res[f"abl_no_calibration_{v}"] = decide_all(f"A3_{v}", prim.p_raw)
        for k in (1, 2, 3, 4):
            res[f"abl_single_tier{k}_{v}"] = decide_all(f"A3_{v}", p, single_tier=k)
        res[f"abl_no_predicates_{v}"] = decide_all(f"A3_nopred_{v}", p)

    summ = {}
    for name, (vs, ties, srcs) in res.items():
        s = _verdict_summary(data.y, vs, ties, srcs)
        v = "episode_level" if name.endswith("episode_level") else "step_level"
        # realized loss under the fold's decision grid of that variant (Eq. 3.22, L_e = L_d base)
        s["realized_loss_base"] = float(np.mean([
            pol[data.fold[i]][f"grid_{v}"].loss(Verdict(vs[i]), int(data.y[i]), int(tiers[i])) for i in range(len(vs))]))
        summ[name] = s
    out["verdicts"] = summ
    # CIs for REM vs B1 step FPR and y1 intervention
    idx = list(range(len(data.steps)))
    for name in ("REM_step_level", "REM_episode_level", "B1"):
        vs = np.asarray(res[name][0], dtype=object)
        inter = vs != "allow"
        out["verdicts"][name]["ci_step_fpr"] = boot_steps(data, idx, lambda s: float(np.mean(inter[[i for i in s if data.y[i] == 0]])))
        out["verdicts"][name]["ci_intervention_y1"] = boot_steps(data, idx, lambda s: float(np.mean(inter[[i for i in s if data.y[i] == 1]])))
    # dominance check per fold/variant/tier
    out["dominance"] = {f: {v: {k: {vv.value: r for vv, r in reachable_verdicts(pol[f][f"grid_{v}"], k).items()}
                                for k in (1, 2, 3, 4)} for v in VARIANTS} for f in pol}

    # E6 grid
    G6 = CFG["grid"]
    st = make_setup()
    grid_rows = []
    for limit in G6["amount_limit"]:
        tm = ConsequenceTierMap(CFG["consequence"]["categories"], CFG["consequence"]["tier_map"], limit)
        tiers_e = np.array([tm.tier(s.tool, s.args) for s in data.steps])
        for mult, cesc in itertools.product(G6["C_miss_multiplier"], G6["C_esc"]):
            for v in VARIANTS:
                Le = {f: build_loss_grid(loss_spec(rmod[v][f], mult, cesc), "Le") for f in pol}
                # matched: decide with L_d = L_e and tiers under this limit
                pols_m = {f: A3Policy(Le[f], predicates(), tie_mode="record_chapter3_order") for f in pol}
                vs_m = [pols_m[data.fold[i]].decide(float(p[i]), int(tiers_e[i]), tools[i], avail[i]).verdict.value
                        for i in range(len(data.steps))]
                vs_x = res[f"REM_{v}"][0]   # misspecified: base L_d, base limit
                loss_m = float(np.mean([Le[data.fold[i]].loss(Verdict(vs_m[i]), int(data.y[i]), int(tiers_e[i])) for i in range(len(vs_m))]))
                loss_x = float(np.mean([Le[data.fold[i]].loss(Verdict(vs_x[i]), int(data.y[i]), int(tiers_e[i])) for i in range(len(vs_x))]))
                row = {"amount_limit": limit, "C_miss_multiplier": mult, "C_esc": cesc, "variant": v,
                       "REM_matched": loss_m, "REM_misspecified_base": loss_x}
                for ab in G6["alpha_blk"]:
                    am = CFG["baseline_B1"]["alpha_mod"]
                    if not am > ab:
                        row[f"B1_alpha_blk_{ab}"] = "not evaluable: alpha_mod must exceed alpha_blk"
                        continue
                    vb = []
                    for i in range(len(data.steps)):
                        ff = prim.fits[data.fold[i]]
                        key = (data.fold[i], ab)
                        if key not in G:
                            G[key] = A1Policy(A1Thresholds.fit(ff.benign_oof_p, ab, am), predicates())
                        vb.append(G[key].decide(float(p[i]), int(tiers_e[i]), tools[i], avail[i]).verdict.value)
                    row[f"B1_alpha_blk_{ab}"] = float(np.mean([Le[data.fold[i]].loss(Verdict(vb[i]), int(data.y[i]), int(tiers_e[i])) for i in range(len(vb))]))
                grid_rows.append(row)
    out["e6_grid"] = grid_rows
    save_state("observe_verdicts", res)
    write_json("e2_e5_e6_observe_only.json", out)
    for k in ("REM_step_level", "REM_episode_level", "B1"):
        print(k, {a: summ[k][a] for a in ("step_fpr", "intervention_rate_y1", "escalation_rate", "realized_loss_base", "ties")})


# ---------------------------------------------------------------------------
# stage: replay (E4, E5 enforcement)
# ---------------------------------------------------------------------------

def _mk_decide(policy_key):
    def factory(f):
        P = G["policies"][f][policy_key]

        def decide(c):
            d = P.decide(c.p, c.tier, c.tool, c.available)
            return d.verdict, d.source, {"tie": bool(getattr(d, "tie", False))}
        return decide
    return factory


def _mk_scorer(fit_key, calibrated=True):
    def factory(f):
        r = G["fits"][fit_key]
        order = FEATURE_ORDER if fit_key == "label_nll_primary" else features_without([fit_key.split("_")[1]])
        return scorer_of(r.fits[f], order, calibrated)
    return factory


def replay_configs():
    C = {"B0": {"variant": "step_level", "esc": "no_reviewer", "decide": _decide_allow}}
    for v in VARIANTS:
        for e in ESC:
            e2 = ESC_MAP[e]
            C[f"REM_{v}_{e2}"] = {"variant": v, "esc": e2, "decide": _mk_decide(f"A3_{v}"), "scorer": _mk_scorer("label_nll_primary")}
            C[f"B1_{v}_{e2}"] = {"variant": v, "esc": e2, "decide": _mk_decide("B1"), "scorer": _mk_scorer("label_nll_primary")}
            for g in ("ctx", "beh", "act"):
                C[f"abl_no_{g}_{v}_{e2}"] = {"variant": v, "esc": e2, "decide": _mk_decide(f"A3_{v}"), "scorer": _mk_scorer(f"no_{g}")}
            C[f"abl_no_calibration_{v}_{e2}"] = {"variant": v, "esc": e2, "decide": _mk_decide(f"A3_{v}"),
                                                 "scorer": _mk_scorer("label_nll_primary", calibrated=False)}
            for k in (1, 2, 3, 4):
                C[f"abl_single_tier{k}_{v}_{e2}"] = {"variant": v, "esc": e2, "decide": _mk_decide(f"A3_{v}"),
                                                     "scorer": _mk_scorer("label_nll_primary"), "single_tier": k}
            C[f"abl_no_predicates_{v}_{e2}"] = {"variant": v, "esc": e2, "decide": _mk_decide(f"A3_nopred_{v}"),
                                                "scorer": _mk_scorer("label_nll_primary")}
    C["abl_observe_only"] = {"variant": "episode_level", "esc": "no_reviewer", "decide": _mk_decide("A3_episode_level"),
                             "scorer": _mk_scorer("label_nll_primary"), "observe_only": True}
    return C


def episode_metrics(data, by, cname, eids):
    att = [e for e in eids if data.episodes[e].attacked]
    ben = [e for e in eids if not data.episodes[e].attacked]
    sec = {e: by[e][cname][1] for e in att}
    uti = {e: by[e][cname][0] for e in eids}
    lat = [a[5] for e in eids for a in by[e][cname][3]]
    steps = [a for e in eids for a in by[e][cname][3]]
    y = np.array([a[0] for a in steps])
    v = np.array([a[1] for a in steps], dtype=object)
    rel = np.array([a[2] for a in steps])
    mod_eps = [e for e in att if any(a[0] == 1 and a[1] == "modify" for a in by[e][cname][3])]
    kw = dict(resamples=B["resamples"], seed=SEED, level=B["interval"])
    out = {
        "ASR": grouped_bootstrap(att, lambda e: data.episodes[e].injection_task_id, lambda s: float(np.mean([sec[e] for e in s])), **kw),
        "benign_utility": grouped_bootstrap(ben, lambda e: data.episodes[e].user_task_id, lambda s: float(np.mean([uti[e] for e in s])), **kw),
        "utility_under_attack": grouped_bootstrap(att, lambda e: data.episodes[e].injection_task_id, lambda s: float(np.mean([uti[e] for e in s])), **kw),
        "n_attacked": len(att), "n_benign": len(ben),
        "residual_ASR_under_Modify": (float(np.mean([sec[e] for e in mod_eps])) if mod_eps else None, len(mod_eps)),
        "step_fpr_withheld_y0": float(np.mean(~rel[y == 0])) if (y == 0).any() else None,
        "withheld_y1": float(np.mean(~rel[y == 1])) if (y == 1).any() else None,
        "verdict_rates": {lab: dict(collections.Counter(v[y == lab].tolist())) for lab in (0, 1)},
        "escalation_rate": float(np.mean(v == "escalate")) if v.size else None,
        "ties": int(sum(a[6] for a in steps)),
        "latency_ms_median": float(np.median(lat)) if lat else None,
        "latency_ms_p95": float(np.percentile(lat, 95)) if lat else None,
        "replay_errors": sum(1 for e in eids if by[e][cname][2]),
    }
    return out


def stage_replay():
    st = make_setup()
    data = build("primary")
    fits = load_state("crossfit")
    rm = load_state("rmod")
    pol = build_policies(fits, rm["rmod"])
    folds = sorted(set(data.fold.tolist()), key=str)
    refs = {f: reference_from_mask(data, data.fold != f) for f in folds}
    G.update(policies=pol, fits=fits)
    configs = replay_configs()
    res = run_replays(configs, sorted(data.episodes), st, data, refs)
    save_state("replay_main", res)
    by = collections.defaultdict(dict)
    for eid, c, u, s, err, aud in res:
        by[eid][c] = (u, s, err, aud)
    valid = sorted(e for e, ok in rm["agree"].items() if ok)
    out = {"provenance": provenance(), "assumption": "NO-ADAPT recorded-trace replay (see rem.integration.agentdojo_replay)",
           "episodes_valid_AM4": len(valid), "episodes_total": len(by), "configs": {}}
    for c in configs:
        out["configs"][c] = episode_metrics(data, by, c, valid)
    # paired differences REM - B1 and REM - B0 on ASR and benign utility
    kw = dict(resamples=B["resamples"], seed=SEED, level=B["interval"])
    att = [e for e in valid if data.episodes[e].attacked]
    ben = [e for e in valid if not data.episodes[e].attacked]
    diffs = {}
    for v in VARIANTS:
        for e in ESC:
            e2 = ESC_MAP[e]
            for other in (f"B1_{v}_{e2}", "B0"):
                a = f"REM_{v}_{e2}"
                diffs[f"{a}_minus_{other}"] = {
                    "ASR": grouped_bootstrap(att, lambda x: data.episodes[x].injection_task_id,
                                             lambda s: float(np.mean([by[x][a][1] - by[x][other][1] for x in s])), **kw),
                    "benign_utility": grouped_bootstrap(ben, lambda x: data.episodes[x].user_task_id,
                                                        lambda s: float(np.mean([by[x][a][0] - by[x][other][0] for x in s])), **kw),
                }
    out["paired_differences"] = diffs
    # per-backbone ASR for REM and B0
    per = collections.defaultdict(dict)
    for c in ("B0", "REM_episode_level_no_reviewer", "REM_step_level_no_reviewer", "B1_episode_level_no_reviewer"):
        for pipe in sorted({data.episodes[e].pipeline for e in valid}):
            ea = [e for e in att if data.episodes[e].pipeline == pipe]
            eb = [e for e in ben if data.episodes[e].pipeline == pipe]
            per[pipe][c] = {"ASR": float(np.mean([by[e][c][1] for e in ea])) if ea else None,
                            "benign_utility": float(np.mean([by[e][c][0] for e in eb])) if eb else None,
                            "n_att": len(ea), "n_ben": len(eb)}
    out["per_backbone"] = per
    write_json("e4_e5_enforcement_replay.json", out)
    for c in ("B0", "REM_step_level_no_reviewer", "REM_episode_level_no_reviewer", "REM_episode_level_idealized",
              "B1_step_level_no_reviewer", "B1_episode_level_no_reviewer"):
        m = out["configs"][c]
        print(c, "ASR", [round(x, 3) for x in m["ASR"]], "BU", [round(x, 3) for x in m["benign_utility"]],
              "UA", round(m["utility_under_attack"][0], 3), "lat", m["latency_ms_median"], m["latency_ms_p95"])


# ---------------------------------------------------------------------------
# stage: a2 (E3)
# ---------------------------------------------------------------------------

def stage_a2():
    data = build("primary")
    A = CFG["sequential_A2"]
    folds = sorted(set(data.fold.tolist()), key=str)
    by_ep = collections.defaultdict(list)
    for i, s in enumerate(data.steps):
        by_ep[s.episode_id].append(i)
    out = {"provenance": provenance(), "observe_only": True, "results": {}}
    for q1 in A["q1_grid"]:
        rows = {"folds": {}, "attacked": [], "benign": []}
        for f in folds:
            ref = reference_from_mask(data, data.fold != f)

            def indicators(eid):
                seq = []
                for i in sorted(by_ep[eid], key=lambda j: data.steps[j].index):
                    s = data.steps[i]
                    x = dict(s.features)
                    x["x_beh4"] = float(s.transition not in ref.transitions)
                    seq.append(deviation_indicator(x))
                return seq

            ben_fit = [indicators(e) for e in data.episodes if not data.episodes[e].attacked
                       and data.episode_fold[e] != f and by_ep[e]]
            try:
                fit = fit_a2(ben_fit, q1, A["q0_floor"], A["false_alarm_target"])
            except ValueError as exc:
                rows["folds"][f] = {"undefined": str(exc)}
                continue
            rows["folds"][f] = {"q0": fit.q0, "q0_raw": fit.q0_raw, "h": fit.h, "fit_false_alarm": fit.benign_false_alarm}
            for e in data.episodes:
                if data.episode_fold[e] != f or not by_ep[e]:
                    continue
                ind = indicators(e)
                ss = sorted(by_ep[e], key=lambda j: data.steps[j].index)
                if data.episodes[e].attacked:
                    nu = next((data.steps[i].index for i in ss if data.steps[i].after_change_point), None)
                    first_pos = next((data.steps[i].index for i in ss if data.steps[i].label), None)
                    r = evaluate_episode(fit, ind, nu)
                    rows["attacked"].append({"eid": e, "nu": nu, "first_pos": first_pos, "alarm": r.alarm_time,
                                             "delay": r.delay, "before": r.alarm_before_change})
                else:
                    r = evaluate_episode(fit, ind, None)
                    rows["benign"].append({"eid": e, "alarm": r.alarm_time})
        att = [r for r in rows["attacked"] if r["first_pos"] is not None]
        det = [r for r in att if r["alarm"] is not None and r["nu"] is not None and r["alarm"] >= r["nu"]]
        timely = [r for r in att if r["alarm"] is not None and r["alarm"] <= r["first_pos"]]
        summary = {
            "folds_defined": sum(1 for v in rows["folds"].values() if "undefined" not in v),
            "attacked_with_positive": len(att),
            "detection_rate_after_change": len(det) / len(att) if att else None,
            "alarm_at_or_before_first_positive_step": len(timely) / len(att) if att else None,
            "median_delay_steps": float(np.median([r["delay"] for r in det])) if det else None,
            "alarm_before_change_rate": float(np.mean([r["before"] for r in rows["attacked"]])) if rows["attacked"] else None,
            "heldout_benign_false_alarm": float(np.mean([r["alarm"] is not None for r in rows["benign"]])) if rows["benign"] else None,
            "attacked_without_change_point": sum(1 for r in rows["attacked"] if r["nu"] is None),
        }
        out["results"][str(q1)] = {"summary": summary, "folds": rows["folds"]}
        print("A2 q1", q1, summary)
    write_json("e3_a2_cusum_observe_only.json", out)


# ---------------------------------------------------------------------------
# stage: xt (cross-template + distributed defenses)
# ---------------------------------------------------------------------------

def stage_xt():
    st = make_setup()
    raw = load_raw()
    data = build("primary", raw)
    fits = load_state("crossfit")
    rm = load_state("rmod")
    pol = build_policies(fits, rm["rmod"])
    prim = fits["label_nll_primary"]
    folds = sorted(set(data.fold.tolist()), key=str)
    refs = {f: reference_from_mask(data, data.fold != f) for f in folds}
    xt = build("cross_template", raw)
    out = {"provenance": provenance(), "cross_template": {}, "distributed_defenses_recorded": {}}
    # discrimination/calibration on other templates with the primary fold models
    templates = sorted({s.attack_type for s in xt.steps})
    p_x = np.full(len(xt.steps), np.nan)
    for f in folds:
        idx = [i for i, s in enumerate(xt.steps) if s.injection_task_id == f]
        if not idx:
            continue
        X = design_matrix([xt.steps[i] for i in idx], refs[f])
        ff = prim.fits[f]
        s = ff.intercept + X @ np.asarray(ff.coefficients)
        p_x[idx] = 1 / (1 + np.exp(-(ff.gamma_1 * s + ff.gamma_0)))
    # replays on cross-template episodes (fold = injection task; benign none here)
    xt.episode_fold = {e: xt.episodes[e].injection_task_id for e in xt.episodes}
    G.update(policies=pol, fits=fits)
    configs = {k: v for k, v in replay_configs().items() if k in ("B0", "REM_step_level_no_reviewer", "REM_episode_level_no_reviewer",
                                                                    "B1_episode_level_no_reviewer", "B1_step_level_no_reviewer")}
    res = run_replays(configs, sorted(xt.episodes), st, xt, refs)
    by = collections.defaultdict(dict)
    for eid, c, u, s_, err, aud in res:
        by[eid][c] = (u, s_, err, aud)
    for t in templates:
        m = np.array([s.attack_type == t for s in xt.steps])
        eids = [e for e in xt.episodes if xt.episodes[e].attack_type == t]
        valid = [e for e in eids if by[e]["B0"][0] == xt.episodes[e].utility and by[e]["B0"][1] == xt.episodes[e].security]
        row = {"steps": prob_metrics(xt.y[m], p_x[m]), "episodes": len(eids), "replay_valid": len(valid)}
        for c in configs:
            row[c] = {"ASR": float(np.mean([by[e][c][1] for e in valid])) if valid else None,
                      "utility_under_attack": float(np.mean([by[e][c][0] for e in valid])) if valid else None}
        out["cross_template"][t] = row
        print(t, row["steps"]["roc_auc"], {c: row[c]["ASR"] for c in configs})
    dd = build("defense", raw)
    for pipe in sorted({e.pipeline for e in dd.episodes.values()}):
        eps = [e for e in dd.episodes.values() if e.pipeline == pipe]
        att = [e for e in eps if e.attacked]
        ben = [e for e in eps if not e.attacked]
        out["distributed_defenses_recorded"][pipe] = {
            "ASR_recorded": float(np.mean([e.security for e in att])) if att else None,
            "benign_utility_recorded": float(np.mean([e.utility for e in ben])) if ben else None,
            "utility_under_attack_recorded": float(np.mean([e.utility for e in att])) if att else None,
            "n_att": len(att), "n_ben": len(ben)}
    write_json("e4_cross_template_and_defenses.json", out)
    print(out["distributed_defenses_recorded"])


if __name__ == "__main__":
    stages = {"crossfit": stage_crossfit, "rmod": stage_rmod, "observe": stage_observe,
              "replay": stage_replay, "a2": stage_a2, "xt": stage_xt}
    for name in sys.argv[1:] or list(stages):
        print(f"== stage {name}")
        stages[name]()
