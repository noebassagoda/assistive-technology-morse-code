import time
import webbrowser

from util.buttons_helper  import ButtonsHelper
from util.state_helper    import StateHelper
from util.buttons_handler import ButtonsHandler

buttons_helper  = ButtonsHelper()
state_helper    = StateHelper()
buttons_handler = ButtonsHandler(state_helper, buttons_helper)

def main():
  while True:
    state_button = buttons_helper.state_button()
    if state_button == 1:
      state_helper.change_state()
    else:
      buttons_handler.process_buttons()

if __name__ == "__main__":
  main()
  