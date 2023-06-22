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
from src.model.issues import IssuesData
from src.model.pull_requests import PRData
from src.model.milestones import MilestoneData
from src.model.labels import LabelsData
from src.model.facts import PRIssuesData


def main():
    logging.info("reading raw data")

    issues_data_path: Path = Path("../data/prepared_issues")
    pr_data_path: Path = Path("../data/prepared_pull_requests")

    pr_data = PRData(pr_data_path)
    issues_data = IssuesData(issues_data_path)

    # generate facts table
    pr_issues_joined_df = PRIssuesData(pr_data=pr_data, issues_data=issues_data).join_data()
    pr_issues_joined_df.show()

    # generate dimension tables
    label_dim_data = LabelsData(pr_data=pr_data)
    label_dim_df = label_dim_data.create_dim_df()
    label_dim_df.show()

    milestone_dim_data = MilestoneData(pr_data=pr_data)
    milestone_dim_df = milestone_dim_data.create_dim_df()
    milestone_dim_df.show()

    # TODO: add sinks for data
    # TODO: does not run yet

    # TODO: add schema classes & quality checks when reading data (?)

    # TODO: create logic to update dim tables on new batch
    # TODO: should fact tables also be updated?

    # TODO: update data model

    # data flow:
    # Spark --> S3 --> copy into Redshift (upsert)

    # Nice to have:
    # logging


if __name__ == '__main__':
    main()
