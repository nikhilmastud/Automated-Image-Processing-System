# Deployment Evidence

This folder contains screenshots validating the AWS deployment and CI/CD pipeline.

## Evidence screenshots

- `jenkins-build-8-success.png` — Jenkins Build #8 console showing `S3 integration test PASSED` and `Finished: SUCCESS`.
- `ecr-image-tag-8.png` — Amazon ECR image tag `:8` and digest.
- `lambda-deployed-image.png` — Lambda function deployed from the ECR image.
- `s3-source-test-object.png` — source object `uploads/ci-test-8.png`.
- `s3-processed-test-object.png` — destination object `processed/ci-test-8-processed.jpg`.
- `cloudwatch-build-8-log.png` — CloudWatch execution log and REPORT metrics.

## Verified Build #8 results

- Jenkins pipeline: SUCCESS.
- ECR image push: SUCCESS.
- Lambda image update: SUCCESS.
- S3 integration test: PASSED.
- Processed output Content-Type: `image/jpeg`.
- Processed output size: 285 bytes (1x1 CI fixture only).
- Application processing duration: 147.64 ms.
- Lambda execution duration: 149.83 ms.
- Billed duration: 3,284 ms.
- Maximum memory used: 95 MB (1,024 MB allocated).
- Cold-start initialization: 3,133.76 ms.

**Measurement note:** These values come from a tiny 1x1 pixel CI test image. They are execution evidence, not a representative performance benchmark.

Before uploading screenshots, ensure they contain no access keys, secret keys, session tokens, credentials, or other sensitive information.
