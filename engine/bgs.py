from core import *
from chars import fig

SKY = {
 'blue':      ['#283066', '#5B5F9E', '#C79AB4'],
 'morning':   ['#78AEDB', '#B9D6EA', '#F6E6C6'],
 'noon':      ['#7DBDE8', '#BFE0F2', '#F4F2E4'],
 'afternoon': ['#7FB4DB', '#C2D9E6', '#F4DDB0'],
 'late':      ['#8BA7CF', '#E6C7A0', '#F5C77E'],
 'sunset':    ['#4E4C8C', '#D9826A', '#F7C066'],
 'night':     ['#0F1433', '#1F2652', '#3A3F78'],
}
# ground/foliage tint per time of day (multiplier & warm add)
TINT = {'blue': (0.62, 0.66, 0.9), 'morning': (1, 0.98, 0.95), 'noon': (1.04, 1.03, 0.98), 'afternoon': (1.02, 0.97, 0.88),
        'late': (1.0, 0.9, 0.75), 'sunset': (0.95, 0.75, 0.62), 'night': (0.42, 0.46, 0.72)}
def T(c, tod):
    m = TINT[tod]; return (clamp(c[0]*m[0]), clamp(c[1]*m[1]), clamp(c[2]*m[2]), c[3] if len(c) > 3 else 1)
def H_(h, tod, a=1.0): return T(hexc(h, a), tod)

def sky(cr, w, h, tod, horizon=None):
    s = SKY[tod]; hz = horizon or h*0.7
    g = cairo.LinearGradient(0, 0, 0, hz)
    g.add_color_stop_rgb(0, *hexc(s[0])[:3]); g.add_color_stop_rgb(0.6, *hexc(s[1])[:3]); g.add_color_stop_rgb(1, *hexc(s[2])[:3])
    cr.set_source(g); cr.rectangle(0, 0, w, h); cr.fill()
    rnd = random.Random(w+len(tod))
    if tod in ('night', 'blue'):
        for _ in range(int(w*0.12)):
            x, y = rnd.uniform(0, w), rnd.uniform(0, hz*0.8)
            a = rnd.uniform(0.3, 0.95)*(1 if tod == 'night' else 0.45)
            ell(cr, x, y, rnd.uniform(1, 2.6), rnd.uniform(1, 2.6)); fill(cr, (1, 1, 0.92, a))
    else:
        for _ in range(int(w/320)):   # soft gouache clouds
            cx, cy = rnd.uniform(0, w), rnd.uniform(hz*0.1, hz*0.5)
            ccol = (1, 0.97, 0.93) if tod not in ('sunset', 'late') else (1, 0.85, 0.7)
            for k in range(7):
                ell(cr, cx+rnd.uniform(-120, 120), cy+rnd.uniform(-18, 18), rnd.uniform(50, 120), rnd.uniform(18, 34))
                fill(cr, ccol+(0.18,))

def dabs(cr, rnd, x0, y0, x1, y1, col, n, rmin=6, rmax=22, a=0.18, var=0.08):
    for _ in range(n):
        k = 1+rnd.uniform(-var, var)
        ell(cr, rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(rmin, rmax), rnd.uniform(rmin*0.5, rmax*0.6), rnd.uniform(0, 3))
        fill(cr, (clamp(col[0]*k), clamp(col[1]*k), clamp(col[2]*k), a))

def hills(cr, w, base, amp, col, seed, step=60):
    rnd = random.Random(seed); cr.move_to(0, base)
    pts = []; x = 0
    while x <= w+step:
        pts.append((x, base-amp*(0.5+0.5*math.sin(x/w*math.pi*rnd.uniform(1.5, 3.5)+seed))-rnd.uniform(0, amp*0.15))); x += step
    cr.move_to(0, 4000)
    for p in pts: cr.line_to(*p)
    cr.line_to(w, 4000); cr.close_path(); fill(cr, col)

def foliage_blob(cr, rnd, x, y, r, cols, n=26):
    for i in range(n):
        c = cols[min(len(cols)-1, int(i/n*len(cols)))]
        ell(cr, x+rnd.uniform(-r, r)*0.9, y+rnd.uniform(-r, r)*0.55-i*0.6, rnd.uniform(r*0.25, r*0.5), rnd.uniform(r*0.18, r*0.34), rnd.uniform(-0.4, 0.4))
        fill(cr, c)

def cypress(cr, x, base, h, tod, rnd):
    cols = [H_('#2F4A2A', tod), H_('#3E5E33', tod), H_('#58773F', tod)]
    for i in range(40):
        t = i/40; yy = base-t*h; ww = (1-t)*h*0.12+6
        ell(cr, x+rnd.uniform(-ww, ww)*0.5, yy, ww*0.7, h*0.06, rnd.uniform(-0.3, 0.3)); fill(cr, cols[min(2, int(rnd.random()*3))])

def olive_tree_small(cr, x, base, s, tod, rnd):
    cr.move_to(x-6*s, base); cr.curve_to(x-10*s, base-40*s, x+8*s, base-50*s, x, base-80*s)
    stroke(cr, H_('#5A4636', tod), 9*s)
    foliage_blob(cr, rnd, x, base-90*s, 48*s, [H_('#55693A', tod, 0.9), H_('#7A8B4F', tod, 0.9), H_('#A3AE7A', tod, 0.8)], 18)

