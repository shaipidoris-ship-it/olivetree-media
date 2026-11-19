"""Episode 2 cast: Leon the lion, Mikri the mouse, olive nets, butterfly. Same style as chars.py."""
from chars import *

LION = dict(fur=hexc('#E0A84E'), belly=hexc('#F3D9A4'), mane=hexc('#B5612A'), mane2=hexc('#CC7A35'),
            muzzle=hexc('#F6E6C4'), nose=hexc('#6B3A2A'), iris=hexc('#C98A2B'), tuft=hexc('#8A4A24'))
MOUSE = dict(fur=hexc('#A0928A'), belly=hexc('#EDE2D3'), pink=hexc('#E7A9A0'), scarf=hexc('#D9462F'), tail=hexc('#D8A49C'))

def _mane(cr, cx, cy, r, t, fluff=0.0, seed=1):
    c = LION
    n = 15
    for ring, (rr, col) in enumerate(((r, c['mane']), (r*0.8, c['mane2']))):
        for k in range(n):
            a = 2*math.pi*k/n + ring*0.2
            w = 1+0.06*math.sin(t*2+k)+fluff*0.15*math.sin(t*25+k*1.7)
            x = cx+math.cos(a)*rr*0.78*w; y = cy+math.sin(a)*rr*0.74*w
            ell(cr, x, y, rr*0.36, rr*0.27, a); fill_stroke(cr, col, 4 if ring == 0 else 0)
        ell(cr, cx, cy, rr*0.86, rr*0.8); fill(cr, col)

def lion_head(cr, P, t):
    c = LION
    _mane(cr, -14, -6, 128, t, P.get('fluff', 0))
    # ears
    for ex, col in ((-42, shade(c['fur'], 0.88)), (34, c['fur'])):
        ell(cr, ex, -62, 20, 18); fill_stroke(cr, col); ell(cr, ex, -60, 10, 9); fill(cr, shade(c['mane'], 1.1))
    # face
    cr.move_to(-70, -10); cr.curve_to(-72, -70, 66, -76, 70, -12); cr.curve_to(74, 40, 40, 72, 2, 72); cr.curve_to(-40, 72, -68, 40, -70, -10)
    cr.close_path(); fill_stroke(cr, c['fur'])
    P2 = dict(P); P2['lidcol'] = c['fur']
    for i, ex in enumerate((-26, 24)):
        eye(cr, ex, -16, 13, 15, c['iris'], P2, ir=10, side=i)
    br = P.get('brow', 0)
    for ex, fl in ((-26, -1), (24, 1)):
        cr.move_to(ex-14, -38-4*br); cr.curve_to(ex-6, -46-7*br, ex+6, -46-7*br, ex+14, -38-4*br+fl*2*min(0, br)); stroke(cr, OUT+(1,), 4.5)
    # muzzle
    for mx in (-14, 14):
        ell(cr, mx, 26, 22, 17); fill_stroke(cr, c['muzzle'], 3)
    for mx in (-22, -12, 12, 22):
        ell(cr, mx, 26+(mx % 3), 2.2, 2.2); fill(cr, shade(c['fur'], 0.6))
    cr.move_to(-13, 8); cr.curve_to(-13, -2, 13, -2, 13, 8); cr.curve_to(10, 16, 4, 18, 0, 20); cr.curve_to(-4, 18, -10, 16, -13, 8)
    cr.close_path(); fill_stroke(cr, c['nose'], 3)
    mo = P.get('mouth', 0); sm = P.get('smile', 0.6)
    if mo > 0.08:
        h = 6+mo*44
        ell(cr, 0, 44+h*0.3, 22+mo*6, h*0.55); fill_stroke(cr, hexc('#4A1E1E'), 3.5)
        ell(cr, 0, 44+h*0.55, 13, h*0.25); fill(cr, hexc('#D9727A'))
        for fx in (-10, 10):   # little friendly fangs
            cr.move_to(fx-3, 44+h*0.3-h*0.5+3); cr.line_to(fx, 44+h*0.3-h*0.5+8); cr.line_to(fx+3, 44+h*0.3-h*0.5+3); fill(cr, (1, 1, 1, 1))
    else:
        cr.move_to(0, 20); cr.line_to(0, 38); stroke(cr, OUT+(1,), 3.5)
        cr.move_to(-22, 40-sm*3); cr.curve_to(-14, 46+sm*6, -4, 44+sm*4, 0, 38); cr.curve_to(4, 44+sm*4, 14, 46+sm*6, 22, 40-sm*3)
        stroke(cr, OUT+(1,), 4)
    if P.get('blush'):
        for bx in (-46, 44): ell(cr, bx, 14, 12, 7); fill(cr, (0.95, 0.5, 0.45, 0.35*P['blush']))
    for side in (-1, 1):
        for k in (-1, 0, 1):
            cr.move_to(side*30, 30+k*6); cr.line_to(side*68, 24+k*12)
    stroke(cr, OUT+(0.45,), 1.8)

