import logging
import socket
# format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'

def init_logger(name:str,level:object=logging.INFO) -> logging.Logger:
    """Make/get a logger.

    Args:
        name (str): logger name
        level (object, optional): Log level. Defaults to logging.INFO.

    Returns:
        logging.Logger: logger object
    """
    formatter = logging.Formatter(fmt=f'[%(asctime)s {socket.gethostname()}] %(module)s:%(funcName)s:%(lineno)s -/| [%(levelname)s] %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger