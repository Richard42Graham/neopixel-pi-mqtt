import paho.mqtt.publish as publish

publish.single("test/", "wippy whooo", hostname="192.168.1.5")
