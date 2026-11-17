from core import *

def vecd(a, l): return (math.sin(a)*l, math.cos(a)*l)   # 0 = down, + toward +x

# ---------------- palettes ----------------
HARE = dict(fur=hexc('#B9824A'), cream=hexc('#F1E1C2'), tip=hexc('#2B211B'), pink=hexc('#E7A9A0'),
            iris=hexc('#E3A33A'), sash=hexc('#B8432F'), bell=hexc('#C9963B'))
TORT = dict(shell=hexc('#9C8A3E'), plate=hexc('#B5A24E'), edge=hexc('#4E4223'), skin=hexc('#A7A77A'),
            belly=hexc('#E8DDB4'), eye=hexc('#3E2C1E'), scarf=hexc('#3E7CB1'), straw=hexc('#D9B86A'), fig=hexc('#6B3B5E'))
FOX = dict(fur=hexc('#D9692C'), white=hexc('#F6F1E7'), dark=hexc('#3B2A20'), eye=hexc('#7FAE5B'),
           cloak=hexc('#E3A946'), pin=hexc('#B07A2A'))
OWL = dict(body=hexc('#7D6A55'), spot=hexc('#EFE6D6'), brow=hexc('#EDE3C8'), eye=hexc('#E8C33C'), beak=hexc('#C9A86A'),
           leaf=hexc('#6E8B3D'))

# ---------------- shared face bits ----------------
def eye(cr, x, y, rx, ry, iris, P, ir=None, side=0):
    op = P.get('eye', 1.0)
    if side == 1 and 'eye2' in P: op = P['eye2']
    lid = P.get('lidcol', (0.6, 0.5, 0.4, 1))
    if P.get('happy') and op > 0.5:
        cr.new_path(); cr.arc(x, y+ry*0.5, rx*0.9, math.pi*1.15, math.pi*1.85); stroke(cr, OUT+(1,), 4.5); return
    sc = P.get('wide', 1.0); rx *= sc; ry *= sc
    ell(cr, x, y, rx, ry); cr.set_source_rgb(1, 1, 1); cr.fill_preserve(); cr.save(); cr.clip()
    px, py = P.get('look', (0, 0)); ir = ir or rx*0.72
    ell(cr, x+px*rx*0.35, y+py*ry*0.3, ir, ir); fill(cr, iris)
    ell(cr, x+px*rx*0.4, y+py*ry*0.32, ir*0.55, ir*0.55); fill(cr, (0.08, 0.06, 0.05, 1))
    ell(cr, x+px*rx*0.4-ir*0.3, y+py*ry*0.32-ir*0.35, ir*0.25, ir*0.25); fill(cr, (1, 1, 1, 1))
    if op < 1:
        cr.rectangle(x-rx-2, y-ry-2, rx*2+4, (ry*2+4)*(1-op)); fill(cr, lid)
        cr.move_to(x-rx, y-ry+(ry*2)*(1-op)); cr.line_to(x+rx, y-ry+(ry*2)*(1-op)); stroke(cr, OUT+(1,), 3.5)
    cr.restore(); ell(cr, x, y, rx, ry); stroke(cr, OUT+(1,), 3.5)

def brow(cr, x, y, w, b, flip=1):
    # b: -1 angry/worried down at inner, +1 raised
    cr.move_to(x-w/2, y-4*b*flip*0); cr.curve_to(x-w/4, y-6-6*b, x+w/4, y-6-6*b, x+w/2, y+2*b*flip)
    stroke(cr, OUT+(1,), 4)

def mouth(cr, x, y, w, open_, smile, teeth=False, tongue=hexc('#D9727A')):
    if open_ > 0.08:
        h = 4+open_*w*0.9
        ell(cr, x, y+h*0.35, w*0.55, h*0.6); fill_stroke(cr, hexc('#4A1E1E'), 3.5)
        ell(cr, x, y+h*0.6, w*0.35, h*0.28); fill(cr, tongue)
    else:
        cr.move_to(x-w/2, y-smile*3); cr.curve_to(x-w/5, y+smile*8, x+w/5, y+smile*8, x+w/2, y-smile*3)
        stroke(cr, OUT+(1,), 4)
    if teeth:
        cr.rectangle(x-w*0.22, y-2, w*0.2, w*0.25); cr.rectangle(x+0.02*w, y-2, w*0.2, w*0.25); fill_stroke(cr, (1, 1, 1, 1), 2.5)

