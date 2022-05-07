import json
from db_connect import get_db_connection
from create_db import create_db


def delete_property(req):
    print('deleting property')
    property_id = req['pathParameters']['id']
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM rs_properties WHERE id='{property_id}'")
        return {'result': f'Success delete_property[{property_id}]'}

    except Exception as e:
        # Error while opening connection or processing
        print(e)
        return {'result': 'unable to delete data from DB'}
    finally:
        print("Closing Connection")
        if conn.open:
            conn.close()


def create_or_get_owner(req):
    pass


def new_property(req):
    print('creating property')
    conn = get_db_connection()
    user_id = create_or_get_owner(req)
    insert_sql = """INSERT INTO `rs_properties` ()"""
    property_id = None
    try:
        with conn.cursor() as cur:
            cur.execute(insert_sql)
        return {'result': 'newProperty', 'property_id': property_id}

    except Exception as e:
        # Error while opening connection or processing
        print(e)
        return {'result': 'unable to delete data from DB'}
    finally:
        print("Closing Connection")
        if conn.open:
            conn.close()


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
    elif type_call == 'createDB':
        result = create_db(clean_db=event['clean_db'])
    else:
        result = {'result': f'Not Found service call {type_call}'}
    return json.dumps(result).encode(encoding='utf8')
