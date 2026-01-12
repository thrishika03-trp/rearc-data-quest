# Rearc Data Quest

## Part 1 – AWS S3 & Sourcing Datasets

### Dataset Source
https://download.bls.gov/pub/time.series/pr/

### Public S3 Location
https://rearc-quest-thrishika-1234.s3.amazonaws.com/bls/pr/

### Description
For Part 1, I implemented a Python script that programmatically syncs the BLS PR time-series datasets into Amazon S3.

The script:
- Dynamically discovers available files (no hardcoded filenames)
- Uploads new or changed files
- Skips unchanged files to avoid duplicate uploads
- Removes files from S3 if they are deleted upstream
- Uses a custom User-Agent to comply with BLS data access policies

Script: `src/part1_sync_bls_to_s3.py`