# ---------------- HARE (Lagos) ----------------
def hare_head(cr, P, t):
    c = HARE
    ears = P.get('ears', (-0.25, -0.05)); flop = P.get('flop', (0, 0))
    for i, (bx, by) in enumerate(((-16, -34), (0, -40))):
        a = ears[i]; fl = flop[i]
        cr.save(); cr.translate(bx, by); cr.rotate(a)
        L = 112*(1-0.35*fl)
        if fl > 0: cr.rotate(fl*1.6)
        ell(cr, 0, -L/2, 16, L/2); col = shade(c['fur'], 0.85) if i == 0 else c['fur']
        cr.set_source_rgba(*col); cr.fill_preserve(); cr.save(); cr.clip()
        ell(cr, 2, -L/2+6, 8, L/2-14); fill(cr, c['pink'] if i == 1 else shade(c['pink'], 0.8))
        ell(cr, 0, -L+8, 16, 18); fill(cr, c['tip'])
        cr.restore(); ell(cr, 0, -L/2, 16, L/2); stroke(cr, OUT+(1,), 4)
        cr.restore()
    # head
    ell(cr, 0, 0, 58, 49); fill_stroke(cr, c['fur'])
    for k in range(3):
        cr.move_to(-48, 8+k*10); cr.line_to(-66, 12+k*12); cr.line_to(-46, 18+k*10)
    fill(cr, c['fur']);
    ell(cr, 30, 16, 30, 23); fill(cr, c['cream'])
    P2 = dict(P); P2['lidcol'] = c['fur']
    eye(cr, 18, -8, 15, 19, c['iris'], P2)
    brow(cr, 18, -34, 26, P.get('brow', 0))
    ell(cr, 56, 2, 9, 6.5); fill_stroke(cr, c['pink'], 3)
    mouth(cr, 49, 20, 20, P.get('mouth', 0), P.get('smile', 0.6), P.get('teeth', False))
    for k in (-1, 0, 1):
        cr.move_to(42, 12+k*4); cr.line_to(74, 6+k*9)
    stroke(cr, OUT+(0.5,), 1.8)

def hare(cr, P, t=0):
    c = HARE
    cr.save(); cr.translate(P['x'], P['y']); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    if 'rot' in P: cr.rotate(P['rot'])
    if P.get('squash'): sq = P['squash']; cr.scale(1+sq*0.25, 1-sq*0.25)
    L1, L2, FL = 62, 66, 74
    legs = P.get('legs', [(0.15, -0.3), (0.05, -0.25)])
    lean = P.get('lean', 0.0)
    def leg_pts(th, sh):
        k = vecd(th, L1); a = add(k, vecd(th+sh, L2)); return k, a
    low = max(leg_pts(*l)[1][1] for l in legs) + 8
    hip = (0, -(low) - P.get('air', 0))
    neck = add(hip, vec(lean, 112)); sho = add(hip, vec(lean, 92))
    arms = P.get('arms', [(0.3, -0.5), (0.15, -0.4)])
    def arm(i, col, w=18):
        sa, ea = arms[i]; e = add(sho, vecd(lean+sa, 44)); h = add(e, vecd(lean+sa+ea, 42))
        capsule(cr, sho, e, w+5, col); capsule(cr, e, h, w+3, col)
        ell(cr, h[0], h[1], 10, 9); fill_stroke(cr, col)
        return h
    def leg(i, col):
        th, sh = legs[i]; k, a = leg_pts(th, sh); kk = add(hip, k); aa = add(hip, a)
        ell(cr, hip[0]+k[0]*0.45, hip[1]+k[1]*0.45, 34, 50, -th); fill_stroke(cr, col)
        capsule(cr, kk, aa, 22, col)
        fa = P.get('foot', [0, 0])[i] if 'foot' in P else (0 if aa[1] > -12 else (th+sh)*0.6)
        cr.save(); cr.translate(*aa); cr.rotate(fa); ell(cr, FL*0.42, 2, FL*0.55, 13); fill_stroke(cr, col); cr.restore()
    dark = shade(c['fur'], 0.82)
    arm(1, dark); leg(1, dark)
    # tail
    tp = add(hip, vec(lean-1.9, 40)); ell(cr, tp[0]-6, tp[1], 16, 14); fill_stroke(cr, c['cream'])
    # torso
    mid = add(hip, vec(lean, 56))
    ell(cr, mid[0], mid[1], 46, 70, lean); fill_stroke(cr, c['fur'])
    cr.save(); ell(cr, mid[0], mid[1], 46, 70, lean); cr.clip()
    ell(cr, mid[0]+math.cos(lean)*26, mid[1]+math.sin(lean)*26, 30, 60, lean); fill(cr, c['cream']); cr.restore()
    # sash
    sp = add(hip, vec(lean, 30)); cr.save(); cr.translate(*sp); cr.rotate(lean)
    cr.rectangle(-47, -10, 94, 20); cr.save(); ell(cr, 0, -26, 46, 70); cr.clip(); fill_stroke(cr, c['sash'], 3.5); cr.restore()
    fl = P.get('flutter', 0)
    for k, off in ((0, 0), (1, 0.8)):
        w = math.sin(t*14+off)*0.25*(0.3+fl)
        cr.move_to(-40, 2); cr.curve_to(-60, 8+off*6, -75-fl*20, 14+w*30, -90-fl*35, 18+off*14+w*40)
        cr.line_to(-84-fl*35, 30+off*14+w*40); cr.curve_to(-70, 24, -56, 18, -40, 10); cr.close_path()
        fill_stroke(cr, c['sash'], 3)
    bx, by = -90-fl*35, 24+14+math.sin(t*14+0.8)*0.25*(0.3+fl)*40
    ell(cr, bx, by, 6, 6); fill_stroke(cr, c['bell'], 2.5)
    ell(cr, -42, 0, 10, 12); fill_stroke(cr, shade(c['sash'], 0.85), 3)
    cr.restore()
    leg(0, c['fur'])
    # head
    hc = add(neck, vec(lean*0.45+P.get('hd', 0), 52))
    cr.save(); cr.translate(*hc); cr.rotate(lean*0.4+P.get('hd', 0)); hare_head(cr, P, t); cr.restore()
    hp = arm(0, c['fur'])
    if P.get('hold'):  # draw held object in near paw
        P['hold'](cr, hp)
    cr.restore()

