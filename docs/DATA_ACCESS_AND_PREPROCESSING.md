# Data access, licences and preprocessing

**Scope:** Jaaks/GDSC drug-combination screening, DepMap Public 26Q1 expression, and associated DrugComb pharmacological annotations used in the MSc thesis *Machine learning for drug-combination modelling in pancreatic ductal adenocarcinoma* (2026).

**Last reviewed:** 26 October 2026. **Status:** Source access and the documented processing/validation contract are provided below. This is **not** an independently executable, byte-for-byte reconstruction of the author's original data-assembly pipeline. Exact source-file versions, join rules and the original name/SMILES mapping files must be preserved or recovered from that pipeline before claiming full computational reproducibility. Licences must be checked against the actual files downloaded.

## 1. Why the large processed CSVs are not distributed here

The public repository contains code, documentation, and the small attributed `tables/candidate_pair_secondary_support.csv` summary; it does **not** distribute:

- `tables/pdac_multicell_drug_pair_units_with_morgan.csv` — integrated Jaaks/GDSC–DepMap/DrugComb modelling table (8,450 units);
- `tables/depmap_pdac_full_expression_for_fold_pca.csv` — a 26-cell-line subset of DepMap Public 26Q1 expression (19,216 harmonised gene columns).

These files are expected to be supplied **locally**. They are expressly ignored in `.gitignore`. The raw downloads in `data/raw/` and generated outputs in `results/` are also ignored. No repository licence conveys a right to redistribute third-party source datasets.

This is a conservative distribution policy, **not** a claim that academic use or all redistribution is forbidden. Deleting tracked files from the current branch does **not** remove their copies from earlier Git commits. See §6.

## 2. Original source access and licence checks

