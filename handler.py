#!/usr/bin/env python
import json
from collections import Counter
from itertools import chain

import boto3
from boto3.dynamodb.conditions import Attr, Key

table_name = "cmm.results"
dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")
table = dynamodb.Table(table_name)


def scan_params(kwargs):
    """
    scans table based on provided
    k,v args and returns results
    """
    queries = []
    for k, v in kwargs.items():
        response = table.scan(FilterExpression=Attr(k).eq(v))
        items = response["Items"]
        queries.append(items)
    # intersect query calc returns common dicts in lists of dicts
    intersect_query = [
        dict(k)
        for k, v in Counter(
            frozenset(x.items()) for x in chain.from_iterable(queries)
        ).items()
        if v > 1
    ]
    return intersect_query


def scan_table(**kwargs):
    if kwargs:
        return scan_params(kwargs)
    else:
        return table.scan()["Items"]


def lambda_handler(event, context):
    """
    event handlered triggered by API GW
    """
    # program_id=Z02 FRT VAL LH CYC L3&point=L02A712AHP_Y
    if event["queryStringParameters"]:
        results = scan_table(**event["queryStringParameters"])
        results_json = json.dumps(results)
        return {"statusCode": 200, "body": results_json}
    else:
        return {"statusCode": 404, "body": "QueryError: Provide query parameters"}


if __name__ == "__main__":
    queries = {"program_id": "Z02 FRT VAL LH CYC L3", "point": "L02A712AHP_Y"}
    results = scan_table(**queries)
    print(json.dumps(results))
