### Machine learning for drug-combination modelling in pancreatic ductal adenocarcinoma (2026) official repository

This is the corresponding repository to my Master's thesis from University of Helsinki, titled _Machine learning for drug-combination modelling in pancreatic ductal adenocarcinoma_ (2026). You may access my thesis from the University of Helsinki Library.

- Inside the **notebooks** file, there are Jupyter notebooks containing all the algorithms used for the thesis analyses, including single-cell-line benchmarking, multi-cell-line modelling, drug combination prioritisation and testing the models on external experimental evidence.

## Analysis notebooks

| Stage | Notebook | Analysis |
|---|---|---|
| 1 | [NCATS/PANC-1 benchmark](notebooks/NCATS_PANC1_single_cell_line_benchmark.ipynb) | Published model reproduction and feature comparisons |
| 2 | [Dataset assembly](notebooks/multi_cell_line_dataset.ipynb) | Jaaks/GDSC–DepMap integration and feature construction |
| 3 | [Multi-cell-line modelling](notebooks/multi_cell_line_grouped_validation.ipynb) | Grouped validation, model comparisons and cold-drug testing |
| 4 | [Candidate prioritisation](notebooks/drug_pair_candidate_ranking.ipynb) | Three-model consensus, ranking and quantitative support |
| 5 | [External data harmonisation](notebooks/external_pdac_dataset_harmonisation.ipynb) | Preparation of independent experimental datasets |
| 6 | [External validation](notebooks/external_experimental_validation.ipynb) | Prediction transfer and chemical generalisation |

- The **tables/** directory contains the published derived candidate-support table. Larger source-derived modelling inputs are kept locally and are not redistributed in this repository.

### Required local input files

The notebooks use local data paths relative to the repository root.
The following files are required for the corresponding analyses:

| Notebook | Required local input |
|---|---|
| `NCATS_PANC1_single_cell_line_benchmark.ipynb` | `data/raw/NCATS_PANC1/Training_set.csv` |
| `multi_cell_line_grouped_validation.ipynb` | `tables/pdac_multicell_drug_pair_units_with_morgan.csv` |
| `multi_cell_line_grouped_validation.ipynb` | `tables/depmap_pdac_full_expression_for_fold_pca.csv` |

The PANC-1 training set is available in the original
[NCATS/PANC1 repository](https://github.com/ncats/PANC1)
under `datasets/Training_set.csv` (Pourmousa et al., 2025).

The multi-cell-line inputs are derived from the Jaaks/GDSC
drug-combination screen and DepMap Public 26Q1 expression data.
The required canonical unit table contains 8,450 observations
from 26 cell lines and 325 drug pairs. The expression table
contains the corresponding 26 PDAC cell lines and 19,215
gene-expression features (19,216 CSV columns including ModelID).

These two larger datasets are intentionally excluded from
public Git tracking. Their preparation requires the
data-assembly and feature-construction workflow; downloading
the raw source files alone is not sufficient.

For source access, licence caveats, documented preprocessing
steps, expected validation counts and remaining provenance
gaps, see [Data access and preprocessing](docs/DATA_ACCESS_AND_PREPROCESSING.md).
The two-stage assembly workflow is provided in
`notebooks/multi_cell_line_dataset.ipynb`. Original source
datasets must still be downloaded and supplied locally.

Files under `data/raw/` and the two specified modelling CSVs
are listed in `.gitignore`. They must be supplied locally
before executing the relevant notebooks.

### Multi-cell-line dataset assembly

The notebook `notebooks/multi_cell_line_dataset.ipynb`
reconstructs the Jaaks/GDSC--DepMap dataset, aggregates the
8,450 canonical modelling units and generates Morgan fingerprints.
It also exports the two local CSV inputs required by the
multi-cell-line modelling notebooks. Original source files
remain excluded from GitHub.

### External experimental validation

External validation was performed using five published
drug-combination datasets: Yale, NCATS/PANC-1, Höfer,
Vis and Bashi.

The analysis is organised into two notebooks:

- `notebooks/external_pdac_dataset_harmonisation.ipynb`
  prepares and harmonises the external experimental
  responses and drug-pair identifiers.

- `notebooks/external_experimental_validation.ipynb`
  evaluates the three-model fingerprint-only panel
  using HistGradientBoosting, LightGBM and CatBoost.

The final experimental registry contains 1,619 pairs,
of which 1,539 (95.1%) could be scored using verified
molecular fingerprints.

The file
`data/processed/external_validation/external_approved_smiles.csv`
contains two additional literature-supported chemical
structures, GSK650394A and AZ3202.

Pairs involving CREBi1, oligomycin or DITC were
excluded from scoring because their exact screened
molecular structures could not be verified sufficiently.

The notebooks use additional published source data and
locally prepared analysis inputs. Original data sources
and local input paths are documented in the notebooks.

### Data sources and licensing

The analysis uses experimental drug-combination
measurements from Jaaks et al. (2022), molecular
data from DepMap/CCLE, and pharmacological
annotations from DrugComb.

The original Jaaks and Coker screening data are
available at:
https://doi.org/10.6084/m9.figshare.16843597

The dataset is marked CC BY 4.0 by Figshare.
Derived tables should be attributed to the
original data creators.

DepMap expression data were obtained from
DepMap Public 26Q1:
https://depmap.org/portal/data_page/

The redistribution rights for newer DepMap
releases differ from those of older CC BY 4.0
Figshare releases. Users should obtain the
required source data directly from DepMap
and comply with the applicable terms.

The analysis code and derived model results
are provided separately from source datasets.
The licences of third-party datasets are not
superseded by the licence of this repository.

Exact sources used from other studies (accessed October 2026):

- Langdon et al. (2017), doi: 10.1158/1535-7163.MCT-16-0794 — Yale	Raw_YALE-PDAC.zip	Internal Pancreas_study_summary.csv, particularly observed_bliss_diff. The separate raw-signal CSV is not needed for the harmonised outcome.
- Höfer et al. (2025), doi: 10.1038/s44320-025-00085-6	hoefer_2025_Dataset_EV2.xlsx	Sheet Dataset EV2_146Drugs_Synergy; supplied Synergy labels and AUC∆_sum [%]. HPDE is excluded.
- Vis et al. (2024), doi: 10.1016/j.xcrm.2024.101687	pancan_combi_fitted_data_jan21.tsv.gz from publication Data S1	Pancreatic rows and continuous SYNERGY_DELTA_EMAX. No binary labels are constructed.
- Bashi et al. (2024), doi: 10.1158/2159-8290.CD-23-0388	cd-23-0388_table_s18_suppst18.xlsx	Sheet Supplementary Table 18 Single; combo_MaxE, HSA_matrix and drug/cell-line identities. The notebook constructs the original analysis's binary response rule.

## Computational environment

The Python dependencies and their recorded versions are listed in
[requirements.txt](requirements.txt).

The Python version, operating system, installation instructions,
package versions and reproducibility considerations are documented
in [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md).

The environment specification was generated from the author's
thesis-analysis Python environment. Package imports were verified,
but this does not constitute a complete fresh-environment rerun
of every notebook.

Original experimental and molecular datasets are not redistributed.
See [Data access and preprocessing](docs/DATA_ACCESS_AND_PREPROCESSING.md)
for source access and preprocessing instructions.

