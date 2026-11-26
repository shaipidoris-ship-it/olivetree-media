"""Episode 3 location: the valley road under a big sky (registers 'road' in bgs.LOCS).
Windmill sails are animated separately with windmill_sails() at back parallax (over_back)."""
import bgs
from bgs import *
import bgs2

ROAD_GY = 1330                       # where characters stand on the road
ROAD_TREE = 2780                     # big olive tree giving shade
WINDMILLS = [(560, 905, 0.9), (2980, 870, 1.0), (3260, 900, 0.8)]   # back-layer coords (tower base)

def road_y(x):
    return ROAD_GY - 25*math.sin(x/3600*math.pi)

def _windmill_tower(cr, x, y, s, tod):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(-46, 0); cr.line_to(-34, -150); cr.line_to(34, -150); cr.line_to(46, 0); cr.close_path()
    fill_stroke(cr, H_('#F3EDE1', tod), 4)
    cr.rectangle(14, -150, 20, 150); fill(cr, H_('#D9CDB8', tod, 0.7))
    cr.move_to(-40, -150); cr.curve_to(-36, -196, 36, -196, 40, -150); cr.close_path(); fill_stroke(cr, H_('#B5582F', tod), 4)
    rrect(cr, -10, -40, 20, 40, 9); fill(cr, H_('#3E7CB1', tod))
    rrect(cr, -8, -110, 16, 20, 6); fill(cr, H_('#2B3A4A', tod))
    cr.restore()

def windmill_sails(cr, t, spin, tod='morning'):
    """spin = revolutions so far (caller integrates wind speed)."""
    for i, (x, y, s) in enumerate(WINDMILLS):
        cx, cy = x, y-160*s
        cr.save(); cr.translate(cx, cy); cr.scale(s, s); cr.rotate(spin*2*math.pi*(1 if i % 2 else 1.1)+i)
        for k in range(6):
            cr.save(); cr.rotate(k*math.pi/3)
            cr.move_to(0, 0); cr.line_to(0, -118); stroke(cr, OUT+(1,), 4)
            cr.move_to(3, -24); cr.line_to(30, -34); cr.line_to(26, -116); cr.line_to(3, -116); cr.close_path()
            fill_stroke(cr, T((0.97, 0.95, 0.9, 1), tod), 2.5)
            cr.restore()
        ell(cr, 0, 0, 9, 9); fill_stroke(cr, H_('#7A5A3A', tod), 3)
        cr.restore()

def soft_hills(cr, w, base, amp, col, seed):
    r = random.Random(seed); fs = [(r.uniform(1.0, 2.5), r.uniform(0, 6)), (r.uniform(3, 5), r.uniform(0, 6)), (r.uniform(6, 9), r.uniform(0, 6))]
    cr.move_to(0, 4000)
    for x in range(0, w+41, 40):
        u = x/w*math.pi
        y = base-amp*(0.55+0.3*math.sin(u*fs[0][0]+fs[0][1])+0.12*math.sin(u*fs[1][0]+fs[1][1])+0.05*math.sin(u*fs[2][0]+fs[2][1]))
        cr.line_to(x, y)
    cr.line_to(w, 4000); cr.close_path(); fill(cr, col)

