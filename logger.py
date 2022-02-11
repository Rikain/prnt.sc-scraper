import logging


def create_logger():
    logger = logging.getLogger('exc_logger')
    logger.setLevel(logging.INFO)

    logfile = logging.FileHandler('exc_logger.log')

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)

    logfile.setFormatter(formatter)
    logger.addHandler(logfile)

    return logger


logger = create_logger()


def exception():
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
                raise
        return wrapper
    return decorator
