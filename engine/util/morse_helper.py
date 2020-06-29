# coding: utf-8
import sys
# library to manage keyboard events
from pynput.keyboard import Key, Controller
from playsound import playsound

keyboard = Controller()

# morse parameters
SMALLEST_TIME_UNIT = .1  # the unit of time in seconds that other duration will be multiple of
LETTER_END_DURATION_THRESHOLD = SMALLEST_TIME_UNIT * 4
LONG_PRESS_DURATION_THRESHOLD = SMALLEST_TIME_UNIT * 5

class MorseHelper:
  def __init__(self):
    self.__key_to_morse = {'a': '.-', 'b': '-...', 'c': '-.-.',
                            'd': '-..', 'e': '.', 'f': '..-.',
                            'g': '--.', 'h': '....', 'i': '..',
                            'j': '.---', 'k': '-.-', 'l': '.-..',
                            'm': '--', 'n': '-.', 'o': '---',
                            'p': '.--.', 'q': '--.-', 'r': '.-.',
                            's': '...', 't': '-', 'u': '..-',
                            'v': '...-', 'w': '.--', 'x': '-..-',
                            'y': '-.--', 'z': '--..', '0': '-----',
                            '1': '.----', '2': '..---', '3': '...--',
                            '4': '....-', '5': '.....', '6': '-....',
                            '7': '--...', '8': '---..', '9': '----.',
                            '.': '·−·−·−', ',': '−−··−−', '?': '··−−··',
                            '!': '−·−·−−', '(': '−·−−·', ')': '−·−−·−',
                            ':': '−−−···', '"': '·−··−·', '$': '···−··−',
                            '@': '·−−·−·', '-': '−····−'}
    self.__morse_to_key = {morse: letter for letter, morse in self.__key_to_morse.items()}

  @property
  def letter_end_pause_duration(self):
    return LETTER_END_DURATION_THRESHOLD
  
  @property
  def long_press_duration(self):
    return LONG_PRESS_DURATION_THRESHOLD

  def __process_keyboard_events(self, sequence):
    keys = []
    if "/" in sequence:
      keys = [key for key in sequence.split('/') if key != '']
      if len(keys) > 1 :
        with keyboard.pressed(Key.shift):
          keyboard.press(Key.tab)
      else:
        press_key = getattr(Key, keys[0])
        if keys[0] == "space":
          keyboard.press(Key.space)
          playsound('audio/morse.wav')
        elif keys[0] == "tab" :
          keyboard.press(Key.tab)
        else :
          keyboard.press(Key.enter)
    elif sequence in self.__morse_to_key:
      keyboard.press(self.__morse_to_key[sequence])
      playsound('audio/morse.wav')


  def trigger_event(self, sequence):
    self.__process_keyboard_events(sequence)

