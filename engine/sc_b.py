from kit import *

LINE = 1950
def chalk(cr):
    for k in range(9):
        f = k/8; x = lerp(LINE-4, LINE+26, f); y = lerp(985, 1125, f)
        cr.move_to(x-3, y); cr.line_to(x+3, y+12); stroke(cr, (1, 1, 1, 0.8), 6+6*f)
def bunting(cr):
    cr.move_to(1150, 300); cr.curve_to(1600, 400, 2300, 400, 2750, 300); stroke(cr, OUT+(1,), 2.5)
    for k in range(26):
        f = k/25; x = lerp(1150, 2750, f); y = 300+math.sin(f*math.pi)*75
        cr.move_to(x-14, y); cr.line_to(x, y+34); cr.line_to(x+14, y); cr.close_path(); fill_stroke(cr, hexc('#6E8B3D') if k % 2 else hexc('#93AA55'), 2)
SPAR3 = [(2070, 795), (2125, 795), (2180, 795)]
CROWD3 = [('bunny', 2330, 795, 0.9, None), ('goat', 2520, 795, 0.85, hexc('#C9B08A')), ('hedgehog', 2700, 795, 0.9, None),
          ('bunny', 2830, 795, 0.85, hexc('#A89A8A')), ('goat', 3010, 795, 0.8, hexc('#E8DCC8'))]
def crowd3(cr, t, sb, cheer=0.0):
    for i, (kind, x, y, s, col) in enumerate(CROWD3):
        P = dict(x=x, y=y, s=s, f=-1, hop=cheer*abs(math.sin(t*8+i))*14, mouth=cheer*0.6, eye=blink_at(t, sb[i::3]))
        if col: P['col'] = col
        dict(goat=goat, bunny=bunny, hedgehog=hedgehog)[kind](cr, P, t)
def spar3(cr, t, S, sb, **kw):
    for i, w in enumerate(('PIP', 'PIM', 'PIO')):
        x, y = SPAR3[i]
        P = dict(x=x, y=y, s=1.2, who=w, f=kw.get('f', [-1, -1, -1])[i], mouth=S.cues.mouth(w, t), eye=kw.get('eye', [None]*3)[i] or blink_at(t, sb[i::2]),
                 look=(-0.5, 0.3), squash=kw.get('squash', [0, 0, 0])[i])
        sparrow(cr, P, t)

