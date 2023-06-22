#!/usr/bin/env python
"""
this module contains a part of the data model
"""

__author__ = "Andreas Kreitschmann"
__email__ = "a.kreitschmann@gmail.com"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.1.0"

from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
from src.loader import DataLoader
from src.model.pull_requests import PRData


class MilestoneData:
    """
    this class models milestones that can be attached to issues and pull requests. Our analytical questions
    are only concerned with milestones in the context of PRs, so we can limit the input
    data to data coming from pull requests.
    """
    pr_data: DataFrame

    def __init__(self, pr_data: PRData):
        self.pr_data = pr_data.input_df

    def prepare_milestone_data(self) -> DataFrame:
        """
        returns a dataframe representing the dimension tablef or milestones.
        Note that the 'creator' field is explicitely dropped because our data
        model excludes the person relation.

        schema:
         |-- closed_at: string (nullable = true)
         |-- closed_issues: long (nullable = true)
         |-- created_at: string (nullable = true)
         |-- description: string (nullable = true)
         |-- due_on: string (nullable = true)
         |-- html_url: string (nullable = true)
         |-- id: long (nullable = true)
         |-- labels_url: string (nullable = true)
         |-- node_id: string (nullable = true)
         |-- number: long (nullable = true)
         |-- open_issues: long (nullable = true)
         |-- state: string (nullable = true)
         |-- title: string (nullable = true)
         |-- updated_at: string (nullable = true)
         |-- url: string (nullable = true)
        """
        return self.pr_data\
            .select("milestone.*")\
            .drop("creator")

    def create_dim_df(self) -> DataFrame:
        """
        de-duplicates label data and drops record without id,
        so that data can be written to normalized dimension table.
        :return:
        """
        return (self.prepare_milestone_data()
                .na.drop(subset=["id"])
                .drop_duplicates())

