import json
import os
from faker import Faker
import boto3
import time

fake = Faker()


def get_s3_client():
    """
    Get S3 Client from boto3
    :return:
    """
    return boto3.client('s3')


def get_fake_data():
    return {"userName": fake.name(), "address": fake.address(), "email": fake.email(), "description": fake.text()}


def upload_fake_data_to_s3(bucket_name):
    fake_data = get_fake_data()
    file_name = str(int(time.time())) + ".json"
    tags = {"name": file_name.replace(".json", ""), "user_name": fake_data["userName"]}
    meta_data = {"key1": "value1", "key2": "value2"}
    with open(f"/tmp/${file_name}", "w") as file:
        json.dump(fake_data, file)
    get_s3_client().upload_file(f"/tmp/${file_name}", bucket_name, file_name,
                                ExtraArgs={"Metadata": meta_data, "Tagging": tags})


def handler(event, context):
    bucket_name = os.environ["BUCKET_NAME"]
    for i in range(0, 4500):
        upload_fake_data_to_s3(bucket_name)
