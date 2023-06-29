#!/usr/bin/env python

"""
This module contains helpers to instantiate a logging context
"""

__author__ = "Andreas Kreitschmann"
__email__ = "a.kreitschmann@gmail.com"
__copyright__ = "the author, 2023"
__license__ = "MIT"
__version__ = "0.1.0"


from pyspark.sql import SparkSession


class Logger:
    def get_logger(self, spark: SparkSession):
        log4j_logger = spark._jvm.org.apache.log4j
        return log4j_logger.LogManager.getLogger(self.__full_name__())

    def __full_name__(self):
        cls = self.__class__
        module = cls.__module__
        if module == "__builtin__":
            return cls.__name__  # avoid outputs like '__builtin__.str'
        return module + "." + cls.__name__