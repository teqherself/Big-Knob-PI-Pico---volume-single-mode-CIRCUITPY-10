# Big Knob V1 - A Gendemik Digital Project

A Raspberry Pi Pico (2) USB volume knob using CircuitPython, an EC11 rotary encoder, and a 24 LED WS2812/NeoPixel ring.

## Features

- Turn EC11 encoder to control macOS volume
- Press encoder button to mute/unmute
- 24 LED ring visual feedback
- Blue ambient background
- Red active position LED
- Orange/red tracer effect while turning
- Mute mode turns background LEDs off and leaves the active LED lit
- Boot animation
- No Arduino HID hacks
- No Python helper script required on Mac

## Hardware

### Parts

- Raspberry Pi Pico 2
- EC11 rotary encoder with push button
- 24 LED WS2812 / NeoPixel ring
- USB cable
- Optional: knob, enclosure, diffuser

## Wiring

### WS2812 LED Ring

| LED Ring | Pico 2 |
|---|---|
| 5V | VBUS |
| GND | GND |
| DI | GP16 |

### EC11 Rotary Encoder

| EC11 | Pico 2 |
|---|---|
| A / CLK | GP14 |
| B / DT | GP15 |
| SW | GP13 |
| GND / C | GND |

## CircuitPython Setup

### 1. Install CircuitPython

Download CircuitPython for Raspberry Pi Pico 2:

https://circuitpython.org/board/raspberry_pi_pico2/

Put the Pico 2 into bootloader mode, then copy the `.uf2` file onto the `RPI-RP2` drive.

After reboot, a drive called `CIRCUITPY` should appear.

## Required Libraries

Download the CircuitPython library bundle:

https://circuitpython.org/libraries

From the bundle, copy these into:

```text
CIRCUITPY/lib/
