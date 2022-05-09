from persistence_helper import PersistenceHelper
import json


class PropertyService:
    def __init__(self, type_call, event):
        self.persistence = PersistenceHelper()
        self.event = event
        self.type_call = type_call
        print(event)

    def __initialize_db(self):
        return self.persistence.create_db(self.event['clean_db'])

    def __register_property(self):
        print('registering property...')
        body = json.loads(self.event['body'])
        owner = body['owner']
        properties = body['properties']
        property_ids = self.persistence.register_properties(owner, properties)
        if property_ids:
            return {
                "result": "newProperty",
                "property_ids": property_ids
            }
        return {"result": "unable to register properties"}

    def __delete_property(self):
        property_id = self.event['pathParameters']['id']
        print('deleting property')
        if not self.persistence.delete_property(property_id):
            return {"result": "unable to delete data from DB"}
        return {"result": "Success delete_property[" + property_id}

    def __get_property(self):
        property_id = self.event['pathParameters']['id']
        print('get property')
        return {"result": "getProperty"}

    def __get_all_properties(self):
        print('get all properties')
        query_params = self.event['queryStringParameters']
        print('1')
        page = int(query_params['page'])
        print('2')
        page_size = int(query_params['pageSize'])
        print('3')
        column = query_params['filterColumn']
        print('4')
        asc = query_params['asc'] == 'true'
        print('5')
        page_result = self.persistence.get_properties_page(page, page_size, column, asc)
        print('6')
        if not page_result:
            print('7')
            return {"result": "unable to retrieve page from BD"}
        print('8')
        return page_result

    def __get_owner(self, req):
        print('get owner')
        return {"result": "getOwner"}

    def process_request(self):
        if self.type_call == 'newProperty':
            print("90")
            return self.__register_property()
        elif self.type_call == 'deleteProperty':
            print("91")
            return self.__delete_property()
        elif self.type_call == 'getProperty':
            print("92")
            return self.__get_property()
        elif self.type_call == 'getAllProperties':
            print("93")
            return self.__get_all_properties()
        elif self.type_call == 'getOwner':
            print("94")
            return self.__get_owner()
        elif self.type_call == 'createDB':
            print("95")
            return self.__initialize_db()
        return {"result": "Not Found service call :" + self.type_call}
