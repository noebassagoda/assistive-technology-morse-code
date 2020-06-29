#!/usr/bin/env python
# coding: utf-8
import sys
import pdb

from gtts import gTTS
from playsound import playsound
from pynput.keyboard import Key, Controller

keyboard = Controller()

STATES_COUNT = 2  #eventually we could add more states by changing this value
                  #available states: 0 = navigation, 1 = writing

class StateHelper:
  def __init__(self):
    self.__current_state = 1
  
  @property
  def current_state(self):
    if self.__current_state == 0:
      return "nav"
    elif self.__current_state == 1:
      return "write"

  def change_state(self):
    self.__current_state = (self.__current_state + 1) % STATES_COUNT
    self.__change_state_audio()

  def process_button(self, button):
    switcher = {
      0: self.__determine_aux_button(),
      1: self.__determine_left_button(),
      2: self.__determine_right_button(),
      3: self.__determine_state_button(),
    }
    return switcher.get(button, None) 

  def __determine_left_button(self):
    if self.__current_state == 0:
      return "tab/"
    elif self.__current_state == 1:
      return "."
    elif self.__current_state == 2:
      return [0,-15]

  def __determine_right_button(self):
    if self.__current_state == 0:
      return "shift/tab/"
    elif self.__current_state == 1:
      return "-"
    elif self.__current_state == 2:
      return [0,15]
  
  def __determine_aux_button(self):
    if self.__current_state == 0:
      return "enter/"
    elif self.__current_state == 1:
      return "space/"
    elif self.__current_state == 2:
      return [15,0]
  
  def __determine_state_button(self):
    if self.__current_state == 2:
      return [-15,0]

  def __change_state_audio(self):
    if self.__current_state == 0:
      mode = "Navegar"
    elif self.__current_state == 1:
      mode = "Escritura"

    text = "Modo " + mode + " activado"
    tts = gTTS(text, lang='es')
    tts.save('audio/change_state.mp3')
    keyboard.press(Key.shift)
    playsound('audio/change_state.mp3')
