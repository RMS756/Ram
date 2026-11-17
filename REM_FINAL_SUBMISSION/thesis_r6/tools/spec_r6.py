"""Specification of the sixth, condensed editorial edition (R6), 17 November 2026. See make_r6.py.

MOVE         : R5 units printed in the supplement only (with all their sub-units).
REPLACE      : R5 units whose heading stays and whose body is replaced by a shorter text (text_r6/<file>); the R5 body goes
               verbatim to the supplement.
INSERT_AFTER : (R5 unit, text_r6 file) new text placed after the unit and its sub-units.
EDITS        : (file, exact R5 text, new text) dated corrections; each must match exactly once.
ALIAS        : R5 section numbers that are printed elsewhere in R6 (cross-references follow them).

Sources of the corrections: the external review of 17 November 2026 (REM_Claude_Latest_Review_AR_2026-11-17.md) and the
repair study of 17 November 2026 (REM_REPAIR_STUDY_2026_11_17/).
"""
C1, C2, C3, C4, C5, AP = ('CHAPTER_01_FINAL', 'CHAPTER_02_FINAL', 'CHAPTER_03_FINAL', 'CHAPTER_04_FINAL', 'CHAPTER_05_FINAL',
                          'APPENDICES_FINAL')

MOVE = [
    # Chapter 2: detail of the review process (summarized in a new short section) and secondary syntheses
    '2.2.2', '2.2.3', '2.8.4', '2.9.1', '2.10', '2.12.1', '2.12.4',
    # Chapter 3: duplicates of Chapter 1 and implementation detail
    '3.1.2', '3.1.3', '3.1.4', '3.11.8', '3.15',
    # Chapter 4: chronology, pilot feasibility, diagnostic arms, processing-time detail
    '4.2.1#Chronology of design, amendments and analyses', '4.2.1#Chronology of the analyses of November 2026', '4.2.3',
    '4.6.6#What the diagnostic arms show', '4.6.8#Intervention burden and processing time', '4.4.4',
    '4.6.10#Why benign utility falls', '4.6.10#Why behavioral evidence did not help, and calibration changed little',
    '4.6.10#The security–utility frontier that was measured',
    # Chapter 3: outcome-layer detail and the threats list (Chapter 4, Section 4.6.11, holds the complete list)
    '3.12.4', '3.16',
    # Appendices: review tables, implementation detail, live status, mitigation-semantics replay
    'App-A', 'App-B', 'App-D', 'App-E',
]
REPLACE = {'4.5.3': 'ch4_permission_ablation.md'}
INSERT_AFTER = [
    ('2.2.1', 'ch2_search_summary.md'),
    ('2.12.6', 'ch2_update_1117.md'),
    ('3.14', 'ch3_amount.md'),
    ('4.5.3', 'ch4_repair.md'),
    ('C.4', 'app_logistic.md'),
]
ALIAS = {'A.15': 'C.90'}
APPENDIX_RENAME = {'C': 'A', 'F': 'B'}

