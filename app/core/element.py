import logging

import matplotlib
logger = logging.getLogger('root')

from musicpy import *
from musicpy.sampler import *
import numpy as np
import scipy.signal as sig

import matplotlib as mpl
from matplotlib import pyplot as plt
backend = plt.get_backend()
logger.info(f"MPL BACKEND: {backend}")

from . import utils as ul
from . import chords as cd
import pretty_midi
import libfmp.c1
from . import machine as mx

from . import analyze as anly

plt.switch_backend(backend)

tmp_dir = "/app/app/static/audio/tmp"

try: smp
except NameError:
    smp = sampler(6, name='sfz')
    names = ['akai_steinway.sf2','akai_steinway.sf2','koto.sf2','shamisen.sf2','ruteki.sf2','air_gamelan.sf2']
    for i in range(len(names)):
        logger.info(f"Loading : {names[i]}")
        smp.load(i,f'app/static/sfz/{names[i]}')

def load(midi:str) -> list:
    """Loads a midi file into the framework

    Args:
        midi (str): path to midifile

    Returns:
        list: musicpy object, and prettyMidi object with the midi data
    """
    return mp.read(midi),pretty_midi.PrettyMIDI(midi)

def analyze(chord:mp.track, type:int, width:int=1) -> list:
    """Run Chord Analysis and get emotional vector data

    Args:
        chord (mp.track): musicpy track to run analysis on
        type (int): is this a progression or a full song?
        width (int, optional): kernel width for postprocessing analysis. Defaults to 1.

    Returns:
        list: chord start times, chords as mp objects, chord names, and the emotional value matrix (not regular in time)
    """
    chordNames = chord.chord_analysis(get_original_order=True, is_chord=(type==1))
    chords = chord.chord_analysis(get_original_order=True,mode='chords',is_chord=(type==1))

    bars = np.cumsum([np.sum(c.interval) for c in chords])
    
    kernel = np.ones((width,ul.n_keys))/(width*ul.n_keys)
    data = np.zeros((len(chordNames),ul.n_keys))
    for i in range(len(chordNames)):
        data[i,:] = cd.value(chordNames[i])
    data = sig.convolve2d(data, kernel, mode='same')
    
    return bars, chords, chordNames, data

def interpdata(top:float,bars:list,data:np.array,mt:int = 32) -> list:
    """Interpolate emotional value data to make a matrix

    Args:
        top (float):  total length of piece in bars
        bars (list):  chord start times in bars
        data (np.array): emotional value data
        mt (int, optional): Discretization size in 1/bars. Defaults to 32.

    Returns:
        list: returns x-values and matrix
    """
    x = np.linspace(0,top,mt*top)
    sp = data.shape
    idata = np.zeros((top*mt,sp[1]))
    for i in range(sp[1]):
        idata[:,i] = np.interp(x,bars,data[:,i])
    return x,idata

def info(piece:mp.piece, type:int, i:int=0) -> list:
    """Get all information from a single track of a piece.

    Args:
        piece (object): piece to get data from
        type (int): chord progression or not? (bool, really)
        i (int, optional): the particular track of interest.

    Returns:
        list: all informations (self-explanatory)
    """
    track = piece.tracks[i]
    name = f'{tmp_dir}{i}.mid'
    write(track,
      bpm=piece.bpm,
      channel=0,
      start_time=None,
      name=name,
      instrument=None,
      i=None,
      save_as_file=True,
      msg=None,
      nomsg=False,
      deinterleave=False,
      remove_duplicates=False)
    midi = pretty_midi.PrettyMIDI(name)
    bars, chords, chordNames, data = analyze(track, type)
    return bars, chords, chordNames, data, midi

def save(piece:mp.piece,nm:str):
    """Save a piece to midi.

    Args:
        piece (mp.piece): piece to save.
        nm (str): name of piece.
    """
    track = piece.tracks[0]
    name = f'/app/app/core/midi/{nm}.mid'
    write(track,
      bpm=piece.bpm,
      channel=0,
      start_time=None,
      name=name,
      instrument=None,
      i=None,
      save_as_file=True,
      msg=None,
      nomsg=False,
      deinterleave=False,
      remove_duplicates=False)


def _plot2(ax:object,x:np.array,data:np.ndarray):
    """Helper plot function for ev plots

    Args:
        ax (object): axes of figure
        x (np.array): x-values
        data (np.array): emotional value matrix
    """
    leg = []                    
    for k in range(data.shape[1]):
        ax.plot(x, data[:, k], c=ul.cs[k])
        leg.append(ul.keys[k])
        