def house(cr, x, y, w, h, tod, rnd, roof=True):
    wall = H_('#F3EDE1', tod); sh = H_('#D9CDB8', tod)
    cr.rectangle(x, y-h, w, h); fill(cr, wall)
    cr.rectangle(x+w*0.82, y-h, w*0.18, h); fill(cr, sh)
    dabs(cr, rnd, x, y-h, x+w, y, hexc('#E6DCC8'), int(w*h/2500), 8, 26, 0.25)
    if roof:
        cr.move_to(x-14, y-h); cr.line_to(x+w/2, y-h-h*0.32); cr.line_to(x+w+14, y-h); cr.close_path(); fill(cr, H_('#C8643B', tod))
        cr.move_to(x-14, y-h); cr.line_to(x+w+14, y-h); stroke(cr, H_('#9E4A2A', tod), 6)
    for i in range(max(1, int(w/110))):
        wx = x+30+i*110;
        if wx+40 > x+w-20: break
        cr.rectangle(wx, y-h*0.72, 40, 50); fill(cr, H_('#2B3A4A', tod))
        cr.rectangle(wx-14, y-h*0.72, 14, 50); cr.rectangle(wx+40, y-h*0.72, 14, 50); fill(cr, H_('#3E7CB1', tod))
    if w > 160:
        rrect(cr, x+w*0.5-28, y-110, 56, 110, 26); fill(cr, H_('#3E7CB1', tod))
        cr.rectangle(x+w*0.5-28, y-60, 56, 60); fill(cr, H_('#3E7CB1', tod))

def bougainvillea(cr, x, y, r, tod, rnd):
    foliage_blob(cr, rnd, x, y, r*0.9, [H_('#3E5E33', tod, 0.9), H_('#58773F', tod, 0.9)], 14)
    for _ in range(int(r*1.2)):
        ell(cr, x+rnd.uniform(-r, r), y+rnd.uniform(-r*0.6, r*0.5), rnd.uniform(4, 9), rnd.uniform(3, 7)); fill(cr, H_('#C2357A', tod, 0.85))

def ground(cr, w, y, h, cols, tod, seed, n=900):
    g = cairo.LinearGradient(0, y, 0, y+h)
    g.add_color_stop_rgb(0, *H_(cols[0], tod)[:3]); g.add_color_stop_rgb(1, *H_(cols[1], tod)[:3])
    cr.set_source(g); cr.rectangle(0, y, w, h); cr.fill()
    dabs(cr, random.Random(seed), 0, y, w, y+h, H_(cols[0], tod), n, 6, 30, 0.12, 0.12)

# =============== LOCATIONS ===============
# each returns dict(size=(w,h), layers={'back':fn, 'main':fn, 'fg':fn}) ; fn(cr,tod)

def L_olive():
    Wd, Hd = 2600, 1700
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=1200)
        rnd = random.Random(1)
        cr.rectangle(0, 1170, Wd, 40); fill(cr, H_('#3E7CB1', tod))  # sea strip
        hills(cr, Wd, 1260, 140, H_('#7C8FA8', tod), 3, 80)
        hills(cr, Wd, 1360, 160, H_('#6E8462', tod), 7, 70)
        # valley village
        for i in range(26):
            x = 300+i*72+rnd.uniform(-20, 20); y = 1420+rnd.uniform(-30, 30)
            cr.rectangle(x, y-30, 46, 30); fill(cr, H_('#E8E0D0', tod))
            cr.move_to(x-4, y-30); cr.line_to(x+23, y-44); cr.line_to(x+50, y-30); fill(cr, H_('#C8643B', tod))
            if tod in ('blue', 'night'):
                glow(cr, x+23, y-14, 26, (1, 0.8, 0.4), 0.55); cr.rectangle(x+18, y-20, 9, 9); fill(cr, (1, 0.85, 0.5, 1))
        hills(cr, Wd, 1520, 120, H_('#5E7A4A', tod), 11, 60)
        for i in range(30): olive_tree_small(cr, rnd.uniform(0, Wd), 1560+rnd.uniform(0, 100), 0.6, tod, rnd)
    def main(cr, tod):
        rnd = random.Random(2)
        # hilltop
        cr.move_to(0, 1700); cr.line_to(0, 1290); cr.curve_to(600, 1180, 1000, 1150, 1500, 1150)
        cr.curve_to(2000, 1150, 2300, 1190, 2600, 1260); cr.line_to(2600, 1700); cr.close_path()
        g = cairo.LinearGradient(0, 1150, 0, 1700); g.add_color_stop_rgb(0, *H_('#B9A46A', tod)[:3]); g.add_color_stop_rgb(1, *H_('#7A6A3E', tod)[:3])
        cr.set_source(g); cr.fill()
        dabs(cr, rnd, 0, 1160, Wd, 1700, H_('#C9B67A', tod), 900, 6, 26, 0.16)
        for _ in range(160):
            x = rnd.uniform(0, Wd); y = rnd.uniform(1180, 1650)
            cr.move_to(x, y); cr.line_to(x+rnd.uniform(-6, 6), y-rnd.uniform(10, 24)); stroke(cr, H_('#8C9A54', tod, 0.7), 2.5)
        # giant olive tree
        tx = 1500; tr = H_('#6B5440', tod); trd = H_('#4A3A2C', tod)
        cr.move_to(tx-260, 1160); cr.curve_to(tx-160, 1100, tx-170, 900, tx-140, 760); cr.curve_to(tx-180, 640, tx-260, 560, tx-330, 470)
        cr.line_to(tx-280, 450); cr.curve_to(tx-180, 520, tx-90, 600, tx-40, 650); cr.curve_to(tx+20, 560, tx+120, 470, tx+260, 400)
        cr.line_to(tx+290, 430); cr.curve_to(tx+170, 520, tx+90, 640, tx+110, 760); cr.curve_to(tx+140, 900, tx+150, 1100, tx+280, 1160)
        cr.close_path(); cr.set_source_rgba(*tr); cr.fill_preserve(); cr.set_source_rgb(*OUT); cr.set_line_width(5); cr.stroke()
        for k in range(14):  # bark grooves
            x = tx-120+k*18+rnd.uniform(-6, 6)
            cr.move_to(x, 1140); cr.curve_to(x+rnd.uniform(-40, 40), 1000, x+rnd.uniform(-40, 40), 880, x+rnd.uniform(-20, 20), 760)
            stroke(cr, trd+(0,) if False else (trd[0], trd[1], trd[2], 0.55), 4)
        # hollow
        ell(cr, tx-30, 830, 78, 96); fill_stroke(cr, H_('#2A1E16', tod), 5)
        ell(cr, tx-30, 905, 70, 16); fill(cr, H_('#4A3A2C', tod))
        # roots
        for sx, d in ((tx-250, -1), (tx+270, 1), (tx-120, -1), (tx+140, 1)):
            cr.move_to(sx-d*60, 1150); cr.curve_to(sx, 1120, sx+d*80, 1150, sx+d*170, 1175); cr.line_to(sx+d*150, 1185); cr.curve_to(sx+d*60, 1170, sx, 1160, sx-d*60, 1170)
            cr.close_path(); fill_stroke(cr, tr, 4)
        # canopy
        cols = [H_('#3F5230', tod, 0.95), H_('#55693A', tod, 0.95), H_('#7A8B4F', tod, 0.95), H_('#A9B489', tod, 0.9)]
        for (cx, cy, r) in [(tx-380, 430, 230), (tx-120, 330, 260), (tx+200, 300, 260), (tx+430, 420, 220), (tx+40, 520, 200), (tx-300, 590, 150), (tx+300, 570, 150), (tx-580, 520, 140), (tx+620, 500, 130)]:
            foliage_blob(cr, rnd, cx, cy, r, cols, 70)
        for _ in range(500):
            x, y = tx+rnd.uniform(-700, 700), rnd.uniform(150, 700)
            ell(cr, x, y, rnd.uniform(5, 10), rnd.uniform(2, 3.5), rnd.uniform(0, 3)); fill(cr, H_('#C9D2B0', tod, 0.3))
    def fg(cr, tod):
        rnd = random.Random(4)
        for _ in range(30):
            x = rnd.uniform(0, Wd); y = 1700
            for k in range(5):
                cr.move_to(x+k*6, y); cr.curve_to(x+k*6, y-60, x+k*6+rnd.uniform(-20, 20), y-110, x+k*8+rnd.uniform(-30, 30), y-rnd.uniform(110, 170))
                stroke(cr, H_('#55693A', tod, 0.9), 4)
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1500, 850))

