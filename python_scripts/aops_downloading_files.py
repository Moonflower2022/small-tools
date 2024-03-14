from pyautogui import *
import pyautogui
import time
#import keyboard
import numpy
import random
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller

mouse = Controller()
keyboard = Controller()
running = True
number = 1

# for in game action use these integrated functions that simulate human behaviour
# otherwise, use original functions


def click(x, y):
    mouse.position = (x, y)
    mouse.press(Button.left)
    time.sleep(numpy.random.uniform(0.1, 0.3))
    mouse.release(Button.left)

# for moving the mouse to the right onto the next week, 108 is for 12 weeks in class
# in order to find, use pyautogui.displayMousePosition()
# to find x values of the centers of the week buttons.

# example:
# X:  630 Y:  482 RGB: (255, 255, 255)
# X:  522 Y:  481 RGB: (102, 102, 102)
# X:  413 Y:  479 RGB: (255, 255, 255)

# diff is around 108 or 109 so thats the value


xIncrement = 51
mousePos = None
time.sleep(10)

for i in range(22):
    # save mouse pos
    mousePos = mouse.position
    # print (preset to download pdf)
    time.sleep(3)
    pyautogui.hotkey('command', 'p')
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(3)

    # enter name
    pyautogui.typewrite('Week ' + str(number), interval=0.25)
    pyautogui.hotkey('enter')
    
    # increment number for naming purposes
    number = number + 1
    # go back to where we were
    mouse.position = mousePos
    mouse.move(xIncrement, 0)
    time.sleep(0.5)
    # click on the next week
    mouse.click(Button.left, 1)
    time.sleep(0.5)
