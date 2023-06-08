import sys
import logging
from logging import Logger

from src.utils.find_parent import get_project_root

def init_logging(log_level, filename:str) -> Logger:
    """method to initialize the logger with configurations

    Args:
        log_level (_type_): log class from which the logs needs to be logged
        filename (str): Python script name to which the logger is initialized

    Returns:
        Logger: Logger intialized for the corresponding script
    """
    root_dir = get_project_root()
    formatter = '%(asctime)s-%(levelname)s-%(name)s-%(message)s'
    logging.basicConfig(format = formatter, stream=sys.stdout,
                        datefmt='%Y-%m-%d,%H:%M:%S')
    filename = filename.replace(root_dir, '')
    logger = logging.getLogger(filename)
    logger.setLevel(log_level)
    return logger
