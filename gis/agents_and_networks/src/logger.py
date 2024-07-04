import logging


def logger(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.info(f"About to run {func.__name__}")
        out = func(*args, **kwargs)
        logger.info(f"Done running {func.__name__}")
        return out

    return wrapper
