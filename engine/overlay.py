from PIL import Image, ImageDraw, ImageFont, ImageFilter
BI='/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf'; B='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
def make(path, part, sub=None):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0))
    items=[("The Lion",BI,92,360,(246,232,190)),("and the Mouse",BI,92,470,(246,232,190)),("Tales from the Olive Tree",B,40,545,(201,210,160)),
           (f"Part {part} of 2",B,58,1470,(246,232,190))]
    if sub: items.append((sub,B,40,1555,(225,222,215)))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ds=ImageDraw.Draw(sh); d=ImageDraw.Draw(im)
    for txt,f,sz,y,col in items:
        fnt=ImageFont.truetype(f,sz); w=d.textlength(txt,font=fnt)
        ds.text((540-w/2+4,y+4),txt,font=fnt,fill=(0,0,0,200),anchor='ls')
        d.text((540-w/2,y),txt,font=fnt,fill=col+(255,),anchor='ls')
    sh=sh.filter(ImageFilter.GaussianBlur(3)); out=Image.alpha_composite(sh,im); out.save(path)
make('out/ov1.png',1,'Part 2 on my page'); make('out/ov2.png',2)
