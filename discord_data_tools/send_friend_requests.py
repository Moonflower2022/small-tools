import time

usernames = [] # these come from `parse_discord_data.py`

time.sleep(3)

delay = 4

last_person = "" # can use this to start from a specified position if something goes wrong halfway through

from pynput import keyboard

keyboard_controller = keyboard.Controller()
for username in usernames[usernames.index(last_person) + 1:]:
    keyboard_controller.type(username)
    keyboard_controller.press(keyboard.Key.enter)
    keyboard_controller.release(keyboard.Key.enter)
    time.sleep(delay)
    # this is for the captcha
    keyboard_controller.press(keyboard.Key.tab)
    keyboard_controller.release(keyboard.Key.tab)
    time.sleep(delay)
    keyboard_controller.press(keyboard.Key.space)
    keyboard_controller.release(keyboard.Key.space)
    time.sleep(delay)

# potential problems:
# * some people dont accept fr's
# * halfway through, discord starts making you add the tab and space for a captcha, but idk when