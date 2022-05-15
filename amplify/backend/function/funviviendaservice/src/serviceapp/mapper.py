
class PropertyMapper:
    @staticmethod
    def to_table_properties(db_items: list):
        return list(map(lambda s: PropertyMapper.__to_table_item(s), db_items))

    @staticmethod
    def __to_table_item(db_item):
        """
            p.property_id(0), p.property_address(1), p.property_district(2),
            p.property_area(3), p.property_rooms(4), p.property_price(5), r.registered_on(6),
            o.owner_name(7), o.owner_id(8), o.owner_email(9), o.owner_phone_number(10)
        """
        return {
            "id": db_item[0],
            "address": db_item[1],
            "district": db_item[2],
            "area": db_item[3],
            "rooms": db_item[4],
            "price": db_item[5],
            "registeredOn": str(db_item[6]),
            "ownerName": db_item[7],
            "ownerId": db_item[8],
            "ownerEmail": db_item[9],
            "ownerPhone": db_item[10]
        }