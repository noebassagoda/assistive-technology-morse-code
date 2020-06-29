# library to manage keyboard events
import sys
import time

from util.morse_helper   import MorseHelper
from util.buttons_helper import ButtonsHelper
from util.state_helper   import StateHelper

morse_helper   = MorseHelper()


class ButtonsHandler:
  def __init__(self, state_helper, buttons_helper):
    self.__buttons_helper = buttons_helper
    self.__state_helper = state_helper

  def process_buttons(self):
    pressed_button = self.__current_button()
    if pressed_button > -1:
      text = self.__button_to_char(pressed_button)
      current_state = self.__state_helper.current_state
      if current_state == "write" and text != "space/":
        text += self.__process_sequence()
      morse_helper.trigger_event(text) 

  def __button_to_char(self, button):
    return self.__state_helper.process_button(button)

  def __current_button(self):
    return self.__buttons_helper.current_button()

  def __process_sequence(self):
    sequence = ""
    init = time.time()
    while time.time() - init < morse_helper.letter_end_pause_duration:
      pressed_button = self.__current_button()
      if pressed_button > 0:
        sequence += self.__button_to_char(pressed_button)
        init = time.time()
    return sequence

