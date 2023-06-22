"""
unit tests for module src.model.issues
"""

import pytest
from pathlib import Path
from src.model.issues import IssuesData


@pytest.fixture
def create_test_df():
    pr_data_path: Path = Path("tests/src/resources/sample_issues")
    issues: IssuesData = IssuesData(pr_data_path)

    return issues


def test_issues_prefixes_df(create_test_df):
    """
    the final pr df should have only prefixed columns
    """
    prepared_df = create_test_df.prepare_issues_df()

    assert all(col.startswith("issue_") for col in prepared_df.columns)


def test_issues_schema_df(create_test_df):
    """
    the final pr df's schema should match the length of the list of columns we select from the raw data
    """
    prepared_df = create_test_df.prepare_issues_df()

    assert (len(create_test_df.issue_cols) == len(prepared_df.columns))
