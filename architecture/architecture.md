# Architecture

~~~mermaid
flowchart LR
    U[User / Application] -->|Upload image| S1[(Amazon S3 - Source)]
    S1 -->|ObjectCreated event| L[AWS Lambda - Image Processor]
    L -->|Processed JPEG| S2[(Amazon S3 - Destination)]
    L --> CW[Amazon CloudWatch - Logs]
    IAM[AWS IAM - Least Privilege] -.-> L
~~~

## Processing Tasks

- Resize while preserving aspect ratio
- Compress as optimized JPEG
- Convert supported inputs to JPEG
- Store processed files separately from uploads

## Flow

1. Upload to source bucket.
2. S3 sends an ObjectCreated event.
3. Lambda reads the image.
4. Pillow resizes and compresses it.
5. Lambda writes the result to the destination bucket.
6. CloudWatch records execution logs.

Separate source and destination storage prevents recursive S3-to-Lambda invocation.
