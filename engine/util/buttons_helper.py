#!/usr/bin/env python
import sys
import time

from pybot.usb4butia     import USB4Butia
from util.morse_helper   import MorseHelper

BUTTON_PORT_LEFT  = 5
BUTTON_PORT_RIGHT = 3
BUTTON_PORT_AUX   = 4
BUTTON_PORT_STATE = 6

morse_helper = MorseHelper()

class ButtonsHelper:
  def __init__(self):
    self.__robot = USB4Butia()

  def current_button(self):
    if self.__aux_button() > 0:
      return 0
    elif self.__left_button() > 0:
      return 1
    elif self.__right_button() > 0:
      return 2
    else:
      return -1

  def state_button(self):
    return self.__sense_button(BUTTON_PORT_STATE)
    # return 0
    
  def __left_button(self):
    return self.__sense_button(BUTTON_PORT_LEFT)
    # return self.__sense_button("s")
    return 0

  def __right_button(self):
    return self.__sense_button(BUTTON_PORT_RIGHT)
    # return self.__sense_button("k")
    return 0

  def __aux_button(self):
    return self.__sense_button(BUTTON_PORT_AUX)
    # return self.__sense_button("l")
    # return 0

  def __button_pressed(self, button):
    return self.__robot.getButton(button) > 0
    # return keyboard.is_pressed(button)

  def __return_after_key_up(self, button):
    while self.__button_pressed(button):
      pass
    return 1
  
  def __sense_button(self, button):
    if self.__button_pressed(button):
      return self.__return_after_key_up(button)
    else:
      return 0
