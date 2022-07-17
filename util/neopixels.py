import time
import random
import board
import neopixel
import asyncio

ORDER = neopixel.GRB
num_pixels = 144
pixels = neopixel.NeoPixel(board.D18, num_pixels, auto_write=False, pixel_order=ORDER, brightness=0.2)


# Static Color Mode
def static(color):
    pixels.fill(color)
    pixels.show()


# Breathing Lighting Mode
def breathe(color, wait):
    # Function to fill pixels for breathing lighting
    def fill_pixels():
        pixels.fill((round(color[0] * i / 255), round(color[1] * i / 255), round(color[2] * i / 255)))
        pixels.show()
        time.sleep(wait / 1000)

    # Increase Brightness
    for i in range(255):
        fill_pixels()

    # Decrease Brightness
    for i in range(255, 0, -1):
        fill_pixels()


# Rainbow Cycle Mode (All pixels are the same color at any given time)
async def rainbow_cycle(wait):
    for i in range(255):
        pixels.fill(wheel(i))
        pixels.show()
        await asyncio.sleep(wait / 1000)


# Rainbow Wave Mode (All pixels are different colors at any given time)
async def rainbow_wave(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        await asyncio.sleep(wait / 1000)


# Sets the Entire Strip to a Random Color
def random_color():
    pixels.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    pixels.show()

# Clear Lighting
def clear():
    pixels.fill((0, 0, 0))
    pixels.show()


# Color Wheel for Rainbow Color Modes
def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)

    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)