This is the corresponding repository to my Master's thesis from University of Helsinki, titled _Machine learning for drug-combination modelling in pancreatic ductal adenocarcinoma_ and submitted on xx.11.2026. You may access my thesis from the open-source University of Helsinki Library (link).

- Inside the **notebooks** file, there are Jupyter notebooks containing all the algorithms used for the thesis analyses, including single-cell-line benchmarking, multi-cell-line modelling, drug combination prioritisation and testing the models on external experimental evidence.

- Inside the **tables** file, there are the canonical unit-level table and the depmap gene expression table, which are both requirements to have to run the multi_cell_line_grouped_validation notebook.

Exact sources used from other studies (accessed October 2026):

- Langdon et al. (2017), doi: 10.1158/1535-7163.MCT-16-0794 — Yale	Raw_YALE-PDAC.zip	Internal Pancreas_study_summary.csv, particularly observed_bliss_diff. The separate raw-signal CSV is not needed for the harmonised outcome.
- Höfer et al. (2025), doi: 10.1038/s44320-025-00085-6	hoefer_2025_Dataset_EV2.xlsx	Sheet Dataset EV2_146Drugs_Synergy; supplied Synergy labels and AUC∆_sum [%]. HPDE is excluded.
- Vis et al. (2024), doi: 10.1016/j.xcrm.2024.101687	pancan_combi_fitted_data_jan21.tsv.gz from publication Data S1	Pancreatic rows and continuous SYNERGY_DELTA_EMAX. No binary labels are constructed.
- Bashi et al. (2024), doi: 10.1158/2159-8290.CD-23-0388	cd-23-0388_table_s18_suppst18.xlsx	Sheet Supplementary Table 18 Single; combo_MaxE, HSA_matrix and drug/cell-line identities. The notebook constructs the original analysis's binary response rule.
