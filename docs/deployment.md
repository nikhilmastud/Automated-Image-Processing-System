# Deployment and CI/CD

This document describes the deployed AWS image-processing workflow and the Jenkins pipeline used to publish and deploy Lambda container images.

## AWS Resources

- Source S3 bucket with incoming objects under `uploads/`
- Destination S3 bucket with processed objects under `processed/`
- Lambda function: `automated-image-processing-processor`
- ECR repository: `automated-image-processing-processor`
- CloudWatch Logs for Lambda execution
- IAM execution role for Lambda and a separate IAM identity for Jenkins deployment

AWS Region: `ap-south-1`.

## Runtime Deployment Flow

1. An image is uploaded to the source bucket under `uploads/`.
2. S3 emits an object-created event.
3. The Lambda function receives the event and reads the source image.
4. Python/Pillow corrects orientation where applicable, resizes the image, and converts it to JPEG.
5. Lambda writes the processed image to the destination bucket under `processed/`.
6. CloudWatch Logs capture Lambda execution details.

The source and destination buckets are separate to avoid recursive invocation when Lambda writes its output.

## Jenkins CI/CD

The repository's `Jenkinsfile` defines the deployment pipeline:

1. Checkout source from GitHub.
2. Build the Lambda Docker image for `linux/amd64`, with provenance and SBOM attestations disabled for Lambda image compatibility.
3. Authenticate to Amazon ECR using the Jenkins credential ID `aws-ecr-credentials`.
4. Push an immutable build-number-tagged image.
5. Update the Lambda function to the new ECR image and wait for the update to complete.
6. Run an S3 integration test by uploading a generated PNG to the source bucket and polling for its processed JPEG in the destination bucket.

The pipeline reports success only when the deployment stage and S3 integration test both complete successfully.

## Jenkins Credential Setup

Create a Jenkins credential with:

- Kind: Username with password
- ID: `aws-ecr-credentials`
- Username: AWS access key ID
- Password: AWS secret access key

Do not put credentials in the Jenkinsfile or commit them to GitHub.

## IAM Permissions

The Jenkins IAM identity needs permissions for the pipeline operations, scoped to the required resources where possible:

- ECR authentication and image push permissions.
- Lambda update and read permissions for the target function.
- `s3:PutObject` on the source bucket's `uploads/*` prefix for the integration test.
- `s3:GetObject` on the destination bucket's `processed/*` prefix to verify the test output.

The Lambda execution role separately needs access to read source objects, write destination objects, and publish logs.

## Verification Checklist

- [x] Jenkins checks out the intended branch.
- [x] Docker image builds successfully.
- [x] Image is pushed to ECR with the Jenkins build number.
- [x] Lambda update completes and reports a successful update status.
- [x] Jenkins prints `S3 integration test PASSED.`
- [x] The corresponding processed JPEG exists in the destination bucket.
- [x] Lambda logs show successful processing in CloudWatch.

## Operational Notes

- Keep both buckets private and block public access.
- Use least-privilege IAM policies.
- Never commit AWS access keys, secret keys, Terraform state, or real secret variable files.
- Review CloudWatch Logs when the integration test times out or Lambda processing fails.

## Remaining Validation

The verified Jenkins integration test currently exercises a generated PNG fixture only. Before describing the application as fully functionally tested, run and record separate JPEG and WEBP cases, transparent PNG behavior, invalid-file handling, and oversized-image handling. Representative performance and concurrency benchmarks are also pending. Do not mark these as passed without execution evidence.

The Terraform configuration provisions resources from a project-name prefix, while the current Jenkins pipeline targets the deployed bucket names configured in its environment block. When recreating the infrastructure in another AWS account or environment, update the Jenkins bucket configuration from the Terraform outputs before running the pipeline.
