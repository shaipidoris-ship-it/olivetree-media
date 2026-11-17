import sys, importlib
from PIL import Image
mod, fn = sys.argv[1], sys.argv[2]; ts = [float(x) for x in sys.argv[3:]]
S = getattr(importlib.import_module(mod), fn)()
ims = []
for t in ts:
    s = S.render(t); s.write_to_png('/tmp/st.png'); ims.append(Image.open('/tmp/st.png').convert('RGB').resize((640, 360)))
cols = 3; rows = (len(ims)+cols-1)//cols
c = Image.new('RGB', (640*cols, 360*rows))
for i, im in enumerate(ims): c.paste(im, ((i % cols)*640, (i//cols)*360))
c.save(f'cs_{fn}.png')
