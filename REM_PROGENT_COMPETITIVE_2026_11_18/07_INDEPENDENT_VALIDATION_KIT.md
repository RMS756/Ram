# Independent-validation kit (sealed; NOT EXECUTED)

Files:
- `validation_kit/authorization_label_schema.json`: the label schema frozen on 16 November 2026, copied unchanged;
- `validation_kit/VALIDATION_MANIFEST.json`: arms to score, SHA-256 of every code file that decides, one allowed run;
- `experiments/progent_competitive/validation_scorer.py`: the executable scorer.

**Procedure:**
1. Two people who have not seen the code, fixtures or results write and cross-check the request items under the schema. Each item states its authorized and unauthorized calls, plus the reviewer's agreement.
2. The receiver records the file's SHA-256, the two pseudonyms and `simulated_participants: false` in the manifest, in one dated commit, **before** scoring.
3. Run `python3 experiments/progent_competitive/validation_scorer.py --requests <file>`. It refuses to run in any of these cases:
   - the file or any code hash differs from the manifest;
   - participants are simulated;
   - an item lacks an independent reviewer;
   - the single allowed run was already used.

   It writes `RESULT_<date>.json` and `RUN_RECORD.json`.
4. Report all counts: authorized, unauthorized and not-decidable released / n per arm. Items whose reviewer disagrees are reported separately; nothing is dropped.

**Checked in this session:**
- `--selftest` on one synthetic item (C1 released the authorized call and withheld the unauthorized one; nothing was written);
- the refusal path with an unsealed manifest.

No real items exist, and no reviewer took part.
