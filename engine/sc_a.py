from kit import *

# ======================= SCENE 1 =======================
def s1():
    S = Scene('s1', 34.0); c = S.cues
    c.say('s1_01', 13.6); c.say('s1_02', 16.0); c.say('s1_03', 23.3); c.say('s1_04', 27.5)
    S.music.append((0.0, 34.0, 'theme'))
    S.fx(1.0, 'crickets_on'); S.fx(9.6, 'flint'); S.fx(10.0, 'flame'); S.fx(4.0, 'hoot', 0.35)
    blinks = [11.6, 19.4, 25.0, 30.6]
    def gl(t, **kw):
        P = dict(x=1100, y=905, s=2.4, eye=blink_at(t, blinks), mouth=c.mouth('GLAFKA', t), tilt=0.05*osc(t, 0.35))
        P.update(kw); return P
    LAMP = (1300, 902)
    def lampdraw(cr, t, lit): lamp(cr, LAMP[0], LAMP[1], 1.7, lit, t)

    def sh1(lt, t):
        cam = campath(lt, 0, 8, (1500, 1330, 1.05), (1500, 850, 0.82))
        def d(cr, L):
            fireflies(cr, t, 1, (900, 700, 2100, 1250), 40)
            ell(cr, 1470, 880, 8, 8); fill(cr, (1, 0.8, 0.4, 0.0))
        return frame('olive', 'blue', cam, draw=d, fade=1-ramp(lt, 0, 1.5))
    S.shot(0, 8, sh1)

    def sh2(lt, t):
        cam = campath(lt, 0, 5, (1100, 650, 0.92), (1150, 700, 1.12))
        lit = ramp(t, 10.0, 10.5)
        def d(cr, L):
            if lit > 0: glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35*lit)
            owl(cr, gl(t, look=(0.7, 0.4), tilt=0.12), t)
            lampdraw(cr, t, lit)
            if 9.5 <= t < 9.75:
                for k in range(8):
                    a = k*0.8; cr.move_to(LAMP[0]+40, LAMP[1]-50); cr.line_to(LAMP[0]+40+math.cos(a)*30, LAMP[1]-50+math.sin(a)*30); stroke(cr, (1, 0.9, 0.5, 1), 3)
        return frame('hollow', 'blue', cam, draw=d, extra_grade=(1, 0.6, 0.3, 0.06*lit))
    S.shot(8, 13, sh2)

    def sh3(lt, t):
        cam = (1120, 680, 1.25)
        sw = lerp(0.7, 0.0, ramp(t, 13.0, 13.5))
        rem = pulse(t, 21.0, 22.8, 0.3)
        def d(cr, L):
            glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35)
            owl(cr, gl(t, swivel=sw*0.5, look=(sw, 0), wings=(0.2*rem, 1.1*rem), wide=1+0.15*pulse(t, 13.4, 14.4)), t)
            lampdraw(cr, t, 1)
        return frame('hollow', 'blue', cam, draw=d, extra_grade=(1, 0.6, 0.3, 0.06))
    S.shot(13, 23.1, sh3)

    def sh4(lt, t):
        cam = campath(t, 23.1, 26.0, (1120, 680, 1.25), (1110, 600, 1.8))
        if t > 31.0: cam = campath(t, 31.0, 33.6, cam, (LAMP[0]+61, LAMP[1]-50, 7.0), ease)
        lean = pulse(t, 23.3, 27.0, 0.4)
        laugh = pulse(t, 27.5, 28.6, 0.1)
        def d(cr, L):
            glow(cr, LAMP[0]+60, LAMP[1]-60, 700, (1, 0.7, 0.3), 0.35)
            P = gl(t, tilt=0.18*lean+0.06*math.sin(t*30)*laugh, wings=(0.5*laugh, 0.5*laugh), y=905-8*laugh*abs(math.sin(t*20)))
            if 25.9 <= t < 26.5: P['wink'] = 1-math.sin(math.pi*(t-25.9)/0.6)
            if laugh > 0.3: P['happy'] = True
            owl(cr, P, t); lampdraw(cr, t, 1)
        return frame('hollow', 'blue', cam, draw=d, extra_grade=(1, 0.6, 0.3, 0.06), flash=ramp(t, 32.6, 33.9))
    S.shot(23.1, 34.0, sh4)
    return S

