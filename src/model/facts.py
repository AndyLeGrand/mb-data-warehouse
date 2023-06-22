"""
Class for preparation of final facts dataframe / table
"""

__author__ = "Andreas Kreitschmann"
__email__ = "a.kreitschmann@gmail.com"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.1.0"

from pyspark.sql import DataFrame
from src.model.pull_requests import PRData
from src.model.issues import IssuesData


class PRIssuesData:
    pr_data: PRData
    issues_data: IssuesData

    def __init__(self, pr_data: PRData, issues_data: IssuesData):
        self.pr_data = pr_data
        self.issues_data = issues_data

    def join_data(self) -> DataFrame:
        """
        joining pull request and issues data
        :return: joined df
        """
        pr_df = self.pr_data.prepare_pr_df()
        issue_df = self.issues_data.prepare_issues_df()

        joined_df = pr_df.join(issue_df, pr_df['pr_url'] == issue_df['issue_pull_request_url'], 'left')

        return joined_df

