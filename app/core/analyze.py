import numpy as np
from scipy import stats
import musicpy as mp
from . import utils as ul

import logging
logger = logging.getLogger('root')

from matplotlib import pyplot as plt
backend = plt.get_backend()
logger.info(f"MPL BACKEND: {backend}")
import jpcm
plt.switch_backend(backend)

from app.redisclient import redis_client

#### st coordinate definition:
def alp(R:float,r:float,t:np.array) -> np.array:
    """Define the lower curve for a Mobius strip with parametrization.

    Args:
        R (float): outer-radius  
        r (float): inner-radius
        t (np.array): theta

    Returns:
        np.array: lower curve positions in XYZ
    """
    A = R + r*np.cos(0.5*t)
    return np.array([A*np.cos(t),A*np.sin(t),r*np.sin(0.5*t)])
def beta(R:float,r:float,t:np.array) -> np.array:
    """Define the upper curve for a Mobius strip with parametrization.

    Args:
        R (float): outer-radius  
        r (float): inner-radius
        t (np.array): theta

    Returns:
        np.array: upper curve positions in XYZ
    """
    B = R + r*np.cos(np.pi+0.5*t)
    return np.array([B*np.cos(t),B*np.sin(t),r*np.sin(np.pi+0.5*t)])
def sig(s:np.array,t:np.array,R:float,r:float) -> np.array:
    """Define a Mobius strip with parametrization.

    Args:
        s (np.array): height (lerping parameter between the upper and lower curves)
        t (np.array): theta
        R (float): outer-radius  
        r (float): inner-radius

    Returns:
        np.array: positions in XYZ
    """
    return (1-s)*alp(R,r,t) + s*beta(R,r,t)
####


def makeLibrary() -> list:
    """make dictionaries for transformations / mappings.

    Returns:
        dict: uv to XYZ coordinate transform (uv are keys)
        dict: uv to ST coordinate transform (uv are keys)
        str: base64 image of unit element on mobius mapping
    """
    u,v = np.mgrid[0:11:12j, 0:11:12j]
    u=u.flatten()
    v=v.flatten()
    #### make x,y (local coordinates) `non-repl st`
    v2 = (6 + v)%12
    x = (u + (v2%12 - 6))
    y = (-u + v2)
    #### make vectors
    ix = (y<=6) & (x>=0) & (x<12) & (y>=-6)
    u = u[ix]
    v = v[ix]
    x = x[ix]
    y = y[ix]
    #### make st and dictionaries along with plot
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter(x,y,c=jpcm.maps.rurikon)
    uvXYZ = {}
    uvST ={}
    for i, txt in enumerate(x):
        ax.annotate(f'{int(u[i])}:{int(v[i])}', (x[i], y[i]))
        s = (y[i]+6)/12
        t = 2*np.pi*(x[i]/12)
        uvXYZ[f'{int(u[i])}:{int(v[i])}'] = sig(s,t,1,1)
        uvXYZ[f'{int(v[i])}:{int(u[i])}'] = sig(s,t,1,1)
        uvST[f'{int(u[i])}:{int(v[i])}'] = [s,t]
        uvST[f'{int(v[i])}:{int(u[i])}'] = [s,t]
    ax.set_ylabel('y, or s (remapped to 0-1)')
    ax.set_ylabel('x, or t (theta) (remapped to 0-2pi)')
    plt.title("Interval UV coordinate to ST coordinate Mapping")
    return uvXYZ,  uvST, ul.img(fig)

try: uvXYZ
except NameError:
    try:
        uvXYZ = redis_client(2).get('uvXYZ')
        uvST = redis_client(2).get('uvST')
    except Exception as e:
        uvST, uvXYZ, im_interval = makeLibrary()
        redis_client(2).set('uvXYZ',uvXYZ)
        redis_client(2).set('uvST',uvST)
        redis_client(2).set('im_interval',im_interval)

#### NOW for classification and transformation functions.

nms = np.array(['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']) ## helper data

def key_chord(chordname:str) -> object:
    """Convert all notes and chord (names) to a well-defined string representation of the current key (using 2 characters).

    Args:
        chordname (str): the chord name from musicpy

    Returns:
        object: either a list of strings or a string representing the key without overall pitch
    """
    cname = chordname
    if 'note' in cname:
        cname = chordname.replace('note','').replace(' ','')
    nm = cname[0]
    if cname[1] == '#':
        nm += '#'
    if nm in nms:
        return mp.note_to_degree(nm)%12
    if '[' in cname:
        # a of b style
        a,b = cname.split(']/[')
        return [key_chord(b),key_chord(a[1:])]
    return 'ERROR'

def current_key(keys:list,w:int=8)->np.array:
    """Perform a moving mode on the keys list to get a value for the `current key`.

    Args:
        keys (list): immediate key value
        w (int, optional): size of moving filter. Defaults to 8.

    Returns:
        np.array: current key
    """
    n = len(keys)
    out =  [stats.mode(keys[max(i-w,0):i+1,1])[0][0] for i in range(n)]
    return np.array(out).astype(int)

def quality(cs:object) -> np.ndarray:
    """Generate the quality matrix from the chord-progression
    Args: 
        cs (musicpy chord object): input chord-progression
    Returns:
        np.ndarray : 3-column quality matrix
    """
    q = np.zeros(shape=(len(cs),3))
    for i in range(len(cs)):
        c = cs[i]
        d = np.unique(c.get_degree())
        a = min(d)
        e = (d-a)%12
        q[i,0] = 0
        q[i,1] = e[1] if len(e) > 1 else 0
        q[i,2] = e[len(e)-1]
    return q

def toST(intervals:np.ndarray):
    """Convert interval matrix to a ST-coordinate matrix (both np.ndarray elements)"""
    return np.array([[uvST[rc] for rc in row] for row in intervals]) ### 4 (s,t) pairs for each chord element.
    
def dST(stcoord:np.ndarray):
    """simple differencing of the st coordinates (the input). 
    Returns a flattened difference array (both np.ndarray objects) with one less point (due to differencing)"""
    out = stcoord[1:] - stcoord[:-1]
    out = np.array([np.concatenate([out[i,:,0],out[i,:,1]]) for i in range(len(out))])
    return out

#### route requests

def all(piece:mp.piece) -> list:
    """_summary_

    Args:
        piece (mp.piece): _description_

    Returns:
        list: _description_
    """
    t1 = piece.tracks[0]
    cs = mp.chord_analysis(t1,mode='chords')
    keys = [key_chord(mp.detect(c,mode='chord')) for c in cs]
    keys = np.array([a if isinstance(a,list) else [0,a] for a in keys])
    c_key = current_key(keys)
    state = np.vstack([c_key,keys.T,quality(cs).T]).T
    intervals = np.vstack([[f"{int(state[i,0])}:{int(state[i,1])}",f"{int(state[i,1])}:{int(state[i,2])}",
            f"{int(state[i,3])}:{int(state[i,4])}",f"{int(state[i,4])}:{int(state[i,5])}"] for i in range(len(state))])
    stcoord = toST(intervals)
    d_st = dST(stcoord)
    return cs, state, intervals, stcoord, d_st

