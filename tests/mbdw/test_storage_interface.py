"""
unit tests for module src2.loader
"""

import pytest
from pathlib import Path
from pyspark.sql.utils import AnalysisException
from mbdw.storage_interface import StorageInterface


def test_loader_instantiaton_local():
    """
    loading data from a local path should work
    """
    try:
        loader: StorageInterface = StorageInterface(Path("tests/mbdw/resources/sample_issues"))
        loader.load_json_sources().printSchema()
    except AnalysisException:
        pytest.fail("data could not be loaded")

    assert True


def test_loader_instantiaton_not_impl():
    """
    attempting to load data from any source other than local or s3 should fail
    """

    with pytest.raises(NotImplementedError):
        assert StorageInterface(path=Path("tests/mbdw/mbdw/resources/sample_issues"), source_type="hive")


def test_loader_instantiaton_s3():
    """
    attempting to load data from any source other than local or s3 should fail
    """
    loader: StorageInterface = StorageInterface(source_type="s3", s3_bucket="my_bucket", s3_prefix="some_prefix")
    assert (loader.data_path == "s3://my_bucket/some_prefix/")




