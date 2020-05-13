#!/usr/bin/env python

import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

table_name = "cmm.results"
dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
table = dynamodb.Table(table_name)

def query_measurement_point(id):
    response = table.get_item(Key={"id": id})
    if "Item" in response:
        item = response["Item"]
        print(item)

def scan_table(**kwargs):
    queries = []
    for k, v in kwargs.items():
        response = dynamodb_scan(k, v)
        queries.extend(response)
    return [dict(t) for t in {tuple(d.items()) for d in queries}]


def lambda_handler(event, context):
    """
    event handlered triggered by S3 put
    """
    return {"statusCode": 200, "body": "Sucess"}


if __name__ == "__main__":
    measurement_point = "L02A712AHP_X"
    program = "Z02 FRT VAL LH CYC L3"
    date = "10/15/2019"
    id = measurement_point + "-" + program + "-" + date
    #get_measurement_point(id)
    point = "L02A712AHP_X"
    #scan_measurement_points(point)
    #scan_program(program)
    print(scan_table(program_id="Z02 FRT VAL LH CYC L3"))
