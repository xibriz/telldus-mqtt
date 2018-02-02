import urllib2
import json
import ConfigParser
import os
import paho.mqtt.publish as publish
from requests_oauthlib import OAuth1Session
import codecs

class Lights:
	lights = []

	def __init__(self, config_file):
		config = ConfigParser.RawConfigParser()
		config.readfp(codecs.open(config_file, 'r', 'utf8'))

		self.mqtt_ip = config.get('MQTT', 'ip')
		self.mqtt_port = config.getint('MQTT', 'port')
		self.topic_pub = config.get('MQTT', 'light_pub')
		self.topic_sub = config.get('MQTT', 'light_sub')
		self.topic_status = config.get('MQTT', 'light_status')

		self.telldus_url = config.get('Telldus', 'url')
		self.telldus_public_key = config.get('Telldus', 'public_key')
		self.telldus_private_key = config.get('Telldus', 'private_key')
		self.telldus_token = config.get('Telldus', 'token')
		self.telldus_token_secret = config.get('Telldus', 'token_secret')

		self.get_lights()

	def get_light(self, light_name):
		id = self.get_light_id(light_name)

		telldus = OAuth1Session(self.telldus_public_key, client_secret=self.telldus_private_key, resource_owner_key=self.telldus_token, resource_owner_secret=self.telldus_token_secret)
		url = '{}/json/device/info?id={}&supportedMethods=19'.format(self.telldus_url, id)
		r = telldus.get(url)

		device = r.json()
		state = int(device['state'])
		if state == 1:
			state = 'ON'
		elif state == 2:
			state = 'OFF'
		else:
			state = int((float(device['statevalue'])/255)*99)

		publish.single(self.topic_pub.format(light_name=device['name'].replace(" ", "")), state, hostname=self.mqtt_ip, port=self.mqtt_port)


	def get_lights(self):
		telldus = OAuth1Session(self.telldus_public_key, client_secret=self.telldus_private_key, resource_owner_key=self.telldus_token, resource_owner_secret=self.telldus_token_secret)
		url = '{}/json/devices/list?supportedMethods=19&includeIgnored=0'.format(self.telldus_url)
		r = telldus.get(url)

		self.lights = r.json()
		try:
			print self.lights['error']
			return None
		except KeyError:
			pass

		for device in self.lights['device']:
			if (device['type'] == u'group'):
				continue
			light_name = device['name'].replace(" ", "")
			state = int(device['state'])
			if state == 1:
				state = 'ON'
			elif state == 2:
				state = 'OFF'
			else:
				state = int((float(device['statevalue'])/255)*99)
			try:
				publish.single(self.topic_pub.format(light_name=light_name), state, hostname=self.mqtt_ip, port=self.mqtt_port)
			except:
				pass

	def set_light(self, light_name, state):
		id = self.get_light_id(light_name)
		if (state == 'ON'):
			url = '{}/json/device/command?id={}&method=1'.format(self.telldus_url, id)
		elif (state == 'OFF'):
			url = '{}/json/device/command?id={}&method=2'.format(self.telldus_url, id)
		else:
			state = int((float(state)/99)*255)
			url = '{}/json/device/command?id={}&method=16&value={}'.format(self.telldus_url, id, state)

		telldus = OAuth1Session(self.telldus_public_key, client_secret=self.telldus_private_key, resource_owner_key=self.telldus_token, resource_owner_secret=self.telldus_token_secret)
		r = telldus.get(url)

		self.get_light(light_name)

	def get_light_id(self, light_name):
		for device in self.lights['device']:
			if light_name == device['name'].replace(" ", ""):
				return device['id']
