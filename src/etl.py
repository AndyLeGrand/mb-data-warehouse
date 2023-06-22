#!/usr/bin/env python

"""
This module contains the transformation logic for trasnforming raw json data into tabular data to be stored in a data
warehouse.
"""

__author__ = "Andreas Kreitschmann"
__email__ = "a.kreitschmann@gmail.com"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.1.0"

import logging
from pathlib import Path
from src.model.issues import *
from src.model.pull_requests import *
from src.model.milestones import *
from src.model.labels import *


def main():
    logging.info("reading raw data")

    issues_data_path: Path = Path("../data/prepared_issues")
    pr_data_path: Path = Path("../data/prepared_pull_requests")

    issues: IssuesData = IssuesData(issues_data_path)
    pull_requests: PRData = PRData(pr_data_path)

    issues_dim_df = issues.prepare_issues_df()
    issues_dim_df.show()
    issues_dim_df.printSchema()

    pr_dim_df = pull_requests.prepare_pr_df()
    pr_dim_df.show()
    pr_dim_df.printSchema()

    milestones: MilestoneData = MilestoneData(pull_requests)
    milestones_dim_df = milestones.prepare_milestone_data()
    milestones_dim_df.show()
    milestones_dim_df.printSchema()

    labels: LabelsData = LabelsData(pull_requests)
    labels_dim_df = labels.prepare_label_data()
    labels_dim_df.show()
    labels_dim_df.printSchema()

    print(f"labels data before deduplication: {labels_dim_df.count()}")
    dedup_df: DataFrame = labels.create_label_dim_df()
    print(f"labels data after deduplication: {dedup_df.count()}")



    # TODO: creation of dimension tables --> separate function
    # TODO: implement facts.py --> creation of facts table

    # TODO: add schema classes & quality checks when reading data (?)

    # TODO: create logic to update dim tables on new batch
    # TODO: should fact tables also be updated?

    # data flow:
    # Spark --> S3 --> copy into Redshift (upsert)

    # Nice to have:
    # logging


if __name__ == '__main__':
    main()
