"""
unit tests for module src2.loader
"""

import pytest
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
from mbdw.interfaces.storage_interface import DataLoader


@pytest.fixture()
def create_spark_session():
    return SparkSession.builder.getOrCreate()


def test_loader_instantiaton_local(create_spark_session):
    """
    loading data from a local path should work
    """
    try:
        loader: DataLoader = DataLoader(create_spark_session, Path("tests/mbdw/resources/sample_issues"))
        loader.load_json_sources().printSchema()
    except AnalysisException:
        pytest.fail("data could not be loaded")

    assert True


def test_loader_instantiaton_not_impl(create_spark_session):
    """
    attempting to load data from any source other than local or s3 should fail
    """

    with pytest.raises(NotImplementedError):
        assert DataLoader(create_spark_session, path=Path("tests/mbdw/mbdw/resources/sample_issues"), source_type="hive")


def test_loader_instantiaton_s3(create_spark_session):
    """
    attempting to load data from any source other than local or s3 should fail
    """
    loader: DataLoader = DataLoader(create_spark_session, source_type="s3", s3_bucket="my_bucket", s3_prefix="some_prefix")
    assert (loader.data_path == "s3://my_bucket/some_prefix/")




