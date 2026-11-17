from kit import *

GY = 1000
LXS, LYS, LSS = 1470, GY-48, 0.85      # sleeping Lagos (meadow)
def sleeping(cr, t, S, **kw):
    hare(cr, H_lie(LXS, LYS, LSS, 1, t, S, **kw), t)
SLEEP_HEAD = (LXS-232*LSS, LYS-6)

# ======================= SCENE 5 =======================
def s5():
    S = Scene('s5', 31.0); c = S.cues
    c.say('s5_01', 4.8); c.say('s5_02', 8.2); c.say('lagos_yawn', 11.4); c.say('s5_03', 12.6); c.say('s5_04', 25.5)
    S.music += [(0.0, 11.0, 'lagos_soft'), (11.0, 31.0, 'lullaby')]
    S.fx(0.0, 'cicadas_on', 0.7); S.fx(0.9, 'skid'); S.fx(14.6, 'grass'); S.fx(21.6, 'pop', 0.4)
    for k in range(6): S.fx(19.2+k*2.0, 'snore', 0.9)
    lb = auto_blinks(11, 32)
    def run_in(t):
        if t < 0.9: return lerp(250, 1380, t/0.9), 'run'
        if t < 1.5: k = (t-0.9)/0.6; return 1380+40*math.sin(k*math.pi), 'skid'
        return 1380, 'stand'
    def sh1(lt, t):
        cam = (1320, 720, 1.05)
        def d(cr, L):
            x, mode = run_in(t)
            if mode == 'run': hare(cr, H_run(x, GY+10, 0.85, 1, t, t*3.4), t)
            elif mode == 'skid':
                P = Hp(x, GY+10, 0.85, 1, t, S, lb, lean=-0.3, legs=[(-0.7, 0.1), (-0.5, 0.0)], ears=(0.3, 0.5), arms=[(1.8, -0.4), (1.5, -0.3)])
                hare(cr, P, t); dust(cr, x+40, GY+20, 70, 0.6)
            else:
                P = Hp(x, GY+10, 0.85, 1, t, S, lb, ears=(-0.25+0.3*math.sin((t-1.5)*14)*math.exp(-(t-1.5)*3), -0.05+0.3*math.sin((t-1.5)*14+1)*math.exp(-(t-1.5)*3)))
                hare(cr, P, t)
        return frame('meadow', 'afternoon', cam, draw=d, flash=1-ramp(lt, 0, 0.8))
    S.shot(0, 4.5, sh1)
    def sh2a(lt, t):
        cam = (1390, 790, 1.8)
        def d(cr, L):
            P = Hp(1380, GY+10, 0.85, -1, t, S, lb, arms=[(2.55, -2.3), (0.15, -0.4)], eye=0.7, look=(0.3, 0))
            hare(cr, P, t)
        return frame('meadow', 'afternoon', cam, draw=d)
    S.shot(4.5, 6.2, sh2a)
    def sh2b(lt, t):
        cam = campath(lt, 0, 1.8, (620, 760, 1.15), (560, 760, 1.15))
        return frame('meadow', 'afternoon', cam)
    S.shot(6.2, 8.0, sh2b)
    def sh2c(lt, t):
        cam = (1390, 790, 1.8)
        def d(cr, L):
            P = Hp(1380, GY+10, 0.85, 1, t, S, lb, arms=[(0.8, -2.2), (0.6, -2.0)], eye=min(blink_at(t, lb), 0.55), smile=1, lean=-0.06)
            hare(cr, P, t)
        return frame('meadow', 'afternoon', cam, draw=d)
    S.shot(8.0, 11.2, sh2c)
    def sh3(lt, t):
        cam = campath(lt, 0, 7.8, (1400, 800, 1.45), (1360, 880, 1.75))
        yawn = pulse(t, 11.4, 12.6, 0.25)
        lie = ramp(t, 14.0, 15.0)
        def d(cr, L):
            if lie < 1:
                P = Hp(lerp(1380, LXS, lie), lerp(GY+10, LYS, lie), lerp(0.85, LSS, lie), 1, t, S, lb,
                       arms=[(lerp(0.3, 2.9, max(yawn, lie)), lerp(-0.5, -2.4, lie)), (lerp(0.15, 2.7, max(yawn, lie)), lerp(-0.4, -2.2, lie))])
                P['rot'] = -1.5*lie; P['mouth'] = max(P['mouth'], yawn); P['eye'] = min(P['eye'], 1-0.6*yawn)
                hare(cr, P, t)
            else:
                P = H_lie(LXS, LYS, LSS, 1, t, S, snore=False)
                P['mouth'] = c.mouth('LAGOS', t); P['eye'] = lerp(0.6, 0.0, ramp(t, 16.5, 18.9)); P['flop'] = (0, ramp(t, 17.5, 18.5))
                hare(cr, P, t)
        return frame('meadow', 'afternoon', cam, draw=d)
    S.shot(11.2, 19.0, sh3)
    def sh4(lt, t):
        cam = (SLEEP_HEAD[0]+20, SLEEP_HEAD[1]-40, 2.6)
        nd = ramp(t, 21.5, 22.3)
        def d(cr, L):
            jit = 0.05*pulse(t, 22.4, 22.6, 0.05)+0.05*pulse(t, 22.75, 22.95, 0.05)
            sleeping(cr, t, S, hd=jit)
            nx, ny = SLEEP_HEAD[0]-20, SLEEP_HEAD[1]-62
            px = lerp(nx+80, nx, nd); py = lerp(ny-500, ny, nd)
            cr.save(); cr.translate(px, py); cr.rotate(0.6+nd*0.8+math.sin(t*3)*0.3*(1-nd))
            cr.move_to(-22, 0); cr.line_to(22, 0); stroke(cr, hexc('#5E6B3A'), 4); cr.restore()
            zzz(cr, SLEEP_HEAD[0]-30, SLEEP_HEAD[1]-80, t, 1.0)
        return frame('meadow', 'afternoon', cam, draw=d)
    S.shot(19.0, 25.0, sh4)
    def sh5(lt, t):
        cam = (1320, 720, 1.0)
        k = ramp(t, 25.0, 31.0)
        def d(cr, L):
            cr.save(); cr.translate(1400+k*260, GY+10); cr.scale(1, 0.2); ell(cr, 0, 0, 420+k*200, 120); fill(cr, (0.1, 0.12, 0.05, 0.25)); cr.restore()
            sleeping(cr, t, S); zzz(cr, SLEEP_HEAD[0]-30, SLEEP_HEAD[1]-80, t, 0.6)
        return frame('meadow', 'afternoon', cam, draw=d, extra_grade=(1, 0.65, 0.3, 0.16*k))
    S.shot(25.0, 31.0, sh5)
    return S

