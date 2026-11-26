"""Episode 3 cast: Vorias the North Wind (cloud), Ilios the Sun, Mitsos the bear (red cloak).
Same style as chars.py: flat fills, umber outline, eye()/mouth() helpers, lip-sync via 'mouth'."""
from chars import *

BEAR = dict(fur=hexc('#8B5A3C'), dark=hexc('#6E4530'), muzzle=hexc('#E8CFA8'), nose=hexc('#3B2A20'), iris=hexc('#5A3A22'),
            cloak=hexc('#C8372D'), lining=hexc('#8E2A22'), clasp=hexc('#E3A946'), stick=hexc('#8A6A48'), basket=hexc('#C99A52'))
CLOUD = dict(body=hexc('#E6EEF5'), shade=hexc('#C2D0DE'), deep=hexc('#9FB2C6'), cheek=hexc('#E9A6B0'), iris=hexc('#4E7FB0'))
SUN = dict(face=hexc('#F7C843'), inner=hexc('#FBE38E'), ray=hexc('#F2A93B'), ray2=hexc('#F7D35A'), cheek=hexc('#F08A5D'), iris=hexc('#8A4A1E'))

def _puffs(cr, puffs, col, lw=4.0, shade_col=None):
    """merged cloud: outline every circle, then fill every circle on top (outline stays only on the silhouette)."""
    for x, y, r in puffs:
        ell(cr, x, y, r, r); cr.set_source_rgb(*OUT); cr.set_line_width(lw*2); cr.stroke()
    for x, y, r in puffs:
        ell(cr, x, y, r, r); fill(cr, col)
    if shade_col:
        for x, y, r in puffs:
            if y > 10: ell(cr, x+r*0.12, y+r*0.3, r*0.75, r*0.55); fill(cr, shade_col[:3]+(0.55,))

# ---------------- VORIAS (North Wind) ----------------
def _cloud_path(cr, puffs):
    cr.new_path()
    for x, y, r in puffs: cr.new_sub_path(); cr.arc(x, y, r, 0, 2*math.pi)

