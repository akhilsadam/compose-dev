from flask import render_template
from app.redisclient import *

import logging
logger = logging.getLogger('root')

from app.options import options


def get_pieces() -> list:
    """Get all piece data.

    Returns:
        list: list of dictionaries containing piece data.
    """
    out = redis_hget(3)
    logger.info(out)
    return out

# def play_piece(key=0):
#     out = redis_get_raw(4)[key]
#     obj = pickle.loads(out)
#     pygame.mixer.init(44100, -16,2,2048)
#     mp.play(obj)

def hrename(db:int,key0:str, key1:str):
    """Rename a hash in Redis.

    Args:
        db (int): database number
        key0 (str): initial hashname
        key1 (str): final hashname
    """
    rd = redis_client(db)
    try:
        mapping = rd.hgetall(key0)
        rd.hset(key1,mapping=mapping)
    except Exception as e:
        logger.critical(f"Redis hrename failed with exception : {e}")
    else:
        rd.hdel(key0,*mapping.keys())
        
def rename_raw(db:int,key0:str, key1:str):
    """Rename a key in Redis.

    Args:
        db (int): database number
        key0 (str): initial key
        key1 (str): final key
    """
    rd = redis_client_raw(db)
    try:
        value = rd.get(key0)
        rd.set(key1,value)
    except Exception as e:
        logger.critical(f"Redis rename failed with exception : {e}")
    else:
        rd.delete(key0)

def n_piece() -> int:
    """Get number of pieces in songbank.

    Returns:
        int: number of pieces.
    """
    return len(redis_client(3).keys())
    
def play_piece(key:int=0) -> str:
    """Returns a HTML page that allows playing of a selected piece.

    Args:
        key (int, optional): Piece ID. Defaults to 0.

    Returns:
        str: HTML rendertemplate with path to audio file
    """
    name = redis_client(3).hget(key,'name').replace(" ","")
    return render_template(
        "audio.jinja2",
        piece=f"\'{options.proxy}/static/audio/{name}.mp3\'",
        proxy=options.proxy,
        piece2=name
    )