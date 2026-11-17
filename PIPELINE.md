# Tales from the Olive Tree — episode pipeline

Animated Aesop's fables for kids, narrated by Glafka the owl. Channel: Instagram @talesfromtheolivetree + YouTube (via Metricool brand id 8172743, timezone Europe/Athens).
This file is the instruction sheet for each weekly run. Episode 1 (The Tortoise and the Hare) is the reference: `engine/sc_a.py`, `sc_b.py`, `sc_c.py`.

## Setup (fresh session)
```
git clone --depth 1 https://github.com/shaipidoris-ship-it/olivetree-media /home/claude/olivetree-media
mkdir -p /home/claude/fable/vo /home/claude/tts && cp /home/claude/olivetree-media/engine/*.py /home/claude/fable/
pip install pycairo kokoro-onnx soundfile pillow numpy --break-system-packages -q
cd /home/claude/tts
curl -sSL -o kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -sSL -o voices.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```
Code paths are hard-coded to `/home/claude/fable` and `/home/claude/tts`.

## Style rules (keep consistent)
- 1920x1080, 24 fps master; flat cartoon, umber outlines (#3B2A20), gouache-like backgrounds with paper grain, Greek valley setting (olive groves, white villages, Aegean light).
- Glafka the owl opens (hollow, lamp lit) and closes (moral + "Goodnight from the Olive Tree", blows out lamp) every episode. Reuse `owl()`, `L_hollow`, `lamp()`.
- Reusable cast in `chars.py`: hare, tortoise, owl, fox, donkey, sparrows (Pip/Pim/Pio), goat, bunny, hedgehog, cat, frog. New fables need new animals: write them in the same style (flat fill + 4px umber outline, `eye()`/`mouth()` helpers, lip-sync via `Cues.mouth`).
- Voices: Kokoro TTS. Glafka = bf_emma 0.9; Lagos = am_puck; Chelona = af_heart; Alepou = bm_george; sparrows = af_nicole/af_bella/af_sky pitched up; Thanasis = am_onyx slowed. New characters: pick distinct voices (see `lines.py` VOICE table).
- English. Warm, simple language for ages 4-10. Moral said once, by Glafka, at the end. No scary or violent imagery.

## Steps
1. Pick the next fable from `episodes.md` (first unchecked). Write a short script: 6-8 scenes, total 2:30-4:00. Keep dialogue punchy.
2. Put lines in `lines.py`, run `tts.py` (and walla for crowd sounds). Durations drive scene timing.
3. Write the scenes in a new `sc_epNN.py` modelled on `sc_a/b/c.py` (Scene, shot(), campath, frame()). In kit/scene files the pose helper is `Hp(...)` — never name anything `H` (it shadows the frame height).
4. Before rendering: `still.py` contact sheets for every scene; look at them and fix framing (characters overlapping, black edges = camera outside world, too small).
5. Render scenes (`render.py module func`, two at a time), concat, `audio.py` (edit its `order` list) for the soundtrack, then the soft limiter + mux (see episode 1 history). Mix levels already tuned: background must stay ~10-15 dB under speech.
6. Reels: 9:16 1080x1920 with blurred background, title overlay (see `reel_overlay` in episode 1 notes below). Split into parts of max ~2:50 at a cliffhanger.
7. Put the reel files in `epNN/` in this repo, commit, push. Public raw URL: `https://raw.githubusercontent.com/shaipidoris-ship-it/olivetree-media/main/epNN/<file>.mp4` (check it returns 200).
8. Schedule in Metricool (createScheduledPost, blogId 8172743): YouTube Shorts, madeForKids true, isAiGeneratedContent true, category FILM_ANIMATION, public. Part 1 Saturday 19:30, Part 2 Sunday 19:30 (Europe/Athens). Instagram: only if the owner asks (he currently posts Instagram by hand).
9. Send the owner the reel files + captions (Instagram caption with max 5 hashtags) so he can review and post to Instagram, and tell him he can delete the YouTube posts in Metricool before Saturday if anything is wrong.
10. Tick the fable in `episodes.md`, commit.

## Reel overlay (episode 1)
Overlay PNG 1080x1920: title in DejaVu Serif bold italic 92px at y=360/470 ("The Tortoise" / "and the Hare"), "Tales from the Olive Tree" 40px at y=545, "Part 1 of 2" 58px at y=1470.
ffmpeg filter: `[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.18:saturation=0.8[bg];[b]scale=1240:-2,crop=1080:ih[fg];[bg][fg]overlay=0:(H-h)/2[v];[v][1:v]overlay=0:0,format=yuv420p`
