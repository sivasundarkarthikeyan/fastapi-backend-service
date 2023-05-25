import os
import yaml
import logging
import psycopg2
from psycopg2 import connect

from utils.logger import init_logging

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

    def execute(self, sql:str) -> list:
        """Executes the given SQL query

        Args:
            sql (str): SQL query to execute

        Returns:
            list: inserted rows count for an insert query or
                  updated rows count for an update query or
                  list of records for a select query
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        return results
