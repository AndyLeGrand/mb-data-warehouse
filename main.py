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
from pyspark.sql import SparkSession
import pydeequ
from mbdw.model.issues import IssuesData
from mbdw.model.pull_requests import PRData
from mbdw.model.milestones import MilestoneData
from mbdw.model.labels import LabelsData
from mbdw.model.issues_prs import PRIssuesData


S3_BUCKET: str = "mb-data-warehouse"


def main():
    logging.info("reading raw data")

    spark: SparkSession = (SparkSession
                           .builder
                           .appName("pr_issues_loader")
                           .config("spark.jars.packages", pydeequ.deequ_maven_coord)
                           .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
                           .getOrCreate())

    s3_issue_prefix: str = "prepared_issues"
    s3_pr_prefix: str = "prepared_pull_requests"

    pr_data = PRData(
        spark=spark,
        s3_bucket=S3_BUCKET,
        source_type="s3",
        s3_prefix=s3_pr_prefix)

    issues_data = IssuesData(spark=spark,
                             s3_bucket=S3_BUCKET,
                             source_type="s3",
                             s3_prefix=s3_issue_prefix)

    # pr_data = PRData(path=pr_data_path)
    # issues_data = IssuesData(path=issues_data_path)

    # pr & issues data semi-normalized
    pr_issues_joined_df = PRIssuesData(pr_data=pr_data, issues_data=issues_data).join_data()
    # pr_issues_joined_df.show()
    pr_issues_joined_df.write.parquet(path=f"s3://{S3_BUCKET}/output/pr_issues_joined", mode="append")

    # labels data
    label_dim_data = LabelsData(pr_data=pr_data)
    label_dim_df = label_dim_data.create_dim_df()
    # label_dim_df.show()
    label_dim_df.write.parquet(path=f"s3://{S3_BUCKET}/output/labels", mode="append")

    # milestones data
    milestone_dim_data = MilestoneData(pr_data=pr_data)
    milestone_dim_df = milestone_dim_data.create_dim_df()
    # milestone_dim_df.show()
    milestone_dim_df.write.parquet(path=f"s3://{S3_BUCKET}/output/milestones", mode="append")


if __name__ == '__main__':
    main()