# ======================= SCENE 3 =======================
def s3():
    S = Scene('s3', 31.0); c = S.cues
    c.say('s3_01', 0.5); c.say('s3_02', 8.4); c.say('s3_03', 17.3); c.say('s3_04', 20.6); c.say('s3_05', 22.8)
    c.say('s3_06', 26.2); c.say('s3_07', 28.3); c.say('crowd_yay', 28.7, 'CROWD')
    S.music += [(0.0, 17.0, 'fanfare_soft'), (22.6, 28.2, 'drumroll'), (28.3, 31.0, 'go_flourish')]
    S.fx(0.0, 'market_on', 0.6); S.fx(8.3, 'paper'); S.fx(26.3, 'pop'); S.fx(28.6, 'whoosh_l'); S.fx(28.7, 'dust')
    lb = auto_blinks(5, 32); cb = auto_blinks(6, 32, 4); sb = auto_blinks(7, 32)
    LX, LY, LS = 1890, 1065, 0.95
    CXp, CYp, CS = 1790, 995, 0.85
    def chel_x(t): return CXp + (TSPEED*CS*(t-28.8) if t > 28.8 else 0)
    def alepou(t, **kw):
        P = dict(x=2200, y=965, s=0.92, f=-1, mouth=c.mouth('ALEPOU', t), smile=0.9, brow=0.4, eye=blink_at(t, lb[1::2]),
                 arms=[(0.3, -0.4), (0.1, -0.3)])
        P.update(kw); return P
    def racers(cr, t, lagos=True, **kw):
        ch = T(chel_x(t), CYp, CS, 1, t, S, cb, walking=t > 28.8)
        if t > 28.8: ch['walk'] = (t-28.8)*0.5
        tortoise(cr, ch, t)
        if lagos: hare(cr, Hp(LX, LY, LS, 1, t, S, lb, **kw), t)

    def sh1(lt, t):
        cam = (2050, 720, 1.3)
        g = pulse(t, 0.6, 3.2, 0.3); sw = pulse(t, 3.8, 7.6, 0.4)
        def d(cr, L):
            bunting(cr); crowd3(cr, t, sb, cheer=0.4*pulse(t, 6.4, 8.2)); spar3(cr, t, S, sb)
            fox(cr, alepou(t, arms=[(lerp(0.3, 2.5, g)+0.6*sw*math.sin(t*2), -0.3), (lerp(0.1, -2.3, g), -0.3)], tail=0.3*g), t)
            chalk(cr); racers(cr, t)
        return frame('square', 'morning', cam, draw=d, flash=1-ramp(lt, 0, 0.3))
    S.shot(0, 8.2, sh1)

    marks = [8.6, 9.9, 11.3, 12.7, 14.6]
    def route_pt(t):
        R = bgs.MAP_ROUTE
        if t <= marks[0]: return R[0], 0
        for i in range(len(marks)-1):
            if marks[i] <= t < marks[i+1]:
                k = eio((t-marks[i])/(marks[i+1]-marks[i])); return (lerp(R[i][0], R[i+1][0], k), lerp(R[i][1], R[i+1][1], k)), i+k
        return R[-1], len(R)-1
    def sh2(lt, t):
        cam = campath(lt, 0, 8.8, (1050, 625, 0.92), (1120, 600, 1.0))
        def d(cr, L):
            R = bgs.MAP_ROUTE; (px, py), u = route_pt(t)
            # dotted line drawn so far
            pts = [R[0]]
            for i in range(1, len(R)):
                if u >= i: pts.append(R[i])
                else:
                    f = u-(i-1); pts.append((lerp(R[i-1][0], R[i][0], f), lerp(R[i-1][1], R[i][1], f))); break
            cr.move_to(*pts[0])
            for p in pts[1:]: cr.line_to(*p)
            cr.set_dash([18, 14]); stroke(cr, hexc('#B8432F'), 9); cr.set_dash([])
            for i, m in enumerate(marks):
                if t >= m:
                    k = clamp((t-m)/0.4); r = 70*(1+0.4*math.sin(k*math.pi))
                    cr.new_path(); cr.arc(R[i][0], R[i][1], r, 0, 2*math.pi); stroke(cr, hexc('#B8432F', 0.8), 6)
            bob = 30*abs(math.sin(t*9))*pulse(t, 14.6, 16.4)
            tip = (px, py-bob)
            cr.move_to(tip[0], tip[1]); cr.line_to(tip[0]+700, tip[1]+900); stroke(cr, hexc('#9C8A3E'), 16)
            cr.move_to(tip[0], tip[1]); cr.line_to(tip[0]+700, tip[1]+900); stroke(cr, hexc('#C9B86A'), 8)
            # fox paw holding the reed
            ell(cr, tip[0]+520, tip[1]+670, 40, 36); fill_stroke(cr, FOX['dark'])
        return frame('map', 'morning', cam, draw=d, grade=False)
    S.shot(8.2, 17.0, sh2)

    def sh3a(lt, t):
        cam = (1880, 780, 1.75)
        k = math.sin((t-17.0)*5)
        def d(cr, L):
            chalk(cr)
            P = Hp(LX, LY, LS, 1, t, S, lb, smile=1, teeth=c.mouth('LAGOS', t) < 0.1)
            if t < 18.8:
                P['crouch'] = 0; P['legs'] = [(0.7+0.3*k, -0.4-0.6*abs(k)), (-0.5, -0.1)]; P['arms'] = [(2.6, -0.4), (2.4, -0.4)]
            elif t < 19.9:
                P['arms'] = [(1.4, -2.0), (1.2, -1.9)]; P['eye'] = min(P['eye'], 0.5)
            else:
                P['arms'] = [(2.9, -0.8), (-0.4, -0.4)]
            hare(cr, P, t)
        return frame('square', 'morning', cam, draw=d)
    S.shot(17.0, 20.3, sh3a)

    def sh3b(lt, t):
        cam = (CXp+100, CYp-110, 2.3)
        br = pulse(t, 20.4, 21.6, 0.4)
        def d(cr, L):
            ch = T(CXp, CYp, CS*(1+0.025*br), 1, t, S, (), eye=1-0.9*pulse(t, 20.4, 21.4, 0.2), brow=-0.3, neck=0.5)
            tortoise(cr, ch, t)
        return frame('square', 'morning', cam, draw=d)
    S.shot(20.3, 22.6, sh3b)

    def sh4a(lt, t):
        cam = (1955, 1060, 3.0)
        def d(cr, L):
            chalk(cr)
            tortoise(cr, T(CXp, CYp, CS, 1, t, S, cb), t)
            P = Hp(LX, LY, LS, 1, t, S, lb); P['foot'] = [-0.35*abs(math.sin(t*10)), 0.0]
            hare(cr, P, t)
        return frame('square', 'morning', cam, draw=d)
    S.shot(22.6, 24.6, sh4a)

    def sh4b(lt, t):
        cam = (2180, 690, 1.9)
        def d(cr, L):
            bunting(cr); crowd3(cr, t, sb)
            spar3(cr, t, S, sb, squash=[0.25, 0.25, 0.25] if t < 26.2 else [0, 0, 0])
            sh = math.sin(t*35)*0.03
            fox(cr, alepou(t, arms=[(2.9+sh, -0.3), (0.1, -0.3)], reed_a=math.pi*0.98+sh, flag=True, look=(0.6*ramp(t, 26.4, 26.6), 0.4*ramp(t, 26.4, 26.6)),
                           brow=-0.6*ramp(t, 26.4, 26.6)), t)
        return frame('square', 'morning', cam, draw=d)
    S.shot(24.6, 27.0, sh4b)

    def sh5(lt, t):
        cam = (1980, 760, 1.05)
        launch = t >= 28.6
        def d(cr, L):
            bunting(cr); crowd3(cr, t, sb, cheer=ramp(t, 28.6, 29.0))
            pio_sq = 0.35*pulse(t, 27.1, 28.4, 0.15)
            spar3(cr, t, S, sb, squash=[0, 0, pio_sq])
            down = ramp(t, 28.3, 28.5)
            fox(cr, alepou(t, arms=[(lerp(2.9, 1.2, down), -0.3), (0.1, -0.3)], reed_a=lerp(math.pi*0.98, math.pi*0.55, down), flag=True,
                           brow=-0.6*(1-ramp(t, 28.0, 28.3)), look=(0.6*(1-ramp(t, 28.0, 28.3)), 0.4), mouth=c.mouth('ALEPOU', t)), t)
            chalk(cr)
            if launch:
                k = clamp((t-28.6)/0.35)
                for j in range(8):
                    dust(cr, LX+j*90*k, LY+5, 60+120*k, 0.7*(1-ramp(t, 29.5, 31)))
                if k < 1: hare(cr, H_run(lerp(LX, LX+1400, k*k), LY, LS, 1, t, t*4), t)
                speed_lines(cr, LX+500, LY-150, 12, 400, 0.6*(1-k), 3)
            racers(cr, t, lagos=not launch)
            if not launch and t > 28.35:
                pass
        def scr(cr):
            a = ramp(t, 30.2, 31.0)
            if a > 0:
                rnd = random.Random(4)
                for k in range(40):
                    ell(cr, rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(200, 500)*a, rnd.uniform(120, 300)*a); fill(cr, (0.85, 0.75, 0.58, 0.6*a))
        return frame('square', 'morning', cam, draw=d, screen=scr)
    S.shot(27.0, 31.0, sh5)
    return S

