#!/usr/bin/env python

import json
import boto3

def lambda_handler(event, context):
    """
    event handlered triggered by S3 put
    """
    return {"statusCode": 200, "body": "Sucess"}


if __name__ == "__main__":
    pass
