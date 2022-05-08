import logging
logger = logging.getLogger('root')

from app.options import options
from app.schema import *
from app.redisclient import redis_client, redis_client_raw

import pickle
from app.core import machine,element

import json as js
class appfields:

    def create_piece(obj,chd='-',**kwargs):
        """Create piece/song field in Redis.
        Args:
        obj (musicpy-piece object): complete song information without instrument timbre/frequencies
        chd (dict): JSON-style chord progression
        kwargs (optional) : optional arguments that further define the object.
        """
        rd = redis_client(3)
        rdr = redis_client_raw(4)
        n_keys = len(rd.keys())

        # fill this in with the rest!
        name = str(obj[0]).split('\n')[0][8:]
        logger.info(name)

        maps = {}
        maps |= kwargs
        maps |= {
        'name'  : name,                                 # piece name
        'chd'   : chd,                                  # chord progression as user defined... '-' for a direct mp object
        'bars'  : obj.bars(),                           # number of bars/measures in piece/song
        'bpm'   : obj.bpm,                              # piece/song BPM
        'time'  : obj.eval_time()                       # length of piece/song in seconds
        }

        rd.hset(n_keys,mapping=maps)
        rdr.set(n_keys, pickle.dumps(obj)) # musicpy object

    def create_chdTransform():
        """Make chord transformation matrix (right-applied) to transform from emotional values to a 2D PCA space.
            (Principal Component Analysis)
        """
        var, tfm, relations = machine.chdSpace() # PVE (proportion of explained variance in emotion space), matrix transformation
        rd = redis_client(2)
        rdr = redis_client_raw(2)

        rd.set('PVE', var)
        rdr.set('CHDTF', pickle.dumps(tfm))
        rd.set('PC-relations', js.dumps(relations))

    def create_eV_plots(id,update=False) -> str:
        """Make emotional value plots for song with integer id `id`; the `update` boolean will regenerate generated plots if True.
        """
        rdr = redis_client_raw(4)
        rd0 = redis_client(3)
        rd = redis_client_raw(7)
        name = f'{id}_0'
        if update:
            rd.delete(name)
        if rd.get(name) is None:
            try:
                piece = pickle.loads(rdr.get(id))
                nm = rd0.hget(id,'name')
                resp = element.plot(piece,nm)
                rd.set(name, resp)
                return str(resp)[:10]
            except Exception as E:
                msg = "Song not available; please check back later."
                logger.info(f"{msg} with exception:{E}")
                return f"{msg} Exited with exception: {E}"
        return "No Action Taken..."

    def create_eV_plot(i,update=False) -> str:
        """Make an emotional value plot for all songs; the `update` boolean will regenerate generated plots if True.
           If integer `i` is nonnegative, then only that song will be plotted.
        """
        rdr = redis_client_raw(4)
        rd0 = redis_client(3)
        rd = redis_client_raw(7)
        rd2 = redis_client(2)
        rdr2 = redis_client_raw(2)
        name = f'value_{i}' if i >=0 else 'value'
        if update:
            rd.delete(name)
        if rd.get(name) is None:
            try:
                pieces, names = [],[]
                keys = rdr.keys()
                kyz = []
                for key in keys:
                    try:
                        a = int(key)
                    except Exception:
                        pass
                    else:
                        kyz.append(a)
                if i >= 0 :
                    key = kyz[i]
                    logger.info(f'Get key {key}')
                    pieces.append(pickle.loads(rdr.get(key)))
                    names.append(rd0.hget(key,'name'))
                else:
                    for key in kyz:
                        logger.info(f'Get key {key}')
                        pieces.append(pickle.loads(rdr.get(key)))
                        names.append(rd0.hget(key,'name'))

                var = rd2.get('PVE')
                tfm = pickle.loads(rdr2.get('CHDTF'))
                relations = js.loads(rd2.get('PC-relations'))
                resp = element.plotPCA(var,tfm,relations,pieces,names)
                rd.set(name, resp)
                return str(resp)[:10]
            except Exception as E:
                msg = "Song not available; please check back later."
                logger.info(f"{msg} with exception:{E}")
                return f"{msg} Exited with exception: {E}"
        return "No Action Taken..."

