# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random

# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 200

# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
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

wait = 1

# define desired triplet array

# define current triplet array

def poxey(wait):
   for i in range(num_pixels):  # start, stop, range
      pixels[i] = wheel(random.randrange(0,255,25))
#	desired triplet array = rand
      pixels.show()
#      time.sleep(wait)


# global verables

# brightness			= desired brightness
# CURRENT_brightness		= current brightness
# num_pixels			= number of pixels in the array

def compute_step(target,current,steps):
   return ((target[0]-current[0])/steps,(target[1]-pixel[1])/steps,(target[2]-pixel[2])/steps)

def bound(value):
   min(255,max(0,int(value)))

def fade(wait):
    steps = wait*30
    pixelSteps = [compute_step( (random.randint(0,255) ,random.randint(0,255),random.randint(0,255)),pixel,wait) for pixel in pixels]
    print(pixelSteps)
    for i in range(len(pixels)):
        pixels[i]=(bound(pixels[i][0]+pixelSteps[i][0]), bound(pixels[i][1]+pixelSteps[i][1]),bound(pixels[i][2]+pixelSteps[i][2]))
        print(pixels)
        time.sleep(1/30)
        pixels.show()
# off(1)

poxey(1)

fade(1)
