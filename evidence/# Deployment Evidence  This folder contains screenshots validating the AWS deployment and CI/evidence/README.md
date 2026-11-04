# Deployment Evidence

This folder contains screenshots validating the AWS deployment and CI/CD pipeline.

## Evidence Files

1. `jenkins-build-8-success.png` – Jenkins pipeline completed successfully.
2. `ecr-image-tag-8.png` – Docker image tag 8 pushed to Amazon ECR.
3. `lambda-deployed-image.png` – Lambda deployed using the ECR image.
4. `s3-source-test-object.png` – Test PNG uploaded to the source bucket.
5. `s3-processed-test-object.png` – Processed JPEG generated in the destination bucket.
6. `cloudwatch-build-8-log.png` – Lambda execution logs and metrics.

## Verified Result

- Jenkins Build: SUCCESS (#8)
- ECR Push: SUCCESS
- Lambda Deployment: SUCCESS
- S3 Integration Test: PASSED
- Lambda Processing Duration: 147.64 ms
- Lambda Execution Duration: 149.83 ms
- Maximum Memory Used: 95 MB

Note: These metrics are from a 1x1 pixel CI test image, not a performance benchmark.
