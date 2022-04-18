import logging
logger = logging.getLogger('root')

from app.options import options
from app.api.schema import *
from app.redisclient import redis_client, redis_client_raw

import musicpy as mp
import pickle

def create_piece(obj,chd='-'):
    """Create piece/song field in Redis.
    Args:
      obj (musicpy-piece object): complete song information without instrument timbre/frequencies
      chd (dict): JSON-style chord progression
    """
    rd = redis_client(3)
    rdr = redis_client_raw(4)
    n_keys = len(rd.keys())

    # fill this in with the rest!
    name = str(obj[0]).split('\n')[0][7:]
    logger.info(name)

    maps = {
      'name'  : name,                                 # piece name
      'chd'   : chd,                                  # chord progression as user defined... '-' for a direct mp object
      'bars'  : obj.bars(),                           # number of bars/measures in piece/song
      'bpm'   : obj.bpm,                              # piece/song BPM
      'time'  : obj.eval_time()                       # length of piece/song in seconds
      }

    rd.hset(n_keys,mapping=maps)
    rdr.set(n_keys, pickle.dumps(obj)) # musicpy object
    
def read_song_info(id,key):
    """Get queryable sub-fields for a piece/song object.
    Args:
        id (int): id of piece object
        key (str): mame of sub-field
    """
    rd = redis_client_raw(3)
    if id in rd.keys():
        e = rd[id]
        if key in e:
            return e[key]
    return "N/A"

