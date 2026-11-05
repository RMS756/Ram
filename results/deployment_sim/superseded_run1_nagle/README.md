# Superseded run 1 (5 Nov 2026) — kept for transparency

Decisions and outcomes of this run are identical to the corrected run: 0 parity mismatches on 3,334 episodes × 3 configurations.

Its latency figures are **not valid as gateway measurements**: about 44 ms per agent turn, for every configuration including B0. The prototype HTTP servers left Nagle's algorithm on, which interacts with delayed TCP acknowledgements to stall each response by about 40 ms; a minimal check confirmed 44 ms versus 0.55 ms. Both servers now set TCP_NODELAY (`disable_nagle_algorithm = True`), and the run was repeated. The per-episode `episodes.jsonl` of this run was not kept.
