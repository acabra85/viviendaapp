from .db_connect import get_db_connection
from .mapper import PropertyMapper
import traceback

DROP_TABLE_OWNER_SQL = "DROP TABLE IF EXISTS rs_owners;"
DROP_TABLE_PROPERTY_SQL = "DROP TABLE IF EXISTS rs_properties;"
DROP_TABLE_PROPERTY_REGISTRY_SQL = "DROP TABLE IF EXISTS rs_property_registry;"
CREATE_TABLE_PROPERTIES_SQL = """
    CREATE TABLE rs_properties (
                    property_id int NOT NULL AUTO_INCREMENT,
                    property_address varchar(300) NOT NULL,
                    property_district varchar(100) NOT NULL,
                    property_rooms int NOT NULL,
                    property_price int NOT NULL,
                    property_area float(8,2) NOT NULL,
                    PRIMARY KEY (property_id) 
                ) ENGINE=InnoDB; """
CREATE_TABLE_OWNER_SQL = """
    CREATE TABLE rs_owners (
                    owner_id varchar(20) NOT NULL,
                    owner_email varchar(100) NOT NULL,
                    owner_phone_number varchar(15) NOT NULL,
                    owner_name varchar(100) NOT NULL,
                    PRIMARY KEY (owner_id) 
                 ) ENGINE=InnoDB;"""
CREATE_TABLE_PROPERTY_REGISTRY_SQL = """
    CREATE TABLE rs_property_registry (
                    registration_id int NOT NULL AUTO_INCREMENT,
                    owner_id varchar(20) NOT NULL,
                    property_id int NOT NULL,
                    registered_on DATETIME,
                    PRIMARY KEY (registration_id),
                    FOREIGN KEY (owner_id) 
                        REFERENCES rs_owners(owner_id), 
                    FOREIGN KEY (property_id) 
                        REFERENCES rs_properties(property_id) 
                        ON DELETE CASCADE 
                 ) ENGINE=InnoDB;"""

INSERT_PROPERTY_REGISTRY = """
    INSERT INTO `rs_property_registry` (owner_id, property_id, registered_on)
                                VALUES (%s, %s, NOW());"""
INSERT_NEW_PROPERTY_SQL = """
    INSERT INTO `rs_properties` ( property_address, property_district, property_rooms, property_price, property_area )
                         VALUES (%s, %s, %s, %s, %s);"""


class PersistenceHelper:
    def create_db(self, clean_db=None):
        print('clean db')
        if "TRUE" == clean_db:
            conn = get_db_connection()
            if not conn:
                return {"result": "failure to connect to DB"}
            try:
                with conn.cursor() as cur:
                    cur.execute(DROP_TABLE_PROPERTY_REGISTRY_SQL)
                    cur.execute(DROP_TABLE_PROPERTY_SQL)
                    cur.execute(DROP_TABLE_OWNER_SQL)
                    cur.execute(CREATE_TABLE_PROPERTIES_SQL)
                    cur.execute(CREATE_TABLE_OWNER_SQL)
                    cur.execute(CREATE_TABLE_PROPERTY_REGISTRY_SQL)
                return {"result": "success_db_created"}
            except Exception as e:
                print(e)
                return {"result": "failure to create DB"}
        return {"result": "clean_up_is_not_enabled"}

    def insert_property_registry(self, cur, owner_id, p_id):
        args = (owner_id, p_id)
        cur.execute(INSERT_PROPERTY_REGISTRY, args)

    def insert_new_property(self, cur, prop):
        args = (prop['address'], prop['district'], prop['rooms'], prop['price'], prop['area'])
        cur.execute(INSERT_NEW_PROPERTY_SQL, args)

    def _owner_exists(self, cursor, owner_id):
        query_count_owner_by_id = f"SELECT COUNT(*) FROM rs_owners WHERE owner_id='{owner_id}';"
        cursor.execute(query_count_owner_by_id)
        result = cursor.fetchone()[0]
        return result > 0

    def create_or_get_owner(self, cursor, owner, owner_id):
        if not self._owner_exists(cursor, owner_id):
            print("creating owner ...")
            insert_owner_sql = "INSERT INTO `rs_owners` (owner_id, owner_name, owner_phone_number, owner_email) " \
                               "VALUES (%s, %s, %s, %s);"
            args = (owner_id, owner['name'], owner['phone_number'], owner['email'])
            return cursor.execute(insert_owner_sql, args) == 1
        return True

    def register_properties(self, owner, properties):
        conn = get_db_connection(False)
        if not conn:
            return None
        try:
            property_ids = []
            with conn.cursor() as cur:
                owner_id = owner['id']
                if not self.create_or_get_owner(cur, owner, owner_id):
                    return {"result": "unable to create owner"}
                for prop in properties:
                    self.insert_new_property(cur, prop)
                    new_property_id = cur.lastrowid
                    property_ids.append(new_property_id)
                    self.insert_property_registry(cur, owner_id, new_property_id)
            conn.commit()
            return property_ids
        except Exception:
            print(traceback.format_exc())
            return []
        finally:
            print("Closing Connection")
            if conn.open:
                conn.close()

    def get_properties_page(self, page, page_size, column, asc):
        conn = get_db_connection()
        if not conn:
            return []
        try:
            column_order = 'r.registered_on' if column == 'registeredOn' else 'p.property_district'
            direction_order = 'ASC' if asc else 'DESC'
            limit = page_size
            offset = (page_size * page) - page_size
            with conn.cursor() as cur:
                total = self.count_total_properties(cur)
                query = f"""SELECT p.property_id, p.property_address, p.property_district, 
                                  p.property_area, p.property_rooms, p.property_price, r.registered_on,
                                  o.owner_name, o.owner_id, o.owner_email, o.owner_phone_number
                             FROM rs_properties p
                             INNER JOIN rs_property_registry r ON p.property_id=r.property_id
                             INNER JOIN rs_owners o ON o.owner_id = r.owner_id
                             ORDER BY {column_order} {direction_order} 
                             LIMIT {limit} OFFSET {offset};"""
                cur.execute(query)
                properties = PropertyMapper.to_table_properties(cur.fetchall())
            return {"result": "success", "totalRecords": total, "records": properties}
        except Exception:
            print(traceback.format_exc())
            return None
        finally:
            if conn.open:
                conn.close()

    def delete_property(self, property_id):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cur:
                delete_property_by_id_sql = f"DELETE FROM rs_properties WHERE property_id={property_id}"
                return cur.execute(delete_property_by_id_sql) > 0
        except Exception as e:
            # Error while opening connection or processing
            print(traceback.format_exc())
            return {"result": "unable to delete data from DB"}
        finally:
            if conn.open:
                conn.close()

    def count_total_properties(self, cur):
        cur.execute("SELECT COUNT(*) FROM rs_properties")
        return cur.fetchone()[0]
