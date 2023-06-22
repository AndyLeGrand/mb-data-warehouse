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
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col
from src.loader import DataLoader


class IssuesData(DataLoader):
    """
    class to load and transform issues data.
    # TODO: add schema for parsing raw data
    """

    input_df: DataFrame

    # the following list represents the schema of the Issues dimension (table)
    issue_cols = [
        "id",  # primary key for Issue dimension
        "url",
        # "repository_url",  # repositories relation
        # "labels_url",  # labels matter only in context of PRs
        # "comments_url",
        # "events_url",
        # "html_url",
        # "node_id",
        "number",
        "title",
        # "user.id AS user_id",  # user relation ignored
        # "labels",  # labels relation ignored
        "state",
        "locked",
        # "assignee.id AS assignee_id",  # user relation ignored
        # "assignees",  # user relation ignored
        # "milestone.id AS milestone_id",  # milestones only matter in context of PRs
        # "comments",
        "created_at",
        "updated_at",
        "closed_at",
        # "author_association",
        "active_lock_reason",
        "draft",
        "pull_request",  # foreign key --> pull_request id not available in issues
        "body",
        # "closed_by",  # user relation ignored
        # "reactions",  # reactions relation ignored
        "timeline_url",
        "performed_via_github_app",
        "state_reason"
    ]

    def __init__(self, path: Path):
        super().__init__(path=path)
        self.input_df = self.load_data()
        self.selected_df = self.input_df.select(*self.issue_cols)

    def prepare_issues_df(self) -> DataFrame:
        """
        This method prepares issues data so that it can be conveniently joined with pull_requests data
        :return: dataframe with schema:

         |-- id: long (nullable = true)
         |-- url: string (nullable = true)
         |-- number: long (nullable = true)
         |-- title: string (nullable = true)
         |-- state: string (nullable = true)
         |-- locked: boolean (nullable = true)
         |-- created_at: string (nullable = true)
         |-- updated_at: string (nullable = true)
         |-- closed_at: string (nullable = true)
         |-- active_lock_reason: string (nullable = true)
         |-- draft: boolean (nullable = true)
         |-- body: string (nullable = true)
         |-- timeline_url: string (nullable = true)
         |-- performed_via_github_app: string (nullable = true)
         |-- state_reason: string (nullable = true)
         |-- pull_request_url: string (nullable = true)
        """

        # we only want to keep the pr url as foreign key to the pr relation
        renamed_df: DataFrame = (self.selected_df
                                 .withColumn("pull_request_url", col("pull_request.url"))
                                 .drop("pull_request")
                                 )

        # prepend issue_ to each column for easier join
        prefix = "issue_"

        # adding prefix to all columns of dataframe
        renamed_df.printSchema()

        prefixed_df: DataFrame = renamed_df.select(
            [renamed_df[clmn].alias(prefix + clmn) for clmn in renamed_df.columns]
        )

        prefixed_df.printSchema()

        return prefixed_df
