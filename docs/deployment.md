# Deployment Plan

Deployment will be performed after the application and repository work is complete.

## Planned Resources

- Source S3 bucket
- Destination S3 bucket
- Lambda function
- IAM execution role
- S3 event notification
- Lambda invoke permission
- CloudWatch log group
- ECR repository for the Lambda container image

## Deployment Order

1. Build and test the Lambda container.
2. Push the image to Amazon ECR.
3. Deploy infrastructure with Terraform.
4. Upload a test image to the source bucket.
5. Verify the processed image in the destination bucket.
6. Check Lambda execution logs in CloudWatch.
7. Test invalid files and failure scenarios.
8. Add CI/CD after the core workflow is verified.

## Security

- Keep buckets private.
- Enable S3 public-access blocking.
- Enable server-side encryption.
- Use least-privilege IAM.
- Never commit AWS credentials or Terraform state.
