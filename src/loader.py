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

from typing import List, Optional
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame


class DataLoader:
    """
    base class for loading and transforming raw data.
    """
    spark: DataFrame
    data_path: Path

    def __init__(self, path: Path):
        self.spark: SparkSession = SparkSession.builder.appName("data_loader").getOrCreate()
        self.data_path = path

    def load_data(self, path: Path) -> DataFrame:
        return (self.spark
                .read
                .option("multiline", "true")
                .option("inferSchema", "true")
                .json(str(path))
                )

    @staticmethod
    def select_from_df(df: DataFrame, cols: List[str]) -> DataFrame:
        """
        Selects a subset of columns (cols) from df
        :param df: input dataframe
        :param cols: a list of column expressions; see documentation of pyspark.sql.dataframe.DataFram.select Expr
        :return: resulting dataframe after applying selectExpr(*cols) to the input data
        """
        return df.selectExpr(*cols)
