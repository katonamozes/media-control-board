# ============================================================
#  Media Control Board — CircuitPython firmware
#  Hardware: Seeed XIAO RP2040
#
#  Pin Map
#  -------
#  D1  → SK6812MINI-E data (4 LEDs, RGBW)
#  D2  → OLED SCL  (I2C)
#  D3  → OLED SDA  (I2C)
#  D4  → Encoder CLK  (A)
#  D5  → Encoder DT   (B)   ← second encoder pin, use next free pin
#  D6  → Encoder push-button  (Mute)
#  D7  → Key: Scroll Right
#  D8  → Key: Next Track
#  D9  → Key: Pause / Play
#  D10 → Key: Previous Track
#  GP11→ Key: Scroll Left   (NOTE: board label "11", access via board.GP11)
#
#  Required CircuitPython libraries (copy to /lib on CIRCUITPY):
#    adafruit_hid            (folder)
#    adafruit_debouncer.mpy
#    adafruit_displayio_ssd1306.mpy
#    adafruit_display_text   (folder)
#    neopixel.mpy
# ============================================================

import time
import board
import busio
import digitalio
import rotaryio
import displayio
import terminalio
import neopixel
import usb_hid

from adafruit_debouncer import Debouncer
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


# ── HID devices ────────────────────────────────────────────
consumer = ConsumerControl(usb_hid.devices)
keyboard  = Keyboard(usb_hid.devices)


# ── Helper: build a debounced button from a pin ────────────
def make_btn(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    return Debouncer(io)


# ── Buttons ────────────────────────────────────────────────
btn_prev   = make_btn(board.D10)   # Previous track
btn_next   = make_btn(board.D8)    # Next track
btn_pause  = make_btn(board.D9)    # Play / Pause
btn_scrR   = make_btn(board.D7)    # Scroll Right
btn_mute   = make_btn(board.D6)    # Mute (encoder push)

# Pin GP11 is the RP2040 GPIO11; it isn't labeled on the XIAO
# silkscreen past D10, but can still be used.
btn_scrL   = make_btn(board.GP11)  # Scroll Left

all_buttons = (btn_prev, btn_next, btn_pause, btn_scrR, btn_scrL, btn_mute)


# ── Rotary encoder ──────────────────────────────────────────
# D4 = CLK (A), D5 = DT (B)
encoder = rotaryio.IncrementalEncoder(board.D4, board.D5)
last_enc_pos = encoder.position


# ── SK6812MINI-E RGB LEDs (RGBW NeoPixels) ─────────────────
NUM_LEDS = 4
pixels = neopixel.NeoPixel(
    board.D1, NUM_LEDS,
    pixel_order=neopixel.GRBW,
    brightness=0.25,
    auto_write=False,
)

# Colour palette  (R, G, B, W)
C_IDLE    = (0,   0,   0,  20)   # soft white
C_PLAY    = (0,  80,   0,   0)   # green
C_PAUSE   = (80, 60,   0,   0)   # amber
C_PREV    = (0,   0, 100,   0)   # blue
C_NEXT    = (0,  80,  80,   0)   # cyan
C_MUTE    = (100, 0,   0,   0)   # red
C_UNMUTE  = (0,   0,   0,  20)   # back to white
C_VOL     = (80, 40,   0,   0)   # orange
C_SCROLL  = (60,  0, 100,   0)   # purple


def set_leds(color):
    pixels.fill(color)
    pixels.show()


# ── OLED display (SSD1306, 128×32) ─────────────────────────
displayio.release_displays()
i2c = busio.I2C(scl=board.D2, sda=board.D3, frequency=400_000)
disp_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(disp_bus, width=128, height=32)

splash = displayio.Group()
display.root_group = splash

lbl_top = label.Label(terminalio.FONT, text="Media Control", color=0xFFFFFF, x=4, y=8)
lbl_bot = label.Label(terminalio.FONT, text="Ready",         color=0xFFFFFF, x=4, y=22)
splash.append(lbl_top)
splash.append(lbl_bot)


def update_display(top: str, bottom: str):
    lbl_top.text = top
    lbl_bot.text = bottom


# ── Volume bar helper ───────────────────────────────────────
VOL_STEPS = 16   # bar characters

def vol_bar(level: int) -> str:
    """Return a simple ASCII progress bar for volume 0-100."""
    filled = round(level / 100 * VOL_STEPS)
    return "[" + "█" * filled + "░" * (VOL_STEPS - filled) + "]"


# ── State ───────────────────────────────────────────────────
muted        = False
vol_virtual  = 50        # 0-100, local tracking only
action_until = 0.0       # timestamp after which we revert to idle display
ACTION_TTL   = 1.5       # seconds to show action on screen


def trigger(led_color, top, bottom):
    """Flash LEDs and update display for ACTION_TTL seconds."""
    global action_until
    set_leds(led_color)
    update_display(top, bottom)
    action_until = time.monotonic() + ACTION_TTL


# ── Boot splash ─────────────────────────────────────────────
set_leds(C_IDLE)
update_display("Media Control", "    Ready  ♪")
time.sleep(0.8)


# ════════════════════════════════════════════════════════════
#  Main loop
# ════════════════════════════════════════════════════════════
while True:
    now = time.monotonic()

    # Poll all buttons
    for btn in all_buttons:
        btn.update()

    # ── Previous track ──────────────────────────────────────
    if btn_prev.fell:
        consumer.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
        trigger(C_PREV, "Previous Track", " |<< ")

    # ── Next track ──────────────────────────────────────────
    elif btn_next.fell:
        consumer.send(ConsumerControlCode.SCAN_NEXT_TRACK)
        trigger(C_NEXT, "Next Track", "  >>|")

    # ── Play / Pause ────────────────────────────────────────
    elif btn_pause.fell:
        consumer.send(ConsumerControlCode.PLAY_PAUSE)
        trigger(C_PLAY, "Play / Pause", "   ▶ / ❚❚")

    # ── Scroll Right (→ arrow) ──────────────────────────────
    elif btn_scrR.fell:
        keyboard.send(Keycode.RIGHT_ARROW)
        trigger(C_SCROLL, "Scroll", "   Right >>")

    # ── Scroll Left (← arrow) ───────────────────────────────
    elif btn_scrL.fell:
        keyboard.send(Keycode.LEFT_ARROW)
        trigger(C_SCROLL, "Scroll", "  << Left")

    # ── Mute toggle ─────────────────────────────────────────
    elif btn_mute.fell:
        muted = not muted
        consumer.send(ConsumerControlCode.MUTE)
        if muted:
            trigger(C_MUTE,   "Audio", "  🔇 Muted")
        else:
            trigger(C_UNMUTE, "Audio", "  🔊 Unmuted")

    # ── Rotary encoder → volume ─────────────────────────────
    enc_pos = encoder.position
    delta   = enc_pos - last_enc_pos
    if delta != 0:
        last_enc_pos = enc_pos
        steps = abs(delta)
        if delta > 0:
            for _ in range(steps):
                consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
            vol_virtual = min(100, vol_virtual + steps)
            direction   = "▲"
        else:
            for _ in range(steps):
                consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
            vol_virtual = max(0, vol_virtual - steps)
            direction   = "▼"

        trigger(C_VOL, f"Volume {direction} {vol_virtual}%", vol_bar(vol_virtual))

    # ── Revert to idle display after timeout ────────────────
    if action_until and now >= action_until:
        action_until = 0.0
        set_leds(C_IDLE)
        mute_indicator = " [MUTED]" if muted else ""
        update_display("Media Control", f"Ready{mute_indicator}")

    time.sleep(0.008)   # ~120 Hz polling rate
