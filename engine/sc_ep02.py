"""Episode 02 — The Lion and the Mouse."""
from kit import *
from chars2 import *
import bgs2
import engine as _eng
def frame(loc, tod, cam, **kw):
    if cam[2] >= 1.45 and 'layers' not in kw: kw['layers'] = ('back', 'main')   # tall fg grass hides small cast in close-ups
    return _eng.frame(loc, tod, cam, **kw)

LAMP = (1300, 902)
def title_card2(cr, a, sub="The Lion and the Mouse"):
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

def arc_pos(t, t0, t1, p0, p1, hgt):
    k = clamp((t-t0)/(t1-t0)); return (lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k)-math.sin(math.pi*k)*hgt), k

def head_world(P):
    hx, hy = P['_head']; return (P['x']+P.get('f', 1)*P['s']*hx, P['y']-P.get('air', 0)+P['s']*hy)

# ======================= SCENE 1 — Glafka opens =======================
def s1():
    S = Scene('s1', 30.0); c = S.cues
    c.say('s1_01', 10.5); c.say('s1_02', 14.8); c.say('s1_03', 20.0); c.say('s1_04', 24.0)
    S.music.append((0.0, 30.0, 'theme'))
    S.fx(1.0, 'crickets_on'); S.fx(7.6, 'flint'); S.fx(8.0, 'flame'); S.fx(3.0, 'hoot', 0.35)
    blinks = [9.4, 13.9, 19.5, 23.2, 27.0]
    def gl(t, **kw):
        P = dict(x=1100, y=905, s=2.4, eye=blink_at(t, blinks), mouth=c.mouth('GLAFKA', t), tilt=0.05*osc(t, 0.35))
        P.update(kw); return P
    def sh1(lt, t):
        cam = campath(lt, 0, 6, (1500, 1330, 1.05), (1500, 850, 0.82))
        def d(cr, L): fireflies(cr, t, 2, (900, 700, 2100, 1250), 40)
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
        cam = campath(t, 10.5, 24, (1120, 680, 1.25), (1110, 640, 1.4))
        sw = lerp(0.7, 0.0, ramp(t, 10.5, 11.0))
        big = pulse(t, 16.2, 17.6, 0.3); small = pulse(t, 18.2, 19.4, 0.3)
        def d(cr, L):
            glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35)
            owl(cr, gl(t, swivel=sw*0.5, look=(sw, 0), wings=(1.3*big+0.2*small, 1.3*big+0.2*small), wide=1+0.18*small,
                       tilt=0.05*osc(t, 0.35)+0.12*small), t)
            lampdraw(cr, t, 1)
            if small > 0.05:   # tiny pinch of wing-tips -> a little sparkle
                glow(cr, 1100, 640, 40, (1, 0.95, 0.7), 0.6*small)
        return frame('hollow', 'blue', cam, draw=d, extra_grade=(1, 0.6, 0.3, 0.06))
    S.shot(10.5, 24.0, sh3)
    def sh4(lt, t):
        cam = campath(t, 24.0, 26.5, (1110, 640, 1.4), (1110, 600, 1.8))
        if t > 27.6: cam = campath(t, 27.6, 29.8, cam, (LAMP[0]+61, LAMP[1]-50, 7.0), ease)
        laugh = pulse(t, 24.0, 25.0, 0.1)
        def d(cr, L):
            glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35)
            P = gl(t, tilt=0.06*math.sin(t*30)*laugh, wings=(0.5*laugh, 0.5*laugh), y=905-8*laugh*abs(math.sin(t*20)))
            if 26.4 <= t < 27.0: P['wink'] = 1-math.sin(math.pi*(t-26.4)/0.6)
            if laugh > 0.3: P['happy'] = True
            owl(cr, P, t); lampdraw(cr, t, 1)
        return frame('hollow', 'blue', cam, draw=d, extra_grade=(1, 0.6, 0.3, 0.06), flash=ramp(t, 28.7, 30.0))
    S.shot(24.0, 30.0, sh4)
    return S

