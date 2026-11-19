"""Episode 2 location: the olive grove at harvest time (registers 'grove' in bgs.LOCS)."""
import bgs
from bgs import *

GROVE_TREES = [450, 1300, 2400, 3200]
GROVE_GY = 960

def _olive_tree(cr, tx, gy, s, tod, rnd, branch=None):
    tr = H_('#6B5440', tod); trd = H_('#4A3A2C', tod)
    cr.save(); cr.translate(tx, gy); cr.scale(s, s)
    cr.move_to(-110, 0); cr.curve_to(-60, -40, -70, -200, -50, -300); cr.curve_to(-90, -380, -150, -420, -200, -470)
    cr.line_to(-170, -490); cr.curve_to(-100, -440, -50, -400, -10, -360); cr.curve_to(30, -420, 90, -470, 170, -500)
    cr.line_to(185, -475); cr.curve_to(110, -430, 50, -370, 50, -300); cr.curve_to(60, -200, 60, -40, 120, 0); cr.close_path()
    fill_stroke(cr, tr, 5)
    for k in range(7):
        x = -45+k*14+rnd.uniform(-4, 4)
        cr.move_to(x, -10); cr.curve_to(x+rnd.uniform(-25, 25), -120, x+rnd.uniform(-25, 25), -200, x+rnd.uniform(-10, 10), -290)
        stroke(cr, (trd[0], trd[1], trd[2], 0.55), 3.5)
    if branch:   # low side branch (for the sparrows / nets)
        d = branch
        cr.move_to(d*20, -330); cr.curve_to(d*120, -360, d*220, -380, d*330, -370); stroke(cr, OUT+(1,), 22)
        cr.move_to(d*20, -330); cr.curve_to(d*120, -360, d*220, -380, d*330, -370); stroke(cr, tr, 15)
    cols = [H_('#3F5230', tod, 0.95), H_('#55693A', tod, 0.95), H_('#7A8B4F', tod, 0.95), H_('#A9B489', tod, 0.9)]
    for (cx, cy, r) in [(-220, -520, 170), (0, -600, 200), (210, -540, 170), (-80, -470, 150), (100, -460, 140)]:
        foliage_blob(cr, rnd, cx, cy, r, cols, 50)
    for _ in range(36):
        x, y = rnd.uniform(-300, 300), rnd.uniform(-720, -380)
        ell(cr, x, y, 6, 8, 0.4); fill(cr, H_('#3F3A5A', tod, 0.9))
    cr.restore()

def L_grove():
    Wd, Hd = 3400, 1200; GY = GROVE_GY
    def back(cr, tod):
        sky(cr, Wd, Hd, tod, horizon=650)
        rnd = random.Random(201)
        hills(cr, Wd, 600, 140, H_('#8FA0A8', tod), 5, 90)
        cr.rectangle(0, 610, Wd, 26); fill(cr, H_('#3E7CB1', tod, 0.85))
        hills(cr, Wd, 690, 120, H_('#7E9466', tod), 17, 70)
        for i in range(16):
            x = 120+i*215+rnd.uniform(-40, 40); y = 700+rnd.uniform(-20, 20)
            cr.rectangle(x, y-26, 40, 26); fill(cr, H_('#EDE5D5', tod))
            cr.move_to(x-4, y-26); cr.line_to(x+20, y-38); cr.line_to(x+44, y-26); fill(cr, H_('#C8643B', tod))
        for i in range(40): olive_tree_small(cr, rnd.uniform(0, Wd), 760+rnd.uniform(0, 60), 0.55, tod, rnd)
    def main(cr, tod):
        rnd = random.Random(202)
        ground(cr, Wd, 760, Hd, ['#BFA868', '#8E7A44'], tod, 203, 1000)
        for _ in range(400):
            x, y = rnd.uniform(0, Wd), rnd.uniform(780, Hd)
            cr.move_to(x, y); cr.line_to(x+rnd.uniform(-6, 6), y-rnd.uniform(10, 26)); stroke(cr, H_('#7E8C4A', tod, 0.7), 2.5)
        # dry stone wall in the back
        for x in range(0, Wd, 70):
            rrect(cr, x, 760+rnd.uniform(-4, 4), 66, 34, 10); fill_stroke(cr, H_('#B8A48A', tod), 3)
        # flat harvest nets on the ground under the side trees
        for nx in (GROVE_TREES[0], GROVE_TREES[3]):
            cr.save(); cr.translate(nx, GY+40); cr.scale(1, 0.18)
            ell(cr, 0, 0, 420, 420); fill(cr, H_('#3E8E5A', tod, 0.25))
            cr.set_line_width(3)
            for k in range(-400, 420, 40):
                cr.move_to(k, -420); cr.line_to(k, 420); cr.move_to(-420, k); cr.line_to(420, k)
            cr.save(); ell(cr, 0, 0, 420, 420); cr.clip(); cr.set_source_rgba(*H_('#2F6E45', tod, 0.7)); cr.set_line_width(12); cr.stroke(); cr.restore()
            cr.new_path(); cr.restore()
            for k in range(70):
                ell(cr, nx+rnd.uniform(-330, 330), GY+40+rnd.uniform(-50, 50), 7, 9, 0.4); fill_stroke(cr, H_('#3F3A5A', tod), 2)
        # baskets of olives
        for bx in (820, 2900):
            cr.move_to(bx-70, GY+30); cr.line_to(bx-55, GY+90); cr.line_to(bx+55, GY+90); cr.line_to(bx+70, GY+30); cr.close_path()
            fill_stroke(cr, H_('#C99A52', tod), 4)
            for k in range(4):
                cr.move_to(bx-66+k*3, GY+42+k*12); cr.line_to(bx+66-k*3, GY+42+k*12); stroke(cr, H_('#9C6E3A', tod), 3)
            for k in range(14):
                ell(cr, bx-55+k*8, GY+26-abs(math.sin(k))*8, 9, 10, 0.4); fill_stroke(cr, H_('#3F3A5A', tod), 2)
        _olive_tree(cr, GROVE_TREES[0], GY, 1.05, tod, rnd)
        _olive_tree(cr, GROVE_TREES[1], GY, 1.0, tod, rnd, branch=1)
        _olive_tree(cr, GROVE_TREES[2], GY, 1.1, tod, rnd, branch=-1)
        _olive_tree(cr, GROVE_TREES[3], GY, 1.0, tod, rnd)
    def fg(cr, tod):
        rnd = random.Random(204)
        for x in range(-40, Wd+200, 110):
            for k in range(5):
                cr.move_to(x+k*8, Hd); cr.curve_to(x+k*8, Hd-50, x+k*8+rnd.uniform(-20, 20), Hd-90, x+k*8+rnd.uniform(-30, 30), Hd-rnd.uniform(90, 150))
                stroke(cr, H_('#7E7A3A', tod), 5)
    return dict(size=(Wd, Hd), layers=dict(back=back, main=main, fg=fg), ref=(1700, 600), gy=GY)

bgs.LOCS['grove'] = L_grove
