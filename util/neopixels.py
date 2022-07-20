import time
import random
import board
import neopixel
import asyncio

ORDER = neopixel.GRB
num_pixels = 144
pixels = neopixel.NeoPixel(board.D18, num_pixels, auto_write=False, pixel_order=ORDER, brightness=0.5)


# Set the brightness of the strip
def set_brightness(brightness):
    pixels.brightness = brightness
    pixels.show()

# Static Color Mode
def static(color):
    pixels.fill(color)
    pixels.show()


# Breathing Lighting Mode
async def breathe(color, wait):
    while True:
        # Increase Brightness
        for i in range(255):
            fill_pixels(color, i)
            await asyncio.sleep(wait)

        # Decrease Brightness
        for i in range(255, 0, -1):
            fill_pixels(color, i)
            await asyncio.sleep(wait)

# Gradient Color Mode
async def gradient(colors, wait):
    while True:
        for color in colors:
            for i in range(num_pixels):
                pixels[i] = (round(color[0] * i / 255), round(color[1] * i / 255), round(color[2] * i / 255))
                pixels.show()
                await asyncio.sleep(wait)


    
# Rainbow Cycle Mode (All pixels are the same color at any given time)
async def rainbow_cycle(wait):
    while True:
        for i in range(255):
            pixels.fill(wheel(i))
            pixels.show()
            await asyncio.sleep(wait)


# Rainbow Wave Mode (All pixels are different colors at any given time)
async def rainbow_wave(wait):
    while True:
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            await asyncio.sleep(wait)

# Rainbow Breathing Mode
async def rainbow_breathing(wait):
    # A matrix of colors in the rainbow
    colors = [[255, 0, 0], [255, 100, 0], [255, 255, 0], [0, 255, 0], [0, 255, 100], [0, 0, 255], [255, 0, 255], [255, 0, 100]]

    while True:
        for color in colors:
            # Increase Brightness
            for i in range(255):
                fill_pixels(color, i)
                await asyncio.sleep(wait)

            # Decrease Brightness
            for i in range(255, 0, -1):
                fill_pixels(color, i)
                await asyncio.sleep(wait)

# Sets the entire strip to a random rolor
def random_color():
    pixels.fill(wheel(random.randint(0, 255)))
    pixels.show()

# Sets each pixel to a random color
def random_pixels():
    for i in range(num_pixels):
        pixels[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
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

# Fill the strip with a color
# i = intensity
def fill_pixels(color, i):
    pixels.fill((round(color[0] * i / 255), round(color[1] * i / 255), round(color[2] * i / 255)))
    pixels.show()