# ---------------- TORTOISE (Chelona) ----------------
def tortoise(cr, P, t=0):
    c = TORT
    cr.save(); cr.translate(P['x'], P['y']); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    ph = P.get('walk', 0.0); amp = P.get('wamp', 1.0 if 'walk' in P else 0)
    bob = abs(math.sin(ph*math.pi*2))*4*amp
    def legd(x, phase, col):
        lift = max(0, math.sin(2*math.pi*(ph+phase)))*16*amp
        sw = math.cos(2*math.pi*(ph+phase))*14*amp
        cr.save(); cr.translate(x+sw, -lift)
        rrect(cr, -18, -48, 36, 48, 14); fill_stroke(cr, col)
        for k in (-10, 0, 10):
            ell(cr, k, -2, 4, 3); fill(cr, hexc('#E8DDB4'))
        cr.restore()
    dk = shade(c['skin'], 0.8)
    legd(78, 0.5, dk); legd(-50, 0.0, dk)
    cr.translate(0, -bob)
    # tail
    cr.move_to(-112, -44); cr.line_to(-134, -38); cr.line_to(-110, -32); fill_stroke(cr, c['skin'], 3)
    # neck + head
    ext = P.get('neck', 0.4); ha = P.get('ha', 0)
    nb = (92, -58); hc = (112+ext*48, -86-ext*10+P.get('hdy', 0))
    capsule(cr, nb, hc, 40, c['skin'])
    # scarf
    sx = nb[0]+(hc[0]-nb[0])*0.35; sy = nb[1]+(hc[1]-nb[1])*0.35
    cr.save(); cr.translate(sx, sy); cr.rotate(math.atan2(hc[1]-nb[1], hc[0]-nb[0])+math.pi/2)
    rrect(cr, -26, -13, 52, 26, 10); fill_stroke(cr, c['scarf'], 3.5)
    cr.set_source_rgb(1, 1, 1); cr.set_line_width(2.5)
    for k in range(-20, 22, 9):
        cr.move_to(k, 8); cr.line_to(k, 4); cr.line_to(k+5, 4); cr.stroke()
    sw = math.sin(t*5)*3*P.get('wind', 1)
    cr.move_to(4, 10); cr.curve_to(10, 30, 2+sw, 44, 8+sw, 54); cr.line_to(20+sw, 50); cr.curve_to(16, 36, 18, 24, 14, 10); cr.close_path()
    fill_stroke(cr, c['scarf'], 3)
    cr.restore()
    # head
    cr.save(); cr.translate(*hc); cr.rotate(ha)
    ell(cr, 6, 0, 38, 30); fill_stroke(cr, c['skin'])
    ell(cr, 30, 10, 16, 12); fill(cr, mix(c['skin'], c['belly'], 0.5))
    P2 = dict(P); P2['lidcol'] = c['skin']
    eye(cr, 14, -8, 10, 12, c['eye'], P2, ir=8.5)
    brow(cr, 14, -24, 20, P.get('brow', 0))
    mouth(cr, 30, 12, 20, P.get('mouth', 0), P.get('smile', 0.5))
    if P.get('chew'):
        ell(cr, -6, 12, 9, 7+3*math.sin(t*12)); fill(cr, mix(c['skin'], (0.9, 0.5, 0.5, 1), 0.35))
    if P.get('sweat', 0) > 0:
        sy2 = -20+P['sweat']*40
        cr.move_to(-14, sy2-10); cr.curve_to(-8, sy2-2, -6, sy2+6, -14, sy2+6); cr.curve_to(-22, sy2+6, -20, sy2-2, -14, sy2-10)
        fill_stroke(cr, (0.75, 0.9, 1, 0.95), 2)
    if P.get('tear'):
        ell(cr, 18, 6, 4, 6); fill(cr, (0.7, 0.88, 1, 0.9))
    cr.restore()
    # shell
    cr.new_path(); cr.move_to(-118, -40); cr.curve_to(-118, -170, 118, -170, 118, -40); cr.close_path()
    fill_stroke(cr, c['shell'], 4.5)
    cr.save(); cr.move_to(-118, -40); cr.curve_to(-118, -170, 118, -170, 118, -40); cr.close_path(); cr.clip()
    cr.set_line_width(4); cr.set_source_rgba(*c['edge'])
    pts = [(-62, -112), (0, -122), (62, -112)]
    for (px, py) in pts:
        cr.new_path()
        for k in range(6):
            a = math.pi/3*k+math.pi/6; cr.line_to(px+math.cos(a)*30, py+math.sin(a)*26)
        cr.close_path(); cr.set_source_rgba(*c['plate']); cr.fill_preserve(); cr.set_source_rgba(*c['edge']); cr.stroke()
        for r in (14, 22):
            cr.new_path()
            for k in range(6):
                a = math.pi/3*k+math.pi/6; cr.line_to(px+math.cos(a)*r, py+math.sin(a)*r*0.85)
            cr.close_path(); cr.set_source_rgba(*c['edge'][:3], 0.35); cr.set_line_width(2); cr.stroke()
    cr.set_line_width(4); cr.set_source_rgba(*c['edge'])
    for x in range(-110, 120, 36):
        cr.move_to(x, -40); cr.line_to(x+6, -78); cr.stroke()
    cr.move_to(-120, -80); cr.curve_to(-60, -88, 60, -88, 120, -80); cr.stroke()
    cr.restore()
    rrect(cr, -122, -48, 244, 16, 8); fill_stroke(cr, shade(c['shell'], 0.8), 4)
    # satchel
    if P.get('satchel', True):
        cr.move_to(-40, -46); cr.curve_to(-30, -130, 40, -140, 50, -60); stroke(cr, shade(c['straw'], 0.7), 6)
        ell(cr, -26, -58, 34, 26); fill_stroke(cr, c['straw'], 3.5)
        cr.set_line_width(2); cr.set_source_rgba(*shade(c['straw'], 0.7))
        for k in range(-50, 0, 8): cr.move_to(k, -78); cr.line_to(k+6, -36); cr.stroke()
        if P.get('figs', 2):
            for k in range(P.get('figs', 2)):
                ell(cr, -36+k*18, -82, 9, 10); fill_stroke(cr, c['fig'], 2.5)
    legd(56, 0.0, c['skin']); legd(-76, 0.5, c['skin'])
    cr.restore()

