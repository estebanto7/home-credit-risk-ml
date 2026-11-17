"""Placeholders for future data loading and validation utilities.

Data cleaning and feature engineering will be implemented in later project
stages. Keeping these responsibilities in a module makes future notebooks
small and easier to reproduce.
"""

from pathlib import Path

import pandas as pd


def load_csv(
    path: str | Path,
    encoding: str = "utf-8"
) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    path : str or Path
        Path to the CSV file.
    encoding : str
        Character encoding used to read the file.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """
    path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    return pd.read_csv(path, encoding=encoding)