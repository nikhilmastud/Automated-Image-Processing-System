import io
import logging
import os
import time
from urllib.parse import unquote_plus

import boto3
from PIL import Image

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]
DESTINATION_PREFIX = os.environ.get("DESTINATION_PREFIX", "processed/")
MAX_WIDTH = int(os.environ.get("MAX_WIDTH", "1280"))
MAX_HEIGHT = int(os.environ.get("MAX_HEIGHT", "1280"))
JPEG_QUALITY = int(os.environ.get("JPEG_QUALITY", "85"))


def process_image(data: bytes) -> bytes:
    with Image.open(io.BytesIO(data)) as image:
        image = image.convert("RGB")
        image.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=JPEG_QUALITY, optimize=True)
        return output.getvalue()


def lambda_handler(event, context):
    started = time.time()
    processed = 0

    for record in event.get("Records", []):
        source_bucket = record["s3"]["bucket"]["name"]
        source_key = unquote_plus(record["s3"]["object"]["key"])

        if not source_key.startswith("uploads/"):
            logger.info("Skipping object outside uploads/: %s", source_key)
            continue

        logger.info("Processing s3://%s/%s", source_bucket, source_key)
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        original = response["Body"].read()
        processed_image = process_image(original)

        filename = os.path.basename(source_key)
        stem, _ = os.path.splitext(filename)
        destination_key = f"{DESTINATION_PREFIX}{stem}-processed.jpg"

        s3.put_object(
            Bucket=DESTINATION_BUCKET,
            Key=destination_key,
            Body=processed_image,
            ContentType="image/jpeg",
        )

        logger.info(
            "Processed %s bytes -> %s bytes; destination=s3://%s/%s",
            len(original), len(processed_image), DESTINATION_BUCKET, destination_key
        )
        processed += 1

    duration_ms = round((time.time() - started) * 1000, 2)
    logger.info("Completed: count=%s duration_ms=%s", processed, duration_ms)

    return {"statusCode": 200, "processed": processed, "duration_ms": duration_ms}