def lion(cr, P, t=0):
    """pose: 'stand' | 'lie'. walk phase 'walk'. head extras: hd (rot), hx/hy offsets."""
    c = LION
    cr.save(); cr.translate(P['x'], P['y']-P.get('air', 0)); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    if 'rot' in P: cr.rotate(P['rot'])
    pose = P.get('pose', 'stand'); dk = shade(c['fur'], 0.84)
    br = 1+0.02*osc(t, 0.3) if pose == 'lie' else 1
    tw = P.get('tail', 0)+0.12*osc(t, 0.6)
    def tail(bx, by):
        cr.save(); cr.translate(bx, by); cr.rotate(tw)
        cr.move_to(0, 0); cr.curve_to(-60, -10, -70, -90, -120, -110); stroke(cr, OUT+(1,), 16)
        cr.move_to(0, 0); cr.curve_to(-60, -10, -70, -90, -120, -110); stroke(cr, c['fur'], 9)
        ell(cr, -126, -114, 20, 15, 0.6); fill_stroke(cr, c['tuft'], 3.5); cr.restore()
    if pose == 'lie':
        tail(-170, -50)
        ell(cr, -60, -14, 58, 16); fill_stroke(cr, dk)             # far back foot
        capsule(cr, (120, -40), (262, -16), 40, dk)                  # far front paw
        ell(cr, -10, -72, 182, 70*br); fill_stroke(cr, c['fur'])     # body
        cr.save(); ell(cr, -10, -72, 182, 70*br); cr.clip(); ell(cr, 10, -18, 160, 30); fill(cr, c['belly']); cr.restore()
        ell(cr, -110, -78, 76, 64); fill_stroke(cr, c['fur'])        # haunch
        ell(cr, -40, -14, 64, 17); fill_stroke(cr, c['fur'])          # near back foot
        hu = P.get('headup', 0.0)
        hc = (lerp(250, 232, hu)+P.get('hx', 0), lerp(-96, -168, hu)+P.get('hy', 0))
        pl = P.get('paw', 0.0)   # near front paw lift 0..1
        pa = (120, -36); pb = (lerp(270, 250, pl)+P.get('pawx', 0), lerp(-14, -110, pl))
        cr.save(); cr.translate(*hc); cr.rotate(P.get('hd', 0)+lerp(0.16, 0, hu)); cr.scale(0.92, 0.92); lion_head(cr, P, t); cr.restore()
        capsule(cr, pa, pb, 44, c['fur'])
        cr.save(); cr.translate(*pb); cr.rotate(-0.35*pl); ell(cr, 6, 0, 30, 20); fill_stroke(cr, c['fur'])
        for k in (-8, 6, 20): cr.move_to(k, 8); cr.line_to(k, 18)
        stroke(cr, OUT+(1,), 3); cr.restore()
        P['_paw'] = pb; P['_head'] = hc
    else:
        ph = P.get('walk', 0.0); amp = P.get('wamp', 1.0 if 'walk' in P else 0.0)
        crouch = P.get('crouch', 0.0)
        by = -150+40*crouch+abs(math.sin(ph*2*math.pi))*4*amp
        def leg(x, phase, col, front):
            sw = math.sin(2*math.pi*(ph+phase))*0.32*amp + P.get('reach', 0)*(0.7 if front else -0.4)
            lift = max(0, math.cos(2*math.pi*(ph+phase)))*18*amp
            top = (x, by+20); L = -by-20-lift
            foot = (x+math.sin(sw)*L, top[1]+math.cos(sw)*L)
            capsule(cr, top, foot, 54 if front else 60, col)
            ell(cr, foot[0]+12, foot[1]-10, 34, 18); fill_stroke(cr, col)
            for k in (0, 12, 24): cr.move_to(foot[0]+k, foot[1]-2); cr.line_to(foot[0]+k, foot[1]-12)
            stroke(cr, OUT+(1,), 3)
        leg(-120, 0.5, dk, False); leg(110, 0.0, dk, True)
        tail(-185, by-10)
        ell(cr, 0, by, 180, 84); fill_stroke(cr, c['fur'])
        cr.save(); ell(cr, 0, by, 180, 84); cr.clip(); ell(cr, 20, by+62, 170, 34); fill(cr, c['belly']); cr.restore()
        ell(cr, -120, by-4, 74, 72); fill_stroke(cr, c['fur'])
        leg(-90, 0.0, c['fur'], False)
        hc = (210+P.get('hx', 0), by-90+P.get('hy', 0))
        leg(140, 0.5, c['fur'], True)
        cr.save(); cr.translate(*hc); cr.rotate(P.get('hd', 0)); lion_head(cr, P, t); cr.restore()
        P['_head'] = hc
    cr.restore()