def fig(cr, x, y, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(0, -16); cr.curve_to(14, -10, 16, 10, 0, 14); cr.curve_to(-16, 10, -14, -10, 0, -16)
    fill_stroke(cr, TORT['fig'], 3); cr.move_to(0, -16); cr.line_to(2, -22); stroke(cr, OUT+(1,), 3)
    ell(cr, -4, -4, 3, 5); fill(cr, (1, 1, 1, 0.35)); cr.restore()

# ---------------- OWL (Glafka) ----------------
def owl(cr, P, t=0):
    c = OWL
    cr.save(); cr.translate(P['x'], P['y']); cr.scale(P.get('s', 1), P.get('s', 1))
    for k in (-1, 1):
        for j in (-6, 0, 6):
            cr.move_to(k*22+j, -4); cr.line_to(k*22+j*1.4, 6); stroke(cr, hexc('#C9A86A'), 5)
    wl, wr = P.get('wings', (0, 0))
    for k, wa in ((-1, wl), (1, wr)):
        cr.save(); cr.translate(k*58, -96); cr.rotate(k*(0.15+wa))
        ell(cr, 0, 26, 24, 54); fill_stroke(cr, shade(c['body'], 0.85))
        for j in range(3): ell(cr, 0, 6+j*20, 6, 4); fill(cr, c['spot'])
        cr.restore()
    ell(cr, 0, -80, 70, 80); fill_stroke(cr, c['body'])
    ell(cr, 0, -62, 46, 56); fill(cr, mix(c['body'], c['spot'], 0.45))
    rnd = random.Random(5)
    for k in range(14):
        ell(cr, rnd.uniform(-40, 40), rnd.uniform(-100, -20), 5, 3.5); fill(cr, shade(c['body'], 0.75))
    cr.save(); cr.translate(0, -150); cr.rotate(P.get('tilt', 0))
    sw = P.get('swivel', 0)
    ell(cr, 0, 0, 72, 58); fill_stroke(cr, c['body'])
    rnd = random.Random(9)
    for k in range(10):
        ell(cr, rnd.uniform(-55, 55), rnd.uniform(-48, -20), 4, 4); fill(cr, c['spot'])
    for k in (-1, 1):
        ex = k*28+sw*30
        ell(cr, ex, 2, 30*(1-abs(sw)*0.4), 28); fill(cr, mix(c['body'], c['spot'], 0.6))
        cr.move_to(ex-26*k, -20); cr.curve_to(ex-8*k, -38, ex+14*k, -34, ex+28*k, -18); stroke(cr, c['brow'], 7)
        P2 = dict(P); P2['lidcol'] = c['body']
        if k == 1 and 'wink' in P: P2['eye'] = P['wink']
        eye(cr, ex, 2, 21*(1-abs(sw)*0.4), 21, c['eye'], P2, ir=17)
    bx = sw*30
    mo = P.get('mouth', 0)
    cr.move_to(bx-9, 20); cr.line_to(bx+9, 20); cr.line_to(bx, 36+mo*4); cr.close_path(); fill_stroke(cr, c['beak'], 3)
    if mo > 0.1:
        ell(cr, bx, 34+mo*6, 6, 2+mo*7); fill_stroke(cr, hexc('#4A1E1E'), 2.5)
    # laurel
    cr.save(); cr.rotate(-0.18)
    for k in range(-5, 6):
        a = -math.pi/2+k*0.17; x, y = math.cos(a)*60, math.sin(a)*50+4
        ell(cr, x, y, 7, 13, a+math.pi/2+0.5*(1 if k > 0 else -1)); fill_stroke(cr, c['leaf'], 2)
    cr.restore()
    cr.restore(); cr.restore()

# ---------------- FOX (Alepou) ----------------
def fox(cr, P, t=0):
    c = FOX
    cr.save(); cr.translate(P['x'], P['y']); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    lean = P.get('lean', 0)
    hip = (0, -128)
    # tail
    tw = P.get('tail', 0)+math.sin(t*2.5)*0.08
    cr.save(); cr.translate(-26, -100); cr.rotate(-0.9+tw)
    cr.move_to(0, 0); cr.curve_to(-30, -60, -90, -150, -20, -200); cr.curve_to(40, -150, 30, -60, 14, 0); cr.close_path()
    fill_stroke(cr, c['fur'])
    cr.move_to(-40, -168); cr.curve_to(-30, -190, -16, -202, -20, -200); cr.curve_to(10, -185, 20, -170, 18, -160); cr.curve_to(0, -150, -20, -150, -40, -168)
    fill(cr, c['white']); cr.restore()
    legs = P.get('legs', [(0.08, -0.08), (-0.08, 0.05)])
    for i in (1, 0):
        th, sh = legs[i]; k = add(hip, vecd(th, 62)); a = add(k, vecd(th+sh, 62))
        col = c['dark'] if i == 0 else shade(c['dark'], 0.75)
        capsule(cr, hip, k, 26, col); capsule(cr, k, a, 20, col); ell(cr, a[0]+12, a[1]-4, 18, 9); fill_stroke(cr, col)
    neck = add(hip, vec(lean, 118)); sho = add(hip, vec(lean, 98))
    arms = P.get('arms', [(0.2, -0.4), (0.1, -0.3)])
    def arm(i, col):
        sa, ea = arms[i]; e = add(sho, vecd(lean+sa, 46)); h = add(e, vecd(lean+sa+ea, 44))
        capsule(cr, sho, e, 18, col); capsule(cr, e, h, 16, col); ell(cr, h[0], h[1], 10, 9); fill_stroke(cr, c['dark']); return h, lean+sa+ea
    arm(1, shade(c['fur'], 0.8))
    mid = add(hip, vec(lean, 58)); ell(cr, mid[0], mid[1], 44, 72, lean); fill_stroke(cr, c['fur'])
    cr.save(); ell(cr, mid[0], mid[1], 44, 72, lean); cr.clip(); ell(cr, mid[0]+18, mid[1]-14, 26, 56, lean); fill(cr, c['white']); cr.restore()
    # cloak over far (left) shoulder, draped across back
    cr.save(); cr.translate(*sho); cr.rotate(lean)
    cr.move_to(-30, -14); cr.curve_to(20, -24, 40, -8, 30, 10); cr.curve_to(10, 40, -30, 80, -56, 96)
    cr.curve_to(-60, 50, -52, 10, -30, -14); fill_stroke(cr, c['cloak'], 3.5)
    ell(cr, 22, 0, 9, 9); fill_stroke(cr, c['pin'], 3)
    cr.restore()
    hc = add(neck, vec(lean*0.5+P.get('hd', 0), 44))
    cr.save(); cr.translate(*hc); cr.rotate(lean*0.4+P.get('hd', 0))
    for i, bx in enumerate((-22, 6)):
        cr.move_to(bx-16, -26); cr.line_to(bx+2, -82+P.get('earl', 0)*10); cr.line_to(bx+20, -24); cr.close_path()
        fill_stroke(cr, c['fur'] if i else shade(c['fur'], 0.85))
        cr.move_to(bx-6, -32); cr.line_to(bx+2, -66); cr.line_to(bx+10, -30); cr.close_path(); fill(cr, c['dark'])
    cr.move_to(-46, -6); cr.curve_to(-46, -46, 10, -50, 30, -20); cr.line_to(84, 8); cr.curve_to(70, 26, 30, 34, -10, 34)
    cr.curve_to(-40, 32, -48, 16, -46, -6); fill_stroke(cr, c['fur'])
    cr.move_to(10, 30); cr.curve_to(40, 26, 70, 22, 84, 8); cr.line_to(20, 10); cr.close_path(); fill(cr, c['white'])
    cr.move_to(-46, 4); cr.curve_to(-50, 30, -30, 36, -16, 34); cr.line_to(-20, 10); cr.close_path(); fill(cr, c['white'])
    ell(cr, 84, 6, 9, 7); fill(cr, (0.08, 0.06, 0.05, 1))
    P2 = dict(P); P2['lidcol'] = c['fur']
    eye(cr, 14, -10, 11, 9, c['eye'], P2, ir=7)
    brow(cr, 14, -26, 22, P.get('brow', 0))
    mouth(cr, 58, 22, 22, P.get('mouth', 0), P.get('smile', 0.8))
    cr.restore()
    hp, ang = arm(0, c['fur'])
    if P.get('reed', True):
        ra = P.get('reed_a', ang)
        a = add(hp, vecd(ra+math.pi, 40)); b = add(hp, vecd(ra+math.pi, -170))
        cr.move_to(*a); cr.line_to(*b); stroke(cr, hexc('#9C8A3E'), 6)
        if P.get('flag'):
            cr.move_to(*b); cr.line_to(b[0]+40, b[1]+8); cr.line_to(b[0]+4, b[1]+28); cr.close_path(); fill_stroke(cr, hexc('#B8432F'), 2.5)
    cr.restore()

# ---------------- DONKEY (Thanasis) ----------------
def donkey(cr, P, t=0):
    g = hexc('#8E8C88'); wm = hexc('#E9E4DA'); mn = hexc('#3D3934')
    cr.save(); cr.translate(P['x'], P['y']); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    for x, col in ((70, shade(g, 0.8)), (-80, shade(g, 0.8))):
        rrect(cr, x-11, -120, 22, 120, 10); fill_stroke(cr, col); ell(cr, x, -4, 14, 8); fill_stroke(cr, mn)
    cr.move_to(-130, -170); cr.curve_to(-170, -150, -160, -110, -170, -80); stroke(cr, mn, 6)
    ell(cr, -170, -76, 8, 14); fill(cr, mn)
    ell(cr, 0, -170, 140, 72); fill_stroke(cr, g)
    ell(cr, 0, -128, 110, 28); fill(cr, mix(g, wm, 0.4))
    # blanket
    cr.save(); ell(cr, 0, -170, 140, 72); cr.clip()
    cols = [hexc('#C8643B'), hexc('#F3EDE1')]
    for i in range(7):
        cr.rectangle(-70+i*20, -260, 20, 130); fill(cr, cols[i % 2])
    cr.restore(); cr.rectangle(-70, -238, 140, 108); stroke(cr, OUT+(1,), 3.5)
    for x in (-40, 40):
        ell(cr, x, -118, 22, 28); fill_stroke(cr, hexc('#B5582F')); rrect(cr, x-8, -150, 16, 10, 3); fill_stroke(cr, hexc('#B5582F'), 3)
    for x, col in ((50, g), (-100, g)):
        rrect(cr, x-12, -120, 24, 120, 10); fill_stroke(cr, col); ell(cr, x, -4, 15, 8); fill_stroke(cr, mn)
    nod = P.get('nod', 0)
    cr.save(); cr.translate(110, -210); cr.rotate(0.35+nod)
    cr.move_to(-30, 40); cr.curve_to(-10, -40, 30, -70, 50, -80); cr.line_to(70, -40); cr.curve_to(50, -10, 30, 30, 20, 50); cr.close_path()
    fill_stroke(cr, g)
    cr.move_to(-26, 30); cr.curve_to(-6, -40, 30, -70, 50, -86); stroke(cr, mn, 10)
    cr.translate(62, -64); cr.rotate(0.9)
    ef = P.get('ear', 0)
    for i, bx in enumerate((-14, 6)):
        cr.save(); cr.translate(bx, -26); cr.rotate(-0.5+i*0.25+ef*(1 if i else 0))
        ell(cr, 0, -40, 12, 42); fill_stroke(cr, g if i else shade(g, 0.85)); ell(cr, 0, -38, 5, 30); fill(cr, hexc('#D9A9A0'))
        cr.restore()
    rrect(cr, -30, -36, 60, 110, 28); fill_stroke(cr, g)
    rrect(cr, -28, 34, 56, 42, 22); fill_stroke(cr, wm)
    ell(cr, -10, 56, 4, 6); fill(cr, mn); ell(cr, 10, 56, 4, 6); fill(cr, mn)
    P2 = dict(P); P2['lidcol'] = g; P2.setdefault('eye', 0.55)
    cr.save(); cr.rotate(-0.9); eye(cr, 4, -4, 9, 10, hexc('#3A2A1E'), P2, ir=7); cr.restore()
    mo = P.get('mouth', 0)
    cr.move_to(-16, 72); cr.curve_to(-6, 78+mo*14, 6, 78+mo*14, 16, 72); stroke(cr, OUT+(1,), 4)
    cr.restore(); cr.restore()

# ---------------- SPARROW ----------------
SPARROW_MARK = {'PIP': 'cheek', 'PIM': 'crest', 'PIO': 'thread'}
def sparrow(cr, P, t=0):
    who = P.get('who', 'PIP'); s = P.get('s', 1)*(0.85 if who == 'PIO' else 1)
    br = hexc('#8A5A35'); gr = hexc('#A8A39A'); cream = hexc('#EADFC8')
    cr.save(); cr.translate(P['x'], P['y']-P.get('hop', 0)); cr.scale(s*P.get('f', 1), s)
    sq = P.get('squash', 0); cr.scale(1+sq*0.2, 1-sq*0.2)
    for k in (-6, 6):
        cr.move_to(k, -12); cr.line_to(k, 0); stroke(cr, hexc('#C08A5A'), 3.5)
        if who == 'PIO' and k == 6:
            cr.move_to(k-4, -6); cr.line_to(k+4, -6); stroke(cr, hexc('#D62E2E'), 3)
    cr.move_to(-18, -26); cr.line_to(-44, -36+P.get('tailw', 0)*8); cr.line_to(-40, -20); cr.close_path(); fill_stroke(cr, shade(br, 0.8), 3)
    ell(cr, 0, -26, 25, 20); fill_stroke(cr, br, 3.5)
    ell(cr, 4, -20, 16, 12); fill(cr, cream)
    fa = P.get('flap', 0)
    cr.save(); cr.translate(-4, -30); cr.rotate(-0.2-fa*1.2); ell(cr, -6, 0, 18, 10); fill_stroke(cr, shade(br, 0.75), 3); cr.restore()
    hx, hy = 16, -46
    ell(cr, hx, hy, 17, 15); fill_stroke(cr, gr, 3.5)
    cr.save(); ell(cr, hx, hy, 17, 15); cr.clip(); ell(cr, hx-2, hy-12, 18, 8); fill(cr, br); cr.restore()
    if who == 'PIP': ell(cr, hx+2, hy+6, 6, 4); fill(cr, (1, 1, 1, 1))
    if who == 'PIM':
        cr.move_to(hx-6, hy-13); cr.curve_to(hx-14, hy-30, hx-2, hy-30, hx+2, hy-14); fill_stroke(cr, br, 2.5)
    mo = P.get('mouth', 0)
    cr.move_to(hx+14, hy-3); cr.line_to(hx+28, hy+1-mo*2); cr.line_to(hx+14, hy+2); cr.close_path(); fill_stroke(cr, hexc('#E3A946'), 2.5)
    if mo > 0.1:
        cr.move_to(hx+14, hy+3); cr.line_to(hx+26, hy+5+mo*6); cr.line_to(hx+14, hy+6+mo*3); cr.close_path(); fill_stroke(cr, hexc('#E3A946'), 2.5)
    P2 = dict(P); P2['lidcol'] = gr
    eye(cr, hx+6, hy-3, 4.5, 5, (0.08, 0.06, 0.05, 1), P2, ir=4)
    cr.restore()

# ---------------- crowd & extras ----------------
def goat(cr, P, t=0):
    col = P.get('col', hexc('#EDE6D6')); dk = shade(col, 0.75)
    cr.save(); cr.translate(P['x'], P['y']-P.get('hop', 0)); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    for x in (40, -40):
        rrect(cr, x-7, -70, 14, 70, 6); fill_stroke(cr, dk, 3)
    ell(cr, 0, -88, 66, 36); fill_stroke(cr, col)
    for x in (54, -28):
        rrect(cr, x-8, -70, 16, 70, 6); fill_stroke(cr, col, 3)
    cr.move_to(-62, -100); cr.line_to(-78, -116); cr.line_to(-60, -92); fill_stroke(cr, col, 3)
    cr.save(); cr.translate(58, -112); cr.rotate(P.get('ht', 0)+math.sin(t*3+P['x'])*0.04)
    cr.move_to(0, -10); cr.curve_to(-6, -50, -30, -56, -36, -40); stroke(cr, hexc('#8C7A5E'), 8)
    rrect(cr, -10, -24, 54, 40, 18); fill_stroke(cr, col)
    cr.move_to(30, 14); cr.line_to(34, 34); cr.line_to(40, 14); fill_stroke(cr, dk, 2.5)
    ell(cr, -4, -22, 8, 14, 0.8); fill_stroke(cr, dk, 3)
    P2 = dict(P); P2['lidcol'] = col
    eye(cr, 14, -8, 6, 6, hexc('#C9963B'), P2, ir=5)
    mouth(cr, 34, 6, 12, P.get('mouth', 0), P.get('smile', 0.4))
    cr.restore(); cr.restore()

def bunny(cr, P, t=0):
    col = P.get('col', hexc('#C9B79C'))
    cr.save(); cr.translate(P['x'], P['y']-P.get('hop', 0)); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    for a in (-0.2, 0.15):
        ell(cr, 4+a*30, -110, 9, 30, a); fill_stroke(cr, col, 3)
    ell(cr, 0, -40, 34, 40); fill_stroke(cr, col)
    ell(cr, 8, -82, 26, 22); fill_stroke(cr, col)
    P2 = dict(P); P2['lidcol'] = col; eye(cr, 18, -86, 5, 6, (0.1, 0.07, 0.05, 1), P2, ir=5)
    mouth(cr, 28, -72, 10, P.get('mouth', 0), 0.5)
    cr.restore()

def hedgehog(cr, P, t=0):
    cr.save(); cr.translate(P['x'], P['y']-P.get('hop', 0)); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    cr.new_path()
    for k in range(19):
        a = math.pi+k*math.pi/18; r = 52 if k % 2 == 0 else 40
        cr.line_to(math.cos(a)*r*1.2, math.sin(a)*r-6)
    cr.close_path(); fill_stroke(cr, hexc('#6B5640'), 3)
    ell(cr, 46, -14, 22, 16); fill_stroke(cr, hexc('#D9C2A0'), 3); ell(cr, 66, -14, 5, 4); fill(cr, (0.08, 0.06, 0.05, 1))
    ell(cr, 46, -20, 3.5, 3.5); fill(cr, (0.08, 0.06, 0.05, 1))
    cr.restore()

def cat(cr, P, t=0):
    col = hexc('#E3A946')
    cr.save(); cr.translate(P['x'], P['y']); cr.scale(P.get('s', 1), P.get('s', 1))
    ell(cr, 0, -26, 60, 28); fill_stroke(cr, col)
    cr.move_to(-58, -14); cr.curve_to(-90, -10, -90, 10, -60, 4); stroke(cr, OUT+(1,), 10); cr.move_to(-58, -14); cr.curve_to(-90, -10, -90, 10, -60, 4); stroke(cr, col, 6)
    ell(cr, 46, -40, 26, 22); fill_stroke(cr, col)
    for bx in (32, 56):
        cr.move_to(bx-10, -56); cr.line_to(bx, -76); cr.line_to(bx+10, -56); cr.close_path(); fill_stroke(cr, col, 3)
    for k, ex in enumerate((38, 58)):
        op = P.get('eye', 0) if k == 1 else 0
        if op > 0.1:
            ell(cr, ex, -42, 5, 6*op); fill_stroke(cr, hexc('#7FAE5B'), 2)
        else:
            cr.move_to(ex-5, -42); cr.curve_to(ex-2, -38, ex+2, -38, ex+5, -42); stroke(cr, OUT+(1,), 3)
    cr.restore()

def frog(cr, P, t=0):
    gcol = hexc('#7FAE5B')
    cr.save(); cr.translate(P['x'], P['y']); cr.scale(P.get('s', 1)*P.get('f', 1), P.get('s', 1))
    th = P.get('throat', 0)
    if th > 0: ell(cr, 18, -14, 14*th+4, 10*th+3); fill_stroke(cr, hexc('#E8DDB4'), 2.5)
    ell(cr, 0, -20, 34, 22); fill_stroke(cr, gcol)
    for ex in (-12, 14):
        ell(cr, ex, -42, 11, 11); fill_stroke(cr, gcol)
        P2 = dict(P); P2['lidcol'] = gcol; eye(cr, ex, -42, 7, 7, (0.1, 0.1, 0.05, 1), P2, ir=6)
    cr.move_to(-10, -10); cr.curve_to(0, -4, 12, -4, 24, -12); stroke(cr, OUT+(1,), 3)
    cr.restore()
