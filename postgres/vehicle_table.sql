CREATE TABLE IF NOT EXISTS VEHICLE (id serial primary key,
                      brand varchar(120),
                      "description" text,
                      metadata json,
                      year_of_manufacture integer,
                      ready_to_drive bool);