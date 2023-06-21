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
from src.model.pull_requests import PRData


class LabelsData:
    """
    this class models labels that can be used to tag issues and pull requests. Our analytical questions
    are only concerned with labels in the context of PRs, so we can limit the input
    data to data coming from pull requests.
    """
    pr_data: DataFrame

    def __init__(self, pr_data: PRData):
        self.pr_data = pr_data.input_df

    def create_label_dim_df(self) -> DataFrame:
        """
        returns a dataframe representing the dimension table for labels.
        Note that the 'creator' field is explicitely dropped because our data
        model excludes the person relation.

        schema:
        """
        return (
                self.pr_data
                .select(explode(col("labels")).alias("labels"))
                .select("labels.*")
                )
