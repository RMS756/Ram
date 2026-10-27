"""Build REFERENCES.bib and REFERENCE_VERIFICATION_MATRIX.xlsx from one table.

Verification in this session (27 Oct 2026) used the FastTrack literature
connector: Crossref DOI lookups (`verify_reference`) and OpenAlex search.
Direct access to api.crossref.org / api.openalex.org was refused by the
environment's network policy. Metadata checks are NOT full-text checks:
the column `formulation_check` carries the Chapter 3 status code and is not
upgraded here.
"""

import os

REFS = [
    # key, apa, bibtex-type, fields, doi, how_checked, metadata_status, formulation_check, used_for, notes
    dict(key="cox1958", apa="Cox, D. R. (1958). The regression analysis of binary sequences. Journal of the Royal Statistical Society: Series B (Methodological), 20(2), 215–232. https://doi.org/10.1111/j.2517-6161.1958.tb00292.x",
         type="article", f=dict(author="Cox, D. R.", title="The Regression Analysis of Binary Sequences", journal="Journal of the Royal Statistical Society: Series B (Methodological)", year="1958", volume="20", number="2", pages="215--232"),
         doi="10.1111/j.2517-6161.1958.tb00292.x", how="Crossref DOI lookup", meta="VERIFIED (Crossref: title, author, journal, vol 20(2), pp. 215-232, 1958)", form="IV (Ch.3 Table 3.17)", used="Eq. 3.1 logistic model", notes="Crossref lists online year 2018 (digitisation); print year 1958 is correct."),
    dict(key="lecessie1992", apa="le Cessie, S., & van Houwelingen, J. C. (1992). Ridge estimators in logistic regression. Applied Statistics, 41(1), 191–201. https://doi.org/10.2307/2347628",
         type="article", f=dict(author="le Cessie, S. and van Houwelingen, J. C.", title="Ridge Estimators in Logistic Regression", journal="Applied Statistics", year="1992", volume="41", number="1", pages="191--201"),
         doi="10.2307/2347628", how="Crossref DOI lookup", meta="VERIFIED (Crossref: title, authors, vol 41(1), 1992; Crossref gives first page 191 only)", form="IV; penalty constant pending (M1)", used="Eq. 3.2 ridge penalty", notes="End page 201 not confirmed by Crossref record."),
    dict(key="platt2000", apa="Platt, J. C. (2000). Probabilities for SV machines. In A. J. Smola, P. L. Bartlett, B. Schölkopf, & D. Schuurmans (Eds.), Advances in large margin classifiers (pp. 61–74). MIT Press. https://doi.org/10.7551/mitpress/1113.003.0008",
         type="incollection", f=dict(author="Platt, John C.", title="Probabilities for {SV} Machines", booktitle="Advances in Large Margin Classifiers", editor="Smola, A. J. and Bartlett, P. L. and Sch{\\\"o}lkopf, B. and Schuurmans, D.", publisher="MIT Press", year="2000", pages="61--74"),
         doi="10.7551/mitpress/1113.003.0008", how="Crossref bibliographic match", meta="DISCREPANCY: thesis cites 'Platt (1999) Probabilistic outputs for support vector machines…'; Crossref registers the MIT Press chapter as 'Probabilities for SV Machines', 2000, pp. 61-74", form="NC (full text not accessed)", used="Eq. 3.3 logistic calibration", notes="Editors listed from the book's standard citation; not returned by Crossref. Decide which version is cited (1999 technical report vs 2000 chapter) — see SOURCE_VERIFICATION_REPORT.md."),
    dict(key="guo2017", apa="Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In Proceedings of the 34th International Conference on Machine Learning (PMLR 70, pp. 1321–1330).",
         type="inproceedings", f=dict(author="Guo, Chuan and Pleiss, Geoff and Sun, Yu and Weinberger, Kilian Q.", title="On Calibration of Modern Neural Networks", booktitle="Proceedings of the 34th International Conference on Machine Learning", series="PMLR", volume="70", year="2017", pages="1321--1330"),
         doi="", how="OpenAlex search (arXiv 1706.04599 record)", meta="EXISTS (arXiv record, 4 authors, 2017); ICML/PMLR venue and pages NOT re-confirmed this session", form="FV (Ch.3)", used="Eqs. 3.3-3.4, 3.20; temperature scaling not adopted", notes="Pages 1321-1330 from the Stage 2 master; not re-checked."),
    dict(key="kull2017aistats", apa="Kull, M., Silva Filho, T., & Flach, P. (2017). Beta calibration: A well-founded and easily implemented improvement on logistic calibration for binary classifiers. In Proceedings of the 20th International Conference on Artificial Intelligence and Statistics (PMLR 54, pp. 623–631).",
         type="inproceedings", f=dict(author="Kull, Meelis and Silva Filho, Telmo and Flach, Peter", title="Beta Calibration: A Well-Founded and Easily Implemented Improvement on Logistic Calibration for Binary Classifiers", booktitle="Proceedings of the 20th International Conference on Artificial Intelligence and Statistics", series="PMLR", volume="54", year="2017", pages="623--631"),
         doi="", how="Stage 2 master only; OpenAlex search found the companion EJS article instead", meta="NOT RE-CONFIRMED THIS SESSION; companion 'Beyond sigmoids' (Electron. J. Statist., 2017, doi 10.1214/17-EJS1338SI) confirmed", form="FV (Ch.3)", used="Eq. 3.3 (logistic calibration discussion); beta calibration NOT adopted", notes="Ambiguity: two Kull et al. (2017) works exist. Chapter 3 must say which is cited."),
    dict(key="brier1950", apa="Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. Monthly Weather Review, 78(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2",
         type="article", f=dict(author="Brier, Glenn W.", title="Verification of Forecasts Expressed in Terms of Probability", journal="Monthly Weather Review", year="1950", volume="78", number="1", pages="1--3"),
         doi="10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2", how="Crossref DOI lookup", meta="VERIFIED (Crossref)", form="Convention unconfirmed (SC-5); Brier withheld in Ch.3", used="Brier score convention", notes="Stage 2 master said 'Not confirmed'; this session's Crossref lookup confirms the record. Full text still needed to settle the r-class sum (SC-5)."),
    dict(key="lundberg2017", apa="Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems 30 (pp. 4765–4774).",
         type="inproceedings", f=dict(author="Lundberg, Scott M. and Lee, Su-In", title="A Unified Approach to Interpreting Model Predictions", booktitle="Advances in Neural Information Processing Systems 30", year="2017", pages="4765--4774"),
         doi="", how="OpenAlex search (arXiv 1705.07874 record)", meta="EXISTS (arXiv record, 2 authors, 2017); NeurIPS pages NOT re-confirmed", form="FV (Ch.3)", used="Eqs. 3.11-3.12 (audit-only attribution)", notes=""),
    dict(key="page1954", apa="Page, E. S. (1954). Continuous inspection schemes. Biometrika, 41(1–2), 100–115. https://doi.org/10.1093/biomet/41.1-2.100",
         type="article", f=dict(author="Page, E. S.", title="Continuous Inspection Schemes", journal="Biometrika", year="1954", volume="41", number="1--2", pages="100--115"),
         doi="10.1093/biomet/41.1-2.100", how="Crossref DOI lookup", meta="VERIFIED (Crossref)", form="IV (Ch.3)", used="Eq. 3.16 CUSUM (optional, observe-only)", notes=""),
    dict(key="basseville1993", apa="Basseville, M., & Nikiforov, I. V. (1993). Detection of abrupt changes: Theory and application. Prentice Hall.",
         type="book", f=dict(author="Basseville, Mich{\\`e}le and Nikiforov, Igor V.", title="Detection of Abrupt Changes: Theory and Application", publisher="Prentice Hall", address="Englewood Cliffs, NJ", year="1993"),
         doi="", how="Crossref bibliographic match (book reviews only)", meta="EXISTS (two independent book reviews: J. R. Stat. Soc. A 158(1) 1995; Int. J. Adapt. Control 12(4) 1998); publication year not confirmed by a primary record — one review cites a 1996 printing", form="FV (Ch.3)", used="Eqs. 3.15-3.17", notes="Books carry no Crossref DOI; year 1993 retained from the standard citation."),
    dict(key="lorden1971", apa="Lorden, G. (1971). Procedures for reacting to a change in distribution. The Annals of Mathematical Statistics, 42(6), 1897–1908. https://doi.org/10.1214/aoms/1177693055",
         type="article", f=dict(author="Lorden, G.", title="Procedures for Reacting to a Change in Distribution", journal="The Annals of Mathematical Statistics", year="1971", volume="42", number="6", pages="1897--1908"),
         doi="10.1214/aoms/1177693055", how="Crossref DOI lookup", meta="VERIFIED (Crossref)", form="Cited only for the scope of optimality (not claimed)", used="CUSUM optimality caveat", notes=""),
    dict(key="moustakides1986", apa="Moustakides, G. V. (1986). Optimal stopping times for detecting changes in distributions. The Annals of Statistics, 14(4), 1379–1387. https://doi.org/10.1214/aos/1176350164",
         type="article", f=dict(author="Moustakides, George V.", title="Optimal Stopping Times for Detecting Changes in Distributions", journal="The Annals of Statistics", year="1986", volume="14", number="4", pages="1379--1387"),
         doi="10.1214/aos/1176350164", how="Crossref DOI lookup", meta="VERIFIED (Crossref)", form="Cited only for the scope of optimality (not claimed)", used="CUSUM optimality caveat", notes=""),
    dict(key="reynolds1999", apa="Reynolds, M. R., Jr., & Stoumbos, Z. G. (1999). A CUSUM chart for monitoring a proportion when inspecting continuously. Journal of Quality Technology, 31(1), 87–108. https://doi.org/10.1080/00224065.1999.11979900",
         type="article", f=dict(author="Reynolds, Marion R. and Stoumbos, Zachary G.", title="A {CUSUM} Chart for Monitoring a Proportion When Inspecting Continuously", journal="Journal of Quality Technology", year="1999", volume="31", number="1", pages="87--108"),
         doi="10.1080/00224065.1999.11979900", how="Crossref DOI lookup", meta="VERIFIED (Crossref)", form="IV (Ch.3)", used="Eq. 3.15 Bernoulli specialisation", notes=""),
    dict(key="duda2001", apa="Duda, R. O., Hart, P. E., & Stork, D. G. (2001). Pattern classification (2nd ed.). Wiley.",
         type="book", f=dict(author="Duda, Richard O. and Hart, Peter E. and Stork, David G.", title="Pattern Classification", edition="2nd", publisher="Wiley", address="New York", year="2001"),
         doi="", how="Crossref bibliographic match (book reviews)", meta="EXISTS (reviews cite Wiley 2001, 2nd ed., ISBN 0-471-05669-3)", form="Not used for a specific equation in Ch.3", used="Bayes decision rule background (master prompt foundational list)", notes="Not cited in Chapter 3 Table 3.17; include only if cited in text."),
    dict(key="elkan2001", apa="Elkan, C. (2001). The foundations of cost-sensitive learning. In Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence (pp. 973–978). Morgan Kaufmann.",
         type="inproceedings", f=dict(author="Elkan, Charles", title="The Foundations of Cost-Sensitive Learning", booktitle="Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence", publisher="Morgan Kaufmann", year="2001", pages="973--978"),
         doi="", how="OpenAlex search (W167016754)", meta="EXISTS (OpenAlex: title, author, 2001; abstract states the lowest-expected-cost decision rule); IJCAI pages NOT re-confirmed", form="FV (Eq. 1 form, Ch.3)", used="Eqs. 3.6-3.7, 3.9 (expected-cost principle only)", notes="Elkan supports the expected-cost decision principle; it does not define REM's four actions (CLAUDE.md)."),
    dict(key="chow1970", apa="Chow, C. K. (1970). On optimum recognition error and reject tradeoff. IEEE Transactions on Information Theory, 16(1), 41–46. https://doi.org/10.1109/TIT.1970.1054406",
         type="article", f=dict(author="Chow, C. K.", title="On Optimum Recognition Error and Reject Tradeoff", journal="IEEE Transactions on Information Theory", year="1970", volume="16", number="1", pages="41--46"),
         doi="10.1109/TIT.1970.1054406", how="Crossref DOI lookup", meta="VERIFIED (Crossref)", form="IV; conceptual support only", used="Eq. 3.10 (conceptual basis for escalation)", notes="Conceptual support for reject/abstain-style escalation only (CLAUDE.md)."),
    dict(key="naeini2015", apa="Naeini, M. P., Cooper, G., & Hauskrecht, M. (2015). Obtaining well calibrated probabilities using Bayesian binning. Proceedings of the AAAI Conference on Artificial Intelligence, 29(1). https://doi.org/10.1609/aaai.v29i1.9602",
         type="article", f=dict(author="Naeini, Mahdi Pakdaman and Cooper, Gregory and Hauskrecht, Milos", title="Obtaining Well Calibrated Probabilities Using {B}ayesian Binning", journal="Proceedings of the AAAI Conference on Artificial Intelligence", year="2015", volume="29", number="1"),
         doi="10.1609/aaai.v29i1.9602", how="Crossref DOI lookup", meta="VERIFIED (Crossref)", form="FV (Ch.3)", used="Eq. 3.20 ECE binary form", notes=""),
    dict(key="fawcett2006", apa="Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010",
         type="article", f=dict(author="Fawcett, Tom", title="An Introduction to {ROC} Analysis", journal="Pattern Recognition Letters", year="2006", volume="27", number="8", pages="861--874"),
         doi="10.1016/j.patrec.2005.10.010", how="Crossref bibliographic match (exact author/journal/vol/pages)", meta="VERIFIED (Crossref)", form="Metric definition", used="ROC-AUC", notes=""),
    dict(key="davis2006", apa="Davis, J., & Goadrich, M. (2006). The relationship between precision-recall and ROC curves. In Proceedings of the 23rd International Conference on Machine Learning (pp. 233–240). ACM. https://doi.org/10.1145/1143844.1143874",
         type="inproceedings", f=dict(author="Davis, Jesse and Goadrich, Mark", title="The Relationship Between Precision-Recall and {ROC} Curves", booktitle="Proceedings of the 23rd International Conference on Machine Learning", publisher="ACM", year="2006", pages="233--240"),
         doi="10.1145/1143844.1143874", how="Crossref bibliographic match", meta="VERIFIED (Crossref)", form="Metric background", used="PR-AUC (reported as average precision)", notes=""),
    dict(key="efron1979", apa="Efron, B. (1979). Bootstrap methods: Another look at the jackknife. The Annals of Statistics, 7(1), 1–26. https://doi.org/10.1214/aos/1176344552",
         type="article", f=dict(author="Efron, B.", title="Bootstrap Methods: Another Look at the Jackknife", journal="The Annals of Statistics", year="1979", volume="7", number="1", pages="1--26"),
         doi="10.1214/aos/1176344552", how="Crossref DOI lookup", meta="VERIFIED (Crossref)", form="Method background", used="Percentile bootstrap intervals", notes="Grouped resampling is this project's adaptation, not Efron's."),
    dict(key="debenedetti2024", apa="Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents. In Advances in Neural Information Processing Systems 37 (Datasets and Benchmarks Track). https://doi.org/10.52202/079017-2636",
         type="inproceedings", f=dict(author="Debenedetti, Edoardo and Zhang, Jie and Balunovi{\\'c}, Mislav and Beurer-Kellner, Luca and Fischer, Marc and Tram{\\`e}r, Florian", title="{AgentDojo}: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for {LLM} Agents", booktitle="Advances in Neural Information Processing Systems 37", year="2024"),
         doi="10.52202/079017-2636", how="OpenAlex search (DOI record, NeurIPS proceedings)", meta="VERIFIED venue (NeurIPS 2024 proceedings DOI); first three authors and author count 6 confirmed; authors 4-6 from the paper's arXiv listing, not re-checked", form="Benchmark", used="Evaluation environment", notes="Stage 2 master marked the venue unverified; now confirmed via the NeurIPS proceedings DOI. Track label (D&B) not confirmed by the record."),
    dict(key="arp2022", apa="Arp, D., Quiring, E., Pendlebury, F., Warnecke, A., Pierazzi, F., Wressnegger, C., Cavallaro, L., & Rieck, K. (2022). Dos and don'ts of machine learning in computer security. In 31st USENIX Security Symposium (pp. 3971–3988). USENIX Association.",
         type="inproceedings", f=dict(author="Arp, Daniel and Quiring, Erwin and Pendlebury, Feargus and Warnecke, Alexander and Pierazzi, Fabio and Wressnegger, Christian and Cavallaro, Lorenzo and Rieck, Konrad", title="Dos and Don'ts of Machine Learning in Computer Security", booktitle="31st USENIX Security Symposium", publisher="USENIX Association", year="2022", pages="3971--3988"),
         doi="", how="OpenAlex search (arXiv 2010.09470; CACM 2024 version 10.1145/3643456)", meta="EXISTS (arXiv preprint 2020, 8 authors; extended CACM 2024 version); USENIX 2022 venue and pages NOT confirmed this session (USENIX issues no DOIs)", form="Cited for leakage pitfalls", used="Sec. 3.11.6 leakage controls", notes="Authors 4-8 and pages from the standard citation; not re-checked."),
]


