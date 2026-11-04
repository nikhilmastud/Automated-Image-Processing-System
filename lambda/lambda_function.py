import io
import logging
import os
import posixpath
import time
import warnings
from urllib.parse import unquote_plus

import boto3
from PIL import Image, ImageOps, UnidentifiedImageError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]
DESTINATION_PREFIX = os.environ.get("DESTINATION_PREFIX", "processed/").strip("/")
DESTINATION_PREFIX = f"{DESTINATION_PREFIX}/" if DESTINATION_PREFIX else ""

MAX_WIDTH = int(os.environ.get("MAX_WIDTH", "1280"))
MAX_HEIGHT = int(os.environ.get("MAX_HEIGHT", "1280"))
JPEG_QUALITY = int(os.environ.get("JPEG_QUALITY", "85"))
MAX_INPUT_BYTES = int(os.environ.get("MAX_INPUT_BYTES", "10485760"))
MAX_IMAGE_PIXELS = int(os.environ.get("MAX_IMAGE_PIXELS", "25000000"))

SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}

if MAX_WIDTH <= 0 or MAX_HEIGHT <= 0:
    raise ValueError("MAX_WIDTH and MAX_HEIGHT must be positive")

if not 1 <= JPEG_QUALITY <= 95:
    raise ValueError("JPEG_QUALITY must be between 1 and 95")

if MAX_INPUT_BYTES <= 0 or MAX_IMAGE_PIXELS <= 0:
    raise ValueError("Image size limits must be positive")

Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS


def process_image(data: bytes) -> bytes:
    """Validate, orient, resize and convert an image to optimized JPEG."""

    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)

        try:
            with Image.open(io.BytesIO(data)) as image:
                if image.format not in SUPPORTED_FORMATS:
                    raise ValueError(
                        f"Unsupported image format: {image.format}"
                    )

                image.load()
                image = ImageOps.exif_transpose(image)

                has_transparency = (
                    "A" in image.getbands()
                    or "transparency" in image.info
                )

                if has_transparency:
                    image = image.convert("RGBA")
                    background = Image.new(
                        "RGBA", image.size, (255, 255, 255, 255)
                    )
                    image = Image.alpha_composite(
                        background, image
                    ).convert("RGB")
                else:
                    image = image.convert("RGB")

                image.thumbnail(
                    (MAX_WIDTH, MAX_HEIGHT),
                    Image.Resampling.LANCZOS
                )

                output = io.BytesIO()
                image.save(
                    output,
                    format="JPEG",
                    quality=JPEG_QUALITY,
                    optimize=True
                )

                return output.getvalue()

        except (
            UnidentifiedImageError,
            OSError,
            Image.DecompressionBombError,
            Image.DecompressionBombWarning
        ) as exc:
            raise ValueError(f"Invalid or unsafe image: {exc}") from exc


def lambda_handler(event, context):
    started = time.time()
    processed = 0
    skipped = 0

    records = event.get("Records", [])

    if not records:
        logger.warning("No S3 records found in event")
        return {
            "statusCode": 200,
            "processed": 0,
            "skipped": 0
        }

    for record in records:
        source_bucket = record["s3"]["bucket"]["name"]
        source_key = unquote_plus(record["s3"]["object"]["key"])

        if not source_key.startswith("uploads/"):
            logger.info("Skipping object outside uploads/: %s", source_key)
            skipped += 1
            continue

        logger.info(
            "Processing s3://%s/%s",
            source_bucket,
            source_key
        )

        response = s3.get_object(
            Bucket=source_bucket,
            Key=source_key
        )

        content_length = response.get("ContentLength", 0)

        if content_length > MAX_INPUT_BYTES:
            logger.warning(
                "Skipping oversized image: key=%s size=%s",
                source_key,
                content_length
            )
            skipped += 1
            continue

        original = response["Body"].read()

        if len(original) > MAX_INPUT_BYTES:
            logger.warning("Skipping oversized image after read: %s", source_key)
            skipped += 1
            continue

        try:
            processed_image = process_image(original)
        except ValueError as exc:
            logger.warning(
                "Skipping invalid image: key=%s reason=%s",
                source_key,
                exc
            )
            skipped += 1
            continue

        relative_key = source_key[len("uploads/"):]
        stem, _ = posixpath.splitext(relative_key)

        destination_key = (
            f"{DESTINATION_PREFIX}{stem}-processed.jpg"
        )

        s3.put_object(
            Bucket=DESTINATION_BUCKET,
            Key=destination_key,
            Body=processed_image,
            ContentType="image/jpeg"
        )

        logger.info(
            "Image processed: input_bytes=%s output_bytes=%s "
            "destination=s3://%s/%s",
            len(original),
            len(processed_image),
            DESTINATION_BUCKET,
            destination_key
        )

        processed += 1

    duration_ms = round((time.time() - started) * 1000, 2)

    logger.info(
        "Execution completed: processed=%s skipped=%s duration_ms=%s",
        processed,
        skipped,
        duration_ms
    )

    return {
        "statusCode": 200,
        "processed": processed,
        "skipped": skipped,
        "duration_ms": duration_ms
    }
