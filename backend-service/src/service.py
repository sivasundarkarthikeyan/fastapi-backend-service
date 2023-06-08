import logging
from typing import List, Dict

from fastapi import FastAPI
from fastapi_health import health

from src.vehicle import Vehicle
from src.db_connector import DBConnector
from src.utils.logger import init_logging

logger = init_logging(logging.INFO, __file__)
logger.info("Starting IONOS FastAPI Backend Service")
DB_CONNECTOR = None

def db_connect() -> bool:
    """establishes Python Postgres DB connection 

    Raises:
        ConnectionError: Raises connection error when the Postgres server is unreachable
    """
    try:
        global DB_CONNECTOR
        DB_CONNECTOR = DBConnector(logging.DEBUG)
        logger.info("Established connection to Postgres DB")
        return True
    except:
        logger.warning("Couldn't establish connection to Postgres DB, restart Postgres container")
        return False

def is_database_online() -> Dict:
    """ Verifies if the backend service is up and 
        if it can connect to the Postgres service

    Returns:
        dict: a dictionary with the statuses of backend and Postgres
        If the backed is offline, we will get interal server error
    """
    if db_connect():
        return {"Backend Status": "Online", "Postgres Status": "Online"}

    return {"Backend Status": "Online", "Postgres Status": "Offline"}

db_connect()
app = FastAPI()

@app.get("/")
def homepage() -> str:
    """Homepage endpoint

    Returns:
        str: Returns basic information about the service
    """
    return "IONOS FastAPI Backend service - Homepage"

app.add_api_route("/health", health([is_database_online]),name="Status Check")

@app.post("/insert/", status_code=201)
def insert_rows(params: List[Vehicle]) -> Dict:
    """endpoint responsible to receive data from client to insert new records

    Args:
        params (List[Vehicle]): list of new records to be inserted

    Returns:
        Dict: total number of rows inserted
    """
    logger.info(f"received data {params}")
    params_dict = [param.dict() for param in params]
    logger.info(f"params_dict:{params_dict}")
    inserted_rows = DB_CONNECTOR.insert(params_dict)
    response = {"Inserted records count":inserted_rows}
    return response

@app.get("/fetch/")
def fetch_rows()-> List:
    """endpoint responsible to fetch all records from the table and send to client

    Returns:
        List[Vehicle]: all records from the table
    """
    return DB_CONNECTOR.fetch()

@app.post("/filter/")
def filter_rows(params: dict)-> List:
    """endpoint responsible to fetch table records that matches 
        the input filter(s) and send to client

    Args:
        params (Dict): column name and corresponding value to use for filtering the records

    Returns:
        List[Vehicle]: table records that matches the input filter(s)
    """
    return DB_CONNECTOR.fetch(params)

@app.get("/nrows/")
def fetch_total_rows()-> Dict:
    """endpoint responsible to fetch total rows in the table

    Returns:
        Dict: total number of rows in the table
    """
    total_rows = DB_CONNECTOR.fetch_row_count()
    response = {"Total records count":total_rows}
    return response

@app.put("/update/")
def update_rows(params: dict)-> Dict:
    """endpoint responsible to update the table rows that match given criteria

    Args:
        params (Dict): The parameters to be used in the update SQL query

    Returns:
        Dict: total number of records updated in the table
    """
    filter_with, replace_with = params["filter_with"], params["replace_with"]
    updated_rows_count = DB_CONNECTOR.update(filter_with, replace_with)
    response = {"Updated records count":updated_rows_count}
    return response

@app.delete("/delete/")
def delete_rows(params: dict)-> Dict:
    """endpoint responsible to delete the table rows that match given criteria

    Args:
        params (Dict): The parameters to be used in the delete SQL query

    Returns:
        Dict: total number of records delete from the table
    """
    if not params:
        raise RuntimeError("Deletion without filter is not allowed")
    deleted_rows_count = DB_CONNECTOR.delete(params)
    response = {"Deleted records count":deleted_rows_count}
    return response
