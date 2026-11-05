# Experimental setup and metrics — update draft

- **Dataset preparation and training:** unchanged from §3.11 and §4.2–4.3. The draft must state the leakage audit's findings (`01_AUDIT/REM_DATA_LEAKAGE_AUDIT.md`):
  - attacker objectives held out per fold;
  - user tasks, models and the attack template shared;
  - no lock-box set;
  - all results exploratory.
- **Configurations evaluated:** No Defense, REM-Lite and Full REM (Mode A). MELON is not executed. No configuration was run in Mode B.
- **Denominators:**
  - ASR: attacked valid episodes (2,979);
  - benign utility: benign valid episodes (334);
  - utility under attack: attacked valid episodes;
  - invalid episodes (21, AM-4) and errors (0) are reported separately.
- **Uncertainty:** grouped bootstrap; paired differences on matched episodes.