# ======================= SCENE 2 — the nap =======================
LX, LY, LS = 1450, 1040, 0.8      # Leon lying under the pine, facing left
def s2():
    S = Scene('s2', 28.0); c = S.cues
    c.say('s2_01', 1.0); c.say('s2_02', 7.8); c.say('s2_03', 14.3); c.say('s2_04', 19.0); c.say('s2_05', 22.6); c.say('s2_06', 26.2)
    S.music += [(0.0, 14.2, 'lullaby'), (14.2, 19.6, 'lagos_soft'), (21.3, 21.9, 'sting'), (22.0, 28.0, 'tension_soft')]
    S.fx(0.0, 'cicadas_on', 0.7)
    for k in range(7): S.fx(1.2+k*2.4, 'snore', 0.5 if k < 6 else 0.3)
    S.fx(8.0, 'patter', 0.6); S.fx(11.6, 'patter', 0.6); S.fx(16.9, 'pop'); S.fx(20.1, 'achoo'); S.fx(20.3, 'whoosh_m')
    S.fx(20.9, 'tap'); S.fx(21.8, 'thud'); S.fx(26.2, 'gasp')
    mb = auto_blinks(11, 30)
    def mouse_pos(t):
        if t < 14.0: return (lerp(250, 1060, clamp((t-6.8)/6.8)), 1052), 1, True
        if t < 16.8: return (1060, 1052), 1, False
        if t < 17.6:
            p, k = arc_pos(t, 16.8, 17.6, (1060, 1052), (1190, 890), 80); return p, 1, False
        if t < 18.6: return (lerp(1190, 1275, ramp(t, 17.6, 18.6)), 890-6*math.sin(t*20)), 1, True
        if t < 20.15: return (1275, 892), -1 if t > 19.0 else 1, False
        if t < 20.9:
            p, k = arc_pos(t, 20.15, 20.9, (1275, 892), (1150, 1056), 160); return p, -1, False
        return (1150, 1056), -1, False
    def leon(t, **kw):
        sneeze = pulse(t, 19.0, 20.2, 0.2)
        wake = ramp(t, 20.3, 20.8)
        P = dict(x=LX, y=LY, s=LS, f=-1, pose='lie', headup=wake*0.8, eye=0 if t < 20.6 else blink_at(t, (23.0, 25.4)),
                 mouth=c.mouth('LEON', t) if t >= 19.0 else 0.18+0.12*osc(t, 0.42), smile=0.4 if t < 20.6 else 0.7,
                 hd=-0.12*sneeze+0.25*pulse(t, 20.1, 20.4, 0.05), brow=0.4*ramp(t, 22.4, 22.8), look=(-0.7, 0.6))
        if 19.0 <= t < 20.1: P['eye'] = 0.25; P['brow'] = 0.8*sneeze
        if t >= 21.0:
            P['paw'] = 0.7*pulse(t, 21.0, 21.8, 0.35); P['pawx'] = 36*ramp(t, 21.0, 21.6)
        P.update(kw); return P
    def mouse_P(t, **kw):
        (x, y), f, running = mouse_pos(t)
        P = dict(x=x, y=y, s=0.55, f=f, eye=blink_at(t, mb), mouth=c.mouth('MIKRI', t), look=(0.4, 0))
        if running: P['run'] = t*4; P['lean'] = 0.25
        if t < 16.8: P['hold'] = lambda cr, h: olive(cr, h[0]+6, h[1]-4, 0.9)
        if 20.15 <= t < 20.9: P['rot'] = -(t-20.15)*8; P['wide'] = 1.3
        if t >= 20.9: P['wide'] = 1.25; P['arms'] = [(2.6, -0.4), (2.4, -0.3)]; P['look'] = (0.6, -0.6)
        if 14.3 <= t < 16.8: P['look'] = (0.5, -0.8); P['arms'] = [(1.2, -1.0), (0.3, -0.5)]
        P.update(kw); return P
    def draw_all(cr, t, show_olive=True):
        L = leon(t)
        if t >= 20.9: mouse(cr, mouse_P(t), t)
        lion(cr, L, t)
        if t < 20.3:
            hx, hy = head_world(L); zzz(cr, hx-40, hy-90, t, 1.0)
        if show_olive and t >= 16.8: olive(cr, 1075, 1046, 0.5)
        if t < 20.9: mouse(cr, mouse_P(t), t)
        if 18.6 <= t < 20.1:   # mouse tail tickles the nose: little puff lines
            hx, hy = head_world(L)
            for k in range(3):
                a = t*6+k*2; cr.move_to(hx-30+k*10, hy+10); cr.line_to(hx-30+k*10+math.cos(a)*8, hy+20+math.sin(a)*6); stroke(cr, OUT+(0.6,), 2)
        if 20.05 <= t < 20.6:
            hx, hy = head_world(L)
            k = ramp(t, 20.05, 20.6)
            for j in range(10):
                a = math.pi*0.8+j*0.12; r = 40+k*220
                ell(cr, hx-30+math.cos(a)*r*0.9, hy+20+math.sin(a)*r*0.4, 10*(1-k)+3, 6*(1-k)+2); fill(cr, (1, 1, 1, 0.6*(1-k)))
    def sh1(lt, t):
        cam = campath(lt, 0, 7, (1350, 760, 0.95), (1300, 840, 1.15))
        return frame('meadow', 'afternoon', cam, draw=lambda cr, L: draw_all(cr, t), fade=1-ramp(lt, 0, 0.8))
    S.shot(0, 7, sh1)
    def sh2(lt, t):
        (x, y), f, r = mouse_pos(t)
        cam = (max(600, x+80), 990, 2.1)
        return frame('meadow', 'afternoon', cam, draw=lambda cr, L: draw_all(cr, t), layers=('back', 'main'))
    S.shot(7, 14.0, sh2)
    def sh3(lt, t):
        cam = campath(t, 14.0, 17.6, (1150, 980, 2.1), (1220, 930, 1.85))
        return frame('meadow', 'afternoon', cam, draw=lambda cr, L: draw_all(cr, t), layers=('back', 'main'))
    S.shot(14.0, 22.4, sh3)
    def sh4(lt, t):
        cam = (1225, 950, 2.4)
        return frame('meadow', 'afternoon', cam, draw=lambda cr, L: draw_all(cr, t), layers=('back', 'main'))
    S.shot(22.4, 26.0, sh4)
    def sh5(lt, t):
        cam = (1165, 1000, 3.2)
        return frame('meadow', 'afternoon', cam, draw=lambda cr, L: draw_all(cr, t), layers=('back', 'main'), shake=(math.sin(t*50)*3*pulse(t, 26.2, 26.7, 0.05), 0))
    S.shot(26.0, 28.0, sh5)
    return S

