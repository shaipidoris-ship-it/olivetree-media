import sys, os, subprocess, importlib, time
mod, fn = sys.argv[1], sys.argv[2]
S = getattr(importlib.import_module(mod), fn)()
FPS = 24; n = int(round(S.length*FPS)); out = f'out/{fn}.mp4'; tmp = f'out/tmp_{fn}.mp4'
os.makedirs('out', exist_ok=True)
ff = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgra','-s','1920x1080','-r',str(FPS),'-i','-',
                       '-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-r',str(FPS), tmp], stdin=subprocess.PIPE)
t0 = time.time()
for i in range(n):
    s = S.render(i/FPS); ff.stdin.write(bytes(s.get_data()))
    if i % 240 == 0: print(fn, i, n, round(time.time()-t0, 1), flush=True)
ff.stdin.close(); rc = ff.wait()
if rc == 0: os.replace(tmp, out)
print(fn, 'done', rc, round(time.time()-t0, 1), flush=True)