def L_hollow():
    Wd, Hd = 2200, 1300
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=Hd)
        rnd = random.Random(7)
        cols = [H_('#2F3F26', tod, 0.9), H_('#3F5230', tod, 0.9), H_('#55693A', tod, 0.85)]
        for _ in range(16): foliage_blob(cr, rnd, rnd.uniform(0, Wd), rnd.uniform(0, 400), rnd.uniform(140, 260), cols, 40)
    def main(cr, tod):
        rnd = random.Random(8); tr = H_('#6B5440', tod)
        cr.move_to(300, Hd); cr.curve_to(380, 900, 330, 500, 420, 150); cr.curve_to(500, 0, 900, -60, 1200, 0)
        cr.curve_to(1600, 40, 1820, 200, 1800, 500); cr.curve_to(1780, 900, 1850, 1100, 1950, Hd); cr.close_path(); fill(cr, tr)
        for k in range(60):
            x = rnd.uniform(320, 1900); y = rnd.uniform(0, Hd)
            cr.move_to(x, y); cr.curve_to(x+rnd.uniform(-30, 30), y+60, x+rnd.uniform(-30, 30), y+120, x+rnd.uniform(-10, 10), y+rnd.uniform(140, 260))
            stroke(cr, H_('#4A3A2C', tod, 0.5), rnd.uniform(3, 7))
        dabs(cr, rnd, 320, 0, 1900, Hd, H_('#7D6650', tod), 500, 8, 30, 0.2)
        # hollow opening
        ell(cr, 1100, 600, 330, 380); fill_stroke(cr, H_('#5A4636', tod), 8)
        ell(cr, 1100, 620, 290, 340); fill(cr, H_('#22180F', tod))
        g = cairo.RadialGradient(1100, 760, 40, 1100, 700, 420); g.add_color_stop_rgba(0, 0.25, 0.17, 0.1, 1); g.add_color_stop_rgba(1, 0.08, 0.05, 0.03, 1)
        ell(cr, 1100, 620, 290, 340); cr.set_source(g); cr.fill()
        # ledge
        ell(cr, 1100, 905, 300, 50); fill_stroke(cr, H_('#7D6650', tod), 6)
        ell(cr, 1100, 895, 280, 36); fill(cr, H_('#8E775E', tod))
    def fg(cr, tod):
        rnd = random.Random(9)
        for _ in range(6): foliage_blob(cr, rnd, rnd.choice([rnd.uniform(-50, 300), rnd.uniform(1900, 2250)]), rnd.uniform(100, 1200), rnd.uniform(90, 160),
                                        [H_('#2F3F26', tod), H_('#3F5230', tod), H_('#55693A', tod)], 40)
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1100, 650))

