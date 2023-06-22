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
import sys
import os
from random import random
from operator import add
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame
from pyspark import SparkContext
from pyspark.conf import SparkConf
import boto3


class DataLoader:
    """
    base class for loading and transforming raw data.
    TODO: add interface to load from S3
    """
    spark: SparkSession
    data_path: Path

    def __init__(self, path: Path, source_type: str = "hdfs", s3_bucket=None, s3_prefix=None):
        self.spark: SparkSession = SparkSession.builder.appName("pr_issues_loader").getOrCreate()

        match source_type:
            case "hdfs":
                self.data_path = path
            case "s3":
                if s3_bucket is None or s3_prefix is None:
                    raise FileNotFoundError
                else:
                    self.data_path = Path(f"s3://{s3_bucket}/{s3_prefix}/")

    def load_data(self) -> DataFrame:
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