def plotPCA(var: float,tfm: np.ndarray,relations:list,pieces : list, names : list, types : list, fgz: list = (16,16)) -> str:
    """Plot emotional value on a latent space of emotion using a PCA transformation defined by the chordbase dictionary set (i.e. what can possibly be explained by the chords).

    Args:
        var (float): Percentage of Variance in emotion-space explained by the chords (PVE)
        tfm (np.ndarray): V matrix from SVD - the PCA transformation matrix
        relations (list): list of most related axes to latent space axes
        pieces (list): pieces to plot
        names (list): names of pieces
        types (list): chord progressions or not? (bools, really)
        fgz (list, optional): figure size. Defaults to (16,16).

    Returns:
        str: Base64 encoded image
    """
    ys = []
    plt.rcParams.update({'font.size': 16})
    for piece,type in zip(pieces,types):
        _, yun = get_data(piece, type)
        y = np.matmul(yun,tfm)
        # logger.info(f'PCA shape: {y.shape}')
        ys.append(y)
    fig = plt.figure(figsize = fgz)
    for i in range(len(pieces)):
        plt.scatter(ys[i][:,0],ys[i][:,1])
    plt.legend(names)
    plt.xlabel(f'Principal Component #1 - {relations[0]}')
    plt.ylabel(f'Principal Component #2 - {relations[1]}')
    plt.title(f'Pieces as a Distribution on a 2D PC Space \n(explains {int(1000*float(var))/10}% of the variance in chordspace)\
    \nspacing between points represents time due to constant slice rate of 32 pts / bar; traversal direction not shown')
    response = ul.img(fig)
    plt.close()
    return response
    
def get_data(piece : object, type: int, mt : int = 32) -> list:
    """Get emotional value data from piece

    Args:
        piece (object): piece to get data from
        type (int): chord progression or not? (bool, really)
        mt (int, optional): Discretization size in 1/bars. Defaults to 32.

    Returns:
        list: x-values and y-values for emotional value matrix
    """
    datas = []
    barlist = []
    for i in range(len(piece.tracks)):
        bars, _,_, data, _ = info(piece,type,i)
        datas.append(data)
        barlist.append(bars)
    #################    
    top = int(piece.bars()+1)
    dataf = np.zeros((top*mt,ul.n_keys))
    xc = [1]
    #################
    for bars,data in zip(barlist,datas):
        x, idata = interpdata(top,bars,data,mt=mt)
        dataf = dataf + idata
        xc[0] = x
    return xc[0],dataf

def plot(piece : object, name : str, type: int, mt : int = 32, fgz: list = (20,8)) -> str:
    """Plot emotional value for a single song

    Args:
        piece (object): piece to plot
        name (str): name of piece
        type (int): chord progression or not? (bool, really)
        mt (int, optional): Discretization size in 1/bars. Defaults to 32.
        fgz (list, optional): figure size. Defaults to (20,8).

    Returns:
        str: Base64 encoded image string
    """
    plt.rcParams.update({'font.size': 12})
    leg = ul.keys
    fig,ax = plt.subplots(2,1,figsize=fgz,sharex=True)
    gs = mpl.gridspec.GridSpec(nrows=2,ncols=1)
    gs.update(wspace=0.0, hspace=0.0, left=0.0, right=0.0, bottom=0.0, top=0.0) 
    #################    
    datas = []
    barlist = []
    for i in range(len(piece.tracks)):
        bars, _, _, data, _ = info(piece,type,i)
        datas.append(data)
        barlist.append(bars)
    #################    
    top = int(piece.bars()+1)
    dataf = np.zeros((top*mt,ul.n_keys))
    xc = [1]
    #################
    for bars,data in zip(barlist,datas):
        x, idata = interpdata(top,bars,data,mt=mt)
        dataf = dataf + idata
        xc[0] = x
    #################
    _plot2(ax[0],xc[0],dataf)
    ################# 
    ax[0].legend(leg)
    ax[0].margins(0)
    ax[1].margins(0)
    midi = pretty_midi.PrettyMIDI(f'/app/app/core/midi/{name}.mid')
    score = libfmp.c1.c1s2_symbolic_rep.midi_to_list(midi)
    tfx = midi.get_downbeats()
    tf = lambda x: np.interp(x,tfx,list(range(len(tfx))))
    tfscore = [[tf(sc[0]),tf(sc[1]),sc[2],1,f'{name}'] for sc in score]
    libfmp.c1.visualize_piano_roll(tfscore, ax=ax[1])
    ax[1].set_ylabel("Note # / Pitch")
    ax[1].set_xlabel("bars / measures into the piece")
    ax[0].set_ylabel("value")
    plt.suptitle(f"Elementwise Graphs for {name}")
    #################
    response = ul.img(fig)
    plt.close()
    #################
    return response    
            