# ======================= SCENE 3 — the promise =======================
def s3():
    S = Scene('s3', 30.0); c = S.cues
    c.say('s3_01', 0.4); c.say('s3_02', 4.0); c.say('s3_03', 6.8); c.say('s3_04', 12.2); c.say('s3_05', 13.8)
    c.say('s3_06', 20.4); c.say('s3_07', 23.9)
    S.music += [(0.0, 13.6, 'theme_soft'), (13.7, 20.2, 'lagos'), (20.2, 30.0, 'theme_soft')]
    S.fx(0.0, 'cicadas_on', 0.7); S.fx(14.1, 'thud', 0.6); S.fx(15.2, 'thud', 0.5); S.fx(26.5, 'patter', 0.7); S.fx(27.5, 'patter', 0.5)
    lb = auto_blinks(21, 32, 3.5); mb = auto_blinks(22, 32)
    MX = 1150
    def leon(t, **kw):
        laugh = pulse(t, 13.8, 19.8, 0.25)
        proud = pulse(t, 4.0, 6.4, 0.2)
        P = dict(x=LX, y=LY, s=LS, f=-1, pose='lie', headup=0.8+0.25*proud, eye=blink_at(t, lb), mouth=c.mouth('LEON', t),
                 smile=0.7, look=(-0.6, 0.6), brow=0.6*proud, fluff=proud)
        P['paw'] = abs(math.sin((t-14.0)*2.6))*0.5*laugh if t >= 14.0 else 0.0; P['pawx'] = 36
        if laugh > 0.3:
            P['happy'] = True; P['hd'] = 0.1*math.sin(t*9)*laugh; P['y'] = LY-4*abs(math.sin(t*9))*laugh
        if 12.2 <= t < 13.4: P['eye'] = 1; P['wide'] = 1.25; P['brow'] = 0.9; P['smile'] = 0.2
        if t >= 20.2: P['look'] = (-0.6, 0.7); P['smile'] = 0.9; P['paw'] = 0.4*pulse(t, 21.4, 23.2, 0.3)
        if t >= 27.5:
            P['headup'] = lerp(0.8, 0.0, ramp(t, 27.5, 29.0)); P['eye'] = 1-ramp(t, 28.4, 29.2); P['smile'] = 0.8
        P.update(kw); return P
    def mouse_P(t, **kw):
        x = MX; f = 1; run = None
        if t >= 26.6: x = MX-ramp(t, 26.6, 30.0, )*0 - (t-26.6)*280; f = -1; run = t*5
        P = dict(x=x, y=1056, s=0.55, f=f, eye=blink_at(t, mb), mouth=c.mouth('MIKRI', t), look=(0.5, -0.7))
        if run is not None: P['run'] = run; P['lean'] = 0.3
        if t < 3.6: P['arms'] = [(2.2, -1.9), (2.0, -1.8)]; P['wide'] = 1.15   # pleading paws together
        if 6.8 <= t < 11.8: P['arms'] = [(2.2, -1.9), (2.0, -1.8)] if t < 10.0 else [(2.8, -0.3), (0.3, -0.5)]
        if 11.8 <= t < 13.5: P['look'] = (0.6, -0.9)
        if 13.8 <= t < 20.0: P['blush'] = 1; P['smile'] = 0.1; P['look'] = (0.4, -0.8)
        if 24.0 <= t < 26.5:
            bow = pulse(t, 24.0, 25.4, 0.3); P['lean'] = 0.45*bow; P['hd'] = 0.3*bow; P['happy'] = bow < 0.3 and t > 25.4
            P['arms'] = [(lerp(0.4, 2.8, ramp(t, 25.3, 25.6)), -0.3), (0.3, -0.5)]
        P.update(kw); return P
    def draw_all(cr, t):
        L = leon(t)
        olive(cr, 1075, 1046, 0.5)
        mouse(cr, mouse_P(t), t)
        lion(cr, L, t)
        if t >= 28.6:
            hx, hy = head_world(L); zzz(cr, hx-40, hy-90, t, 1.0)
    def sh(cam):
        return lambda lt, t: frame('meadow', 'afternoon', cam(t) if callable(cam) else cam, draw=lambda cr, L: draw_all(cr, t), layers=('back', 'main'))
    S.shot(0, 3.9, sh((1150, 990, 3.0)))
    S.shot(3.9, 6.6, sh(lambda t: campath(t, 3.9, 6.6, (1250, 930, 2.4), (1255, 925, 2.6))))
    S.shot(6.6, 12.0, sh(lambda t: campath(t, 6.6, 12.0, (1160, 990, 2.8), (1160, 990, 3.1))))
    S.shot(12.0, 13.6, sh((1250, 920, 3.0)))
    S.shot(13.6, 20.2, sh(lambda t: campath(t, 13.6, 20.2, (1260, 930, 1.6), (1240, 940, 1.75))))
    S.shot(20.2, 26.4, sh(lambda t: campath(t, 20.2, 26.4, (1210, 950, 2.0), (1180, 970, 2.2))))
    S.shot(26.4, 30.0, sh(lambda t: campath(t, 26.4, 30.0, (1150, 900, 1.5), (1250, 850, 1.1))))
    return S

