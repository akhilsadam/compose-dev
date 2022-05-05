from ast import Str
import logging
import os

from joblib import Parallel, delayed
logger = logging.getLogger('root')

from app.options import options
from app.queue.jobs import jobs
from app.schema import *
from app.redisclient import redis_client
from app.core import element
from app.quarry.appfields import appfields
from multiprocessing import Pool,get_context,cpu_count
from app.queue.identity import current_id
# note this class actually runs from top-level!
class initialize:
    def init_midi(midi : str) -> str:
        """Initialize piece that has midi filepath `midi` of (str) type. Returns a success / failure string"""
        if '.ipynb' not in midi:
            try:
                logger.info(f'initalize midi : {midi}')                

                # need to add check that item is not in database

                mp,_ = element.load(f'app/core/midi/{midi}')

                nm = str(mp[0]).split('\n')[0][8:]
                appfields.create_piece(mp)
                os.system(f"touch app/static/audio/{nm}.mp3")
                os.system(f"chmod ugo+rwx app/static/audio/{nm}.mp3")
                element.mp3(mp,f"app/static/audio/{nm}")
            except Exception as E:
                return f'FAILURE: {E}'
            return 'Success'

    def init():
        """Run all necessary setup."""
        logger.info('INITALIZING...')

        logger.info('INITALIZING TRANSFORMATIONS...')
        appfields.create_chdTransform()

        logger.info('INITALIZING PIECES...')
        # sf = []
        # with Pool(processes=8) as pool:
        #     sf.extend(pool.map(initialize.init_midi,os.listdir("app/core/midi")))

        # try:
        #     sf.extend(Parallel(n_jobs=cpu_count(), require='sharedmem')(delayed(initialize.init_midi)(midi) for midi in os.listdir("app/core/midi")))
        # except Exception as e:
        #     return f"exception:{e}" 

        for midi in os.listdir("app/core/midi"):
            jobs.job(["initialize", "init_midi", midi],current_id)

        logger.info('INITIALIZATION COMPLETE')
        # return "|".join(sf)