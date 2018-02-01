#!/usr/bin/python
# coding: utf-8

import os
main_base = os.path.dirname(__file__)
config_file = os.path.join(main_base, "config", "prod.cfg")

import paho.mqtt.client as mqtt
import re
import threading
from src import lights

light = lights.Lights(config_file=config_file)

base = u'^{}$'

rg_light_set = re.compile(base.format(light.topic_sub.format(light_name='(.*?)').replace('/','\\/')), re.U)
rg_light_status = re.compile(base.format(light.topic_status.format(light_name='(.*?)').replace('/','\\/')), re.U)

status_delay = 10.0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	#print("Connected with result code "+str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("telldus/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	#print(msg.topic+" "+str(msg.payload))
	m = rg_light_set.search(msg.topic)
	if m:
		name = m.group(1)
		light.set_light(name, msg.payload)

	m = rg_light_status.search(msg.topic)
	if m:
		name = m.group(1)
		light.get_light(name)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(light.mqtt_ip, light.mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
