import logging
from typing import List, Union
from fastapi import FastAPI, Response, Depends
from src.DBConnector import DBConnector
from src.utils.logger import init_logging

from src.Vehicle import Vehicle

logger = init_logging(logging.INFO, __file__)
logger.info("Starting IONOS FastAPI Backend Service")
db_connector = None

def db_connect():
    """establishes Python Postgres DB connection 

    Raises:
        ConnectionError: Raises connection error when the Postgres server is unreachable
    """
    try:
        global db_connector
        db_connector = DBConnector(logging.DEBUG)
        logger.info("Established connection to Postgres DB")
    except:
        raise ConnectionError("Postgres server is unreachable")

db_connect()

app = FastAPI()


def get_session():
    return True

def is_database_online(session: bool = Depends(get_session)):
    return session

@app.get("/")
def homepage() -> str:
    """Homepage endpoint

    Returns:
        str: Returns basic information about the service
    """
    return "IONOS FastAPI Backend service - Homepage"


@app.get("/status/")
def status_check() -> str:
    """endpoint responsible to verify the status of backend

    Returns:
        str: Status of the backend and Postgres service
    """
    response = Response()
    if db_connector.check_db_status():
        response.status_code = 200
        status_message = "Backend and Postgres services are running"
    else:
        response.status_code = 500
        status_message = "Postgres service is not running"
    logger.info(status_message)
    return status_message

@app.post("/insert/", status_code=201)
def insert_rows(params: List[Vehicle]) -> dict:
    """endpoint responsible  to receive data from client to insert new records

    Args:
        params (List[Vehicle]): list of new records to be inserted

    Returns:
        int: total number of rows inserted
    """
    params_dict = [param.dict() for param in params]
    logger.info(f"params_dict:{params_dict}")
    inserted_rows = db_connector.insert(params_dict)
    response = {"Inserted records count":inserted_rows}
    return response

@app.get("/fetch/")
def fetch_rows()-> List:
    """endpoint responsible to fetch all records from the table and send to client

    Returns:
        List: all records from the table
    """
    return db_connector.fetch()

@app.post("/filter/")
def filter_rows(params: dict)-> List:
    """endpoint responsible to fetch table records that matches the input filter(s) and send to client

    Args:
        params (dict): column name and corresponding value to use for filtering the records

    Returns:
        List: table records that matches the input filter(s)
    """
    return db_connector.fetch(params)

@app.get("/nrows/")
def fetch_total_rows()-> dict:
    """endpoint responsible to fetch total rows in the table

    Returns:
        int: total number of rows in the table
    """
    total_rows = db_connector.fetch_row_count()
    response = {"Total records count":total_rows}
    return response

@app.put("/update/")
def update_row(values: dict)-> dict:
    """_summary_

    Args:
        id (int): id to use for identifying the record for updation
        params (Vehicle): column name and corresponding value to use for 
                            updating the matching records

    Returns:
        int: total number of records updated in the table
    """
    filter_with, replace_with = values["filter_with"], values["replace_with"]
    updated_rows_count = db_connector.update(filter_with, replace_with)
    response = {"Updated records count":updated_rows_count}
    return response