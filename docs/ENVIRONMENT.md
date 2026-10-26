# Computational environment

This document records the installed dependencies in the Python interpreter used to
generate `requirements.txt`. The notebook import checks passed when this snapshot
was created. These are **captured installed versions**, not proof that the complete
analysis was rerun after capture; compare with the original analysis environment
and reproducibility manifests before describing the configuration as fully tested.

- Environment snapshot: **2026-10-26 15:15 UTC**
- Python: **3.14.3** (CPython)
- Operating system: **Windows-11-10.0.26200-SP0**
- PyTorch execution capability at capture: **CPU (CUDA unavailable)**
- RDKit internal version string: **`2026.03.1`**
- Primary reproducibility target: Windows and the thesis Python environment.

## Notebook dependency versions

| Package | Installed version | Use |
| --- | --- | --- |
| `numpy` | `2.4.4` | Required by published notebooks or notebook runtime |
| `pandas` | `2.3.3` | Required by published notebooks or notebook runtime |
| `scipy` | `1.17.1` | Required by published notebooks or notebook runtime |
| `matplotlib` | `3.10.9` | Required by published notebooks or notebook runtime |
| `scikit-learn` | `1.8.0` | Required by published notebooks or notebook runtime |
| `rdkit` | `2026.3.1` | Required by published notebooks or notebook runtime |
| `torch` | `2.13.0` | Required by published notebooks or notebook runtime |
| `lightgbm` | `4.7.0` | Required by published notebooks or notebook runtime |
| `catboost` | `1.2.10` | Required by published notebooks or notebook runtime |
| `xgboost` | `3.3.0` | Required by published notebooks or notebook runtime |
| `openpyxl` | `3.1.5` | Required by published notebooks or notebook runtime |
| `ipython` | `9.13.0` | Required by published notebooks or notebook runtime |
| `ipykernel` | `7.2.0` | Required by published notebooks or notebook runtime |
| `nbformat` | `5.10.4` | Required by published notebooks or notebook runtime |
| `pyarrow` | `Not installed (optional)` | Optional Parquet reader |
| `jupyterlab` | `4.5.7` | Optional local JupyterLab interface |

## Set up a local environment

Use a compatible Python version (the exact version above is preferred), create
a fresh virtual environment, activate it and install the pinned dependencies:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
python -m ipykernel install --user --name pdac-thesis --display-name 'PDAC thesis'
```

PyTorch binary installation may be platform-specific (CPU versus CUDA). If its
default PyPI wheel does not match your system, select the appropriate install
command from https://pytorch.org/get-started/locally/ and retain the version
specified in `requirements.txt`. The `rdkit` name refers to the modern PyPI package
(not the legacy `rdkit-pypi` distribution).

## Scope and limitations

- `requirements.txt` lists pinned direct packages, not every transitive dependency.
- The script checked that the required modules and RDKit Avalon extension import.
- Version capture and import checks do **not** establish byte-for-byte reproduction
  of the fitted models; rerun the notebooks and validate their frozen audit counts
  and performance outputs to establish end-to-end reproducibility.
- Original Jaaks/GDSC, DrugComb, DepMap and external-screen inputs are obtained
  separately according to `docs/DATA_ACCESS_AND_PREPROCESSING.md` and are not
  distributed with the repository.
- `.parquet` inputs require `pyarrow` (optional here because the published source
  files used in the thesis are not solely Parquet).
- For a complete environment audit, run `python -m pip list --format=freeze`
  locally and review its output; do not publish local paths or credentials.
