import requests
import sys
from gtts import gTTS
from playsound import playsound

text = sys.argv[1]


def talk(text):
  tts = gTTS(text, lang='es')
  tts.save('engine/audio/talk.mp3')
  playsound('engine/audio/talk.mp3')
  return "success"

print(talk(text))
sys.stdout.flush()