def mouse(cr, P, t=0):
    c = MOUSE
    cr.save(); cr.translate(P['x'], P['y']-P.get('hop', 0)); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    if 'rot' in P: cr.rotate(P['rot'])
    run = P.get('run', None); dk = shade(c['fur'], 0.82)
    lean = P.get('lean', 0.0)
    # tail
    tw = math.sin(t*4)*6
    cr.move_to(-16, -22); cr.curve_to(-50, -10+tw, -70, -40-tw, -92, -26+tw); stroke(cr, OUT+(1,), 8)
    cr.move_to(-16, -22); cr.curve_to(-50, -10+tw, -70, -40-tw, -92, -26+tw); stroke(cr, c['tail'], 4)
    def foot(i, col):
        if run is not None:
            a = 2*math.pi*run+i*math.pi; fx = 4+math.sin(a)*14; fy = -max(0, math.cos(a))*8
        else:
            fx = 2+i*10; fy = 0
        capsule(cr, (fx-2, -22), (fx, fy-5), 11, col, 3); ell(cr, fx+7, fy-4, 11, 5.5); fill_stroke(cr, c['pink'], 3)
    foot(1, dk)
    arms = P.get('arms', [(0.4, -0.6), (0.3, -0.5)])
    sho = (8+lean*30, -56)
    def arm(i, col):
        a, b = arms[i]; e = add(sho, vecd(a, 17)); h = add(e, vecd(a+b, 15))
        capsule(cr, sho, e, 9, col, 3); capsule(cr, e, h, 8, col, 3); ell(cr, h[0], h[1], 5, 5); fill_stroke(cr, c['pink'], 2.5); return h
    arm(1, dk)
    cr.save(); cr.translate(0, -36); cr.rotate(lean)
    ell(cr, 0, 0, 22, 30); fill_stroke(cr, c['fur'])
    cr.save(); ell(cr, 0, 0, 22, 30); cr.clip(); ell(cr, 9, 6, 13, 22); fill(cr, c['belly']); cr.restore()
    cr.restore()
    foot(0, c['fur'])
    hx, hy = 14+lean*40, -86
    cr.save(); cr.translate(hx, hy); cr.rotate(P.get('hd', 0))
    for ex, ey, r, col in ((-14, -26, 18, dk), (10, -30, 20, c['fur'])):
        ell(cr, ex, ey, r, r); fill_stroke(cr, col, 3.5); ell(cr, ex+1, ey+1, r*0.6, r*0.6); fill(cr, c['pink'])
    ell(cr, 0, 0, 26, 22); fill_stroke(cr, c['fur'], 3.5)
    cr.move_to(14, -10); cr.curve_to(30, -10, 40, -6, 44, 0); cr.curve_to(40, 8, 28, 12, 12, 12); cr.close_path(); fill_stroke(cr, c['fur'], 3.5)
    ell(cr, 45, -1, 5.5, 5); fill_stroke(cr, c['pink'], 2.5)
    # headscarf
    cr.move_to(-24, -6); cr.curve_to(-22, -24, 6, -28, 22, -12); cr.line_to(16, -6); cr.curve_to(4, -16, -12, -14, -24, -6); cr.close_path()
    fill_stroke(cr, c['scarf'], 3)
    for dx, dy in ((-12, -14), (0, -18), (10, -14)): ell(cr, dx, dy, 2.2, 2.2); fill(cr, (1, 1, 1, 0.9))
    cr.move_to(-22, -8); cr.line_to(-34, -2+math.sin(t*6)*2); cr.line_to(-26, 2); cr.close_path(); fill_stroke(cr, c['scarf'], 2.5)
    P2 = dict(P); P2['lidcol'] = c['fur']
    eye(cr, 8, -4, 7, 8, (0.1, 0.07, 0.05, 1), P2, ir=6)
    mo = P.get('mouth', 0)
    if mo > 0.08:
        ell(cr, 30, 12, 6, 2+mo*7); fill_stroke(cr, hexc('#4A1E1E'), 2.5)
    else:
        cr.move_to(24, 10); cr.curve_to(28, 14+P.get('smile', 0.6)*3, 32, 14, 36, 10); stroke(cr, OUT+(1,), 2.8)
    if P.get('teeth'):
        cr.rectangle(29, 11, 4, 6); cr.rectangle(33, 11, 4, 6); fill_stroke(cr, (1, 1, 1, 1), 1.5)
    if P.get('blush'):
        ell(cr, 18, 8, 6, 3.5); fill(cr, (0.95, 0.5, 0.45, 0.5*P['blush']))
    for k in (-1, 0, 1):
        cr.move_to(40, 2+k*3); cr.line_to(58, -2+k*7)
    stroke(cr, OUT+(0.5,), 1.3)
    cr.restore()
    h = arm(0, c['fur'])
    if P.get('hold'): P['hold'](cr, h)
    cr.restore()

