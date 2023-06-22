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

from pathlib import Path
from pyspark.sql import SparkSession, DataFrame


class DataLoader:
    """
    base class for loading and transforming raw data.
    TODO: add interface to load from S3
    """
    spark: DataFrame
    data_path: Path

    def __init__(self, path: Path):
        self.spark: SparkSession = SparkSession.builder.appName("data_loader").getOrCreate()
        self.data_path = path

    def load_data(self) -> DataFrame:
        return (self.spark
                .read
                .option("multiline", "true")
                .option("inferSchema", "true")
                .json(str(self.data_path))
                )
