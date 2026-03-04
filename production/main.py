import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display, TextEntry

keyboard = KMKKeyboard()

encoder_handler = EncoderHandler()

display = Display()

key_feedback = TextEntry(
    text="",
    x=16,
    y=8,
    font=None
)

display.entries.append(key_feedback)
keyboard.extensions.append(display)

def update_oled(keyboard, keycode, pressed):
    if pressed:
        key_feedback.text = f"Sent: {keycode}"
        display.update()

def OLEDKey(keycode):
    return make_key(on_press=lambda kb: update_oled(kb, keycode, True))

keyboard.col_pins = (board.GP0,board.GP1,board.GP2)
keyboard.row_pins = (board.GP6,board.GP7,board.GP8)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [OLEDKey(KC.LCTL(KC.C)), OLEDKey(KC.LCTL(KC.V)), OLEDKey(KC.LCTL(KC.X))],
    [OLEDKey(KC.LCTL(KC.Z)), OLEDKey(KC.LCTL(KC.Y)), OLEDKey(KC.LCTL(KC.F))],
    [OLEDKey(KC.LGUI), OLEDKey(KC.LGUI(KC.R)), OLEDKey(KC.LGUI(KC.LSFT(KC.S)))]
]

encoder_handler.pins = (
    board.GP10, board.GP9, board.GP4
)

encoder_handler.map = [
    (KC.VOLD, KC.VOLU, KC.MUTE)
]

if __name__ == '__main__':
    keyboard.go()