output "source_bucket_name" {
  value = aws_s3_bucket.source.bucket
}

output "destination_bucket_name" {
  value = aws_s3_bucket.destination.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.processor.function_name
}
