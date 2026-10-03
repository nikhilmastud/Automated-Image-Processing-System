# Interview Explanation

## 60-second answer

“I built an event-driven image processing system using Amazon S3 and AWS Lambda. When a user uploads an image to the source S3 bucket, an Object Created event invokes a Lambda function. The function uses Python and Pillow to resize and compress the image, then stores the processed JPEG in a separate destination S3 bucket. CloudWatch is used for logs and monitoring, while IAM controls the Lambda permissions. This project helped me understand serverless architecture, event-driven processing, S3 integration, IAM, and monitoring.”

## Cross Questions

1. What triggers Lambda?
An Amazon S3 ObjectCreated event notification.

2. Why Lambda?
It is serverless and well suited to event-driven workloads because compute runs when an event occurs.

3. Why two S3 buckets?
One receives uploads and the other stores processed files. This also prevents recursive trigger loops.

4. How are permissions handled?
The Lambda execution role follows least privilege: read source objects, write processed objects, and write CloudWatch logs.

5. How do you handle large images?
Memory and timeout can be tuned. For high-volume or very large workloads, SQS or a container-based processing architecture can be introduced.

6. How can it be improved?
Add SQS buffering, SNS notifications, more image formats, retries/dead-letter handling, and CI/CD.
