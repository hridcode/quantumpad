import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, Key
from kmk.extensions.media_keys import MediaKeys
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306
import adafruit_displayio_ssd1306

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())

encoder_handler = EncoderHandler()

keyboard.modules = [encoder_handler]

i2c_bus = busio.I2C(board.D5, board.D4)
driver = SSD1306(i2c=i2c_bus, device_address=0x3C)
display = Display(
    display=driver,
    width=128,
    height=32,
    brightness=1,
    brightness_step=0.1
)

key_feedback = TextEntry(
    text="",
    x=16,
    y=8
)

display.entries.append(key_feedback)
keyboard.extensions.append(display)

class OLEDKey(Key):
    def __init__(self, key):
        self.key = key
        
    def on_press(self, keyboard, coord_int=None):
        key_feedback.text = f"Sent: {self.key}"
        keyboard.add_key(self.key)

    def on_release(self, keyboard, coord_int=None):
        key_feedback.text = ""
        keyboard.remove_key(self.key)

keyboard.col_pins = (board.D0,board.D1,board.D2)
keyboard.row_pins = (board.D6,board.D7,board.D8)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [OLEDKey(KC.LCTL(KC.C)), OLEDKey(KC.LCTL(KC.V)), OLEDKey(KC.LCTL(KC.X)),
    OLEDKey(KC.LCTL(KC.Z)), OLEDKey(KC.LCTL(KC.Y)), OLEDKey(KC.LCTL(KC.F)),
    OLEDKey(KC.LGUI), OLEDKey(KC.LGUI(KC.R)), OLEDKey(KC.LGUI(KC.LSFT(KC.S)))]
]

encoder_handler.pins = (
    ((board.D10, board.D9, board.D3, True),)
)

encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.MUTE),)
]

if __name__ == '__main__':
    keyboard.go()