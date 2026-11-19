"""Episode 02 soundtrack: reuses audio.py (cues, ambience, mix levels) and adds a few new sfx."""
import sys
sys.path.insert(0, '/home/claude/fable')
import numpy as np, soundfile as sf, importlib
import audio
from audio import SR, tvec, noise, lowpass, highpass, drum, tick, place, addv

_base_sfx = audio.sfx
def sfx(name):
    if name == 'patter':
        out = np.zeros(int(1.2*SR))
        for k in range(14): place(out, tick(0.03, 0.25)+0, k*0.08)
        return out
    if name == 'achoo':
        t = tvec(0.5); return lowpass(noise(0.5), 0.15)*np.exp(-t*7)*1.2
    if name == 'thud': return addv(drum(0.35, 60, 0.9), lowpass(noise(0.3), 0.05)*np.exp(-tvec(0.3)*10)*1.2)
    if name == 'nibble':
        out = np.zeros(int(0.85*SR))
        for k in range(7): place(out, tick(0.025, 0.35), k*0.11)
        return out
    if name == 'snip': return addv(tick(0.05, 0.9), drum(0.08, 900, 0.25))
    return _base_sfx(name)
audio.sfx = sfx

if __name__ == '__main__':
    order = [('sc_ep02', f) for f in ('s1', 's2', 's3', 's4', 's5', 's6', 's7')]
    parts = []
    for m, f in order:
        S = getattr(importlib.import_module(m), f)()
        a = audio.scene_audio(S); parts.append(a); print(f, round(len(a)/SR, 2), flush=True)
    full = np.concatenate(parts)
    full = full/np.max(np.abs(full))*0.9
    sf.write('/home/claude/fable/out/soundtrack.wav', full, SR)
    print('total', len(full)/SR)