# ======================= SCENE 6 =======================
def s6():
    S = Scene('s6', 52.0); c = S.cues
    c.say('s6_01', 1.0); c.say('s6_02', 13.0); c.say('s6_03', 18.9); c.say('s6_04', 24.4)
    c.say('s6_05', 34.0); c.say('s6_06', 35.3); c.say('s6_07', 42.3); c.say('s6_08', 44.0)
    S.music += [(0.0, 39.0, 'chelona'), (39.0, 52.0, 'chelona_swell')]
    S.fx(0.0, 'cicadas_on', 0.8); S.fx(7.0, 'stream_on'); S.fx(7.9, 'clack'); S.fx(8.3, 'clack', 0.7); S.fx(8.7, 'clack', 0.5)
    S.fx(14.5, 'snort', 0.6); S.fx(32.3, 'flutter'); S.fx(40.6, 'fig_roll', 0.7)
    for k in range(3): S.fx(28.0+k*2.0, 'snore', 0.5)
    for k in range(3): S.fx(39.5+k*2.2, 'snore', 0.35)
    cb = auto_blinks(12, 53, 3.6); sb = auto_blinks(13, 53); db = auto_blinks(14, 53, 4.5)
    def sh1(lt, t):
        x = 1300+TSPEED*1.0*t; cam = (x+170, 840, 1.75)
        def d(cr, L):
            ch = T(x, 990, 1.0, 1, t, S, cb, walking=True, brow=-0.4, sweat=ramp(t, 3.0, 5.5) if t < 5.6 else 0)
            tortoise(cr, ch, t)
        return frame('vineyard', 'afternoon', cam, draw=d)
    S.shot(0, 7.0, sh1)
    ST = bgs.STONES
    def stones(cr, t, tod):
        for i, (sx, wob) in enumerate(ST):
            r = 0.09*math.sin((t-7.8)*22)*math.exp(-(t-7.8)*2.2) if (wob and t > 7.8) else 0
            ell(cr, sx, 908, 80, 26, r); fill_stroke(cr, bgs.H_('#8A8478', tod), 4); ell(cr, sx-10, 902, 60, 14, r); fill(cr, bgs.H_('#A8A294', tod))
    def sh2(lt, t):
        cam = (1150, 840, 2.3)
        moving = not (8.0 <= t < 9.6)
        x = 1020+TSPEED*0.6*(min(t, 8.0)-7.0)+(TSPEED*0.6*(t-9.6) if t > 9.6 else 0)
        def d(cr, L):
            stones(cr, t, 'afternoon')
            ch = T(x, 905, 0.6, 1, t, S, cb, walking=moving, ha=0.12*pulse(t, 8.0, 9.6, 0.3), neck=0.42+0.3*pulse(t, 8.0, 9.6, 0.3),
                   look=(0.3, 0.6*pulse(t, 8.0, 9.6, 0.3)), brow=-0.3)
            if moving: ch['walk'] = (t-7.0)*0.5
            tortoise(cr, ch, t)
        return frame('stream', 'afternoon', cam, draw=d)
    S.shot(7.0, 12.5, sh2)
    def sh3(lt, t):
        cam = (2090, 800, 1.6)
        walking = t < 13.0 or t > 26.2
        x = 1880+(TSPEED*0.85*(t-26.2) if t > 26.2 else 0)
        def d(cr, L):
            stones(cr, t, 'afternoon')
            nod = 0.12*math.sin((t-24.4)*8)*pulse(t, 24.4, 26.0, 0.2)
            donkey(cr, dict(x=2290, y=1010, s=0.95, f=-1, mouth=c.mouth('THANASIS', t), eye=0.55*blink_at(t, db), nod=nod+0.05*math.sin(t*0.8),
                            ear=0.4*pulse(t, 15.0, 15.4, 0.1)), t)
            bow = 0.15*pulse(t, 22.8, 23.8, 0.3)
            ch = T(x, 1000, 0.85, 1, t, S, cb, walking=walking, ha=bow, smile=0.8, look=(0.4, 0))
            if walking: ch['walk'] = t*0.5
            tortoise(cr, ch, t)
        return frame('stream', 'afternoon', cam, draw=d)
    S.shot(12.5, 27.5, sh3)
    def sh4(lt, t):
        cam = (1100, 730, 1.0)
        def d(cr, L):
            sleeping(cr, t, S); zzz(cr, SLEEP_HEAD[0]-30, SLEEP_HEAD[1]-80, t, 0.6)
            x = 470+TSPEED*0.85*lt
            ch = T(x, GY+5, 0.85, 1, t, S, cb, walking=True); ch['walk'] = t*0.5
            tortoise(cr, ch, t)
        return frame('meadow', 'late', cam, draw=d)
    S.shot(27.5, 32.0, sh4)
    CXm = 1010
    BR = [(1300, 478), (1355, 470), (1410, 476)]
    def spar_fly(cr, t, land_t=32.3):
        for i, w in enumerate(('PIP', 'PIM', 'PIO')):
            k = ramp(t, land_t+i*0.12, land_t+0.7+i*0.12)
            x = lerp(BR[i][0]-500, BR[i][0], k); y = lerp(BR[i][1]-300, BR[i][1], k)
            sparrow(cr, dict(x=x, y=y, s=1.05, who=w, f=1, flap=math.sin(t*30)*(1-k) if k < 1 else 0, mouth=c.mouth(w, t),
                             eye=blink_at(t, sb[i::2]), look=(0.3, 0.7)), t)
    def sh5(lt, t):
        cam = (1330, 750, 1.3)
        def d(cr, L):
            sleeping(cr, t, S); zzz(cr, SLEEP_HEAD[0]-30, SLEEP_HEAD[1]-80, t, 0.6)
            sacc = [(0.6, 0.5), (0.6, -0.6), (0.6, 0.5), (0.6, 0.5)]
            i = 0 if t < 35.0 else (1 if t < 36.2 else (2 if t < 37.3 else 3))
            ch = T(CXm, GY+5, 0.85, 1, t, S, cb, look=sacc[i], neck=0.55, ha=0.15, smile=0.35, brow=0.2)
            tortoise(cr, ch, t)
            spar_fly(cr, t)
        return frame('meadow', 'late', cam, draw=d)
    S.shot(32.0, 39.0, sh5)
    FIGP0 = (CXm+150, 960); FIGP1 = (SLEEP_HEAD[0]+150, GY+5)
    def fig_pos(t):
        if t < 40.5: return None
        k = ramp(t, 40.5, 41.6); return (lerp(FIGP0[0], FIGP1[0], k), lerp(FIGP0[1], FIGP1[1], k)-math.sin(k*math.pi)*20), k*6
    def sh6(lt, t):
        cam = (1330, 930, 2.1)
        def d(cr, L):
            x = CXm+(TSPEED*0.85*(t-43.0) if t > 43.0 else 0)
            ch = T(x, GY+5, 0.85, 1, t, S, cb, walking=t > 43.0, neck=0.42+0.5*pulse(t, 39.6, 40.8, 0.3), ha=0.25*pulse(t, 39.6, 40.8, 0.3),
                   smile=0.7, figs=2 if t < 40.4 else 1)
            if t > 43.0: ch['walk'] = (t-43.0)*0.5
            tortoise(cr, ch, t)
            sleeping(cr, t, S)
            fp = fig_pos(t)
            if fp:
                cr.save(); cr.translate(*fp[0]); cr.rotate(fp[1]); fig(cr, 0, 0, 1.1); cr.restore()
        return frame('meadow', 'late', cam, draw=d)
    S.shot(39.0, 48.5, sh6)
    def sh7(lt, t):
        cam = (FIGP1[0], FIGP1[1]-30, 3.4)
        def d(cr, L):
            sleeping(cr, t, S); fig(cr, FIGP1[0], FIGP1[1], 1.1)
        return frame('meadow', 'late', cam, draw=d, extra_grade=(1, 0.55, 0.25, 0.22*ramp(t, 48.7, 51.0)))
    S.shot(48.5, 52.0, sh7)
    return S