def L_square():
    Wd, Hd = 3200, 1320
    GY = 960
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=700)
        rnd = random.Random(10)
        hills(cr, Wd, 620, 200, H_('#9AB09A', tod), 21, 90)
        for i in range(10): cypress(cr, rnd.uniform(0, Wd), 640, rnd.uniform(140, 220), tod, rnd)
        for i in range(14):
            x = i*240+rnd.uniform(-40, 40); house(cr, x, 700, rnd.uniform(160, 220), rnd.uniform(130, 200), tod, rnd)
    def main(cr, tod):
        rnd = random.Random(11)
        # front row of houses
        xs = [(0, 380, 380), (420, 300, 330), (2300, 340, 360), (2690, 520, 300)]
        for x, w, h in xs: house(cr, x, GY-130, w, h, tod, rnd)
        bougainvillea(cr, 400, 560, 110, tod, rnd); bougainvillea(cr, 2290, 540, 120, tod, rnd)
        # plaza ground
        ground(cr, Wd, GY-140, Hd-GY+140, ['#E6CF9E', '#C9A979'], tod, 12, 1100)
        for _ in range(120):
            x, y = rnd.uniform(0, Wd), rnd.uniform(GY-120, Hd)
            ell(cr, x, y, rnd.uniform(18, 40), rnd.uniform(6, 12)); stroke(cr, H_('#B8976A', tod, 0.35), 2)
        # fountain wall
        fx = 1600
        rrect(cr, fx-170, GY-430, 340, 330, 20); fill_stroke(cr, H_('#E8DCC4', tod), 5)
        cr.move_to(fx-170, GY-430); cr.curve_to(fx-120, GY-520, fx+120, GY-520, fx+170, GY-430); cr.close_path(); fill_stroke(cr, H_('#E8DCC4', tod), 5)
        dabs(cr, rnd, fx-160, GY-500, fx+160, GY-110, hexc('#D6C8AC'), 120, 6, 20, 0.3)
        ell(cr, fx, GY-330, 50, 46); fill_stroke(cr, H_('#C9A979', tod), 4)  # lion head
        ell(cr, fx, GY-330, 64, 60); stroke(cr, H_('#B08A5A', tod), 10)
        for ex in (-16, 16): ell(cr, fx+ex, GY-342, 6, 5); fill(cr, OUT+(1,))
        ell(cr, fx, GY-310, 12, 8); fill(cr, H_('#3B2A20', tod))
        # basin
        cr.move_to(fx-260, GY-160); cr.line_to(fx+260, GY-160); cr.line_to(fx+230, GY-60); cr.line_to(fx-230, GY-60); cr.close_path()
        fill_stroke(cr, H_('#DCCDB0', tod), 5)
        ell(cr, fx, GY-160, 260, 26); fill_stroke(cr, H_('#5E9BC9', tod), 5)
        # stalls
        def stall(x, top, goods):
            for px in (x, x+300): cr.rectangle(px, GY-340, 14, 260); fill_stroke(cr, H_('#8A5A3A', tod), 3)
            cr.move_to(x-30, GY-340); cr.line_to(x+344, GY-340); cr.line_to(x+320, GY-400); cr.line_to(x-6, GY-400); cr.close_path()
            fill_stroke(cr, H_(top, tod), 4)
            for k in range(6): cr.rectangle(x-30+k*62, GY-340, 31, 22); fill(cr, H_('#F3EDE1', tod))
            rrect(cr, x-10, GY-200, 334, 120, 8); fill_stroke(cr, H_('#B07A4A', tod), 4)
            for i in range(14):
                c = goods[i % len(goods)]; ell(cr, x+14+i*22, GY-210-(i % 2)*14, 16, 15); fill_stroke(cr, H_(c, tod), 2.5)
        stall(520, '#3E7CB1', ['#6B3B5E', '#7A8B4F', '#E3A946'])
        stall(2380, '#C8643B', ['#D9462F', '#E3A946', '#7FAE5B'])
        for i in range(5): rrect(cr, 2420+i*44, GY-240, 30, 36, 6); fill_stroke(cr, H_('#E3A946', tod, 0.9), 2.5)
        # low wall for crowd (right)
        rrect(cr, 2050, GY-170, 1150, 90, 8); fill_stroke(cr, H_('#EDE3CF', tod), 4)
        dabs(cr, rnd, 2050, GY-170, 3200, GY-80, hexc('#D6C8AC'), 100, 6, 18, 0.3)
        rrect(cr, 60, GY-150, 420, 70, 8); fill_stroke(cr, H_('#EDE3CF', tod), 4)
    def fg(cr, tod):
        rnd = random.Random(13)
        pass
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1600, 600), gy=GY)

def L_gate():
    Wd, Hd = 2400, 1100; GY = 940
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=760)
        rnd = random.Random(20)
        hills(cr, Wd, 760, 260, H_('#8FAE7A', tod), 4, 80)
        olive_tree_small(cr, 1900, 520, 0.9, tod, rnd)
        for i in range(25): olive_tree_small(cr, rnd.uniform(0, Wd), rnd.uniform(620, 760), rnd.uniform(0.5, 0.8), tod, rnd)
    def main(cr, tod):
        rnd = random.Random(21)
        ground(cr, Wd, GY-90, Hd, ['#D8BC88', '#B8976A'], tod, 22, 700)
        # path
        cr.move_to(0, GY+60); cr.curve_to(800, GY+40, 1500, GY-20, Wd, GY-60); cr.line_to(Wd, GY+20); cr.curve_to(1500, GY+80, 800, GY+140, 0, GY+160); cr.close_path()
        fill(cr, H_('#E6CF9E', tod))
        # gate arch
        gx = 900
        for px in (gx-220, gx+120):
            rrect(cr, px, GY-480, 100, 480, 6); fill_stroke(cr, H_('#E8DCC4', tod), 5)
            dabs(cr, rnd, px, GY-480, px+100, GY, hexc('#D6C8AC'), 50, 6, 18, 0.3)
        cr.move_to(gx-220, GY-480); cr.curve_to(gx-200, GY-660, gx+200, GY-660, gx+220, GY-480); cr.line_to(gx+120, GY-480)
        cr.curve_to(gx+110, GY-560, gx-110, GY-560, gx-120, GY-480); cr.close_path(); fill_stroke(cr, H_('#E8DCC4', tod), 5)
        rrect(cr, 0, GY-200, gx-220, 110, 6); fill_stroke(cr, H_('#EDE3CF', tod), 4)
        rrect(cr, gx+220, GY-200, 700, 110, 6); fill_stroke(cr, H_('#EDE3CF', tod), 4)
        # sign
        cr.rectangle(1500, GY-260, 14, 240); fill_stroke(cr, H_('#8A5A3A', tod), 3)
        cr.move_to(1460, GY-280); cr.line_to(1640, GY-280); cr.line_to(1680, GY-250); cr.line_to(1640, GY-220); cr.line_to(1460, GY-220); cr.close_path(); fill_stroke(cr, H_('#B07A4A', tod), 3)
        olive_tree_small(cr, 1600, GY-246, 0.25, tod, rnd)
        bougainvillea(cr, gx-260, GY-500, 120, tod, rnd)
    def fg(cr, tod): pass
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1200, 550), gy=GY)

