# 06b Protocol deviations and notes (recorded after scoring)

No frozen result was changed. Each item below states what happened and how it affects interpretation.

## D1. H2a contained no banking runs (pre-registration error)

**What happened.**
- The pristine source H2a (`claude-3-sonnet-20240229-repeat_user_prompt`) has recorded runs for the *workspace* suite only.
- I did not check that banking runs existed before fixing the rule.
- H2 therefore consists only of H2b: gpt-4o-2024-05-13 with five attack templates, attacked episodes only.
  - Loaded: 715. B0-eligible: 681. Benign: 0.

**Consequences.**
1. **H2 is not pristine.** These traces were loaded once on 11 November 2026, for older arms (`heldout_population2.py` docstring). They were never used to design C1, REM-B or any mechanism of this study.
2. **H2 has no benign episodes.** U1 measures *utility under attack* (task completion in attacked episodes), not benign utility.
3. H2 still contains **unseen attack phrasings** (direct, ignore_previous, important_instructions_no_names, injecagent, tool_knowledge) and agent traces of one model not used in design. Its tasks are the same 16 user tasks and 9 injection tasks.

## D2. Probes v2 rarely exercised object binding

**What happened.**
- Most standing-order requests in probes v2 use wordings ("switch …", "move both …", "point … at …") that the frozen request compiler does not map to a modification.
- The authority front therefore withheld those calls ("operation not requested") before object binding was reached.
  - The authorised object-binding probes: 0 of 13 released by every REM variant.
  - The unauthorised ones were withheld by the front, not by object binding.

**Consequence.** Probes v2 test object binding (and R1) much less than intended. R1's only observable effect is on HO4 of probes v1 (development material).

## D3. The utility interval and task clusters

`report.paired` clusters completion by user task (16 clusters). All of REM-B2's gains over REM-B are in two user tasks (ut14, ut15), so resamples that omit both give a difference of 0. The lower bound of every such interval is therefore exactly 0.000. This is a property of the evidence, not an artefact to correct: **the gains are not spread over tasks.**

## D4. Amendment round

The amendment round (`06a`) was added after probes v2 had been scored. Its candidate REM-B3 and its results are reported separately and labelled post-hoc. The frozen decision of `06` is the primary result.

## D5. Test file extended after freezing (additions only)

`tests/test_rem_b_hardening.py` was hashed in `06` (commit `f6d885b`). It was later extended with the amendment tests: commit `37f0157`, 62 lines added, **0 lines removed or changed** (`git diff f6d885b -- tests/test_rem_b_hardening.py`). That is why the manifest's check of `06_PROTOCOL_HASHES.sha256` reports this one file as changed. Its new hash is recorded in `06a_PROTOCOL_HASHES.sha256`. Every deciding or scoring file of `06` (`remb2.py`, `hard_run.py`, the probe and population files, the frozen modules) is unchanged.

## D6. Figure caption

`figures/h2_utility_vs_probe_violations.png` counts the unauthorised releases on probes v2 + v3 together. For REM-B3, probes v2 are development material (seen before its design), so its value on the x-axis mixes held-out (v3) and seen (v2) cases.