# ======================= SCENE 4 — the net =======================
GY4 = 990
NETX0, NETX1, NETY, NETH = 1630, 2040, 575, 330
PX = 1830                         # where Leon lands
WRAP = (1900, 890, 252, 145)
def net_ropes(cr, k):
    """ropes from the branch tips to the net corners; k=1 hanging, fades when the net falls"""
    if k <= 0: return
    cr.move_to(1630, 588); cr.line_to(NETX0, NETY); cr.move_to(2040, 556); cr.line_to(NETX1, NETY); stroke(cr, OUT+(k,), 4)
def s4():
    S = Scene('s4', 26.0); c = S.cues
    c.say('s4_01', 0.8); c.say('s4_02', 7.3); c.say('s4_03', 12.4); c.say('s4_04', 14.8)
    c.say('s4_05', 18.2); c.say('s4_06', 19.4); c.say('s4_07', 20.2); c.say('s4_08', 21.8)
    S.music += [(0.0, 7.2, 'theme_soft'), (7.2, 10.4, 'lagos_soft'), (11.6, 26.0, 'tension_soft')]
    S.fx(0.0, 'cicadas_on', 0.6); S.fx(10.4, 'whoosh_l'); S.fx(11.0, 'grass'); S.fx(11.4, 'thud'); S.fx(12.0, 'grass', 0.8)
    S.fx(13.4, 'grass', 0.8); S.fx(15.4, 'grass', 0.8); S.fx(17.8, 'flutter', 0.6)
    lb = auto_blinks(31, 30, 3.0); sb = auto_blinks(32, 30)
    def leon_x(t): return lerp(560, 1420, clamp((t-0.5)/8.6))
    def leon(t):
        if t < 10.4:
            x = leon_x(t); walking = t < 9.1
            P = dict(x=x, y=GY4, s=0.75, f=1, pose='stand', eye=blink_at(t, lb), mouth=c.mouth('LEON', t), smile=0.8, look=(0.5, -0.3))
            if walking: P['walk'] = t*0.8; P['wamp'] = 1.0
            cro = ramp(t, 9.2, 9.7)
            P['crouch'] = cro; P['tail'] = 0.3*math.sin(t*12)*cro; P['hd'] = -0.1*cro
            if t > 9.6: P['look'] = (0.8, -0.2); P['brow'] = 0.5
            return P
        if t < 11.4:   # pounce arc
            k = clamp((t-10.4)/1.0)
            x = lerp(1420, PX, k); air = math.sin(math.pi*k)*200
            return dict(x=x, y=GY4, air=air, s=0.75, f=1, pose='stand', reach=1.0, rot=-0.25+0.5*k, eye=1, mouth=0.5, smile=1, look=(0.8, -0.5))
        wrig = 0.5+0.5*math.sin(t*7)
        P = dict(x=PX, y=GY4, s=0.75, f=1, pose='lie', headup=1.0, eye=blink_at(t, lb), mouth=c.mouth('LEON', t), smile=0.1,
                 brow=-0.5, look=(0.4, -0.3), rot=0.03*math.sin(t*8)*(1-ramp(t, 20.0, 21.0)), paw=0.3*wrig, fluff=0.6)
        if t < 12.2: P['wide'] = 1.3; P['eye'] = 1; P['rot'] = 0.06*math.sin(t*20)
        if 18.2 <= t < 21.2: P['look'] = (0.7, -0.8); P['brow'] = 0.4; P['smile'] = -0.2
        if t >= 21.6: P['look'] = (0.0, -0.9); P['brow'] = -0.8; P['hd'] = -0.15
        return P
    def netf(t):
        if t < 10.9: return net_hang(NETX0, NETX1, NETY, NETH, 30), 1.0
        k = ramp(t, 10.9, 11.7)
        tight = ramp(t, 14.8, 17.6)
        cx, cy, rx, ry = WRAP
        wob = 1.0 if t < 20.5 else 0.3
        return net_blend(net_hang(NETX0, NETX1, NETY, NETH, 30), net_wrap(cx, cy, rx*(1-0.07*tight), ry*(1-0.07*tight), t, wob), k), 1-k
    def bfly(t):
        if t < 10.6: return (1830+120*math.sin(t*1.3), 740+60*math.sin(t*2.1))
        k = t-10.6; return (1830+120*math.sin(10.6*1.3)+k*160, 740+60*math.sin(10.6*2.1)-k*180)
    def sparrows(t):
        out = []
        for i, w in enumerate(('PIP', 'PIM', 'PIO')):
            k = ramp(t, 17.6+i*0.2, 18.2+i*0.2)
            tx, ty = 2120+i*58, 548-i*3
            out.append((w, lerp(tx+500, tx, k), lerp(ty-300, ty, k), k))
        return out
    def draw_all(cr, t):
        nf, rk = netf(t)
        net_ropes(cr, rk)
        L = leon(t)
        if t < 10.9: net_mesh(cr, nf, 11, 8)
        lion(cr, L, t)
        if t >= 10.9: net_mesh(cr, nf, 11, 8)
        if t < 13.0: butterfly(cr, *bfly(t), t, 1.1)
        if t >= 17.6:
            for i, (w, x, y, k) in enumerate(sparrows(t)):
                sparrow(cr, dict(x=x, y=y, s=1.05, who=w, f=-1, flap=math.sin(t*30)*(1-k), mouth=c.mouth(w, t), eye=blink_at(t, sb[i::3]),
                                 look=(-0.5, 0.8), wide=1.2 if t > 18.2 else 1), t)
    def sh1(lt, t):
        cam = campath(lt, 0, 7.2, (1250, 620, 0.92), (1500, 640, 0.95))
        return frame('grove', 'late', cam, draw=lambda cr, L: draw_all(cr, t), fade=1-ramp(lt, 0, 0.8))
    S.shot(0, 7.2, sh1)
    def sh2(lt, t):
        cam = campath(t, 7.2, 10.4, (1500, 760, 1.25), (1650, 760, 1.25))
        sh_ = (0, math.sin(t*40)*6*pulse(t, 11.3, 11.8, 0.05))
        return frame('grove', 'late', cam, draw=lambda cr, L: draw_all(cr, t), shake=sh_)
    S.shot(7.2, 12.2, sh2)
    def sh3(lt, t):
        cam = campath(t, 12.2, 17.6, (1900, 830, 1.6), (1930, 830, 1.8))
        return frame('grove', 'late', cam, draw=lambda cr, L: draw_all(cr, t))
    S.shot(12.2, 17.6, sh3)
    def sh4(lt, t):
        cam = campath(t, 17.6, 18.4, (2080, 680, 1.25), (2100, 690, 1.3))
        return frame('grove', 'late', cam, draw=lambda cr, L: draw_all(cr, t))
    S.shot(17.6, 21.4, sh4)
    def sh5(lt, t):
        cam = campath(t, 21.4, 25.0, (1980, 860, 1.7), (2005, 860, 2.6))
        return frame('grove', 'late', cam, draw=lambda cr, L: draw_all(cr, t), fade=ramp(t, 25.0, 26.0))
    S.shot(21.4, 26.0, sh5)
    return S

