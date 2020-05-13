import os
import boto3
import pytest
from moto import mock_dynamodb2

from handler import scan_table

class TestHandler:
    
    @mock_dynamodb2
    def test_scan_params(self):
        # moto needs these:
        os.environ["AWS_ACCESS_KEY_ID"] = "foo"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "bar"
        os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
        table_name = "cmm.results"
        dynamodb = boto3.resource("dynamodb", region_name="eu-west-1")

        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"},],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"},],
        )

        sample_data = [
            {
                "lsl": {"S": "-696.5"},
                "z": {"S": "1268"},
                "time": {"S": "10:20:00"},
                "dev": {"S": "0.044"},
                "y": {"S": "-695"},
                "id": {"S": "L02A712AHP_Y-Z02 FRT VAL LH CYC L3-06/13/2019"},
                "actual": {"S": "-694.956"},
                "point": {"S": "L02A712AHS_Y"},
                "i": {"S": "0"},
                "x": {"S": "2127.5"},
                "k": {"S": "0"},
                "filename": {"S": "ACCUM_008"},
                "usp": {"S": "-693.5"},
                "date": {"S": "06/13/2019"},
                "nominal": {"S": "-695"},
                "j": {"S": "0"},
                "part_number": {"S": "UNDERBODY"},
                "program_id": {"S": "Z02 FRT VAL LH CYC L3"},
            },
            {
                "lsl": {"S": "-696.5"},
                "z": {"S": "1268"},
                "id": {"S": "L02A712AHP_Y-Z02 FRT VAL LH CYC L3-07/11/2019"},
                "y": {"S": "-695"},
                "actual": {"S": "-694.834"},
                "point": {"S": "L02A712AHP_Y"},
                "i": {"S": "0"},
                "x": {"S": "2127.5"},
                "k": {"S": "0"},
                "filename": {"S": "ACCUM_014"},
                "usp": {"S": "-693.5"},
                "dev": {"S": "0.166"},
                "date": {"S": "07/11/2019"},
                "time": {"S": "21:47:00"},
                "nominal": {"S": "-695"},
                "j": {"S": "0"},
                "part_number": {"S": "UNDERBODY"},
                "program_id": {"S": "Z02 FRT VAL LH CYC L3"},
            },
        ]

        dynamodb = boto3.client("dynamodb")
        for data in sample_data:
            dynamodb.put_item(TableName=table_name, Item=data)

        results = scan_table()
        assert len(results) == 2

        queries = {"program_id": "Z02 FRT VAL LH CYC L3", "point": "L02A712AHP_Y"}
        results = scan_table(**queries)
        assert len(results) == 1
