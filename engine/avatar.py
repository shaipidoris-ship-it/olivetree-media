from kit import *
S = 1080
def make(path, bg='night'):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S); cr = cairo.Context(s)
    g = cairo.RadialGradient(S/2, S*0.55, 50, S/2, S/2, S*0.75)
    if bg == 'night':
        g.add_color_stop_rgb(0, 0.28, 0.27, 0.52); g.add_color_stop_rgb(1, 0.06, 0.07, 0.2)
    else:
        g.add_color_stop_rgb(0, 0.99, 0.86, 0.55); g.add_color_stop_rgb(1, 0.85, 0.48, 0.25)
    cr.set_source(g); cr.paint()
    rnd = random.Random(2)
    if bg == 'night':
        for _ in range(90):
            x, y = rnd.uniform(0, S), rnd.uniform(0, S*0.6); ell(cr, x, y, 2, 2); fill(cr, (1, 1, 0.9, rnd.uniform(0.3, 0.9)))
    # hollow ring (tree bark) behind owl
    ell(cr, S/2, S*0.53, 400, 430); fill(cr, (0.36, 0.27, 0.2, 1))
    ell(cr, S/2, S*0.55, 350, 380); fill(cr, (0.13, 0.09, 0.06, 1))
    glow(cr, S*0.72, S*0.72, 420, (1, 0.7, 0.3), 0.45)
    # olive wreath around
    cr.save(); cr.translate(S/2, S*0.53)
    for side in (-1, 1):
        for k in range(16):
            a = math.pi/2 + side*(0.35+k*0.155); r = 420
            x, y = math.cos(a)*r, math.sin(a)*r*1.02
            ell(cr, x, y, 34, 13, a+side*0.9); fill_stroke(cr, hexc('#7A8B4F') if k % 2 else hexc('#93AA55'), 3)
            if k % 4 == 2: ell(cr, x*0.93, y*0.93, 13, 16); fill_stroke(cr, hexc('#3F3A5A'), 3)
    cr.restore()
    # ledge
    ell(cr, S/2, S*0.86, 330, 50); fill_stroke(cr, hexc('#7D6650'), 6)
    owl(cr, dict(x=S/2-20, y=S*0.86, s=2.75, eye=1, look=(0.05, 0.1), tilt=-0.06, wings=(0, 0.35), mouth=0.0), 0)
    lamp(cr, S*0.73, S*0.855, 1.9, 1, 0.3)
    # subtle vignette
    g = cairo.RadialGradient(S/2, S/2, S*0.35, S/2, S/2, S*0.72)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.35); cr.set_source(g); cr.paint()
    s.write_to_png(path)
make('out/avatar_night.png', 'night'); make('out/avatar_warm.png', 'warm')
