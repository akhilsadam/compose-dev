from app.options import options

import redis

import logging
logger = logging.getLogger('root')

### SETTERS

def redis_client(dbi:int) -> redis.Redis:
    """Get Redis Client.
    Args:
        dbi (int): database number
    Returns:
        object: redis server object.
    """
    # print(f"REDIS host IP: {options.redhost}")
    # logger.info(dbi)
    return redis.Redis(host=options.redhost, port=options.redport, db=dbi, charset="utf-8", decode_responses=True)
def redis_client_raw(dbi:int) -> redis.Redis:
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

def redis_hget(db:int)->list:
    """Get all values for every hash in database as list of dictonaries

    Args:
        db (int): selected database

    Returns:
        list: all values
    """
    rd = redis_client(db)
    s = sorted(rd.keys())
    out = [rd.hgetall(key) for key in s]
    # logger.info(rd.keys())
    return out

def redis_get_raw(db:int)->list:
    """Get all values for every key in raw database as list

    Args:
        db (int): selected database

    Returns:
        list: all values
    """
    rd = redis_client_raw(db)
    s = sorted(rd.keys())
    out = [rd.get(key) for key in s]
    # logger.info(rd.keys())
    return out

def redis_get(db:int)->list:
    """Get all values for every key in raw database as list

    Args:
        db (int): selected database

    Returns:
        list: all values
    """
    rd = redis_client(db)
    s = sorted(rd.keys())
    out = [rd.get(key) for key in s]
    # logger.info(rd.keys())
    return out
