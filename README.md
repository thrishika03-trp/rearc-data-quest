# Rearc Data Quest

This repository contains an end-to-end data ingestion and analytics pipeline implemented using Python and AWS services. The project focuses on correctness, clarity, and infrastructure-as-code best practices.

## Part 1 — AWS S3 & BLS Time-Series Data Ingestion

For Part 1, BLS PR time-series datasets are programmatically ingested and synchronized into Amazon S3.

Dataset source:
https://download.bls.gov/pub/time.series/pr/

S3 storage location:
s3://rearc-quest-thrishika-1234/bls/pr/

Key characteristics:
- Files are dynamically discovered from the source
- Only new or updated files are uploaded; unchanged files are skipped
- Files removed upstream are also removed from S3
- A custom User-Agent is used to comply with BLS access requirements

## Part 2 — Population API to S3

For Part 2, U.S. population data is retrieved from a public Census API and stored in Amazon S3 as a JSON object.

S3 storage location:
s3://rearc-quest-thrishika-1234/api/population/population.json

## Part 3 — Analytics & Reporting

The analytical component computes insights from the ingested datasets, including population and BLS time-series data.

Outputs include:
- Mean and standard deviation of annual U.S. population for 2013–2018
- Best year per series_id based on maximum annual aggregation
- Joined report for series_id PRS30006032, period Q01, with population data when available

## Infrastructure & Deployment

Infrastructure is defined using AWS CDK (Python) and includes:
- Amazon S3
- AWS Lambda
- Amazon SQS

The infrastructure definition successfully synthesizes using `cdk synth`.

Deployment using `cdk deploy` is blocked due to restricted IAM permissions on the provided AWS user. Specifically, permission to read the CDK bootstrap version from AWS Systems Manager Parameter Store (`ssm:GetParameter`) is required.

## Summary

- End-to-end data ingestion and analytics pipeline implemented
- Infrastructure defined using Infrastructure-as-Code principles
- Deployment readiness validated through successful CDK synthesis
- IAM permission constraints clearly identified and documented
