# Automated Image Processing System

A serverless, event-driven image processing system that automatically resizes, compresses, and converts uploaded images using Amazon S3, AWS Lambda, Python/Pillow, IAM, and CloudWatch.

## Architecture

~~~mermaid
flowchart LR
    U[User / Application] -->|Upload| S1[(Amazon S3 - Source Bucket)]
    S1 -->|ObjectCreated| L[AWS Lambda - Image Processor]
    L -->|Processed Image| S2[(Amazon S3 - Destination Bucket)]
    L --> CW[Amazon CloudWatch - Logs]
    IAM[AWS IAM - Least Privilege] -.-> L
~~~

## Image Processing Tasks

- Resize images while preserving aspect ratio
- Compress images as optimized JPEG
- Convert supported input images to JPEG
- Store processed images separately from uploads

## How It Works

1. User uploads an image to the source S3 bucket under the uploads prefix.
2. S3 emits an ObjectCreated event.
3. AWS Lambda receives the event and downloads the image.
4. Python/Pillow resizes and compresses the image.
5. Lambda stores the processed image in the destination S3 bucket under the processed prefix.
6. CloudWatch captures execution logs.

AWS documentation recommends filtering S3 events or separating input/output storage when Lambda writes objects back to S3, to avoid recursive invocation.

## AWS Services

| Service | Purpose |
|---|---|
| Amazon S3 | Source and processed image storage |
| AWS Lambda | Serverless image processing |
| Amazon CloudWatch | Logs and monitoring |
| AWS IAM | Least-privilege access |
| Terraform | Infrastructure as Code |
| Docker / ECR | Lambda container packaging |

## Repository Structure

~~~text
.
├── lambda/
│   ├── lambda_function.py
│   ├── requirements.txt
│   └── Dockerfile
├── infrastructure/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── architecture/
│   └── architecture.md
├── docs/
│   ├── deployment.md
│   └── interview.md
├── .gitignore
└── README.md
~~~

## Current Status

Application logic, architecture documentation, Terraform foundation, security configuration, and interview preparation are added.

AWS deployment is the next phase. Real processing metrics and screenshots will be added only after testing the deployed system.
