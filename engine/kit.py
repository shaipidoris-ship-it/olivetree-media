"""Shared animation kit: scene container, pose helpers, props."""
from engine import *
from chars import *
import bgs

class Scene:
    def __init__(self, name, length):
        self.name = name; self.length = length; self.cues = Cues(); self.shots = []; self.sfx = []; self.music = []
    def shot(self, t0, t1, fn): self.shots.append((t0, t1, fn))
    def fx(self, t, name, gain=1.0): self.sfx.append((t, name, gain))
    def render(self, t):
        for t0, t1, fn in self.shots:
            if t0 <= t < t1: return fn(t-t0, t)
        t0, t1, fn = self.shots[-1]; return fn(t1-t0-1e-3, t)

def campath(lt, a, b, c0, c1, f=eio):
    k = f((lt-a)/(b-a)) if b > a else 1
    return tuple(lerp(c0[i], c1[i], k) for i in range(3))

# ---------- hare poses ----------
STAND_LEGS = [(0.15, -0.3), (0.05, -0.25)]
def Hp(x, y, s, f, t, sc, blinks=(), **kw):
    P = dict(x=x, y=y, s=s, f=f, legs=STAND_LEGS, arms=[(0.3, -0.5), (0.15, -0.4)],
             ears=(-0.25+0.05*osc(t, 0.5), -0.05+0.06*osc(t, 0.7, 1)), eye=blink_at(t, blinks),
             mouth=sc.cues.mouth('LAGOS', t), smile=0.7)
    P.update(kw); return P
def H_run(x, y, s, f, t, ph, **kw):
    a = 2*math.pi*ph
    P = dict(x=x, y=y, s=s, f=f, lean=1.12+0.08*math.sin(2*a),
             legs=[(0.25+1.05*math.sin(a), -0.35-0.9*max(0, math.sin(a+1.4))), (0.25+1.05*math.sin(a+0.7), -0.35-0.9*max(0, math.sin(a+2.1)))],
             arms=[(1.3+0.9*math.sin(a+math.pi), -0.7), (1.3+0.9*math.sin(a), -0.7)],
             ears=(-1.35, -1.15), flutter=1.0, air=18+22*max(0, math.sin(2*a)), smile=1, teeth=True, eye=1)
    P.update(kw); return P
SIT_LEGS = [(1.45, -1.55), (1.35, -1.5)]
def H_lie(x, y, s, f, t, sc, snore=True, **kw):
    br = osc(t, 0.35)
    P = dict(x=x, y=y, s=s, f=f, rot=-1.5, legs=[(0.5, -0.6), (0.3, -0.5)], arms=[(2.9, -2.4), (2.7, -2.2)],
             ears=(-0.9, -0.4), flop=(0, 1), eye=0.0, mouth=(0.25+0.25*br) if snore else 0, smile=0.4, squash=0.04*br)
    P.update(kw); return P

# ---------- tortoise ----------
def T(x, y, s, f, t, sc, blinks=(), walking=False, **kw):
    P = dict(x=x, y=y, s=s, f=f, neck=0.42+0.04*osc(t, 1.0 if walking else 0.3), eye=blink_at(t, blinks),
             mouth=sc.cues.mouth('CHELONA', t), smile=0.55)
    if walking: P['walk'] = t*0.5; P['wamp'] = 1.0
    P.update(kw); return P
TSPEED = 30.0   # px per second at scale 1

# ---------- props ----------
def apple(cr, x, y, s=1.0):
    ell(cr, x, y, 16*s, 15*s); fill_stroke(cr, hexc('#D9462F'), 3*s)
    cr.move_to(x, y-14*s); cr.line_to(x+2*s, y-22*s); stroke(cr, OUT+(1,), 3*s)
    ell(cr, x+8*s, y-20*s, 7*s, 3.5*s, -0.5); fill(cr, hexc('#7FAE5B'))
    ell(cr, x-5*s, y-5*s, 4*s, 6*s); fill(cr, (1, 1, 1, 0.4))

def dust(cr, x, y, r, a, col=(0.85, 0.75, 0.58)):
    for k in range(5):
        ell(cr, x+math.cos(k*1.7)*r*0.5, y+math.sin(k*2.3)*r*0.2, r*(0.6+0.15*k % 0.5), r*0.45); fill(cr, col+(a*0.55,))

def speed_lines(cr, x, y, n, length, a, rnd_seed=0, dirx=-1):
    r = random.Random(rnd_seed)
    for i in range(n):
        yy = y+r.uniform(-90, 90); xx = x+r.uniform(-60, 60)
        cr.move_to(xx, yy); cr.line_to(xx+dirx*length*r.uniform(0.6, 1.2), yy); stroke(cr, (1, 1, 1, a), r.uniform(2, 5))

