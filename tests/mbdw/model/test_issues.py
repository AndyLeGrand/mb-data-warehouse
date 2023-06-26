"""
unit tests for module src2.model.issues
"""

import pytest
from pathlib import Path
from pyspark.sql import SparkSession
from mbdw.model.issues import IssuesData


@pytest.fixture()
def create_spark_session():
    return SparkSession.builder.getOrCreate()


@pytest.fixture
def create_test_df(create_spark_session):
    pr_data_path: Path = Path("tests/mbdw/resources/sample_issues")
    issues: IssuesData = IssuesData(create_spark_session, pr_data_path)

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
