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
from pyspark.sql.functions import explode, col
from src.loader import DataLoader


class PRData(DataLoader):
    """
    class to load and transform pull requests data.
    # TODO: add schema for parsing raw data
    """
    # input data
    input_df: DataFrame

    # list representing the schema of the PullRequests dimension (table)
    pr_cols = [
        "id",
        "url",
        "node_id",
        "html_url",
        "diff_url",
        "patch_url",
        "issue_url",
        "number",
        "state",
        "locked",
        "title",
        # "user"  # user relation ignored
        "body",
        "created_at",
        "updated_at",
        "closed_at",
        "merged_at",
        "merge_commit_sha",
        # "assignee",  # user relation ignored
        # "assignees",  # user relation ignored
        # "requested_reviewers",  # user relation ignored
        # "requested_teams",  # teams relation ignored
        "labels",
        "milestone",
        "draft",
        "commits_url",
        "review_comments_url",
        "review_comment_url",
        "comments_url",
        "statuses_url",
        # "_links",  # ignored
        "author_association",
        "auto_merge",
        "active_lock_reason",
        "merged",
        "mergeable",
        "rebaseable",
        "mergeable_state",
        "merged_by",
        "comments",
        "review_comments",
        "maintainer_can_modify",
        "commits",
        "additions",
        "deletions",
        "changed_files"
    ]

    def __init__(self, path: Path):
        super().__init__(path=path)
        self.input_df = self.load_data()
        self.selected_df = self.input_df.select(*self.pr_cols)

    def prepare_pr_df(self) -> DataFrame:
        """
        This method prepares the pull requests dataframe for the facts table
        :return: dataframe
        """

        # since we move labels and milestones to dimension tables, we only need their ids
        # as foreign keys in our pr data
        normalized_df: DataFrame = (self.selected_df
                                    .withColumn("milestone_id", col("milestone.id"))
                                    .withColumn("labels", explode("labels"))
                                    .withColumn("label_id", col("labels.id"))
                                    .drop("milestone")
                                    .drop("labels")
                                    )

        # prepend pr_ to each column for easier join
        prefix = "pr_"

        prefixed_df: DataFrame = normalized_df.select(
            [normalized_df[clmn].alias(prefix + clmn) for clmn in normalized_df.columns]
        )

        return prefixed_df