def bibtex():
    out = ["% REFERENCES.bib — foundational and method sources for REM (Chapters 3-6).",
           "% Generated by references/build_reference_artifacts.py. Status of each entry:",
           "% see REFERENCE_VERIFICATION_MATRIX.xlsx. Metadata checks are not full-text checks.", ""]
    for r in REFS:
        fields = dict(r["f"])
        if r["doi"]:
            fields["doi"] = r["doi"]
        fields["note"] = "Verification: " + r["meta"].replace("%", "\\%")
        body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items())
        out.append(f"@{r['type']}{{{r['key']},\n{body}\n}}\n")
    return "\n".join(out)


def xlsx(path):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "References"
    head = ["Key", "APA 7 reference", "DOI", "How checked (27 Oct 2026)", "Metadata status", "Formulation vs full text",
            "Used for", "Notes"]
    ws.append(head)
    for r in REFS:
        ws.append([r["key"], r["apa"], r["doi"], r["how"], r["meta"], r["form"], r["used"], r["notes"]])
    for c in ws[1]:
        c.font = Font(bold=True)
    fills = {"VERIFIED": "E3F1E7", "EXISTS": "FFF4D6", "DISCREPANCY": "FBE3E1", "NOT RE": "FBE3E1"}
    for row in ws.iter_rows(min_row=2):
        st = row[4].value or ""
        for k, col in fills.items():
            if st.startswith(k):
                row[4].fill = PatternFill("solid", fgColor=col)
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABCDEFGH", (16, 60, 28, 26, 46, 24, 30, 46)):
        ws.column_dimensions[col].width = w
    ws2 = wb.create_sheet("Legend")
    for line in [
        ["VERIFIED", "DOI registered with Crossref; title, authors, venue, volume/issue/pages match the reference."],
        ["EXISTS", "Work found in an index (OpenAlex/Crossref review records) but some metadata not confirmed by a primary record."],
        ["DISCREPANCY", "Primary record differs from how the thesis cites the work; correction or decision needed."],
        ["NOT RE-CONFIRMED", "Not found in this session's checks; earlier Stage 2 status only."],
        ["Formulation codes", "FV/IV/NC/DER/DEF from Chapter 3 Table 3.17; NOT upgraded by metadata checks."],
        ["Limitation", "api.crossref.org and api.openalex.org were blocked; checks ran through the FastTrack literature connector."],
    ]:
        ws2.append(line)
    wb.save(path)


if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    with open(os.path.join(root, "REFERENCES.bib"), "w", encoding="utf-8") as fh:
        fh.write(bibtex())
    xlsx(os.path.join(root, "REFERENCE_VERIFICATION_MATRIX.xlsx"))
    print(len(REFS), "references written")
