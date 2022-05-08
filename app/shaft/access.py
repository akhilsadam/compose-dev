from flask import jsonify, render_template
from app.redisclient import *

import logging
logger = logging.getLogger('root')

from app.options import options

import pickle
import musicpy as mp
import pygame


def get_pieces():
    out = redis_hget(3)
    logger.info(out)
    return out

# def play_piece(key=0):
#     out = redis_get_raw(4)[key]
#     obj = pickle.loads(out)
#     pygame.mixer.init(44100, -16,2,2048)
#     mp.play(obj)

def hrename(db,key0, key1):
    rd = redis_client(db)
    try:
        mapping = rd.hgetall(key0)
        rd.hset(key1,mapping=mapping)
    except Exception as e:
        logger.critical(f"Redis hrename failed with exception : {e}")
    else:
        rd.hdel(key0,*mapping.keys())
        
def rename_raw(db,key0, key1):
    rd = redis_client_raw(db)
    try:
        value = rd.get(key0)
        rd.set(key1,value)
    except Exception as e:
        logger.critical(f"Redis rename failed with exception : {e}")
    else:
        rd.delete(key0)

def n_piece():
    return len(redis_client(3).keys())
    
def play_piece(key=0):
    name = redis_client(3).hget(key,'name').replace(" ","")
    return render_template(
        "audio.jinja2",
        piece=f"\'{options.proxy}/static/audio/{name}.mp3\'",
        proxy=options.proxy,
        piece2=name
    )