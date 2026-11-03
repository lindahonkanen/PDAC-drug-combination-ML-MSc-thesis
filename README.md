# Machine learning for drug-combination modelling in pancreatic ductal adenocarcinoma

**Master's thesis (2026) · University of Helsinki · Life Science Informatics**

This repository contains the Python notebooks for my master's thesis on machine-learning prediction and prioritisation of drug combinations in pancreatic ductal adenocarcinoma (PDAC). The analyses cover a single-cell-line benchmark, multi-cell-line modelling, candidate ranking and evaluation against external experimental datasets.

## Setup

The analyses were developed using Python 3.14.3 on Windows 11 (CPU). The required Python packages and their versions are listed in requirements.txt.

Install the dependencies in your preferred Python environment and open the notebooks in Jupyter or VS Code. Check the input paths in each notebook before running.

## Notebooks

Run each notebook from top to bottom. The order below follows the analysis workflow; the NCATS benchmark can also be run independently.

| Order | Notebook | Purpose |
|---|---|---|
| 1 | [NCATS/PANC-1 benchmark](notebooks/NCATS_PANC1_single_cell_line_benchmark.ipynb) | Compare models and drug features under one-compound-out validation. |
| 2 | [Multi-cell-line dataset assembly](notebooks/multi_cell_line_dataset.ipynb) | Combine Jaaks/GDSC, DepMap and DrugComb data into modelling tables. |
| 3 | [Grouped multi-cell-line validation](notebooks/multi_cell_line_grouped_validation.ipynb) | Compare classical and neural models under grouped and cold-drug validation. |
| 4 | [Drug-pair candidate ranking](notebooks/drug_pair_candidate_ranking.ipynb) | Rank drug pairs using out-of-fold model predictions. |
| 5 | [External dataset harmonisation](notebooks/external_pdac_dataset_harmonisation.ipynb) | Prepare the Yale, Höfer, Vis and Bashi response datasets. |
| 6 | [External experimental validation](notebooks/external_experimental_validation.ipynb) | Evaluate separately fitted fingerprint-only models on external data, including NCATS/PANC-1. |

**Dependencies:** Notebooks 3 and 4 require the tables produced by notebook 2. Notebook 6 requires the outputs of notebook 5, the canonical modelling table and the relevant external inputs. Results and figures are saved locally; generated files are generally excluded from Git.

## Data and supporting files

**Original experimental datasets and large processed modelling tables are not included** in this repository and are not downloaded automatically. Follow the [data-access and preprocessing guide](docs/DATA_ACCESS_AND_PREPROCESSING.md) to obtain the required source files and check their usage terms. Reproducing the reported results requires the corresponding data releases and mappings.

Notebook 2 generates these local modelling inputs:

```text
tables/pdac_multicell_drug_pair_units_with_morgan.csv
tables/depmap_pdac_full_expression_for_fold_pca.csv
```

Two small supporting files are included in GitHub:

- [`tables/candidate_pair_secondary_support.csv`](tables/candidate_pair_secondary_support.csv) — additional drug-pair measurements used for post-hoc interpretation of the candidate ranking.
- [`data/processed/external_validation/external_approved_smiles.csv`](data/processed/external_validation/external_approved_smiles.csv) — approved molecular-structure mappings used in external validation.

The thesis provides the full methodology, results and discussion. The notebooks contain the executable analyses and their checks.
