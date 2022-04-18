# very limited set, and basic approach (note we have not included 'disgust' which would arise from dissonance!)
from . import utils as ul
import numpy as np
# need to iterate top-down to select properly
def obj(inp):
    inp.append(ul.nlparse(inp[2]))
    return np.array(inp, dtype=object)

chordbase = np.array([
    obj([['add2'],'Added Second','listless, spacey']),
    obj([['add4'],'Added Fourth','restless, dissonant']),
    obj([['add9'],'Added Ninth','steeliness, austerity']),
    obj([['sus','sus4','suspended'],'Suspended Fourth','delightful tension']),
    obj([['9','ninth'],'Regular Ninth','openness, optimism']),
    obj([['aug','augmented fourth'],'Tritone / Augmented 4th','violence, danger, tension, devilishness (of course!)']),
    obj([['dim','diminished'],'Diminished','fear, shock, spookiness, suspense']),
    obj([['♭9','minor ninth'],'Seventh with Minor Ninth','creepiness, ominousness, fear, darkness']),
    obj([['maj2','major second'],'Major 2nd','pleasurable longing, displeasure']),
    obj([['maj3','major third'],'Major 3rd','joy, happiness, brightness']),
    obj([['maj6','major sixth'],'Major 6th','winsomeness, pleasurable longing']),
    obj([['maj7','major seventh'],'Major Seventh','romance, softness, jazziness, serenity, tranquillity, exhilaration, aspiration, displeasure, violent longing']),
    obj([['maj','major'],'Major','happiness, cheerfulness, confidence, brightness, satisfaction']),
    obj([['m2','minor second'],'Minor Second','melancholy, displeasure, anguish, darkness']),
    obj([['m3','minor third'],'Minor Third','tragedy, sadness']),
    obj([['m6','minor sixth'],'Minor Sixth','anguish, sadness']),
    obj([['m7','minor seventh'],'Minor Seventh','mellowness, moodiness, jazziness']),
    obj([['m','minor'],'Minor','sadness, darkness, sullenness, apprehension, melancholy, depression, mystery']),
    obj([['P5','perfect fifth'],'Perfect Fifth','cheerfulness, stability']),
    obj([['P4','perfect fourth'],'Perfect Fourth','buoyancy, pathos']),
    obj([['P8','octave','unison'],'Octave','Lightheartedness (i.e., sudden melodic leap)']),
    obj([['7','seventh'],'Seventh Power','funkiness, soulfulness, moderate edginess']),
    obj([['omit','power chord'],'Power Chord','Power']),
    obj([['note'],'Single Note','']),
])

def value(chd):
    for c in chordbase:
        items = c[0]
        for item in items:
            if item in chd:
                return c[3]
    print(f"[ERROR]: Chord Type Unknown for Chord {chd}")
    return np.array(ul.n_keys)

