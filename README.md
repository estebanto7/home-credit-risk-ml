# Home Credit Risk Modeling

An educational, end-to-end machine learning portfolio project for predicting
credit default risk with the [Home Credit Default Risk dataset on Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk).

## Overview

### Business problem

Lenders need to estimate the likelihood that an applicant will default so they
can make consistent, responsible, and data-informed credit decisions. This
project will investigate the data and develop a reproducible modeling workflow
for that prediction problem.

### Prediction objective

The future model will predict the `TARGET` outcome for a loan application.
This repository currently contains infrastructure and learning prompts only;
it does not contain downloaded data, analyses, model results, or business
findings.

## Planned methodology

The project will be developed incrementally:

1. Assess data quality, schema, missingness, and class balance.
2. Clean and document the input data without leaking information across splits.
3. Explore distributions, relationships, and potential data-quality issues.
4. Engineer and document features using training data only where appropriate.
5. Compare baseline and candidate models with consistent validation.
6. Tune selected models with reproducible hyperparameter searches.
7. Validate the final approach and interpret its predictions.

## Repository structure

```text
├── .github/workflows/ci.yml       # Test and lint workflow
├── data/
│   ├── raw/                       # Original Kaggle files (not committed)
│   ├── interim/                   # Temporary transformed data (not committed)
│   └── processed/                 # Modeling-ready data (not committed)
├── notebooks/                     # Guided stages of the analysis
├── src/credit_risk/               # Reusable project code
├── tests/                         # Lightweight automated checks
├── reports/figures/               # Generated figures (not committed)
├── docs/methodology.md            # Methodology notes and decisions
├── pyproject.toml                 # Project metadata and dependencies
└── README.md
```

## Local setup

Python 3.11 is used for this project. From the repository root:

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### macOS/Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

To open the project in VS Code, install the Python and Jupyter extensions, then
run `code .`. Select the `.venv` interpreter with **Python: Select Interpreter**
and choose the same environment as the notebook kernel.

Run the initial checks with:

```bash
pytest
ruff check .
```

## Dataset download

The dataset is not included in this repository. Create a Kaggle account, open
the [Home Credit Default Risk competition](https://www.kaggle.com/competitions/home-credit-default-risk),
accept its rules, and download the files manually. Unzip the downloaded files
into `data/raw/`. Do not commit the files or Kaggle credentials; the project's
`.gitignore` protects both.

## Reproducibility principles

- Keep the Python version and dependencies declared in `pyproject.toml`.
- Record meaningful methodology and modeling decisions.
- Separate training, validation, and test data before fitting transformations.
- Fit preprocessing and feature engineering on training data only.
- Keep raw data immutable and generated artifacts outside version control.
- Use deterministic random seeds where a future analysis requires randomness.
- Validate changes with automated tests and lint checks.

## Project status

**In development**

This is a scaffold for learning and implementation. No model performance,
evaluation metrics, or completed analytical conclusions are claimed.
