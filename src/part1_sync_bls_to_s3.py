import os
import boto3
import requests

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

BLS_URL = "https://download.bls.gov/pub/time.series/pr/"
S3_PREFIX = "bls/pr/"

s3 = boto3.client("s3")


# ---------------------------------------------------
# Identify ourselves to BLS (avoids 403 errors)
# ---------------------------------------------------

def get_headers():
    return {
        "User-Agent": "RearcQuest/1.0 (contact: thrishika@email.com)"
    }


# ---------------------------------------------------
# Get list of BLS files (FINAL, WORKING LOGIC)
# ---------------------------------------------------

def get_bls_files():
    response = requests.get(BLS_URL, headers=get_headers(), timeout=60)
    response.raise_for_status()

    files = []

    # Filenames appear inside HTML anchor tags: >pr.xxx<
    for part in response.text.split(">"):
        if "<" in part:
            name = part.split("<")[0].strip()
            if name.startswith("pr."):
                files.append(name)

    if not files:
        raise Exception("No BLS files found")

    return sorted(files)


# ---------------------------------------------------
# Check if file exists in S3
# ---------------------------------------------------

def s3_exists(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except:
        return False


# ---------------------------------------------------
# Upload only if missing
# ---------------------------------------------------

def upload_file(bucket, filename):
    s3_key = f"{S3_PREFIX}{filename}"
    url = f"{BLS_URL}{filename}"

    if s3_exists(bucket, s3_key):
        print(f"SKIPPED: {filename}")
        return False

    print(f"UPLOADING: {filename}")
    r = requests.get(url, headers=get_headers(), stream=True)
    r.raise_for_status()

    s3.upload_fileobj(r.raw, bucket, s3_key)
    return True


# ---------------------------------------------------
# Remove files deleted upstream
# ---------------------------------------------------

def cleanup_removed_files(bucket, valid_files):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=S3_PREFIX)

    if "Contents" not in response:
        return

    valid_keys = {f"{S3_PREFIX}{f}" for f in valid_files}

    for obj in response["Contents"]:
        if obj["Key"] not in valid_keys:
            print(f"DELETING: {obj['Key']}")
            s3.delete_object(Bucket=bucket, Key=obj["Key"])


# ---------------------------------------------------
# Main sync logic
# ---------------------------------------------------

def sync_bls_to_s3(bucket):
    bls_files = get_bls_files()

    uploaded = 0
    for f in bls_files:
        if upload_file(bucket, f):
            uploaded += 1

    cleanup_removed_files(bucket, bls_files)

    print("\nSYNC COMPLETE")
    print(f"Files on BLS : {len(bls_files)}")
    print(f"Uploaded    : {uploaded}")


# ---------------------------------------------------
# Entry point
# ---------------------------------------------------

if __name__ == "__main__":
    bucket_name = os.environ["QUEST_BUCKET"]
    sync_bls_to_s3(bucket_name)
