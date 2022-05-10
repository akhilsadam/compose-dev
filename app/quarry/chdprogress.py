import pickle
import musicpy as mp
import json as js
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
