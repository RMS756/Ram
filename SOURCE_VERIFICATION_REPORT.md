# Source Verification Report

Date: 27 Oct 2026.
Scope: foundational and method sources used by Chapter 3, the implementation and the pilot (21 works).
The Chapter 2 literature corpus has its own verification record (`chapter2/CHAPTER2_VERIFICATION_LOG.md`,
`chapter2/CHAPTER2_REFERENCE_EVIDENCE_MATRIX.md`); it was not re-verified here.

Artefacts:
- `REFERENCE_VERIFICATION_MATRIX.xlsx`: one row per source, with the method used and the status.
- `REFERENCES.bib`: APA-convertible BibTeX; every entry carries its verification status in `note`.
- `references/build_reference_artifacts.py`: the single source table that generates both.

## Method and its limits

- Direct requests to `api.crossref.org` and `api.openalex.org` were **refused by the environment's network policy**. Checks therefore ran through the FastTrack literature connector:
  - Crossref DOI and bibliographic lookups (`verify_reference`);
  - OpenAlex search.
- A metadata match establishes that the work exists and that its bibliographic details are correct. It does **not** establish that the cited formula or claim is in the work. The Chapter 3 formulation codes (FV/IV/NC) are carried forward unchanged and were not upgraded.
- No full text was opened in this session.

## Results

| Status | Count | Works |
|---|---|---|
| VERIFIED (Crossref record matches) | 13 | Cox 1958; le Cessie & van Houwelingen 1992; Brier 1950; Page 1954; Lorden 1971; Moustakides 1986; Reynolds & Stoumbos 1999; Chow 1970; Naeini et al. 2015; Fawcett 2006; Davis & Goadrich 2006; Efron 1979; Debenedetti et al. 2024 (venue) |
| EXISTS, some metadata unconfirmed | 6 | Guo et al. 2017; Lundberg & Lee 2017; Elkan 2001; Basseville & Nikiforov 1993; Duda, Hart & Stork 2001; Arp et al. 2022 |
| DISCREPANCY | 1 | Platt |
| NOT RE-CONFIRMED | 1 | Kull et al. 2017 (AISTATS) |

## Findings that need action

1. **Platt.** The thesis cites "Platt (1999), *Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods*". Crossref registers the MIT Press chapter as "Probabilities for SV Machines" (2000), *Advances in Large Margin Classifiers*, pp. 61–74, doi:10.7551/mitpress/1113.003.0008.
   - The 1999 title is the widely circulated version.
   - The thesis must cite one version consistently, with its own title and year.
   - **Decision needed:** cite the 2000 chapter (registered) or the 1999 report (needs a stable source).
2. **Kull et al. (2017).** Two different 2017 works exist:
   - "Beta calibration…" (AISTATS, PMLR 54);
   - "Beyond sigmoids…" (*Electronic Journal of Statistics*, doi:10.1214/17-EJS1338SI, confirmed).

   Chapter 3 cites "Kull et al. (2017)" without disambiguation.
3. **Brier (1950).** The earlier Stage 2 master marked this "Not confirmed". This session's Crossref lookup confirms the record (*Monthly Weather Review* 78(1), 1–3). The Brier-convention question (SC-5) still needs the full text.
4. **AgentDojo (Debenedetti et al., 2024).** The earlier status was "venue unverified". The NeurIPS 2024 proceedings DOI (10.52202/079017-2636) now confirms the venue. The "Datasets and Benchmarks" track label is not shown in the record.
5. **Arp et al. (2022).**
   - The arXiv preprint (2020) and an extended *Communications of the ACM* version (2024, doi:10.1145/3643456) are confirmed.
   - The USENIX Security 2022 venue and pages are not confirmed, because USENIX issues no DOIs.
   - If the thesis cites the USENIX version, it needs checking against usenix.org.
6. **Basseville & Nikiforov (1993).** Only book-review records exist in Crossref; one review describes a 1996 printing. The year 1993 is retained from the standard citation and should be confirmed from the book's copyright page.
7. **Duda, Hart & Stork (2001).** Exists (Wiley, 2nd ed., ISBN 0-471-05669-3, per reviews). It is not cited in Chapter 3 Table 3.17, so it should appear in the reference list only if the text cites it.

## Not claimed

- The bibliography is **not** "fully verified". 13 of 21 works have Crossref-confirmed metadata; none has had its cited formulation re-checked against the full text in this session.