# ======================= SCENE 4 =======================
def s4():
    S = Scene('s4', 28.5); c = S.cues
    c.say('s4_01', 4.2); c.say('s4_02', 11.0); c.say('s4_03', 13.8); c.say('s4_04', 15.0); c.say('s4_05', 16.2); c.say('s4_06', 19.3)
    S.music += [(0.0, 13.0, 'dance'), (13.0, 18.5, 'lagos_soft'), (18.5, 28.5, 'dance')]
    S.fx(0.0, 'cicadas_on'); S.fx(1.6, 'whoosh_l'); S.fx(3.6, 'whoosh_m'); S.fx(6.6, 'clap'); S.fx(10.5, 'pop')
    for k in range(7): S.fx(19.0+k*0.42, 'tap', 0.6)
    S.fx(22.4, 'whoosh_s'); S.fx(23.6, 'croak'); S.fx(23.9, 'croak', 0.7); S.fx(25.0, 'whoosh_l')
    lb = auto_blinks(8, 30); sb = auto_blinks(9, 30); cb = auto_blinks(10, 30, 4)

    def sh1(lt, t):
        cam = (900, 700, 1.0)
        def d(cr, L):
            if t < 1.5:
                x = lerp(150, 880, t/1.5); hare(cr, H_run(x, 1030, 0.75, 1, t, t*3.4), t)
                dust(cr, x-120, 1050, 50, 0.5)
            elif t < 2.3:
                k = (t-1.5)/0.8; s = lerp(0.75, 4.0, k*k); x = lerp(880, 1000, k); y = lerp(1030, 1500, k*k)
                hare(cr, H_run(x, y, s, 1, t, t*3.4, lean=lerp(1.12, 0.6, k)), t)
            for j in range(4): dust(cr, 300+j*180, 1040, 70, 0.35*(1-ramp(t, 1.5, 3.5)))
        def scr(cr):
            a = 1-ramp(t, 0, 0.7)
            if a > 0:
                rnd = random.Random(4)
                for k in range(40):
                    ell(cr, rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(200, 500)*a, rnd.uniform(120, 300)*a); fill(cr, (0.85, 0.75, 0.58, 0.6*a))
        return frame('gate', 'noon', cam, draw=d, screen=scr)
    S.shot(0, 3.5, sh1)

    def Lx(t): return 700+520*(t-3.5)
    GXg = Lx(6.6)
    def sh2(lt, t):
        x = Lx(t); cam = (x+160, 720, 1.2)
        def d(cr, L):
            spin = ramp(t, 6.8, 7.6)
            gf = -1 if (spin == 0 or spin >= 1) else (1 if math.sin(spin*math.pi*4) > 0 else -1)
            goat(cr, dict(x=GXg+150, y=925, s=0.85, f=gf, hop=24*pulse(t, 6.4, 6.9, 0.15), mouth=0.5*pulse(t, 6.6, 7.6), eye=1, wide=1+0.2*spin), t)
            P = H_run(x, 965, 0.85, 1, t, t*3.4)
            if 6.3 <= t < 6.9: P['arms'] = [(2.8, -0.1), (1.0, -0.6)]
            P['mouth'] = max(c.mouth('LAGOS', t), 0.2); P['look'] = (0.6, 0)
            hare(cr, P, t)
            if 6.55 <= t < 6.9:
                k = (t-6.55)/0.35; cx2, cy2 = GXg+95, 770
                for j in range(8):
                    a = j*math.pi/4; cr.move_to(cx2+math.cos(a)*20*k, cy2+math.sin(a)*20*k); cr.line_to(cx2+math.cos(a)*70*k, cy2+math.sin(a)*70*k)
                    stroke(cr, (1, 0.95, 0.5, 1-k), 6)
            for j in range(1, 5): dust(cr, x-90*j, 990, 30+10*j, 0.4*(1-j/5))
        return frame('vineyard', 'noon', cam, draw=d)
    S.shot(3.5, 9.0, sh2)

    GRX = Lx(9.0)+180
    def sh3(lt, t):
        x = Lx(9.0)+90*(t-9.0); cam = (x+80, 660, 1.9)
        def d(cr, L):
            # grape cluster
            n = 7 if t < 10.5 else 6
            for k in range(n):
                ell(cr, GRX+(k % 3)*14-14, 610+(k//3)*14, 9, 9); fill_stroke(cr, hexc('#5E3A6E'), 2)
            cr.move_to(GRX, 560); cr.line_to(GRX, 600); stroke(cr, hexc('#5A4636'), 4)
            air = 150+40*math.sin(clamp((t-9)/4)*math.pi)
            P = H_run(x, 965, 0.85, 1, t, 0.15+(t-9)*0.12, air=air, lean=0.9)
            if t >= 10.5:
                P['mouth'] = max(c.mouth('LAGOS', t), 0.0); P['smile'] = 1; P['teeth'] = False; P['eye'] = 0.6
            hare(cr, P, t)
        def scr(cr):
            if t >= 10.5:   # cheek puff hint: tiny grape pop sparkle
                a = 1-ramp(t, 10.5, 11.0)
                glow(cr, W*0.55, H*0.35, 120, (1, 0.9, 0.6), 0.4*a)
        return frame('vineyard', 'noon', cam, draw=d, screen=scr)
    S.shot(9.0, 13.0, sh3)

    def sh4(lt, t):
        cam = (1990, 800, 1.1)
        CXs = 1790+TSPEED*0.85*(t+2.2)
        def d(cr, L):
            bunting(cr)
            look = [None, None, None]; fs = []
            for i, tt in enumerate((13.4, 13.7, 14.0)): fs.append(-1 if t < tt else -1)
            spar3(cr, t, S, sb, eye=[0.5, 0.5, 0.55])
            chalk(cr)
            for j in range(4): dust(cr, 2100+j*140, 1060, 70, 0.15)
            ch = T(CXs, 995, 0.85, 1, t, S, cb, walking=True); ch['walk'] = t*0.5
            tortoise(cr, ch, t)
        return frame('square', 'noon', cam, draw=d)
    S.shot(13.0, 18.5, sh4)

    ST = bgs.STONES
    hops = [(19.0+i*0.42, ST[i][0]) for i in range(7)]
    def hare_on_stones(t):
        if t < 19.0: return lerp(300, ST[0][0], ramp(t, 18.5, 19.0)), 0, 0
        for i in range(len(hops)):
            t0, x0 = hops[i]
            x1 = ST[i+1][0] if i+1 < len(ST) else 1960
            dur_ = 0.42 if i+1 < len(ST) else 0.9
            if t0 <= t < t0+dur_:
                k = (t-t0)/dur_; air = math.sin(k*math.pi)*(90 if i+1 < len(ST) else 260)
                rot = 2*math.pi*k if i+1 >= len(ST) else 0
                return lerp(x0, x1, k), air, rot
        return 1960, 0, 0
    def sh5(lt, t):
        cam = (1250, 660, 1.05)
        def d(cr, L):
            for i, (sx, wob) in enumerate(ST):
                r = 0.06*math.sin(t*30)*pulse(t, 19.0+i*0.42, 19.3+i*0.42, 0.05) if wob else 0
                ell(cr, sx, 908, 80, 26, r); fill_stroke(cr, bgs.H_('#8A8478', 'noon'), 4); ell(cr, sx-10, 902, 60, 14, r); fill(cr, bgs.H_('#A8A294', 'noon'))
            for i, (fx_, fy) in enumerate(((900, 1000), (1420, 990))):
                th = pulse(t, 23.6+i*0.3, 24.0+i*0.3, 0.05)
                frog(cr, dict(x=fx_, y=fy, s=1.0, f=1 if i == 0 else -1, throat=th, eye=blink_at(t, [20.5, 22.9])), t)
            x, air, rot = hare_on_stones(t)
            bow = pulse(t, 22.7, 23.8, 0.25)
            if t < 22.6:
                P = Hp(x, 900, 0.75, 1, t, S, lb, air=air, crouch=0.3)
                P['legs'] = [(0.6, -1.2), (0.4, -1.0)] if air > 20 else STAND_LEGS
                P['arms'] = [(2.4, -0.3), (2.2, -0.3)] if air > 20 else P['arms']
                if rot: P['rot'] = -rot
                P['smile'] = 1; P['teeth'] = air < 20
            else:
                P = Hp(1960, 900, 0.75, -1, t, S, lb, lean=0.6*bow)
                P['arms'] = [(lerp(0.3, 1.6, bow), lerp(-0.5, -1.4, bow)), (lerp(0.15, -0.8, bow), -0.3)]
                if t > 23.8: P['arms'] = [(2.6, -0.3), (2.4, -0.3)]
            hare(cr, P, t)
        return frame('stream', 'noon', cam, draw=d)
    S.shot(18.5, 25.0, sh5)

    def sh6(lt, t):
        cam = campath(lt, 0.6, 3.0, (1500, 640, 1.6), (1500, 340, 1.6))
        def d(cr, L):
            x = lerp(1960, 2800, ramp(t, 25.0, 25.5))
            if t < 25.6: hare(cr, H_run(x, 900, 0.75, 1, t, t*3.4), t)
            for j in range(5): dust(cr, 1960+j*120, 910, 60, 0.4*(1-ramp(t, 25.5, 27)))
            glow(cr, 1500, 180, 500, (1, 1, 0.9), 0.9); ell(cr, 1500, 180, 90, 90); fill(cr, (1, 1, 0.95, 1))
        return frame('stream', 'noon', cam, draw=d, flash=ramp(t, 27.6, 28.5))
    S.shot(25.0, 28.5, sh6)
    return S
