import musicpy as mp

"""
[
    {
        'chd' : 'Cm7',
        'time': 0.5,
        'arp' : 1/8,
        'start': 0,
        'inst' : 'Acoustic Grand Piano'
    },
    {
        'chd' : 'Dsus',
        'time': 0.5,
        'arp' : 1/8,
        'start': 0.5,
        'inst' : 'Acoustic Grand Piano'
    },
    {
        'chd' : 'Caug7',
        'time': 0.5,
        'arp' : 1/8,
        'start': 1,
        'inst' : 'Acoustic Grand Piano'
    },
    {
        'chd' : 'Dadd2',
        'time': 0.5,
        'arp' : 1/8,
        'start': 1.5,
        'inst' : 'Acoustic Grand Piano'
    },
    {
        'chd' : 'Cm7',
        'time': 0.5,
        'arp' : 1/8,
        'start': 2,
        'inst' : 'Acoustic Grand Piano'
    },
    {
        'chd' : 'Dsus',
        'time': 0.5,
        'arp' : 1/8,
        'start': 2.5,
        'inst' : 'Acoustic Grand Piano'
    },
    {
        'chd' : 'Caug7',
        'time': 0.5,
        'arp' : 1/8,
        'start': 3,
        'inst' : 'Acoustic Grand Piano'
    },
    {
        'chd' : 'D,G,A,A# / Dadd2',
        'time': 0.5,
        'arp' : 1/4,
        'start': 3.5,
        'inst' : 'Acoustic Grand Piano'
    }
]
"""

class chdprogress:

    def convert_to_mp(chp : list, bpm : float=130, name: str='Progression 0') -> mp.piece:
        """Convert a song from JSON (really list of dictionaries) to a musicpy object

        Args:
            chp (list): _description_
            bpm (float): BPM to play the song at.

        Returns:
            mp.piece: musicpy piece from song
        """
        chord = [mp.C(i['chd']) % (i['time'], i['arp']) for i in chp]
        inst = [i['inst'] for i in chp]
        start = [i['start'] for i in chp]
        bpm, chdnotes, _ = mp.piece(chord,inst,bpm,start,['0']*len(chord)).merge()
        return mp.build(mp.track(chdnotes),bpm=bpm,name=name)
