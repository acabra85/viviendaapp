import json


def delete_property(req):
    print('deleting property')
    return {'result': 'deleteProperty'}


def new_property(req):
    print('creating property')
    return {'result': 'newProperty'}


def get_property(req):
    print('get property')
    return {'result': 'getProperty'}


def get_all_properties(req):
    print('get all properties')
    return {'result': 'getAllProperties'}


def get_owner(req):
    print('get owner')
    return {'result': 'getOwner'}


def handler(event, context):
    type_call = event['serviceCall']
    result = None
    if type_call == 'deleteProperty':
        result = delete_property(event['event'])
    elif type_call == 'newProperty':
        result = new_property(event['event'])
    elif type_call == 'getProperty':
        result = get_property(event['event'])
    elif type_call == 'getAllProperties':
        result = get_all_properties(event['event'])
    elif type_call == 'getOwner':
        result = get_owner(event['event'])
    else:
        result = {'result': f'Not Found service call {type_call}'}
    print(result)
    return json.dumps(result)
