variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "automated-image-processing"
}

variable "lambda_image_uri" {
  description = "ECR image URI for Lambda"
  type        = string
}
