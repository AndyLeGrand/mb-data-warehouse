#!/usr/bin/env python
"""
this module contains a part of the data model
"""

__author__ = "Andreas Kreitschmann"
__email__ = "a.kreitschmann@gmail.com"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.1.0"

from pyspark.sql import DataFrame
from pyspark.sql.functions import explode, col
from src.mbdw.model.pull_requests import PRData


class LabelsData:
    """
    this class models labels that can be used to tag issues and pull requests. Our analytical questions
    are only concerned with labels in the context of PRs, so we can limit the input
    data to data coming from pull requests.
    """
    pr_data: DataFrame

    def __init__(self, pr_data: PRData):
        self.pr_data = pr_data.input_df

    def prepare_label_data(self) -> DataFrame:
        """
        returns a dataframe representing the dimension table for labels.

        schema:
         |-- color: string (nullable = true)
         |-- default: boolean (nullable = true)
         |-- description: string (nullable = true)
         |-- id: long (nullable = true)
         |-- name: string (nullable = true)
         |-- node_id: string (nullable = true)
         |-- url: string (nullable = true)
        """
        return (
                self.pr_data
                .select(explode(col("labels")).alias("labels"))
                .select("labels.*")
                )

    def create_dim_df(self) -> DataFrame:
        """
        de-duplicates label data and drops record without id,
        so that data can be written to normalized dimension table.
        :return:
        """
        return (self.prepare_label_data()
                .na.drop(subset=["id"])
                .drop_duplicates())
