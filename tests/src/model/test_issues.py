"""
unit tests for module src.model.issues
"""
import json
import pytest
from pathlib import Path
from pyspark.sql import DataFrame
from src.model.issues import IssuesData
from pyspark.sql.types import StructType


@pytest.fixture
def create_test_df():
    issues_data_path: Path = Path("../resources/sample_issues")
    issues: IssuesData = IssuesData(issues_data_path)

    return issues


def test_prepare_issue_cols():
    input_cols = ["a", "b", "c", "d"]
    prefixed_cols = IssuesData.prepare_issue_cols(input_cols, "test_", ["c", "d"])

    expected = ["a as test_a", "b as test_b"]

    assert(prefixed_cols == expected)


def test_prepare_issues_df(create_test_df):

    issues_df: DataFrame = create_test_df.prepare_issues_df()
    print(issues_df.schema.jsonValue())

    # schema_dict = issues_df.schema.jsonValue()
    # schema_dict_json = json.dumps(schema_dict)
    #
    # with open(str(Path("../../../src/schemas/issues_json_schema")), 'w') as f:
    #     json.dump(schema_dict_json, f)
    #
    # json_schema = issues_df.schema.json()
    # new_schema = StructType.fromJson(json.loads(json_schema))
    #
    # assert(issues_df.schema == new_schema)
