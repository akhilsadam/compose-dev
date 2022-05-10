from ast import Str
import base64
import logging
import os
import pickle
import json as js

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
from app.quarry.chdprogress import chdprogress as chdp
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

    def init_chd(chp : str, bpm : float=138, name: str='Progression 0', id=None) -> str:
        """Initialize/Update piece that has a base-64 encoded JSON chord progression `chd` of (str) type. Returns a success / failure string
        Args:
            chp (str) : chord progression as over-encoded JSON
            bpm (float): BPM
            name (str): song name,
            id (int, optional) : if exists, id of song to replace.
        Returns:
            str : success / failure
        """
        try:
            chd = pickle.loads(base64.b64decode(chp))
            # return (chd[0])

            logger.info(f'initalize chd : {chd}') 

            name = name.replace(" ","")               

            mp = chdp.convert_to_mp(chd, bpm, name)
            
            nm = str(mp[0]).split('\n')[0][8:]
            chds = js.dumps(chd)

            if id is None:
                appfields.create_piece(mp,chd=chds)
            else: appfields.create_piece(mp,chd=chds,id=id)

            os.system(f"touch app/static/audio/{nm}.mp3")
            os.system(f"chmod ugo+rwx app/static/audio/{nm}.mp3")
            element.mp3(mp,f"app/static/audio/{nm}")

            element.save(mp,nm)

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