# ======================= SCENES 5 & 6 — nibble, nibble, snip =======================
SNIPS = [(13.1, (1975, 780)), (14.1, (1935, 790)), (15.6, (1740, 810)), (16.8, (1690, 900)), (18.0, (2090, 830)), (19.2, (2020, 1000))]
def holes_cut(t, snips):
    act = [(p, 48*ramp(t, ts, ts+0.5)) for ts, p in snips if t >= ts]
    if not act: return None
    def cut(x, y):
        for (hx, hy), r in act:
            if (x-hx)**2+(y-hy)**2 < r*r: return True
        return False
    return cut
def gnaw_spot(t, snips):
    """mouse position along the net: hop to each snip point, gnaw before the snip"""
    prev = (2150, GY4)
    for ts, p in snips:
        if t < ts-0.9:
            pp, k = arc_pos(t, ts-1.5, ts-0.9, prev, p, 50) if t >= ts-1.5 else (prev, 0)
            return pp, False
        if t < ts: return p, True
        prev = p
    return prev, False

def s5():
    S = Scene('s5', 21.0); c = S.cues
    c.say('s5_01', 0.6); c.say('s5_02', 4.6); c.say('s5_03', 9.0); c.say('s5_04', 12.0); c.say('s5_05', 15.0)
    S.music += [(0.0, 1.9, 'sting'), (2.0, 4.6, 'race'), (4.6, 11.6, 'tension_soft'), (11.6, 21.0, 'chelona')]
    S.fx(0.0, 'cicadas_on', 0.6); S.fx(2.0, 'whoosh_m'); S.fx(2.2, 'patter'); S.fx(3.4, 'patter'); S.fx(11.5, 'pop')
    for ts, p in SNIPS:
        S.fx(ts-0.85, 'nibble', 0.8); S.fx(ts, 'snip', 0.9)
    lb = auto_blinks(41, 30, 3.0); mb = auto_blinks(42, 30)
    def leon(t):
        P = dict(x=PX, y=GY4, s=0.75, f=1, pose='lie', headup=1.0 if t < 5 else lerp(1.0, 0.6, ramp(t, 5, 6)), eye=blink_at(t, lb),
                 mouth=c.mouth('LEON', t), smile=-0.3, brow=-0.7, look=(0.7, 0.5), fluff=0.2)
        if 5.0 <= t < 8.6: P['eye'] = min(P['eye'], 0.6)
        if t >= 9.0: P['look'] = (0.6, 0.2); P['brow'] = 0.3; P['smile'] = 0.2
        if t >= 11.6: P['look'] = (0.1, -0.9); P['brow'] = 0.6; P['smile'] = 0.4; P['eye'] = 1 if t < 13 else P['eye']
        if 13.0 <= t: P['headup'] = 0.6
        return P
    def mouse_P(t):
        if t < 2.0: x, y, f = 2880, GY4+10, -1
        elif t < 9.6: x, y, f = lerp(2880, 2160, clamp((t-2.0)/2.6)), GY4+10, -1
        elif t < 11.5: x, y, f = 2160, GY4+10, -1
        elif t < 12.1:
            p, k = arc_pos(t, 11.5, 12.1, (2160, GY4+10), SNIPS[0][1], 120); x, y = p; f = -1
        else:
            (x, y), g = gnaw_spot(t, SNIPS); f = -1 if x > 1880 else 1
        P = dict(x=x, y=y, s=0.5, f=f, eye=blink_at(t, mb), mouth=c.mouth('MIKRI', t), look=(-0.2, 0))
        if t < 2.0:
            P['f'] = 1; P['wide'] = 1+0.3*ramp(t, 0.4, 0.6); P['look'] = (0.8, -0.2)
            if t < 0.5: P['hold'] = lambda cr, h: olive(cr, h[0]+6, h[1]-4, 0.9)
        if 2.0 <= t < 4.6: P['run'] = t*5; P['lean'] = 0.35
        if 4.6 <= t < 9.0: P['look'] = (0.6, -0.8)
        if 9.0 <= t < 11.5: P['arms'] = [(2.8, -0.3), (0.3, -0.5)] if t < 10.3 else [(1.0, -2.2), (1.0, -2.2)]; P['brow'] = 0.5
        if t >= 12.1:
            sp, g = gnaw_spot(t, SNIPS)
            if g:
                P['teeth'] = True; P['hd'] = 0.15*math.sin(t*22); P['mouth'] = max(P['mouth'], 0.3+0.3*math.sin(t*22))
                P['arms'] = [(2.6, -0.6), (2.4, -0.5)]
            P['rot'] = 0.0
        return P
    def draw_all(cr, t):
        cx, cy, rx, ry = WRAP
        lion(cr, leon(t), t)
        net_mesh(cr, net_wrap(cx, cy, rx*0.93, ry*0.93, t, 0.3 if t < 11 else 0.1), 12, 9, cut=holes_cut(t, SNIPS))
        if t < 0.5: pass
        elif t < 2.0: olive(cr, 2905, GY4+6, 0.45)
        mouse(cr, mouse_P(t), t)
        for ts, p in SNIPS:
            if ts <= t < ts+0.35:
                k = (t-ts)/0.35
                for j in range(6):
                    a = j*1.05; cr.move_to(p[0]+math.cos(a)*14*(1+k), p[1]+math.sin(a)*14*(1+k)); cr.line_to(p[0]+math.cos(a)*30*(1+k), p[1]+math.sin(a)*30*(1+k))
                stroke(cr, (1, 1, 0.9, 1-k), 3)
    def sh(cam, **kw):
        return lambda lt, t: frame('grove', 'late', cam(t) if callable(cam) else cam, draw=lambda cr, L: draw_all(cr, t), **kw)
    S.shot(0, 2.6, lambda lt, t: frame('grove', 'late', (2860, 930, 2.4), draw=lambda cr, L: draw_all(cr, t), fade=1-ramp(lt, 0, 0.5)))
    S.shot(2.6, 4.6, sh(lambda t: campath(t, 2.6, 4.6, (2500, 870, 1.3), (2120, 850, 1.4))))
    S.shot(4.6, 9.0, sh(lambda t: campath(t, 4.6, 9.0, (2070, 880, 2.1), (2065, 885, 2.3))))
    S.shot(9.0, 12.0, sh((2100, 900, 2.0)))
    S.shot(12.0, 15.0, sh(lambda t: campath(t, 12.0, 15.0, (1960, 800, 2.6), (1950, 800, 2.8))))
    S.shot(15.0, 21.0, sh(lambda t: campath(t, 15.0, 21.0, (1890, 860, 1.5), (1900, 850, 1.6))))
    return S

