import sys, numpy as np, soundfile as sf, json
sys.path.insert(0,'/home/claude/fable')
from lines import LINES, VOICE
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/tts/kokoro.onnx','/home/claude/tts/voices.bin')
SR=24000
def gen(spk, text):
    v, sp, pf, g = VOICE[spk]
    a, sr = k.create(text, voice=v, speed=sp, lang="en-us")
    if pf != 1.0:  # resample: pitch+tempo shift
        n = int(len(a)/pf); a = np.interp(np.linspace(0, len(a)-1, n), np.arange(len(a)), a)
    return a*g
meta={}
for lid, spk, text in LINES:
    if spk == "SPARROWS":
        parts=[gen(s, text) for s in ("PIP","PIM","PIO")]
        n=max(len(p) for p in parts)+1200; a=np.zeros(n)
        for i,p in enumerate(parts): a[i*500:i*500+len(p)]+=p*0.6
    else:
        a = gen(spk, text)
    # trim silence
    idx=np.where(np.abs(a)>0.01)[0]
    a=a[max(0,idx[0]-240):idx[-1]+480]
    sf.write(f'/home/claude/fable/vo/{lid}.wav', a, SR)
    meta[lid]=dict(spk=spk, dur=len(a)/SR)
    print(lid, spk, round(len(a)/SR,2))
json.dump(meta, open('/home/claude/fable/vo/meta.json','w'), indent=0)