# ======================= SCENE 7 =======================
FIN = 1150
def s7():
    S = Scene('s7', 36.0); c = S.cues
    c.say('s7_01', 0.8); c.say('s7_02', 2.9); c.say('s7_03', 6.5); c.say('s7_04', 10.0); c.say('s7_05', 17.4)
    c.say('s7_06', 19.6); c.say('s7_07', 20.8); c.say('s7_08', 30.3); c.say('crowd_cheer', 32.8, 'CROWD'); c.say('crowd_yay', 33.6, 'CROWD')
    S.music += [(0.0, 9.5, 'tension_soft'), (9.5, 25.0, 'race'), (25.0, 30.2, 'heartbeat'), (32.7, 36.0, 'victory')]
    S.fx(2.9, 'gasp'); S.fx(9.6, 'whoosh_l'); S.fx(22.5, 'whoosh_l'); S.fx(24.4, 'whoosh_l'); S.fx(29.5, 'snap'); S.fx(29.7, 'tumble')
    lb = auto_blinks(15, 37); cb = auto_blinks(16, 37, 3.5); sb = auto_blinks(17, 37)
    FIGP = (SLEEP_HEAD[0]+150, GY+5)
    def sh1(lt, t):
        sit = ramp(t, 1.6, 2.4)
        cam = campath(t, 1.4, 2.6, (SLEEP_HEAD[0]+60, SLEEP_HEAD[1]-30, 2.2), (1420, 830, 1.9))
        def d(cr, L):
            if t < 4.6: fig(cr, FIGP[0], FIGP[1], 1.1)
            if sit < 1:
                P = H_lie(LXS, LYS, LSS, 1, t, S, snore=False)
                st = pulse(t, 0.2, 1.4, 0.3)
                P['arms'] = [(lerp(2.9, 3.1, st), lerp(-2.4, -0.2, st)), (lerp(2.7, 3.0, st), lerp(-2.2, -0.2, st))]
                P['legs'] = [(lerp(0.5, 0.0, st), lerp(-0.6, 0.0, st)), (0.3, -0.5)]
                P['rot'] = lerp(-1.5, 0, sit); P['x'] = lerp(LXS, 1420, sit); P['y'] = lerp(LYS, GY+10, sit)
                P['legs'] = [(lerp(P['legs'][0][0], SIT_LEGS[0][0], sit), lerp(P['legs'][0][1], SIT_LEGS[0][1], sit)), (lerp(0.3, SIT_LEGS[1][0], sit), lerp(-0.5, SIT_LEGS[1][1], sit))]
                P['mouth'] = c.mouth('LAGOS', t); P['eye'] = 0.45; P['flop'] = (0, 1-sit)
                hare(cr, P, t)
            else:
                shock = ramp(t, 2.85, 3.0)
                P = Hp(1420, GY+10, 0.85, 1, t, S, lb, legs=SIT_LEGS, eye=lerp(0.5, 1, shock), wide=1+0.3*shock,
                       ears=(lerp(-0.6, 0.1, shock), lerp(-0.3, 0.2, shock)), look=(0.3, -0.8) if t < 3.8 else (0.4, 0.8), smile=0.0)
                if t > 3.0 and c.mouth('LAGOS', t) < 0.05: P['mouth'] = 0.4
                if t >= 4.6:
                    P['arms'] = [(1.4, -0.9), (0.4, -0.5)]; P['hold'] = lambda cr, hp: fig(cr, hp[0]+4, hp[1]-10, 1.0)
                hare(cr, P, t)
        return frame('meadow', 'sunset', cam, draw=d)
    S.shot(0, 5.5, sh1)
    def sh2(lt, t):
        cam = (1840, 540, 1.0)
        def ob(cr, L):
            ch = T(2275, 300, 0.12, 1, t, S, (), walking=True); ch['walk'] = t*0.5; tortoise(cr, ch, t)
        def scr(cr):
            fig(cr, 260, 900, 6.0)
            cr.save(); cr.translate(150, 1180); capsule(cr, (0, 0), (200, -220), 110, HARE['fur'], 6); cr.restore()
        return frame('meadow', 'sunset', cam, over_back=ob, screen=scr)
    S.shot(5.5, 9.5, sh2)
    PATH = bgs.L_aerial()['path']
    def path_pt(u):
        n = len(PATH)-1; u = clamp(u, 0, 0.999)*n; i = int(u); f = u-i
        return (lerp(PATH[i][0], PATH[i+1][0], f), lerp(PATH[i][1], PATH[i+1][1], f))
    def sh3(lt, t):
        u = ease(lt/5.5)*0.88
        p = path_pt(u); cam = (p[0]*0.4+1200*0.6, p[1]+60, 0.85)
        def d(cr, L):
            for k in range(1, 40):
                q = path_pt(u-k*0.006)
                if q: dust(cr, q[0], q[1], 30+k, 0.5*(1-k/40))
            pn = path_pt(u+0.003); ang = math.atan2(pn[1]-p[1], pn[0]-p[0])
            cr.save(); cr.translate(*p); cr.rotate(ang)
            ell(cr, 0, 0, 34, 18); fill_stroke(cr, HARE['fur'], 3); ell(cr, 30, 0, 16, 13); fill_stroke(cr, HARE['fur'], 3)
            for s_ in (-1, 1): ell(cr, 10, s_*12, 22, 6, s_*0.3); fill_stroke(cr, HARE['fur'], 2.5)
            cr.move_to(-30, 0); cr.line_to(-60, 8*math.sin(t*20)); stroke(cr, HARE['sash'], 6)
            cr.restore()
            for j, (gx, gy) in enumerate(((1300, 1150), (900, 760), (1500, 600))):
                near = math.hypot(p[0]-gx, p[1]-gy) < 300
                dx = (gx-p[0]); off = clamp(1-math.hypot(p[0]-gx, p[1]-gy)/500)*180
                ell(cr, gx+math.copysign(off, dx), gy-off*0.3, 22, 14); fill_stroke(cr, hexc('#EDE6D6'), 3)
        return frame('aerial', 'sunset', cam, draw=d)
    S.shot(9.5, 15.0, sh3)
    def CX(t): return 860+TSPEED*0.9*(t-15.0)*0.9
    CROWD7 = [('goat', 1460, 1170, 0.8, hexc('#EDE6D6')), ('bunny', 1600, 1160, 0.85, None), ('hedgehog', 1720, 1165, 0.85, None),
              ('goat', 1850, 1165, 0.8, hexc('#C9B08A')), ('bunny', 1980, 1170, 0.8, hexc('#A89A8A'))]
    def crowd7(cr, t, cheer=0.3):
        for i, (kind, x, y, s, col) in enumerate(CROWD7):
            P = dict(x=x, y=y, s=s, f=-1, hop=cheer*abs(math.sin(t*8+i))*16, mouth=cheer*0.6*(0.5+0.5*math.sin(t*12+i)), eye=1)
            if col: P['col'] = col
            dict(goat=goat, bunny=bunny, hedgehog=hedgehog)[kind](cr, P, t)
    def spar7(cr, t):
        for i, w in enumerate(('PIP', 'PIM', 'PIO')):
            sparrow(cr, dict(x=1240+i*45, y=1165, s=1.0, who=w, f=-1, mouth=c.mouth(w, t), hop=abs(math.sin(t*8+i))*10, eye=1), t)
    def alepou7(t, **kw):
        P = dict(x=1340, y=1190, s=0.95, f=-1, mouth=c.mouth('ALEPOU', t), smile=0.9, eye=blink_at(t, lb), brow=0.5,
                 arms=[(1.4+0.5*math.sin(t*3), -0.8), (2.3, -0.4)], reed_a=math.pi*0.85)
        P.update(kw); return P
    def sh4(lt, t):
        if t < 18.0:
            cam = (1330, 960, 1.35)
            def d(cr, L):
                finish_posts(cr, FIN); crowd7(cr, t); spar7(cr, t); fox(cr, alepou7(t), t)
            return frame('olive', 'sunset', cam, draw=d)
        if t < 20.4 or 23.7 <= t < 24.4:
            x = CX(t); cam = (x+150, 1060, 1.8 if t < 20.4 else 2.3)
            def d(cr, L):
                finish_posts(cr, FIN)
                ch = T(x, 1190, 0.9, 1, t, S, cb, walking=True, brow=-0.5, sweat=(t*0.6) % 1, eye=0.35 if t > 23.7 else 0.8); ch['walk'] = t*0.5
                tortoise(cr, ch, t)
            return frame('olive', 'sunset', cam, draw=d)
        if t < 22.5:
            x = CX(t); cam = (x+120, 1095, 2.7)
            def d(cr, L):
                ch = T(x, 1190, 0.9, 1, t, S, cb, walking=True, brow=-0.6, eye=0.1, sweat=(t*0.6) % 1); ch['walk'] = t*0.5
                tortoise(cr, ch, t)
            return frame('olive', 'sunset', cam, draw=d)
        x = 500+1700*((t-22.5) if t < 23.7 else (t-24.4)); cam = (x+120, 720, 1.4)
        def d(cr, L):
            P = H_run(x, 960, 0.9, 1, t, t*4.2, brow=-0.8, teeth=True, smile=-0.3, mouth=0.0)
            hare(cr, P, t); speed_lines(cr, x-300, 760, 14, 500, 0.7, int(t*10))
            for j in range(1, 6): dust(cr, x-120*j, 980, 40+10*j, 0.5*(1-j/6))
        return frame('hill', 'sunset', cam, draw=d)
    S.shot(15.0, 25.0, sh4)
    # slow motion finish
    def chel_fin(t):
        return 992-TSPEED*0.9*0.25*(27.9-t) if t < 28.0 else (992+TSPEED*0.9*0.25*0.1 if t < 29.5 else 992+(t-29.5)*20)
    def lag_fin(t):
        if t < 28.0: return lerp(250, 975, ease((t-25.0)/3.0)*0.6+((t-25.0)/3.0)*0.4)
        if t < 29.5: return 975
        return 975+(t-29.5)*700
    def sh5(lt, t):
        cam = (1060, 1060, 1.65)
        frz = 28.0 <= t < 29.5
        tt = 28.0 if frz else t
        def d(cr, L):
            snapped = t >= 29.5
            rib = clamp((chel_fin(tt)+150-FIN)/20)
            finish_posts(cr, FIN, ribbon=rib, snapped=snapped)
            ch = T(chel_fin(tt), 1190, 0.9, 1, tt, S, (), walking=not frz, eye=0.1, brow=-0.6, neck=0.75)
            ch['walk'] = tt*0.5*0.25
            tortoise(cr, ch, tt)
            x = lag_fin(tt)
            if t < 29.5:
                P = H_run(x, 1240, 0.95, 1, tt, 0.25+tt*0.15, air=55, lean=1.35, arms=[(2.2, -0.15), (1.6, -0.4)], legs=[(-1.2, -0.3), (-0.9, -0.5)],
                          brow=-0.7, mouth=0.5, smile=-0.2)
            else:
                k = ramp(t, 29.5, 30.0)
                P = H_run(x, 1240, 0.95, 1, t, 0.3, air=55*(1-k), lean=1.35+k*1.2, arms=[(2.2, -0.15), (1.6, -0.4)], legs=[(-1.2, -0.3), (-0.9, -0.5)], eye=0.0)
            hare(cr, P, tt)
        return frame('olive', 'sunset', cam, draw=d, extra_grade=(1, 1, 1, 0.12) if frz else None, flash=0.5*pulse(t, 27.95, 28.25, 0.05))
    S.shot(25.0, 30.0, sh5)
    def sh6a(lt, t):
        cam = (1310, 905, 2.6)
        def d(cr, L):
            finish_posts(cr, FIN, snapped=True)
            up = ramp(t, 32.0, 32.3)
            sq = 0.9*(1-ramp(t, 31.6, 31.9))
            fox(cr, alepou7(t, eye=lerp(1, 0.35, sq), brow=-0.4*sq+0.6*(1-sq), hd=0.15*sq, arms=[(lerp(1.0, 2.9, up), -0.3), (2.3, -0.4)], reed_a=lerp(math.pi*0.6, math.pi*0.98, up),
                                flag=True), t)
        return frame('olive', 'sunset', cam, draw=d)
    S.shot(30.0, 32.7, sh6a)
    def sh6b(lt, t):
        cam = campath(lt, 0, 3.3, (1350, 1060, 1.05), (1400, 930, 0.9))
        def d(cr, L):
            finish_posts(cr, FIN, snapped=True)
            crowd7(cr, t, cheer=1.0)
            fox(cr, alepou7(t, arms=[(2.9, -0.3), (2.3, -0.4)], reed_a=math.pi*0.98, flag=True, mouth=0.4, smile=1), t)
            ch = T(1040, 1190, 0.9, 1, t, S, cb, happy=True, smile=1, neck=0.6, tear=True)
            tortoise(cr, ch, t)
            cr.move_to(1050, 1080); cr.curve_to(1080, 1050, 1120, 1060, 1150, 1100); stroke(cr, hexc('#B8432F'), 7)
            hare(cr, H_lie(1270, 1150, 0.9, 1, t, S, snore=False, eye=0.0, mouth=0.2, flop=(1, 1), rot=-1.3), t)
            for i, w in enumerate(('PIP', 'PIM', 'PIO')):
                sparrow(cr, dict(x=1000+i*70+math.sin(t*3+i)*30, y=850+math.sin(t*4+i*2)*30, s=1.0, who=w, f=1, flap=math.sin(t*30+i), mouth=0.5), t)
            leaf_confetti(cr, t, 32.8, 5, (700, 500, 2100, 1300), 80)
        return frame('olive', 'sunset', cam, draw=d)
    S.shot(32.7, 36.0, sh6b)
    return S

