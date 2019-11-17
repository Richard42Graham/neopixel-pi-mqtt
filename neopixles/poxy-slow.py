# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random

pixel_pin = board.D18
num_pixels = 200
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = 0 # int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = 0 # int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = 0 # int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def pixey(wiat):
   for i in range(num_pixels):
      pixels[i] = wheel(random.randint(0,255))
      pixels.show()
      time.sleep(wait)

def poxey(wait):
   for i in range(num_pixels):	# start, stop, range
      pixels[i] = wheel(random.randrange(0,255,25))
      pixels.show()
      time.sleep(wait)

def Rando(wait):
   while True:
      pixels[ random.randint(1,(num_pixels -1)) ] = wheel(random.randint(0,255) & 255)
      pixels.show()
      time.sleep(wait)
#      time.sleep(random.randint(10,100))

while True:

#   time.sleep(1)
   poxey(0)
   Rando(random.randint(0,100))
