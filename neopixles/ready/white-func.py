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

def poxey(wait):
   for i in range(num_pixels):  # start, stop, range
      pixels[i] = wheel(random.randrange(0,255,25))
      pixels.show()
#      time.sleep(wait)


# global verables

# brightness			= desired brightness
# CURRENT_brightness		= current brightness
# num_pixels			= number of pixels in the array


def white(wait):
    steps = wait*30
    pixelSteps = [((255-pixel[0])/steps,(255-pixel[1])/steps,(255-pixel[2])/steps) for pixel in pixels]
    print(pixelSteps)
    while True:
        for i in range(len(pixels)):
            pixels[i]=(min(255,int(pixels[i][0]+pixelSteps[i][0])), min(255,int(pixels[i][1]+pixelSteps[i][1])),min(255,int(pixels[i][2]+pixelSteps[i][2])))
        print(pixels)
        time.sleep(1/30)
        pixels.show()
# off(1)

# poxey(1)
white(4)
