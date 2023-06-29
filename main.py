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
from pyspark.sql import SparkSession, DataFrame
from typing import List
from datetime import datetime
import pydeequ
from mbdw.interfaces.storage_interface import DataWriter
from mbdw.model.issues import IssuesData
from mbdw.model.pull_requests import PRData
from mbdw.model.milestones import MilestoneData
from mbdw.model.labels import LabelsData
from mbdw.model.issues_prs import PRIssuesData


S3_BUCKET: str = "mb-data-warehouse"


def main():

    # create a spark session
    spark: SparkSession = (SparkSession
                           .builder
                           .appName("pr_issues_loader")
                           .config("spark.jars.packages", pydeequ.deequ_maven_coord)
                           .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
                           .getOrCreate())

    # read raw data
    s3_issue_prefix: str = "data/raw/issues"
    s3_pr_prefix: str = "data/raw/pull_requests"

    pr_data = PRData(
        spark=spark,
        s3_bucket=S3_BUCKET,
        source_type="s3",
        s3_prefix=s3_pr_prefix)

    issues_data = IssuesData(spark=spark,
                             s3_bucket=S3_BUCKET,
                             source_type="s3",
                             s3_prefix=s3_issue_prefix)

    # pr & issues data semi-normalized
    pr_issues_joined_df = PRIssuesData(pr_data=pr_data, issues_data=issues_data).join_data()

    # labels data
    labels_data: LabelsData = LabelsData(pr_data=pr_data)
    labels_df: DataFrame = labels_data.create_dim_df()

    # milestones data
    milestones_data: MilestoneData = MilestoneData(pr_data=pr_data)
    milestones_df: DataFrame = milestones_data.create_dim_df()

    # write prepared data back to S3
    dfs_to_write: List[DataFrame] = [pr_issues_joined_df, labels_df, milestones_df]
    obj_suffixes: List[str] = ["pr_issues", "labels", "milestones"]

    for idx, df in enumerate(dfs_to_write):
        writer: DataWriter = DataWriter(spark, df)
        date_str: str = datetime.today().strftime('%Y-%m-%d')
        writer.write_to_s3(s3_bucket=S3_BUCKET, prefix=f"data/output/{date_str}/{obj_suffixes[idx]}")


if __name__ == '__main__':
    main()
