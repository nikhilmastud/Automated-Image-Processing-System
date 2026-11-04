pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPOSITORY = 'automated-image-processing-processor'
        LAMBDA_FUNCTION = 'automated-image-processing-processor'
        SOURCE_BUCKET = 'automated-image-processing-source-065bff4abbbeef74507fc0cb5f'
        DESTINATION_BUCKET = 'automated-image-processing-dest-21a6e17e6604686cfb5e733809'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Deploy') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-ecr-credentials',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    sh '''
                        set -e

                        export AWS_DEFAULT_REGION="$AWS_REGION"

                        AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
                        ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                        IMAGE_URI="${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}"

                        echo "Building Lambda-compatible Docker image..."
                        docker build \
                            --platform linux/amd64 \
                            --provenance=false \
                            --sbom=false \
                            -t "$IMAGE_URI" ./lambda

                        echo "Logging in to ECR..."
                        aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_REGISTRY"

                        echo "Pushing image to ECR..."
                        docker push "$IMAGE_URI"

                        echo "Updating Lambda..."
                        aws lambda update-function-code \
                            --function-name "$LAMBDA_FUNCTION" \
                            --image-uri "$IMAGE_URI" \
                            --region "$AWS_REGION"

                        aws lambda wait function-updated \
                            --function-name "$LAMBDA_FUNCTION" \
                            --region "$AWS_REGION"

                        echo "Verifying deployment..."
                        aws lambda get-function \
                            --function-name "$LAMBDA_FUNCTION" \
                            --region "$AWS_REGION" \
                            --query 'Configuration.[FunctionName,LastUpdateStatus,PackageType]' \
                            --output table

                        echo "Deployment completed: $IMAGE_URI"
                    '''
                }
            }
        }

        stage('S3 Integration Test') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-ecr-credentials',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    sh '''
                        set -eu
                        export AWS_DEFAULT_REGION="$AWS_REGION"

                        TEST_NAME="ci-test-${BUILD_NUMBER}"
                        SOURCE_KEY="uploads/${TEST_NAME}.png"
                        DESTINATION_KEY="processed/${TEST_NAME}-processed.jpg"

                        echo "Creating a small valid PNG test image..."
                        printf '%s' 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=' | base64 -d > /tmp/"${TEST_NAME}".png

                        echo "Uploading test image to source S3 bucket..."
                        aws s3 cp /tmp/"${TEST_NAME}".png "s3://${SOURCE_BUCKET}/${SOURCE_KEY}" --content-type image/png

                        echo "Waiting for Lambda to create the processed image..."
                        for attempt in $(seq 1 30); do
                            if aws s3api head-object \
                                --bucket "$DESTINATION_BUCKET" \
                                --key "$DESTINATION_KEY" >/dev/null 2>&1; then
                                echo "S3 integration test PASSED."
                                echo "Processed object: s3://${DESTINATION_BUCKET}/${DESTINATION_KEY}"
                                aws s3api head-object \
                                    --bucket "$DESTINATION_BUCKET" \
                                    --key "$DESTINATION_KEY" \
                                    --query '[ContentType,ContentLength]' \
                                    --output table
                                exit 0
                            fi
                            sleep 2
                        done

                        echo "S3 integration test FAILED: processed image was not found within 60 seconds."
                        exit 1
                    '''
                }
            }
        }
    }
}
