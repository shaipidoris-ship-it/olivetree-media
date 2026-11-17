import numpy as np, soundfile as sf, importlib, json, math, random
SR = 44100
rng = np.random.default_rng(1)

def tvec(d): return np.arange(int(d*SR))/SR
def env_adsr(n, a=0.01, r=0.1):
    e = np.ones(n); ai = max(1, int(a*SR)); ri = max(1, int(r*SR))
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return e
NOTE = {'C': -9, 'C#': -8, 'Db': -8, 'D': -7, 'D#': -6, 'Eb': -6, 'E': -5, 'F': -4, 'F#': -3, 'Gb': -3, 'G': -2, 'G#': -1, 'Ab': -1, 'A': 0, 'A#': 1, 'Bb': 1, 'B': 2}
def hz(n):
    name, octv = n[:-1], int(n[-1]); return 440*2**((NOTE[name]+(octv-4)*12)/12)

def pluck(f, d, bright=1.0, decay=2.5, n=8):
    t = tvec(d); s = np.zeros_like(t)
    for k in range(1, n+1):
        s += (1/k**(1.6/bright))*np.sin(2*np.pi*f*k*t+k)*np.exp(-t*decay*(1+0.5*k))
    return s*env_adsr(len(t), 0.003, 0.05)*0.5
def bouz(f, d): return pluck(f, d, 1.7, 2.0, 10)+0.6*pluck(f*1.003, d, 1.7, 2.0, 10)
def clar(f, d, vib=5.0):
    t = tvec(d); ph = 2*np.pi*f*t+0.004*f*np.sin(2*np.pi*vib*t)/vib*2*np.pi*0.5
    s = sum((1/k)*np.sin(k*ph) for k in (1, 3, 5, 7))
    return s*env_adsr(len(t), 0.06, 0.12)*0.35
def pad(fs, d, a=0.8, r=0.8):
    t = tvec(d); s = np.zeros_like(t)
    for f in fs:
        for det in (0.997, 1.0, 1.003):
            for k in range(1, 6): s += (1/k)*np.sin(2*np.pi*f*det*k*t+k*det*7)
    return s*env_adsr(len(t), a, r)*0.05/len(fs)
def mbox(f, d):
    t = tvec(d); return (np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*f*4*t)*np.exp(-t*6))*np.exp(-t*2.5)*env_adsr(len(t), 0.002, 0.05)*0.4
def brass(f, d):
    t = tvec(d); a = np.clip(t/0.08, 0, 1); s = sum((1/k)*np.sin(2*np.pi*f*k*t)*(a**(k*0.5)) for k in range(1, 9))
    return s*env_adsr(len(t), 0.03, 0.2)*0.25
def noise(d): return rng.standard_normal(int(d*SR))
def lowpass(x, a=0.1):
    y = np.empty_like(x); acc = 0.0
    # vectorised one-pole via cumulative trick (approx with convolution)
    k = int(1/a*3); w = np.exp(-np.arange(k)*a); w /= w.sum()
    return np.convolve(x, w, 'same')
def highpass(x, a=0.1): return x-lowpass(x, a)
def drum(d=0.5, f0=110, amp=1.0):
    t = tvec(d); f = f0*(1+1.5*np.exp(-t*30)); ph = 2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph)*np.exp(-t*9)+0.15*lowpass(noise(d), 0.3)[:len(t)]*np.exp(-t*25))*amp*0.8
def tick(d=0.08, amp=0.5): t = tvec(d); return highpass(noise(d), 0.4)*np.exp(-t*60)*amp
def clap(): return highpass(noise(0.15), 0.3)*np.exp(-tvec(0.15)*35)*0.6

def addv(*xs):
    n = max(len(x) for x in xs); o = np.zeros(n)
    for x in xs: o[:len(x)] += x
    return o
def place(buf, sig, t, g=1.0):
    i = int(t*SR)
    if i >= len(buf) or i < 0: return
    j = min(len(buf), i+len(sig)); buf[i:j] += sig[:j-i]*g