def lamp(cr, x, y, s, lit, t):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    if lit > 0:
        glow(cr, 26, -36, 160, (1, 0.75, 0.35), 0.35*lit)
    cr.move_to(-30, -6); cr.curve_to(-34, -30, 10, -34, 26, -22); cr.line_to(40, -26); cr.line_to(30, -14); cr.curve_to(20, 0, -20, 2, -30, -6)
    cr.close_path(); fill_stroke(cr, hexc('#B5582F'), 3)
    ell(cr, -4, -22, 10, 4); fill(cr, hexc('#5A2A18'))
    if lit > 0:
        fl = 1+0.12*osc(t, 7)+0.08*osc(t, 11.3)
        cr.save(); cr.translate(36, -30); cr.scale(lit*fl, lit*fl*(1+0.1*osc(t, 5)))
        cr.move_to(0, 2); cr.curve_to(12, -6, 6, -22, 0, -34); cr.curve_to(-6, -22, -12, -6, 0, 2); fill(cr, (1, 0.62, 0.2, 0.95))
        cr.move_to(0, 0); cr.curve_to(6, -6, 3, -14, 0, -22); cr.curve_to(-3, -14, -6, -6, 0, 0); fill(cr, (1, 0.95, 0.6, 1))
        cr.restore()
    cr.restore()

def fireflies(cr, t, seed, box, n=24):
    r = random.Random(seed); x0, y0, x1, y1 = box
    for i in range(n):
        bx, by = r.uniform(x0, x1), r.uniform(y0, y1); f1, f2 = r.uniform(0.1, 0.3), r.uniform(0.1, 0.3)
        x = bx+60*math.sin(t*f1*6+i); y = by+30*math.sin(t*f2*6+i*2)
        a = 0.5+0.5*math.sin(t*3+i)
        glow(cr, x, y, 18, (1, 0.95, 0.5), 0.6*a); ell(cr, x, y, 2.5, 2.5); fill(cr, (1, 1, 0.8, a))

def zzz(cr, x, y, t, s=1.0):
    for k in range(3):
        ph = (t*0.6+k/3) % 1
        xx = x+ph*60*s+math.sin(ph*6)*8; yy = y-ph*120*s; sz = (10+ph*16)*s
        cr.move_to(xx-sz/2, yy-sz/2); cr.line_to(xx+sz/2, yy-sz/2); cr.line_to(xx-sz/2, yy+sz/2); cr.line_to(xx+sz/2, yy+sz/2)
        stroke(cr, (1, 1, 1, 0.9*(1-ph)), 3.5*s)

def leaf_confetti(cr, t, t0, seed, box, n=60):
    r = random.Random(seed); x0, y0, x1, y1 = box
    for i in range(n):
        st = t0+r.uniform(0, 1.0);
        if t < st: continue
        lt = t-st; x = r.uniform(x0, x1)+math.sin(lt*2+i)*40; y = y0+lt*r.uniform(120, 220)
        if y > y1: continue
        ell(cr, x, y, 10, 4, lt*3+i); fill(cr, (0.48+r.uniform(0, .2), 0.56, 0.3, 1))

def lanterns(cr, t, pts):
    for i, (x, y) in enumerate(pts):
        f = 0.85+0.15*math.sin(t*5+i*2)
        glow(cr, x, y, 90, (1, 0.7, 0.3), 0.45*f)
        cr.move_to(x, y-60); cr.line_to(x, y-28); stroke(cr, OUT+(1,), 2)
        ell(cr, x, y, 18, 24); fill_stroke(cr, (1, 0.72*f, 0.35, 1), 3)
LANTERNS = [(1050, 640), (1250, 560), (1700, 600), (1900, 660), (1400, 700), (2050, 560), (850, 600)]

def finish_posts(cr, x, ribbon=0.0, snapped=False):
    # near post (bottom), far post (top), ribbon between; ribbon bulge toward +x
    for (px, py, h) in ((x+30, 1130, 70), (x-10, 1225, 90)):
        rrect(cr, px-7, py-h, 14, h, 5); fill_stroke(cr, hexc('#7A5A3A'), 3)
    if not snapped:
        cr.move_to(x+30, 1080); cr.curve_to(x+30+ribbon*40, 1120, x-10+ribbon*40, 1160, x-10, 1155); stroke(cr, hexc('#B8432F'), 7)
    else:
        cr.move_to(x+30, 1080); cr.curve_to(x+50, 1100, x+60, 1120, x+80, 1125); stroke(cr, hexc('#B8432F'), 7)
        cr.move_to(x-10, 1155); cr.curve_to(x+20, 1170, x+40, 1185, x+70, 1190); stroke(cr, hexc('#B8432F'), 7)

def title_card(cr, a):
    cr.set_source_rgba(0.05, 0.05, 0.12, 1); cr.paint()
    cr.select_font_face("DejaVu Serif", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL); cr.set_font_size(96)
    txt = "Tales from the Olive Tree"; e = cr.text_extents(txt)
    cr.set_source_rgba(0.95, 0.88, 0.7, a); cr.move_to(W/2-e.x_advance/2, H/2+20); cr.show_text(txt)
    cr.set_font_size(40); cr.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    t2 = "The Tortoise and the Hare"; e = cr.text_extents(t2)
    cr.set_source_rgba(0.95, 0.88, 0.7, a*0.8); cr.move_to(W/2-e.x_advance/2, H/2+100); cr.show_text(t2)
    rnd = random.Random(3)
    cr.move_to(W/2-260, H/2-110); cr.curve_to(W/2-100, H/2-150, W/2+100, H/2-150, W/2+260, H/2-110); stroke(cr, (0.6, 0.65, 0.4, a), 4)
    for k in range(12):
        x = W/2-240+k*44; y = H/2-128-math.sin(k/11*math.pi)*28
        ell(cr, x, y-10*((-1)**k), 16, 6, 0.5*((-1)**k)); fill(cr, (0.55, 0.65, 0.38, a))
