"""Capture the actual Python environment used for the PDAC thesis notebooks.

Run with the Python interpreter from the thesis analysis .venv, from the root
of the cleaned public Git repository. No third-party datasets are read.

Outputs:
    requirements.txt      version-pinned direct notebook dependencies
    docs/ENVIRONMENT.md   Python/OS/backend information and validation notes

Refuses to guess missing versions or overwrite existing specifications without
an explicit --overwrite flag.
"""

from __future__ import annotations

import argparse
import importlib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import platform
import sys
from datetime import datetime, timezone

REQUIRED = {
    "numpy": "numpy",
    "pandas": "pandas",
    "scipy": "scipy",
    "matplotlib": "matplotlib",
    "scikit-learn": "sklearn",
    "rdkit": "rdkit",
    "torch": "torch",
    "lightgbm": "lightgbm",
    "catboost": "catboost",
    "xgboost": "xgboost",
    "openpyxl": "openpyxl",
    "ipython": "IPython",
    "ipykernel": "ipykernel",
    "nbformat": "nbformat",
}
OPTIONAL = {
    "pyarrow": "pyarrow",  # Needed when using optional Parquet input files
    "jupyterlab": "jupyterlab",  # Notebook UI; not required for VS Code notebooks
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overwrite", action="store_true", help="Refresh existing files")
    args = parser.parse_args()

    root = Path.cwd()
    if not (root / ".git").exists() or not (root / "notebooks").is_dir():
        raise SystemExit(
            "Run this script from the root of the CLEANED PDAC thesis Git repository."
        )
    if not (root / "notebooks" / "multi_cell_line_grouped_validation.ipynb").is_file():
        raise SystemExit("Expected PDAC thesis modelling notebook not found. Refusing to write.")

    requirements_path = root / "requirements.txt"
    documentation_path = root / "docs" / "ENVIRONMENT.md"
    if not args.overwrite and any(p.exists() for p in (requirements_path, documentation_path)):
        raise SystemExit("Specification already exists. Review it first; use --overwrite to update.")

    pins: dict[str, str] = {}
    missing: list[str] = []
    problems: list[str] = []

    for distribution, module in REQUIRED.items():
        try:
            pins[distribution] = version(distribution)
        except PackageNotFoundError:
            missing.append(distribution)
            continue
        try:
            importlib.import_module(module)
        except Exception as exc:
            problems.append(f"{distribution} ({exc.__class__.__name__}: {exc})")

    try:
        from rdkit.Avalon import pyAvalonTools  # noqa: F401
    except Exception as exc:
        problems.append(f"RDKit Avalon fingerprint extension ({exc.__class__.__name__}: {exc})")

    if missing or problems:
        if missing:
            print("MISSING packages:", ", ".join(missing), file=sys.stderr)
        if problems:
            print("IMPORT FAILURES:", *problems, sep="\n  ", file=sys.stderr)
        raise SystemExit(
            "Environment not yet verified: no files written. "
            "Use the actual thesis analysis .venv and resolve issues first."
        )

    installed_optional = {}
    for distribution in OPTIONAL:
        try:
            installed_optional[distribution] = version(distribution)
        except PackageNotFoundError:
            pass

    pins.update(installed_optional)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    import torch
    import sklearn
    from rdkit import rdBase

    device = "CUDA available" if torch.cuda.is_available() else "CPU (CUDA unavailable)"
    # The wheel distribution version and RDKit's internal version may have
    # different zero padding; record both instead of silently equating them.
    rdkit_runtime = rdBase.rdkitVersion

    sections = [
        "# PDAC thesis computational dependencies", 
        f"# Generated {now} using the Python environment selected by the user.",
        "# Direct notebook/runtime dependencies are pinned to installed versions.",
        "# Python version and platform are recorded in docs/ENVIRONMENT.md.",
        "# This is NOT a complete transitive lockfile or an end-to-end execution test.",
        "",
    ]
    for distribution in REQUIRED:
        sections.append(f"{distribution}=={pins[distribution]}")
    if installed_optional:
        sections.extend(["", "# Optional components present in the captured environment"])
        for distribution in OPTIONAL:
            if distribution in installed_optional:
                sections.append(f"{distribution}=={pins[distribution]}")
    requirements_path.write_text("\n".join(sections) + "\n", encoding="utf-8")

    version_rows = [
        "| Package | Installed version | Use |",
        "| --- | --- | --- |",
    ]
    for distribution in REQUIRED:
        version_rows.append(f"| `{distribution}` | `{pins[distribution]}` | Required by published notebooks or notebook runtime |")
    for distribution in OPTIONAL:
        label = pins.get(distribution, "Not installed (optional)")
        purpose = "Optional Parquet reader" if distribution == "pyarrow" else "Optional local JupyterLab interface"
        version_rows.append(f"| `{distribution}` | `{label}` | {purpose} |")

    doc = "\n".join([
        "# Computational environment",
        "",
        "This document records the installed dependencies in the Python interpreter used to",
        "generate `requirements.txt`. The notebook import checks passed when this snapshot",
        "was created. These are **captured installed versions**, not proof that the complete",
        "analysis was rerun after capture; compare with the original analysis environment",
        "and reproducibility manifests before describing the configuration as fully tested.",
        "",
        f"- Environment snapshot: **{now}**",
        f"- Python: **{platform.python_version()}** ({platform.python_implementation()})",
        f"- Operating system: **{platform.platform()}**",
        f"- PyTorch execution capability at capture: **{device}**",
        f"- RDKit internal version string: **`{rdkit_runtime}`**",
        "- Primary reproducibility target: Windows and the thesis Python environment.",
        "",
        "## Notebook dependency versions",
        "",
        *version_rows,
        "",
        "## Set up a local environment",
        "",
        "Use a compatible Python version (the exact version above is preferred), create",
        "a fresh virtual environment, activate it and install the pinned dependencies:",
        "",
        "```powershell",
        "py -3.14 -m venv .venv",
        r".\.venv\Scripts\Activate.ps1",
        "python -m pip install -r requirements.txt",
        "python -m pip check",
        "python -m ipykernel install --user --name pdac-thesis --display-name 'PDAC thesis'",
        "```",
        "",
        "PyTorch binary installation may be platform-specific (CPU versus CUDA). If its",
        "default PyPI wheel does not match your system, select the appropriate install",
        "command from https://pytorch.org/get-started/locally/ and retain the version",
        "specified in `requirements.txt`. The `rdkit` name refers to the modern PyPI package",
        "(not the legacy `rdkit-pypi` distribution).",
        "",
        "## Scope and limitations",
        "",
        "- `requirements.txt` lists pinned direct packages, not every transitive dependency.",
        "- The script checked that the required modules and RDKit Avalon extension import.",
        "- Version capture and import checks do **not** establish byte-for-byte reproduction",
        "  of the fitted models; rerun the notebooks and validate their frozen audit counts",
        "  and performance outputs to establish end-to-end reproducibility.",
        "- Original Jaaks/GDSC, DrugComb, DepMap and external-screen inputs are obtained",
        "  separately according to `docs/DATA_ACCESS_AND_PREPROCESSING.md` and are not",
        "  distributed with the repository.",
        "- `.parquet` inputs require `pyarrow` (optional here because the published source",
        "  files used in the thesis are not solely Parquet).",
        "- For a complete environment audit, run `python -m pip list --format=freeze`",
        "  locally and review its output; do not publish local paths or credentials.",
        "",
    ])
    documentation_path.parent.mkdir(parents=True, exist_ok=True)
    documentation_path.write_text(doc, encoding="utf-8")

    print(f"Python: {platform.python_version()} | OS: {platform.system()} | Torch: {torch.__version__}")
    print(f"RDKit: package {pins['rdkit']} / runtime {rdkit_runtime}")
    print(f"Scikit-learn: {sklearn.__version__}")
    print(f"Verified {len(REQUIRED)} required package imports and the RDKit Avalon extension.")
    print("Written:", requirements_path)
    print("Written:", documentation_path)


if __name__ == "__main__":
    main()
