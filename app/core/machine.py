import numpy as np

import logging
logger = logging.getLogger('root')

from . import chords
from . import utils as ul

def chdSpace(L:int=2) -> list:
    """Make PCA transformation using SVD for list of chords in chordbase (using the emotional vector data)

    Args:
        L (int, optional): Number of latent space axis. Defaults to 2.

    Returns:
        list: PVE, transformation matrix, axis relations (see element.plotPCA for more)
    """
    a = np.vstack([c[3] for c in chords.chordbase])
    # data shape = n x 20
    # latent shape is L
    # we do a sign flip twice to maintain consistency with a more readable result
    u,s,vh = np.linalg.svd(a)
    ut = u[:,:L]
    sh = np.diag(1/s)
    var = np.sum(np.power(s[:L],2))/np.sum(np.power(s,2))
    v = np.linalg.inv(vh)[:,:L] #np.matmul(np.linalg.inv(vh),sh)[:,:L]
    ##### get pc axis components (first n)
    n = 3
    relations = [f'related to {", ".join(ul.keys[np.argsort((v[:,i]))[-n:]])}\n in amounts {v[np.argsort((v[:,i]))[-n:],i]}' for i in range(L)]
    # print(var)
    # print(tfm)
    return var, v, relations

# def similarity(data1,data2):
#     mu1 = np.mean(data1,axis=0)
#     mu2 = np.mean(data2,axis=0)
