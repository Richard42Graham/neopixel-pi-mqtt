import time
import board
import neopixel
import paho.mqtt.client as mqtt
import multiprocessing
import random

def off(wait):
    steps = wait*30
    pixelSteps = [(pixel[0]/steps,pixel[1]/steps,pixel[2]/steps) for pixel in pixels]
    while True:
        for i in range(len(pixels)):
            pixels[i]=(max(0,int(pixels[i][0]-pixelSteps[i][0])), max(0,int(pixels[i][1]-pixelSteps[i][1])),max(0,int(pixels[i][2]-pixelSteps[i][2])))
        time.sleep(1/30)

def white():
    pixels.fill((255,255,255))
    print("white")
 
def wheel(pos):
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

def poxey(wait):
   for i in range(num_pixels):	# start, stop, range
      pixels[i] = wheel(random.randrange(0,255,25))
      pixels.show()
      time.sleep(wait)

commands = {
  "poxey":{
      "func":poxey,
      "args":[float]
  },
  "off":{
     "func":off,
     "args":[int]
   },
   "white":{
     "func":white,
     "args":[]
   }
}

mqttc = mqtt.Client()
mqttc.connect("192.168.1.5")
mqttc.subscribe("test/")
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
# The number of NeoPixels
num_pixels = 200
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

class Pixels():
    def __init__(self,data):
       self.data = data
    def __getitem__(self, key):
        self.__check_key__(key)
        return (self.data[key*3],self.data[key*3+1],self.data[key*3+2])
    def __setitem__(self, key, value):
        self.__check_key__(key)
        self.data[key*3] = value[0]
        self.data[key*3+1] = value[1]
        self.data[key*3+2] = value[2]
    def __len__(self):
        return int(len(self.data)/3)
    def __check_key__(self,key):
        if not isinstance(key,int):
            raise TypeError('must be an int')
        if key >= len(self.data)/3 or key < 0:
            raise IndexError("out of bounds")
    def show(self):
        show_lock.acquire()
        show_lock.release()
    def fill(self,val):
        for i in range(len(self)):
            self[i]=val
    def __iter__(self):
        return PixelsIter(self)

class PixelsIter():
    def __init__(self,pixels):
        self.__pixels = pixels
        self.__index=0
    def __next__(self):
        print(self.__index)
        if self.__index < len(self.__pixels):
            val = self.__pixels[self.__index]
        else:
            raise StopIteration
        self.__index=self.__index+1
        return val

data_array = multiprocessing.Array('i',num_pixels*3)

#global variable to store pixels in thread
pixels = None
# setup thread globals
def process_starter(array,func,args):
    global pixels
    pixels = Pixels(array)
    func(*args)

show_lock = multiprocessing.Lock()

current_thread = None
# start a thread with args
def startThread(func,args):
    global current_thread
    thread = multiprocessing.Process(target=process_starter,args=(data_array,func,args))
    if current_thread:
        current_thread.terminate()
    current_thread = thread
    thread.start()

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
    cmd,args = message.payload.decode().split(":")
    args = args.split(',')
    commands_type = commands[cmd]
    startThread(commands_type["func"],[commands_type["args"][i](args[i]) for i in range(len(commands_type["args"]))])

def __main__():
    neo_pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
    pixels = Pixels(data_array)
    startThread(poxey,[0.1])
    mqttc.on_message = on_message
    mqttc.loop_start()
    while True:
        for i in range(num_pixels):
            neo_pixels[i] = pixels[i]
        neo_pixels.show()
        show_lock.release()
        show_lock.acquire(block=False)
        time.sleep(1/30)

if __name__ == "__main__":
    __main__()