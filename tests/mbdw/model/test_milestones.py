#!/usr/bin/env python

"""
unit tests for module src2.model.milestones
"""

import pytest
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from mbdw.model.pull_requests import PRData
from mbdw.model.milestones import MilestoneData


@pytest.fixture
def create_spark_session() -> SparkSession:
    return SparkSession.builder.getOrCreate()


@pytest.fixture
def create_test_df(create_spark_session):
    pr_data_path: Path = Path("tests/mbdw/resources/sample_prs")
    prs: PRData = PRData(create_spark_session, pr_data_path)

    milestone: MilestoneData = MilestoneData(prs)

    return milestone


def test_dim_df_count(create_test_df):
    """tests whether duplicate and null ids are dropped as intended"""

    milestones_df: DataFrame = create_test_df.create_dim_df()
    # count should be two only, null milestone from pr3.json dropped
    assert (milestones_df.count() == 2)


def test_dim_df_conditions(create_test_df):
    """extension of previous test: no null ids or duplicates should exist in the labels dimension df"""

    labels_df: DataFrame = create_test_df.create_dim_df()
    assert (labels_df['id'].isNotNull and
           labels_df.drop_duplicates().count() == labels_df.count())
