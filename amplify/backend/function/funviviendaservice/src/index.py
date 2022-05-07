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


def owner_exists(cursor, owner_id):
    query_count_owner_by_id = f"SELECT COUNT(*) FROM rs_owner WHERE owner_id='{owner_id}';"
    cursor.execute(query_count_owner_by_id)
    result = cursor.fetchone()[0]
    print(f"--------{query_count_owner_by_id}=[{result}]")
    return result > 0


def create_or_get_owner(cursor, owner, owner_id):
    if not owner_exists(cursor, owner_id):
        INSERT_OWNER_QUERY = "INSERT INTO `rs_owner` (owner_id, owner_name, owner_phone_number, owner_email) " \
                  "VALUES (%s, %s, %s, %s);"
        print(f"------{INSERT_OWNER_QUERY}")
        args = (owner_id, owner['name'], owner['phone_number'], owner['email'])
        return cursor.execute(INSERT_OWNER_QUERY, args) == 1
    return True


def new_property(req):
    print('creating property')
    conn = get_db_connection(False)
    try:
        cursor = conn.cursor()
        insert_new_property_sql = "INSERT " \
                                  " INTO `rs_properties` (property_address, property_district, property_rooms, " \
                                  " property_price, property_area )" \
                                  " VALUES (%s, %s, %s, %s, %s);"

        with cursor as cur:
            owner = req['owner']
            owner_id = owner['id']
            if not create_or_get_owner(cur, owner, owner_id):
                return {'result': 'unable to create owner'}
            print(f"-------{insert_new_property_sql}")
            property_ids = []
            for prop in req['properties']:
                args = (prop['address'], prop['district'], prop['rooms'], prop['price'], prop['area'])
                cur.execute(insert_new_property_sql, args)
                p_id = cur.lastrowid
                property_ids.append(p_id)
                insert_property_ownership_sql = "INSERT" \
                                                " INTO `rs_properties_owner` (owner_id, property_id, registered_on)" \
                                                f" VALUES ('{owner_id}', '{p_id}', NOW());"
                print(f"---------{insert_property_ownership_sql}")
                cur.execute(insert_property_ownership_sql)
            conn.commit()
        return {'result': 'newProperty', 'property_ids': property_ids}
    except Exception as e:
        # Error while opening connection or processing
        print(e)
        return {'result': 'unable to update to DB'}
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


# TODO sanitize inputs to prevent SQL INJECTION
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
