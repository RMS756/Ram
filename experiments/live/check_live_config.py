"""Fail-closed check of a live-evaluation configuration (R4). It runs nothing.

usage: python3 experiments/live/check_live_config.py <config.yaml>
Exit status 0 only when no value is REQUIRED_FROM_DESIGN; 2 otherwise.
"""
import sys

import yaml


def missing(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from missing(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from missing(v, f"{path}[{i}]")
    elif node == "REQUIRED_FROM_DESIGN":
        yield path


def main(path):
    cfg = yaml.safe_load(open(path, encoding="utf-8"))
    gaps = list(missing(cfg))
    for g in gaps:
        print(f"[DESIGN BLOCKED] {g}: not specified")
    if gaps:
        print(f"{len(gaps)} required design inputs missing; the live evaluation must not start.")
        return 2
    print("All design inputs present. Authorization, budget and pre-registration must still be checked by a person.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
