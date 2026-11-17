from core import *
import bgs
import numpy as np

PAR = {'back': 0.45, 'main': 1.0, 'fg': 1.3}
GRADE = {'blue': (0.25, 0.25, 0.6, 0.14), 'night': (0.08, 0.1, 0.35, 0.22), 'sunset': (1.0, 0.55, 0.25, 0.12),
         'late': (1.0, 0.75, 0.4, 0.08), 'noon': (1, 1, 0.92, 0.05), 'afternoon': (1, 0.9, 0.7, 0.05), 'morning': (1, 0.95, 0.85, 0.03)}

_grain = None
def grain():
    global _grain
    if _grain is None:
        rng = np.random.default_rng(3)
        n = rng.integers(0, 255, (H, W), dtype=np.uint8)
        a = (rng.random((H, W)) < 0.5).astype(np.uint8)*10
        arr = np.zeros((H, W, 4), dtype=np.uint8)
        v = (n.astype(np.uint16)*a//255).astype(np.uint8)
        arr[..., 0] = v; arr[..., 1] = v; arr[..., 2] = v; arr[..., 3] = a
        s = cairo.ImageSurface.create_for_data(memoryview(arr).cast('B'), cairo.FORMAT_ARGB32, W, H, W*4)
        _grain = (s, arr)
    return _grain[0]

def cam_xform(cr, cam, p, ref):
    cx, cy, z = cam
    ex = ref[0]+(cx-ref[0])*p; ey = ref[1]+(cy-ref[1])*p
    cr.translate(W/2, H/2); cr.scale(z, z); cr.translate(-ex, -ey)

def frame(loc, tod, cam, draw=None, over=None, layers=('back', 'main', 'fg'), grade=True, shake=(0, 0), extra_grade=None, fade=0.0, flash=0.0, over_back=None, screen=None):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(s)
    cr.set_source_rgb(0, 0, 0); cr.paint()
    L = bgs.get(loc, tod); ref = L['ref']
    cw, ch = L['size']; z = cam[2]; hw, hh = W/2/z, H/2/z
    cx = clamp(cam[0]+shake[0], hw, cw-hw) if cw > 2*hw else cw/2
    cy = clamp(cam[1]+shake[1], hh, ch-hh) if ch > 2*hh else ch/2
    cam = (cx, cy, z)
    for name in ('back', 'main'):
        if name in layers:
            cr.save(); cam_xform(cr, cam, PAR[name], ref); cr.set_source_surface(L['surf'][name], 0, 0)
            cr.get_source().set_filter(cairo.FILTER_GOOD); cr.paint(); cr.restore()
    if over_back:
        cr.save(); cam_xform(cr, cam, PAR['back'], ref); over_back(cr, L); cr.restore()
    if draw:
        cr.save(); cam_xform(cr, cam, 1.0, ref); draw(cr, L); cr.restore()
    if 'fg' in layers:
        cr.save(); cam_xform(cr, cam, PAR['fg'], ref); cr.set_source_surface(L['surf']['fg'], 0, 0); cr.paint(); cr.restore()
    if over:
        cr.save(); cam_xform(cr, cam, 1.0, ref); over(cr, L); cr.restore()
    if screen: screen(cr)
    if grade and tod in GRADE:
        cr.set_source_rgba(*GRADE[tod]); cr.paint()
    if extra_grade: cr.set_source_rgba(*extra_grade); cr.paint()
    g = cairo.RadialGradient(W/2, H/2, H*0.45, W/2, H/2, H*1.05)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.08, 0.04, 0.02, 0.45)
    cr.set_source(g); cr.paint()
    cr.set_source_surface(grain(), 0, 0); cr.paint()
    if flash > 0: cr.set_source_rgba(1, 1, 0.95, flash); cr.paint()
    if fade > 0: cr.set_source_rgba(0, 0, 0, fade); cr.paint()
    return s