def olive(cr, x, y, s=1.0):
    ell(cr, x, y, 9*s, 12*s, 0.4); fill_stroke(cr, hexc('#3F3A5A'), 2.5*s); ell(cr, x-3*s, y-4*s, 2.5*s, 3.5*s, 0.4); fill(cr, (1, 1, 1, 0.35))

def butterfly(cr, x, y, t, s=1.0, col=hexc('#E8B53C')):
    fl = abs(math.sin(t*16))
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    for side in (-1, 1):
        cr.save(); cr.scale(side*(0.25+0.75*fl), 1)
        ell(cr, 14, -8, 16, 12, -0.4); fill_stroke(cr, col, 2.5); ell(cr, 11, 8, 10, 8, 0.4); fill_stroke(cr, shade(col, 0.85), 2.5)
        ell(cr, 16, -9, 4, 3); fill(cr, (1, 1, 1, 0.8)); cr.restore()
    ell(cr, 0, 0, 3, 12); fill(cr, OUT+(1,))
    cr.move_to(0, -10); cr.line_to(-6, -20); cr.move_to(0, -10); cr.line_to(6, -20); stroke(cr, OUT+(1,), 1.5)
    cr.restore()

# ---------------- olive-harvest net ----------------
NET = hexc('#3E8E5A')
def _sq2disk(u, v):
    a, b = 2*u-1, 2*v-1
    return a*math.sqrt(max(0, 1-b*b/2)), b*math.sqrt(max(0, 1-a*a/2))

def net_mesh(cr, mapfn, n=12, m=10, cut=None, alpha=1.0, seed=4):
    """mapfn(u,v)->(x,y). cut(x,y)->True removes that rope segment."""
    rnd = random.Random(seed)
    def seg(p, q):
        mid = ((p[0]+q[0])/2, (p[1]+q[1])/2)
        if cut and cut(*mid): return
        cr.move_to(*p); cr.line_to(*q)
    pts = [[mapfn(i/n, j/m) for j in range(m+1)] for i in range(n+1)]
    for pass_, (col, w) in enumerate(((OUT+(alpha,), 5.5), (NET[:3]+(alpha,), 3))):
        cr.new_path()
        for i in range(n+1):
            for j in range(m):
                seg(pts[i][j], pts[i][j+1])
        for j in range(m+1):
            for i in range(n):
                seg(pts[i][j], pts[i+1][j])
        stroke(cr, col, w)
    for i in range(n+1):
        for j in range(m+1):
            x, y = pts[i][j]
            if cut and cut(x, y): continue
            ell(cr, x, y, 3, 3); fill(cr, shade(NET, 0.7)[:3]+(alpha,))

def net_hang(x0, x1, ytop, h, sag=40):
    def f(u, v):
        return (lerp(x0, x1, u), ytop+v*h+sag*math.sin(math.pi*u)*(0.3+v))
    return f
def net_wrap(cx, cy, rx, ry, t, wob=0.0):
    def f(u, v):
        a, b = _sq2disk(u, v)
        w = 1+wob*0.06*math.sin(t*9+u*7+v*5)
        return (cx+rx*a*w, cy+ry*b*w)
    return f
def net_pile(cx, gy, rx):
    def f(u, v):
        a, b = 2*u-1, v
        return (cx+rx*a*(0.7+0.3*b), gy-8-38*b*(1-abs(a))-6*math.sin(u*20+v*9))
    return f
def net_blend(f0, f1, k):
    def f(u, v):
        p, q = f0(u, v), f1(u, v); return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))
    return f
