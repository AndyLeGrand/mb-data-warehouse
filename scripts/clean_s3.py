"""
helper script to delete artifacts from S3 during development.
"""

import logging
import boto3

S3_BUCKET_NAME = "akreit-dev-bucket"


def main():
    # Usage example
    bucket_name = S3_BUCKET_NAME
    prefix = 'pr_issues_package/'

    delete_objects_in_bucket(bucket_name, prefix)


def delete_objects_in_bucket(bucket_name, prefix):
    s3 = boto3.client('s3')
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)['Contents']
    object_keys = [{'Key': obj['Key']} for obj in objects]

    # for key in object_keys:
    # print(key)

    s3.delete_objects(Bucket=bucket_name, Delete={'Objects': object_keys})


if __name__ == '__main__':
    main()
