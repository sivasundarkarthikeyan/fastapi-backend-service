import sys
import logging
from src.utils.findParent import get_project_root

def init_logging(log_level, filename:str):
    root_dir = get_project_root()
    formatter = '%(asctime)s-%(levelname)s-%(name)s-%(message)s'
    logging.basicConfig(format = formatter, stream=sys.stdout, 
                        datefmt='%Y-%m-%d,%H:%M:%S')
    filename = filename.replace(root_dir, '')
    logger = logging.getLogger(filename)
    logger.setLevel(log_level)
    return logger