def L_vineyard():
    Wd, Hd = 4400, 1100; GY = 900
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=600)
        rnd = random.Random(30)
        hills(cr, Wd, 560, 160, H_('#A8B88A', tod), 5, 100)
        for row in range(5):
            y = 560+row*60
            hills(cr, Wd, y+40, 20, H_(['#B9A46A', '#AE9A60', '#A39058', '#988650', '#8E7C48'][row], tod), 30+row, 120)
            for x in range(0, Wd, 46):
                ell(cr, x+rnd.uniform(-6, 6), y+20, 22, 14); fill(cr, H_(['#7A8B4F', '#6E8247', '#647A40', '#5A7038', '#506632'][row], tod))
    def main(cr, tod):
        rnd = random.Random(31)
        ground(cr, Wd, GY-60, Hd, ['#D6B57E', '#B08A5A'], tod, 32, 1400)
        rrect(cr, 0, GY-150, Wd, 100, 0); fill(cr, H_('#C9AE7E', tod))
        for x in range(0, Wd, 58):
            rrect(cr, x, GY-150+rnd.uniform(-4, 4), 56, 34, 8); fill_stroke(cr, H_('#D9C9A6', tod), 3)
        # vines on posts behind path
        for x in range(40, Wd, 230):
            cr.rectangle(x, GY-330, 10, 190); fill_stroke(cr, H_('#7A5A3A', tod), 3)
        cr.move_to(0, GY-310); cr.line_to(Wd, GY-310); stroke(cr, H_('#5A4636', tod), 2.5)
        for x in range(0, Wd, 34):
            foliage_blob(cr, rnd, x, GY-300+rnd.uniform(-10, 10), 40, [H_('#4E6B33', tod), H_('#6E8B3D', tod), H_('#93AA55', tod)], 10)
            if rnd.random() < 0.35:
                gx2, gy2 = x+rnd.uniform(-10, 10), GY-250
                for k in range(7): ell(cr, gx2+(k % 3)*9-9, gy2+(k//3)*9, 6, 6); fill_stroke(cr, H_('#5E3A6E', tod), 1.5)
        # amphora scarecrow
        ax = 2600
        cr.rectangle(ax-4, GY-420, 8, 280); fill(cr, H_('#7A5A3A', tod)); cr.rectangle(ax-80, GY-360, 160, 8); fill(cr, H_('#7A5A3A', tod))
        ell(cr, ax, GY-440, 40, 52); fill_stroke(cr, H_('#B5582F', tod), 4); ell(cr, ax-14, GY-450, 6, 6); fill(cr, OUT+(1,)); ell(cr, ax+12, GY-450, 6, 6); fill(cr, OUT+(1,))
    def fg(cr, tod):
        rnd = random.Random(33)
        for x in range(0, Wd, 140):
            foliage_blob(cr, rnd, x+rnd.uniform(-30, 30), Hd+20, 90, [H_('#3F5A2A', tod), H_('#4E6B33', tod), H_('#6E8B3D', tod)], 16)
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(2200, 550), gy=GY)

STONES = [(640, 0), (820, 0), (1000, 0), (1180, 1), (1360, 0), (1540, 0), (1720, 0)]
def L_stream():
    Wd, Hd = 2600, 1100; GY = 900
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=560)
        rnd = random.Random(40)
        hills(cr, Wd, 560, 220, H_('#8FAE7A', tod), 8, 90)
        for i in range(30): olive_tree_small(cr, rnd.uniform(0, Wd), rnd.uniform(480, 600), rnd.uniform(0.5, 0.9), tod, rnd)
    def main(cr, tod):
        rnd = random.Random(41)
        ground(cr, Wd, 600, Hd, ['#A9B477', '#7F8C55'], tod, 42, 800)
        # stream flowing toward the viewer
        cr.move_to(850, 600); cr.curve_to(1000, 610, 1200, 590, 1350, 600); cr.curve_to(1600, 800, 1800, 950, 1980, 1100)
        cr.line_to(420, 1100); cr.curve_to(600, 950, 750, 800, 850, 600); cr.close_path()
        g = cairo.LinearGradient(0, 600, 0, 1100); g.add_color_stop_rgb(0, *H_('#8FC0E0', tod)[:3]); g.add_color_stop_rgb(1, *H_('#3E7CB1', tod)[:3])
        cr.set_source(g); cr.fill_preserve(); cr.set_source_rgba(*H_('#6B5A3A', tod)); cr.set_line_width(7); cr.stroke()
        for _ in range(160):
            y = rnd.uniform(620, 1090); f = (y-600)/500; x0 = lerp(870, 440, f); x1 = lerp(1330, 1960, f)
            x = rnd.uniform(x0+20, x1-60); cr.move_to(x, y); cr.line_to(x+rnd.uniform(20, 50)*(0.5+f), y); stroke(cr, (1, 1, 1, 0.3), 2+f*2)
        for side in (0, 1):
            for k in range(26):
                f = k/26; y = lerp(610, 1090, f); x = lerp(850, 430, f) if side == 0 else lerp(1350, 1970, f)
                for j in range(3):
                    cr.move_to(x+j*6-10, y); cr.line_to(x+j*6-10+rnd.uniform(-8, 8), y-rnd.uniform(20, 50)*(0.5+f)); stroke(cr, H_('#6E8B3D', tod), 2.5)
        # plane tree far bank right
        px = 2200
        cr.move_to(px-40, GY-120); cr.curve_to(px-30, GY-300, px-60, GY-420, px-30, GY-560); cr.line_to(px+30, GY-560); cr.curve_to(px+20, GY-420, px+50, GY-300, px+50, GY-120)
        cr.close_path(); fill_stroke(cr, H_('#A89A80', tod), 4)
        for k in range(10): ell(cr, px+rnd.uniform(-30, 30), GY-150-rnd.uniform(0, 380), 14, 10); fill(cr, H_('#D2C8B0', tod, 0.7))
        for (cx, cy, r) in [(px-160, GY-620, 200), (px+140, GY-640, 210), (px, GY-760, 220)]:
            foliage_blob(cr, rnd, cx, cy, r, [H_('#3F5A2A', tod), H_('#58773F', tod), H_('#7FA055', tod)], 50)
        for lx, ly in ((900, 1000), (1420, 990), (760, 1060)):
            ell(cr, lx, ly, 36, 11); fill_stroke(cr, H_('#5E8C3A', tod), 2.5)
    def fg(cr, tod):
        rnd = random.Random(43)
        for x in range(0, Wd, 60):
            for k in range(4):
                cr.move_to(x+k*8, Hd); cr.curve_to(x+k*8, Hd-70, x+k*8+rnd.uniform(-20, 20), Hd-120, x+k*8+rnd.uniform(-20, 20), Hd-rnd.uniform(130, 200))
                stroke(cr, H_('#4E6B33', tod), 5)
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1300, 550), gy=GY)

