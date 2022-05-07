from db_connect import get_db_connection


def create_db(clean_db=None):
    print('clean db')
    if "TRUE" == clean_db:
        conn = get_db_connection()
        if not conn:
            return {'result': 'failure to connect to DB'}
        create_table_properties = "CREATE TABLE rs_properties (" \
                                  " property_id int NOT NULL AUTO_INCREMENT," \
                                  " property_address varchar(300) NOT NULL," \
                                  " property_district varchar(100) NOT NULL," \
                                  " property_rooms int NOT NULL," \
                                  " property_price int NOT NULL," \
                                  " property_area float(8,2) NOT NULL," \
                                  " PRIMARY KEY (property_id) " \
                                  ") ENGINE=InnoDB;"
        create_table_owner = "CREATE TABLE rs_owner (" \
                             " owner_id varchar(20) NOT NULL," \
                             " owner_email varchar(100) NOT NULL," \
                             " owner_phone_number varchar(15) NOT NULL," \
                             " owner_name varchar(100) NOT NULL," \
                             " PRIMARY KEY (owner_id) " \
                             ") ENGINE=InnoDB;"
        create_table_owner_property = "CREATE TABLE rs_properties_owner (" \
                                      " ownership_id int NOT NULL AUTO_INCREMENT," \
                                      " owner_id varchar(20) NOT NULL," \
                                      " property_id int NOT NULL," \
                                      " registered_on DATETIME," \
                                      " PRIMARY KEY (ownership_id)," \
                                      " FOREIGN KEY (owner_id) REFERENCES rs_owner(owner_id), " \
                                      " FOREIGN KEY (property_id) " \
                                      "     REFERENCES rs_properties(property_id) " \
                                      "     ON DELETE CASCADE " \
                                      ") ENGINE=InnoDB;"
        try:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS rs_properties_owner;")
                cur.execute("DROP TABLE IF EXISTS rs_properties;")
                cur.execute("DROP TABLE IF EXISTS rs_owner;")
                print(f'----[{create_table_properties}]')
                cur.execute(create_table_properties)
                print(f'----[{create_table_owner}]')
                cur.execute(create_table_owner)
                print(f'----[{create_table_owner_property}]')
                cur.execute(create_table_owner_property)
            return {'result': 'success_db_created'}
        except Exception as e:
            print(e)
            return {'result': 'failure to create DB'}
    return {'result': 'clean_up_is_not_enabled'}
