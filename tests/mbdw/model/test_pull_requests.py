"""
unit tests for module src2.model.pull_requests
"""

import pytest
from pathlib import Path
from pyspark.sql import SparkSession
from mbdw.model.pull_requests import PRData


@pytest.fixture()
def create_spark_session() -> SparkSession:
    return SparkSession.builder.getOrCreate()


@pytest.fixture
def create_test_df(create_spark_session) -> PRData:
    pr_data_path: Path = Path("tests/mbdw/resources/sample_prs")
    prs: PRData = PRData(create_spark_session, pr_data_path)

    return prs


def test_pr_prefixes_df(create_test_df):
    """
    the final pr df should have only prefixed columns
    """
    prepared_df = create_test_df.prepare_pr_df()

    assert all(col.startswith("pr_") for col in prepared_df.columns)


def test_pr_schema_df(create_test_df):
    """
    the final pr df's schema should match the length of the list of columns we select from the raw data
    """
    prepared_df = create_test_df.prepare_pr_df()

    assert (len(create_test_df.pr_cols) == len(prepared_df.columns))
