import time
import board
import digitalio
import neopixel
import usb_hid

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

LED_PIN = board.GP16
NUM_LEDS = 24

ENCODER_DETENTS_PER_REV = 20
VOLUME_STEPS_TOTAL = 16
START_VOLUME_STEP = 8

SYNC_MAC_VOLUME_ON_BOOT = True

ENC_A = board.GP14
ENC_B = board.GP15
ENC_SW = board.GP13

BG = (0, 4, 18)
INDICATOR = (255, 0, 0)
TRAIL = (130, 12, 0)
MUTE_COLOUR = (255, 0, 0)

BRIGHTNESS_IDLE = 0.28
BRIGHTNESS_ACTIVE = 0.48

TRAIL_HOLD_TIME = 0.18
TRAIL_FADE_TIME = 0.45
GESTURE_TIMEOUT = 0.35
MUTE_FLASH_TIME = 0.25
BUTTON_DEBOUNCE_TIME = 0.25

ENCODER_STEPS_PER_CLICK = 4
DRAW_INTERVAL = 0.025

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=BRIGHTNESS_IDLE,
    auto_write=False
)

cc = ConsumerControl(usb_hid.devices)

a = digitalio.DigitalInOut(ENC_A)
a.direction = digitalio.Direction.INPUT
a.pull = digitalio.Pull.UP

b = digitalio.DigitalInOut(ENC_B)
b.direction = digitalio.Direction.INPUT
b.pull = digitalio.Pull.UP

sw = digitalio.DigitalInOut(ENC_SW)
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP

volume_position = START_VOLUME_STEP
muted = False

gesture_active = False
gesture_start = 0
gesture_last_direction = 1

last_move_time = time.monotonic()
last_mute_flash_time = -10.0
last_button = sw.value
last_press_time = 0
last_draw_time = 0

last_enc_state = (int(a.value) << 1) | int(b.value)
encoder_accumulator = 0

encoder_table = [
    0, -1,  1,  0,
    1,  0,  0, -1,
   -1,  0,  0,  1,
    0,  1, -1,  0
]


def volume_to_detent(v):
    scaled = (v / VOLUME_STEPS_TOTAL) * (ENCODER_DETENTS_PER_REV - 1)
    return int(round(scaled))


def detent_to_led(detent):
    scaled = (detent / (ENCODER_DETENTS_PER_REV - 1)) * (NUM_LEDS - 1)
    return int(round(scaled))


def current_led():
    return detent_to_led(volume_to_detent(volume_position))


def fade(age, fade_time):
    if age >= fade_time:
        return 0.0
    if age <= 0:
        return 1.0
    return 1.0 - (age / fade_time)


def add_colour(base, add, amount):
    return (
        min(255, base[0] + int(add[0] * amount)),
        min(255, base[1] + int(add[1] * amount)),
        min(255, base[2] + int(add[2] * amount)),
    )


def blend_colour(base, target, amount):
    return (
        int(base[0] + (target[0] - base[0]) * amount),
        int(base[1] + (target[1] - base[1]) * amount),
        int(base[2] + (target[2] - base[2]) * amount),
    )


def trail_strength():
    age = time.monotonic() - last_move_time

    if age < TRAIL_HOLD_TIME:
        return 1.0

    return fade(age - TRAIL_HOLD_TIME, TRAIL_FADE_TIME)


def smooth_brightness():
    age = time.monotonic() - last_move_time

    if age < 0.8:
        target = BRIGHTNESS_ACTIVE
    else:
        target = BRIGHTNESS_IDLE

    pixels.brightness = pixels.brightness + ((target - pixels.brightness) * 0.08)


