import logging
logger = logging.getLogger('root')

from musicpy import *
from musicpy.sampler import *
import numpy as np
import scipy.signal as sig

import matplotlib as mpl
from matplotlib import pyplot as plt
backend = plt.get_backend()
logger.info(f"MPL BACKEND: {backend}")
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from . import utils as ul
from . import chords as cd
import pretty_midi
import libfmp.c1
# from django.http import HttpResponse
import io
import base64


plt.switch_backend(backend)

tmp_dir = "/app/app/static/audio/tmp"

smp = sampler(6, name='sfz')
names = ['akai_steinway.sf2','akai_steinway.sf2','koto.sf2','shamisen.sf2','ruteki.sf2','air_gamelan.sf2']
for i in range(len(names)):
    logger.info(f"Loading : {names[i]}")
    smp.load(i,f'app/static/sfz/{names[i]}')

def load(midi):
    return mp.read(midi),pretty_midi.PrettyMIDI(midi)

def analyze(chord,width=5):

    chordNames = chord.chord_analysis(get_original_order=True)
    chords = chord.chord_analysis(get_original_order=True,mode='chords')

    bars = np.cumsum([np.sum(c.interval) for c in chords])
    
    kernel = np.ones((width,ul.n_keys))/(width*ul.n_keys)
    data = np.zeros((len(chordNames),ul.n_keys))
    for i in range(len(chordNames)):
        data[i,:] = cd.value(chordNames[i])
    data = sig.convolve2d(data, kernel, mode='same')
    
    return bars, chords, chordNames, data

def interpdata(top,bars,data,mt = 32):
    x = np.linspace(0,top,mt*top)
    sp = data.shape
    idata = np.zeros((top*mt,sp[1]))
    for i in range(sp[1]):
        idata[:,i] = np.interp(x,bars,data[:,i])
    return x,idata

def info(piece, i):
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
    bars, chords, chordNames, data = analyze(track)
    return bars, chords, chordNames, data, midi

def plot(bars,data,midi,tracklabel=0,fgz=(20,8)):
    sp = data.shape
    leg = []
    fig,ax = plt.subplots(2,1,figsize=fgz,sharex=True)
    gs = mpl.gridspec.GridSpec(nrows=2,ncols=1)
    gs.update(wspace=0.0, hspace=0.0, left=0.0, right=0.0, bottom=0.0, top=0.0) 
    for k in range(ul.n_keys):
        ax[0].plot(bars, data[:, k], c=ul.cs[k])
        leg.append(ul.keys[k])
    ax[0].legend(leg)
    ax[0].margins(0)
    ax[1].margins(0)
    score = libfmp.c1.c1s2_symbolic_rep.midi_to_list(midi)
    tfx = midi.get_downbeats()
    tf = lambda x: np.interp(x,tfx,list(range(len(tfx))))
    tfscore = [[tf(sc[0]),tf(sc[1]),sc[2],1,f'Track {tracklabel}'] for sc in score]
    libfmp.c1.visualize_piano_roll(tfscore, ax=ax[1])
    ax[1].set_ylabel("Note # / Pitch")
    ax[1].set_xlabel("bars / measures into the piece")
    ax[0].set_ylabel("value")
    plt.suptitle(f"Elementwise Graphs for Track {tracklabel}")
    # plt.show()
    response = img(fig)
    plt.close()
    return response
   
def plotall(piece : object, name : str) -> str:
    i = 0 # assume single-track songs for now...
    bars, chords, chordNames, data, midi = info(piece,i)
    return plot(bars,data,midi,tracklabel=f'{i} from {name}')

def img(fig):
    my_stringIObytes = io.BytesIO()
    fig.savefig(my_stringIObytes, format='jpg', dpi=160)
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read())
    # canvas=FigureCanvas(fig)
    # response=HttpResponse(content_type='image/png')
    # fig.savefig(response, format='png', dpi=600)
    # return response.content
    
            
def mp3(piece,name): 
    smp.export(obj=piece,mode='mp3',action='export',filename=f'{name}.mp3')
            
############################# testing methods / sandbox below / not part of API ###################

def _plot2(x,data,tracklabel=0,fgz=(20,8),title="Elementwise Graphs for Piece"):
    sp = data.shape
    leg = []
    fig = plt.figure(1,figsize=fgz)                     
    for k in range(ul.n_keys):
        plt.plot(x, data[:, k], c=ul.cs[k])
        leg.append(ul.keys[k])
    plt.legend(leg)
    plt.margins(0)
    plt.xlabel("bars / measures into the piece")
    plt.ylabel("value")
    plt.suptitle(title)
    plt.show()
    plt.close()
    
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
