# Rearc Data Quest

## Part 1 – AWS S3 & Sourcing Datasets (BLS)

### Dataset Source
https://download.bls.gov/pub/time.series/pr/

### Public S3 Location
S3 prefix (canonical location):
s3://rearc-quest-thrishika-1234/bls/pr/

Public HTTP examples (downloadable objects):
- https://rearc-quest-thrishika-1234.s3.amazonaws.com/bls/pr/pr.data.0.Current
- https://rearc-quest-thrishika-1234.s3.amazonaws.com/bls/pr/pr.series

Note: Amazon S3 does not provide a browsable directory view by default. Public access is validated using direct object URLs.

### Description
For Part 1, I implemented a Python script that programmatically syncs the BLS PR time-series datasets into Amazon S3.

The script:
- Dynamically discovers available files (no hardcoded filenames)
- Uploads only missing/updated files and skips unchanged ones to avoid duplicate uploads
- Removes files from S3 if they are deleted upstream
- Uses a custom User-Agent to comply with BLS access policies

Script: `src/part1_sync_bls_to_s3.py`

---

## Part 2 – Population API → JSON → S3

For Part 2, population data is fetched from a public US Census API and stored as a JSON object in Amazon S3.

S3 location:
s3://rearc-quest-thrishika-1234/api/population/population.json

Script: `src/part2_fetch_population_api.py`

---

## Part 3 – Analytics Notebook
Notebook: `notebooks/part3_analysis.ipynb`

Outputs included:
- Mean and standard deviation of annual US population for 2013–2018
- Best year per `series_id` (max annual sum of quarterly `value`)
- Joined report for `series_id = PRS30006032`, `period = Q01`, with population (when available)
