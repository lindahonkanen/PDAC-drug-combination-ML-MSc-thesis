# Machine learning for drug-combination modelling in pancreatic ductal adenocarcinoma

**Master's thesis (2026) · University of Helsinki · Life Science Informatics**

This repository contains the Python analysis notebooks and selected shareable supporting files for the master's thesis *Machine learning for drug-combination modelling in pancreatic ductal adenocarcinoma*. The thesis investigates whether machine-learning models can predict drug-combination synergy in pancreatic ductal adenocarcinoma (PDAC), how predictions change under different validation designs, and whether candidate rankings agree with external experimental evidence.

The principal analyses are:

1. Reproduce and extend the published NCATS/PANC-1 single-cell-line benchmark using drug identity, mechanism-of-action, activity and molecular fingerprint features.
2. Assemble Jaaks/GDSC drug-combination responses with DepMap expression and pharmacological information, then compare classical and neural models using **unseen-cell-line**, **unseen-drug-pair** and **identity-free cold-drug** validation.
3. Rank combinations using a three-model, two-endpoint out-of-fold consensus, with separate post-hoc pharmacological support.
4. Evaluate transfer to five experimental sources (Yale, NCATS/PANC-1, Höfer, Vis and Bashi), distinguishing same-pair, one-cold-drug and both-cold-drug comparisons.

**Scope:** This is a documented research workflow, not a plug-and-play release of all experimental datasets. Restricted/source-derived modelling inputs and original external datasets are **not** distributed. The README explains how to obtain and place inputs and what the published notebooks verify; exact reproduction also depends on matching the original source versions and mappings.

## Repository structure

```text
.
├── README.md
├── .gitignore
├── requirements.txt
├── docs/
│   ├── DATA_ACCESS_AND_PREPROCESSING.md
│   └── ENVIRONMENT.md
├── notebooks/
│   ├── NCATS_PANC1_single_cell_line_benchmark.ipynb
│   ├── multi_cell_line_dataset.ipynb
│   ├── multi_cell_line_grouped_validation.ipynb
│   ├── drug_pair_candidate_ranking.ipynb
│   ├── external_pdac_dataset_harmonisation.ipynb
│   └── external_experimental_validation.ipynb
├── scripts/
│   └── capture_thesis_environment.py
├── tables/
│   └── candidate_pair_secondary_support.csv
└── data/processed/external_validation/
    └── external_approved_smiles.csv
```

The notebooks are published with selected saved execution results. Generated local files under `results/`, original files under `data/raw/` and the restricted modelling tables are deliberately excluded from this repository. Do not commit private or restricted data when following these instructions.

## Installation

The documented analysis environment is **Python 3.14.3 on Windows 11**, with a CPU-based PyTorch installation at the time of environment capture. See [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) for the full recorded versions and limitations. [`requirements.txt`](requirements.txt) pins the installed direct notebook dependencies (including RDKit, scikit-learn, PyTorch, LightGBM, CatBoost and XGBoost); it is not a complete transitive lockfile or evidence of a clean-room rerun.

From **Windows PowerShell**:

```powershell
git clone https://github.com/lindahonkanen/PDAC-drug-combination-ML-MSc-thesis.git
Set-Location .\PDAC-drug-combination-ML-MSc-thesis
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
python -m ipykernel install --user --name pdac-thesis --display-name "PDAC thesis"
jupyter lab
```

Open notebooks from within this repository and select the **PDAC thesis** kernel. Most notebooks locate the repository root from the current working directory; if you launch a notebook elsewhere, configure its project-root override where provided. Do not run from an unrelated directory. On macOS/Linux, use a compatible Python interpreter, `python -m venv .venv` and `source .venv/bin/activate` instead of the Windows activation command. RDKit and PyTorch wheel availability may differ by platform; use the instructions in [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) if installation requires adaptation.

## Obtain the required inputs

**The repository does not download source files automatically.** Obtain them from the cited original providers, check their terms and preserve their exact filenames and provenance. Details, known licensing caveats and reconstruction limitations are in [Data access and preprocessing](docs/DATA_ACCESS_AND_PREPROCESSING.md).

### A. NCATS/PANC-1 benchmark

