"""REM-X proposed architecture (design only). Exactly five layers; audit, transaction
ledger, monitoring and offline fitting form a cross-cutting band (not a layer).
Status: [V1] REM v1.0; [DiD] implemented in REM-DiD; [X-P] proposed, not implemented."""
import textwrap
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

INK, MUTED, SURF = "#1f2933", "#52606d", "#ffffff"
LAYER_FILL, LAYER_EDGE = "#eef2f7", "#3e4c59"
V1_FILL = "#e4e7eb"
PROP_EDGE, PROP_FILL = "#b4530f", "#fff4e8"
BAND = "#f5f5f0"
STYLE = {"V1": (V1_FILL, MUTED, "-"), "DiD": (SURF, MUTED, "-"), "X": (PROP_FILL, PROP_EDGE, "--")}

LAYERS = ["1  Input & Context", "2  Detection", "3  Behavioral Analysis",
          "4  Decision Engine", "5  Mitigation"]
ROWS = [
    [("[DiD] Field-level sources, canonical forms, inferred lineage", "DiD"),
     ("[X-P] Authorization record: pinned, unspecified or delegated fields; limits", "X"),
     ("[X-P] Deterministic schema extraction from a named source", "X")],
    [("[DiD] Sub-signals, call-linked evidence; unavailable = unknown", "DiD"),
     ("[X-P] Delegated-source screening (clean / flagged / unknown)", "X")],
    [("[DiD] New payee, redirect, repeat, retry, switch", "DiD"),
     ("[X-P] Ledger-derived cumulative and read-then-pay features", "X"),
     ("[X-P] Optional learned anomaly score (advisory)", "X")],
    [("[DiD] 4A authorization; most-restrictive precedence", "DiD"),
     ("[X-P] Delegation conditions (a)-(d); atomic reservation", "X"),
     ("[V1] 4B ridge LR -> Platt -> tier -> expected loss: advisory, tighten-only", "V1")],
    [("[DiD] Exact-action single-use permits; fail-closed", "DiD"),
     ("[X-P] Independent adapter re-check of economic terms", "X"),
     ("[X-P] Post-execution reconciliation: detect and halt, no reversal", "X")],
]
BAND_ITEMS = [("[DiD] Hash-chained audit", "DiD"),
              ("[X-P] Transaction ledger: envelope, reservations, permits, effects; read by 4A and L5 only", "X"),
              ("[V1] Monitoring: CUSUM observe-only", "V1"),
              ("[V1] Offline fitting and recalibration", "V1")]


def box(ax, x, y, w, h, txt, kind, fs=7.4):
    fc, ec, ls = STYLE[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.8",
                                fc=fc, ec=ec, lw=1.1, ls=ls))
    ax.text(x + w / 2, y + h / 2, "\n".join(textwrap.wrap(txt, max(12, int(w * 1.15)))),
            fontsize=fs, color=INK, ha="center", va="center")


def main(out):
    fig, ax = plt.subplots(figsize=(11.5, 8.0), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    fig.patch.set_facecolor(SURF)
    ax.text(2, 98, "REM-X (proposed design): five layers, cross-cutting ledger and audit",
            fontsize=13, weight="bold", color=INK, va="top")
    ax.text(2, 94.6, "Design only. Nothing marked [X-P] is implemented or evaluated.",
            fontsize=8.5, color=MUTED, va="top")
    top, h, gap = 91, 13.4, 1.9
    for i, (name, items) in enumerate(zip(LAYERS, ROWS)):
        y = top - i * (h + gap) - h
        ax.add_patch(FancyBboxPatch((2, y), 75, h, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=LAYER_FILL, ec=LAYER_EDGE, lw=1.2))
        ax.text(3.2, y + h - 1.5, name, fontsize=10.2, weight="bold", color=INK, va="top")
        n = len(items); w = (72.6 - (n - 1) * 1.2) / n
        for j, (txt, kind) in enumerate(items):
            box(ax, 3.2 + j * (w + 1.2), y + 1.0, w, h - 6.0, txt, kind)
        if i < 4:
            ax.annotate("", xy=(40, y - gap + 0.15), xytext=(40, y - 0.15),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0))
    yb = top - 5 * (h + gap) + gap
    ax.add_patch(FancyBboxPatch((79.5, yb), 18.5, top - yb, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=BAND, ec=MUTED, lw=1.0))
    ax.text(88.75, top - 1.4, "Cross-cutting\n(not a layer)", fontsize=9, weight="bold",
            color=INK, ha="center", va="top")
    bh = 12.5
    for k, (txt, kind) in enumerate(BAND_ITEMS):
        box(ax, 80.5, top - 9 - (k + 1) * (bh + 2.5), 16.5, bh, txt, kind, fs=7.2)
    lx = 2
    for kind, label in (("V1", "[V1] REM v1.0, evaluated in the thesis"),
                        ("DiD", "[DiD] implemented in REM-DiD (replay or unit tested)"),
                        ("X", "[X-P] proposed, not implemented, not evaluated")):
        fc, ec, ls = STYLE[kind]
        ax.add_patch(FancyBboxPatch((lx, yb - 5.0), 2.6, 2.0, boxstyle="round,pad=0,rounding_size=0.4",
                                    fc=fc, ec=ec, ls=ls))
        ax.text(lx + 3.3, yb - 4.0, label, fontsize=7.6, color=INK, va="center")
        lx += 34
    ax.set_ylim(yb - 7, 100)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor=SURF)


if __name__ == "__main__":
    main(Path(__file__).resolve().parents[1] / "figures" / "fig_rem_x_proposed.png")