def wind_cloud(cr, P, t=0):
    """x,y,s,f (f=-1 faces left). puff 0..1 cheeks blown, mouth lip-sync, brow, look, eye, happy, sweat(tired)."""
    c = CLOUD
    cr.save(); cr.translate(P['x'], P['y']); sc = P.get('s', 1); cr.scale(sc*P.get('f', 1), sc)
    cr.rotate(P.get('rot', 0))
    pf = P.get('puff', 0.0); wob = P.get('wob', 1.0)
    bob = lambda k: 5*wob*math.sin(t*1.6+k)
    # trailing wisps behind
    for k in range(3):
        y0 = -30+k*40; ph = t*2+k
        cr.move_to(-250, y0); cr.curve_to(-300, y0-20+8*math.sin(ph), -340, y0+20, -380-10*k, y0+6*math.sin(ph+1))
        stroke(cr, (1, 1, 1, 0.75), 7-k)
    body = [(0, -10, 112), (-110, 0, 98), (-205, 20, 70), (-150, -70, 66), (-60, -88, 78), (40, -84, 70), (100, -20, 80),
            (-40, 60, 80), (-140, 60, 60)]
    body = [(x, y+bob(i), r) for i, (x, y, r) in enumerate(body)]
    beard = [(112, 96, 34), (80, 118, 38), (36, 116, 36), (-6, 102, 34), (128, 128, 24), (100, 150, 22)]
    beard = [(x, y+bob(i+3)*0.6, r) for i, (x, y, r) in enumerate(beard)]
    allp = body+beard
    for x, y, r in allp:
        ell(cr, x, y, r, r); cr.set_source_rgb(*OUT); cr.set_line_width(9); cr.stroke()
    for x, y, r in allp:
        ell(cr, x, y, r, r); fill(cr, c['body'])
    cr.save(); _cloud_path(cr, allp); cr.clip()
    ell(cr, -40, 150, 300, 90); fill(cr, c['shade'][:3]+(0.6,))
    ell(cr, -60, -120, 160, 40); fill(cr, (1, 1, 1, 0.5))
    cr.restore()
    # face (front = +x)
    P2 = dict(P); P2['lidcol'] = c['body']; P2.setdefault('look', (0.6, 0.2))
    E = ((48, -30), (112, -26))
    for i, (ex, ey) in enumerate(E):
        eye(cr, ex, ey, 22, 26, c['iris'], P2, ir=15, side=i)
    br = P.get('brow', 0)
    for ex, ey in E:   # bushy cloud brows
        for k in range(3):
            ell(cr, ex-16+k*16, ey-36-7*br-(3 if k == 1 else 0)+(4*(k-1)*min(0, br)), 13, 9); fill_stroke(cr, (1, 1, 1, 1), 2.5)
    cr_r = 22+24*pf
    for cx, cy in ((40, 26), (132, 30)):
        ell(cr, cx, cy, cr_r, cr_r*0.9); fill_stroke(cr, c['body'], 3)
        ell(cr, cx, cy+4, cr_r*0.62, cr_r*0.42); fill(cr, c['cheek'][:3]+(0.6+0.3*pf,))
    mo = P.get('mouth', 0); mx, my = 88, 66
    if pf > 0.35:   # blowing: round "o"
        ell(cr, mx+4, my, 10+5*pf, 12+5*pf); fill_stroke(cr, hexc('#4A1E1E'), 3.5)
    else:
        mouth(cr, mx, my-6, 40, mo, P.get('smile', 0.6))
    for k, (x, y) in enumerate(((66, 44), (108, 46))):    # moustache puffs
        ell(cr, x, y, 24, 14, (-0.25 if k == 0 else 0.25)); fill_stroke(cr, (1, 1, 1, 1), 3)
    ell(cr, 88, 22, 16, 13); fill_stroke(cr, c['shade'], 3)
    if P.get('sweat'):
        for k, (dx, dy) in enumerate(((10, -80), (150, -70))):
            ph = (t*1.2+k*0.5) % 1
            cr.save(); cr.translate(dx, dy+ph*30); cr.move_to(0, -10); cr.curve_to(8, 0, 6, 8, 0, 8); cr.curve_to(-6, 8, -8, 0, 0, -10)
            fill_stroke(cr, (0.75, 0.88, 1, 1-ph), 2.5); cr.restore()
    P['_mouth'] = (mx, my)
    cr.restore()

def cloud_mouth(P):
    """world position of Vorias' mouth (for gusts)."""
    s = P.get('s', 1); f = P.get('f', 1)
    return (P['x']+f*s*92, P['y']+s*66)

def gust(cr, x0, y0, x1, y1, k, t, seed=1, n=9, col=(1, 1, 1), spread=90, lw=6):
    """animated wind streaks travelling from (x0,y0) toward (x1,y1); k = strength 0..1."""
    if k <= 0.01: return
    r = random.Random(seed); dx, dy = x1-x0, y1-y0; L = math.hypot(dx, dy); ux, uy = dx/L, dy/L; nx, ny = -uy, ux
    for i in range(n):
        off = r.uniform(-spread, spread)*(0.6+0.8*k); sp = r.uniform(0.5, 0.8); ph = (t*sp*(0.7+0.9*k)+r.random()) % 1
        seg = 0.22+0.12*k; a0, a1 = ph, min(1, ph+seg)
        pts = []
        for j in range(9):
            u = lerp(a0, a1, j/8); w = math.sin(u*9+i+t*3)*16*(1+u)
            pts.append((x0+dx*u+nx*(off*(0.4+u)+w), y0+dy*u+ny*(off*(0.4+u)+w)))
        cr.move_to(*pts[0])
        for p in pts[1:]: cr.line_to(*p)
        a = k*math.sin(math.pi*ph)
        stroke(cr, col+(0.85*a,), lw*(0.6+0.6*k))
        if i % 3 == 0:   # curl at the head of some streaks
            hx, hy = pts[-1]; cr.new_path(); cr.arc(hx, hy, 14+10*k, 0, math.pi*1.4); stroke(cr, col+(0.7*a,), lw*0.6)

