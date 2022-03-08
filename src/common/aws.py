import os

import boto3


def client(resource):
    return boto3.client(resource, region_name=os.environ['AWS_DEFAULT_REGION'])