def L_road():
    Wd, Hd = 3600, 1500
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=1000)
        rnd = random.Random(301)
        soft_hills(cr, Wd, 900, 150, H_('#93A3B8', tod), 31)
        cr.rectangle(0, 900, Wd, 28); fill(cr, H_('#3E7CB1', tod, 0.85))
        soft_hills(cr, Wd, 985, 90, H_('#88A06C', tod), 37)
        # white village on the left slope
        for i in range(12):
            x = 120+i*95+rnd.uniform(-20, 20); y = 950+rnd.uniform(-25, 10)
            cr.rectangle(x, y-30, 46, 30); fill(cr, H_('#EDE5D5', tod))
            cr.rectangle(x+34, y-30, 12, 30); fill(cr, H_('#D9CDB8', tod, 0.8))
            cr.rectangle(x+10, y-20, 10, 12); fill(cr, H_('#3E7CB1', tod))
        cr.move_to(1180, 930); cr.line_to(1180, 880); stroke(cr, H_('#EDE5D5', tod), 26)   # chapel
        ell(cr, 1180, 878, 16, 16); fill(cr, H_('#3E7CB1', tod))
        for x, y, s in WINDMILLS: _windmill_tower(cr, x, y, s, tod)
        for i in range(30): olive_tree_small(cr, rnd.uniform(1300, Wd), 990+rnd.uniform(0, 50), rnd.uniform(0.45, 0.65), tod, rnd)
        for i in range(8): cypress(cr, rnd.uniform(1400, 3400), 1010, rnd.uniform(110, 170), tod, rnd)
    def main(cr, tod):
        rnd = random.Random(302)
        g = cairo.LinearGradient(0, 1040, 0, Hd); g.add_color_stop_rgb(0, *H_('#B9AE6A', tod)[:3]); g.add_color_stop_rgb(1, *H_('#8E8246', tod)[:3])
        cr.move_to(0, 1080); cr.curve_to(1000, 1040, 2400, 1060, Wd, 1030); cr.line_to(Wd, Hd); cr.line_to(0, Hd); cr.close_path(); cr.set_source(g); cr.fill()
        dabs(cr, rnd, 0, 1050, Wd, Hd, H_('#C9BC78', tod), 700, 6, 26, 0.18)
        # dry stone wall behind the road
        for x in range(0, 2300, 64):
            rrect(cr, x, 1180+rnd.uniform(-4, 4)-8*math.sin(x/900), 62, 36, 10); fill_stroke(cr, H_('#B8A48A', tod), 3)
        for x in range(30, 2300, 64):
            rrect(cr, x, 1152+rnd.uniform(-4, 4)-8*math.sin(x/900), 58, 32, 10); fill_stroke(cr, H_('#C4B196', tod), 3)
        # the road
        cr.move_to(0, ROAD_GY-40)
        for x in range(0, Wd+1, 100): cr.line_to(x, road_y(x)-40)
        for x in range(Wd, -1, -100): cr.line_to(x, road_y(x)+70+25*math.sin(x/500))
        cr.close_path(); fill(cr, H_('#E2C990', tod))
        for _ in range(160):
            x = rnd.uniform(0, Wd); y = road_y(x)+rnd.uniform(-30, 60)
            ell(cr, x, y, rnd.uniform(3, 7), rnd.uniform(2, 4)); fill(cr, H_('#C9AE7E', tod, 0.7))
        # dry grass tufts + autumn asters
        for _ in range(420):
            x, y = rnd.uniform(0, Wd), rnd.uniform(1060, Hd)
            if abs(y-road_y(x)-10) < 70: continue
            cr.move_to(x, y); cr.line_to(x+rnd.uniform(-8, 8), y-rnd.uniform(14, 30)); stroke(cr, H_('#A39448', tod, 0.8), 2.5)
        for _ in range(90):
            x, y = rnd.uniform(0, Wd), rnd.uniform(1080, Hd)
            if abs(y-road_y(x)-10) < 80: continue
            ell(cr, x, y-20, 7, 6); fill(cr, H_('#9A7FC0', tod)); ell(cr, x, y-20, 2.2, 2.2); fill(cr, H_('#E3A946', tod))
        for k in range(6):
            x = rnd.uniform(200, 3400); y = road_y(x)+rnd.uniform(110, 150)
            ell(cr, x, y, 50, 24); fill_stroke(cr, H_('#9C8E7A', tod), 3)
        # big shady olive tree
        cr.save(); ell(cr, ROAD_TREE+20, ROAD_GY+20, 420, 50); fill(cr, (0.15, 0.12, 0.05, 0.22)); cr.restore()
        bgs2._olive_tree(cr, ROAD_TREE, ROAD_GY-10, 0.95, tod, rnd)
    def fg(cr, tod):
        rnd = random.Random(303)
        for x in range(-40, Wd+100, 120):
            for k in range(5):
                cr.move_to(x+k*8, Hd); cr.curve_to(x+k*8, Hd-50, x+k*8+rnd.uniform(-20, 20), Hd-80, x+k*8+rnd.uniform(-30, 30), Hd-rnd.uniform(80, 130))
                stroke(cr, H_('#8C7E3A', tod), 5)
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1800, 700), gy=ROAD_GY)

bgs.LOCS['road'] = L_road
