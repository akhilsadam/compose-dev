# types
import nltk
nltk.download('punkt')
from nrclex import NRCLex as nl
import numpy as np
from matplotlib import pyplot as plt
backend = plt.get_backend()
import jpcm
plt.switch_backend(backend)
import io,base64

keys = ['fear', 'anger', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy', 'anticipation']
cs = [jpcm.maps.murasaki,jpcm.maps.nakabeni,jpcm.maps.chigusa_iro,jpcm.maps.shinshu,jpcm.maps.sora_iro,jpcm.maps.kokushoku,
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

def img(fig):
    my_stringIObytes = io.BytesIO()
    fig.savefig(my_stringIObytes, format='jpg', dpi=160)
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read())
    # canvas=FigureCanvas(fig)
    # response=HttpResponse(content_type='image/png')
    # fig.savefig(response, format='png', dpi=600)
    # return response.content

def draw(inp,name,figsize=(10,8)):
    fig=plt.figure(figsize=figsize)
    if len(inp.shape)==2:
        for i in inp.shape[1]:
            plt.plot(inp[:,i], c=cs[i])
        if inp.shape[1]==n_keys:
            plt.legend(keys)
        else:
            plt.legend(list(range(inp.shape[1])))
        plt.ylabel(name)
        plt.title(name)
        plt.xlabel('X')
        out = img(fig)
        plt.close()
    return out