# ======================= SCENE 8 =======================
LANT2 = [(980, 760), (1180, 720), (1680, 740), (1880, 780), (2080, 760)]
def s8():
    S = Scene('s8', 41.5); c = S.cues
    c.say('s8_01', 1.5); c.say('s8_02', 3.4); c.say('s8_03', 9.3); c.say('s8_04', 11.6); c.say('s8_05', 13.0); c.say('s8_06', 16.3)
    c.say('lagos_laugh', 17.0); c.say('chel_laugh', 17.3); c.say('crowd_yay', 19.4, 'CROWD'); c.say('s8_07', 26.8); c.say('s8_08', 34.6)
    S.music += [(0.0, 17.0, 'theme_soft'), (17.0, 24.0, 'village_dance'), (24.0, 37.5, 'theme'), (37.5, 41.5, 'end_sting')]
    S.fx(0.0, 'crickets_on'); S.fx(36.7, 'puff'); S.fx(37.2, 'hoot', 0.6)
    lb = auto_blinks(18, 42); cb = auto_blinks(19, 42, 3.6); gb = [28.5, 31.6]
    LXr, LYr = 1220, 1175
    def cx8(t): return lerp(1650, 1530, ramp(t, 0.0, 3.0))
    def lagos8(t, **kw):
        P = Hp(LXr, LYr, 0.85, 1, t, S, lb, legs=SIT_LEGS, ears=(-1.0, -0.8), look=(0.4, 0.7), smile=0.1,
               arms=[(1.3, -1.0), (0.5, -0.6)])
        P['hold'] = lambda cr, hp: fig(cr, hp[0]+4, hp[1]-10, 1.0)
        P.update(kw); return P
    def chel8(t, **kw):
        ch = T(cx8(t), 1190, 0.85, -1, t, S, cb, walking=t < 3.0, smile=0.75, look=(0.3, 0.1))
        if t < 3.0: ch['walk'] = t*0.5
        ch.update(kw); return ch
    def scene_props(cr, t):
        lanterns(cr, t, LANT2); fireflies(cr, t, 8, (800, 700, 2200, 1150), 30)
    def sh1(lt, t):
        cam = (1370, 1030, 1.6)
        def d(cr, L):
            scene_props(cr, t)
            tortoise(cr, chel8(t), t); hare(cr, lagos8(t, look=(0.4, 0.8) if t < 3.3 else (0.7, 0.0)), t)
        return frame('olive', 'night', cam, draw=d, extra_grade=(1, 0.6, 0.25, 0.06))
    S.shot(0, 9.0, sh1)
    def sh2(lt, t):
        if t < 11.3: cam = (LXr+40, 960, 2.5)
        elif t < 12.8: cam = (1440, 1080, 2.5)
        else: cam = (1370, 1030, 1.75)
        rise = ramp(t, 12.5, 14.0)
        offer = ramp(t, 14.3, 14.9)
        laugh = pulse(t, 17.0, 19.0, 0.2)
        def d(cr, L):
            scene_props(cr, t)
            ch = chel8(t, neck=0.42+0.45*pulse(t, 15.4, 16.2, 0.2), brow=0.6*pulse(t, 16.2, 17.0, 0.1), happy=laugh > 0.3)
            if laugh: ch['mouth'] = max(ch['mouth'], 0.5*abs(math.sin(t*14)))
            tortoise(cr, ch, t)
            P = lagos8(t, ears=(lerp(-1.0, -0.2, ramp(t, 9.8, 11.0)), lerp(-0.8, 0.0, ramp(t, 9.8, 11.0))), look=(0.4, 0.7) if t < 11.0 else (0.7, 0),
                       smile=lerp(0.1, 1.0, ramp(t, 10.5, 11.2)))
            if offer > 0:
                P['arms'] = [(lerp(1.3, 1.55, offer), lerp(-1.0, -0.15, offer)), (0.5, -0.6)]; P['hold'] = None
                P['ears'] = (lerp(-0.2, 0.05, offer), lerp(0.0, 0.1, offer))
            if laugh > 0: P['happy'] = laugh > 0.3; P['mouth'] = max(P['mouth'], 0.6*abs(math.sin(t*15))); P['y'] = LYr-6*abs(math.sin(t*15))*laugh
            hare(cr, P, t)
            if t >= 17.3:
                for i, w in enumerate(('PIP', 'PIM', 'PIO')):
                    k = ramp(t, 17.3+i*0.15, 17.9+i*0.15)
                    tx_, ty_ = LXr+20+i*38, LYr-370+(i == 1)*(-30)
                    sparrow(cr, dict(x=lerp(tx_-400, tx_, k), y=lerp(ty_-300, ty_, k), s=0.85, who=w, f=1, flap=math.sin(t*30)*(1-k), mouth=0.4*laugh, eye=1), t)
        return frame('olive', 'night', cam, draw=d, extra_grade=(1, 0.6, 0.25, 0.06))
    S.shot(9.0, 19.0, sh2)
    DANCE = [('goat', hexc('#EDE6D6')), ('bunny', None), ('hedgehog', None), ('goat', hexc('#C9B08A')), ('bunny', hexc('#A89A8A')), ('goat', hexc('#E8DCC8'))]
    def sh3(lt, t):
        cam = campath(lt, 0, 5, (1500, 960, 0.92), (1520, 940, 0.95))
        def d(cr, L):
            scene_props(cr, t)
            items = []
            for i, (kind, col) in enumerate(DANCE):
                a = t*0.9+i*2*math.pi/len(DANCE); x = 1600+430*math.cos(a); y = 1200+55*math.sin(a)
                items.append((y, kind, col, x, -1 if math.sin(a) > 0 else 1, i))
            hare(cr, lagos8(t, ears=(0.0, 0.1), smile=1, look=(0.7, 0), happy=True), t)
            tortoise(cr, chel8(t, smile=1, happy=True), t)
            for y, kind, col, x, f, i in sorted(items):
                P = dict(x=x, y=y, s=0.8+0.1*(y-1145)/110, f=f, hop=abs(math.sin(t*7+i))*20, mouth=0.4, eye=1)
                if col: P['col'] = col
                dict(goat=goat, bunny=bunny, hedgehog=hedgehog)[kind](cr, P, t)
        return frame('olive', 'night', cam, draw=d, extra_grade=(1, 0.6, 0.25, 0.06))
    S.shot(19.0, 24.0, sh3)
    def sh4a(lt, t):
        cam = campath(lt, 0, 2.5, (1470, 1080, 1.0), (1470, 860, 2.0))
        def d(cr, L):
            scene_props(cr, t)
            glow(cr, 1500, 880, 140, (1, 0.7, 0.3), 0.5)
            owl(cr, dict(x=1450, y=905, s=0.55, eye=1, look=(0, 0.5)), t); lamp(cr, 1500, 903, 0.45, 1, t)
        return frame('olive', 'night', cam, draw=d)
    S.shot(24.0, 26.5, sh4a)
    LAMP = (1300, 902)
    def sh4b(lt, t):
        cam = campath(t, 26.5, 34.0, (1110, 690, 1.25), (1100, 620, 1.6))
        blow = pulse(t, 36.2, 37.0, 0.15); out = t >= 36.9
        gest = pulse(t, 28.0, 30.5, 0.4)
        def d(cr, L):
            if not out: glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35)
            P = dict(x=1100, y=905, s=2.4, eye=blink_at(t, gb), mouth=max(c.mouth('GLAFKA', t), 0.6*blow), tilt=0.05*osc(t, 0.35)+0.25*blow,
                     wings=(0.0, 0.9*gest), look=(0.6*blow, 0.3*blow))
            if 33.9 <= t < 34.5: P['wink'] = 1-math.sin(math.pi*(t-33.9)/0.6)
            owl(cr, P, t)
            if not out: lamp(cr, LAMP[0], LAMP[1], 1.7, 1-0.6*ramp(t, 36.4, 36.9), t)
            else:
                lamp(cr, LAMP[0], LAMP[1], 1.7, 0, t)
                k = clamp((t-36.9)/1.2)
                for j in range(6):
                    ell(cr, LAMP[0]+62+math.sin(j+t*2)*10*k, LAMP[1]-60-j*18-k*60, 6+j*2, 4+j, 0); fill(cr, (0.8, 0.8, 0.85, 0.35*(1-k)))
        return frame('hollow', 'night', cam, draw=d, extra_grade=(0, 0, 0.05, 0.55*ramp(t, 36.9, 37.2)) if True else None, fade=ramp(t, 37.0, 37.5))
    S.shot(26.5, 37.5, sh4b)
    def sh5(lt, t):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, 1080); cr = cairo.Context(s)
        title_card(cr, ramp(lt, 0.2, 1.2)*(1-ramp(lt, 3.2, 4.0)))
        return s
    S.shot(37.5, 41.5, sh5)
    return S
