import paho.mqtt.client as mqtt
mqttc = mqtt.Client()
mqttc.connect("192.168.1.5")
mqttc.subscribe("test/")

def off(wait):
    print("off called")


messages = {
  "off":{
     "func":off,
     "args":[int]
   }
}




def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    cmd,args = message.payload.decode().split(":")
    print(cmd)
    args = args.split(',')
    message_type = messages[cmd]
    print(message_type)
    message_type["func"](*[message_type["args"][i](args[i]) for i in range(len(message_type["args"]))])

mqttc.on_message = on_message
mqttc.loop_forever()
