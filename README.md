![cf workflow](https://github.com/404shades/RohanIPATrainingAWS/actions/workflows/deploy-ci-cd.yml/badge.svg)

# Week1
- Create Cloud Formation Template for event based trigger on s3 using lambda function. Whenever a new object is inserted in s3 bucket it should trigger the lambda and copy the newly inserted object to another bucket as backup

## Resources Created
- Lambda Function
- Source Bucket
- Destination
- IAM Role
- Notification Trigger on S3 Bucket

## CI/CD Stages
- Checkout 
- Configure Credentials using GitHub Secrets
- Create Artifactory Bucket to store lambda code (Python)
- Package Cloud formation resources such as lambda code to store it into the bucket created in last step
- Lint Cloud Formation template to validate errors before deploying
- Deploy Cloud Formation Stack to AWS

## Lambda Function
Lambda function written in python which is event source mapped with source bucket in s3. Whenever a new object is created this lambda function will be triggered to copy the new object to the given destination bucket in s3


# Week 2
- Create Lambda function to delete objects from s3 bucket based upon its meta data and tags

## Resources Created
- Lambda Function (Faker to generate fake data and store it as files with tags and meta data attached to s3 bucket)
- Lambda Function (S3QuerySelectorAndDestroyer to delete objects based on regex pattern of their tags/meta data values)
- Lambda layer to store common python dependencies

## CI/CD Stages
- Added a new stage to package python dependencies using pip install


