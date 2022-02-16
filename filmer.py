import os
import time
import sys

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from gtts import gTTS
from moviepy.editor import AudioFileClip, ImageClip
from pydub import AudioSegment

__author__ = 'info-lab'

def gommer(_texte, _stopwords : list):
    for stopword in _stopwords:
        _texte = _texte.replace(stopword, '')
    return _texte

def remplacer(_texte,  _stopwords : list):
    for stopword in _stopwords:
        _texte = _texte.replace(stopword[0], stopword[1])
    return _texte

def effacer_parentheses(_texte):
    str = ''
    b = True
    for i in range(len(_texte)):
        if _texte[i] == '(' or _texte[i] == '[':
            b = False
        if _texte[i] == ')' or _texte[i] == ']':
            b = True
            continue
        if b:
            str += _texte[i]
    return str

CHEMIN_TMP = "tmp/"
LANGUE_DEPARTURE = sys.argv[1]
NOM_FICHIER_IMAGE = sys.argv[3]
NOM_FICHIER_AUDIO = "audio.mp3"

def ecrire_en_image(_n, _texte1, _texte2):
    font1 = ImageFont.truetype("rsc/AbrilFatface-Regular.ttf", 330)
    font2 = ImageFont.truetype("rsc/SCDream4.otf", 200)
    font3 = ImageFont.truetype("rsc/SCDream4.otf", 180)
    image = Image.open(NOM_FICHIER_IMAGE)
    depeindre = ImageDraw.Draw(image)
    
    decalage = 500
    y = len(_texte2.split('; ')) * -150
    l, h = image.size
    l1, h1 = depeindre.textsize(_texte1, font=font1)
    depeindre.text(((l - l1) / 2, (h - h1) / 2 - decalage + y), _texte1, (255, 255, 255), font=font1)

    for i, _texte2 in enumerate(_texte2.split('; ')):
        l2, h2 = depeindre.textsize(_texte2, font=font2)
        depeindre.text(((l - l2) / 2, (h - h2) / 2 + decalage + y + 300 * i), _texte2, (255, 255, 255), font=font2)
    depeindre.text((200, 200), str(_n + 1), (255, 255, 255), font=font3)

    image.save(CHEMIN_TMP + NOM_FICHIER_IMAGE)

def faire_audio(_texte1, _texte2):
    gTTS(text=_texte1, lang=LANGUE_DEPARTURE, slow=False).save(CHEMIN_TMP + "audio1.mp3")
    gTTS(text=_texte2, lang='ko', slow=False).save(CHEMIN_TMP + "audio2.mp3")

    tts1 = AudioSegment.from_mp3(CHEMIN_TMP + "audio1.mp3")
    tts2 = AudioSegment.from_mp3(CHEMIN_TMP + "audio2.mp3")
    son1 = AudioSegment.from_mp3("rsc/nosound1.mp3")
    son05 = AudioSegment.from_mp3("rsc/nosound05.mp3")
    son_combine = son1 + tts1 + son05 + tts2 + son1
    time.sleep(0.5)
    son_combine.export(CHEMIN_TMP + NOM_FICHIER_AUDIO, format="mp3")

def ajouter_image_statique_a_audio(_chemin_image, _chemin_audio, _chemin_output):
    clip_image = ImageClip(_chemin_image)
    clip_audio = AudioFileClip(_chemin_audio)
    clip_video = clip_image.set_audio(clip_audio)
    clip_video.duration = clip_audio.duration
    clip_video.fps = 1
    clip_video.write_videofile(_chemin_output)


if not os.path.exists("tmp"):
    os.makedirs("tmp")
list_texte_cru = [line.strip() for line in open(sys.argv[2], 'r', encoding="UTF-8")]

for i, texte_cru in enumerate(list_texte_cru):
    list_texte = texte_cru.split('|')
    print(list_texte)
    texte1, texte2 = list_texte[0], list_texte[1]
    texte2 = gommer(texte2, ['(2) ', '(3) ', '(4) '])
    texte2 = remplacer(texte2, [('~을', '~를'), ('~과', '~와'), ('~이', '~가'), ('~은', '~는')])

    if "fr" == LANGUE_DEPARTURE:
        texte1_tts = effacer_parentheses(remplacer(texte1, [(' qc', ' quelque chose'), (' qn', ' quelqu\'un')]))
    elif "en" == LANGUE_DEPARTURE:
        texte1_tts = effacer_parentheses(texte1)
    else:
        raise Exception()
    texte2_tts = effacer_parentheses(remplacer(texte2, [('~', '뭐뭐')]))
    if len(texte2_tts) <= 2 and texte2_tts[-1] == '다':
        texte2_tts = texte2_tts + '아'

    ecrire_en_image(i, texte1, texte2)
    faire_audio(texte1_tts, texte2_tts)

    time.sleep(0.5)
    ajouter_image_statique_a_audio(
        CHEMIN_TMP + NOM_FICHIER_IMAGE, 
        CHEMIN_TMP + NOM_FICHIER_AUDIO, 
        CHEMIN_TMP + "mv" + str(i) + ".mp4")

with open(CHEMIN_TMP + "mylist.txt", "w") as f:
    for i in range(len(list_texte_cru)):
        f.write("file mv" + str(i) + ".mp4\n")
os.system("ffmpeg -f concat -safe 0 -i " + CHEMIN_TMP + "mylist.txt -c copy " + sys.argv[2].split('.')[0] + ".mp4")