def blown_leaves(cr, t, k, box, seed=5, n=26, dirx=-1):
    if k <= 0.02: return
    r = random.Random(seed); x0, y0, x1, y1 = box; w = x1-x0
    for i in range(n):
        sp = r.uniform(380, 700)*k+60; ph = r.random()*w
        x = x1-((t*sp+ph) % w) if dirx < 0 else x0+((t*sp+ph) % w)
        y = r.uniform(y0, y1)+math.sin(t*3+i)*40
        a = min(1, k*1.6)
        col = [(0.48, 0.56, 0.3), (0.78, 0.56, 0.22), (0.66, 0.42, 0.2)][i % 3]
        ell(cr, x, y, 11, 5, t*6+i); cr.set_source_rgba(*col, a); cr.fill_preserve(); cr.set_source_rgba(*OUT, a*0.8); cr.set_line_width(1.5); cr.stroke()

# ---------------- ILIOS (the Sun) ----------------
def sun(cr, P, t=0):
    """x,y,s; shine 0..1 (glow, longer rays); mouth, look, eye, happy, wink, smile."""
    c = SUN
    cr.save(); cr.translate(P['x'], P['y']); sc = P.get('s', 1); cr.scale(sc, sc)
    sh = P.get('shine', 0.3)
    glow(cr, 0, 0, 260+140*sh, (1, 0.85, 0.4), 0.25+0.35*sh)
    rot = t*0.12+P.get('spin', 0)
    for k in range(16):
        a = rot+k*2*math.pi/16; L = (62 if k % 2 == 0 else 42)*(1+0.35*sh)+5*math.sin(t*3+k)
        cr.save(); cr.rotate(a)
        cr.move_to(-18, -112); cr.line_to(0, -112-L); cr.line_to(18, -112); cr.close_path()
        fill_stroke(cr, c['ray'] if k % 2 == 0 else c['ray2'], 3.5); cr.restore()
    ell(cr, 0, 0, 120, 120); fill_stroke(cr, c['face'], 5)
    ell(cr, -14, -16, 92, 88); fill(cr, c['inner'][:3]+(0.7,))
    P2 = dict(P); P2['lidcol'] = c['face']; P2.setdefault('look', (0, 0.2))
    for i, ex in enumerate((-38, 38)):
        P3 = dict(P2)
        if i == 1 and 'wink' in P: P3['eye'] = P['wink']
        eye(cr, ex, -18, 18, 22, c['iris'], P3, ir=14, side=i)
    br = P.get('brow', 0)
    for ex in (-38, 38):
        cr.move_to(ex-18, -52-5*br); cr.curve_to(ex-6, -60-7*br, ex+6, -60-7*br, ex+18, -52-5*br); stroke(cr, hexc('#C9782E')[:3]+(1,), 5)
    for bx in (-70, 70): ell(cr, bx, 22, 20, 12); fill(cr, c['cheek'][:3]+(0.55,))
    mouth(cr, 0, 36, 52, P.get('mouth', 0), P.get('smile', 0.9))
    cr.restore()

def sky_cloud(cr, x, y, s, a=1.0, seed=3):
    """plain cloud (no face) for covering the sun."""
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.push_group()
    _puffs(cr, [(0, 0, 90), (-100, 20, 70), (100, 25, 72), (-40, -50, 70), (50, -40, 66), (-170, 40, 46), (170, 45, 48)], CLOUD['body'], 4, CLOUD['shade'])
    cr.pop_group_to_source(); cr.paint_with_alpha(a)
    cr.restore()

# ---------------- MITSOS the bear ----------------
def folded_cloak(cr, x, y, s=1.0):
    c = BEAR
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    rrect(cr, -70, -34, 140, 34, 14); fill_stroke(cr, c['cloak'], 4)
    cr.move_to(-62, -20); cr.line_to(62, -20); stroke(cr, c['lining'][:3]+(1,), 3)
    rrect(cr, -60, -56, 120, 26, 12); fill_stroke(cr, c['cloak'], 4)
    ell(cr, 40, -44, 8, 8); fill_stroke(cr, c['clasp'], 2.5)
    cr.restore()

