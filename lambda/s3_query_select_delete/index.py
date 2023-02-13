import boto3
import re
import os


def get_s3_client():
    """
    Get S3 Client from boto3
    :return:
    """
    return boto3.client('s3')


def delete_objects_from_bucket(bucket_name: str, object_keys: list):
    client = get_s3_client()
    print(object_keys)
    client.delete_objects(Bucket=bucket_name, Delete={"Objects": [{"Key": key} for key in object_keys]})


def find_objects_by_tag(bucket_name: str, key_name: str, value_pattern: str):
    client = get_s3_client()
    paginator = client.get_paginator("list_objects_v2")
    found_keys = []
    for result in paginator.paginate(Bucket=bucket_name):
        bucket_objects = result.get("Contents", [])
        for obj in bucket_objects:
            object_tags = client.get_object_tagging(Bucket=bucket_name, Key=obj["Key"])
            all_tags = object_tags.get("TagSet", [])
            if len(all_tags) > 0 and any(
                    tag.get("Key") == key_name and re.match(value_pattern, tag.get("Value")) for tag in all_tags):
                found_keys.append(obj.get("Key"))
    return found_keys


def find_objects_by_metadata(bucket_name: str, key_name: str, value_pattern: str):
    client = get_s3_client()
    paginator = client.get_paginator("list_objects_v2")
    found_keys = []
    for result in paginator.paginate(Bucket=bucket_name):
        bucket_objects = result.get("Contents", [])
        for obj in bucket_objects:
            object_meta_data = client.head_object(Bucket=bucket_name, Key=obj["Key"])
            all_meta_tags = object_meta_data.get("Metadata", [])
            if re.match(value_pattern, all_meta_tags.get(key_name)):
                found_keys.append(obj.get("Key"))
    return found_keys


def handler(event, context):
    """
    Lambda Handler to delete objects from bucket using tags and meta data
    :param event:
    :param context:
    :return:
    """
    # find objects if their tag key name is user_name and its value contains ch
    delete_keys_tags = find_objects_by_tag(bucket_name=os.environ["BUCKET_NAME"], key_name="user_name",
                                           value_pattern=".*ch.*")
    # find objects if their metadata email has .org at last
    delete_keys_meta = find_objects_by_metadata(bucket_name=os.environ["BUCKET_NAME"], key_name="email",
                                                value_pattern=".*\.org")
    # delete the objects found above
    delete_objects_from_bucket(bucket_name=os.environ["BUCKET_NAME"], object_keys=delete_keys_meta)
    delete_objects_from_bucket(bucket_name=os.environ["BUCKET_NAME"], object_keys=delete_keys_tags)
    return "Success"


if __name__ == "__main__":
    handler(None, None)
