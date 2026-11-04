
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
    }
}
