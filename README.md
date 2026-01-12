Part 1 — AWS S3 & BLS Time-Series Data Ingestion
Dataset Source

U.S. Bureau of Labor Statistics (BLS) – PR Time Series
https://download.bls.gov/pub/time.series/pr/

Public S3 Location

Canonical S3 prefix:

s3://rearc-quest-thrishika-1234/bls/pr/


Public HTTP object examples (direct access):

https://rearc-quest-thrishika-1234.s3.amazonaws.com/bls/pr/pr.data.0.Current

https://rearc-quest-thrishika-1234.s3.amazonaws.com/bls/pr/pr.series

Note: Amazon S3 does not provide a browsable directory listing by default. Public access is validated using direct object URLs.

Description

For Part 1, I implemented a Python-based ingestion pipeline that synchronizes the BLS PR time-series datasets into Amazon S3.

The script performs the following:

Dynamically discovers available files from the BLS source (no hardcoded filenames)

Uploads only new or modified files and skips unchanged files to prevent duplicate uploads

Deletes objects from S3 if they are removed from the upstream source

Uses a custom User-Agent header to comply with BLS access policies

Script:

src/part1_sync_bls_to_s3.py

Part 2 — Population API → JSON → S3

For Part 2, U.S. population data is retrieved from a public Census API and stored in Amazon S3 as a JSON object.

S3 location:

s3://rearc-quest-thrishika-1234/api/population/population.json


Script:

src/part2_fetch_population_api.py

Part 3 — Analytics Notebook

Notebook:

notebooks/part3_analysis.ipynb

Outputs & Analysis

The notebook produces the following analytical results:

Mean and standard deviation of annual U.S. population for the years 2013–2018

Best year per series_id, defined as the year with the maximum annual sum of quarterly values

Joined analytical report for:

series_id = PRS30006032

period = Q01

Population data included when available
