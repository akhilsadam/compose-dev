import logging
import os
logger = logging.getLogger('root')

from app.options import options
from app.api.schema import *
from app.redisclient import redis_client
from app.core import element
from . import fields

# note this class actually runs from top-level!
class initialize:
    def init():
        """Run all necessary setup"""
        logger.info('INITALIZING...')
        for midi in os.listdir("app/core/midi"):
            if '.ipynb' not in midi:
                logger.info(f'initalize midi : {midi}')                
                
                # need to add check that item is not in database

                mp,_ = element.load(f'app/core/midi/{midi}')
                nm = str(mp[0]).split('\n')[0][7:]
                fields.create_piece(mp)
                os.system(f"touch app/static/audio/{nm}.mp3")
                os.system(f"chmod ugo+rwx app/static/audio/{nm}.mp3")
                element.mp3(mp,f"app/static/audio/{nm}")
        