EDITS = [
    # ---------------------------------------------------------------- Chapter 1
    (C1, "and the same rule used alone, without any learned decision, gives the outcomes of every learned or statistically "
         "calibrated decision tested behind it. The measured change is due to the rule and not to the learned core, and a "
         "validation on independently written requests was defined and not executed (Chapter 4, Sections 4.4.3, 4.5.3 and 4.6.9).",
     "and the rule's authority guard used alone (GV), without any learned decision, gives the outcomes of every learned or "
     "statistically calibrated decision tested behind it, except a Neyman-Pearson threshold at 0.01, which loses tasks. The "
     "measured change is due to deterministic components and not to the learned core. An external review then found that the "
     "guard accepted computed amounts it never computed and read a percentage coefficient as an amount; a typed amount verifier "
     "repairs both, at the cost of the tasks whose amounts the request does not determine. Request-derived argument checks of "
     "this kind have also been published by others (Chapter 2, Section 2.12.6). A validation on independently written requests "
     "was defined and not executed (Chapter 4, Sections 4.4.3, 4.5.3, 4.5.90 and 4.6.9)."),
    (C1, "Appendices A to F hold the evidence matrix of the review, the implementation details, the equation provenance table, "
         "the design and status of the live-agent and MELON evaluations, the sensitivity analysis of the mitigation semantics, "
         "and the register of open supervisor decisions.",
     "Appendix C holds the notation, the layer interfaces, the optional sequential analysis, the provenance of the equations and "
     "the logistic model of Equation 2.1, and Appendix F the register of open supervisor decisions. This condensed edition "
     "prints the review's evidence matrix, the implementation details, the live-agent and MELON status, the sensitivity "
     "analysis of the mitigation semantics, and the history of the analyses in an indexed supplement; a reference of the form "
     "\"Section S-x\" or \"Table S-x\" points to it. Nothing was removed from the record: the fifth edition is preserved."),
    # ---------------------------------------------------------------- Chapter 2
    (C2, "**Bounds.** The gap is bounded by the record-level review, by the absence of a systematic search after 30 October 2026, "
         "and by the abstract-level knowledge of three close works.",
     "**Bounds.** The gap is bounded by the record-level review, by the absence of a systematic search after 30 October 2026, "
     "and by the abstract-level knowledge of three close works. Three preprints of November 2026 (PACT, ROPE and CapLite; "
     "Section 2.12.6) check tool arguments against the request or against their origin. At abstract level none of them "
     "compares a learned decision behind such a check with the check used alone, so the evidence gap stands; request-derived "
     "argument checking is not itself a gap."),
    # ---------------------------------------------------------------- Chapter 3
    (C3, "It serves as the deterministic control against which every learned or calibrated decision behind the guard is "
         "compared (Chapter 4, Section 4.5.3).",
     "It serves as the deterministic control against which every learned or calibrated decision behind the guard is "
     "compared (Chapter 4, Section 4.5.3). The constraint has a defect: it can read a percentage coefficient as the amount "
     "(paragraph F)."),
    # ---------------------------------------------------------------- Chapter 4
    (C4, "| Kairos (Hempel et al., 2026; abstract only) | Enforces on effects at the system boundary | Not available; full text not read |",
     "| Kairos (Hempel et al., 2026; abstract only) | Enforces on effects at the system boundary | Not available; full text not read |\n"
     "| PACT (Fan et al., 2026; abstract only) | Checks each tool argument's provenance against a role-specific contract; the "
     "closest conceptual match to the authority guard of Section 4.4.3 | Not run; full text not reachable |\n"
     "| ROPE (Ma et al., 2026; abstract and repository) | Admits a value to a state-changing tool only if it traces to the user, a "
     "named source or the user's records; its audited banking table guards recipients, not amounts | Not run; needs a router "
     "model and live agents |\n"
     "| CapLite (Xu et al., 2026; abstract only) | Admits a write only if its recipient, amount, object or destination is stated "
     "in the request; reports no successful attack on AgentDojo | Not run; full text not reachable |"),
    (C4, "4. **Attribution.** The measured changes come from deterministic matching of the call against the instruction. The "
         "guard used alone (GV) gives the outcomes of every learned or calibrated variant that was tested (Table 4.19). The "
         "semantic verifier was not run.",
     "4. **Attribution.** The measured changes come from deterministic matching of the call against the instruction. The "
     "guard used alone (GV) gives the outcomes of every learned or calibrated variant that was tested, except the "
     "Neyman-Pearson threshold at 0.01, which completes fewer tasks (Table 4.19). With the typed amount verifier the same holds: "
     "HV_math has the outcomes of GV_math (Section 4.5.90). The semantic verifier was not run."),
    (C4, "Best supported on development data: GV.",
     "Best supported on development data: GV, whose amount handling has the defects of Section 4.5.90. GV_math repairs them at "
     "a cost in completed tasks; no choice between them is made here (decision SD-AMT, Appendix F)."),
    (C4, "| Section 4.5.3: the guard used alone (GV) has the outcomes of the learned arm and of every threshold and estimator "
         "tested; every attack-labelled call is stopped before a model is consulted.",
     "| Section 4.5.3: the guard used alone (GV) has the outcomes of the learned arm and of every threshold and estimator "
     "tested except the Neyman-Pearson threshold at 0.01, which loses tasks; every attack-labelled call is stopped before a "
     "model is consulted; with the typed amount verifier, HV_math has the outcomes of GV_math (Section 4.5.90)."),
    (C4, "18. **The benchmark's attacks do not reach the decision behind the permission guard.** Every attack-labelled call is "
         "stopped by the guard, so the comparison of decision methods behind it measures only how much legitimate work each "
         "withholds (Section 4.5.3).",
     "18. **The benchmark's attacks do not reach the decision behind the permission guard.** Every attack-labelled call is "
     "stopped by the guard, so the comparison of decision methods behind it measures only how many calls that are not "
     "attack-labelled each withholds (Section 4.5.3). A call that is not attack-labelled is not thereby authorized: the label "
     "refers to the benchmark's attacker goal, and no independent authorization audit was made.\n"
     "19. **Defects in amount handling.** The guard accepted unverified computed amounts, and its value constraint misread "
     "percentage coefficients (Section 4.5.90). No stored outcome count changes, because no attack-labelled call reached that "
     "stage, but the frozen GV and HV do not verify derived amounts. The repair was written after the defects and the "
     "benchmark's requests were known; its grammar withholds one legitimate fixture; and its benefit cannot be measured on "
     "AgentDojo, whose requests contain no supported calculation.\n"
     "20. **Close work known from abstracts.** PACT, ROPE and CapLite (November 2026) are known from abstracts, ROPE also from "
     "its repository; none was run."),
    (C4, "The guard used alone (GV) has the outcomes of every learned or calibrated decision tested behind it. The measured "
         "change belongs to the rule, not to t",
     "The guard used alone (GV; 147 and 32 benign tasks, against G3's 132 and 29) has the outcomes of every learned or "
     "calibrated decision tested behind it, except a Neyman-Pearson threshold at 0.01, which loses tasks. An external review "
     "found that the guard accepted unverified computed amounts; a typed amount verifier repairs this with no successful "
     "attack and 95 and 159 fewer completed tasks, all in requests whose amount it cannot verify, and the learned decision "
     "behind it again changes nothing (Section 4.5.90). The measured change belongs to the rule, not to t"),
    # ---------------------------------------------------------------- Chapter 5
    (C5, "In the exploratory extension the deterministic permission rule carries the measured change; behind it, a learned "
         "model, two calibrated thresholds and boosted trees changed no outcome compared with the rule alone, because no "
         "attack-labelled call reached them",
     "In the exploratory extension the deterministic permission rule carries the measured change; behind its authority "
     "guard, a learned model, calibrated thresholds and boosted trees changed no outcome compared with the guard used alone "
     "(GV), except a Neyman-Pearson threshold at 0.01 that lost tasks, because no attack-labelled call reached them; the same "
     "holds with the typed amount verifier (GV_math and HV_math)"),
    (C5, "The rule used alone (GV) has the outcomes of the learned model and of every calibrated threshold and estimator "
         "tested behind it |",
     "The authority guard used alone (GV; 147 and 32 benign tasks, against G3's 132 and 29) has the outcomes of the learned "
     "model and of every calibrated threshold and estimator tested behind it, except a Neyman-Pearson threshold at 0.01, which "
     "loses tasks. GV accepted unverified computed amounts; with a typed amount verifier (GV_math) there is no successful "
     "attack, 95 and 159 fewer completed tasks, and again no learned contribution |"),
    (C5, "| Identical outcomes to the guard used alone (GV) on every episode, the probe and the fixtures; no attack-labelled "
         "call reaches them |",
     "| Identical outcomes to the guard used alone (GV) on every episode, the probe and the fixtures, except a Neyman-Pearson "
     "threshold at 0.01, which loses tasks; no attack-labelled call reaches them |"),
    (C5, "| Decision parity with GV; the provenance rule removes no attack and withholds a few legitimate calls | "
         "Implementation option; not recommended without new evidence |",
     "| Decision parity with GV; the provenance rule removes no attack and withholds a few legitimate calls | "
     "Implementation option; not recommended without new evidence |\n"
     "| Typed amount verifier behind the guard (GV_math; HV_math with the learned decision) | Repairs the two amount defects; "
     "no successful attack; 95 and 159 fewer completed tasks, in requests whose amount it cannot verify; one legitimate fixture "
     "withheld; HV_math has the outcomes of GV_math | Exploratory; decision SD-AMT pending |"),
    (C5, "the Progent paper was read in full.",
     "the Progent paper was read in full. PACT, ROPE and CapLite (November 2026) are known from abstracts, ROPE also from its "
     "repository."),
    (C5, "10. **Further benchmarks,** with new user tasks, reported per benchmark.",
     "10. **Further benchmarks,** with new user tasks, reported per benchmark.\n"
     "11. **Independent validation of the amount verifier** on payment requests written and reviewed by others, with half of "
     "the accounts taken from Progent's list so that the comparison tests amounts and not recipients "
     "(`REM_REPAIR_STUDY_2026_11_17/07_INDEPENDENT_VALIDATION_KIT.md`)."),
    (C5, "Behind the rule, a learned model, two statistically calibrated thresholds and boosted trees gave exactly the outcomes "
         "of the rule used alone, because",
     "Behind its authority guard, a learned model, calibrated thresholds and boosted trees gave exactly the outcomes of the "
     "guard used alone (GV), except one threshold that lost tasks, because"),
    (C5, "and the rule has not been tested on requests written by anyone but its author.",
     "and the rule has not been tested on requests written by anyone but its author. An external review then showed that the "
     "guard accepted computed amounts it never computed; a typed verifier repairs this, and the price is that payments whose "
     "amount the request does not determine are withheld."),
    # ---------------------------------------------------------------- Appendix F
    (AP, "| SD-D2 | Whether the declared predicate D2",
     "| SD-AMT | Typed verification of request-derived amounts (GV_math; Chapter 4, Section 4.5.90) | Reported as proposed and "
     "exploratory; the frozen GV keeps its defects | Adopt the verifier, extend its grammar after independent validation, or "
     "keep GV |\n| SD-D2 | Whether the declared predicate D2"),
]
