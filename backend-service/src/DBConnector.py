import os
import yaml
import logging
from typing import Union, Dict, List
from psycopg2 import connect, sql
from psycopg2.extras import execute_batch
from src.utils.logger import init_logging

class DBConnector():

    def __init__(self, log_level:str = logging.INFO) -> None:
        self.logger = init_logging(log_level, __file__)
        self.conn = self._db_connect()

    def check_db_status(self) -> int:
        """to fetch the current status of the docker hosted Postgres service

        Returns:
            int: connection status code
        """
        return self.conn.status
    
    def read_config(self) -> dict:
        """reads configuration file

        Raises:
            ValueError: raised when the file is empty
            FileNotFoundError: raised when the file does not exist

        Returns:
            dict: configuration values from the config file
        """
        if os.path.exists('config.yml'):
            with open('config.yml') as f:
                config = yaml.safe_load(f)   
                if config:
                    return config
                else:
                    raise ValueError("Config file is empty")
        else:
            raise FileNotFoundError("config.yml is not in the project directory")
        
    def _db_connect(self):
        """creates a connection to Postgres DB

        Returns:
            connection: DB connection based on psycopg2 module
        """
        credentials = self.read_config()
        conn = connect(
        host=credentials["DB_HOST"],
        database=credentials["DB_NAME"],
        user=credentials["DB_USER"],
        password=credentials["DB_PASS"])
        return conn

    def fetch_row_count(self) -> int:
        """fetches total number of rows in the table VEHICLE

        Returns:
            int: Total number of rows in the table VEHICLE
        """
        query = sql.SQL("SELECT COUNT(1) FROM VEHICLE;")
        return self.execute(query, None, "fetch")[0][0]
    
    def fetch(self, params: dict = None) -> List:
        """fetches all or subset of records from the table VEHICLE

        Args:
            params (dict, optional): column(s) parameters to use for filtering. Defaults to None.

        Returns:
            List: all or subset of records from the table VEHICLE
        """
        query = "SELECT * FROM VEHICLE"
        if params and isinstance(params, dict):
            filter_clause = " AND ".join([f"{key}='{val}'" if isinstance(val, str) else f"{key}={val}" for key, val in params.items()])
            query += f" WHERE {filter_clause}"    
        query += " ORDER BY id;"
        return self.execute(query, None, "fetch")
    
    def insert(self, params:list[dict]) -> int:
        """inserts data in to the table VEHICLE

        Args:
            params (list[dict]): list of new records to insert where each item 
                                 in list is a dictionary with record details

        Returns:
            int: total number of records inserted
        """
        column_keys = ["brand", "description", "metadata", 
                       "year_of_manufacture", "ready_to_drive"]

        query = sql.SQL("INSERT INTO VEHICLE ({}) values ({})").format(
            sql.SQL(",").join(map(sql.Identifier, column_keys)),
            sql.SQL(",").join(map(sql.Placeholder, column_keys))
        )
        return self.execute(query, params, "insert")
    
    def update(self, id: list, params:dict) -> int:
        """updates the records that matches the given id with new data

        Args:
            id (list): ids of records where the data needs to be updated
            params (dict): data to update the matching records

        Returns:
            int: total number of records updated
        """
        update_clause = ", ".join([f"{key}='{val}'" if isinstance(val, str) else f"{key}={val}" for key, val in params.items()])
        query = f"UPDATE VEHICLE SET {update_clause} WHERE id in {id};"
        return self.execute(query, None, "update")
    
    def execute(self, query:str, params:Union[Dict, None], query_type:str) -> list:
        """Executes the given SQL query

        Args:
            query (str): SQL query to execute

        Returns:
            list: inserted rows count for an insert query or
                  updated rows count for an update query or
                  list of records for a select query
        """
        cur = self.conn.cursor()
        if query_type == 'insert':
            results = 0
            cur.executemany(query, params)
            results = cur.rowcount
        else:
            cur.execute(query)
            
            if query_type == 'fetch':
                results = cur.fetchall()
            else:
                results = cur.rowcount
        self.conn.commit()
        return results
