import os
import json
import boto3
import requests
from datetime import datetime, timezone

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

API_URL = "https://api.census.gov/data/2019/pep/population"
S3_KEY = "api/population/population.json"

s3 = boto3.client("s3")

# ---------------------------------------------------
# Fetch population data from Census API
# ---------------------------------------------------

def fetch_population():
    params = {
        "get": "NAME,POP",
        "for": "us:*"
    }

    response = requests.get(API_URL, params=params, timeout=60)
    response.raise_for_status()
    return response.json()

# ---------------------------------------------------
# Save JSON to S3
# ---------------------------------------------------

def save_json_to_s3(bucket: str, key: str, data):
    wrapped_payload = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": API_URL,
        "data": data
    }

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(wrapped_payload, indent=2).encode("utf-8"),
        ContentType="application/json"
    )

    print(f"✅ Saved population data to s3://{bucket}/{key}")

# ---------------------------------------------------
# Entry point
# ---------------------------------------------------

if __name__ == "__main__":
    bucket = os.environ["QUEST_BUCKET"]
    population_data = fetch_population()
    save_json_to_s3(bucket, S3_KEY, population_data)