def L_stones_top():
    Wd, Hd = 2400, 1300
    def back(cr, tod):
        pass
    def main(cr, tod):
        rnd = random.Random(50)
        cr.rectangle(0, 0, Wd, Hd); fill(cr, H_('#4A8BBF', tod))
        for _ in range(400):
            x, y = rnd.uniform(0, Wd), rnd.uniform(0, Hd)
            cr.move_to(x, y); cr.curve_to(x+20, y-6, x+40, y+6, x+70, y); stroke(cr, (1, 1, 1, 0.22), 3)
        for x0, x1, y0, y1 in ((0, Wd, 0, 220), (0, Wd, 1080, Hd)):
            cr.rectangle(x0, y0, x1-x0, y1-y0); fill(cr, H_('#8FA55E', tod))
            dabs(cr, rnd, x0, y0, x1, y1, H_('#A9B477', tod), 300, 8, 30, 0.3)
        for i, (sx, w) in enumerate(STONES):
            x = 260+i*290; y = 650+math.sin(i*1.3)*90
            ell(cr, x+10, y+12, 100, 70); fill(cr, (0, 0, 0.1, 0.25))
            ell(cr, x, y, 100, 70); fill_stroke(cr, H_('#8A8478', tod), 5); ell(cr, x-16, y-14, 60, 36); fill(cr, H_('#A8A294', tod))
        for k in range(5):
            x, y = rnd.uniform(100, 2300), rnd.uniform(300, 1000)
            ell(cr, x, y, 50, 46); fill_stroke(cr, H_('#5E8C3A', tod), 3); cr.move_to(x, y); cr.line_to(x+50, y-10); stroke(cr, H_('#3E6B2A', tod), 3)
    def fg(cr, tod): pass
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1200, 650),
                stone_xy=[(260+i*290, 650+math.sin(i*1.3)*90) for i in range(7)])

