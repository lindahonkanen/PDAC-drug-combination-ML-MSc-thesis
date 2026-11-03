# Data access and preprocessing

This guide lists the datasets required for the PDAC thesis notebooks and how to prepare their inputs. Original experimental datasets and large processed modelling tables are not included in the repository and must be obtained separately.

## Data sources

| Dataset | Source | Required file |
| --- | --- | --- |
| Jaaks/GDSC drug-combination screen | [Coker and Jaaks, original screening data](https://doi.org/10.6084/m9.figshare.16843597) | Original screening-response file |
| DepMap expression and cell-line metadata | [DepMap downloads](https://depmap.org/portal/data_page/) | Public 26Q1 expression data and `Model.csv` |
| DrugComb annotations | [DrugComb dataset](https://researchportal.helsinki.fi/en/datasets/drugcomb/) / [identifier archive](https://zenodo.org/records/18449193) | Drug-identifier/annotation workbook |
| NCATS/PANC-1 | [NCATS/PANC1](https://github.com/ncats/PANC1) | `datasets/Training_set.csv` |
| Yale / Langdon | [Langdon et al., 2017](https://doi.org/10.1158/1535-7163.MCT-16-0794) | `Raw_YALE-PDAC.zip` |
| Höfer | [Höfer et al., 2025](https://doi.org/10.1038/s44320-025-00085-6) | `hoefer_2025_Dataset_EV2.xlsx` |
| Vis | [Vis et al., 2024](https://doi.org/10.1016/j.xcrm.2024.101687) | `pancan_combi_fitted_data_jan21.tsv.gz` (Data S1) |
| Bashi | [Bashi et al., 2024](https://doi.org/10.1158/2159-8290.CD-23-0388) | `cd-23-0388_table_s18_suppst18.xlsx` |

Download the required files into `data/raw/` and check the input paths in each notebook's configuration cell. The notebooks do not download the original data automatically.

Use the corresponding source releases and verify the relevant data-usage terms before redistributing any original or derived files.

## Preparing the modelling inputs

Run [`multi_cell_line_dataset.ipynb`](../notebooks/multi_cell_line_dataset.ipynb) with the Jaaks/GDSC, DepMap and DrugComb datasets. The notebook generates two local files:

```text
tables/pdac_multicell_drug_pair_units_with_morgan.csv
tables/depmap_pdac_full_expression_for_fold_pca.csv
```

These files are required for the multi-cell-line analyses and are excluded from Git.

The dataset assembly should reproduce **8,450 canonical cell-line–drug-pair units** across 26 PDAC cell lines and 325 unordered drug pairs. Additional dataset checks are included in the notebook.

**Note:** For unseen-cell-line validation, expression preprocessing and PCA must be fitted using training cell lines only. The global PCA features created during dataset assembly must not be used as substitutes.

## External validation inputs

Run [`external_pdac_dataset_harmonisation.ipynb`](../notebooks/external_pdac_dataset_harmonisation.ipynb) with the Yale, Höfer, Vis and Bashi datasets to prepare the external response tables.

Then run [`external_experimental_validation.ipynb`](../notebooks/external_experimental_validation.ipynb) using these outputs, the NCATS/PANC-1 dataset and the canonical modelling table.

Check the `TRAINING_UNITS_PATH` and molecular-structure input paths in the external-validation notebook. The repository includes `data/processed/external_validation/external_approved_smiles.csv`, but additional verified structure inputs may be required.

## Data availability

Original datasets, large processed modelling tables and generated results are excluded from the public repository. The small supporting files needed for candidate ranking and molecular-structure mapping are provided in GitHub.

Reproducing the reported results requires matching the original data releases, compound identifiers and preprocessing inputs.
