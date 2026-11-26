"""Episode 03 — The North Wind and the Sun."""
from kit import *
from chars3 import *
import bgs3
from bgs3 import road_y, ROAD_TREE, windmill_sails
import engine as _eng
from engine import PAR, GRADE, grain, cam_xform

def _frame(loc, tod, cam, draw=None, layers=('back', 'main', 'fg'), extra_grade=None, fade=0.0, flash=0.0, over_back=None, shake=(0, 0)):
    """engine.frame, but over_back (windmill sails) is painted between the back and main layers."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(s)
    cr.set_source_rgb(0, 0, 0); cr.paint()
    L = bgs.get(loc, tod); ref = L['ref']
    cw, ch = L['size']; z = cam[2]; hw, hh = W/2/z, H/2/z
    cx = clamp(cam[0]+shake[0], hw, cw-hw) if cw > 2*hw else cw/2
    cy = clamp(cam[1]+shake[1], hh, ch-hh) if ch > 2*hh else ch/2
    cam = (cx, cy, z)
    cr.save(); cam_xform(cr, cam, PAR['back'], ref); cr.set_source_surface(L['surf']['back'], 0, 0); cr.get_source().set_filter(cairo.FILTER_GOOD); cr.paint()
    if over_back: over_back(cr, L)
    cr.restore()
    cr.save(); cam_xform(cr, cam, PAR['main'], ref); cr.set_source_surface(L['surf']['main'], 0, 0); cr.get_source().set_filter(cairo.FILTER_GOOD); cr.paint(); cr.restore()
    if draw:
        cr.save(); cam_xform(cr, cam, 1.0, ref); draw(cr, L); cr.restore()
    if 'fg' in layers:
        cr.save(); cam_xform(cr, cam, PAR['fg'], ref); cr.set_source_surface(L['surf']['fg'], 0, 0); cr.paint(); cr.restore()
    if tod in GRADE: cr.set_source_rgba(*GRADE[tod]); cr.paint()
    if extra_grade: cr.set_source_rgba(*extra_grade); cr.paint()
    g = cairo.RadialGradient(W/2, H/2, H*0.45, W/2, H/2, H*1.05)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.08, 0.04, 0.02, 0.45)
    cr.set_source(g); cr.paint()
    cr.set_source_surface(grain(), 0, 0); cr.paint()
    if flash > 0: cr.set_source_rgba(1, 1, 0.95, flash); cr.paint()
    if fade > 0: cr.set_source_rgba(0, 0, 0, fade); cr.paint()
    return s

def frame(loc, tod, cam, **kw):
    if cam[2] >= 1.45 and 'layers' not in kw: kw['layers'] = ('back', 'main')   # tall fg grass hides the cast in close-ups
    if loc == 'road': return _frame(loc, tod, cam, **kw)
    return _eng.frame(loc, tod, cam, **kw)

LAMP = (1300, 902)
SUBTITLE = "The North Wind and the Sun"
def title_card3(cr, a, sub=SUBTITLE):
    cr.set_source_rgba(0.05, 0.05, 0.12, 1); cr.paint()
    cr.select_font_face("DejaVu Serif", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL); cr.set_font_size(96)
    txt = "Tales from the Olive Tree"; e = cr.text_extents(txt)
    cr.set_source_rgba(0.95, 0.88, 0.7, a); cr.move_to(W/2-e.x_advance/2, H/2+20); cr.show_text(txt)
    cr.set_font_size(40); cr.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    e = cr.text_extents(sub)
    cr.set_source_rgba(0.95, 0.88, 0.7, a*0.8); cr.move_to(W/2-e.x_advance/2, H/2+100); cr.show_text(sub)
    cr.move_to(W/2-260, H/2-110); cr.curve_to(W/2-100, H/2-150, W/2+100, H/2-150, W/2+260, H/2-110); stroke(cr, (0.6, 0.65, 0.4, a), 4)
    for k in range(12):
        x = W/2-240+k*44; y = H/2-128-math.sin(k/11*math.pi)*28
        ell(cr, x, y-10*((-1)**k), 16, 6, 0.5*((-1)**k)); fill(cr, (0.55, 0.65, 0.38, a))

def lampdraw(cr, t, lit): lamp(cr, LAMP[0], LAMP[1], 1.7, lit, t)

# ---- shared sky staging ----
VX, VY, VS = 2350, 430, 1.1        # Vorias (faces left)
IX, IY, IS = 1250, 420, 1.0        # Ilios
def mitsos_y(x): return road_y(x)+8

def spin_of(t, Wf, base=0.06):
    """windmill revolutions: integrate wind strength Wf over time."""
    n = max(1, int(t*8)); dt = t/n
    return base*t + 0.9*sum(Wf(i*dt) for i in range(n))*dt

def wm(Wf, extra=0.0):
    return lambda cr, L, t: windmill_sails(cr, t, spin_of(t, Wf)+extra)

def ground_gust(cr, t, k, x_from, x_to, y, seed=7):
    gust(cr, x_from, y-260, x_to, y+40, k*0.6, t, seed=seed, n=8, spread=160, lw=4)

# ======================= SCENE 1 — Glafka opens =======================
def s1():
    S = Scene('s1', 32.0); c = S.cues
    c.say('s1_01', 10.5); c.say('s1_02', 15.8); c.say('s1_03', 19.8); c.say('s1_04', 25.0)
    S.music.append((0.0, 32.0, 'theme'))
    S.fx(0.0, 'wind_soft_on', 0.8); S.fx(1.0, 'crickets_on', 0.6); S.fx(7.6, 'flint'); S.fx(8.0, 'flame'); S.fx(3.0, 'hoot', 0.35)
    S.fx(1.6, 'whoosh_l', 0.5); S.fx(12.2, 'whoosh_m', 0.4)
    blinks = [9.4, 14.6, 19.3, 24.4, 28.6]
    def gl(t, **kw):
        P = dict(x=1100, y=905, s=2.4, eye=blink_at(t, blinks), mouth=c.mouth('GLAFKA', t), tilt=0.05*osc(t, 0.35))
        P.update(kw); return P
    def leaves_in(cr, t, k, box): blown_leaves(cr, t, k, box, seed=11, n=18, dirx=1)
    def sh1(lt, t):
        cam = campath(lt, 0, 6, (1500, 1330, 1.05), (1500, 850, 0.82))
        def d(cr, L):
            fireflies(cr, t, 2, (900, 700, 2100, 1250), 30)
            leaves_in(cr, t, 0.6, (300, 500, 2400, 1300))
        return frame('olive', 'blue', cam, draw=d, fade=1-ramp(lt, 0, 1.5))
    S.shot(0, 6, sh1)
    def sh2(lt, t):
        cam = campath(lt, 0, 4.5, (1100, 650, 0.92), (1150, 700, 1.12))
        lit = ramp(t, 8.0, 8.5)
        def d(cr, L):
            if lit > 0: glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35*lit)
            owl(cr, gl(t, look=(0.7, 0.4), tilt=0.12), t)
            lampdraw(cr, t, lit)
            if 7.5 <= t < 7.75:
                for k in range(8):
                    a = k*0.8; cr.move_to(LAMP[0]+40, LAMP[1]-50); cr.line_to(LAMP[0]+40+math.cos(a)*30, LAMP[1]-50+math.sin(a)*30); stroke(cr, (1, 0.9, 0.5, 1), 3)
        return frame('hollow', 'blue', cam, draw=d, extra_grade=(1, 0.6, 0.3, 0.06*lit))
    S.shot(6, 10.5, sh2)
    def sh3(lt, t):
        cam = campath(t, 10.5, 25, (1120, 680, 1.25), (1110, 640, 1.4))
        sw = lerp(0.7, 0.0, ramp(t, 10.5, 11.0))
        gust_ = pulse(t, 12.0, 13.4, 0.3)                 # a gust rushes past the hollow: Glafka ruffles
        wind_g = pulse(t, 17.2, 18.4, 0.3); sun_g = pulse(t, 18.6, 19.6, 0.3)
        def d(cr, L):
            glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35*(1-0.3*gust_))
            P = gl(t, swivel=sw*0.5, look=(sw, 0), tilt=0.05*osc(t, 0.35)-0.12*gust_+0.1*sun_g,
                   wings=(1.1*wind_g+0.2*gust_, 1.1*wind_g+0.9*sun_g+0.2*gust_), wide=1+0.15*gust_)
            owl(cr, P, t)
            lampdraw(cr, t, 1-0.4*gust_)
            if gust_ > 0.05: blown_leaves(cr, t, gust_, (500, 300, 1800, 1100), seed=12, n=14, dirx=1)
            if sun_g > 0.05: glow(cr, 1260, 620, 120, (1, 0.85, 0.4), 0.5*sun_g)
        return frame('hollow', 'blue', cam, draw=d, extra_grade=(1, 0.6, 0.3, 0.06))
    S.shot(10.5, 25.0, sh3)
    def sh4(lt, t):
        cam = campath(t, 25.0, 27.5, (1110, 640, 1.4), (1110, 600, 1.8))
        if t > 29.4: cam = campath(t, 29.4, 31.8, cam, (LAMP[0]+61, LAMP[1]-50, 7.0), ease)
        laugh = pulse(t, 25.0, 26.0, 0.1)
        def d(cr, L):
            glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35)
            P = gl(t, tilt=0.06*math.sin(t*30)*laugh, wings=(0.5*laugh, 0.5*laugh), y=905-8*laugh*abs(math.sin(t*20)))
            if 27.8 <= t < 28.4: P['wink'] = 1-math.sin(math.pi*(t-27.8)/0.6)
            if laugh > 0.3: P['happy'] = True
            owl(cr, P, t); lampdraw(cr, t, 1)
        return frame('hollow', 'blue', cam, draw=d, extra_grade=(1, 0.6, 0.3, 0.06), flash=ramp(t, 30.6, 32.0))
    S.shot(25.0, 32.0, sh4)
    return S

# ======================= SCENE 2 — the argument in the sky =======================
def s2():
    S = Scene('s2', 28.0); c = S.cues
    c.say('s2_01', 2.0); c.say('s2_02', 7.6); c.say('s2_03', 11.2); c.say('s2_04', 15.5); c.say('s2_05', 19.7); c.say('s2_06', 24.0)
    S.music += [(0.0, 7.4, 'lagos_soft'), (7.4, 11.0, 'theme_soft'), (11.0, 15.2, 'lagos_soft'), (15.2, 19.4, 'theme_soft'),
                (19.4, 23.6, 'tension_soft'), (23.6, 28.0, 'theme_soft')]
    S.fx(0.0, 'wind_soft_on', 0.7); S.fx(0.3, 'whoosh_l', 0.8); S.fx(4.6, 'whoosh_l'); S.fx(5.4, 'whoosh_m'); S.fx(12.4, 'whoosh_m', 0.6)
    vb = auto_blinks(201, 30, 3.0); ib = auto_blinks(202, 30, 3.6)
    Wf = lambda t: 0.25+0.6*pulse(t, 4.6, 6.6, 0.3)
    def vor(t, **kw):
        enter = ramp(t, 0.0, 1.6)
        blow = pulse(t, 4.6, 6.4, 0.25)
        proud = pulse(t, 11.2, 15.0, 0.4)
        P = dict(x=lerp(VX+700, VX, enter), y=VY+lerp(-120, 0, enter), s=VS*(1+0.12*proud), f=-1, eye=blink_at(t, vb),
                 mouth=c.mouth('VORIAS', t), puff=blow, brow=0.5+0.5*proud, smile=0.8, rot=-0.15*(1-enter)+0.04*math.sin(t*1.3))
        if blow > 0.3: P['look'] = (0.8, 0.8)
        if 7.6 <= t < 11.0: P['look'] = (1, 0.1); P['brow'] = -0.3; P['smile'] = 0.2
        if 15.5 <= t < 19.4: P['look'] = (1, 0); P['brow'] = -0.4; P['smile'] = 0.3
        if 19.7 <= t < 23.6: P['brow'] = 0.9; P['smile'] = 1.0
        if t >= 25.6: P['look'] = (0.6, 1); P['smile'] = 0.9
        P.update(kw); return P
    def ili(t, **kw):
        P = dict(x=IX, y=IY, s=IS, eye=blink_at(t, ib), mouth=c.mouth('ILIOS', t), shine=0.35, look=(0.8, 0), smile=0.9)
        if t < 2.0: P['look'] = (0.3, 0.3)
        if 11.2 <= t < 15.0: P['brow'] = 0.6; P['smile'] = 0.6   # unimpressed eyebrow
        if 15.5 <= t < 19.2: P['brow'] = 0.3
        if t >= 25.8: P['look'] = (0.2, 1)
        P.update(kw); return P
    def draw_all(cr, t):
        sun(cr, ili(t), t)
        V = vor(t); wind_cloud(cr, V, t)
        b = pulse(t, 4.6, 6.4, 0.25)
        if b > 0.05:
            mx, my = cloud_mouth(V); gust(cr, mx-20, my+10, mx-900, my+520, b, t, seed=21, n=12, spread=70)
    def sh(cam, fade_in=0.0):
        return lambda lt, t: frame('road', 'morning', cam(t) if callable(cam) else cam, draw=lambda cr, L: draw_all(cr, t),
                                   over_back=lambda cr, L: windmill_sails(cr, t, spin_of(t, Wf)), fade=(1-ramp(t, 0, fade_in)) if fade_in else 0.0)
    S.shot(0, 7.4, sh(lambda t: campath(t, 0, 7.4, (2250, 520, 1.25), (2050, 560, 1.05)), fade_in=0.8))
    S.shot(7.4, 11.0, sh(lambda t: campath(t, 7.4, 11.0, (1300, 470, 1.55), (1290, 465, 1.65))))
    S.shot(11.0, 15.2, sh(lambda t: campath(t, 11.0, 15.2, (2320, 500, 1.5), (2330, 490, 1.4))))
    S.shot(15.2, 19.4, sh(lambda t: campath(t, 15.2, 19.4, (1300, 470, 1.6), (1300, 470, 1.7))))
    S.shot(19.4, 28.0, sh(lambda t: campath(t, 19.4, 28.0, (1800, 520, 1.0), (1800, 600, 0.95))))
    return S

# ======================= SCENE 3 — the traveller =======================
MSPEED = 50.0
def s3():
    S = Scene('s3', 25.0); c = S.cues
    c.say('s3_01', 1.0); c.say('s3_02', 9.0); c.say('s3_03', 12.6); c.say('s3_04', 18.4)
    S.music += [(0.0, 12.4, 'chelona'), (12.4, 18.2, 'theme_soft'), (18.2, 23.0, 'lagos_soft'), (22.6, 25.0, 'tension_soft')]
    S.fx(0.0, 'wind_soft_on', 0.5); S.fx(0.0, 'birds_on', 0.6)
    for k in range(int(25/0.56)): S.fx(0.2+k*0.56, 'step', 0.35)
    S.fx(22.6, 'inhale', 0.9)
    mb = auto_blinks(301, 30); vb = auto_blinks(302, 30, 3.0); ib = auto_blinks(303, 30, 3.6)
    Wf = lambda t: 0.2
    def mx(t): return 150+MSPEED*t
    def mit(t, **kw):
        x = mx(t)
        sing = 9.0 <= t < 11.8
        P = dict(x=x, y=mitsos_y(x), s=0.72, f=1, walk=t*0.9, wamp=1.0, eye=blink_at(t, mb), mouth=c.mouth('MITSOS', t), smile=0.9,
                 basket=True, look=(0.5, -0.1), wind=0.12+0.05*math.sin(t*2), hd=0.06*math.sin(t*5.6)*(1 if sing else 0.3))
        if sing: P['happy'] = (t % 1.2) < 0.7
        P.update(kw); return P
    def vor(t, **kw):
        inh = ramp(t, 22.6, 24.6)
        P = dict(x=VX, y=VY, s=VS*(1+0.18*inh), f=-1, eye=blink_at(t, vb), mouth=c.mouth('VORIAS', t), puff=0.9*inh, brow=0.7, smile=1.0,
                 look=(0.7, 0.9))
        if 18.4 <= t < 22.6: P['look'] = (1, 0.1)
        P.update(kw); return P
    def ili(t, **kw):
        P = dict(x=IX, y=IY, s=IS, eye=blink_at(t, ib), mouth=c.mouth('ILIOS', t), shine=0.35, look=(0.5, 1.0), smile=0.9)
        if 15.4 <= t < 18.0: P['look'] = (1, 0.1)
        P.update(kw); return P
    def draw_road(cr, t, sky=False):
        if sky:
            sun(cr, ili(t), t); wind_cloud(cr, vor(t), t)
        bear(cr, mit(t), t)
    def wmb(t): return lambda cr, L: windmill_sails(cr, t, spin_of(t, Wf))
    S.shot(0, 9.0, lambda lt, t: frame('road', 'morning', campath(t, 0, 9.0, (900, 900, 0.95), (1000, 960, 1.0)),
                                       draw=lambda cr, L: draw_road(cr, t), over_back=wmb(t), fade=1-ramp(t, 0, 0.6)))
    S.shot(9.0, 12.4, lambda lt, t: frame('road', 'morning', (mx(t)+60, 1150, 1.75), draw=lambda cr, L: draw_road(cr, t), over_back=wmb(t)))
    S.shot(12.4, 18.2, lambda lt, t: frame('road', 'morning', campath(t, 12.4, 18.2, (1700, 780, 0.76), (1700, 770, 0.78)),
                                           draw=lambda cr, L: draw_road(cr, t, True), over_back=wmb(t)))
    S.shot(18.2, 25.0, lambda lt, t: frame('road', 'morning', campath(t, 18.2, 25.0, (2300, 500, 1.4), (2320, 490, 1.55)),
                                           draw=lambda cr, L: wind_cloud(cr, vor(t), t), over_back=wmb(t)))
    return S

# ======================= SCENE 4 — the wind blows =======================
X4 = 150+MSPEED*25.0     # where Mitsos is when the wind starts (1950)
WALL_Y = lambda x: 1150-8*math.sin(x/900)
def s4():
    S = Scene('s4', 30.0); c = S.cues
    c.say('s4_01', 2.6); c.say('s4_02', 5.6); c.say('s4_03', 10.6); c.say('s4_04', 12.0); c.say('s4_05', 12.5)
    c.say('s4_06', 14.4); c.say('s4_07', 18.6); c.say('s4_08', 23.4); c.say('s4_09', 27.6)
    S.music += [(0.0, 5.4, 'tension_soft'), (5.4, 22.8, 'race'), (22.8, 27.3, 'tension_soft'), (27.3, 30.0, 'sting')]
    def Wf(t): return clamp(0.55*ramp(t, 0.2, 1.4)+0.45*ramp(t, 5.4, 9.0)) * (1-0.9*ramp(t, 22.8, 24.6))
    S.fx(0.0, 'wind_strong_on', 0.9)
    for tt in (0.2, 3.0, 5.6, 8.0, 10.2, 13.0, 16.2, 18.8, 21.0): S.fx(tt, 'whoosh_l', 0.55)
    S.fx(12.0, 'flutter', 0.7); S.fx(10.4, 'flutter', 0.4); S.fx(14.4, 'chatter', 0.6); S.fx(23.2, 'puff', 0.8); S.fx(27.4, 'chime', 0.7)
    mb = auto_blinks(401, 40); vb = auto_blinks(402, 40, 3.0); ib = auto_blinks(403, 40, 3.6); sb = auto_blinks(404, 40)
    def mx(t): return X4+lerp(0, 120, clamp(t/22))
    def mit(t, **kw):
        W = Wf(t); x = mx(t)
        hug = ramp(t, 13.6, 14.6)
        P = dict(x=x, y=mitsos_y(x), s=0.72, f=1, eye=blink_at(t, mb), mouth=c.mouth('MITSOS', t), smile=0.4, basket=hug < 0.5,
                 wind=W, hug=hug, look=(0.6, -0.1), brow=0.0, lean=0.15*W, walk=t*0.5 if (t > 6 and t < 23) else 0.0,
                 wamp=0.5 if (6 < t < 23) else 0.0)
        if t < 5.6: P['look'] = (-0.3+0.9*math.sin(t*1.4), -0.4); P['wide'] = 1.15; P['shiver'] = 0.5*ramp(t, 0.5, 1.5)
        if 14.4 <= t < 15.4: P['chatter'] = True; P['shiver'] = 1.0
        if t >= 14.4: P['brow'] = -0.7; P['smile'] = -0.1; P['look'] = (0.9, -0.3)
        if 18.4 <= t < 23.0: P['lean'] = 0.3*W; P['eye'] = min(P['eye'], 0.55); P['shiver'] = 0.5
        if t >= 23.6: P['eye'] = blink_at(t, mb); P['brow'] = 0.3; P['look'] = (0.6, -0.8); P['smile'] = 0.3
        P.update(kw); return P
    def vor(t, **kw):
        W = Wf(t); tired = ramp(t, 22.8, 24.4)
        P = dict(x=VX, y=VY+40*tired, s=VS*(1.12-0.2*tired), f=-1, eye=blink_at(t, vb), mouth=c.mouth('VORIAS', t),
                 puff=clamp(W*1.3)*(1-tired), brow=0.8*(1-tired)-0.6*tired, look=(0.7, 0.9), rot=0.05*math.sin(t*9)*W+0.12*tired,
                 sweat=tired > 0.3, wob=1+2*W)
        if tired > 0.3: P['eye'] = min(blink_at(t, vb), 0.55); P['smile'] = -0.2
        P.update(kw); return P
    def ili(t, **kw):
        P = dict(x=IX, y=IY, s=IS, eye=blink_at(t, ib), mouth=c.mouth('ILIOS', t), shine=0.35, look=(0.6, 0.9), smile=0.9)
        if t >= 27.0: P['look'] = (0.0, 0.2); P['smile'] = 1.0
        if 28.6 <= t < 29.2: P['wink'] = 1-math.sin(math.pi*(t-28.6)/0.6)
        P.update(kw); return P
    def sparrows_P(t):
        out = []
        base = mx(t)-400
        for i, w in enumerate(('PIP', 'PIM', 'PIO')):
            x = base+i*70; y = WALL_Y(x)
            P = dict(x=x, y=y, s=1.0, who=w, f=1, mouth=c.mouth(w, t), eye=blink_at(t, sb[i::3]), look=(0.6, -0.2), wide=1.2,
                     tailw=math.sin(t*25+i), squash=0.2)
            if w == 'PIM' and t >= 11.9:
                k = clamp((t-11.9)/1.6)
                P['x'] = x-k*520; P['y'] = y-math.sin(k*math.pi)*160-k*40; P['flap'] = math.sin(t*30); P['happy'] = True; P['squash'] = 0
                P['_rot'] = -k*6.28
            if w == 'PIO': P['look'] = (0.9, 0.3); P['wide'] = 1.0
            out.append(P)
        return out
    def draw_sky(cr, t, gust_to=None):
        sun(cr, ili(t), t)
        V = vor(t); wind_cloud(cr, V, t)
        W = Wf(t)
        if gust_to and W > 0.05:
            mx_, my_ = cloud_mouth(V); gust(cr, mx_-20, my_+10, gust_to[0], gust_to[1], W, t, seed=41, n=14, spread=110)
    def draw_road(cr, t, sky=False, birds=True):
        W = Wf(t)
        if sky: draw_sky(cr, t, gust_to=(mx(t)-700, 1260))
        if birds:
            for P in sparrows_P(t):
                if '_rot' in P:
                    cr.save(); cr.translate(P['x'], P['y']-30); cr.rotate(P['_rot']); P['x'], P['y'] = 0, 30; sparrow(cr, P, t); cr.restore()
                else: sparrow(cr, P, t)
        ground_gust(cr, t, W, mx(t)+900, mx(t)-900, 1200, seed=44)
        bear(cr, mit(t), t)
        blown_leaves(cr, t, W, (mx(t)-1500, 700, mx(t)+1500, 1400), seed=45, n=40)
    def eg(t): return (0.55, 0.65, 0.85, 0.07*Wf(t))
    def ob(t): return lambda cr, L: windmill_sails(cr, t, spin_of(t, Wf)+0.3)
    def F(cam, d, **kw):
        return frame('road', 'morning', cam, draw=d, extra_grade=eg(kw.pop('t')), **kw)
    S.shot(0, 2.6, lambda lt, t: F(campath(t, 0, 2.6, (2280, 520, 1.45), (2200, 560, 1.3)), lambda cr, L: draw_sky(cr, t, (1000, 1250)), t=t, over_back=ob(t)))
    S.shot(2.6, 5.6, lambda lt, t: F((mx(t)+40, 1150, 1.9), lambda cr, L: draw_road(cr, t, birds=False), t=t, over_back=ob(t), shake=(math.sin(t*37)*3*Wf(t), 0)))
    S.shot(5.6, 10.4, lambda lt, t: F(campath(t, 5.6, 10.4, (1750, 780, 0.78), (1780, 790, 0.8)), lambda cr, L: draw_road(cr, t, sky=True), t=t, over_back=ob(t)))
    S.shot(10.4, 14.2, lambda lt, t: F(campath(t, 10.4, 14.2, (mx(t)-260, 1090, 2.2), (mx(t)-280, 1080, 2.1)), lambda cr, L: draw_road(cr, t), t=t, over_back=ob(t)))
    S.shot(14.2, 18.4, lambda lt, t: F(campath(t, 14.2, 18.4, (mx(t)+30, 1120, 2.1), (mx(t)+30, 1110, 2.3)), lambda cr, L: draw_road(cr, t, birds=False), t=t, over_back=ob(t),
                                       shake=(math.sin(t*41)*4*Wf(t), 0)))
    S.shot(18.4, 23.0, lambda lt, t: F(campath(t, 18.4, 23.0, (1780, 790, 0.8), (1800, 800, 0.84)), lambda cr, L: draw_road(cr, t, sky=True), t=t, over_back=ob(t)))
    S.shot(23.0, 27.3, lambda lt, t: F(campath(t, 23.0, 27.3, (2330, 520, 1.45), (2340, 560, 1.6)), lambda cr, L: draw_sky(cr, t), t=t, over_back=ob(t)))
    S.shot(27.3, 30.0, lambda lt, t: F(campath(t, 27.3, 30.0, (1270, 450, 1.6), (1260, 440, 1.8)), lambda cr, L: draw_sky(cr, t), t=t, over_back=ob(t),
                                       fade=ramp(t, 29.2, 30.0)))
    return S

# ======================= SCENE 5 — the sun shines =======================
X5 = X4+120
SIT_X = ROAD_TREE-90
def s5():
    S = Scene('s5', 28.0); c = S.cues
    c.say('s5_01', 1.0); c.say('s5_02', 7.8); c.say('s5_03', 11.6); c.say('s5_04', 15.4); c.say('s5_05', 18.4); c.say('s5_06', 24.6)
    S.music += [(0.0, 7.6, 'sunrise'), (7.6, 18.2, 'theme_soft'), (18.2, 28.0, 'lullaby')]
    S.fx(0.0, 'birds_on', 0.6); S.fx(0.0, 'cicadas_on', 0.5); S.fx(2.0, 'chime', 0.6)
    S.fx(19.3, 'whoosh_m', 0.8); S.fx(19.9, 'pop', 0.5); S.fx(22.6, 'thud', 0.4); S.fx(24.4, 'sigh', 0.0)
    mb = auto_blinks(501, 40); ib = auto_blinks(502, 40, 3.6)
    warm = lambda t: ramp(t, 2.0, 7.0)*0.5+0.5*ramp(t, 9.0, 17.0)
    def mpos(t):
        if t < 11.4: return X5, False
        if t < 18.4: return X5+lerp(0, 560, (t-11.4)/7.0), True
        if t < 20.9: return X5+560+lerp(0, 60, clamp((t-18.4)/2.5)), (t < 18.9 or t > 20.4)
        if t < 23.6: return X5+620+lerp(0, SIT_X-X5-620-40, clamp((t-20.9)/2.7)), True
        return SIT_X, False
    def mit(t, **kw):
        x, walking = mpos(t)
        w = warm(t)
        P = dict(x=x, y=mitsos_y(x), s=0.72, f=1, eye=blink_at(t, mb), mouth=c.mouth('MITSOS', t), smile=0.7, basket=True,
                 wind=0.05, hug=1-ramp(t, 8.0, 9.2), closed=1-ramp(t, 9.2, 10.0), look=(0.4, -0.6), warm=w, sweat=ramp(t, 12.0, 14.0)*(1-ramp(t, 20.0, 21.0)))
        if walking: P['walk'] = t*(0.8 if t < 18.4 else 1.1); P['wamp'] = 0.9
        if 7.8 <= t < 10.6: P['look'] = (0.2, -0.9); P['smile'] = 1.0; P['happy'] = 8.6 < t < 9.8
        if 11.4 <= t < 18.4: P['fan'] = ramp(t, 12.4, 12.9)
        if 15.4 <= t < 18.4: P['brow'] = 0.5; P['smile'] = 0.3
        if t >= 18.4:
            P['cloak'] = 'carry' if t >= 19.6 else 'on'; P['fan'] = 0
            if t < 19.6: P['arms'] = [(lerp(0.25, 2.2, ramp(t, 18.5, 19.0)), lerp(-0.35, 1.3, ramp(t, 18.5, 19.0))), (0.1, -0.25)]
            elif t < 20.4: P['arms'] = [(lerp(2.2, 1.2, ramp(t, 19.6, 20.1)), lerp(1.3, -0.9, ramp(t, 19.6, 20.1))), (0.1, -0.25)]
            else: P['arms'] = [(1.2, -0.9), (0.1, -0.25)]
            P['swish'] = clamp((t-19.25)/0.7) if 19.25 <= t < 19.95 else 0.0
            P['basket'] = 'far'
            P['look'] = (0.7, -0.2); P['smile'] = 1.0; P['happy'] = 19.8 < t < 20.8
        if t >= 23.6:
            P = dict(x=SIT_X+60, y=mitsos_y(SIT_X)+14, s=0.72, f=-1, sit=True, cloak='off', eye=blink_at(t, mb), mouth=c.mouth('MITSOS', t),
                     smile=1.0, look=(0.3, -0.3), arms=[(0.6, -0.6), (0.4, -0.5)], warm=0.3)
            if t >= 24.4: P['happy'] = True
        P.update(kw); return P
    def ili(t, **kw):
        P = dict(x=IX, y=IY, s=IS, eye=blink_at(t, ib), mouth=c.mouth('ILIOS', t), shine=0.35+0.65*ramp(t, 2.0, 5.0), look=(0.5, 1.0), smile=1.0)
        P.update(kw); return P
    def draw_road(cr, t, sky=False):
        if sky: sun(cr, ili(t), t)
        if t >= 23.6:
            folded_cloak(cr, SIT_X-60, mitsos_y(SIT_X)+26, 0.62); basket(cr, SIT_X-150, mitsos_y(SIT_X)+18, 0.62)
        bear(cr, mit(t), t)
    def sunrays(cr, t, a):
        if a <= 0: return
        for k in range(7):
            ang = 0.35+k*0.12+0.02*math.sin(t*0.7+k)
            cr.move_to(IX, IY); cr.line_to(IX+math.cos(ang)*3000, IY+math.sin(ang)*3000); cr.line_to(IX+math.cos(ang+0.04)*3000, IY+math.sin(ang+0.04)*3000)
            cr.close_path(); fill(cr, (1, 0.9, 0.55, 0.06*a))
    def eg(t): return (1, 0.72, 0.35, 0.1*warm(t))
    def ob(t): return lambda cr, L: windmill_sails(cr, t, 0.03*t+2.0)
    def F(cam, d, t, **kw): return frame('road', 'morning', cam, draw=d, extra_grade=eg(t), over_back=ob(t), **kw)
    def sky1(cr, t):
        sunrays(cr, t, ramp(t, 3.0, 6.0))
        sun(cr, ili(t), t)
        k = ramp(t, 1.2, 4.2)
        sky_cloud(cr, IX+lerp(20, -520, k), IY+40+lerp(0, 60, k), 1.15, 1.0)
        sky_cloud(cr, IX+lerp(-60, 560, k), IY-60-lerp(0, 40, k), 0.8, 1.0)
    S.shot(0, 7.6, lambda lt, t: F(campath(t, 0, 7.6, (1300, 470, 1.35), (1350, 560, 1.1)), lambda cr, L: sky1(cr, t), t, fade=1-ramp(t, 0, 0.8)))
    S.shot(7.6, 11.4, lambda lt, t: F((X5+40, 1140, 1.9), lambda cr, L: draw_road(cr, t), t))
    S.shot(11.4, 15.2, lambda lt, t: F((mpos(t)[0]+60, 1085, 1.5),
                                       lambda cr, L: (sunrays(cr, t, 1), draw_road(cr, t)), t))
    S.shot(15.2, 18.4, lambda lt, t: F((mpos(t)[0]+40, 1130, 2.3), lambda cr, L: draw_road(cr, t), t))
    S.shot(18.4, 20.9, lambda lt, t: F((mpos(t)[0]+30, 1120, 1.9), lambda cr, L: draw_road(cr, t), t))
    S.shot(20.9, 23.6, lambda lt, t: F(campath(t, 20.9, 23.6, (2300, 880, 0.95), (2450, 920, 1.0)), lambda cr, L: (sunrays(cr, t, 1), draw_road(cr, t, True)), t))
    S.shot(23.6, 28.0, lambda lt, t: F(campath(t, 23.6, 28.0, (SIT_X-20, 1170, 1.9), (SIT_X-20, 1160, 2.1)), lambda cr, L: draw_road(cr, t), t))
    return S

# ======================= SCENE 6 — who won =======================
def s6():
    S = Scene('s6', 28.0); c = S.cues
    c.say('s6_01', 0.6); c.say('s6_02', 4.0); c.say('s6_03', 10.8); c.say('s6_04', 14.8); c.say('s6_05', 21.0); c.say('s6_06', 25.0, 'SPARROWS')
    S.music += [(0.0, 4.0, 'tension_soft'), (4.0, 17.2, 'theme_soft'), (17.2, 21.0, 'lullaby'), (21.0, 25.0, 'theme_soft'), (25.0, 28.0, 'village_dance')]
    S.fx(0.0, 'birds_on', 0.5); S.fx(0.0, 'cicadas_on', 0.4); S.fx(17.6, 'breeze', 0.9); S.fx(24.0, 'flutter', 0.6); S.fx(25.0, 'pop', 0.5)
    vb = auto_blinks(601, 40, 3.0); ib = auto_blinks(602, 40, 3.6); mb = auto_blinks(603, 40); sb = auto_blinks(604, 40)
    Wb = lambda t: 0.3*pulse(t, 17.6, 27.0, 0.8)
    def vor(t, **kw):
        P = dict(x=VX, y=VY+30, s=VS*0.95, f=-1, eye=blink_at(t, vb), mouth=c.mouth('VORIAS', t), brow=0.2, look=(1, 0.1), smile=0.3, wob=0.6)
        if t < 3.6: P['brow'] = 0.9; P['wide'] = 1.2; P['smile'] = -0.2; P['look'] = (0.6, 0.9)
        if 10.8 <= t < 12.4: P['look'] = (0.6, 0.6); P['brow'] = -0.2
        if 12.4 <= t < 14.6: P['brow'] = 0.9; P['smile'] = 0.9
        if 17.4 <= t < 21.0: P['puff'] = 0.45*pulse(t, 17.6, 20.6, 0.4); P['look'] = (0.8, 0.9)
        if t >= 21.0: P['look'] = (0.6, 0.9); P['smile'] = 1.0; P['happy'] = t > 25.0
        P.update(kw); return P
    def ili(t, **kw):
        P = dict(x=IX, y=IY, s=IS, eye=blink_at(t, ib), mouth=c.mouth('ILIOS', t), shine=0.6, look=(0.8, 0.1), smile=1.0)
        if t >= 17.4: P['look'] = (0.6, 0.9)
        if t >= 25.0: P['happy'] = True
        P.update(kw); return P
    def mit(t, **kw):
        P = dict(x=SIT_X+60, y=mitsos_y(SIT_X)+14, s=0.72, f=-1, sit=True, cloak='off', eye=blink_at(t, mb), mouth=c.mouth('MITSOS', t),
                 smile=1.0, look=(0.3, -0.3), arms=[(0.6, -0.6), (0.4, -0.5)], warm=0.3*(1-ramp(t, 19, 22)))
        if 19.0 <= t < 21.0: P['eye'] = 0.0; P['smile'] = 1.0
        if t >= 24.6: P['happy'] = True; P['arms'] = [(2.8, -0.3), (0.4, -0.5)]
        P.update(kw); return P
    def draw_sky(cr, t, breeze_to=None):
        sun(cr, ili(t), t); V = vor(t); wind_cloud(cr, V, t)
        if breeze_to and Wb(t) > 0.02:
            mx_, my_ = cloud_mouth(V)
            gust(cr, mx_-20, my_+10, breeze_to[0], breeze_to[1], Wb(t), t, seed=61, n=6, spread=60, col=(1, 1, 1), lw=4)
    def sparrows(cr, t):
        for i, w in enumerate(('PIP', 'PIM', 'PIO')):
            k = ramp(t, 23.8+i*0.2, 24.6+i*0.2)
            tx, ty = ROAD_TREE-150+i*70, 945-i*6
            P = dict(x=lerp(tx-500, tx, k), y=lerp(ty-300, ty, k), s=0.95, who=w, f=1, flap=math.sin(t*30)*(1-k), mouth=c.mouth(w, t),
                     eye=blink_at(t, sb[i::3]), look=(0.5, 0.6), happy=t > 25.0)
            if k > 0: sparrow(cr, P, t)
    def draw_road(cr, t, sky=False):
        if sky: draw_sky(cr, t, breeze_to=(SIT_X-100, 1200))
        folded_cloak(cr, SIT_X-60, mitsos_y(SIT_X)+26, 0.62); basket(cr, SIT_X-150, mitsos_y(SIT_X)+18, 0.62)
        bear(cr, mit(t), t)
        blown_leaves(cr, t, Wb(t)*0.6, (SIT_X-900, 700, SIT_X+600, 1300), seed=66, n=14)
        sparrows(cr, t)
    def ob(t): return lambda cr, L: windmill_sails(cr, t, 0.03*t+2.0+0.4*Wb(t))
    def F(cam, d, t, **kw): return frame('road', 'morning', cam, draw=d, extra_grade=(1, 0.72, 0.35, 0.05), over_back=ob(t), **kw)
    S.shot(0, 4.0, lambda lt, t: F(campath(t, 0, 4.0, (2330, 520, 1.5), (2340, 520, 1.6)), lambda cr, L: draw_sky(cr, t), t, fade=1-ramp(t, 0, 0.4)))
    S.shot(4.0, 10.4, lambda lt, t: F(campath(t, 4.0, 10.4, (1290, 470, 1.55), (1290, 470, 1.7)), lambda cr, L: draw_sky(cr, t), t))
    S.shot(10.4, 14.6, lambda lt, t: F(campath(t, 10.4, 14.6, (2320, 520, 1.6), (2320, 510, 1.5)), lambda cr, L: draw_sky(cr, t), t))
    S.shot(14.6, 21.0, lambda lt, t: F(campath(t, 14.6, 21.0, (1800, 560, 1.0), (1850, 620, 0.95)), lambda cr, L: draw_sky(cr, t, breeze_to=(2600, 1200)), t))
    S.shot(21.0, 24.8, lambda lt, t: F(campath(t, 21.0, 24.8, (SIT_X-60, 1130, 1.8), (SIT_X-60, 1110, 1.7)), lambda cr, L: draw_road(cr, t), t))
    S.shot(24.8, 28.0, lambda lt, t: F(campath(t, 24.8, 28.0, (2300, 820, 0.85), (2000, 760, 0.76)), lambda cr, L: draw_road(cr, t, True), t,
                                       fade=ramp(t, 27.3, 28.0)))
    return S

# ======================= SCENE 7 — home, and goodnight =======================
def s7():
    S = Scene('s7', 25.0); c = S.cues
    c.say('s7_01', 0.9); c.say('s7_02', 10.4); c.say('s7_03', 16.0)
    S.music += [(0.0, 9.6, 'theme_soft'), (9.6, 20.4, 'lullaby'), (20.8, 25.0, 'theme')]
    S.fx(0.0, 'birds_on', 0.3); S.fx(9.6, 'crickets_on'); S.fx(19.6, 'puff')
    gb = auto_blinks(701, 30, 3.5)
    def sh1(lt, t):
        cam = campath(t, 0, 9.6, (1900, 760, 0.8), (2200, 760, 0.8))
        def d(cr, L):
            sun(cr, dict(x=IX+200, y=IY+260+t*12, s=0.9, shine=0.6, eye=1, look=(0.6, 0.6), smile=1.0, happy=True, mouth=0), t)
            wind_cloud(cr, dict(x=VX+100, y=VY+80, s=0.85, f=-1, eye=1, look=(0.5, 0.8), smile=1.0, happy=True, wob=0.6), t)
            gust(cr, VX-60, VY+160, VX-1000, VY+700, 0.25, t, seed=71, n=5, spread=50, lw=4)
            x = 1700+t*95
            bear(cr, dict(x=x, y=mitsos_y(x), s=0.66, f=1, walk=t*0.9, wamp=1.0, basket=True, wind=0.15, eye=1, smile=1.0, look=(0.5, -0.1)), t)
            blown_leaves(cr, t, 0.15, (1400, 900, 3400, 1300), seed=72, n=8)
        return frame('road', 'sunset', cam, draw=d, over_back=lambda cr, L: windmill_sails(cr, t, 0.06*t), fade=max(1-ramp(t, 0, 0.5), ramp(t, 9.0, 9.6)))
    S.shot(0, 9.6, sh1)
    def sh2(lt, t):
        cam = campath(t, 9.6, 16.0, (1110, 690, 1.25), (1100, 620, 1.6))
        blow = pulse(t, 19.5, 20.3, 0.15); out = t >= 20.2
        gest = pulse(t, 12.4, 15.0, 0.4)
        def d(cr, L):
            if not out: glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35)
            P = dict(x=1100, y=905, s=2.4, eye=blink_at(t, gb), mouth=max(c.mouth('GLAFKA', t), 0.6*blow), tilt=0.05*osc(t, 0.35)+0.25*blow,
                     wings=(0.0, 0.9*gest), look=(0.6*blow, 0.3*blow))
            if 18.4 <= t < 19.0: P['wink'] = 1-math.sin(math.pi*(t-18.4)/0.6)
            owl(cr, P, t)
            if not out: lamp(cr, LAMP[0], LAMP[1], 1.7, 1-0.6*ramp(t, 19.7, 20.2), t)
            else:
                lamp(cr, LAMP[0], LAMP[1], 1.7, 0, t)
                k = clamp((t-20.2)/1.2)
                for j in range(6):
                    ell(cr, LAMP[0]+62+math.sin(j+t*2)*10*k, LAMP[1]-60-j*18-k*60, 6+j*2, 4+j, 0); fill(cr, (0.8, 0.8, 0.85, 0.35*(1-k)))
        return frame('hollow', 'night', cam, draw=d, extra_grade=(0, 0, 0.05, 0.55*ramp(t, 20.2, 20.5)), fade=max(1-ramp(t, 9.6, 10.2), ramp(t, 20.3, 20.8)))
    S.shot(9.6, 20.8, sh2)
    def sh3(lt, t):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(s)
        title_card3(cr, ramp(lt, 0.2, 1.2)*(1-ramp(lt, 3.4, 4.2)))
        return s
    S.shot(20.8, 25.0, sh3)
    return S
