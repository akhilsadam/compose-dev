import logging
import socket
# format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'

def init_logger(name,level=logging.INFO):
    formatter = logging.Formatter(fmt=f'[%(asctime)s {socket.gethostname()}] %(module)s:%(funcName)s:%(lineno)s -/| [%(levelname)s] %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger