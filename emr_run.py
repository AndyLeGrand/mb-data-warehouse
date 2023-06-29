"""
helper script to launch the spark application on an EMR serverless instance.
"""

import logging
import subprocess
import sys
from subprocess import CompletedProcess
import re


def main():
    emr_run_str = \
        ("""emr run
        --application-id 00fb646prhfsc31d
        --job-role arn:aws:iam::402104294849:role/EMRServerlessS3RuntimeRole-custom
        --s3-code-uri s3://mb-data-warehouse/pyspark_package/master/
        --entry-point main.py
        --job-name etl-prs-issues
        --wait
        """)

    # remove any newline and tab characters
    emr_cmd = re.sub('\s+', ' ', emr_run_str).strip()

    output: CompletedProcess = subprocess.run(emr_cmd, shell=True, stderr=sys.stderr, stdout=sys.stdout)

    logging.info(output.stdout)
    logging.error(output.stderr)


if __name__ == '__main__':
    main()
