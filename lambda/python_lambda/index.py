import boto3

import os


def get_s3_client():
    """
    Get S3 Client from boto3
    :return:
    """
    return boto3.client('s3')


def copy_file_to_destination(copy_object, file_name):
    """
    Copies file from source bucket to destination bucket with given file name(key)
    :param copy_object: {Bucket:"SOURCE BUCKET NAME", Key: "File to copy"
    :param file_name: File name to be used after copying in destination
    :return:
    """
    destination_bucket_name = os.environ["DESTINATION_BUCKET"]
    return get_s3_client().copy_object(CopySource=copy_object, Bucket=destination_bucket_name, Key=file_name)


def handler(event, context):
    """
    Lambda handler to be called on lambda function trigger
    :param event:
    :param context:
    :return:
    """
    source_bucket_name = event["Records"][0]['s3']['bucket']['name']
    source_object_key = event["Records"][0]['s3']['object']['key']
    copy_object = {'Bucket': source_bucket_name, 'Key': source_object_key}
    print(copy_file_to_destination(copy_object, source_object_key))
    return "'Hello Lambda'"