def L_meadow():
    Wd, Hd = 2800, 1300; GY = 1000
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=700)
        rnd = random.Random(60)
        # distant hill with olive tree upper right
        cr.move_to(0, 760); cr.curve_to(800, 700, 1700, 420, 2300, 300); cr.curve_to(2500, 270, 2700, 300, 2800, 330); cr.line_to(2800, Hd); cr.line_to(0, Hd); cr.close_path()
        fill(cr, H_('#9DB07A', tod))
        dabs(cr, rnd, 0, 300, Wd, 900, H_('#9DB07A', tod), 300, 10, 40, 0.15)
        tx = 2380; cr.move_to(tx-14, 300); cr.curve_to(tx-20, 260, tx, 240, tx, 210); stroke(cr, H_('#5A4636', tod), 10)
        foliage_blob(cr, rnd, tx, 190, 90, [H_('#55693A', tod), H_('#7A8B4F', tod), H_('#A3AE7A', tod)], 40)
        # zig-zag path on the far hill
        cr.move_to(1300, 640); cr.line_to(1700, 560); cr.line_to(1500, 500); cr.line_to(1950, 420); cr.line_to(1800, 380); cr.line_to(2300, 300)
        stroke(cr, H_('#E6CF9E', tod, 0.9), 10)
        for i in range(20): olive_tree_small(cr, rnd.uniform(0, 2000), rnd.uniform(650, 820), rnd.uniform(0.4, 0.6), tod, rnd)
    def main(cr, tod):
        rnd = random.Random(61)
        g = cairo.LinearGradient(0, 780, 0, Hd); g.add_color_stop_rgb(0, *H_('#C9B45E', tod)[:3]); g.add_color_stop_rgb(1, *H_('#9C8A3E', tod)[:3])
        cr.move_to(0, 820); cr.curve_to(900, 780, 1800, 800, Wd, 760); cr.line_to(Wd, Hd); cr.line_to(0, Hd); cr.close_path(); cr.set_source(g); cr.fill()
        dabs(cr, rnd, 0, 800, Wd, Hd, H_('#D6C470', tod), 800, 6, 26, 0.18)
        # path
        cr.move_to(0, GY+40); cr.curve_to(900, GY+10, 1800, GY-10, Wd, GY-30); cr.line_to(Wd, GY+60); cr.curve_to(1800, GY+80, 900, GY+100, 0, GY+130); cr.close_path()
        fill(cr, H_('#E2C990', tod))
        # umbrella pine
        px = 1400
        cr.move_to(px-30, GY-20); cr.curve_to(px-40, GY-200, px+20, GY-340, px-10, GY-520); cr.line_to(px+30, GY-520); cr.curve_to(px+60, GY-340, px+10, GY-200, px+30, GY-20); cr.close_path()
        fill_stroke(cr, H_('#7A5A3E', tod), 4)
        for b in (-1, 1):
            cr.move_to(px+5, GY-470); cr.curve_to(px+b*100, GY-520, px+b*200, GY-540, px+b*300, GY-560); stroke(cr, H_('#5A4636', tod), 14)
        cols = [H_('#2F4A2A', tod), H_('#3F5A2A', tod), H_('#4E6B33', tod), H_('#6E8B3D', tod)]
        for k in range(12):
            foliage_blob(cr, rnd, px-420+k*76, GY-600+abs(k-5.5)*10, 120, cols, 30)
        # grass + poppies
        for _ in range(500):
            x, y = rnd.uniform(0, Wd), rnd.uniform(820, Hd)
            cr.move_to(x, y); cr.line_to(x+rnd.uniform(-8, 8), y-rnd.uniform(14, 34)); stroke(cr, H_('#B5A24E', tod, 0.8), 2.5)
        for _ in range(140):
            x, y = rnd.uniform(0, Wd), rnd.uniform(830, Hd)
            if abs(y-GY) < 70: continue
            cr.move_to(x, y); cr.line_to(x, y-24); stroke(cr, H_('#5E7A3A', tod), 2)
            ell(cr, x, y-28, 9, 7); fill(cr, H_('#D93A2B', tod)); ell(cr, x, y-28, 2.5, 2.5); fill(cr, OUT+(1,))
    def fg(cr, tod):
        rnd = random.Random(62)
        for x in range(-40, Wd, 90):
            for k in range(5):
                cr.move_to(x+k*8, Hd); cr.curve_to(x+k*8, Hd-60, x+k*8+rnd.uniform(-20, 20), Hd-100, x+k*8+rnd.uniform(-30, 30), Hd-rnd.uniform(110, 180))
                stroke(cr, H_('#9C8A3E', tod), 5)
            if rnd.random() < 0.4: ell(cr, x+20, Hd-150, 12, 9); fill(cr, H_('#D93A2B', tod))
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1400, 650), gy=GY, pine=(1400, GY))

def L_hill():
    Wd, Hd = 3000, 1100; GY = 900
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=700)
        rnd = random.Random(70)
        hills(cr, Wd, 700, 160, H_('#8A7FA0', tod), 9, 100)
        hills(cr, Wd, 760, 120, H_('#9C8A6A', tod), 13, 80)
        cr.rectangle(0, 760, Wd, 30); fill(cr, H_('#3E7CB1', tod, 0.8))
    def main(cr, tod):
        rnd = random.Random(71)
        ground(cr, Wd, GY-140, Hd, ['#C99A62', '#9C6E42'], tod, 72, 800)
        cr.move_to(0, GY+20); cr.line_to(Wd, GY-20); cr.line_to(Wd, GY+70); cr.line_to(0, GY+110); cr.close_path(); fill(cr, H_('#E2BE88', tod))
        for x in range(0, Wd, 64):
            rrect(cr, x, GY-210+rnd.uniform(-4, 4), 62, 40, 10); fill_stroke(cr, H_('#B8A48A', tod), 3)
        for _ in range(40):
            x = rnd.uniform(0, Wd); y = GY-160+rnd.uniform(-20, 10)
            foliage_blob(cr, rnd, x, y, 40, [H_('#6E7A4A', tod), H_('#8E9A62', tod), H_('#B9A0C0', tod)], 10)
        for k in range(5):
            x = rnd.uniform(200, 2800); ell(cr, x, GY-60+rnd.uniform(40, 120), 60, 30); fill_stroke(cr, H_('#9C8E7A', tod), 3)
    def fg(cr, tod):
        rnd = random.Random(73)
        for x in range(0, Wd, 120):
            foliage_blob(cr, rnd, x, Hd+10, 70, [H_('#5E6A3A', tod), H_('#7A8650', tod)], 14)
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1500, 550), gy=GY)

