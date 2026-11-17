import cairo, math, json, random
import numpy as np, soundfile as sf

W, H, FPS = 1920, 1080, 24
OUT = (0.231, 0.165, 0.125)  # umber line #3B2A20

def hexc(h, a=1.0):
    h = h.lstrip('#'); return (int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255, a)
def mix(c1, c2, k):
    return tuple(c1[i]+(c2[i]-c1[i])*k for i in range(3)) + (1.0,)
def shade(c, k):  # k<1 darker
    return (c[0]*k, c[1]*k, c[2]*k, c[3] if len(c) > 3 else 1)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(t): t = clamp(t); return t*t*(3-2*t)
def eio(t): t = clamp(t); return 0.5-0.5*math.cos(math.pi*t)
def ramp(t, a, b): return ease((t-a)/(b-a)) if b != a else float(t >= a)
def lerp(a, b, k): return a+(b-a)*k
def pulse(t, a, b, fade=0.15): return ramp(t, a, a+fade)*(1-ramp(t, b-fade, b))
def osc(t, f, ph=0): return math.sin(2*math.pi*f*t+ph)

def rrect(cr, x, y, w, h, r):
    r = min(r, abs(w)/2, abs(h)/2); cr.new_sub_path()
    cr.arc(x+w-r, y+r, r, -math.pi/2, 0); cr.arc(x+w-r, y+h-r, r, 0, math.pi/2)
    cr.arc(x+r, y+h-r, r, math.pi/2, math.pi); cr.arc(x+r, y+r, r, math.pi, 1.5*math.pi); cr.close_path()
def ell(cr, x, y, rx, ry, rot=0):
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(max(rx, 0.01), max(ry, 0.01))
    cr.new_sub_path(); cr.arc(0, 0, 1, 0, 2*math.pi); cr.restore()
def fill_stroke(cr, col, lw=4.0, line=OUT):
    cr.set_source_rgba(*col); cr.fill_preserve()
    if lw > 0:
        cr.set_source_rgb(*line); cr.set_line_width(lw); cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.stroke()
    else: cr.new_path()
def fill(cr, col): cr.set_source_rgba(*col); cr.fill()
def stroke(cr, col, lw):
    cr.set_source_rgba(*col); cr.set_line_width(lw); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.stroke()
def capsule(cr, a, b, w, col, lw=4.0):
    # filled capsule with outline
    dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 0.01; ang = math.atan2(dy, dx)
    cr.save(); cr.translate(*a); cr.rotate(ang)
    cr.new_path(); cr.arc(0, 0, w/2, math.pi/2, 3*math.pi/2); cr.arc(L, 0, w/2, -math.pi/2, math.pi/2); cr.close_path()
    cr.restore(); fill_stroke(cr, col, lw)
def glow(cr, x, y, r, col, a):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], a); g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    cr.set_source(g); cr.arc(x, y, r, 0, 2*math.pi); cr.fill()
def vec(a, l): return (math.sin(a)*l, -math.cos(a)*l)   # angle 0 = up, + = clockwise (toward +x)
def add(p, q): return (p[0]+q[0], p[1]+q[1])

# ---------------- audio cues / lip-sync ----------------
VO = '/home/claude/fable/vo/'
META = json.load(open(VO+'meta.json'))
_env = {}
def envelope(lid):
    if lid not in _env:
        a, sr = sf.read(VO+lid+'.wav')
        if a.ndim > 1: a = a.mean(1)
        hop = sr//60; n = len(a)//hop
        e = np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2)) for i in range(n)])
        e = e/(np.percentile(e, 95)+1e-6)
        _env[lid] = (e, 60)
    return _env[lid]
def dur(lid):
    if lid in META: return META[lid]['dur']
    a, sr = sf.read(VO+lid+'.wav'); return len(a)/sr

class Cues:
    def __init__(self): self.items = []   # (t0, lid, speaker)
    def say(self, lid, t0, spk=None):
        self.items.append((t0, lid, spk or (META[lid]['spk'] if lid in META else None))); return t0+dur(lid)
    def mouth(self, spk, t):
        v = 0.0
        for t0, lid, s in self.items:
            if s == spk or (s == 'SPARROWS' and spk in ('PIP','PIM','PIO')):
                d = dur(lid)
                if t0 <= t <= t0+d:
                    e, r = envelope(lid); i = int((t-t0)*r)
                    if 0 <= i < len(e): v = max(v, clamp(e[i]*1.1))
        return v
    def talking(self, spk, t):
        return any(s == spk and t0 <= t <= t0+dur(l) for t0, l, s in self.items)

def blink_at(t, times, d=0.16):
    for b in times:
        if b <= t < b+d: return 1-math.sin(math.pi*(t-b)/d)
    return 1.0
def auto_blinks(seed, length, every=3.2):
    r = random.Random(seed); t = r.uniform(0.5, 2); out = []
    while t < length: out.append(t); t += r.uniform(every*0.6, every*1.4)
    return out
