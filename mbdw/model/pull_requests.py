#!/usr/bin/env python

"""
This module represents the pull requests relation in the data model.
"""

__author__ = "Andreas Kreitschmann"
__email__ = "a.kreitschmann@gmail.com"
__copyright__ = "the author, 2023"
__license__ = "MIT"
__version__ = "0.1.0"

from pathlib import Path
import logging
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import explode, col
from mbdw.interfaces.storage_interface import DataLoader


class PRData(DataLoader):
    """
    class to load and transform pull requests data.
    # TODO: add schema for parsing raw data
    """
    # input data
    input_df: DataFrame

    # list representing the schema of the PullRequests relation
    # multiple columns are excluded for simplification
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

    def __init__(self,
                 spark: SparkSession,
                 path: Path = None,
                 source_type: str = "local",
                 s3_bucket: str = None,
                 s3_prefix: str = None):
        if path is None and s3_bucket is None:
            logging.error("either path or s3_bucket must be specified")
            raise NotImplementedError

        super().__init__(
            spark=spark,
            path=path,
            source_type=source_type,
            s3_bucket=s3_bucket,
            s3_prefix=s3_prefix)

        self.input_df = self.load_json_sources()
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
