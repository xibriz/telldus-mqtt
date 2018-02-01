#!/usr/bin/python
# coding: utf-8

"""
Publish all sensors.
Make a cron job that runs every so often (every 5 minutes):
0/5 * * * * /usr/bin/python /path/to/publish_sensors.py
"""

import os
main_base = os.path.dirname(__file__)
config_file = os.path.join(main_base, "config", "prod.cfg")

from src import sensors

sensors.Sensors(config_file)
