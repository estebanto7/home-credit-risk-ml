"""Placeholders for future data loading and validation utilities.

Data cleaning and feature engineering will be implemented in later project
stages. Keeping these responsibilities in a module makes future notebooks
small and easier to reproduce.
"""

from pathlib import Path


def describe_data_location(path: Path) -> str:
    """Return a human-readable description of a planned data location."""
    return f"Data location: {path}"
