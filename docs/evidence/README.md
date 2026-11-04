# Deployment Evidence

This folder contains screenshots validating the AWS deployment and CI/CD pipeline.

## Evidence screenshots

- `jenkins-build-8-success.png` — Jenkins Build #8.
- `ecr-image-tag-8.png` — Amazon ECR private registry repository and images.
- `lambda-deployed-image.png` — Lambda function using the ECR image.
- `s3-source-test-object.png` — S3 source bucket upload.
- `s3-processed-test-object.png` — S3 processed output folder.
- `cloudwatch-build-8-log.png` — CloudWatch log events for image processing.

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

A screenshot that contained sensitive credential information was removed from this folder. Never commit access keys, secret keys, session tokens, passwords, or other credentials.
