# Big Knob Standard

A Raspberry Pi Pico 2 USB volume knob using CircuitPython, an EC11 rotary encoder, and a 24 LED WS2812 / NeoPixel ring.

---

# Features

* Volume Up / Down
* Mute / Unmute
* USB HID Media Controller
* 24 LED Ring
* Blue ambient glow
* Red active position LED
* Dynamic tracer effect
* Mute mode (background off)
* Boot animation

Works on:

* macOS
* Windows
* Linux
* Raspberry Pi OS

---

# Hardware Required

## Components

* Raspberry Pi Pico 2
* EC11 Rotary Encoder with Push Button
* WS2812 / NeoPixel 24 LED Ring
* USB Cable

---

# Wiring

## EC11 Encoder

| EC11    | Pico 2 |
| ------- | ------ |
| CLK / A | GP14   |
| DT / B  | GP15   |
| SW      | GP13   |
| GND     | GND    |

## LED Ring

| WS2812 Ring | Pico 2 |
| ----------- | ------ |
| 5V          | VBUS   |
| GND         | GND    |
| DIN         | GP16   |

---

# Installing CircuitPython

## Download CircuitPython

Go to:

https://circuitpython.org/board/raspberry_pi_pico2/

Download the latest CircuitPython UF2 file.

---

## Put Pico Into Bootloader Mode

1. Unplug Pico.
2. Hold BOOTSEL button.
3. Plug Pico into USB.
4. Release BOOTSEL.

A drive appears:

```text
RPI-RP2
```

---

## Install CircuitPython

Drag the downloaded UF2 file onto:

```text
RPI-RP2
```

The Pico will reboot automatically.

A new drive appears:

```text
CIRCUITPY
```

You now have CircuitPython installed.

---

# Installing Mu Editor

Download Mu Editor:

https://codewith.mu/

Install it normally.

---

# First Run of Mu Editor

Open Mu Editor.

Select:

```text
Mode
```

Choose:

```text
CircuitPython
```

Click:

```text
OK
```

Mu should detect your Pico automatically.

---

# Installing Required Libraries

Download CircuitPython Library Bundle:

https://circuitpython.org/libraries

Download the bundle matching your CircuitPython version.

Extract it.

---

## Open CIRCUITPY Drive

Open:

```text
CIRCUITPY
```

You should see something like:

```text
boot_out.txt
code.py
settings.toml
```

If code.py does not exist that is fine.

---

## Create lib Folder

If not already present create:

```text
CIRCUITPY/lib
```

---

## Copy Required Libraries

From the downloaded bundle copy:

```text
neopixel.mpy
```

and

```text
adafruit_hid
```

into:

```text
CIRCUITPY/lib
```

Result:

```text
CIRCUITPY
│
├── code.py
│
└── lib
    │
    ├── neopixel.mpy
    │
    └── adafruit_hid
```

---

# Uploading The Big Knob Code

Open Mu Editor.

Delete everything currently shown.

Paste the Big Knob code.

Click:

```text
Save
```

Choose:

```text
CIRCUITPY
```

Save as:

```text
code.py
```

CircuitPython automatically runs:

```text
code.py
```

every time it is saved.

No upload button required.

No compile button required.

No flashing required.

---

# How CircuitPython Works

Unlike Arduino:

```text
Write code
Compile
Upload
Run
```

CircuitPython works like:

```text
Write code
Save code.py
Runs automatically
```

Every save instantly updates the Pico.

---

# Serial Console

To view messages:

In Mu click:

```text
Serial
```

You should see:

```text
BIG KNOB STANDARD v1.7
No wraparound at min/max.
Mute background off.
```

---

# If You Get

```text
ImportError: no module named neopixel
```

You forgot:

```text
neopixel.mpy
```

inside:

```text
CIRCUITPY/lib
```

---

# If You Get

```text
ImportError: no module named adafruit_hid
```

You forgot:

```text
adafruit_hid
```

inside:

```text
CIRCUITPY/lib
```

---

# Using The Knob

Turn clockwise:

```text
Volume Up
```

Turn anti-clockwise:

```text
Volume Down
```

Press encoder:

```text
Mute
```

Press again:

```text
Unmute
```

---

# LED Behaviour

## Normal

```text
Blue Ring
Red Position Marker
Orange Tracer
```

## Mute

```text
Background Off
Red Position Marker Remains
```

---

# Current Configuration

```python
ENCODER_DETENTS_PER_REV = 20
VOLUME_STEPS_TOTAL = 16
START_VOLUME_STEP = 8
```

This matches:

```text
20 Detent EC11
16 macOS HID Volume Steps
24 LED Ring
```

---

# Stable Baseline

```text
Big Knob Standard v1.7

Pico 2
CircuitPython
EC11 Encoder
24 LED WS2812 Ring

Volume
Mute

Blue Ambient Ring
Red Position Marker
Dynamic Tracer
Mute Background Off
```