| Material | Authoritative source | Status and action |
| --- | --- | --- |
| Jaaks/Coker original drug-combination screen | [Original screen drug combination data (Figshare)](https://figshare.com/articles/dataset/Original_screen_drug_combination_data/16843597); DOI [10.6084/m9.figshare.16843597](https://doi.org/10.6084/m9.figshare.16843597). See [Jaaks et al., *Nature* (2022)](https://doi.org/10.1038/s41586-022-04437-2). | The Figshare record displays **CC BY 4.0**, while its description also specifies a non-transferable research/educational-use grant and excludes resale/significant-part resale and commercial services. Read and preserve both statements; do not infer that all related Sanger files have identical terms. Credit the original authors. |
| Sanger GDSC combination documentation / data | [GDSC Combinations](https://gdsc-combinations.depmap.sanger.ac.uk/), [Sanger data-usage policy](https://depmap.sanger.ac.uk/documentation/data-usage-policy/) | Consult the original source and policy for each screen or derivative. The research-use policy limits certain commercial activity. A public download link by itself is not a universal redistribution licence. |
| Broad DepMap/CCLE gene expression and model metadata | [DepMap Downloads](https://depmap.org/portal/data_page/) — choose **DepMap Public 26Q1** and its expression/model-metadata files. | Record the **exact downloaded filenames**, 26Q1 release, download date and file-specific “Data Usage / Terms and conditions” before processing. Older DepMap datasets were generally described as CC BY 4.0; DepMap staff [described changed terms for newly generated data in July 2026](https://forum.depmap.org/t/provide-an-open-endpoint-for-latest-version-retrieval/4652). Precise public rehosting permission for the 26Q1 expression file has **not** been established, so do not republish it here without confirmation. |
| DrugComb compound/target annotations, when applicable | [University of Helsinki DrugComb portal/dataset entry](https://researchportal.helsinki.fi/en/datasets/drugcomb/); [DrugComb raw data and identifier archive](https://zenodo.org/records/18449193) | Record which actual version/files supplied the target/pathway/drug-type fields, cite DrugComb, and inspect that archive's **specific** licence before redistributing source-derived annotation columns. These links do not establish the provenance of each column in the canonical table. |

**Keep a local, non-committed provenance record** for each original download:

`source_name | release | filename | origin URL or DOI | accessed_on | SHA-256 | source licence/terms URL | preprocessing script/commit`

Useful local hash command (PowerShell): `Get-FileHash -Algorithm SHA256 "path/to/source-file.csv"`.

## 3. Required local layout

From the repository root:

```text
data/
  raw/                                      # Original downloaded files (ignored)
    ...                                     # Preserve original source filenames/version
  processed/
    external_validation/
      external_approved_smiles.csv           # Small approved mapping already in GitHub
tables/
  candidate_pair_secondary_support.csv     # Small derived summary in GitHub
  pdac_multicell_drug_pair_units_with_morgan.csv  # LOCAL ONLY
  depmap_pdac_full_expression_for_fold_pca.csv    # LOCAL ONLY
notebooks/
  multi_cell_line_grouped_validation.ipynb
  drug_pair_candidate_ranking.ipynb
  external_pdac_dataset_harmonisation.ipynb
  external_experimental_validation.ipynb
```

`notebooks/multi_cell_line_grouped_validation.ipynb` uses both local CSVs. `notebooks/drug_pair_candidate_ranking.ipynb` uses the canonical unit table and the published secondary-support table. The external validation notebook may additionally require the locally prepared harmonisation contract, study-specific source tables, source-backed SMILES files, and its own canonical-training path setting; see its configuration cell. This document does not claim that a fresh clone already contains those additional local inputs.

## 4. Documented preprocessing specification

The steps below describe **the transformations reported in thesis Methods §§2.3.1–2.3.3 and checked by the released notebooks**. They are a specification for comparing a reconstruction with the original analysis. **Do not invent missing source filters or identifiers to force a match.**

### 4.1 Obtain and harmonise the screening data

1. Download the original Jaaks/Coker screen from its source, retaining the original file(s), schema, provenance and permitted-use terms. This is the **original anchor drug-combination screen**, not a substitute response table from a different GDSC release.
2. Use the original analysis's pancreatic-cancer cell-line selection and source-to-DepMap `ModelID` crosswalk. Retain only observations with corresponding DepMap expression data.
3. Apply the original drug-name/compound identifier normalisation and construct an **unordered** pair identifier for drugs A and B, invariant to their original order. Preserve the mapping file, ambiguity rules and exclusion log.
4. Interpret the original `Synergy` field as **Boolean**, with `True → 1` and `False → 0`. Do **not** invent a new continuous-score synergy threshold.
5. Validate the assembled, filtered concentration-level dataset against the original analysis: **53,441 observations**, **26** PDAC cell lines, **26** distinct individual drugs and **325** unordered pairs, with **2,483** positive concentration-level labels. These are target audit counts, **not** substitute instructions for obtaining the original rows.

The exact source file variant, full cell-line identifiers, source-to-`ModelID` crosswalk, excluded rows, drug alias dictionary and intermediate join keys are **not supplied by this public repository**. Those are outstanding inputs from the original data-assembly notebooks/code.

### 4.2 Aggregate to the canonical modelling unit

Group the retained concentration-level measurements by (`ModelID`, canonical unordered drug pair). For each group, compute:

- `n_rows`: number of concentration-level observations;
- `positive_fraction`: mean of the original binary `Synergy` labels;
- `any_positive_label = int(positive_fraction > 0)`;
- `majority_label = int(positive_fraction > 0.5)`, **strict**, with ties at 0.5 negative;
- the applicable secondary numerical response summaries, including mean `ΔfAUC`, using only the original valid source measurements and the original aggregation conventions.

**Expected unit-table audits:** 8,450 unique (`ModelID`, pair) rows = 26 cell lines × 325 pairs; each pair appears in all 26 lines; **1,063** any-positive and **188** majority-positive units; **999** units have mixed original binary labels; **206** units have `positive_fraction == 0.5`. Confirm those counts before fitting models. Do not remove mixed-label or tied units.

### 4.3 Pharmacological features and molecular fingerprints

- Use the originally harmonised compound SMILES and independently sourced target/pathway/drug-type/DrugComb annotations. Check their column-level provenance and licence.
- Reproduce the recorded **512-bit Morgan fingerprint per drug** with RDKit and the original pipeline's fingerprint settings. The external-validation notebook uses radius 2, 512 bits and no chirality; confirm that the input-assembly notebook used the same options before declaring an exact bitwise match.
- The original canonical table stores drug A and B fingerprint bits as columns resembling `drug_a_fp_0000` … `drug_a_fp_0511` and `drug_b_fp_0000` … `drug_b_fp_0511` (1024 stored raw drug-bit columns).
- For the **order-invariant prediction representation**, calculate `(fpA + fpB)/2` and `abs(fpA - fpB)`, a total of **1,024 symmetric columns**. The wider unit table also contains response summaries, identifiers, annotations and expression PCs; do not assume its shape is just 1,024 columns.
- Avoid fingerprinting a guessed salt, stereoisomer or differently named compound when the original chemical identity cannot be established.

### 4.4 Prepare the DepMap 26Q1 PDAC expression input

1. Download the **matching Public 26Q1** expression and cell-model metadata directly from DepMap; save filenames, checksums and terms.
2. Join using the **same 26 exact `ModelID` values** retained in the canonical screening table. Use the original default/representative-profile selection when multiple profiles exist.
3. Harmonise the original gene feature names; collapse duplicate gene columns and duplicate `ModelID` rows by averaging, as reported in the thesis.
4. Validate a matrix with **26 distinct `ModelID` rows × 19,216 gene-expression columns**, excluding identifier/metadata columns. Save locally to `tables/depmap_pdac_full_expression_for_fold_pca.csv`.
5. Do **not** globally fit expression PCA before an **unseen-cell-line** evaluation. That notebook fits training-only expression preprocessing (training-based gene filtering and scaling, then up to 20 PCs). Its training SD threshold is **0.05**, with unused component slots zero-padded where needed. For unseen-*drug-pair* analyses, the separately stored 20-component expression-PCA scores are used because all cell lines are represented in training.

The public notebook validates the expression shape and column consistency; it does **not** generate the whole expression file from the raw DepMap download.

### 4.5 Assemble the final local unit-table input

Join the canonical per-cell-line/pair labels with the original pharmacological annotations, drug fingerprints and expression-derived features, using the **same original mappings and data-preparation code**. Save the local merged CSV as:

`tables/pdac_multicell_drug_pair_units_with_morgan.csv`

At minimum, the published multi-cell-line and ranking notebooks expect `ModelID`, `drug_a_norm`, `drug_b_norm`, `positive_fraction`, correctly labelled symmetric/model features and the original fingerprint/PCA fields. Other required feature columns are defined and validated in the corresponding notebooks.

The screening aggregation counts above are necessary checks but **are not a sufficient substitute** for faithfully reconstructing the feature table. In particular, any guessed drug aliases, PDAC line exclusions, SMILES structures, DrugComb joins or PCA feature values could change predictions.

## 5. Validation before model execution

From the repository root, with the local two CSVs installed:

```powershell
Test-Path "tables/pdac_multicell_drug_pair_units_with_morgan.csv"
Test-Path "tables/depmap_pdac_full_expression_for_fold_pca.csv"
Get-FileHash -Algorithm SHA256 "tables/pdac_multicell_drug_pair_units_with_morgan.csv"
Get-FileHash -Algorithm SHA256 "tables/depmap_pdac_full_expression_for_fold_pca.csv"
git check-ignore -v -- "tables/pdac_multicell_drug_pair_units_with_morgan.csv"
git check-ignore -v -- "tables/depmap_pdac_full_expression_for_fold_pca.csv"
```

Then run the input-validation portions of the notebooks. Expected audits include:

| Check | Expected |
| --- | ---: |
| Concentration-level observations | 53,441 |
| Positive concentration-level observations | 2,483 |
| Unique canonical units | 8,450 |
| Distinct `ModelID` | 26 |
| Distinct canonical unordered drug pairs | 325 |
| Distinct drugs | 26 |
| Any-positive units | 1,063 |
| Strict majority-positive units | 188 |
| DepMap expression matrix | 26 × 19,216 genes |
| Morgan bits per drug | 512 |

These numbers come from the original thesis analysis. They are **audit targets**, not assurances that a newly downloaded source will match without the author's exact upstream source versions and processing.

## 6. Git history and compliance boundary

The two large tables were removed from **current `main`**, but GitHub commit history still contains earlier blobs. A normal `git rm` or `.gitignore` does **not** erase historical copies.

1. **First obtain authoritative, file-specific permission/terms** for the exact DepMap Public 26Q1 expression download and any restricted annotations embedded in the old canonical file. The July 2026 DepMap clarification restricts commercial use, but does **not by itself prove** that non-profit academic redistribution is forbidden.
2. If the actual terms forbid public rehosting, remove the corresponding blobs from repository history with a **coordinated, backed-up history rewrite**, or obtain clearance from the provider. Do not force-push simply to tidy history: it replaces commit SHAs, affects clones, and may require GitHub support to address retained server-side objects or caches.
3. Check forks, releases, archived artefacts and any other copies separately; rewriting one branch is not a universal recall of files.
4. Retain written permission decisions and a record of what was removed, by whom and when.

**Current status:** conservative current-branch sharing and data-access documentation are in place. This file is not legal clearance and does not claim that historical distribution has been resolved.

## 7. What remains to reach exact computational reproducibility

This repository currently lacks the complete public data-assembly pipeline. To convert this protocol into a fully executable recipe, add or link to the actual original preparation scripts/notebooks, plus:

- exact source release/file names and SHA-256 values;
- 26 `ModelID` values and source cell-line crosswalk;
- drug-name aliases and verified SMILES mapping;
- source exclusions, duplicate-handling, field selection and drug-target/DrugComb joins;
- the full versioned commands to generate both local CSVs;
- final source-to-derived provenance, and hashes of the validated outputs.

**Do not claim that this README/document recreates the exact modelling tables until those files and rules are provided.**

## Primary references

- Jaaks et al. (2022), *Effective drug combinations in breast, colon and pancreatic cancer cells*, *Nature*, https://doi.org/10.1038/s41586-022-04437-2.
- Coker and Jaaks, *Original screen drug combination data*, https://doi.org/10.6084/m9.figshare.16843597.
- Sanger, *Data Usage Policy*, https://depmap.sanger.ac.uk/documentation/data-usage-policy/.
- DepMap, Broad, *DepMap Public 26Q1*; downloads and citing instructions: https://depmap.org/portal/data_page/.
- DepMap licensing discussion (older data): https://forum.depmap.org/t/license-for-data-found-in-the-depmap-portal/130.
- DepMap updated-terms clarification (July 2026): https://forum.depmap.org/t/provide-an-open-endpoint-for-latest-version-retrieval/4652.
- DrugComb, dataset/source listings: https://researchportal.helsinki.fi/en/datasets/drugcomb/.
