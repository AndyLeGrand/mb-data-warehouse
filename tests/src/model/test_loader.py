"""
unit tests for module src.loader
"""

import pytest
from pyspark.sql.utils import AnalysisException
from pathlib import Path
from src.loader import DataLoader


def create_test_df():
    """
    test if loading source data works as expected
    """
    issues_data_path: Path = Path("tests/src/resources/sample_issues")
    try:
        loader: DataLoader = DataLoader(issues_data_path)
        loader.load_data()
    except AnalysisException as e:
        pytest.fail(f"could not load json data from given path due to {e}")
