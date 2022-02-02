from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from gtts import gTTS
from moviepy.editor import AudioFileClip, ImageClip
from pydub import AudioSegment
import os
import time
import sys
import re

def add_static_image_to_audio(image_path, audio_path, output_path):
    """Create and save a video file to `output_path` after 
    combining a static image that is located in `image_path` 
    with an audio file in `audio_path`"""
    # create the audio clip object
    audio_clip = AudioFileClip(audio_path)
    # create the image clip object
    image_clip = ImageClip(image_path)
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile(output_path)

__author__ = 'info-lab'
decalage = 500

if not os.path.exists("tmp"):
    os.makedirs("tmp")
list_texte_cru = [line.strip() for line in open(sys.argv[1], 'r', encoding="UTF-8")]

for i, texte_cru in enumerate(list_texte_cru):
    list_texte = texte_cru.split('|')
    print(list_texte)

    img = Image.open(sys.argv[2])
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype("rsc/AbrilFatface-Regular.ttf", 350)
    font2 = ImageFont.truetype("rsc/SCDream4.otf", 230)
    W, H = img.size
    w1, h1 = draw.textsize(list_texte[0], font=font1)
    y = len(list_texte[1].split('; ')) * -150
    draw.text(((W - w1) / 2, (H - h1) / 2 - decalage + y), list_texte[0], (255,255,255), font=font1)

    for j, texte2 in enumerate(list_texte[1].split('; ')):
        texte2 = texte2.replace('(2) ', '').replace('(3) ', '').replace('(4) ', '') 
        w2, h2 = draw.textsize(texte2, font=font2)
        draw.text(((W - w2) / 2, (H - h2) / 2 + decalage + y + 300 * j), texte2, (255,255,255), font=font2)
    
    font3 = ImageFont.truetype("rsc/SCDream4.otf", 180)
    draw.text((200, 200), str(i + 1), (255,255,255), font=font3)

    nom_scene = "tmp/__scene." + sys.argv[2].split('.')[-1]
    img.save(nom_scene)
    
    text=list_texte[0].replace('qc', 'quelque chose').replace('qn', 'quelqu\'un')
    tts = gTTS(text=text, lang='fr', slow=False)
    tts.save("tmp/__fr_audio.mp3")

    text = list_texte[1].replace('~', '뭐뭐').replace('(2) ', '').replace('(3) ', '').replace('(4) ', '')
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\[[^)]*\]', '', text)
    if len(text) <= 2 and text[-1] == '다': text = text + '아'
    tts = gTTS(text=text, lang='ko', slow=False)
    tts.save("tmp/__kr_audio.mp3")
    
    tts_fr = AudioSegment.from_mp3("tmp/__fr_audio.mp3")
    tts_kr = AudioSegment.from_mp3("tmp/__kr_audio.mp3")
    son1 = AudioSegment.from_mp3("rsc/nosound1.mp3")
    son05 = AudioSegment.from_mp3("rsc/nosound05.mp3")
    combined_sounds = son1 + tts_fr + son05 + tts_kr + son1
    combined_sounds.export("tmp/__audio.mp3", format="mp3")

    add_static_image_to_audio(nom_scene, "tmp/__audio.mp3", "tmp/__mv" + str(i) + ".mp4")

with open("tmp/__mylist.txt", "w") as f:
    for i in range(len(list_texte_cru)):
        f.write("file __mv" + str(i) + ".mp4\n")
os.system("ffmpeg -f concat -safe 0 -i tmp/__mylist.txt -c copy __resultat.mp4")