# ======================= SCENE 2 =======================
FX = 1600            # fountain x
def s2():
    S = Scene('s2', 55.5); c = S.cues
    c.say('s2_01', 11.2); c.say('s2_02', 13.0); c.say('s2_03', 14.6); c.say('s2_04', 15.6)
    c.say('s2_05', 18.6); c.say('s2_06', 24.2); c.say('s2_07', 27.1); c.say('s2_08', 30.4)
    c.say('s2_09', 33.6); c.say('crowd_laugh', 36.6, 'CROWD'); c.say('sparrows_ooh', 38.3, 'SPARROWS')
    c.say('s2_10', 40.3); c.say('crowd_gasp', 45.5, 'CROWD'); c.say('s2_11', 48.8); c.say('s2_12', 49.7); c.say('s2_13', 50.6)
    c.say('s2_14', 52.6)
    S.music += [(0.0, 33.4, 'lagos'), (36.6, 52.0, 'lagos_soft'), (52.2, 55.5, 'sting')]
    S.fx(0.0, 'market_on'); S.fx(5.8, 'whoosh_s'); S.fx(6.3, 'whoosh_m'); S.fx(7.4, 'whoosh_m'); S.fx(8.5, 'whoosh_m'); S.fx(9.8, 'catch')
    S.fx(28.9, 'whoosh_m'); S.fx(29.6, 'whoosh_m'); S.fx(52.2, 'pop'); S.fx(55.0, 'whoosh_l'); S.fx(46.0, 'chew', 0.6)
    lb = auto_blinks(2, 56); cb = auto_blinks(3, 56, 4.0); sb = auto_blinks(4, 56)
    GY = 1000
    SPAR = [(1490, 535), (1570, 530), (1650, 535)]
    CROWD = [('goat', 2150, 795, 0.8, hexc('#EDE6D6')), ('bunny', 2330, 795, 0.9, None), ('goat', 2520, 795, 0.85, hexc('#C9B08A')),
             ('hedgehog', 2700, 795, 0.9, None), ('bunny', 2830, 795, 0.85, hexc('#A89A8A')), ('goat', 3010, 795, 0.8, hexc('#E8DCC8'))]
    def crowd(cr, t, laugh=0.0, gasp=0.0):
        for i, (kind, x, y, s, col) in enumerate(CROWD):
            hop = laugh*abs(math.sin(t*9+i))*14
            P = dict(x=x, y=y, s=s, f=-1, hop=hop, mouth=max(laugh*(0.5+0.5*math.sin(t*14+i)), gasp*0.8), eye=blink_at(t, sb[i::3]))
            if col: P['col'] = col
            if gasp > 0.3: P['wide'] = 1.25
            dict(goat=goat, bunny=bunny, hedgehog=hedgehog)[kind](cr, P, t)
        cat(cr, dict(x=2960, y=795, s=0.9, eye=ramp(t, 37.2, 37.5)*(1-ramp(t, 39.0, 39.3))), t)
    def sparrows(cr, t, ooh=0.0, **kw):
        for i, w in enumerate(('PIP', 'PIM', 'PIO')):
            x, y = SPAR[i]; m = c.mouth(w, t)
            late = 0.25 if w == 'PIO' else 0
            sparrow(cr, dict(x=x, y=y, s=1.25, who=w, f=-1, mouth=max(m, ooh), hop=abs(math.sin((t-late)*7))*6*kw.get('excite', 0),
                             eye=blink_at(t, sb[i::2]), look=(-0.6, 0.2)), t)
    # Lagos laps around the fountain
    def lap_pos(t):
        th = 2*math.pi*3*ease((t-6.2)/3.3)
        x = FX - 380*math.cos(th); y = GY+20+55*math.sin(th)
        front = math.sin(th) > -0.2
        dxdt = math.sin(th); return x, y, front, (1 if dxdt >= 0 else -1), th
    def goat_apple(cr, t):
        goat(cr, dict(x=2050, y=GY+10, s=0.95, f=-1, ht=-0.3*pulse(t, 5.4, 6.2), mouth=0.3*pulse(t, 9.6, 10.4)), t)
    def apple_pos(t):
        if t < 5.8: return None
        if t < 9.8:
            k = (t-5.8)/4.0; kk = 0.5-0.5*math.cos(math.pi*k)   # slow apex
            x = lerp(1990, 1400, kk); y = lerp(880, 880, k)-math.sin(math.pi*k)*520
            return (x, y)
        return None
    def sh1(lt, t):
        cam = campath(lt, 0, 5, (1150, 640, 0.95), (1700, 640, 0.95))
        def d(cr, L):
            crowd(cr, t); sparrows(cr, t); goat_apple(cr, t)
            hare(cr, Hp(1380, GY+10, 0.82, 1, t, S, lb, air=abs(math.sin(t*4))*6), t)
        return frame('square', 'morning', cam, draw=d, flash=1-ramp(lt, 0, 0.8))
    S.shot(0, 5, sh1)

    def sh2(lt, t):
        cam = (1620, 640, 1.0); shake = (math.sin(t*40)*6*pulse(t, 6.2, 9.5), 0)
        def d(cr, L):
            sparrows(cr, t, excite=pulse(t, 6.2, 10)); goat_apple(cr, t); crowd(cr, t)
            ap = apple_pos(t)
            x, y, front, f, th = lap_pos(t) if 6.2 <= t < 9.5 else (1380, GY+10, True, 1, 0)
            if 6.2 <= t < 9.5:
                for k in range(1, 7):
                    xx, yy, fr, _, _ = lap_pos(t-k*0.04)
                    if fr: dust(cr, xx, yy+10, 40, 0.5*(1-k/7))
                if front: hare(cr, H_run(x, y, 0.8, f, t, t*3.2), t)
            else:
                k = ramp(t, 9.5, 9.7)
                P = Hp(1380, GY+10, 0.82, 1, t, S, lb, air=abs(math.sin(t*4))*6)
                up = pulse(t, 9.55, 10.6, 0.15)
                P['arms'] = [(lerp(0.3, 2.6, up), lerp(-0.5, -0.2, up)), (0.15, -0.4)]
                if t >= 9.8: P['hold'] = lambda cr, hp: apple(cr, hp[0], hp[1]-8, 1.0)
                P['eye'] = 1; P['look'] = (0.2, -0.8*up)
                hare(cr, P, t)
            if ap: apple(cr, ap[0], ap[1], 1.1)
        return frame('square', 'morning', cam, draw=d, shake=shake)
    S.shot(5, 11, sh2)

    def sh3(lt, t):
        cam = campath(lt, 0, 6.9, (1450, 720, 1.4), (1450, 700, 1.48))
        bow = pulse(t, 15.5, 17.2, 0.35)
        def d(cr, L):
            sparrows(cr, t, excite=1.0 if t < 15.4 else 0.2)
            P = Hp(1380, GY+10, 0.95, 1, t, S, lb, air=abs(math.sin(t*4))*5*(1-bow))
            P['lean'] = 0.55*bow; P['arms'] = [(lerp(0.3, 1.6, bow), lerp(-0.5, -1.4, bow)), (lerp(0.15, -0.8, bow), -0.3)]
            P['ears'] = (-0.25-0.7*bow, -0.05-0.8*bow)
            P['hold'] = lambda cr, hp: apple(cr, hp[0], hp[1]-8, 1.0)
            P['eye'] = min(P['eye'], 0.55+0.45*(1-pulse(t, 11.0, 15.4))); P['smile'] = 1; P['teeth'] = bow < 0.2
            hare(cr, P, t)
        return frame('square', 'morning', cam, draw=d)
    S.shot(11, 17.9, sh3)

    # Chelona walking in; Lagos teasing and orbiting
    CX0 = 870
    def chel_x(t):
        return CX0+TSPEED*0.9*clamp(t-17.9, 0, 31.9-17.9)
    def orbit(t):
        th = 2*math.pi*2*ease((t-28.9)/1.4); cx = chel_x(t)+40
        return cx+260*math.cos(th), GY+30+45*math.sin(th), math.sin(th) > -0.1, (1 if -math.sin(th) >= 0 else -1)
    def lagos_x(t):
        if t < 27.0: return 1380-ramp(t, 18.0, 19.0)*40
        if t < 28.9: return 1340
        return chel_x(t)+300
    def sh4(lt, t):
        cam = campath(lt, 0, 14.1, (1130, 760, 1.4), (1290, 760, 1.4))
        walking = t < 31.9
        def d(cr, L):
            sparrows(cr, t)
            ch = T(chel_x(t), GY+30, 0.9, 1, t, S, cb, walking=walking)
            if walking: ch['walk'] = (t-17.9)*0.5
            if 28.9 <= t < 30.3:
                x, y, front, f = orbit(t)
                if not front: hare(cr, H_run(x, y, 0.8, f, t, t*3.2), t)
                tortoise(cr, ch, t)
                if front: hare(cr, H_run(x, y, 0.8, f, t, t*3.2), t)
                for k in range(1, 6):
                    xx, yy, fr, _ = orbit(t-k*0.035); dust(cr, xx, yy+10, 34, 0.45*(1-k/6))
            else:
                tortoise(cr, ch, t)
                P = Hp(lagos_x(t), GY+10, 0.9, -1, t, S, lb, air=abs(math.sin(t*4))*6)
                if 27.1 <= t < 28.9:   # pointing to the stall
                    P['arms'] = [(2.0, -0.2), (0.15, -0.4)]; P['f'] = 1
                if t >= 30.3:
                    P['arms'] = [(0.8, -2.2), (0.6, -2.0)]; P['lean'] = -0.08; P['eye'] = min(P['eye'], 0.6)
                P['look'] = (0.6, 0.2)
                hare(cr, P, t)
        return frame('square', 'morning', cam, draw=d)
    S.shot(17.9, 32.0, sh4)

    CXS = chel_x(32.0)
    def sh5a(lt, t):
        cam = (CXS+95, GY-55, 3.6)
        def d(cr, L):
            e = 1.0
            if 32.3 <= t < 33.3: e = 1-math.sin(math.pi*(t-32.3)/1.0)
            tortoise(cr, T(CXS, GY+30, 0.9, 1, t, S, (), eye=e, smile=0.75, brow=0.3*ramp(t, 33.5, 33.8)), t)
        return frame('square', 'morning', cam, draw=d)
    S.shot(32.0, 35.0, sh5a)
    def sh5b(lt, t):
        LX = CXS+300
        cam = (LX+10, GY-300, 2.4)
        def d(cr, L):
            ears = (0.05+0.15*pulse(t, 35.55, 35.7, 0.05), 0.12+0.2*pulse(t, 35.95, 36.1, 0.05))
            P = Hp(LX, GY+10, 0.9, -1, t, S, (), air=26, ears=ears, eye=1, wide=1.15, mouth=0.15, smile=0.0)
            P['arms'] = [(0.8, -2.2), (0.6, -2.0)]
            hare(cr, P, t)
        return frame('square', 'morning', cam, draw=d)
    S.shot(35.0, 36.5, sh5b)

    def sh6(lt, t):
        cam = (2250, 680, 0.95); shake = (0, math.sin(t*30)*4*pulse(t, 36.6, 38.0))
        def d(cr, L):
            sparrows(cr, t, ooh=pulse(t, 38.3, 39.0, 0.1)*0.9)
            crowd(cr, t, laugh=pulse(t, 36.6, 38.2, 0.15))
            tortoise(cr, T(CXS, GY+30, 0.9, 1, t, S, cb), t)
            P = Hp(CXS+300, GY+10, 0.9, -1, t, S, lb); P['arms'] = [(0.8, -2.2), (0.6, -2.0)]; P['ears'] = (-0.1, -0.6*pulse(t, 37, 40))
            hare(cr, P, t)
        return frame('square', 'morning', cam, draw=d, shake=shake)
    S.shot(36.5, 40.0, sh6)

    def sh7(lt, t):
        z = lerp(1.7, 1.85, ramp(lt, 0, 12))
        wx = (t-55.0)/0.5
        cam = (CXS+170+(2400*ease(wx) if t > 55.0 else 0), 790, z)
        lean_in = pulse(t, 40.3, 45.0, 0.4)
        def d(cr, L):
            # Alepou pops up between them
            if t >= 52.2:
                k = ramp(t, 52.2, 52.55); ov = math.sin(clamp((t-52.55)/0.3)*math.pi)*20
                fx_y = lerp(GY+520, GY+5, k)-ov
                fox(cr, dict(x=CXS+235, y=fx_y, s=0.92, f=1, arms=[(2.4, -0.5), (-0.6, -0.4)], mouth=S.cues.mouth('ALEPOU', t),
                             smile=0.9, brow=0.6, eye=1, reed=False, look=(0.3, -0.3)), t)
            chew = 46.0 <= t < 48.6
            ch = T(CXS, GY+30, 0.9, 1, t, S, cb, chew=chew, mouth=max(S.cues.mouth('CHELONA', t), 0.15 if chew else 0))
            tortoise(cr, ch, t)
            if 45.6 <= t < 46.1: fig(cr, CXS+(112+0.42*48)*0.9+34, GY+30-80*0.9+12, 0.7)
            P = Hp(CXS+300, GY+10, 0.9, -1, t, S, lb, air=abs(math.sin(t*4))*5)
            P['lean'] = 0.3*lean_in
            if 40.3 <= t < 45.0:
                pt = pulse(t, 42.6, 45.0, 0.3)
                P['arms'] = [(lerp(0.3, -2.4, pt), lerp(-0.5, 0.2, pt)), (0.15, -0.4)]
                P['f'] = -1
            jd = pulse(t, 49.6, 50.6, 0.08)
            P['ears'] = (lerp(P['ears'][0], 0.15, jd), lerp(P['ears'][1], 0.25, jd)); P['wide'] = 1+0.25*jd
            if jd > 0.5: P['eye'] = 1
            if t >= 52.3: P['ears'] = (0.1, 0.2); P['wide'] = 1.2; P['eye'] = 1; P['look'] = (-0.3, -0.6)
            hare(cr, P, t)
        def scr(cr):
            if t > 55.0:
                a = ramp(t, 55.0, 55.25)
                for i in range(40):
                    y = (i*53) % H; cr.move_to(0, y); cr.line_to(W, y); stroke(cr, (1, 1, 1, 0.15*a), 30)
        return frame('square', 'morning', cam, draw=d, screen=scr)
    S.shot(40.0, 55.5, sh7)
    return S