# ---------------- music cues ----------------
THEME = ['D4', 'F#4', 'A4', 'B4', 'A4', 'F#4', 'E4', 'D4', 'E4', 'F#4', 'A4', 'D5', 'B4', 'A4', 'F#4', 'A4']
CHORDS = [['D3', 'A3', 'F#4'], ['B2', 'F#3', 'D4'], ['G2', 'D3', 'B3'], ['A2', 'E3', 'C#4']]
LAG = ['G4', 'B4', 'D5', 'B4', 'C5', 'A4', 'F#4', 'A4', 'G4', 'D5', 'E5', 'D5', 'B4', 'G4', 'A4', 'D4']
CHEL = ['A3', 'C4', 'D4', 'E4', 'D4', 'C4', 'A3', 'G3', 'A3', 'C4', 'E4', 'G4', 'E4', 'D4', 'C4', 'A3']
def cue(name, d, seed=0):
    b = np.zeros(int(d*SR)+SR)
    if name in ('theme', 'theme_soft', 'end_sting'):
        bpm = 72; beat = 60/bpm; g = 0.6 if name == 'theme_soft' else 1.0
        t = 0; i = 0
        while t < d:
            ch = CHORDS[(i//4) % 4]
            if i % 4 == 0: place(b, pad([hz(n) for n in ch], beat*4+0.5, 0.6, 0.8), t, 1.0*g)
            place(b, pluck(hz(THEME[i % 16]), beat*1.6, 1.0, 2.0), t, 0.55*g)
            place(b, pluck(hz(ch[0])/2*2, beat*1.2, 0.8, 3.0), t, 0.25*g)
            t += beat; i += 1
    elif name in ('lagos', 'lagos_soft'):
        bpm = 132; beat = 60/bpm/2; g = 0.55 if name == 'lagos_soft' else 1.0
        t = 0; i = 0
        while t < d:
            n = LAG[i % 16]
            if i % 2 == 0 or (i % 4 == 3): place(b, pluck(hz(n), 0.25, 1.4, 9.0), t, 0.5*g)
            if i % 4 == 0: place(b, pluck(hz('G2') if (i//16) % 2 == 0 else hz('D2'), 0.3, 0.8, 7.0), t, 0.55*g)
            if i % 4 == 2: place(b, pluck(hz('D3'), 0.25, 0.8, 8.0), t, 0.35*g)
            if i % 8 == 6: place(b, bouz(hz(n)*2, 0.2), t, 0.18*g)
            t += beat; i += 1
    elif name in ('dance', 'race'):
        t = 0; i = 0
        while t < d:
            bpm = 120+60*min(1, t/max(d, 1)); beat = 60/bpm/2
            n = LAG[i % 16] if name == 'dance' else ['E4', 'G4', 'A4', 'B4', 'A4', 'G4', 'E4', 'D4'][i % 8]
            place(b, bouz(hz(n), 0.22), t, 0.32)
            if i % 2 == 0: place(b, drum(0.3, 90, 0.35), t)
            else: place(b, tick(0.06, 0.4), t)
            if i % 4 == 0: place(b, pluck(hz('E2') if name == 'race' else hz('G2'), 0.3, 0.8, 6), t, 0.5)
            if name == 'race' and i % 8 == 0: place(b, clar(hz(CHEL[(i//8) % 16]), beat*7), t, 0.35)
            t += beat; i += 1
    elif name == 'lullaby':
        beat = 0.55; mel = ['B5', 'G5', 'D5', 'G5', 'A5', 'F#5', 'D5', 'E5', 'G5', 'B4', 'D5', 'G5']
        t = 0.3; i = 0
        while t < d:
            place(b, mbox(hz(mel[i % 12]), 1.5), t, 0.5)
            if i % 3 == 0: place(b, mbox(hz(['G3', 'D3', 'E3', 'C3'][(i//3) % 4])*2, 2.0), t, 0.3)
            t += beat*(1+0.04*i*(t > d*0.6)); i += 1
    elif name in ('chelona', 'chelona_swell'):
        beat = 1.0; t = 0; i = 0
        while t < d:
            place(b, drum(0.6, 70, 0.25), t)
            place(b, tick(0.05, 0.15), t+0.5)
            if i % 2 == 0: place(b, clar(hz(CHEL[(i//2) % 16]), 1.9), t, 0.6)
            if i % 4 == 0: place(b, pad([hz('A2'), hz('E3'), hz('C4')], 4.4, 1.0, 1.0), t, 0.8 if name == 'chelona' else 0.8+1.6*t/d)
            t += beat; i += 1
    elif name == 'fanfare_soft':
        seq = [('D4', 0.25), ('D4', 0.25), ('A4', 0.5), ('F#4', 0.25), ('A4', 0.25), ('D5', 1.0)]; t = 0.3
        for n, dd in seq: place(b, brass(hz(n), dd+0.1), t, 0.6); place(b, brass(hz(n)/2, dd+0.1), t, 0.3); t += dd
        tt = t+0.5
        while tt < d:
            place(b, pluck(hz(THEME[int(tt*2) % 16]), 0.6), tt, 0.3); place(b, tick(0.05, 0.2), tt); tt += 0.5
    elif name == 'drumroll':
        t = 0
        while t < d:
            place(b, tick(0.05, 0.25+0.5*t/d), t); t += 0.045
        place(b, pad([hz('A3'), hz('E4')], d, 0.5, 0.2), 0, 1.4)
    elif name == 'go_flourish':
        for k, n in enumerate(['D4', 'F#4', 'A4', 'D5', 'F#5', 'A5']): place(b, pluck(hz(n), 1.2, 1.3), k*0.06, 0.5)
        place(b, brass(hz('D4'), 1.2), 0.36, 0.4)
    elif name == 'sting':
        place(b, pluck(hz('G3'), 0.3, 1, 6), 0.0, 0.7); place(b, pluck(hz('D3'), 0.6, 1, 4), 0.25, 0.8)
    elif name == 'tension_soft':
        t = tvec(d); b[:len(t)] += pad([hz('E2'), hz('B2'), hz('G3')], d, 1.0, 0.5)*(0.6+0.4*np.sin(2*np.pi*6*t))*1.3
    elif name == 'heartbeat':
        t = 0.2
        while t < d:
            place(b, drum(0.3, 55, 0.9), t); place(b, drum(0.3, 50, 0.6), t+0.22); t += 0.85
    elif name == 'victory':
        for n in ('D4', 'F#4', 'A4', 'D5'): place(b, brass(hz(n), d-0.3), 0, 0.35)
        sw = highpass(noise(2.0), 0.2)*np.linspace(0, 1, int(2.0*SR))**2*np.exp(-np.linspace(0, 2, int(2.0*SR))); place(b, sw, 0, 0.3)
        for k, n in enumerate(['D5', 'E5', 'F#5', 'A5', 'B5', 'A5', 'F#5', 'D5']): place(b, pluck(hz(n), 0.8, 1.2), 0.2+k*0.18, 0.4)
    elif name == 'village_dance':
        t = 0; i = 0; beat = 60/150/2
        while t < d:
            place(b, pluck(hz(LAG[i % 16]), 0.25, 1.4, 6), t, 0.3)
            if i % 4 == 2: place(b, clap(), t, 0.5)
            if i % 4 == 0: place(b, drum(0.3, 90, 0.5), t)
            t += beat; i += 1
    return b[:int(d*SR)]

# ---------------- ambience ----------------
def amb(name, d):
    n = int(d*SR); t = np.arange(n)/SR
    if name == 'crickets_on':
        s = np.zeros(n)
        for f, rate, ph in ((4200, 2.6, 0), (4700, 3.1, 1), (3900, 2.2, 2)):
            gate = (np.sin(2*np.pi*rate*t+ph) > 0.4)*(np.sin(2*np.pi*rate*12*t) > 0)
            s += np.sin(2*np.pi*f*t)*lowpass(gate.astype(float), 0.3)*0.05
        return s
    if name == 'cicadas_on':
        x = highpass(noise(d), 0.5); am = 0.5+0.5*np.sin(2*np.pi*48*t); slow = 0.6+0.4*np.sin(2*np.pi*0.15*t)
        return x*am*slow*0.05
    if name == 'market_on':
        x = lowpass(noise(d), 0.05); x = x-lowpass(x, 0.01)
        return x*(0.7+0.3*np.sin(2*np.pi*0.3*t))*0.15
    if name == 'stream_on':
        x = lowpass(noise(d), 0.2)-lowpass(noise(d), 0.02); return x*(0.6+0.4*np.sin(2*np.pi*3.3*t)*np.sin(2*np.pi*0.7*t))*0.25
    return np.zeros(n)

# ---------------- sfx ----------------
def sfx(name):
    if name.startswith('whoosh'):
        d = {'whoosh_s': 0.3, 'whoosh_m': 0.45, 'whoosh_l': 0.8}[name]; x = noise(d); t = tvec(d)
        e = np.sin(np.pi*t/d)**2; lp = lowpass(x, 0.08); return (x*0.3+lp*3)*e*0.35
    if name == 'catch': return addv(drum(0.2, 200, 0.6), tick(0.05, 0.6))
    if name == 'pop':
        t = tvec(0.15); f = 600+900*t/0.15; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*0.5
    if name == 'flint': return addv(tick(0.04, 0.9), 0.3*highpass(noise(0.3), 0.5)*np.exp(-tvec(0.3)*12))
    if name == 'flame': t = tvec(0.8); return lowpass(noise(0.8), 0.05)*np.sin(np.pi*t/0.8)*0.9
    if name == 'hoot':
        out = np.zeros(int(1.2*SR))
        for st, dd in ((0, 0.35), (0.45, 0.6)):
            t = tvec(dd); f = 420-60*t/dd; s = np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/dd)*0.4
            place(out, s, st)
        return out
    if name == 'skid': t = tvec(0.6); return highpass(noise(0.6), 0.2)*np.exp(-t*4)*0.4
    if name == 'snore':
        d = 1.6; t = tvec(d); inb = (t < 0.9)
        rasp = lowpass(noise(d), 0.05)*(0.5+0.5*np.sin(2*np.pi*35*t))*np.sin(np.pi*np.clip(t/0.9, 0, 1))*inb*2.5
        wh = np.sin(2*np.pi*(900+300*(t-0.9))*t)*np.sin(np.pi*np.clip((t-0.95)/0.6, 0, 1))*(t > 0.95)*0.15
        return rasp+wh
    if name == 'clap': return clap()
    if name == 'tap': return drum(0.12, 300, 0.4)
    if name == 'croak':
        d = 0.45; t = tvec(d); return np.sign(np.sin(2*np.pi*90*t))*(0.5+0.5*np.sin(2*np.pi*18*t))*np.sin(np.pi*t/d)*0.18
    if name == 'clack': return addv(drum(0.12, 420, 0.5), tick(0.04, 0.5))
    if name == 'snort': t = tvec(0.4); return lowpass(noise(0.4), 0.06)*np.exp(-t*8)*1.6
    if name == 'flutter':
        out = np.zeros(int(0.8*SR))
        for k in range(14): place(out, tick(0.03, 0.35), k*0.05)
        return out
    if name == 'fig_roll': t = tvec(1.1); return lowpass(noise(1.1), 0.03)*(0.6+0.4*np.sin(2*np.pi*9*t))*1.2
    if name == 'gasp': t = tvec(0.35); return highpass(noise(0.35), 0.3)*np.sin(np.pi*t/0.35)*0.25
    if name == 'snap': return addv(tick(0.08, 1.0), drum(0.15, 260, 0.4))
    if name == 'tumble':
        out = np.zeros(int(1.0*SR))
        for k in range(4): place(out, drum(0.25, 80, 0.7-k*0.12), k*0.18)
        return out
    if name == 'puff': t = tvec(0.5); return lowpass(noise(0.5), 0.1)*np.sin(np.pi*t/0.5)*0.9
    if name == 'paper': t = tvec(0.7); return highpass(noise(0.7), 0.3)*(0.5+0.5*np.sin(2*np.pi*14*t))*np.sin(np.pi*t/0.7)*0.25
    if name == 'dust': t = tvec(0.7); return lowpass(noise(0.7), 0.05)*np.exp(-t*4)*1.5
    if name == 'grass': t = tvec(0.6); return highpass(noise(0.6), 0.25)*np.sin(np.pi*t/0.6)*0.18
    if name == 'chew':
        out = np.zeros(int(2.4*SR))
        for k in range(8): place(out, tick(0.04, 0.25), k*0.3)
        return out
    return np.zeros(1)

def load_vo(lid):
    a, sr = sf.read(f'/home/claude/fable/vo/{lid}.wav')
    if a.ndim > 1: a = a.mean(1)
    n = int(len(a)*SR/sr); a = np.interp(np.linspace(0, len(a)-1, n), np.arange(len(a)), a)
    act = a[np.abs(a) > 0.02]; r = np.sqrt(np.mean(act**2)) if len(act) else 1
    return a*(0.11/r)

def scene_audio(S):
    n = int(S.length*SR)
    vo = np.zeros(n+SR); mus = np.zeros(n+SR); am = np.zeros(n+SR); fx = np.zeros(n+SR)
    for t0, lid, spk in S.cues.items:
        g = 0.75 if spk in ('CROWD',) else 1.0
        place(vo, load_vo(lid), t0, g)
    for t0, t1, name in S.music:
        c = cue(name, t1-t0)
        f = int(0.4*SR); c[-f:] *= np.linspace(1, 0, f); f2 = int(0.15*SR); c[:f2] *= np.linspace(0, 1, f2)
        place(mus, c, t0)
    for t, name, g in S.sfx:
        if name.endswith('_on'):
            a = amb(name, S.length-t); f = int(1.0*SR); a[:f] *= np.linspace(0, 1, f); place(am, a, t, g)
        else:
            place(fx, sfx(name), t, g)
    # duck music under dialogue
    env = lowpass(np.abs(vo), 0.0005)
    env = np.clip(env/ (np.percentile(env[env > 0], 90) if np.any(env > 0) else 1), 0, 1)
    duck = 1-0.55*env
    mix = vo*1.0+mus*0.16*(1-0.6*env)+am*0.07+fx*0.3
    return mix[:n]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/home/claude/fable')
    order = [('sc_a', 's1'), ('sc_a', 's2'), ('sc_b', 's3'), ('sc_b', 's4'), ('sc_c', 's5'), ('sc_c', 's6'), ('sc_c', 's7'), ('sc_c', 's8')]
    parts = []
    for m, f in order:
        S = getattr(importlib.import_module(m), f)()
        a = scene_audio(S); parts.append(a); print(f, round(len(a)/SR, 2), flush=True)
    full = np.concatenate(parts)
    full = full/np.max(np.abs(full))*0.9
    sf.write('/home/claude/fable/out/soundtrack.wav', full, SR)
    print('total', len(full)/SR)
