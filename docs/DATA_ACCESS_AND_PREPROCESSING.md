# Data access and preprocessing

This guide lists the datasets needed to run the PDAC thesis notebooks. The repository includes the analysis code and selected small supporting files, but not the original experimental datasets or the two large modelling tables. Download the original files yourself and check their source-specific usage terms.

## Data sources

| Dataset | Source | Input to locate |
| --- | --- | --- |
| Jaaks/GDSC drug-combination screen | [Coker and Jaaks, original screening data](https://doi.org/10.6084/m9.figshare.16843597) ([Jaaks et al., 2022](https://doi.org/10.1038/s41586-022-04437-2)) | Original screening-response file |
| DepMap expression and cell-line metadata | [DepMap downloads](https://depmap.org/portal/data_page/) | Public 26Q1 expression data and `Model.csv` |
| DrugComb annotations | [DrugComb dataset](https://researchportal.helsinki.fi/en/datasets/drugcomb/) / [identifier archive](https://zenodo.org/records/18449193) | Drug-identifier/annotation workbook |
| NCATS/PANC-1 | [NCATS/PANC1](https://github.com/ncats/PANC1) | `datasets/Training_set.csv` |
| Yale / Langdon | [Langdon et al., 2017](https://doi.org/10.1158/1535-7163.MCT-16-0794) | `Raw_YALE-PDAC.zip` |
| Höfer | [Höfer et al., 2025](https://doi.org/10.1038/s44320-025-00085-6) | `hoefer_2025_Dataset_EV2.xlsx` |
| Vis | [Vis et al., 2024](https://doi.org/10.1016/j.xcrm.2024.101687) | `pancan_combi_fitted_data_jan21.tsv.gz` (from Data S1) |
| Bashi | [Bashi et al., 2024](https://doi.org/10.1158/2159-8290.CD-23-0388) | `cd-23-0388_table_s18_suppst18.xlsx` |

Save the raw files locally under `data/raw/`. Follow the input-discovery or configuration cells for accepted filenames, subdirectories and any required source-specific sheets. Preserve the exact source versions and compound mappings used for a reproducible run; do not substitute unrelated files merely to match the expected counts.

## Preparing the modelling inputs

Run [`multi_cell_line_dataset.ipynb`](../notebooks/multi_cell_line_dataset.ipynb) with the Jaaks/GDSC, DepMap and DrugComb inputs. It performs concentration-level assembly followed by canonical drug-pair aggregation, and generates two downstream files:

```text
tables/pdac_multicell_drug_pair_units_with_morgan.csv
tables/depmap_pdac_full_expression_for_fold_pca.csv
```

These files are saved locally and excluded from Git. The first is needed for grouped validation, candidate ranking and external model training; the second is needed for training-fold expression PCA in grouped validation. The repository already includes `tables/candidate_pair_secondary_support.csv` for post-hoc ranking support.

For external evaluation, run [`external_pdac_dataset_harmonisation.ipynb`](../notebooks/external_pdac_dataset_harmonisation.ipynb) with the Yale, Höfer, Vis and Bashi source files, then [`external_experimental_validation.ipynb`](../notebooks/external_experimental_validation.ipynb) with those outputs, NCATS/PANC-1 and the canonical modelling table. Check its `TRAINING_UNITS_PATH` setting and structure-file paths; the repository includes `data/processed/external_validation/external_approved_smiles.csv`, but additional original structure sources may be needed.

## Processing rules and expected checks

The assembly harmonises PDAC cell-line and compound identifiers, represents drug pairs without regard to order, and treats the original `Synergy` field as Boolean rather than applying a new numerical threshold. At the canonical cell-line–pair level, `any_positive_label` means at least one positive measurement, while `majority_label` requires more than 50% positive measurements (ties are negative). Molecular features include 512-bit Morgan fingerprints per drug and order-invariant pair representations.

For unseen-cell-line validation, expression preprocessing and PCA must be fitted on the training cell lines only; the assembly's descriptive global PCs must not replace this fold-specific processing.

| Check from the recorded thesis analysis | Expected |
| --- | ---: |
| Concentration-level observations / positive labels | 53,441 / 2,483 |
| Canonical cell-line–pair units | 8,450 |
| PDAC cell lines / unordered pairs | 26 / 325 |
| Any-positive / strict majority-positive units | 1,063 / 188 |
| Mixed-label units / exact-half units | 999 / 206 |
| Full-expression input | 26 cell lines × 19,215 gene features (plus `ModelID`) |
| Morgan fingerprint length | 512 bits per drug |

These are verification targets, not guarantees that different source releases will reproduce the same values. The notebooks contain the detailed transformations and assertions.

## Data availability and usage

The original datasets, generated `results/`, assembly intermediates and the two large modelling tables are excluded from the current repository by `.gitignore`. Check the actual terms of each source before redistributing any original or derived data; public access does not automatically grant unrestricted rehosting rights. See also the [Sanger data-usage policy](https://depmap.sanger.ac.uk/documentation/data-usage-policy/).

Exact reproduction also depends on matching the original source releases, cell-line/drug identifier mappings and verified chemical structures. Preserve this provenance locally when rerunning the notebooks.
