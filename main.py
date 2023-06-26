#!/usr/bin/env python

"""
Entry point for the pyspark application.
"""

__author__ = "Andreas Kreitschmann"
__email__ = "a.kreitschmann@gmail.com"
__copyright__ = "the author, 2023"
__license__ = "MIT"
__version__ = "0.1.0"

import logging
from src.mbdw.model.issues import IssuesData
from src.mbdw.model.pull_requests import PRData
from src.mbdw.model.milestones import MilestoneData
from src.mbdw.model.labels import LabelsData
from src.mbdw.model.facts import PRIssuesData


def main():
    logging.info("reading raw data")

    # issues_data_path: Path = Path("../data/prepared_issues")
    # pr_data_path: Path = Path("../data/prepared_pull_requests")

    # TODO: make data soure and sink configurable via yaml

    s3_bucket: str = "akreit-dev-bucket"
    s3_issue_prefix: str = "prepared_issues"
    s3_pr_prefix: str = "prepared_pull_requests"

    pr_data = PRData(s3_bucket=s3_bucket,
                     source_type="s3",
                     s3_prefix=s3_pr_prefix)

    issues_data = IssuesData(s3_bucket=s3_bucket,
                             source_type="s3",
                             s3_prefix=s3_issue_prefix)

    # pr_data = PRData(path=pr_data_path)
    # issues_data = IssuesData(path=issues_data_path)

    # pr & issues data semi-normalized
    pr_issues_joined_df = PRIssuesData(pr_data=pr_data, issues_data=issues_data).join_data()
    pr_issues_joined_df.show()
    pr_issues_joined_df.write.parquet(path=f"s3://{s3_bucket}/output/pr_issues_joined", mode="append")

    # labels data
    label_dim_data = LabelsData(pr_data=pr_data)
    label_dim_df = label_dim_data.create_dim_df()
    label_dim_df.show()
    label_dim_df.write.parquet(path=f"s3://{s3_bucket}/output/labels", mode="append")

    # milestones data
    milestone_dim_data = MilestoneData(pr_data=pr_data)
    milestone_dim_df = milestone_dim_data.create_dim_df()
    milestone_dim_df.show()

    milestone_dim_df.write.parquet(path=f"s3://{s3_bucket}/output/milestones", mode="append")

    # TODO: add schema classes & quality checks when reading data (?)

    # TODO: add architecture documentation

    # TODO: create logic to update dim tables on new batch
    # TODO: should fact tables also be updated?

    # TODO: update data model

    # data flow:
    # Spark --> S3 --> copy into Redshift (upsert)

    # Nice to have:
    # integrate with Spark logging


if __name__ == '__main__':
    main()
