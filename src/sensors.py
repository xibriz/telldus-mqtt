#!/usr/bin/python
# coding: utf-8

import urllib2
import json
import ConfigParser
import os
import paho.mqtt.publish as publish
from requests_oauthlib import OAuth1Session
import codecs

class Sensors:

	def __init__(self, config_file):
		config = ConfigParser.RawConfigParser()
		config.readfp(codecs.open(config_file, 'r', 'utf8'))

		self.mqtt_ip = config.get('MQTT', 'ip')
		self.mqtt_port = config.getint('MQTT', 'port')
		self.topic_pub = config.get('MQTT', 'sensor_pub')

		self.telldus_url = config.get('Telldus', 'url')
		self.telldus_public_key = config.get('Telldus', 'public_key')
		self.telldus_private_key = config.get('Telldus', 'private_key')
		self.telldus_token = config.get('Telldus', 'token')
		self.telldus_token_secret = config.get('Telldus', 'token_secret')

		self.get_sensors()

	def get_sensors(self):
		telldus = OAuth1Session(self.telldus_public_key, client_secret=self.telldus_private_key, resource_owner_key=self.telldus_token, resource_owner_secret=self.telldus_token_secret)
		url = '{}/json/sensors/list?includeValues=1&includeIgnored=0&includeScale=1'.format(self.telldus_url)
		r = telldus.get(url)

		sensors = r.json()

		for sensor in sensors['sensor']:
			for data in sensor['data']:
				try:
					sensor_name = sensor['name'].replace(" ", "")
				except AttributeError:
					sensor_name = "Unknown"
				sensor_type = data['name']
				sensor_value = data['value']
				try:
					publish.single(self.topic_pub.format(sensor_name=sensor_name, sensor_type=sensor_type), sensor_value, hostname=self.mqtt_ip, port=self.mqtt_port)
				except:
					pass
