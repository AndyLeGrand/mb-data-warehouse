"""
unit tests for module src.model.labels
"""

import json
import pytest
from pathlib import Path
from pyspark.sql import DataFrame
from src.model.pull_requests import PRData
from src.model.labels import LabelsData


@pytest.fixture
def create_test_df():
    pr_data_path: Path = Path("tests/src/resources/sample_prs/pr1.json")
    prs: PRData = PRData(pr_data_path)

    labels: LabelsData = LabelsData(prs)

    return labels


def test_dim_df_count(create_test_df):
    """tests whether duplicate and null ids are dropped as intended"""

    labels_df: DataFrame = create_test_df.create_dim_df()
    assert(labels_df.count() == 3)


def test_dim_df_conditions(create_test_df):
    """extension of previous test: no null ids or duplicates should exist in the labels dimension df"""

    labels_df: DataFrame = create_test_df.create_dim_df()
    assert(labels_df['id'].isNotNull and
           labels_df.drop_duplicates().count() == labels_df.count())