def draw_ring():
    global gesture_active

    smooth_brightness()

    now = time.monotonic()

    if gesture_active and now - last_move_time > GESTURE_TIMEOUT + TRAIL_FADE_TIME:
        gesture_active = False

    position = current_led()
    mute_flash_amount = fade(now - last_mute_flash_time, MUTE_FLASH_TIME)
    trail_amount = trail_strength()

    for i in range(NUM_LEDS):
        if muted:
            colour = (0, 0, 0)
        else:
            colour = BG

        if not muted and gesture_active and trail_amount > 0:
            if gesture_start <= position:
                on_path = gesture_start <= i <= position
                distance = i - gesture_start
                path_length = max(1, position - gesture_start)
            else:
                on_path = position <= i <= gesture_start
                distance = gesture_start - i
                path_length = max(1, gesture_start - position)

            if on_path:
                distance_strength = 1.0 - (distance / (path_length + 1))
                amount = trail_amount * distance_strength
                colour = add_colour(colour, TRAIL, amount)

        if i == position:
            colour = INDICATOR

        if mute_flash_amount > 0:
            colour = blend_colour(colour, MUTE_COLOUR, mute_flash_amount)

        pixels[i] = colour

    pixels.show()


def volume_up():
    cc.send(ConsumerControlCode.VOLUME_INCREMENT)


def volume_down():
    cc.send(ConsumerControlCode.VOLUME_DECREMENT)


def mute():
    cc.send(ConsumerControlCode.MUTE)


def sync_mac_volume():
    if not SYNC_MAC_VOLUME_ON_BOOT:
        return

    for _ in range(VOLUME_STEPS_TOTAL + 5):
        volume_down()
        time.sleep(0.01)

    for _ in range(START_VOLUME_STEP):
        volume_up()
        time.sleep(0.01)


def boot_animation():
    pixels.brightness = BRIGHTNESS_ACTIVE

    for s in range(VOLUME_STEPS_TOTAL + 1):
        led = detent_to_led(volume_to_detent(s))

        for j in range(NUM_LEDS):
            pixels[j] = BG

        pixels[led] = INDICATOR

        if led - 1 >= 0:
            pixels[led - 1] = add_colour(BG, TRAIL, 0.7)

        if led - 2 >= 0:
            pixels[led - 2] = add_colour(BG, TRAIL, 0.35)

        pixels.show()
        time.sleep(0.018)

    pixels.brightness = BRIGHTNESS_IDLE


def move(step):
    global volume_position, last_move_time
    global gesture_active, gesture_start, gesture_last_direction
    global muted

    now = time.monotonic()

    old_led = current_led()
    new_volume = volume_position + step

    if new_volume < 0:
        new_volume = 0

    if new_volume > VOLUME_STEPS_TOTAL:
        new_volume = VOLUME_STEPS_TOTAL

    if new_volume == volume_position:
        return

    volume_position = new_volume
    new_led = current_led()

    if (not gesture_active) or (now - last_move_time > GESTURE_TIMEOUT) or (step != gesture_last_direction):
        gesture_start = old_led
        gesture_last_direction = step
        gesture_active = True

    last_move_time = now

    if muted:
        muted = False

    if step > 0:
        volume_up()
    else:
        volume_down()


def read_encoder():
    global last_enc_state, encoder_accumulator

    enc_state = (int(a.value) << 1) | int(b.value)
    index = (last_enc_state << 2) | enc_state
    movement = encoder_table[index]

    if movement != 0:
        encoder_accumulator += movement

        while encoder_accumulator >= ENCODER_STEPS_PER_CLICK:
            move(-1)
            encoder_accumulator -= ENCODER_STEPS_PER_CLICK

        while encoder_accumulator <= -ENCODER_STEPS_PER_CLICK:
            move(1)
            encoder_accumulator += ENCODER_STEPS_PER_CLICK

    last_enc_state = enc_state


def read_button():
    global last_button, last_press_time, last_mute_flash_time, muted

    button = sw.value
    now = time.monotonic()

    if last_button and not button:
        if now - last_press_time > BUTTON_DEBOUNCE_TIME:
            muted = not muted
            mute()
            last_mute_flash_time = now
            last_press_time = now

    last_button = button


print("BIG KNOB STANDARD v1.7")
print("No wraparound at min/max. Mute background off.")

sync_mac_volume()
boot_animation()
draw_ring()

while True:
    read_encoder()
    read_button()

    now = time.monotonic()

    if now - last_draw_time > DRAW_INTERVAL:
        draw_ring()
        last_draw_time = now