Download `datasets/Training_set.csv` from the [original NCATS/PANC1 repository](https://github.com/ncats/PANC1) and place it at:

```text
data/raw/NCATS_PANC1/Training_set.csv
```

The expected benchmark contains **496 combinations from 32 compounds**, with **256 positive labels**.

### B. Jaaks/GDSC–DepMap dataset assembly

The assembly notebook expects source files under these directories (filenames listed are examples explicitly searched by its configuration cell):

| Local directory | Required source and accepted example |
| --- | --- |
| `data/raw/Jaaks_GDSC_combinations/` | Original Jaaks/GDSC combination response, e.g. `original_screen_drug_combination_data.csv` |
| `data/raw/DepMap/` | DepMap model metadata, e.g. `Model.csv`, and **Public 26Q1** expression, e.g. `OmicsExpressionTPMLogp1HumanProteinCodingGenes.csv` |
| `data/raw/DrugComb/` | Drug identifier/annotation workbook, e.g. `DrugComb_drug_identifiers.xlsx` (sheet `drug`) |

**Do not substitute unrelated datasets merely to match the expected counts.** The original source releases, cell-line crosswalk and drug identity mappings affect the reconstructed outputs. The assembly notebook performs two stages (concentration-level harmonisation followed by canonical-unit aggregation) and, when its assertions pass, writes the following **local-only** files:

```text
tables/pdac_multicell_drug_pair_units_with_morgan.csv
tables/depmap_pdac_full_expression_for_fold_pca.csv
```

These are required by the multi-cell-line modelling notebook; the first is also required for candidate ranking. The assembly's frozen audit targets include **53,441 concentration-level rows**, **2,483 positive source rows**, **8,450 units** (26 PDAC cell lines × 325 unordered pairs), **1,063 any-positive units**, **188 strict majority-positive units**, **999 mixed-label units** and **206 exact-half units**. The original source files and completed local audit are needed to independently verify every upstream count.

### C. External experimental validation

Download the original study data manually and edit the path variables in the **first configuration cell** of [`external_pdac_dataset_harmonisation.ipynb`](notebooks/external_pdac_dataset_harmonisation.ipynb) if your saved locations differ:

| Source | Input expected by the notebook | Reference |
| --- | --- | --- |
| Yale / Langdon | `data/raw/external_validation/yale_pdac/Raw_YALE-PDAC.zip` (member `Pancreas_study_summary.csv`) | [Langdon et al. (2017)](https://doi.org/10.1158/1535-7163.MCT-16-0794) |
| Höfer | `data/raw/external_validation/hoefer_2025/hoefer_2025_Dataset_EV2.xlsx` (sheet `Dataset EV2_146Drugs_Synergy`) | [Höfer et al. (2025)](https://doi.org/10.1038/s44320-025-00085-6) |
| Vis | The `pancan_combi_fitted_data_jan21.tsv.gz` fitted-response file inside Data S1; set `VIS_TSV_PATH` to its actual location | [Vis et al. (2024)](https://doi.org/10.1016/j.xcrm.2024.101687) |
| Bashi | `data/raw/Bashi_2024/cd-23-0388_table_s18_suppst18.xlsx` (sheet `Supplementary Table 18 Single`) | [Bashi et al. (2024)](https://doi.org/10.1158/2159-8290.CD-23-0388) |
| NCATS/PANC-1 | The same `Training_set.csv` used by the PANC-1 benchmark | [NCATS/PANC1](https://github.com/ncats/PANC1) |

**Keep downloaded Vis and other external files out of Git.** The example Vis input location is under `data/external/`, which is already excluded by `.gitignore`. Alternatively, store the file under the ignored `data/raw/` directory and update `VIS_TSV_PATH` accordingly.

The harmonisation notebook writes an **external source contract** to `results/tables/ml_comprehensive/external_dataset_harmonisation/external_source_harmonisation_contract.csv` and the four source-specific pair tables under `results/tables/ml_comprehensive/`.

**Important input setting for the final validation notebook:** `external_experimental_validation.ipynb` defaults `TRAINING_UNITS_PATH = None` to a historical local file under `data/processed/final_github/`, **not** to the table produced by the assembly notebook. Set this value explicitly in its first configuration cell, for example:

```python
TRAINING_UNITS_PATH = "tables/pdac_multicell_drug_pair_units_with_morgan.csv"
```

This is the intended locally generated canonical-table path; the notebook checks its columns, endpoint counts and 512-bit fingerprints before proceeding. Set `NCATS_RAW_PATH` explicitly if more than one `Training_set.csv` exists beneath `data/`. External molecular-structure resolution also uses source-backed local SMILES/compound files and, where available, a local PubChem cache; the two approved additional structures are included in `data/processed/external_validation/external_approved_smiles.csv`. **Matching the original structure-source selections and coverage may require additional non-redistributed local inputs.** Do not invent SMILES to force complete coverage.

## Notebook execution order

Run each notebook **from top to bottom** with the appropriate source data already in place. The workflow is sequential where indicated; some analyses can be revisited independently after their local inputs exist.

| Order | Notebook | Prerequisites | Main checks or outputs |
| --- | --- | --- | --- |
| 1 | [NCATS/PANC-1 benchmark](notebooks/NCATS_PANC1_single_cell_line_benchmark.ipynb) | Original NCATS `Training_set.csv` | 496 combinations; 32 held-out-compound rounds; feature/model benchmark |
| 2 | [Multi-cell-line dataset assembly](notebooks/multi_cell_line_dataset.ipynb) | Original Jaaks/GDSC, DepMap 26Q1 and DrugComb files | Produces the two ignored modelling input CSVs and local audit records |
| 3 | [Grouped multi-cell-line validation](notebooks/multi_cell_line_grouped_validation.ipynb) | Both CSVs from step 2 | Ten grouped validation splits, model-family comparisons, propensity baselines, neural models and cold-drug splits |
| 4 | [Candidate ranking](notebooks/drug_pair_candidate_ranking.ipynb) | Canonical CSV from step 2; published `tables/candidate_pair_secondary_support.csv` | Ten-fold out-of-fold ranking of 325 pairs; three models × two endpoints; post-hoc secondary support |
| 5 | [External data harmonisation](notebooks/external_pdac_dataset_harmonisation.ipynb) | Yale, Höfer, Vis and Bashi original files | Source harmonisation tables and external contract; 820 + 146 + 48 + 109 pairs |
| 6 | [External experimental validation](notebooks/external_experimental_validation.ipynb) | Contract and source tables from step 5, NCATS source, canonical training CSV, verified external SMILES/structure sources | 1,619 external pairs, 1,539 fingerprint-complete pairs in the original analysis; model predictions, consensus and agreement metrics |

Steps 3 and 4 use the output of step 2; step 6 requires step 5. Step 1 can be run independently of the Jaaks/DepMap data. Some model-fitting cells, especially the multi-cell-line neural and nested-tuning analyses, are computationally intensive. Results are displayed inside notebooks; some audit, prediction and figure outputs are written to ignored local `results/` directories. Do not assume every displayed summary has a separate committed CSV.

## Random seeds and validation design

The notebooks define seeds at their relevant configuration or model-creation cells:

| Analysis | Seed / design |
| --- | --- |
| NCATS/PANC-1 | `RANDOM_STATE = 42` for the general estimators; `NCATS_RANDOM_STATE = 2` for the NCATS random-forest variants; all **32** compounds serve as held-out compounds |
| Dataset assembly | `RANDOM_STATE = 42` for expression PCA; Morgan radius **2**, **512** bits per drug |
| Grouped multi-cell-line modelling | `SEED = 42`, `N_SPLITS = 10`, `TEST_FRACTION = 0.20`; grouped by cell line or drug pair; model/neural/tuning seeds also derive deterministically from the base seed and fold identifiers |
| Identity-free cold-drug validation | Ten drug-identity 80/20 holdouts, derived from `SEED = 42`; 20 familiar training drugs and 6 held-out drugs per split |
| Candidate ranking | `SEED = 42`; deterministic `GroupKFold(n_splits = 10)` over unordered drug pairs |
| External harmonisation | Deterministic response harmonisation; no separate simulation seed required |
| External model refit | `random_state = 42` / `random_seed = 42` for HistGradientBoosting, LightGBM and CatBoost |

Seeds help with repeatability but do not guarantee bit-for-bit equality across library versions, CPU/GPU setups, parallel training configurations or different inputs. Refer to the exact model parameters and train/test definitions in the notebooks rather than assuming a single global seed controls every routine.

## Verify a local reproduction

Before interpreting model performance, confirm that the source versions and processed input contracts match. Representative checks include:

| Check | Expected in the recorded thesis analysis |
| --- | ---: |
| PANC-1 source combinations / compounds / positives | 496 / 32 / 256 |
| Jaaks/GDSC concentration observations / positive labels | 53,441 / 2,483 |
| Canonical cell-line × drug-pair units | 8,450 = 26 × 325 |
| Any-positive / strict majority-positive units | 1,063 / 188 |
| Internal expression input | 26 cell lines × 19,215 gene features (+ `ModelID`) |
| Candidate ranking | 325 pairs; top consensus pair in the saved analysis: NAVITOCLAX + OSI027 |
| External harmonisation | Yale 820; Höfer 146; Vis 48; Bashi 109; NCATS 496 |
| External fingerprint coverage | 1,539 / 1,619 (95.1%) |

The notebooks include assertions and displayed audit/performance tables. Compare your fresh run with **those actual computed outputs**, not just the frozen expected-value constants. The public assembly notebook does not retain execution outputs for all upstream counts, so a new reader cannot independently confirm the original concentration-level assembly without the corresponding source files. Numerical equality alone is insufficient if different source mappings or chemistry were used.

For the two required restricted modelling tables, confirm local presence and check that Git ignores them (Windows PowerShell, from the repository root):

```powershell
Test-Path "tables/pdac_multicell_drug_pair_units_with_morgan.csv"
Test-Path "tables/depmap_pdac_full_expression_for_fold_pca.csv"
git check-ignore -v -- "tables/pdac_multicell_drug_pair_units_with_morgan.csv"
git check-ignore -v -- "tables/depmap_pdac_full_expression_for_fold_pca.csv"
```

Preserve locally the source versions, SHA-256 checksums, notebook run settings, and generated manifests. Do not commit local restricted input data or intermediate fitted-model artifacts merely to document reproducibility.

## Data sources, attribution and licences

- **Jaaks/Coker screening:** [Original screen drug combination data](https://doi.org/10.6084/m9.figshare.16843597) and [Jaaks et al. (2022)](https://doi.org/10.1038/s41586-022-04437-2). The Figshare record displays CC BY 4.0 alongside further usage information; consult the exact source conditions.
- **DepMap/CCLE:** [DepMap downloads](https://depmap.org/portal/data_page/), specifically the **Public 26Q1** release used in the thesis. Check version-specific terms; public availability does not necessarily establish permission to republish derived expression tables.
- **DrugComb:** [dataset information](https://researchportal.helsinki.fi/en/datasets/drugcomb/) and the actual identifier/annotation file used in the workflow; inspect its file-specific terms.
- **External screens:** Yale/Langdon, Höfer, Vis, Bashi and NCATS/PANC-1, as individually linked above. Each study's source data and publication retain their own terms and attribution requirements.

For details on source licences, original-versus-processed files, known reconstruction gaps and appropriate attribution, read [docs/DATA_ACCESS_AND_PREPROCESSING.md](docs/DATA_ACCESS_AND_PREPROCESSING.md). This repository does not redistribute the original restricted datasets, and no licence for third-party material is granted by making the analysis code publicly viewable. **No repository-level `LICENSE` file is currently provided; do not assume an open-source licence for this code.**

## Reproducibility limitations

- The environment snapshot records successful dependency imports, **not** an independently validated fresh installation and full run on every platform.
- Full reconstruction requires the matching original Jaaks/GDSC, DrugComb and DepMap source releases, mapping/identifier decisions and chemical structures. Source retrieval alone does not guarantee identical processed tables.
- The external experimental workflow depends on original study files and several separately sourced molecular-structure lookups; missing or ambiguous compounds are excluded rather than guessed.
- The fixed random seeds and frozen expected counts facilitate checks but cannot replace actual source- and output-level verification.
- Candidate rankings and external agreement are computational research findings, **not clinically validated treatment recommendations**.

For package versions, installation caveats and the environment-capture method, see [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) and [`scripts/capture_thesis_environment.py`](scripts/capture_thesis_environment.py).
