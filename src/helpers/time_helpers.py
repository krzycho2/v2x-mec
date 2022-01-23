import logging
from functools import wraps
from time import time

from src.constants import DEFAULT_LOGGER_NAME

logger = logging.getLogger(DEFAULT_LOGGER_NAME)


def print_execution_time(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logger.info('Func: %s took %f', f.__name__, te - ts)
        return result
    return wrap
