import logging


def get_logger(module):
    """
    :param module: (module) the module name (__name__) of the code calling this function
    :return: returns a configured standard library logger.
    """

    logger = logging.getLogger(module)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler('/var/log/http_traffic_monitor.log')
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    err_handler = logging.StreamHandler()
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(formatter)
    logger.addHandler(err_handler)

    return logger