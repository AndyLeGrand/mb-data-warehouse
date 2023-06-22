"""
bootstrap pipeline by uploading data to S3
"""

from pathlib import Path
import logging
import boto3
from botocore.exceptions import ClientError
import os

S3_BUCKET_NAME = "akreit-dev-bucket"


def main():
    s3 = boto3.resource('s3')

    # list all buckets
    for bucket in s3.buckets.all():
        print(bucket.name)

    # we currently have
    issues_data_path = Path("data/prepared_issues/prepared_issues.json")
    pr_data_path = Path("data/prepared_pull_requests/prepared_pull_requests.json")

    upload_file(str(issues_data_path), S3_BUCKET_NAME)
    upload_file(str(pr_data_path), S3_BUCKET_NAME)


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == '__main__':
    main()