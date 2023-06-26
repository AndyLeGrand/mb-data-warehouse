# mb-data-warehouse
[![Python application](https://github.com/AndyLeGrand/mb-data-warehouse/actions/workflows/python-app.yml/badge.svg)](https://github.com/AndyLeGrand/mb-data-warehouse/actions/workflows/python-app.yml)

## About

This repository contains code and configuration for a pyspark data pipeline using AWS cloud infrastructure

## Maintainer

Andreas Kreitschmann, e-mail: [a.kreitschmann@gmail.com](mailto:a.kreitschmann@gmail.com)

## Background

For an architecture overview and details on the data model, refer to the `docs` folder.

## Building & testing the project

### Build

This project is a python project and can thus be built with standard python tooling.
The tested approaches include: 

    python -m build

Since this application was built to be run on AWS infrastructure, the [aws-emr-cli](https://pypi.org/project/aws-emr-cli/) Python library
offers a convenient alternative for packaging the application:

    emr package --entry-point main.py

Further information on how the second option works in detail, visit this [page](https://aws.amazon.com/de/blogs/big-data/build-deploy-and-run-spark-jobs-on-amazon-emr-with-the-open-source-emr-cli-tool/)

### Test

Tests are implemented using the `pytest` library. As usual, they reside in the `tests` folder.
Execute all tests by running `pytest -vvv` in the projects root directory.

This repo comes with a pre-configured Github actions workflow that executes all tests automatically.
For details see the `.github/workflows` folder.

## How to use the project

This project loads, transforms and writes data using Apache Spark. It can be run locally in standalone mode (during development).
To run the application for production loads, it should be run on a Spark cluster instead.

### Deploy the app

In order to run Spark workloads on AWS (tested with different flavours of the AWS EMR service), artefacts need to be first deployed to a
S3 bucket from which the Spark cluster can read. This can be either achieved manually or using the aws-emr-cli tool mentioned above.
In this repo's CI/CD workflow, a deploy step is included.

You can simply edit the file `.github/workflows/python-app.yml` to adjust the target S3_BUCKET. See steps starting with `Deploy package...`

### Run the app

Once your pyspark package is deployed to S3 (see previous point), you can run the application on any of the available AWS EMR flavours.
For testing, these have been provisioned manually. A future improvement of this package is to include automated provisioning
of infrastructure, e.g. an AWS EMR Serverless instance / application.
Details on the setup of an AWS EMR Serverless application can be found [here](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/getting-started.html)

Once the Spark cluster is available, an easy way to start the Spark is using the aws-emr-cli, like so:

```
    emr run --application-id <your EMR serverless application ID> \
         --job-role <job role created during setup of EMR serverless application>
         --s3-code-uri s3://akreit-dev-bucket/pr_issues_package/master/
         --entry-point main.py
         --job-name pr_issues_transform
         --wait
```

Note that this command can be run from any environment (also from outside of AWS). All you need is to configure the respective
AWS access, e.g. via aws-cli. More on this [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
This can be useful during development e.g. in a local environment.

For productive workloads, a scheduler like Apache Airflow should be used.




