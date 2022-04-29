from flask import jsonify, render_template
from app.redisclient import redis_client, redis_client_raw

import logging
logger = logging.getLogger('root')

from app.options import options

import pickle
import musicpy as mp
import pygame

def redis_hget(db):
    rd = redis_client(db)
    out = [rd.hgetall(key) for key in rd.keys()]
    # logger.info(rd.keys())
    return out

def redis_get_raw(db):
    rd = redis_client_raw(db)
    out = [rd.get(key) for key in rd.keys()]
    # logger.info(rd.keys())
    return out

def redis_get(db):
    rd = redis_client(db)
    out = [rd.get(key) for key in rd.keys()]
    # logger.info(rd.keys())
    return out


def get_pieces():
    out = redis_hget(3)
    logger.info(out)
    return out

# def play_piece(key=0):
#     out = redis_get_raw(4)[key]
#     obj = pickle.loads(out)
#     pygame.mixer.init(44100, -16,2,2048)
#     mp.play(obj)

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