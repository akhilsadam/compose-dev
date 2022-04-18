# types
import nltk
nltk.download('punkt')
from nrclex import NRCLex as nl
import numpy as np
import jpcm

keys = ['fear', 'anger', 'anticip', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy', 'anticipation']
cs = [jpcm.maps.murasaki,jpcm.maps.nakabeni,None,jpcm.maps.chigusa_iro,jpcm.maps.shinshu,jpcm.maps.sora_iro,jpcm.maps.kokushoku,
      jpcm.maps.benihibata,jpcm.maps.omeshi_onando,jpcm.maps.tomorokoshi_iro,jpcm.maps.enji_iro]
n_keys = len(keys)

def norm(v):
    return v/np.linalg.norm(v) if any(v) != 0 else v

def nlparse(tx):
    item = nl(text=tx)
    res = item.affect_frequencies
    rkeys = res.keys()
    effect = np.zeros(n_keys)
    for j in range(n_keys):
        key = keys[j]
        if key in rkeys:
            effect[j] = res[key]
    return norm(effect)

   
