import os
import musicpy as mp
import app.core.element as element
import numpy as np
import app.quarry.appfields as apf
import app.core.analyze as anly
"""
An example of format:
{
	"name": "Progression 0",
	"bpm": 174,
	"chord": [{
			"chd": "Cm7",
			"duration": 0.5,
			"interval": 0.125,
			"start": 0,
			"inst": "Acoustic Grand Piano"
		},
		{
			"chd": "Dsus",
			"duration": 0.5,
			"interval": 0.125,
			"start": 0.5,
			"inst": "Acoustic Grand Piano"
		},
		{
			"chd": "Caug7",
			"duration": 0.5,
			"interval": 0.125,
			"start": 1,
			"inst": "Acoustic Grand Piano"
		},
		{
			"chd": "Dadd2",
			"duration": 0.5,
			"interval": 0.125,
			"start": 1.5,
			"inst": "Acoustic Grand Piano"
		},
		{
			"chd": "Cm7",
			"duration": 0.5,
			"interval": 0.125,
			"start": 2,
			"inst": "Acoustic Grand Piano"
		},
		{
			"chd": "Dsus",
			"duration": 0.5,
			"interval": 0.125,
			"start": 2.5,
			"inst": "Acoustic Grand Piano"
		},
		{
			"chd": "Caug7",
			"duration": 0.5,
			"interval": 0.125,
			"start": 3,
			"inst": "Acoustic Grand Piano"
		},
		{
			"chd": "D,G,A,A# / Dadd2",
			"duration": 0.5,
			"interval": 0.25,
			"start": 3.5,
			"inst": "Acoustic Grand Piano"
		}
	]
}
"""

class chdprogress:

    def convert_to_mp(chp : list, bpm : float=138, name: str='Progression 0') -> mp.piece:
        """Convert a chord-progression from a dict `chd` to a musicpy object

        Args:
            chp (list): chord progression
            bpm (float): BPM to play the song at.

        Returns:
            mp.piece: musicpy piece from chord progression
        """
        chord = [mp.C(i['chd']) % (i['duration'], i['interval']) for i in chp]
        inst = [i['inst'] for i in chp]
        start = [i['start'] for i in chp]
        bpm, chdnotes, _ = mp.piece(chord,inst,bpm,start,['0']*len(chord)).merge()
        return mp.build(mp.track(chdnotes),bpm=bpm,name=name)
		
    def genNULL(piece : object, name : str, type: int) -> str:
        """Make a progression with the nullspace of another song

		Args:
			piece (object): piece to plot
			name (str): name of piece
			type (int): chord progression or not? (bool, really)

		Returns:
			str: path to generated song
		"""
        cs, state, intervals, stcoord, d_st = anly.all(piece, type)
        bars, chords, _, data = element.analyze(piece.tracks[0], type)
        # get matrix transformation
        dst = np.zeros(shape=(d_st.shape[0]+1,d_st.shape[1]))
        dst[1:,:] = d_st
        A = np.linalg.lstsq(data,dst,rcond=None)[0] # A matrix
		## get output d_st
        data_const = np.ones(shape=data.shape)
		# raise ValueError(A.shape)
        dst_out = np.matmul(data_const,A)
		## output st
        stout = np.cumsum(dst_out,axis=0)[1:,:]
        ks = ((stout[:,1::2]) / (2*np.pi))
        ts = np.mod((stout[:,1::2]), (2*np.pi))
        fz = np.vectorize(lambda x: ((2-x) if x > 1 else (-x if x < 0 else x)))
        s4s = fz(stout[:,0::2])
		## 
        st1 = np.array([(s4s[:,0]-0.5)*(1-2*ks[:,0])+0.5, ts[:,0]]).T
        st2 = np.array([(s4s[:,1]-0.5)*(1-2*ks[:,1])+0.5, ts[:,1]]).T
        st3 = np.array([(s4s[:,2]-0.5)*(1-2*ks[:,2])+0.5, ts[:,2]]).T
        st4 = np.array([(s4s[:,3]-0.5)*(1-2*ks[:,3])+0.5, ts[:,3]]).T
		#
        uvST = anly.getLibrary()[1]
		#
        minval = lambda stv: min(zip(uvST.keys(),uvST.values()),key=lambda x: np.sum(np.power((x[1][1] - stv),2)))[0] # quick way to get closest match
		##
        key = np.array([int(minval(i).split(':')[0]) for i in st1]) + 57 # A3 is base note
        n1 = np.array([int(minval(i).split(':')[1]) for i in st2]) + key
        n2 = np.array([int(minval(i).split(':')[1]) for i in st3]) + n1
        n3 = np.array([int(minval(i).split(':')[1]) for i in st4]) + n1
		# make output
        times = np.zeros(shape=(len(bars)+1))
        times[1:] = bars
        durs = times[1:]-times[:-1]
        chds = [(mp.degrees_to_chord(ls = [k,n11,n21,n31],duration=[dur]*4)) for k,n11,n21,n31,dur in zip(key,n1,n2,n3,durs)]
        bpm, chdnotes, _ = mp.piece(chds,bpm=piece.bpm,start_times=times[:-1]).merge()
        track = mp.track(chdnotes)
        
        pcz = mp.build(track,bpm=bpm,name=name)

        try: apf.appfields.create_piece(pcz)
        except:
            pass # just ignore the exception for now, since it does not affect user experience...

        os.system(f"touch app/static/audio/{name}.mp3")
        os.system(f"chmod ugo+rwx app/static/audio/{name}.mp3")
        element.mp3(pcz,f"app/static/audio/{name}")

        element.save(pcz,name)
  
        return "Success"
		
