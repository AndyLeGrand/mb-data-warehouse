#!/usr/bin/env python
"""
this module contains a part of the data model
"""

__author__ = "Andreas Kreitschmann"
__email__ = "a.kreitschmann@gmail.com"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.1.0"

from typing import List
from pathlib import Path
from pyspark.sql import DataFrame
from src.loader import DataLoader


class IssuesData(DataLoader):
    """
    class to load and transform issues data.
    # TODO: add schema for parsing raw data
    """

    # the following list represents the schema of the Issues dimension (table)
    issue_dim_cols = [
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
        "pull_request.url AS pull_request_url",  # foreign key --> pull_request id not available in issues
        "body",
        # "closed_by",  # user relation ignored
        "reactions",
        "timeline_url",
        "performed_via_github_app",
        "state_reason"
    ]

    def __init__(self, path: Path):
        super().__init__(path)

    @staticmethod
    def prepare_issue_cols(input_cols: List[str], prefix: str, excl_cols: List[str]) -> List[str]:
        return [f"{col} as {prefix}{col}"
                for col in input_cols
                if col not in excl_cols
                ]

    def prepare_issues_df(self) -> DataFrame:
        """
        This method prepares issues data so that it can be conveniently joined with pull_requests data
        :return: dataframe
        """
        # load input data
        input_data = DataLoader.load_data(self, self.data_path)

        # prepend issue_ to each column for easier join; exclude foreign key to pull requests
        prefix = "issue_"
        issue_cols_prefixed: List[str] = self.prepare_issue_cols(self.issue_dim_cols,
                                                                 prefix,
                                                                 ["pull_request.url AS pull_request_url"])

        return DataLoader.select_from_df(
            input_data,
            issue_cols_prefixed
        )
