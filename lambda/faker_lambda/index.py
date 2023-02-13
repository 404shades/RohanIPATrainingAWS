import json
import os
from faker import Faker
from urllib import parse
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
    """
    Generate fake data using Faker Library
    :return: Dictionary[String:String]
    """
    return {"userName": fake.name(), "address": fake.address(), "email": fake.email(), "description": fake.text()}


def upload_fake_data_to_s3(bucket_name):
    """
    Upload fake data to the destination bucket by creating a file out of fake data
    :param bucket_name: Where to store json files
    :return:
    """
    fake_data = get_fake_data()
    file_name = str(int(time.time())) + ".json"
    tags = {"name": file_name.replace(".json", ""), "user_name": fake_data["userName"]}
    meta_data = {"email": fake_data["email"], "name": file_name.replace(".json", "")}
    with open(f"/tmp/{file_name}", "w") as file:
        json.dump(fake_data, file)
    get_s3_client().upload_file(f"/tmp/{file_name}", bucket_name, file_name,
                                ExtraArgs={"Metadata": meta_data, "Tagging": parse.urlencode(tags)})


def handler(event, context):
    """
    Lambda handler to store fake data to be used for other testing purpose
    :param event:
    :param context:
    :return:
    """
    bucket_name = os.environ["BUCKET_NAME"]
    for i in range(0, 2000):
        upload_fake_data_to_s3(bucket_name)
