import json
import boto3
import os

client = boto3.client('lambda')
HEADERS = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,GET",
    "Access-Control-Allow-Credentials": True,
    "Content-Type": "application/json"
}


def handler(event, context):
    event['clean_db'] = os.getenv('CLEAN_DB')
    service_req_input = {"serviceCall": "createDB", "event": event}

    response = client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:530526123093:function:funviviendaservice-dev',
        InvocationType='RequestResponse',
        Payload=json.dumps(service_req_input).encode(encoding='utf8')
    )

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": response['Payload'].read().decode('utf8', 'strict'),
        "isBase64Encoded": False
    }
