import boto3

import os


def get_s3_client():
    return boto3.client('s3')


def copy_file_to_destination(copy_object, file_name):
    destination_bucket_name = os.environ["DESTINATION_BUCKET"]
    return get_s3_client().copy_object(CopySource=copy_object, Bucket=destination_bucket_name, Key=file_name)


def handler(event, context):
    source_bucket_name = event["Records"][0]['s3']['bucket']['name']
    source_object_key = event["Records"][0]['s3']['object']['key']
    copy_object = {'Bucket': source_bucket_name, 'Key': source_object_key}
    print(copy_file_to_destination(copy_object, source_object_key))
    return "'Hello Lambda'"
