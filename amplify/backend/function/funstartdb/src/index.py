import json
import boto3
import os

CLEAN_DB_VAR = 'CLEAN_DB'

client = boto3.client('lambda')
HEADERS = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,GET',
    'Content-Type': 'application/json'
}


def handler(event, context):
    service_req_input = {'serviceCall': 'createDB', 'event': event, 'clean_db': os.getenv(CLEAN_DB_VAR)}

    response = client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:530526123093:function:funviviendaservice-dev',
        InvocationType='RequestResponse',
        Payload=json.dumps(service_req_input)
    )

    body = json.loads(response["Payload"].read().decode('utf8', 'strict'))
    if 'success_db_created' == body['result']:
        os.environ[CLEAN_DB_VAR] = ''
    return {
        'statusCode': 200,
        'headers': HEADERS,
        'body': body
    }
