import dask
import dask.array as da
import numpy as np

import logging
logger = logging.getLogger('root')

from . import chords

def toDask(data,chunks=(20,8)):
    a = da.from_array(data, chunks)
    return a
    
def chdSpace(L=2):
    a = np.vstack([c[3] for c in chords.chordbase])
    # data shape = n x 20
    # latent shape is L
    u,s,vh = np.linalg.svd(a)
    ut = u[:,:L]
    sh = np.diag(1/s)
    var = np.sum(np.power(s[:L],2))/np.sum(np.power(s,2))
    tfm = np.linalg.inv(vh)[:,:L] #np.matmul(np.linalg.inv(vh),sh)[:,:L]
    # print(var)
    # print(tfm)
    return var, tfm

def similarity(data1,data2):
    mu1 = np.mean(data1,axis=0)
    mu2 = np.mean(data2,axis=0)
