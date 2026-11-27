"""Five-layer REM architecture diagrams: current v1.0 and proposed REM-DiD.
Exactly five layers; audit, monitoring and offline fitting/recalibration are a cross-cutting band.
Proposed (unimplemented) items are drawn dashed and tagged [P]."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

INK, MUTED, SURF = "#1f2933", "#52606d", "#ffffff"
LAYER_FILL, LAYER_EDGE = "#eef2f7", "#3e4c59"
PROP_EDGE, PROP_FILL = "#b4530f", "#fff4e8"
BAND = "#f5f5f0"

LAYERS = ["1  Input & Context", "2  Detection", "3  Behavioral Analysis",
          "4  Decision Engine", "5  Mitigation"]

CURRENT = [
    [("Segment provenance labels (least-trusted inheritance)", 0),
     ("Exact-string entity matching", 0)],
    [("x_ctx2: union of 6 instruction patterns (episode-level)", 0)],
    [("History x_beh1-4 (x_beh1 duplicates x_ctx2)", 0),
     ("Action x_act1-3", 0)],
    [("Predicates D1 (prohibited list), D2 (missing evidence)", 0),
     ("Ridge LR -> Platt on logit -> consequence tier -> expected-loss verdict", 0)],
    [("Allow / Modify / Escalate / Block, step-level", 0),
     ("No reviewer: Modify and Escalate both withhold", 0)],
]
PROPOSED = [
    [("Segment provenance labels", 0), ("[P] Value lineage + canonical forms", 1),
     ("[P] Trusted Authorization Envelope (trusted channel only)", 1)],
    [("x_ctx2 patterns", 0), ("[P] Separate sub-signals + correlation control", 1),
     ("[P] Call-linked injection evidence; x_ctx1 classifier (D-8)", 1)],
    [("History + action evidence", 0), ("[P] Dedupe x_beh1; credential integrity", 1),
     ("[P] TAE divergence; retry tracking (live only)", 1)],
    [("4A  D1, D2 + [P] non-compensatory constraints A1-A9", 1),
     ("4B  Ridge LR -> Platt -> tier -> expected loss (may tighten, never loosen)", 0)],
    [("Step-level verdict semantics", 0), ("[P] Parameter-bound permits; fail-safe", 1),
     ("[P] Reviewer channel; ONE declared Modify (no recipient/amount change)", 1)],
]

def draw(rows, title, out, legend):
    fig, ax = plt.subplots(figsize=(11, 7.6), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    fig.patch.set_facecolor(SURF)
    ax.text(2, 97, title, fontsize=13, weight="bold", color=INK, va="top")
    top, h, gap = 89, 13.2, 1.8
    for i, (name, items) in enumerate(zip(LAYERS, rows)):
        y = top - i * (h + gap) - h
        ax.add_patch(FancyBboxPatch((2, y), 76, h, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=LAYER_FILL, ec=LAYER_EDGE, lw=1.2))
        ax.text(3.2, y + h - 1.6, name, fontsize=10.5, weight="bold", color=INK, va="top")
        n = len(items); w = (73.5 - (n - 1) * 1.2) / n
        for j, (txt, prop) in enumerate(items):
            x = 3.2 + j * (w + 1.2)
            ax.add_patch(FancyBboxPatch((x, y + 1.0), w, h - 6.2,
                         boxstyle="round,pad=0,rounding_size=0.8",
                         fc=PROP_FILL if prop else SURF, ec=PROP_EDGE if prop else MUTED,
                         lw=1.1, ls="--" if prop else "-"))
            ax.text(x + w / 2, y + 1.0 + (h - 6.2) / 2, _wrap(txt, int(w * 1.05)),
                    fontsize=7.6, color=INK, ha="center", va="center")
        if i < 4:
            ax.annotate("", xy=(40, y - gap + 0.15), xytext=(40, y - 0.15),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0))
    yb = top - 5 * (h + gap) + gap
    ax.add_patch(FancyBboxPatch((81, yb), 17, top - yb, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=BAND, ec=MUTED, lw=1.0))
    ax.text(89.5, top - 1.5, "Cross-cutting\n(not a layer)", fontsize=9, weight="bold",
            color=INK, ha="center", va="top")
    cc = ["Append-only audit record\n(verdict source, p,\nattribution audit-only)",
          "Monitoring: CUSUM\nobserve-only, outside\nthe verdict path",
          "Offline fitting and\nrecalibration\n(ridge LR, Platt)"]
    if legend:
        cc[0] += "\n[P] + 4A reason codes,\npermit IDs"
    for k, t in enumerate(cc):
        ax.text(89.5, top - 14 - k * 22, t, fontsize=7.6, color=INK, ha="center", va="top")
    if legend:
        ax.add_patch(FancyBboxPatch((2, 0.8), 3, 2.2, boxstyle="round,pad=0,rounding_size=0.4",
                     fc=PROP_FILL, ec=PROP_EDGE, ls="--"))
        ax.text(5.8, 1.9, "[P] proposed, not implemented, not evaluated; each needs a supervisor decision",
                fontsize=8, color=INK, va="center")
        ax.add_patch(FancyBboxPatch((60, 0.8), 3, 2.2, boxstyle="round,pad=0,rounding_size=0.4",
                     fc=SURF, ec=MUTED))
        ax.text(63.8, 1.9, "exists in REM v1.0", fontsize=8, color=INK, va="center")
    else:
        ax.text(2, 1.9, "All boxes describe REM v1.0 as implemented and evaluated in offline replay "
                "(AgentDojo 0.1.35 banking, NO-ADAPT).", fontsize=8, color=MUTED, va="center")
    fig.savefig(out, bbox_inches="tight", facecolor=SURF); plt.close(fig)

def _wrap(t, width):
    import textwrap
    return "\n".join(textwrap.wrap(t, max(width, 12)))

if __name__ == "__main__":
    d = Path(__file__).resolve().parents[1] / "figures"; d.mkdir(exist_ok=True)
    draw(CURRENT, "REM v1.0 (current): five layers", d / "fig_rem_v1_0_current.png", False)
    draw(PROPOSED, "REM-DiD (proposed): same five layers, strengthened controls",
         d / "fig_rem_did_proposed.png", True)
    print("ok")
