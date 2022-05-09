import json
import traceback
from property_service import PropertyService


# TODO sanitize inputs to prevent SQL INJECTION
def handler(event, context):
    try:
        print('general handler')
        type_call = event['serviceCall']
        internal_evt = event['event']
        print(event)
        service = PropertyService(type_call, internal_evt)
        print('a')
        result = service.process_request()
        print('b')
        return json.dumps(result).encode(encoding='utf8')
    except Exception:
        print('c')
        print(traceback.format_exc())
        return json.dumps({"result": "Unable to process the request"}).encode(encoding='utf8')
