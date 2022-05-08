from app.options import options

import redis

import logging
logger = logging.getLogger('root')

### SETTERS

def redis_client(dbi):
    """Get Redis Client.
    Args:
        dbi (int): database number
    Returns:
        object: redis server object.
    """
    # print(f"REDIS host IP: {options.redhost}")
    # logger.info(dbi)
    return redis.Redis(host=options.redhost, port=options.redport, db=dbi, charset="utf-8", decode_responses=True)
def redis_client_raw(dbi):
    """Get Redis Client (without decoding).
    Args:
        dbi (int): database number
    Returns:
        object: redis server object.
    """
    # print(f"REDIS host IP: {options.redhost}")
    # logger.info(dbi)
    return redis.Redis(host=options.redhost, port=options.redport, db=dbi, charset="utf-8", decode_responses=False)

### GETTERS

def redis_hget(db):
    rd = redis_client(db)
    s = sorted(rd.keys())
    out = [rd.hgetall(key) for key in s]
    # logger.info(rd.keys())
    return out

def redis_get_raw(db):
    rd = redis_client_raw(db)
    s = sorted(rd.keys())
    out = [rd.get(key) for key in s]
    # logger.info(rd.keys())
    return out

def redis_get(db):
    rd = redis_client(db)
    s = sorted(rd.keys())
    out = [rd.get(key) for key in s]
    # logger.info(rd.keys())
    return out
