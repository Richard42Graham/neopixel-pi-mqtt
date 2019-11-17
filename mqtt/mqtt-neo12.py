import time
import board
import neopixel
import paho.mqtt.client as mqtt
import multiprocessing
mqttc = mqtt.Client()
mqttc.connect("192.168.1.5")
mqttc.subscribe("test/")

# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 200

# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)
print("startedp")

def off(wait):
#    pixels.fill((255,255,255))
    steps = wait*30
    pixelSteps = [(pixel[0]/steps,pixel[1]/steps,pixel[2]/steps) for pixel in pixels]
    print(pixelSteps)
    while True:
        for i in range(len(pixels)):
            pixels[i]=(max(0,int(pixels[i][0]-pixelSteps[i][0])), max(0,int(pixels[i][1]-pixelSteps[i][1])),max(0,int(pixels[i][2]-pixelSteps[i][2])))
        time.sleep(1/30)

def white():
    pixels.fill((255,255,255))
    print("white")


class MetaContainer():
    def __delitem__(self, key):
        self.__delattr__(key)
    def __getitem__(self, key):
        return self.__getattribute__(key)
    def __setitem__(self, key, value):
        self.__setattr__(key, value)
    

def process_starter(array,func,args):


messages = {
  "off":{
     "func":off,
     "args":[int]
   },
   "white":{
     "func":white,
     "args":[]
   }
}


current_thread = None


def startThread(func,args):
    global current_thread
    thread = multiprocessing.Process(target=func,args=tuple(args))
    if current_thread:
        current_thread.terminate()
    current_thread = thread
    thread.start()
    print("started")

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    cmd,args = message.payload.decode().split(":")
    print(cmd)
    args = args.split(',')
    message_type = messages[cmd]
    print(message_type)
    startThread(message_type["func"],[message_type["args"][i](args[i]) for i in range(len(message_type["args"]))])

# global verables

# brightness                    = desired brightness
# CURRENT_brightness            = current brightness
# num_pixels                    = number of pixels in the array
startThread(white,[])

mqttc.on_message = on_message
mqttc.loop_start()

while True:
   pixels.show()
   time.sleep(1/30)
