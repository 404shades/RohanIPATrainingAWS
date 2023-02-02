import boto3


def get_s3_client():
    return boto3.client('s3')


def handler(event, context):
    source_bucket_name = event["Records"][0]['s3']['bucket']['name']
    print(source_bucket_name)
    print(event)
    return "'Hello Lambda'"
