#!/usr/bin/env python

"""
This module contains the transformation logic for trasnforming raw json data into tabular data to be stored in a data
warehouse.
"""

__author__ = "Andreas Kreitschmann"
__email__ = "a.kreitschmann@gmail.com"
__copyright__ = "the author, 2023"
__license__ = "MIT"
__version__ = "0.1.0"

import logging
import sys
import os
from random import random
from operator import add
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
from slash3 import S3Uri
from pyspark import SparkContext
from pyspark.conf import SparkConf
import boto3


class StorageInterface:
    """
    base class for loading and transforming raw data.
    TODO: add interface to load from S3
    """
    spark: SparkSession
    data_path: str

    def __init__(self,
                 path: Path = None,
                 source_type: str = "local",
                 s3_bucket: str = None,
                 s3_prefix: str = None
                 ):
        """
        creates a DataLoader object to load the source data for this application
        :param path: source data path if source_type is local; for s3 source, keep default (None)
        :param source_type: local or s3; other inputs will raise an NotImplementedError
        :param s3_bucket: bucket name (without leading s3:// or trailing slashes)
        :param s3_prefix: s3 prefix w/o slashes such that object id becomes: s3://<bucket_name>/<s3_prefix>
        """
        self.spark: SparkSession = SparkSession.builder.appName("pr_issues_loader").getOrCreate()

        match source_type:
            case "local":
                logging.info("reading data from local path")
                self.data_path = str(path)
            case "s3":
                if s3_bucket is None:
                    logging.error("for s3 data source, specify bucket and optionally a prefix")
                    raise FileNotFoundError
                else:
                    logging.info("reading data from s3 p")
                    # self.data_path = str(S3Uri.to_uri(s3_bucket, s3_prefix))
                    self.data_path = f"s3://{s3_bucket}/{s3_prefix}/"
            case _:
                logging.error("currently only local / hdfs or s3 sources are supported")
                raise NotImplementedError

    def load_json_sources(self) -> DataFrame:
        logging.info(f"attempting to load source data from {self.data_path}")
        return (self.spark
                .read
                .option("multiline", "true")
                .option("inferSchema", "true")
                .json(str(self.data_path))
                )


class DataWriter:
    """
    class for writing data to sinks
    """
    spark: SparkSession

    def __init__(self, sink_type: str):
        """
        create a Spark dataframe writer object pre-configured for the desired sink type
        :param sink_type:
        """
        self.spark: SparkSession = SparkSession.getActiveSession()

        logging.info(f"re-using Spark session for: {self.spark.sparkContext.applicationId}")

        match sink_type:
            case "local":
                pass
            case "s3":
                self.write_to_s3()

    def write_to_hdfs(self) -> None:
        pass

    def write_to_hive_tbl(self) -> None:
        pass

    def write_to_s3(self) -> None:
        sc = self.spark.sparkContext

        # sc._jsc.hadoopConfiguration().set("fs.s3.awsAccessKeyId", access_key)
        # sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", access_key)
        # sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
        # sc._jsc.hadoopConfiguration().set("fs.s3.awsSecretAccessKey", secret_key)
        # sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", secret_key)
        # sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
        # sc._jsc.hadoopConfiguration().set("fs.s3n.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
        # sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        # sc._jsc.hadoopConfiguration().set("fs.s3.impl", "org.apache.hadoop.fs.s3.S3FileSystem")



