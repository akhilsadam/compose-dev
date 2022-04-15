import logging
import os
logger = logging.getLogger('root')

from app.options import options
from app.api.schema import *
from app.redisclient import redis_client
from app.core import element
from . import fields

class initialize:
    def init():
        """Run all necessary setup"""
        for midi in os.listdir("app/core/midi"):
            if '.ipynb' not in midi:
                mp,_ = element.load(f'app/core/midi/{midi}')
                fields.create_piece(mp)
            