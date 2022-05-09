--RECREATE
DROP TABLE IF EXISTS rs_owners;
DROP_TABLE_PROPERTY_SQL = "DROP TABLE IF EXISTS rs_properties;
DROP_TABLE_PROPERTY_REGISTRY_SQL = "DROP TABLE IF EXISTS rs_property_registry;

--CREATE TABLES
CREATE TABLE rs_properties (
                property_id int NOT NULL AUTO_INCREMENT,
                property_address varchar(300) NOT NULL,
                property_district varchar(100) NOT NULL,
                property_rooms int NOT NULL,
                property_price int NOT NULL,
                property_area float(8,2) NOT NULL,
                PRIMARY KEY (property_id)
            ) ENGINE=InnoDB;
CREATE TABLE rs_owners (
                owner_id varchar(20) NOT NULL,
                owner_email varchar(100) NOT NULL,
                owner_phone_number varchar(15) NOT NULL,
                owner_name varchar(100) NOT NULL,
                PRIMARY KEY (owner_id)
             ) ENGINE=InnoDB;
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
             ) ENGINE=InnoDB;