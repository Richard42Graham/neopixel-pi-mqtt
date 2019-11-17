# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 200

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)




# global verables

# brightness			= desired brightness
# CURRENT_brightness		= current brightness
# num_pixels			= number of pixels in the array


def off(wait):
    pixels.fill((255,255,255))
    steps = wait*30
    pixelSteps = [(pixel[0]/steps,pixel[1]/steps,pixel[2]/steps) for pixel in pixels]
    print(pixelSteps)
    while True:
        for i in range(len(pixels)):
            pixels[i]=(max(0,int(pixels[i][0]-pixelSteps[i][0])), max(0,int(pixels[i][1]-pixelSteps[i][1])),max(0,int(pixels[i][2]-pixelSteps[i][2])))
        print(pixels)
        time.sleep(1/30)
off(1)
