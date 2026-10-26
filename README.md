### Machine learning for drug-combination modelling in pancreatic ductal adenocarcinoma (2026) official repository

This is the corresponding repository to my Master's thesis from University of Helsinki, titled _Machine learning for drug-combination modelling in pancreatic ductal adenocarcinoma_ and submitted on xx.11.2026. You may access my thesis from the open-source University of Helsinki Library (link).

- Inside the **notebooks** file, there are Jupyter notebooks containing all the algorithms used for the thesis analyses, including single-cell-line benchmarking, multi-cell-line modelling, drug combination prioritisation and testing the models on external experimental evidence.

- Inside the **tables** file, there are the canonical unit-level table and the depmap gene expression table, which are both requirements to have to run the multi_cell_line_grouped_validation notebook.

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