def s6():
    S = Scene('s6', 23.5); c = S.cues
    c.say('s6_01', 0.3); c.say('s6_02', 3.4); c.say('s6_03', 5.3); c.say('s6_04', 8.0); c.say('s6_05', 15.0); c.say('s6_06', 16.8)
    c.say('s6_07', 19.4, 'SPARROWS')
    S.music += [(0.0, 2.6, 'drumroll'), (2.6, 5.2, 'victory'), (5.2, 18.2, 'theme_soft'), (18.2, 23.5, 'village_dance')]
    S.fx(0.0, 'cicadas_on', 0.5); S.fx(1.2, 'nibble', 0.8); S.fx(1.9, 'snip'); S.fx(2.6, 'snap'); S.fx(2.7, 'whoosh_m'); S.fx(3.3, 'grass')
    S.fx(3.6, 'pop'); S.fx(18.3, 'pop'); S.fx(18.8, 'pop'); S.fx(19.0, 'flutter', 0.6)
    lb = auto_blinks(51, 30, 3.0); mb = auto_blinks(52, 30); sb = auto_blinks(53, 30)
    SN = SNIPS+[(1.9-0.0, (1880, 990))]
    snips6 = [(ts-30 if ts > 5 else ts, p) for ts, p in SN]   # earlier holes already open
    MXF = 2190
    def leon(t):
        if t < 2.6:
            push = ramp(t, 2.0, 2.6)
            return dict(x=PX, y=GY4, s=0.75, f=1, pose='lie', headup=0.6+0.4*push, eye=1, mouth=c.mouth('LEON', t), smile=0.3,
                        brow=0.6, look=(0.5, -0.6), fluff=push, paw=push)
        if t < 7.6:
            jump = pulse(t, 3.4, 4.6, 0.3)
            P = dict(x=PX, y=GY4, s=0.75, f=1, pose='stand', air=abs(math.sin((t-3.4)*5.2))*60*jump, eye=blink_at(t, lb),
                     mouth=c.mouth('LEON', t), smile=1.0, look=(0.6, -0.3), fluff=max(ramp(t, 2.6, 2.8)*(1-ramp(t, 3.3, 3.6)), jump))
            if jump > 0.3: P['happy'] = True
            if t >= 5.0: P['look'] = (0.9, 0.6); P['happy'] = False
            return P
        if t < 19.6:
            lo = ramp(t, 15.0, 16.0)
            P = dict(x=PX, y=GY4, s=0.75, f=1, pose='lie', headup=lerp(1.0, 0.35, lo), eye=blink_at(t, lb), mouth=c.mouth('LEON', t),
                     smile=0.8, look=(0.8, 0.6), brow=0.5, blush=pulse(t, 8.0, 14.6, 0.5))
            if 8.0 <= t < 10.6: P['eye'] = min(P['eye'], 0.6); P['look'] = (0.6, 0.9); P['brow'] = -0.3; P['smile'] = 0.2
            return P
        wk = clamp((t-19.8)/3.7)
        P = dict(x=PX+wk*3.7*95, y=GY4, s=0.75, f=1, pose='stand', eye=blink_at(t, lb), mouth=0, smile=1.0, look=(-0.2, -0.9), walk=(t-19.8)*0.75 if t > 19.8 else 0, wamp=1.0 if t > 19.8 else 0)
        return P
    def mouse_P(t, L):
        P = dict(x=MXF, y=GY4+10, s=0.5, f=-1, eye=blink_at(t, mb), mouth=c.mouth('MIKRI', t), look=(-0.4, -0.5))
        if t < 1.9:
            P['x'], P['y'] = SN[-1][1][0]+40, GY4-10; P['f'] = -1; P['teeth'] = t > 0.9; P['arms'] = [(2.8, -0.4), (1.2, -2.0)]
            if t > 1.2: P['hd'] = 0.15*math.sin(t*22)
        elif t < 3.4:
            p, k = arc_pos(t, 2.6, 3.4, (1920, GY4-10), (MXF, GY4+10), 220) if t >= 2.6 else ((1920, GY4-10), 0)
            P['x'], P['y'] = p; P['rot'] = -6.28*k if t >= 2.6 else 0
        if 5.3 <= t < 7.6:
            P['arms'] = [(0.9, -2.4), (0.9, -2.4)]; P['look'] = (-0.5, -0.6); P['smile'] = 1.0
            if t > 6.2: P['happy'] = True
        if 8.0 <= t < 15.0: P['look'] = (-0.6, -0.7); P['blush'] = ramp(t, 12.0, 13.0)
        if 16.8 <= t < 18.2: P['hop'] = abs(math.sin((t-16.8)*8))*14; P['happy'] = True; P['arms'] = [(2.9, -0.2), (2.7, -0.2)]
        if t >= 18.2:
            hx, hy = head_world(L)
            top = (hx-6, hy-58)
            if t < 19.0:
                p, k = arc_pos(t, 18.2, 19.0, (MXF, GY4+10), top, 120); P['x'], P['y'] = p
            else:
                P['x'], P['y'] = top; P['arms'] = [(2.9, -0.3), (0.4, -0.6)] if t < 21 else [(0.4, -0.6), (0.3, -0.5)]
                P['hold'] = None; P['f'] = 1; P['happy'] = 19.2 < t < 20.8; P['look'] = (0.5, -0.2)
        return P
    def draw_all(cr, t):
        cx, cy, rx, ry = WRAP
        L = leon(t)
        if t < 2.6:
            lion(cr, L, t)
            burst = ramp(t, 2.0, 2.6)
            net_mesh(cr, net_wrap(cx, cy, rx*(0.93+0.15*burst), ry*(0.93+0.15*burst), t, 0.3+burst), 12, 9, cut=holes_cut(t, snips6))
        else:
            k = ramp(t, 2.6, 3.4)
            nf = net_blend(net_wrap(cx, cy, rx*1.08, ry*1.08, t, 1.0), net_pile(1840, GY4+30, 320), k)
            if t < 3.4: lion(cr, L, t)
            net_mesh(cr, nf, 12, 9, cut=holes_cut(t, snips6) if k < 0.15 else None)
            if t >= 3.4: lion(cr, L, t)
        mouse(cr, mouse_P(t, L), t)
        if t >= 18.8:
            for i, w in enumerate(('PIP', 'PIM', 'PIO')):
                k = ramp(t, 18.8+i*0.15, 19.4+i*0.15)
                ang = t*2.2+i*2.1
                tx, ty = L['x']+80+math.cos(ang)*160, 640+math.sin(ang)*40
                sparrow(cr, dict(x=lerp(tx+400, tx, k), y=lerp(ty-300, ty, k), s=0.9, who=w, f=-1 if math.sin(ang) > 0 else 1,
                                 flap=math.sin(t*30), mouth=c.mouth(w, t), eye=1, happy=True), t)
    def sh(cam, **kw):
        return lambda lt, t: frame('grove', 'late', cam(t) if callable(cam) else cam, draw=lambda cr, L: draw_all(cr, t), **kw)
    S.shot(0, 2.4, sh((1950, 930, 2.2)))
    S.shot(2.4, 5.2, sh(lambda t: campath(t, 2.4, 5.2, (1960, 780, 1.25), (1990, 780, 1.3)), ))
    S.shot(5.2, 7.6, sh((2170, 950, 3.0)))
    S.shot(7.6, 15.0, sh(lambda t: campath(t, 7.6, 15.0, (2080, 880, 1.8), (2090, 880, 2.0))))
    S.shot(15.0, 18.0, sh((2090, 900, 2.0)))
    S.shot(18.0, 23.5, sh(lambda t: campath(t, 18.0, 23.5, (2060, 780, 1.4), (2380, 760, 1.3))))
    return S

