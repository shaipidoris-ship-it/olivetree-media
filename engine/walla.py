import numpy as np, soundfile as sf, random
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/tts/kokoro.onnx','/home/claude/tts/voices.bin'); SR=24000
vs=['af_bella','am_adam','af_nicole','am_eric','bf_alice','am_liam','af_sarah','bm_lewis','af_river','am_michael']
def crowd(text, n=8, spread=0.5, name='x', pitch=(0.9,1.3)):
    rnd=random.Random(name); out=np.zeros(int(SR*6))
    for i in range(n):
        a,_=k.create(rnd.choice(text) if isinstance(text,list) else text, voice=vs[i%len(vs)], speed=rnd.uniform(0.9,1.2), lang='en-us')
        pf=rnd.uniform(*pitch); m=int(len(a)/pf); a=np.interp(np.linspace(0,len(a)-1,m),np.arange(len(a)),a)
        s=int(rnd.uniform(0,spread)*SR); out[s:s+len(a)]+=a*rnd.uniform(0.35,0.6)
    idx=np.where(np.abs(out)>0.01)[0]; out=out[:idx[-1]+2400]; out=out/np.max(np.abs(out))*0.8
    sf.write(f'vo/{name}.wav',out,SR); print(name, round(len(out)/SR,2))
crowd(["Ha ha ha!","Ha ha!","Hah hah ha ha!","Ho ho ho!"], 9, 0.4, 'crowd_laugh')
crowd(["Ohhh!","Oh!","Whoa!"], 8, 0.25, 'crowd_gasp')
crowd(["Hooray!","Yay!","Woo hoo!","Hooray for Chelona!","Bravo!"], 10, 0.6, 'crowd_cheer')
crowd(["Yay!","Woo!","Wow!"], 7, 0.3, 'crowd_yay')
crowd("Ooooooooh!", 3, 0.08, 'sparrows_ooh', pitch=(1.25,1.4))