def basket(cr, x, y, s=1.0):
    c = BEAR
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.new_path(); cr.arc(0, -6, 30, math.pi, 2*math.pi); stroke(cr, OUT+(1,), 8); cr.new_path(); cr.arc(0, -6, 30, math.pi, 2*math.pi); stroke(cr, c['basket'], 4)
    cr.move_to(-34, -6); cr.line_to(-26, 30); cr.line_to(26, 30); cr.line_to(34, -6); cr.close_path(); fill_stroke(cr, c['basket'], 3.5)
    for k in range(3): cr.move_to(-30+k*2, 4+k*9); cr.line_to(30-k*2, 4+k*9)
    stroke(cr, shade(c['basket'], 0.75), 2.5)
    for k, col in enumerate(('#6B3B5E', '#E3A946', '#6B3B5E')): ell(cr, -16+k*16, -10, 10, 9); fill_stroke(cr, hexc(col), 2.5)
    cr.restore()

def bear(cr, P, t=0):
    """Mitsos. facing +x (f=-1 flips). keys: walk (phase), wamp, wind 0..1 (cloak streams back), hug 0..1 (wraps cloak),
    cloak 'on'|'off'|'carry', sit (bool), fan 0..1 (near paw fans face), sweat 0..1, warm 0..1 (rosy), lean, hd, mouth, look, eye, happy."""
    c = BEAR
    cr.save(); cr.translate(P['x'], P['y']-P.get('hop', 0)); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    sit = P.get('sit', False); cl = P.get('cloak', 'on'); wind = P.get('wind', 0.0); hug = P.get('hug', 0.0)
    ph = P.get('walk', 0.0); amp = P.get('wamp', 1.0 if 'walk' in P else 0.0)
    lean = P.get('lean', 0.0) + 0.12*wind
    shiver = P.get('shiver', 0.0)*math.sin(t*45)*2.5
    bob = abs(math.sin(ph*2*math.pi))*6*amp
    hip = (0, -120+bob) if not sit else (0, -34)
    def up(p):   # rotate upper-body point about the hip by lean
        dx, dy = p[0]-hip[0], p[1]-hip[1]; ca, sa = math.cos(lean), math.sin(lean)
        return (hip[0]+dx*ca-dy*sa+shiver, hip[1]+dx*sa+dy*ca)
    sho_far, sho_near = up((-26, -270+120+hip[1]+0)), up((30, -262+120+hip[1]))
    neck = up((14, -290+120+hip[1]))
    # ---- cloak back drape ----
    flutter = lambda u, k: math.sin(t*(9+5*wind)+u*7+k)*(6+22*wind)
    if cl == 'on':
        if hug > 0.01: wb = wind*(1-0.75*hug)
        else: wb = wind
        top = up((-46, -296+120+hip[1])); back_hem = (-70-200*wb, hip[1]+40-150*wb) if not sit else (-80, 0)
        front_hem = (lerp(52, -30, wb*(1-hug)), hip[1]+46-30*wb*(1-hug)) if not sit else (60, -6)
        cr.move_to(*neck); cr.curve_to(top[0]-20, top[1]-6, top[0]-50-40*wb, top[1]+60, back_hem[0], back_hem[1])
        for j in range(1, 7):
            u = j/6; x = lerp(back_hem[0], front_hem[0], u); y = lerp(back_hem[1], front_hem[1], u)+flutter(u, 0)*(1-u*0.6)
            cr.line_to(x, y)
        cr.curve_to(front_hem[0]+10, front_hem[1]-80, neck[0]+40, neck[1]+40, neck[0], neck[1]); cr.close_path()
        fill_stroke(cr, c['lining'])
    # ---- legs ----
    def leg(x, phase, col):
        if sit:
            a = hip[0]+x*0.5, hip[1]+10; b = (a[0]+96, a[1]+6)
            capsule(cr, a, b, 50, col); ell(cr, b[0]+14, b[1]-8, 22, 28); fill_stroke(cr, col)
            ell(cr, b[0]+18, b[1]-8, 11, 14); fill(cr, c['muzzle']); return
        sw = math.sin(2*math.pi*(ph+phase))*0.38*amp
        lift = max(0, math.cos(2*math.pi*(ph+phase)))*16*amp
        top = (hip[0]+x, hip[1]+10); Lg = -top[1]-lift
        foot = (top[0]+math.sin(sw)*Lg, top[1]+math.cos(sw)*Lg)
        capsule(cr, top, foot, 64, col); ell(cr, foot[0]+14, foot[1]-10, 36, 17); fill_stroke(cr, col)
    leg(-14, 0.5, c['dark'])
    # ---- far arm ----
    def arm_pts(shp, a1, a2, l1=58, l2=54):
        e = add(shp, vecd(a1+lean, l1)); h = add(e, vecd(a1+a2+lean, l2)); return e, h
    arms = P.get('arms', [(0.25, -0.35), (0.1, -0.25)])
    if hug > 0.5 and cl == 'on':
        arms = [(lerp(arms[0][0], 1.5, hug), lerp(arms[0][1], 1.2, hug)), (lerp(arms[1][0], 1.25, hug), lerp(arms[1][1], 1.35, hug))]
    e, h = arm_pts(sho_far, *arms[1])
    capsule(cr, sho_far, e, 34, c['dark']); capsule(cr, e, h, 30, c['dark']); ell(cr, h[0], h[1], 17, 15); fill_stroke(cr, c['dark'])
    if P.get('basket') and (P.get('fan', 0.0) > 0.3 or P['basket'] == 'far'):   # basket swaps to the far paw while the near paw fans
        basket(cr, h[0]-4, h[1]+28, 0.9)
    stick_h = None
    # ---- body ----
    bc = up((4, -192+120+hip[1]))
    ell(cr, bc[0], bc[1], 80, 106, lean); fill_stroke(cr, c['fur'])
    cr.save(); ell(cr, bc[0], bc[1], 80, 106, lean); cr.clip(); ell(cr, bc[0]+30, bc[1]+16, 46, 70, lean); fill(cr, c['muzzle']); cr.restore()
    leg(18, 0.0, c['fur'])
    # ---- cloak front (closed / hugging) or shoulder mantle ----
    if cl == 'on':
        wrap = max(hug, P.get('closed', 0.0))
        if wrap > 0.05:
            fh = up((40, -40+hip[1]+120-120))
            fh = (bc[0]+lerp(30, 60, wrap), bc[1]+92)
            cr.move_to(*neck); cr.curve_to(neck[0]+70*wrap+10, neck[1]+20, fh[0]+30, fh[1]-80, fh[0], fh[1])
            cr.line_to(bc[0]-70, bc[1]+96+flutter(0.3, 2)*0.3); cr.curve_to(bc[0]-82, bc[1], neck[0]-60, neck[1]+10, neck[0], neck[1]); cr.close_path()
            cr.save(); cr.push_group(); fill_stroke(cr, c['cloak']); cr.pop_group_to_source(); cr.paint_with_alpha(min(1, wrap*1.6)); cr.restore()
            cr.move_to(neck[0]+20, neck[1]+30); cr.curve_to(neck[0]+30, neck[1]+80, fh[0]-10, fh[1]-60, fh[0]-6, fh[1]-6)
            stroke(cr, c['lining'][:3]+(0.7*min(1, wrap*1.6),), 3)
        # mantle over shoulders
        m0 = up((-50, -300+120+hip[1])); m1 = up((60, -284+120+hip[1])); m2 = up((56, -236+120+hip[1])); m3 = up((-56, -232+120+hip[1]))
        cr.move_to(*m0); cr.curve_to(m0[0]+30, m0[1]-22, m1[0]-30, m1[1]-22, *m1); cr.line_to(m2[0]+4, m2[1])
        cr.curve_to(m2[0]-30, m2[1]+16+flutter(0.5, 1)*0.3, m3[0]+30, m3[1]+16, *m3); cr.close_path(); fill_stroke(cr, c['cloak'])
        ell(cr, neck[0]+22, neck[1]+8, 10, 10); fill_stroke(cr, c['clasp'], 3)
    # ---- head ----
    hc = up((22, -352+120+hip[1]+P.get('hy', 0)))
    cr.save(); cr.translate(*hc); cr.rotate(lean*0.5+P.get('hd', 0))
    for ex, col in ((-40, c['dark']), (26, c['fur'])):
        ell(cr, ex, -50, 22, 21); fill_stroke(cr, col); ell(cr, ex+1, -48, 11, 10); fill(cr, c['muzzle'])
    ell(cr, 0, 0, 64, 58); fill_stroke(cr, c['fur'])
    ell(cr, 40, 16, 34, 24); fill_stroke(cr, c['muzzle'], 3.5)
    ell(cr, 64, 6, 12, 9); fill(cr, c['nose']); ell(cr, 61, 3, 4, 2.5); fill(cr, (1, 1, 1, 0.5))
    P2 = dict(P); P2['lidcol'] = c['fur']; P2.setdefault('look', (0.4, 0))
    for i, (ex, ey, rr) in enumerate(((4, -14, 11), (34, -16, 12))):
        eye(cr, ex, ey, rr, rr+2, c['iris'], P2, ir=rr*0.75, side=i)
    br = P.get('brow', 0)
    for ex in (4, 34):
        cr.move_to(ex-11, -32-4*br); cr.curve_to(ex-4, -38-5*br, ex+4, -38-5*br, ex+11, -32-4*br); stroke(cr, OUT+(1,), 4)
    wm = P.get('warm', 0)
    if wm > 0:
        for bx in (-14, 52): ell(cr, bx, 12, 11, 7); fill(cr, (0.95, 0.45, 0.4, 0.5*wm))
    mo = P.get('mouth', 0)
    if P.get('chatter'): mo = 0.15+0.12*abs(math.sin(t*30))
    mouth(cr, 42, 28, 24, mo, P.get('smile', 0.7), teeth=P.get('chatter', False))
    cr.restore()
    # sweat drops
    sw_ = P.get('sweat', 0)
    if sw_ > 0.05:
        for k, (dx, dy) in enumerate(((-56, -40), (60, -60), (-30, -66))):
            pp = (t*0.9+k*0.37) % 1
            x, y = hc[0]+dx, hc[1]+dy+pp*40
            cr.save(); cr.translate(x, y); cr.move_to(0, -10); cr.curve_to(7, 0, 6, 8, 0, 8); cr.curve_to(-6, 8, -7, 0, 0, -10)
            fill_stroke(cr, (0.7, 0.86, 1, sw_*(1-pp)), 2.5); cr.restore()
    # ---- near arm (on top) ----
    a0, a1 = arms[0]
    fan = P.get('fan', 0.0)
    if fan > 0.01:
        a0, a1 = lerp(a0, 1.9, fan), lerp(a1, 1.05+0.35*math.sin(t*14), fan)
    e, h = arm_pts(sho_near, a0, a1)
    capsule(cr, sho_near, e, 36, c['fur']); capsule(cr, e, h, 32, c['fur']); ell(cr, h[0], h[1], 18, 16); fill_stroke(cr, c['fur'])
    if cl == 'carry':   # folded cloak over the forearm
        cr.move_to(e[0]-10, e[1]-6); cr.curve_to(e[0]+10, e[1]+40, h[0]-30, h[1]+70, h[0]-20, h[1]+90); cr.line_to(h[0]+30, h[1]+84)
        cr.curve_to(h[0]+30, h[1]+40, h[0]+20, h[1]+10, h[0]+10, h[1]-14); cr.close_path(); fill_stroke(cr, c['cloak'])
    if P.get('stick', False) and not sit:
        cr.move_to(h[0]+4, h[1]-60); cr.line_to(h[0]+4+math.sin(lean)*20, h[1]+(0-h[1])+0); stroke(cr, OUT+(1,), 11)
        cr.move_to(h[0]+4, h[1]-60); cr.line_to(h[0]+4+math.sin(lean)*20, h[1]+(0-h[1])+0); stroke(cr, c['stick'], 6)
        ell(cr, h[0], h[1], 18, 16); fill_stroke(cr, c['fur'])
    if P.get('basket') and fan <= 0.3 and P['basket'] != 'far':
        bx, by = P['basket'] if isinstance(P['basket'], tuple) else (h[0]-6, h[1]+30)
        basket(cr, bx, by, 0.9)
    sw = P.get('swish', 0.0)
    if sw > 0.02:   # cartoon swish while the cloak comes off
        cc = up((10, -250+120+hip[1]))
        for k in range(3):
            r = 120+k*26; a0 = -1.2+sw*2.6+k*0.3
            cr.new_path(); cr.arc(cc[0], cc[1], r, a0, a0+1.6); stroke(cr, (1, 1, 1, 0.8*math.sin(math.pi*sw)), 6-k*1.5)
    cr.restore()
