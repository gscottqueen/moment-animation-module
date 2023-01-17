# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import os
import board
import displayio
from digitalio import DigitalInOut, Pull
from adafruit_matrixportal.matrix import Matrix
from adafruit_debouncer import Debouncer

SPRITESHEET_FOLDER = "/bmps"
FILENAME = "/breathe-dark-two.bmp"
DEFAULT_FRAME_DURATION = 0.20  # 100ms

# --- Display setup ---
matrix = Matrix(width=64, height=64, bit_depth=2, tile_rows=2, rotation=90, serpentine=True)
sprite_group = displayio.Group()
matrix.display.show(sprite_group)

file_list = sorted(
    [
        f
        for f in os.listdir(SPRITESHEET_FOLDER)
        if (f.endswith(".bmp") and not f.startswith("."))
    ]
)

if len(file_list) == 0:
    raise RuntimeError("No images found")

current_image = None
current_frame = 0
current_loop = 0
frame_count = 0
frame_duration = DEFAULT_FRAME_DURATION

def load_image():
    """
    Load an image as a sprite
    """
    # pylint: disable=global-statement
    global current_frame, current_loop, frame_count, frame_duration
    while sprite_group:
        sprite_group.pop()

    filename = SPRITESHEET_FOLDER + FILENAME

    # CircuitPython 7+ compatible
    bitmap = displayio.OnDiskBitmap(filename)
    sprite = displayio.TileGrid(
         bitmap,
         pixel_shader=bitmap.pixel_shader,
         tile_width=bitmap.width,
         tile_height=matrix.display.height,
    )

    sprite_group.append(sprite)

    current_frame = 0
    current_loop = 0
    frame_count = int(bitmap.height / matrix.display.height)
    frame_duration = DEFAULT_FRAME_DURATION

def advance_image():
    """
    Advance to the next image in the list and loop back at the end
    """
    # pylint: disable=global-statement
    global current_image
    if current_image is not None:
        current_image += 1
    if current_image is None or current_image >= len(file_list):
        current_image = 0
    load_image()


def advance_frame():
    """
    Advance to the next frame and loop back at the end
    """
    # pylint: disable=global-statement
    global current_frame, current_loop
    current_frame = current_frame + 1
    if current_frame >= frame_count:
        current_frame = 0
        current_loop = current_loop + 1
    sprite_group[0][0] = current_frame


advance_image()

while True:
    advance_frame()
    time.sleep(frame_duration)
