"""Episode 03 soundtrack: reuses audio.py (cues, mix levels) and adds wind ambience, birds and a few sfx.
Ambience is also ducked under dialogue so background stays well under speech."""
import sys
sys.path.insert(0, '/home/claude/fable')
import numpy as np, soundfile as sf, importlib
import audio, audio2
from audio import SR, tvec, noise, lowpass, highpass, drum, tick, place, addv, pad, pluck, hz, mbox

def _ramp(t, a, b): return np.clip((t-a)/(b-a), 0, 1)
def _wind(d, level, seed=0):
    r = np.random.default_rng(seed); n = int(d*SR); t = np.arange(n)/SR
    x = r.standard_normal(n)
    lo = lowpass(x, 0.01); band = lo-lowpass(lo, 0.002)
    band = band/(np.std(band)+1e-9)
    howl = np.sin(2*np.pi*(210+60*np.sin(2*np.pi*0.13*t))*t)*0.08
    mod = 0.65+0.35*np.sin(2*np.pi*0.21*t+1)*np.sin(2*np.pi*0.07*t)
    return (band+howl)*mod*level

def amb(name, d):
    n = int(d*SR); t = np.arange(n)/SR
    if name == 'wind_soft_on': return _wind(d, 0.22, 1)
    if name == 'wind_strong_on':
        env = np.clip(0.55*_ramp(t, 0.2, 1.4)+0.45*_ramp(t, 5.4, 9.0), 0, 1)*(1-0.9*_ramp(t, 22.8, 24.6))
        return _wind(d, 0.4, 2)*(0.15+0.85*env)
    if name == 'birds_on':
        out = np.zeros(n); r = np.random.default_rng(7); tt = 0.5
        while tt < d-1:
            f0 = r.uniform(2800, 4200); k = r.integers(2, 5)
            for j in range(k):
                dd = r.uniform(0.05, 0.1); tv = tvec(dd); f = f0*(1+0.25*np.sin(np.pi*tv/dd))
                place(out, np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*tv/dd)*0.25, tt+j*0.12)
            tt += r.uniform(1.2, 3.0)
        return out
    return audio.amb(name, d)

_base_sfx = audio2.sfx
def sfx(name):
    if name == 'step': return lowpass(drum(0.14, 95, 0.5), 0.2)
    if name == 'inhale':
        d = 1.8; t = tvec(d); return highpass(noise(d), 0.3)*(t/d)**1.5*np.sin(np.pi*np.clip(t/d, 0, 1))**0.3*0.35
    if name == 'chatter':
        out = np.zeros(int(1.0*SR))
        for k in range(22): place(out, tick(0.02, 0.45), k*0.042)
        return out
    if name == 'chime':
        d = 2.0; t = tvec(d); s = np.zeros_like(t)
        for f, a in ((hz('A5'), 1.0), (hz('E6'), 0.5), (hz('A6'), 0.25)): s += a*np.sin(2*np.pi*f*t)*np.exp(-t*2.2)
        return s*0.3
    if name == 'breeze':
        d = 3.0; t = tvec(d); return _wind(d, 0.35, 5)*np.sin(np.pi*t/d)
    if name == 'sigh': return np.zeros(1)
    return _base_sfx(name)
audio.sfx = sfx

_base_cue = audio.cue
def cue(name, d, seed=0):
    if name == 'sunrise':
        b = np.zeros(int(d*SR)+SR)
        place(b, pad([hz('D3'), hz('A3'), hz('F#4')], d, 2.0, 1.0), 0, 1.4)
        arp = ['D4', 'F#4', 'A4', 'D5', 'E5', 'F#5', 'A5', 'D6']
        for k in range(int(d/0.32)):
            place(b, mbox(hz(arp[k % 8]), 1.4), 0.4+k*0.32, 0.35+0.25*min(1, k/12))
        return b[:int(d*SR)]
    return _base_cue(name, d, seed)
audio.cue = cue

MUS_GAIN = {'race': 0.45, 'chelona': 0.55, 'theme': 0.8, 'lagos_soft': 0.8}

def scene_audio(S):
    n = int(S.length*SR)
    vo = np.zeros(n+SR); mus = np.zeros(n+SR); am = np.zeros(n+SR); fx = np.zeros(n+SR)
    for t0, lid, spk in S.cues.items:
        place(vo, audio.load_vo(lid), t0, 1.0)
    for t0, t1, name in S.music:
        c = cue(name, t1-t0)*MUS_GAIN.get(name, 1.0)
        f = int(0.4*SR); c[-f:] *= np.linspace(1, 0, f); f2 = int(0.15*SR); c[:f2] *= np.linspace(0, 1, f2)
        place(mus, c, t0)
    for t, name, g in S.sfx:
        if name.endswith('_on'):
            a = amb(name, S.length-t); f = int(1.0*SR); a[:f] *= np.linspace(0, 1, f); place(am, a, t, g)
        else:
            place(fx, sfx(name), t, g)
    env = lowpass(np.abs(vo), 0.0005)
    env = np.clip(env/(np.percentile(env[env > 0], 90) if np.any(env > 0) else 1), 0, 1)
    bg = mus*0.16*(1-0.75*env) + am*0.07*(1-0.65*env) + fx*0.3*(1-0.6*env)
    mix = vo*1.0 + bg
    return mix[:n], vo[:n]

if __name__ == '__main__':
    order = [('sc_ep03', f) for f in ('s1', 's2', 's3', 's4', 's5', 's6', 's7')]
    parts = []; vos = []
    for m, f in order:
        S = getattr(importlib.import_module(m), f)()
        a, v = scene_audio(S); parts.append(a); vos.append(v); print(f, round(len(a)/SR, 2), flush=True)
    full = np.concatenate(parts); vfull = np.concatenate(vos)
    bg = full-vfull
    # speech-vs-background check over speech-active windows
    w = SR//2; rs = []
    for i in range(0, len(full)-w, w):
        v = vfull[i:i+w]
        if np.sqrt(np.mean(v**2)) > 0.03:
            rs.append(20*np.log10(np.sqrt(np.mean(v**2))/(np.sqrt(np.mean(bg[i:i+w]**2))+1e-9)))
    rs = np.array(rs); print('speech over bg dB: median %.1f  p10 %.1f  min %.1f' % (np.median(rs), np.percentile(rs, 10), rs.min()))
    full = full/np.max(np.abs(full))*0.9
    sf.write('/home/claude/fable/out/soundtrack.wav', full, SR)
    print('total', len(full)/SR)
