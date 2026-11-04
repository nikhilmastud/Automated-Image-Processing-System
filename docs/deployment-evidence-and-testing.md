# Deployment Evidence and Test Results

This directory documents reproducible deployment evidence and measured test results for the Automated Image Processing System.

## Verified deployment evidence

The following items were verified from Jenkins Build #8 console output on 4 November 2026:

- GitHub checkout completed.
- Lambda container image built for `linux/amd64`.
- Image tag `:8` was pushed to the project's Amazon ECR repository.
- Lambda `automated-image-processing-processor` update completed with status `Successful`.
- Jenkins uploaded `uploads/ci-test-8.png` to the source S3 bucket.
- The processed object `processed/ci-test-8-processed.jpg` appeared in the destination S3 bucket.
- The integration test reported `S3 integration test PASSED.`
- Output metadata reported Content-Type `image/jpeg` and Content-Length `285` bytes.
- Jenkins build result was `SUCCESS`.

These are deployment/integration checks, not a performance benchmark.

## Evidence screenshots

Sanitized screenshots are organized in [`docs/evidence/`](evidence/README.md). The folder README lists the expected filenames. Confirm each image is present in the repository before treating the evidence package as complete.

1. `jenkins-build-8-success.png` — Jenkins console showing final successful stages and `Finished: SUCCESS`.
2. `ecr-image-tag-8.png` — ECR repository showing image tag `:8` and digest.
3. `lambda-deployed-image.png` — Lambda function showing package type Image and deployed image details.
4. `s3-source-test-object.png` — source bucket object `uploads/ci-test-8.png`.
5. `s3-processed-test-object.png` — destination bucket object `processed/ci-test-8-processed.jpg`.
6. `cloudwatch-build-8-log.png` — CloudWatch log event for the processing invocation.

Before committing screenshots, redact account-sensitive details if desired and never include access keys, secret keys, session tokens, credentials, or personal information.

## Test results

| Test | Result | Evidence / measurement |
|---|---|---|
| Jenkins CI/CD deployment | PASS | Build #8 console output |
| ECR image push | PASS | Build #8 pushed tag `:8` |
| Lambda code/image update | PASS | Lambda update waiter completed; status Successful |
| S3 event-driven integration | PASS | Output object appeared in destination bucket |
| Output format | PASS | `image/jpeg` |
| Output size | PASS | 285 bytes for the 1x1 CI fixture only |
| CloudWatch log verification | PASS | Build #8 invocation log; processed=1, skipped=0; processing 147.64 ms; execution 149.83 ms; max memory 95 MB; cold-start init 3,133.76 ms |
| Multi-format functional tests | Pending | Record separate JPEG, PNG, WEBP results |
| Invalid/oversized input tests | Pending | Record expected skip/rejection behavior |
| Performance benchmark | Pending | Measure with representative images and repeated runs |
| Concurrent-load test | Pending | Measure only after defining safe test volume |

## Performance measurement rules

Do not report invented throughput, latency, success-rate, or concurrency figures. The 285-byte output above is only the generated 1x1 PNG CI fixture; it is not representative of normal images.

For a defensible benchmark, record:
- Test date, AWS region, Lambda memory, and timeout.
- Input format, dimensions, and file size for each test image.
- Number of successful, failed, and skipped images.
- End-to-end upload-to-output latency for each run.
- p50 and p95 latency across repeated runs.
- Output file size and dimensions.
- Cold-start versus warm-invocation observations where available.

Keep benchmark inputs and results reproducible. Do not run high-volume or concurrent tests against production resources without checking AWS quotas, expected cost, and cleanup requirements first.