def L_aerial():
    Wd, Hd = 2400, 1500
    PATH = [(300, 1400), (1700, 1220), (600, 1010), (1800, 820), (700, 640), (1650, 460), (1250, 300)]
    def back(cr, tod):
        rnd = random.Random(80)
        g = cairo.LinearGradient(0, 0, 0, Hd); g.add_color_stop_rgb(0, *H_('#B98A5A', tod)[:3]); g.add_color_stop_rgb(1, *H_('#8E6A44', tod)[:3])
        cr.set_source(g); cr.paint()
        dabs(cr, rnd, 0, 0, Wd, Hd, H_('#C9A06A', tod), 900, 10, 40, 0.18)
    def main(cr, tod):
        rnd = random.Random(81)
        cr.move_to(*PATH[0])
        for p in PATH[1:]: cr.line_to(*p)
        stroke(cr, H_('#5A3E26', tod, 0.6), 74); cr.move_to(*PATH[0])
        for p in PATH[1:]: cr.line_to(*p)
        stroke(cr, H_('#EBCB98', tod), 60)
        for i in range(len(PATH)-1):
            a, b = PATH[i], PATH[i+1]
            for k in range(14):
                f = k/14; x = lerp(a[0], b[0], f); y = lerp(a[1], b[1], f)
                rrect(cr, x-14, y+40, 28, 16, 5); fill_stroke(cr, H_('#B8A48A', tod), 2)
        for _ in range(70):
            x, y = rnd.uniform(0, Wd), rnd.uniform(0, Hd)
            foliage_blob(cr, rnd, x, y, 30, [H_('#6E7A4A', tod), H_('#8E9A62', tod)], 8)
        for _ in range(16):
            x, y = rnd.uniform(0, Wd), rnd.uniform(0, Hd); ell(cr, x, y, 40, 30); fill_stroke(cr, H_('#9C8E7A', tod), 3)
        # olive tree at top (seen from above)
        foliage_blob(cr, rnd, 1250, 200, 200, [H_('#3F5230', tod), H_('#55693A', tod), H_('#7A8B4F', tod), H_('#A9B489', tod)], 80)
    def fg(cr, tod): pass
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1200, 800), path=PATH)

def L_map():
    Wd, Hd = 2100, 1250
    def back(cr, tod):
        cr.set_source_rgba(*hexc('#C9A979')); cr.paint()
        dabs(cr, random.Random(90), 0, 0, Wd, Hd, hexc('#B8976A'), 500, 10, 40, 0.3)
    def main(cr, tod):
        rnd = random.Random(91)
        cr.move_to(140, 160); cr.curve_to(700, 100, 1400, 140, 1960, 120); cr.curve_to(2010, 500, 1990, 800, 1970, 1130)
        cr.curve_to(1400, 1160, 700, 1120, 130, 1150); cr.curve_to(100, 800, 120, 400, 140, 160); cr.close_path()
        fill_stroke(cr, hexc('#8A6A48'), 8)
        cr.move_to(170, 190); cr.curve_to(700, 140, 1400, 170, 1930, 150); cr.curve_to(1970, 500, 1950, 800, 1940, 1100)
        cr.curve_to(1400, 1130, 700, 1090, 160, 1120); cr.curve_to(140, 800, 150, 400, 170, 190); cr.close_path()
        fill(cr, hexc('#E8D5AE'))
        dabs(cr, rnd, 170, 190, 1930, 1100, hexc('#D9C29A'), 400, 8, 30, 0.35)
        for i in range(12):
            x = rnd.uniform(200, 1900); cr.move_to(x, 190); cr.curve_to(x+rnd.uniform(-40, 40), 600, x+rnd.uniform(-40, 40), 800, x, 1100)
            stroke(cr, hexc('#C9AE84', 0.4), 3)
        # icons along route
        ic = MAP_ROUTE
        # fountain
        x, y = ic[0]; ell(cr, x, y, 50, 18); fill_stroke(cr, hexc('#5E9BC9'), 4); rrect(cr, x-14, y-60, 28, 50, 6); fill_stroke(cr, hexc('#E8DCC4'), 3)
        for k in range(4): house(cr, x-260+k*70, y+60, 56, 50, 'morning', rnd, True)
        x, y = ic[1]
        for k in range(4):
            for j in range(3): ell(cr, x-60+k*40, y-30+j*30, 16, 12); fill_stroke(cr, hexc('#6E8B3D'), 2.5)
        x, y = ic[2]; cr.move_to(x-160, y-30); cr.curve_to(x-60, y+10, x+60, y-40, x+160, y+10); stroke(cr, hexc('#3E7CB1'), 26)
        x, y = ic[3]; cr.rectangle(x-6, y, 12, 50); fill(cr, hexc('#7A5A3E')); ell(cr, x, y-10, 70, 30); fill_stroke(cr, hexc('#3F5A2A'), 3)
        x, y = ic[4]; cr.move_to(x-10, y+60); cr.curve_to(x-12, y+20, x+6, y, x, y-20); stroke(cr, hexc('#5A4636'), 12)
        foliage_blob(cr, rnd, x, y-50, 80, [hexc('#55693A'), hexc('#7A8B4F'), hexc('#A3AE7A')], 30)
        cr.move_to(x-200, y+80); cr.curve_to(x-100, y+20, x+100, y+20, x+200, y+80); stroke(cr, hexc('#8A6A48'), 5)
    def fg(cr, tod): pass
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1050, 625))
MAP_ROUTE = [(420, 900), (760, 720), (1080, 820), (1380, 560), (1700, 330)]

LOCS = dict(olive=L_olive, hollow=L_hollow, square=L_square, gate=L_gate, vineyard=L_vineyard, stream=L_stream,
            stones=L_stones_top, meadow=L_meadow, hill=L_hill, aerial=L_aerial, map=L_map)

_cache = {}
def get(loc, tod):
    key = (loc, tod)
    if key not in _cache:
        L = LOCS[loc](); w, h = L['size']; surfs = {}
        for name, fn in L['layers'].items():
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); c = cairo.Context(s); fn(c, tod); surfs[name] = s
        L['surf'] = surfs; _cache[key] = L
    return _cache[key]
