import traceback
from serviceapp.property_service import PropertyService


# TODO sanitize inputs to prevent SQL INJECTION
def handler(event, context):
    try:
        print('general handler')
        type_call = event['serviceCall']
        internal_evt = event['event']
        service = PropertyService(type_call, internal_evt)
        result = service.process_request()
        return result
    except Exception:
        print(traceback.format_exc())
        return {"result": "Unable to process the request"}
