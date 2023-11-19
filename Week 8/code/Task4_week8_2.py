import paho.mqtt.publish as publish

publish.single("/edge_device/data", "This is a message", hostname="192.168.153.132")
