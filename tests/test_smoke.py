"""Basic checks that the project package can be imported."""

from credit_risk import __version__
from credit_risk.config import RAW_DATA_DIR
from credit_risk.data_utils import describe_data_location


def test_package_imports() -> None:
    """The package exposes a version and configured raw-data location."""
    assert __version__ == "0.1.0"
    assert RAW_DATA_DIR.name == "raw"
    assert describe_data_location(RAW_DATA_DIR).endswith("raw")
