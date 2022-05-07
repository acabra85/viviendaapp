import json
import boto3

client = boto3.client('lambda')
HEADERS = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,GET',
    'Content-Type': 'application/json'
}


def handler(event, context):
    service_req_input = {'serviceCall': 'getProperty', 'event': event}

    response = client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:530526123093:function:funviviendaservice-dev',
        InvocationType='RequestResponse',
        Payload=json.dumps(service_req_input)
    )

    return {
        'statusCode': 200,
        'headers': HEADERS,
        'body': json.loads(response["Payload"].read().decode('utf8', 'strict'))
    }
