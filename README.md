# mb-data-warehouse
[![Python application](https://github.com/AndyLeGrand/mb-data-warehouse/actions/workflows/python-app.yml/badge.svg)](https://github.com/AndyLeGrand/mb-data-warehouse/actions/workflows/python-app.yml)

## About

This repository contains code and configuration for a pyspark data pipeline using AWS cloud infrastructure

## Maintainer

Andreas Kreitschmann, e-mail: [a.kreitschmann@gmail.com](mailto:a.kreitschmann@gmail.com)

## Background

For an architecture overview and details on the data model, refer to the folder docs.

## How to build project

This project is a python project and can thus be built with standard python tooling.
The tested approaches include: 

    python -m build

Since this application was built to be run on AWS infrastructure, the [aws-emr-cli](https://pypi.org/project/aws-emr-cli/) Python library
offers a convenient alternative for packaging the application:

    emr package --entry-point main.py

Further information on how the second option works in detail, visit this [page](https://aws.amazon.com/de/blogs/big-data/build-deploy-and-run-spark-jobs-on-amazon-emr-with-the-open-source-emr-cli-tool/)

## How to use project


