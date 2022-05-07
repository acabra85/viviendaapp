import json
import boto3

client = boto3.client('lambda')


def handler(event, context):
    print('handler fun nuevo inmueble')
    service_req_input = {"serviceCall": "newProperty", "event": event}

    response = client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:530526123093:function:funviviendaservice-dev',
        InvocationType='RequestResponse',
        Payload=json.dumps(service_req_input).encode(encoding='utf8')
    )

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Access-Control-Allow-Credentials": True,
            "Content-Type": "application/json"
        },
        'body': response["Payload"].read().decode('utf8', 'strict'),
        "isBase64Encoded": False
    }
