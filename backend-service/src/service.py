import logging

from DBConnector import DBConnector
from utils.logger import init_logging


def status_check() -> str:
    """fetches 

    Returns:
        str: _description_
    """
    if db_connector.check_db_status():
        status_message = "Backend and Postgres services are running"
    else:
        status_message = "Postgres service is not running"
    logger.info(status_message)
    return status_message

if __name__=="__main__":
    logger = init_logging(logging.INFO, __file__)
    logger.info("Starting IONOS FastAPI Backend Service")
    db_connector = DBConnector(logging.DEBUG)
    status_check()