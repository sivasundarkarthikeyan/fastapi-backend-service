import os
import logging
from datetime import datetime
from typing import Union, Dict, List
from psycopg2 import connect, sql, DatabaseError

from src.utils.logger import init_logging

class DBConnector():
    """Class for communicating with the Postgres DB
    """
    def __init__(self, log_level:str = logging.INFO) -> None:
        self.logger = init_logging(log_level, __file__)
        self.conn = self._db_connect()

    def check_db_status(self) -> int:
        """to fetch the current status of the docker hosted Postgres service

        Returns:
            int: connection status code
        """
        return self.conn.status

    def _db_connect(self):
        """creates a connection to Postgres DB

        Returns:
            connection: DB connection based on psycopg2 module
        """
        username = os.environ['POSTGRES_USER']
        password = os.environ['POSTGRES_PASS']
        database = os.environ['POSTGRES_DB']
        hostname = os.environ['POSTGRES_HOST']
        port = os.environ['POSTGRES_PORT']

        conn = connect(
		host=hostname,
		port = port,
		dbname=database,
		user=username,
		password=password)
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
            filter_clause = " AND ".join([f"{key}='{val}'"
                                          if isinstance(val, str)
                                          else f"{key}={val}"
                                          for key, val in params.items()])
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
                       "year_of_manufacture", "ready_to_drive",
                       "created_on", "updated_on"]

        query = sql.SQL("INSERT INTO VEHICLE ({}) values ({})").format(
            sql.SQL(",").join(map(sql.Identifier, column_keys)),
            sql.SQL(",").join(map(sql.Placeholder, column_keys))
        )
        created_on = datetime.now()
        updated_on = None

        params_with_date = []
        for param in params:
            param["created_on"] = created_on
            param["updated_on"] = updated_on
            params_with_date.append(param)

        return self.execute(query, params_with_date, "insert")

    def update(self, filter_with: dict, replace_with:dict) -> int:
        """updates the records that matches the given filter criteria
            with new data

        Args:
            filter_with (dict): criteria to filter the rows
            replace_with (dict): new data to replace the existing rows

        Returns:
            int: total number of records updated
        """

        updated_on = str(datetime.now())
        replace_with['updated_on'] = updated_on

        update_clause = ", ".join([f"{key}='{val}'"
                                   if isinstance(val, str)
                                   else f"{key}={val}"
                                   for key, val in replace_with.items()])
        filter_clause = "AND ".join([f"{key}='{val}'"
                                     if isinstance(val, str)
                                     else f"{key}={val}"
                                     for key, val in filter_with.items()])
        query = "UPDATE VEHICLE SET " + update_clause +" WHERE " + filter_clause +";"
        return self.execute(query, None, "update")

    def delete(self, params: dict) -> int:
        """deletes the records that matches the given filter criteria

        Args:
            filter_with (dict): criteria to filter the rows
        
        Returns:
            int: total number of records deleted
        """

        filter_clause = "AND ".join([f"{key}='{val}'"
                                     if isinstance(val, str)
                                     else f"{key}={val}"
                                     for key, val in params.items()])
        query = "DELETE FROM VEHICLE WHERE " + filter_clause +";"
        return self.execute(query, None, "delete")

    def execute(self, query:str, params:Union[Dict, None], query_type:str) -> list:
        """Executes the given SQL query

        Args:
            query (str): SQL query to execute

        Returns:
            list: inserted rows count for an insert query or
                  updated rows count for an update query or
                  deleted rows count for an update query or
                  list of records for a select query and few 
                  more results based on the type of DML operations
        """
        if self.conn.closed:
            self.conn = self._db_connect()
        cur = self.conn.cursor()
        try:
            if query_type == 'insert':
                results = 0
                cur.executemany(query, params)
                results = cur.rowcount
            else:
                cur.execute(query)

                if query_type == 'fetch':
                    results = cur.fetchall()
                elif query_type in ['update', 'delete']:
                    results = cur.rowcount
                else:
                    raise ValueError("Invalid query type")
            self.conn.commit()
            return results
        except (Exception, DatabaseError) as error:
            self.conn.rollback()
            raise DatabaseError("Error in transaction, reverting all changes using rollback ", error)
            