# ======================= SCENE 7 — home, and goodnight =======================
def s7():
    S = Scene('s7', 25.0); c = S.cues
    c.say('s7_01', 0.9); c.say('s7_02', 9.5); c.say('s7_03', 16.3)
    S.music += [(0.0, 9.0, 'theme_soft'), (9.0, 20.4, 'lullaby'), (20.8, 25.0, 'theme')]
    S.fx(0.0, 'cicadas_on', 0.4); S.fx(9.0, 'crickets_on'); S.fx(19.6, 'puff')
    gb = auto_blinks(61, 30, 3.5)
    def sh1(lt, t):
        cam = campath(t, 0, 9.0, (900, 830, 1.15), (1250, 820, 1.15))
        def d(cr, L):
            x = 380+t*100
            P = dict(x=x, y=1062-x*0.02, s=0.6, f=1, pose='stand', walk=t*1.0, wamp=1.0, eye=1, mouth=0, smile=1.0, look=(0.3, -0.6))
            lion(cr, P, t)
            hx, hy = head_world(P)
            mouse(cr, dict(x=hx-4, y=hy-50+abs(math.sin(t*2*math.pi))*3, s=0.42, f=1, eye=1, happy=True, mouth=0.3*pulse(t, 2, 4),
                           arms=[(2.9+0.3*math.sin(t*6), -0.3), (0.4, -0.6)], hold=lambda cr, h: olive(cr, h[0]+5, h[1]-4, 0.9)), t)
            butterfly(cr, x+260+40*math.sin(t*1.7), hy-120+30*math.sin(t*2.3), t, 0.9)
            fireflies(cr, t, 5, (300, 600, 2500, 1100), 12)
        return frame('meadow', 'sunset', cam, draw=d, fade=ramp(t, 8.4, 9.0))
    S.shot(0, 9.0, sh1)
    def sh2(lt, t):
        cam = campath(t, 9.0, 16.0, (1110, 690, 1.25), (1100, 620, 1.6))
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
        return frame('hollow', 'night', cam, draw=d, extra_grade=(0, 0, 0.05, 0.55*ramp(t, 20.2, 20.5)), fade=max(1-ramp(t, 9.0, 9.6), ramp(t, 20.3, 20.8)))
    S.shot(9.0, 20.8, sh2)
    def sh3(lt, t):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(s)
        title_card2(cr, ramp(lt, 0.2, 1.2)*(1-ramp(lt, 3.4, 4.2)))
        return s
    S.shot(20.8, 25.0, sh3)
    return S
