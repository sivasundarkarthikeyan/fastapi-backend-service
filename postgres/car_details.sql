CREATE TABLE IF NOT EXISTS VEHICLE (id serial primary key,
                      brand varchar(120),
                      "description" text,
                      metadata json,
                      year_of_manufacture integer,
                      ready_to_drive bool);

INSERT INTO VEHICLE (brand, "description", metadata, year_of_manufacture, ready_to_drive) VALUES ('test_Brand', 'test_Desc', '{"test_metadata_key":"test_metadata_val"}', 0, false);

