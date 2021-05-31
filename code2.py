# Write your code here :-)
import time
import usb_hid
import board
import touchio
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer


#print(ConsumerControlCode.PLAY_PAUSE)

MODE_LAUNCH = 1
PASWORD = (0,250,250)
MODE_CLICK  = 2
COLOR_CLICK = (255,0,200)
MODE_THREE = 3
COLOR_THREE = (0,0,255)

WHITE = (255,255,255)
BLACK = (0,0,0)

CLICK_TIME = 1

# avoid race condition
time.sleep(1)

# look for touch
# touch selects mode
# mode determines which subroutine is run

# setup touch sensor
touch = touchio.TouchIn(board.TOUCH)

# setup RGB pixel
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

# setup mechanical key button
button = DigitalInOut(board.SWITCH)
button.switch_to_input(pull=Pull.DOWN)
bs = False
db = Debouncer(button)

# setup USB keyboard output
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
key_output = "Hello World!\n"

# setup USB mouse output
mouse = Mouse(usb_hid.devices)


latch = False
button_state = False
clicker_running = False
hold_running = False
prev_time = time.monotonic()
mode = MODE_CLICK
pixels.fill(COLOR_CLICK)

def process_launch():
    global mode
    if mode == MODE_LAUNCH:
        mode = MODE_CLICK
        pixels.fill(COLOR_CLICK)
    elif mode == MODE_CLICK:
        mode = MODE_THREE
        pixels.fill(COLOR_THREE)
    else:
        mode = MODE_LAUNCH
        pixels.fill(PASWORD)

    print("next mode", mode)

def next_mode():
    global db
    # on press
    if db.rose:
        pixels.fill(WHITE)
    if db.fell:
        pixels.fill(PASWORD)
        keyboard_layout.write("062609")  # ...Print the string
        keyboard.send(Keycode.ENTER, )


def process_clicker():
    global clicker_running
    global prev_time
    global db
    if db.rose:
        pixels.fill(WHITE)
    if db.fell:
        pixels.fill(COLOR_CLICK)

def process_hold():
    global hold_running
    global prev_time
    global db
    if db.rose:
        pixels.fill(WHITE)
    if db.fell:
         pixels.fill(COLOR_THREE)
         keyboard.send(Keycode.GUI, Keycode.FIVE)
         time.sleep (4)



while True:
    # cycle mode on touch
    if not touch.value:
        latch = False
    if touch.value and not latch:
        latch = True
        next_mode()
    db.update()
    # print("mode = ", mode)
    time.sleep(0.01)
    # run current mode
    if mode == MODE_CLICK:
        process_clicker()
    if mode == MODE_LAUNCH:
        process_launch()
    if mode == MODE_THREE:
        process_hold()


# Write your code here :-)