def plotST(piece : object, name : str, type: int, fgz: list = (20,8)) -> str:
    """Plot st and dst for a single song

    Args:
        piece (object): piece to plot
        name (str): name of piece
        type (int): chord progression or not? (bool, really)
        fgz (list, optional): figure size. Defaults to (20,8).

    Returns:
        str: Base64 encoded image string
    """
    plt.rcParams.update({'font.size': 12})
    fig,ax = plt.subplots(3,1,figsize=fgz,sharex=True)
    gs = mpl.gridspec.GridSpec(nrows=3,ncols=1)
    gs.update(wspace=0.0, hspace=0.0, left=0.0, right=0.0, bottom=0.0, top=0.0) 
    #################    
    cs, state, intervals, stcoord, d_st = anly.all(piece, type)
    #################
    _plot2(ax[0],list(range(len(d_st))),d_st)
    _plot2(ax[1],list(range(len(stcoord))),np.vstack([stcoord[:,0,0],stcoord[:,0,1],stcoord[:,1,0],stcoord[:,1,1],stcoord[:,2,0],stcoord[:,2,1],stcoord[:,3,0],stcoord[:,3,1]]).T)
    _plot2(ax[2],list(range(len(stcoord))),np.vstack([state[:,0],state[:,2],state[:,3],state[:,4]]).T)
    ################# 
    ax[0].legend(["ds1","dt1","ds2","dt2","ds3","dt3","ds4","dt4"])
    ax[1].legend(["s1","t1","s2","t2","s3","t3","s4","t4"])
    ax[2].legend(["current-key","chord-key","quality: interval_1","quality: interval_2"])
    ax[0].margins(0)
    ax[1].margins(0)
    ax[2].margins(0)
    ax[2].set_ylabel("state\n(state-vector representation)")
    ax[2].set_xlabel("chords into the piece")
    ax[0].set_ylabel("dST\n(d/dt of ST)")
    ax[1].set_ylabel("ST\n(4-interval representation of state)\nusing Mobius ST parametrization")
    ax[0].set_title(f"Derivative-Representation for {name}\n(ST coordinate Graphs)")
    #################
    response = ul.img(fig)
    plt.close()
    #################
    return response

def mp3(piece:mp.piece,name:str): 
    """Generate an MP3 file on disk

    Args:
        piece (mp.piece): piece object to save
        name (str): filename
    """
    smp.export(obj=piece,mode='mp3',action='export',filename=f'{name}.mp3')
            
############################# testing methods / sandbox below / not part of API ###################

    
def _plotAll(piece,mt=32,fgz=(20,4)):
    datas = []
    barlist = []
    for i in range(len(piece.tracks)):
        bars, chords, chordNames, data, midi = info(piece,i)
        plot(bars,data,midi,tracklabel=i)
        datas.append(data)
        barlist.append(bars)
    #################    
    top = int(piece.bars()+1)
    dataf = np.zeros((top*mt,ul.n_keys))
    xc = [1]
    for bars,data in zip(barlist,datas):
        x, idata = interpdata(top,bars,data,mt=mt)
        dataf = dataf + idata
        xc[0] = x
    plot2(xc[0],dataf,tracklabel=0,fgz=fgz)
    marray = np.repeat(np.reshape(np.transpose(np.mean(dataf,axis=1)),[top*mt,1]),ul.n_keys,axis=1)
    fig = plt.figure(1,figsize=fgz)
    plt.plot(xc[0],marray)
    plt.xlabel("bars / measures into the piece")
    plt.ylabel("value")
    plt.margins(0)
    plt.suptitle("Elementwise Graphs for Piece: Average Intensity")
    plt.show()
    plt.close()
    plot2(xc[0],dataf -marray,tracklabel=0,fgz=fgz,title="Elementwise Graphs for Piece - Demeaned")
    return xc[0], dataf
